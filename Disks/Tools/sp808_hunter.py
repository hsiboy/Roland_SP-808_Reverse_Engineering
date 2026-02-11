import sys
import struct

def hunt_directory(image_path):
    print(f"[*] Hunting for Roland Directory Entries in: {image_path}")
    print(f"{'Offset':<12} | {'LBA':<8} | {'Name Found'}")
    print("-" * 40)

    with open(image_path, 'rb') as f:
        data = f.read()

    # Search every 32-byte boundary
    for i in range(0, len(data), 32):
        chunk = data[i:i+32]
        if len(chunk) < 32: break
        
        # Look for printable ASCII at the start of the block (8 chars)
        name_part = chunk[0:8]
        if all(32 <= b <= 126 for b in name_part) and name_part.strip():
            # Potential Match: Now check if the 'Size' or 'Pointer' fields make sense
            # Roland usually puts the LBA pointer at offset 20 or 24 (4 bytes)
            # We try both Little and Big Endian
            ptr_le = struct.unpack('<I', chunk[20:24])[0]
            ptr_be = struct.unpack('>I', chunk[20:24])[0]
            
            # If the pointer points to a valid part of the disk, it's a directory!
            if (0 < ptr_le < (len(data)//512)) or (0 < ptr_be < (len(data)//512)):
                name = name_part.decode('ascii').strip()
                print(f"{hex(i):<12} | {i//512:<8} | {name}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sp808_hunter.py <disk_image.img>")
    else:
        hunt_directory(sys.argv[1])
