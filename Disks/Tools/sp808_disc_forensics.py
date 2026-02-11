import sys

def scan_headers(image_path):
    print(f"{'Sector':<8} | {'Hex Header':<32} | {'ASCII'}")
    print("-" * 65)
    
    with open(image_path, 'rb') as f:
        # Scan the first 128 sectors (The "System Area")
        for sector in range(128):
            f.seek(sector * 512)
            data = f.read(16)
            
            hex_data = data.hex(' ')
            ascii_data = "".join(chr(b) if 32 <= b <= 126 else "." for b in data)
            
            # Highlight sectors that aren't empty
            if any(b != 0 for b in data):
                print(f"{sector:<8} | {hex_data:<32} | {ascii_data}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sp808_forensics.py <disk_image.img>")
    else:
        scan_headers(sys.argv[1])
