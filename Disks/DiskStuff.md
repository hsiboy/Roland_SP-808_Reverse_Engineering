```sh 
➜  ZIP100 SP-808 DEMO disk: file SP-808TS25E.ima 
SP-808TS25E.ima: DOS/MBR boot sector; partition 1 : ID=0x6, start-CHS (0x0,1,1), end-CHS (0xff,11,31), startsector 32, 196575 sectors, extended partition table (last)

➜  ZIP100 SP-808 DEMO disk: python ../disk_inspect.py SP-808TS25E.ima 
[*] Scanning image: SP-808TS25E.ima
[+] Found Possible Disk Header at Offset: 0x6600
[+] Found Effects Patch Data (.VS2) at Offset: 0xa640
[+] Found Song Metadata at Offset: 0x6700
[+] Found Possible Disk Header at Offset: 0x59da604
[+] Found Possible Disk Header at Offset: 0x5a0a604

➜  ZIP100 SP-808 DEMO disk: python ../disk_tool.py SP-808TS25E.ima 
Analyzing: SP-808TS25E.ima (96.00 MB)
--------------------------------------------------
[!] Found standard MBR signature at Sector 0.
[*] Scanning for Roland signatures...
FOUND: Disk Header / Project Info | Offset: 0x6600 | LBA: 51
FOUND: Effects Patch (.VS2) | Offset: 0xa640 | LBA: 83
FOUND: Disk Header / Project Info | Offset: 0x59da604 | LBA: 184019
FOUND: Disk Header / Project Info | Offset: 0x5a0a604 | LBA: 184403

➜  ZIP100 SP-808 DEMO disk: python ../disc_diff.py ../ZIP100\ 44.1kHZ\ empty\ disk/SP-808TS25E.ima SP-808TS25E.ima 
[*] Comparing ../ZIP100 44.1kHZ empty disk/SP-808TS25E.ima and SP-808TS25E.ima...
[!] Difference at Sector (LBA): 1 | Offset: 0x200
[!] Difference at Sector (LBA): 2 | Offset: 0x400
[!] Difference at Sector (LBA): 3 | Offset: 0x600
[!] Difference at Sector (LBA): 4 | Offset: 0x800
[!] Difference at Sector (LBA): 5 | Offset: 0xa00
[!] Difference at Sector (LBA): 6 | Offset: 0xc00
[!] Difference at Sector (LBA): 7 | Offset: 0xe00
[!] Difference at Sector (LBA): 8 | Offset: 0x1000
[!] Difference at Sector (LBA): 9 | Offset: 0x1200
[!] Difference at Sector (LBA): 32 | Offset: 0x4000
[!] Difference at Sector (LBA): 33 | Offset: 0x4200
[!] Difference at Sector (LBA): 34 | Offset: 0x4400
[!] Difference at Sector (LBA): 35 | Offset: 0x4600
[!] Difference at Sector (LBA): 36 | Offset: 0x4800
[!] Difference at Sector (LBA): 37 | Offset: 0x4a00
[!] Difference at Sector (LBA): 38 | Offset: 0x4c00
[!] Difference at Sector (LBA): 39 | Offset: 0x4e00
[!] Difference at Sector (LBA): 40 | Offset: 0x5000
[!] Difference at Sector (LBA): 41 | Offset: 0x5200
[!] Difference at Sector (LBA): 42 | Offset: 0x5400
[!] Difference at Sector (LBA): 43 | Offset: 0x5600
--- Too many changes, stopping scan ---

```
