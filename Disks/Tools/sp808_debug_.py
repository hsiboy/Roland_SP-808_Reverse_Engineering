import sys
import os
import struct

# Configuration
SECTOR_SIZE = 512
DOF_START_SECTOR = 2
RECORD_SIZE = 32

def debug_extraction(img_path):
    print(f"DEBUG: Analyzing {img_path}")
    
    if not os.path.exists(img_path):
        print("ERROR: File not found.")
        return

    file_size = os.path.getsize(img_path)
    total_sectors = file_size // SECTOR_SIZE
    print(f"DEBUG: Image Size: {file_size} bytes ({total_sectors} sectors)")

    out_dir = os.path.splitext(os.path.basename(img_path))[0] + "_debug_extract"
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    with open(img_path, 'rb') as f:
        # Move to Directory
        print(f"DEBUG: Seeking to Sector {DOF_START_SECTOR} (Offset {DOF_START_SECTOR * SECTOR_SIZE})")
        f.seek(DOF_START_SECTOR * SECTOR_SIZE)

        # Read first 20 entries for debugging (no need to scroll 256 lines of empty data)
        for i in range(20):
            offset_loc = (DOF_START_SECTOR * SECTOR_SIZE) + (i * RECORD_SIZE)
            entry = f.read(RECORD_SIZE)
            
            # RAW HEX DUMP
            hex_dump = entry.hex(' ')
            print(f"\n--- Entry {i} (Offset {hex(offset_loc)}) ---")
            print(f"HEX: {hex_dump}")

            if not any(entry) or entry == b'\xff' * 32:
                print("STATUS: Skipped (Empty/Padding)")
                continue

            # Attempt Parse
            # Name at 0x00
            name_raw = entry[0:12]
            try:
                name = name_raw.split(b'\x00')[0].decode('ascii', errors='ignore').strip()
            except:
                name = "<decode error>"
            
            # LBA at 0x14 (20)
            try:
                lba = struct.unpack('>I', entry[20:24])[0]
            except:
                lba = -1
            
            # Size at 0x18 (24)
            try:
                size = struct.unpack('>I', entry[24:28])[0]
            except:
                size = -1

            print(f"PARSED: Name='{name}' | LBA={lba} | Size={size}")

            # VALIDATION LOGIC DEBUG
            reasons = []
            if not name: reasons.append("Name is empty")
            if lba == 0: reasons.append("LBA is 0")
            if size == 0: reasons.append("Size is 0")
            if lba >= total_sectors: reasons.append(f"LBA {
