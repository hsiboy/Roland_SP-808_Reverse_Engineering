import sys

def find_changes(file1, file2):
    print(f"[*] Comparing {file1} and {file2}...")
    s1 = open(file1, 'rb')
    s2 = open(file2, 'rb')
    
    sector = 0
    changes_found = 0
    
    while True:
        b1 = s1.read(512)
        b2 = s2.read(512)
        
        if not b1 or not b2:
            break
            
        if b1 != b2:
            # We found a difference!
            print(f"[!] Difference at Sector (LBA): {sector} | Offset: {hex(sector * 512)}")
            changes_found += 1
            if changes_found > 20:
                print("--- Too many changes, stopping scan ---")
                break
        
        sector += 1

    s1.close()
    s2.close()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python sp808_diff.py empty_disk.img recorded_disk.img")
    else:
        find_changes(sys.argv[1], sys.argv[2])
