import sys

def parse_sp808_directory(image_path):
    print(f"[*] Parsing Roland Directory Table: {image_path}")
    print(f"{'Entry':<6} | {'Pad/Object Name':<20} | {'Start LBA':<10} | {'Size (Sectors)'}")
    print("-" * 60)

    with open(image_path, 'rb') as f:
        # Sector 2 is the traditional starting point for the Roland File Table
        f.seek(512 * 2) 
        
        # Scan 128 entries (standard Roland limit for these units)
        for i in range(128):
            record = f.read(32) # Standard Roland DOF entry size
            if len(record) < 32: break
            
            # The Name is usually the first 8-12 bytes
            name_raw = record[0:12].split(b'\x00')[0]
            name = name_raw.decode('ascii', errors='ignore').strip()
            
            # Pointers are usually at Offset 20 and 24 (4-byte integers)
            # We use Big Endian ('>') because of the H8S CPU
            try:
                start_lba = int.from_bytes(record[20:24], byteorder='big')
                size = int.from_bytes(record[24:28], byteorder='big')
            except:
                continue

            if name and start_lba > 0:
                print(f"{i:<6} | {name:<20} | {start_lba:<10} | {size}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sp808_directory.py <unscrambled_image.img>")
    else:
        parse_sp808_directory(sys.argv[1])
