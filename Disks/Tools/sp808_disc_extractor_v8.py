import sys
import os
import struct
import re

SECTOR_SIZE = 512
RECORD_SIZE = 32

def extract_confirmed(img_path):
    print(f"[*] Opening {img_path}...")
    file_size = os.path.getsize(img_path)
    total_sectors = file_size // SECTOR_SIZE
    
    # Create output folder
    out_dir = os.path.splitext(os.path.basename(img_path))[0] + "_extracted"
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    with open(img_path, 'rb') as f:
        # 1. SCAN FOR DIRECTORY
        # Instead of guessing Sector 2 or 51, we scan the first 1MB for "SONG" or "PAD"
        # to find the directory anchor.
        print("[*] Scanning for Directory Anchor...")
        search_window = f.read(1024 * 1024) # Read first 1MB
        
        # Pattern: "SONG" followed by alphanumeric
        match = re.search(b'SONG[0-9]', search_window)
        if not match:
            print("[!] Could not find 'SONG' signature. Trying 'PAD'...")
            match = re.search(b'PAD[0-9]', search_window)
        
        if not match:
            print("[!] CRITICAL: Could not find any file signatures in first 1MB.")
            return

        # Calculate the start of the Table
        # The match found the name, which is at offset 0 of the record.
        # We align to the nearest 32-byte boundary just to be safe.
        anchor_offset = match.start()
        directory_start = anchor_offset - (anchor_offset % 32)
        
        print(f"[+] Directory Table located at Offset {directory_start} (Sector {directory_start // 512})")
        
        # 2. PARSE THE TABLE
        f.seek(directory_start)
        
        # Scan 512 records from this point
        for i in range(512):
            entry = f.read(RECORD_SIZE)
            if not any(entry) or entry == b'\xff'*32: continue

            # --- PARSING LOGIC (Based on your Hex Dump) ---
            
            # Name: Bytes 0-11
            name_raw = entry[0:12].split(b'\x00')[0]
            try:
                name = name_raw.decode('ascii', errors='ignore').strip()
            except:
                continue

            # Start LBA: Offset 20, 4 bytes, BIG ENDIAN
            start_lba = struct.unpack('>I', entry[20:24])[0]

            # Size: Offset 24, 4 bytes, LITTLE ENDIAN
            size_sectors = struct.unpack('<I', entry[24:28])[0]

            # Validation
            if start_lba == 0 or size_sectors == 0: continue
            if start_lba >= total_sectors: continue
            
            # Print findings
            print(f"[+] Found: {name:<12} | LBA: {start_lba:<8} | Size: {size_sectors:<8} ({size_sectors*512/1024/1024:.2f} MB)")

            # --- EXTRACTION ---
            safe_name = re.sub(r'[^a-zA-Z0-9_\-]', '', name)
            # Detect extension based on name (VS2 = Song, VP0 = Pad?)
            if "VS2" in name: ext = ".vs2" 
            elif "VR1" in name: ext = ".vr1"
            else: ext = ".bin"
            
            out_fn = os.path.join(out_dir, safe_name + ext)
            
            save_pos = f.tell()
            f.seek(start_lba * SECTOR_SIZE)
            data = f.read(size_sectors * SECTOR_SIZE)
            
            with open(out_fn, 'wb') as out_f:
                out_f.write(data)
            
            f.seek(save_pos)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sp808_extract_confirmed.py <disk.img>")
    else:
        extract_confirmed(sys.argv[1])
