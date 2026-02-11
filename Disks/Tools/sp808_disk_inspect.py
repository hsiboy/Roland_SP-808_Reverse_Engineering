import sys
import os

# Known Roland SP-808 / R-DAC Signatures
SIGNATURES = {
    b'SP-808': "Possible Disk Header",
    b'R-DAC': "R-DAC Audio Data Block",
    b'EFFECT__': "Effects Patch Data (.VS2)",
    b'SONG': "Song Metadata",
    b'IOMEGA': "Zip Drive Identifier String",
}

def scan_image(file_path):
    print(f"[*] Scanning image: {file_path}")
    file_size = os.path.getsize(file_path)
    
    with open(file_path, 'rb') as f:
        offset = 0
        while chunk := f.read(1024 * 1024): # Read 1MB at a time
            for sig, desc in SIGNATURES.items():
                pos = chunk.find(sig)
                if pos != -1:
                    print(f"[+] Found {desc} at Offset: {hex(offset + pos)}")
            offset += len(chunk)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sp808_inspect.py <disk_image.img>")
    else:
        scan_image(sys.argv[1])
