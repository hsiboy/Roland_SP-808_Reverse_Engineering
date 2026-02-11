import sys
import os
import struct
import re

SECTOR_SIZE = 512
DOF_START_SECTOR = 2
RECORD_SIZE = 32

def extract_smart(img_path):
    print(f"[*] Smart Scanning {img_path}...")
    
    file_size = os.path.getsize(img_path)
    total_sectors = file_size // SECTOR_SIZE
    out_dir = os.path.splitext(os.path.basename(img_path))[0] + "_smart_extract"
    
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    with open(img_path, 'rb') as f:
        f.seek(DOF_START_SECTOR * SECTOR_SIZE)
        
        # Scan 256 entries
        for i in range(256):
            entry = f.read(RECORD_SIZE)
            if not any(entry) or entry == b'\xff'*32: continue

            # 1. Extract Name (First 12 bytes)
            name_raw = entry[0:12].split(b'\x00')[0]
            name = name_raw.decode('ascii', errors='ignore').strip()
            
            if len(name) < 3: continue # Ignore noise
            
            # 2. AUTO-DETECT LBA and SIZE
            # We look for two integers in the record that look like (Start, Size)
            # Valid Start LBA: > 32 (System Area) and < Total Sectors
            # Valid Size: > 0 and < Total Sectors
            
            found_lba = 0
            found_size = 0
            detected_offset = -1
            
            # Scan the record for 4-byte integers (Big Endian)
            # We skip the name area (0-11)
            for offset in range(12, 28, 1): # Scan bytes 12 to 28
                try:
                    val1 = struct.unpack('>I', entry[offset:offset+4])[0] # Potential LBA
                    val2 = struct.unpack('>I', entry[offset+4:offset+8])[0] # Potential Size
                    
                    # Logic Check: Does this pair make sense?
                    if (32 < val1 < total_sectors) and (0 < val2 < total_sectors):
                        if (val1 + val2) <= total_sectors:
                            found_lba = val1
                            found_size = val2
                            detected_offset = offset
                            break
                except:
                    continue
            
            if found_lba == 0:
                # Debug: Print the hex so we can see where the numbers are hiding
                # print(f"[?] Found Name '{name}' but no valid LBA. Hex: {entry.hex()}")
                continue

            # 3. Extract
            print(f"[+] Extracting: {name:<12} | Offset Found: {detected_offset} | LBA: {found_lba} | Size: {found_size}")
            
            safe_name = re.sub(r'[^a-zA-Z0-9_\-]', '', name)
            out_fn = os.path.join(out_dir, f"{safe_name}.rdac")
            
            save_pos = f.tell()
            f.seek(found_lba * SECTOR_SIZE)
            data = f.read(found_size * SECTOR_SIZE)
            f.seek(save_pos)
            
            with open(out_fn, 'wb') as out_f:
                out_f.write(data)

    print(f"[*] Done. Check {out_dir}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sp808_extract_smart.py <disk.img>")
    else:
        extract_smart(sys.argv[1])
