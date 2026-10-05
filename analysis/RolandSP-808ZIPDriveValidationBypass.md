# Roland SP-808 ZIP Drive Validation Bypass

## Executive Summary

The Roland SP-808 uses an artificial restriction to reject non-ZIP storage devices despite hardware compatibility. 
This research documents the validation mechanism and provides a patch to enable hard drive and other IDE device support.

## Key Discovery

The Edirol A6 video editor uses identical hardware (same MCU, ASIC, and IDE interface) but accepts hard drives. 
By comparing the SP-808 and A6 firmwares, I identified the specific code that enforces the ZIP-only restriction.

## Hardware Architecture

### Components
- **MCU**: Hitachi H8S/2653 (HD6432653)
  - 64KB mask ROM, 4KB RAM
  - 20MHz, 5V operation
  - Operating Mode 6 (Advanced mode)
- **IDE Controller**: EPSON SLA919F ASIC
  - Handles ATAPI communication
  - No DMA support (pins 21, 29 not connected)
- **Flash**: Sharp LH28F800SUT-70 (1MB)
  - Contains main firmware
  - Word-aligned access (A0 disconnected)

### Memory Map
```
0x000000-0x00FFFF: On-chip ROM (boot/initialization)
0x100000-0x1C0000: Firmware from external flash
0x400000-0x4FFFFF: Runtime memory space
0x403xxx: Device control registers
0x43Bxxx: Shadow registers
```

## ZIP Drive Validation Process

### 1. Initialization Sequence (from IDE trace)
```
1. Software Reset (0x08 → 0x0C to control register)
2. IDENTIFY PACKET DEVICE (0xA1 command)
3. Device returns identifier including "IOMEGA ZIP100"
4. REQUEST SENSE (0x03)
5. START/STOP UNIT (0x1B)  
6. INQUIRY (0x12)
7. MODE SENSE (0x5A) with vendor subcommand 0x2F
8. Device must respond with: 2F 5C FF D9
```

### 2. Firmware Validation Points

#### SZHC Command Table (0x71AD0)
Contains device types and command sequences:
```
SZHC
ZIP HD CD -SZHC
IOMEGA iomega
[Command entries]
```

#### Device Type Check (0x4B520)
Critical validation code:
```asm
6b 20 00 40 33 e4  ; Load device type from 0x4033E4
79 10 00 05        ; Compare with 0x05 (ZIP type)
17 70              ; Branch if not equal (reject)
```

### 3. String References
Error messages at 0x17Axxx:
- "Wrong Disk."
- "Not SP-808 Disk"
- "Format Now?"

## The Patch

### Location: 0x4B523
- **Original**: `05` (ZIP device type)
- **Patched**: `FF` (impossible value)
- **Effect**: Comparison always fails, allowing all devices

### Python Patcher Script
```python
#!/usr/bin/env python3
"""
SP-808 Firmware Patcher
Patches SP-808 firmware to accept hard drives like the A6
"""

import sys
import os
import hashlib

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 patch_sp808.py <input_firmware> <output_firmware>")
        print("Example: python3 patch_sp808.py SP8EXall.bin SP8EXall_patched.bin")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Read the firmware
    try:
        with open(input_file, 'rb') as f:
            firmware = bytearray(f.read())
        print(f"Loaded firmware: {input_file} ({len(firmware)} bytes)")
    except FileNotFoundError:
        print(f"Error: Cannot find file '{input_file}'")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    
    # Calculate checksum of original
    original_hash = hashlib.md5(firmware).hexdigest()
    print(f"Original MD5: {original_hash}")
    
    # Define patches
    patches = [
        {
            'name': 'Device Type Check',
            'offset': 0x4b523,
            'original': bytes([0x05]),
            'patch': bytes([0xFF]),
            'description': 'Changes device type comparison from 0x05 to 0xFF to allow all devices'
        }
    ]
    
    # Apply patches
    patches_applied = 0
    for patch in patches:
        offset = patch['offset']
        original = patch['original']
        new_value = patch['patch']
        
        # Verify original bytes
        if firmware[offset:offset+len(original)] != original:
            print(f"\nWarning: Patch '{patch['name']}' at 0x{offset:06x}")
            print(f"Expected: {original.hex()}")
            print(f"Found:    {firmware[offset:offset+len(original)].hex()}")
            
            response = input("Apply anyway? (y/N): ").lower()
            if response != 'y':
                print("Skipping patch")
                continue
        
        # Apply patch
        for i, byte in enumerate(new_value):
            firmware[offset + i] = byte
        
        print(f"\nApplied patch: {patch['name']}")
        print(f"Offset: 0x{offset:06x}")
        print(f"Original: {original.hex()}")
        print(f"Patched:  {new_value.hex()}")
        print(f"Description: {patch['description']}")
        patches_applied += 1
    
    if patches_applied == 0:
        print("\nNo patches were applied.")
        sys.exit(0)
    
    # Write patched firmware
    try:
        with open(output_file, 'wb') as f:
            f.write(firmware)
        print(f"\nPatched firmware written to: {output_file}")
    except Exception as e:
        print(f"Error writing file: {e}")
        sys.exit(1)
    
    # Verify patch
    patched_hash = hashlib.md5(firmware).hexdigest()
    print(f"Patched MD5: {patched_hash}")
    
    # Summary
    print("\n=== Patch Summary ===")
    print(f"Original file: {input_file}")
    print(f"Patched file: {output_file}")
    print(f"Patches applied: {patches_applied}")
    print("\nThe SP-808 should now accept hard drives and other IDE devices.")
    print("Remember to backup your original firmware before flashing!")

if __name__ == "__main__":
    main()
```

## Critical Functions and Memory Locations

### Firmware Functions
```
0x100020: init_hardware - System initialization
0x1008AC: Device status management
0x107050: VS2 filesystem handler
0x1064DE: FAT12/FAT16 implementation
0x1537F4: UI string display
0x12E8E0: Device identification (checks IOMEGA/ZIP)
```

### Device Registers
```
0x4033E4: Device type register (SP-808)
0x403462: Alternate device register (A6)
0x4225CE: Device status (frequently read)
0x43B7C3-4: Validation state shadow
```

### String Locations
```
0x171AF0: "IOMEGA  " (SP-808)
0x171AF9: "iomega  " (SP-808)  
0x177ACE: "IOMEGA  " (A6)
0x177AD7: "iomega  " (A6)
0x71AC0:  Device type list
```

## Usage Instructions

1. Extract firmware from SP-808 MIDI system exclusive files
2. Run the patcher:
   ```bash
   python3 patch_sp808.py SP8EXall.bin SP8EXall_patched.bin
   ```
3. Convert patched firmware back to MIDI format
4. Update SP-808 via MIDI
5. Connect IDE hard drive with appropriate adapter

## Technical Details

### H8S Assembly Instructions Used
```
6b xx: MOV.B @(disp,ERn),Rd
79 xx: MOV.W #xx:16,ERn
17 70: BNE (Branch if Not Equal)
5A xx: JMP @aa:24
28 xx: CMP.B #xx:8,Rd
```

### ATAPI Commands
```
0xA1: IDENTIFY PACKET DEVICE
0x03: REQUEST SENSE
0x1B: START/STOP UNIT
0x12: INQUIRY
0x5A: MODE SENSE
0x2F: Vendor-specific subcommand
```

## Acknowledgments

This research was made possible by comparing the SP-808 with the Edirol A6, which revealed that the hardware limitation was purely artificial. Special thanks to the HddGuru forum community for initial firmware investigations.

## Disclaimer

This modification is provided for educational and preservation purposes. Users should backup their original firmware before applying any patches. The authors are not responsible for any damage to equipment.
