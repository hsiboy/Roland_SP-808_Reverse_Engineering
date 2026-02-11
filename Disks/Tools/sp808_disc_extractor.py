import sys
import os
import struct

# Roland SP-808 Constants
SECTOR_SIZE = 512
DOF_START_LBA = 16    # Common for SP-808
FAT_START_LBA = 2     # Common for SP-808
RECORD_SIZE = 32      # DOF Record length

def rip_samples(img_path):
    if not os.path.exists("extracted"): os.makedirs("extracted")
    
    with open(img_path, 'rb') as f:
        print(f"[*] Parsing Directory at LBA {DOF_START_LBA}...")
        f.seek(DOF_START_LBA * SECTOR_SIZE)
        
        # Scan 1024 possible directory entries
        for i in range(1024):
            entry = f.read(RECORD_SIZE)
            if not any(entry): continue
            
            # Bytes 0-11: Name (ASCII)
            name = entry[0:12].decode('ascii', errors='ignore').strip()
            if not name: continue
            
            # Bytes 20-23: Start Sector (Big Endian)
            # Bytes 24-27: Size in Sectors (Big Endian)
            start_lba = struct.unpack('>I', entry[20:24])[0]
            size_sectors = struct.unpack('>I', entry[24:28])[0]
            
            if start_lba > 0 and size_sectors > 0:
                print(f"[+] Found Object: '{name}' | LBA: {start_lba} | Size: {size_sectors} sectors")
                
                # Extraction logic
                f.seek(start_lba * SECTOR_SIZE)
                audio_data = f.read(size_sectors * SECTOR_SIZE)
                
                output_fn = f"extracted/{name.replace(' ', '_')}.rdac"
                with open(output_fn, 'wb') as out:
                    out.write(audio_data)
                print(f"    -> Extracted to {output_fn}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sp808_extractor.py <disk.img>")
    else:
        rip_samples(sys.argv[1])
