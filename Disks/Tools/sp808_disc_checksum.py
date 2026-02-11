import sys

def calculate_checksum(file_path):
    """Calculates a simple 8-bit or 16-bit additive checksum common in Roland gear."""
    print(f"[*] Analyzing firmware: {file_path}")
    
    with open(file_path, 'rb') as f:
        data = f.read()
    
    # Standard Roland Checksum: Sum of all bytes % 256
    chk8 = sum(data) & 0xFF
    # Alternate 16-bit Checksum
    chk16 = sum(data) & 0xFFFF
    
    print(f"[+] 8-bit Sum (Hex): {hex(chk8)}")
    print(f"[+] 16-bit Sum (Hex): {hex(chk16)}")
    print(f"[*] Total Bytes: {len(data)}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sp808_checksum.py <firmware.bin>")
    else:
        calculate_checksum(sys.argv[1])
