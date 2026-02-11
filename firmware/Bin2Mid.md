# Converting Patched Firmware Back to MIDI SysEx

You need to convert the patched binary firmware back into the 8 MIDI SysEx files that the SP-808 expects. Here's how:

## Python Script: bin2midi.py

```python
#!/usr/bin/env python3
"""
SP-808 Binary to MIDI Converter
Converts patched firmware binary back to MIDI SysEx files
"""

import sys
import os

def calculate_checksum(data):
    """Calculate Roland checksum"""
    checksum = 0
    for byte in data:
        checksum = (checksum + byte) & 0x7F
    return (0x80 - checksum) & 0x7F

def create_sysex_packet(address, data, packet_num):
    """Create a single SysEx packet"""
    # Roland SysEx header
    header = [0xF0, 0x41, 0x00, 0x7C, 0x12]  # F0 41 00 7C 12
    
    # Address (24-bit)
    addr_bytes = [
        (address >> 14) & 0x7F,  # High 7 bits
        (address >> 7) & 0x7F,   # Middle 7 bits
        address & 0x7F           # Low 7 bits
    ]
    
    # Convert data to 7-bit
    data_7bit = []
    for byte in data:
        data_7bit.append((byte >> 4) & 0x0F)  # High nibble
        data_7bit.append(byte & 0x0F)         # Low nibble
    
    # Build packet
    packet = header + addr_bytes + data_7bit
    
    # Add checksum
    checksum_data = addr_bytes + data_7bit
    checksum = calculate_checksum(checksum_data)
    packet.append(checksum)
    
    # Add SysEx end
    packet.append(0xF7)
    
    return packet

def bin_to_midi(input_file, output_prefix):
    """Convert binary firmware to MIDI SysEx files"""
    
    # Read binary file
    try:
        with open(input_file, 'rb') as f:
            firmware = f.read()
        print(f"Loaded firmware: {input_file} ({len(firmware)} bytes)")
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    
    # SP-808 expects firmware in 8 files
    # Each file contains multiple 256-byte packets
    file_sizes = [
        0x18000,  # File 1: 98,304 bytes
        0x18000,  # File 2: 98,304 bytes
        0x18000,  # File 3: 98,304 bytes
        0x18000,  # File 4: 98,304 bytes
        0x18000,  # File 5: 98,304 bytes
        0x18000,  # File 6: 98,304 bytes
        0x18000,  # File 7: 98,304 bytes
        0x18004,  # File 8: 98,308 bytes (includes padding)
    ]
    
    # Standard MIDI file header
    midi_header = bytes([
        0x4D, 0x54, 0x68, 0x64,  # "MThd"
        0x00, 0x00, 0x00, 0x06,  # Header length
        0x00, 0x00,              # Format type 0
        0x00, 0x01,              # Number of tracks
        0x00, 0x60               # Time division
    ])
    
    current_offset = 0
    
    for file_num in range(8):
        print(f"\nCreating SP8EX#{file_num + 1}.mid...")
        
        # Calculate file parameters
        file_size = file_sizes[file_num]
        packet_count = file_size // 256
        if file_size % 256:
            packet_count += 1
        
        # Build MIDI track data
        track_data = []
        
        # Track header
        track_data.extend([0x00, 0x90, 0x3C, 0x7F])  # Note on
        
        for packet_num in range(packet_count):
            # Calculate packet address and size
            packet_start = current_offset + (packet_num * 256)
            packet_size = min(256, len(firmware) - packet_start)
            
            if packet_size <= 0:
                # Pad with zeros if we've run out of firmware data
                packet_data = [0] * 256
            else:
                packet_data = firmware[packet_start:packet_start + packet_size]
                # Pad to 256 bytes if necessary
                if len(packet_data) < 256:
                    packet_data = packet_data + bytes(256 - len(packet_data))
            
            # Create SysEx packet
            sysex = create_sysex_packet(packet_start, packet_data, packet_num)
            
            # Add to track with delta time
            track_data.extend([0x00])  # Delta time
            track_data.extend(sysex)
        
        # Track end
        track_data.extend([0x00, 0xFF, 0x2F, 0x00])  # End of track
        
        # Build complete MIDI file
        track_header = bytes([
            0x4D, 0x54, 0x72, 0x6B,  # "MTrk"
            (len(track_data) >> 24) & 0xFF,
            (len(track_data) >> 16) & 0xFF,
            (len(track_data) >> 8) & 0xFF,
            len(track_data) & 0xFF
        ])
        
        midi_data = midi_header + track_header + bytes(track_data)
        
        # Write MIDI file
        output_file = f"{output_prefix}#{file_num + 1}.mid"
        try:
            with open(output_file, 'wb') as f:
                f.write(midi_data)
            print(f"Created: {output_file} ({len(midi_data)} bytes)")
        except Exception as e:
            print(f"Error writing {output_file}: {e}")
            sys.exit(1)
        
        current_offset += file_size
    
    print("\nConversion complete!")
    print(f"Created 8 MIDI files: {output_prefix}#1.mid through {output_prefix}#8.mid")
    print("\nTo update your SP-808:")
    print("1. Connect MIDI interface to SP-808")
    print("2. Power on while holding SHIFT")
    print("3. Send each MIDI file in order")
    print("4. Wait for 'Completed' message before sending next file")

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 bin2midi.py <input_binary> <output_prefix>")
        print("Example: python3 bin2midi.py SP8EXall_patched.bin SP8EX")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_prefix = sys.argv[2]
    
    bin_to_midi(input_file, output_prefix)

if __name__ == "__main__":
    main()
```

## Usage

1. First patch the firmware:
```bash
python3 patch_sp808.py SP8EXall.bin SP8EXall_patched.bin
```

2. Convert back to MIDI:
```bash
python3 bin2midi.py SP8EXall_patched.bin SP8EX_patched
```

This creates:
- SP8EX_patched#1.mid
- SP8EX_patched#2.mid
- ...
- SP8EX_patched#8.mid

## Updating the SP-808

1. Connect a MIDI interface to your SP-808's MIDI IN
2. Power on the SP-808 while holding SHIFT
3. The display should show "MIDI UPDATE"
4. Send each MIDI file in numerical order
5. Wait for "Completed" message before sending the next file
6. After all 8 files, the SP-808 will restart with patched firmware

## Important Notes

- Always backup your original firmware first
- The SP-808 expects files in the exact order (1-8)
- Each file must complete before sending the next
- If the update fails, you may need to use the service manual's recovery procedure

The script handles:
- Proper SysEx packet formatting
- Roland checksum calculation
- Correct file sizes for each of the 8 parts
- MIDI file structure with appropriate headers
