import sys
import os

def list_project_info(image_path):
    print(f"[*] Loading SP-808 Project: {image_path}")
    with open(image_path, 'rb') as f:
        # Sector 0 usually contains Disk/Project Name
        f.seek(0)
        header = f.read(512)
        
        # In Roland gear, names are often at specific offsets in the first few sectors
        # Let's look for common name locations (offsets 0x20, 0x40, etc.)
        disk_name = header[0:16].decode('ascii', errors='ignore').strip()
        print(f"[!] Disk Name: {disk_name if disk_name else 'Unnamed Project'}")
        
        # Let's scan for Pad Names (Banks A-D, 16 pads each = 64 pads)
        # These are often found in the 'Virtual Memory' map in Sectors 1-4
        print("\n[ Pad Assignment Map ]")
        print("-" * 30)
        f.seek(512) # Move to Sector 1
        map_data = f.read(4096) # Read 8 sectors of metadata
        
        # Searching for ASCII strings that look like Pad names
        for i in range(0, len(map_data), 32):
            chunk = map_data[i:i+16]
            name = "".join(chr(b) if 32 <= b <= 126 else "" for b in chunk).strip()
            if len(name) > 2:
                pad_num = (i // 32) + 1
                bank = "A" if pad_num <= 16 else "B" if pad_num <= 32 else "C" if pad_num <= 48 else "D"
                num = pad_num % 16 or 16
                print(f"Pad {bank}{num:02}: {name}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sp808_manager.py <image.img>")
    else:
        list_project_info(sys.argv[1])
