import sys
import struct
import os

def decode_structure(image_path):
    print(f"[*] Analyzing Structure of {image_path}")
    file_size = os.path.getsize(image_path)
    total_sectors = file_size // 512
    print(f"[*] Disk Size: {file_size} bytes ({total_sectors} sectors)")
    print("-" * 80)

    with open(image_path, 'rb') as f:
        # Scan the first 100 sectors for ANY string that looks like a file name
        # We look for typical SP-808 names like "SONG", "PAD", "EFFECT"
        # We start at Sector 2 (Standard Roland DOF) but scan broadly
        f.seek(512 * 2) 
        data = f.read(512 * 100)
        
        found_offset = -1
        
        # Heuristic: Find a string of 4+ uppercase chars followed by 0x00 or space
        # This locates the "Name" field.
        import re
        # Look for typical Roland names (Project, Song, Pad)
        match = re.search(b'(SONG|PAD|EFFECT|PROJECT)[A-Z0-9_]{0,8}', data)
        
        if match:
            found_offset = match.start()
            name = match.group().decode('ascii')
            print(f"[!] Found Candidate Entry: '{name}' at Offset {found_offset + (512*2)}")
            
            # Grab the 32-byte record surrounding this name
            # Assuming name is at offset 0 of the record
            start_of_record = found_offset
            record = data[start_of_record : start_of_record + 32]
            
            print(f"\nHEX DUMP (32 bytes):")
            print(" ".join(f"{b:02X}" for b in record))
            print("-" * 40)
            
            print(f"{'Offset':<8} | {'Value (Big Endian)':<20} | {'Value (Little Endian)':<20} | {'Is Valid LBA?'}")
            
            # Analyze every 4-byte window for potential pointers
            for i in range(0, 29):
                # Read 4 bytes
                chunk = record[i:i+4]
                if len(chunk) < 4: continue
                
                val_be = struct.unpack('>I', chunk)[0]
                val_le = struct.unpack('<I', chunk)[0]
                
                # Check if it makes sense as an LBA (Must be > 0 and < Total Sectors)
                valid_be = "YES" if (32 < val_be < total_sectors) else ""
                valid_le = "YES" if (32 < val_le < total_sectors) else ""
                
                # Check if it makes sense as a SIZE (Must be > 0)
                if valid_be or valid_le:
                    print(f"+{i:<7} | {val_be:<20} | {val_le:<20} | {valid_be or valid_le}")

        else:
            print("[!] Could not find any standard 'SONG' or 'PAD' strings in the first 100 sectors.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sp808_struct_decoder.py <disk.img>")
    else:
        decode_structure(sys.argv[1])
