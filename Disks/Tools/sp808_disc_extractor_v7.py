import sys
import os
import struct

# SP-808 Structure based on your Demo Disk Analysis
SECTOR_SIZE = 512
DOF_START_SECTOR = 2  # Confirmed by your "Sector 2" hex dump
RECORD_SIZE = 32      # Confirmed by the 32-byte repeating pattern

def extract_from_demo_disk(img_path):
    print(f"[*] Opening {img_path}...")
    
    # Create output folder
    out_dir = os.path.splitext(os.path.basename(img_path))[0] + "_extracted"
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    with open(img_path, 'rb') as f:
        # Jump to Sector 2 (The File Table)
        f.seek(DOF_START_SECTOR * SECTOR_SIZE)
        
        # We'll read 256 entries. 
        # In your analysis, the table is clearly visible here.
        for i in range(256):
            entry = f.read(RECORD_SIZE)
            
            # Stop if we hit an empty block (all 00s or FFs)
            if not any(entry) or entry == b'\xff'*32:
                continue

            # --- FIELD PARSING (Based on your Hex Dump) ---
            # Name: First 12 bytes (Null terminated)
            name_bytes = entry[0:12].split(b'\x00')[0]
            name = name_bytes.decode('ascii', errors='ignore').strip()
            
            # Start LBA: Offset 20 (0x14), 4 bytes, Big Endian
            start_lba = struct.unpack('>I', entry[20:24])[0]
            
            # Size (Sectors): Offset 24 (0x18), 4 bytes, Big Endian
            size_sectors = struct.unpack('>I', entry[24:28])[0]
            
            # Skip invalid entries
            if not name or start_lba == 0 or size_sectors == 0:
                continue
                
            print(f"[+] Found: {name} (LBA: {start_lba}, Size: {size_sectors})")
            
            # --- EXTRACTION ---
            save_pos = f.tell()
            
            # Jump to the data
            f.seek(start_lba * SECTOR_SIZE)
            data = f.read(size_sectors * SECTOR_SIZE)
            
            # Save the file
            # We append .rdac because this is raw encoded audio
            safe_name = "".join([c for c in name if c.isalnum() or c in '_-'])
            out_path = os.path.join(out_dir, f"{safe_name}.rdac")
            
            with open(out_path, 'wb') as out_f:
                out_f.write(data)
                
            # Return to directory table
            f.seek(save_pos)

    print(f"[*] Extraction complete. check folder: {out_dir}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sp808_extract_demo.py <disk_image.img>")
    else:
        extract_from_demo_disk(sys.argv[1])
