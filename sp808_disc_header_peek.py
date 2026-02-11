import sys

def peek_signatures(image_path, target_sig):
    sig_bytes = target_sig.encode('ascii')
    print(f"[*] Searching for '{target_sig}' in {image_path}...")
    
    with open(image_path, 'rb') as f:
        content = f.read()
        
    offset = 0
    while True:
        offset = content.find(sig_bytes, offset)
        if offset == -1:
            break
            
        print(f"\n[+] Match found at {hex(offset)} (LBA: {offset // 512})")
        # Grab 64 bytes of context
        context = content[offset:offset+64]
        
        # Hex Dump
        hex_str = " ".join(f"{b:02x}" for b in context)
        # ASCII Dump
        ascii_str = "".join(chr(b) if 32 <= b <= 126 else "." for b in context)
        
        print(f"HEX:   {hex_str}")
        print(f"ASCII: {ascii_str}")
        
        offset += len(sig_bytes)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python sp808_peek.py <image.img> <signature>")
        print("Example: python sp808_peek.py disk.img RDAC")
    else:
        peek_signatures(sys.argv[1], sys.argv[2])
