import os
import struct

# SP-808 Specific Constants
SECTOR_SIZE = 512

# Signatures to look for
SIGNATURES = {
    b'SP-808': "Disk Header / Project Info",
    b'R-DAC': "Audio Data Block",
    b'EFFECT__': "Effects Patch (.VS2)",
    b'IOMEGA': "Drive ID String",
    b'RDAC': "Alternative Audio Header"
}

def analyze_image(path):
    if not os.path.exists(path):
        print(f"Error: File {path} not found.")
        return

    file_size = os.path.getsize(path)
    print(f"Analyzing: {path} ({file_size / (1024*1024):.2f} MB)")
    print("-" * 50)

    with open(path, 'rb') as f:
        # 1. Check for Standard MBR (Sector 0)
        f.seek(0)
        mbr_check = f.read(512)
        if mbr_check[510:512] == b'\x55\xAA':
            print("[!] Found standard MBR signature at Sector 0.")
        else:
            print("[?] No standard MBR. This may be a 'Superfloppy' or proprietary Roland format.")

        # 2. Signature Scan
        print("[*] Scanning for Roland signatures...")
        f.seek(0)
        chunk_size = 1024 * 1024 # 1MB chunks
        offset = 0
        
        while True:
            data = f.read(chunk_size)
            if not data:
                break
            
            for sig, desc in SIGNATURES.items():
                idx = data.find(sig)
                if idx != -1:
                    abs_offset = offset + idx
                    lba = abs_offset // SECTOR_SIZE
                    print(f"FOUND: {desc} | Offset: {hex(abs_offset)} | LBA: {lba}")
            
            offset += len(data)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python sp808_disk_tool.py <image_name.img>")
    else:
        analyze_image(sys.argv[1])
