import sys
import os
import struct
import re

# SP-808 Disk Constants
SECTOR_SIZE = 512
DOF_START_LBA = 2  # The standard start for Roland's file table
RECORD_SIZE = 32

def sanitize_filename(name):
    """
    Aggressively strips non-alphanumeric characters to prevent OS errors.
    Returns 'Unknown_Index' if the name becomes empty.
    """
    # Keep only A-Z, 0-9, and underscores
    clean = re.sub(r'[^a-zA-Z0-9_]', '', name)
    return clean if clean else "Unnamed"

def extract_samples(img_path):
    print(f"[*] Analyzing {img_path} for R-DAC audio...")
    
    # 1. Setup Output Directory
    out_dir = os.path.join(os.path.dirname(img_path), "extracted_rdac")
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    file_size = os.path.getsize(img_path)
    total_sectors = file_size // SECTOR_SIZE

    with open(img_path, 'rb') as f:
        # 2. Jump to the Directory Table
        f.seek(DOF_START_LBA * SECTOR_SIZE)
        
        # Scan 512 entries (16KB of directory data)
        for i in range(512):
            entry = f.read(RECORD_SIZE)
            if not entry or len(entry) < RECORD_SIZE: break
            
            # Check for empty records (all 0x00 or all 0xFF)
            if entry == b'\x00'*32 or entry == b'\xFF'*32:
                continue

            # 3. Parse Name (Bytes 0-11)
            raw_name = entry[0:12].split(b'\x00')[0]
            try:
                decoded_name = raw_name.decode('ascii', errors='ignore').strip()
            except:
                decoded_name = f"Entry_{i}"

            # 4. Parse Pointers (Big Endian >)
            # Offset 20 = Start LBA, Offset 24 = Length in Sectors
            try:
                start_lba = struct.unpack('>I', entry[20:24])[0]
                length_sectors = struct.unpack('>I', entry[24:28])[0]
            except:
                continue

            # 5. Sanity Checks (Filter out junk)
            if start_lba == 0 or length_sectors == 0: continue
            if start_lba >= total_sectors: continue
            
            # Filter out "System" files (usually small pointers at start of disk)
            # Real audio is usually further down (e.g., LBA > 500)
            if start_lba < 32: continue 

            # 6. Generate Safe Filename
            safe_name = sanitize_filename(decoded_name)
            filename = f"{i:03d}_{safe_name}.rdac"
            out_path = os.path.join(out_dir, filename)

            print(f"[+] Extracting: {safe_name:<16} (LBA: {start_lba}, Len: {length_sectors})")

            # 7. Extract Data
            current_pos = f.tell()
            f.seek(start_lba * SECTOR_SIZE)
            data = f.read(length_sectors * SECTOR_SIZE)
            
            with open(out_path, 'wb') as out_file:
                out_file.write(data)
            
            f.seek(current_pos)

    print(f"[*] Done. Check the '{out_dir}' folder.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sp808_extract_v3.py <disk_image.img>")
    else:
        extract_samples(sys.argv[1])
