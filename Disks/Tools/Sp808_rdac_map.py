import sys
import math

def calculate_entropy(data):
    """Calculates the Shannon entropy of a block of data."""
    if not data:
        return 0
    entropy = 0
    for x in range(256):
        p_x = data.count(x) / len(data)
        if p_x > 0:
            entropy += - p_x * math.log2(p_x)
    return entropy

def map_rdac(image_path, block_size=4096):
    print(f"[*] Mapping R-DAC patterns in {image_path}...")
    print(f"[*] Block Size: {block_size} bytes")
    print(f"{'LBA':<10} | {'Offset':<12} | {'Entropy':<8} | {'Type'}")
    print("-" * 55)

    with open(image_path, 'rb') as f:
        lba = 0
        while True:
            data = f.read(block_size)
            if not data:
                break
            
            ent = calculate_entropy(data)
            
            # R-DAC data is usually high entropy (above 7.0)
            # Empty Zip disk space is usually 0.0 or very low
            # Filesystem tables are usually medium entropy (3.0 - 5.0)
            data_type = "Empty/Padding"
            if ent > 7.2:
                data_type = "DATA (R-DAC?)"
            elif ent > 4.0:
                data_type = "Metadata/Table"
            elif b'RDAC' in data:
                data_type = "RDAC HEADER"

            if ent > 1.0: # Only print non-empty blocks
                print(f"{lba:<10} | {hex(lba*512):<12} | {ent:<8.2f} | {data_type}")
            
            lba += (block_size // 512)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sp808_rdac_map.py <image.img>")
    else:
        map_rdac(sys.argv[1])
