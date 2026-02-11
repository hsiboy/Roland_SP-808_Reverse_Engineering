import sys

def export_sectors(image_path, start_sector, num_sectors, output_file):
    SECTOR_SIZE = 512
    print(f"[*] Extracting {num_sectors} sectors starting at LBA {start_sector}...")
    
    with open(image_path, 'rb') as f_in:
        f_in.seek(start_sector * SECTOR_SIZE)
        data = f_in.read(num_sectors * SECTOR_SIZE)
        
        with open(output_file, 'wb') as f_out:
            f_out.write(data)
            
    print(f"[+] Exported to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python sp808_export.py <image.img> <start_lba> <count> <output.bin>")
    else:
        export_sectors(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])
