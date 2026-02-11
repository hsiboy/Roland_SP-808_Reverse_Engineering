import sys

GOLDEN_SUM_8 = 0x1a # Your discovered value

def patch_firmware(bin_path, out_path):
    with open(bin_path, 'rb') as f:
        data = bytearray(f.read())

    # 1. Patch the "IOMEGA" check (Example: Searching for the hex string)
    target = b'IOMEGA'
    idx = data.find(target)
    if idx != -1:
        print(f"[*] Found 'IOMEGA' at {hex(idx)}. Patching...")
        # Replace with dummy data or a wildcard
        data[idx:idx+6] = b'ZULUID'
    
    # 2. Fix the Checksum (8-bit additive)
    # We sum everything EXCEPT the very last byte, then set the last byte to match GOLDEN_SUM_8
    current_sum = sum(data[:-1]) & 0xFF
    correction = (GOLDEN_SUM_8 - current_sum) & 0xFF
    data[-1] = correction
    
    with open(out_path, 'wb') as f:
        f.write(data)
    
    print(f"[+] Patch complete. Checksum fixed to {hex(GOLDEN_SUM_8)}.")
    print(f"[+] Output saved to: {out_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python sp808_patch_and_fix.py <input.bin> <output.bin>")
    else:
        patch_firmware(sys.argv[1], sys.argv[2])
