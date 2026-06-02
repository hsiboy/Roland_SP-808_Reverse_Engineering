# SP-808 ZIP Drive Reverse Engineering Summary - December 2024

## Overview
What we know so far. 
The Roland SP-808 uses an IOMEGA ZIP drive for storage, the Roland firmware includes a validation sequence. The system uses an EPSON SLA919F ASIC to handle IDE/ATAPI interface between the MCU (H8S/2653) and the storage device.

## Hardware Architecture
- **MCU**: Hitachi H8S/2653
  - 64k ROM and 4k RAM
  - 5V with 20MHz clock
  - Operating in `Mode 6` (Advanced mode)
- **IDE Interface**: 
  - Handled by EPSON SLA919F ASIC
  - No DMA support (DDRQ and DDRACK not connected)
  - MCU communicates with ASIC rather than direct IDE control

## Key Findings

### 1. SZHC Command Table
Found in firmware at offset 0x71AD0, contains command sequence:
```
SZHC
06 00 00 00 00 00 00
06 1B 00 00 00 00 00  // START/STOP UNIT
06 1E 00 00 00 00 00  // PREVENT/ALLOW MEDIA REMOVAL
06 03 00 00 00 00 00  // REQUEST SENSE
IOMEGA  
iomega  
ZIP
06 12 00 00 00 00 00  // INQUIRY
```

### 2. Boot Sequence (from IDE bus trace)
1. IDENTIFY PACKET DEVICE (0xA1)
2. REQUEST SENSE (0x03)
3. START/STOP UNIT (0x1B)
4. INQUIRY (0x12)
5. MODE SENSE (0x5A) with validation sequence
6. MODE SELECT (0x55)
7. Vendor-specific commands

### 3. ZIP Drive Validation
Key sequence involves:
```
Command: 0x5A (MODE SENSE)
Subcommand: 0x2F
Expected Response: 2F 5C FF D9
```

### 4. Vendor-Specific Commands
From the emulator code:
```cpp
case ATAPI_CMD_VENDOR_0x06: return atapi_zip_disk_0x06(cmd);
case ATAPI_CMD_VENDOR_0x0D: return atapi_zip_disk_0x0D(cmd);
```

### 5. IDE/ATAPI Communication
- Uses non-DMA mode (programmed I/O)
- Byte count register used for transfer size
- SP-808 expects specific block sizes and timing

### 6. Critical Mode Page

The SP-808 issues `MODE SENSE (0x5A)` with vendor page code `0x2F`. The bus trace
(`Roland_SP-808_to_ZIP_Drive_sniff.md`, entries 514–517) confirms the real ZIP drive
returns exactly 4 bytes:

```
2F 5C FF D9
```

This is verified directly from the IDE bus capture. The snippet below is from a ZuluIDE
emulator attempt that returns 6 bytes with different values — **it does not match what the
real drive returns and should not be used as a reference**:

```c
// NOTE: This does NOT match the real ZIP drive response (2F 5C FF D9).
// Retained here for historical reference only.
if (page_idx == 0x2F) {
    buffer[0] = 0x2F;
    buffer[1] = 0x04;
    buffer[2] = 0x5c;
    buffer[3] = 0x0f;
    buffer[4] = 0x3c;
    buffer[5] = 0x0f;
    return 6;
}
```

The working ZuluIDE configuration (`zuluide.ini`) produces the correct `2F 5C FF D9`
response through its built-in Zip 100 emulation.

## Implications
1. The EPSON ASIC acts as a protocol translator between MCU commands and ATAPI
2. The 7-byte command structure (06 + command + 5 bytes) appears to be the ASIC's protocol
3. The ZIP drive validation is a multi-step process involving both standard ATAPI commands and vendor-specific checks
4. The system uses a specific sequence of commands during initialization that must be followed exactly

## Next Steps
1. Further analysis of the ASIC command protocol
2. Understanding vendor-specific commands (0x06, 0x0D)
3. Mapping complete initialization sequence
4. Documentation of block transfer requirements
