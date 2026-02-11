import sys

def unscramble_image(input_path, output_path):
    print(f"[*] Unscrambling: {input_path} -> {output_path}")
    
    with open(input_path, 'rb') as f_in, open(output_path, 'wb') as f_out:
        while chunk := f_in.read(2):
            if len(chunk) < 2:
                f_out.write(chunk)
                break
            # Swap the bytes in every 16-bit word
            unswapped = bytes([chunk[1], chunk[0]])
            f_out.write(unswapped)
            
    print("[+] Done. Try running 'sp808_explorer.py' on the NEW file.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python sp808_unscramble.py <input.img> <output_unscrambled.img>")
    else:
        unscramble_image(sys.argv[1], sys.argv[2])
