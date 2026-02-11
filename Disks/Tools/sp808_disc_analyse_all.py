import os
import struct
import math

# Constants
SECTOR_SIZE = 512
GOLDEN_SUM_8 = 0x1a

def get_entropy(data):
    if not data: return 0
    probs = [data.count(i)/len(data) for i in set(data)]
    return -sum(p * math.log2(p) for p in probs)

def analyze_disk(img_path):
    print(f"# SP-808 Analysis Report for {os.path.basename(img_path)}")
    print(f"| Metric | Value |")
    print(f"| :--- | :--- |")
    
    file_size = os.path.getsize(img_path)
    with open(img_path, 'rb') as f:
        data = f.read()

    # 1. Checksum & Size
    chk8 = sum(data) & 0xFF
    print(f"| Total Size | {file_size / (1024*1024):.2f} MB |")
    print(f"| 8-bit Sum | {hex(chk8)} ({'MATCH' if chk8 == GOLDEN_SUM_8 else 'MISMATCH'}) |")

    # 2. Key LBA Mapping
    print(f"\n## Found Signatures and High Entropy Blocks")
    print(f"| LBA | Offset | Type | Entropy | Preview |")
    print(f"| :--- | :--- | :--- | :--- | :--- |")
    
    # Scan every 16 sectors (8KB) for speed
    for lba in range(0, len(data)//SECTOR_SIZE, 16):
        chunk = data[lba*SECTOR_SIZE : (lba+16)*SECTOR_SIZE]
        ent = get_entropy(chunk)
        
        sig = "Unknown"
        if b'SP-808' in chunk: sig = "**DISK HEADER**"
        elif b'RDAC' in chunk: sig = "R-DAC AUDIO"
        elif b'EFFECT__' in chunk: sig = "EFFECTS"
        
        if ent > 7.0 or sig != "Unknown":
            preview = chunk[:16].hex()
            print(f"| {lba} | {hex(lba*512)} | {sig} | {ent:.2f} | `{preview}` |")

if __name__ == "__main__":
    import sys
    analyze_disk(sys.argv[1])
