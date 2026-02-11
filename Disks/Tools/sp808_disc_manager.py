import sys
import re

def deep_scan(image_path):
    print(f"[*] Deep Scanning SP-808 Image: {image_path}")
    print(f"{'Offset':<12} | {'Type':<12} | {'Name/Data'}")
    print("-" * 50)

    with open(image_path, 'rb') as f:
        data = f.read()

    # Roland names are usually 8-16 chars, often followed by 0x00 or 0x20
    # This regex looks for 4+ alphanumeric characters in a row
    name_pattern = re.compile(rb'[A-Za-z0-9\s\-_]{4,16}')

    # Keywords we are hunting for
    keywords = {
        b'SP-808': "PROJECT",
        b'SONG': "SONG",
        b'EFFECT__': "FX_PATCH",
        b'RDAC': "AUDIO_HDR"
    }

    for key, label in keywords.items():
        offset = 0
        while True:
            offset = data.find(key, offset)
            if offset == -1: break
            
            # Peek 32 bytes ahead for a name
            peek = data[offset:offset+64]
            names = name_pattern.findall(peek)
            
            # Filter out the keyword itself from the names list
            display_name = "N/A"
            for n in names:
                if n.upper() != key and len(n) > 3:
                    display_name = n.decode('ascii', errors='ignore').strip()
                    break

            print(f"{hex(offset):<12} | {label:<12} | {display_name}")
            offset += len(key)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sp808_explorer.py <image.img>")
    else:
        deep_scan(sys.argv[1])
