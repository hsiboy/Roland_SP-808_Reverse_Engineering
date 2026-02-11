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

➜  ZIP100 SP-808 DEMO disk: python ../disc_header_peek.py SP-808TS25E.ima RDAC
[*] Searching for 'RDAC' in SP-808TS25E.ima...

➜  ZIP100 SP-808 DEMO disk: python ../disc_header_peek.py SP-808TS25E.ima SP-808
[*] Searching for 'SP-808' in SP-808TS25E.ima...

[+] Match found at 0x6600 (LBA: 51)
HEX:   53 50 2d 38 30 38 54 53 32 35 45 08 00 00 00 00 00 00 00 00 00 00 92 86 9a 28 00 00 00 00 00 00 e5 4f 4e 47 4c 49 53 54 56 53 32 20 00 00 00 00 00 00 00 00 00 00 92 86 9a 28 50 0b 42 01 00 00
ASCII: SP-808TS25E..............(.......ONGLISTVS2 .............(P.B...

[+] Match found at 0x59da604 (LBA: 184019)
HEX:   53 50 2d 38 30 38 20 30 31 30 30 00 01 00 00 44 43 48 49 4d 45 52 41 20 20 20 20 20 04 00 00 00 04 00 00 00 15 00 ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff
ASCII: SP-808 0100....DCHIMERA     ....................................

[+] Match found at 0x59f2604 (LBA: 184211)
HEX:   53 50 2d 38 30 38 20 30 31 30 30 00 01 00 00 44 64 65 65 70 20 63 61 76 69 74 79 20 06 00 00 00 04 00 00 00 4b 00 ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff
ASCII: SP-808 0100....Ddeep cavity ........K...........................

[+] Match found at 0x5a0a604 (LBA: 184403)
HEX:   53 50 2d 38 30 38 20 30 31 30 30 00 01 00 00 44 45 66 66 65 63 74 69 76 65 20 20 20 06 00 00 00 04 00 00 00 54 00 ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff
ASCII: SP-808 0100....DEffective   ........T...........................

[+] Match found at 0x5a22604 (LBA: 184595)
HEX:   53 50 2d 38 30 38 20 30 31 30 30 00 01 00 00 44 43 48 49 4d 45 52 41 20 45 58 20 20 04 00 02 00 04 00 00 00 27 00 00 00 54 00 00 00 64 80 ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff
ASCII: SP-808 0100....DCHIMERA EX  ........'...T...d...................

[+] Match found at 0x5a3a604 (LBA: 184787)
HEX:   53 50 2d 38 30 38 20 30 31 30 30 00 01 00 00 44 45 66 66 65 63 74 69 76 65 20 45 58 06 00 00 00 04 00 00 00 54 00 00 00 90 00 00 00 c0 00 ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff
ASCII: SP-808 0100....DEffective EX........T...........................

[+] Match found at 0x5a52604 (LBA: 184979)
HEX:   53 50 2d 38 30 38 20 30 31 30 30 00 01 00 00 44 31 33 35 20 53 6f 6e 67 20 20 20 20 02 00 00 00 04 00 ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff
ASCII: SP-808 0100....D135 Song    ....................................

[+] Match found at 0x5a6a604 (LBA: 185171)
HEX:   53 50 2d 38 30 38 20 30 31 30 30 00 01 00 00 44 31 36 31 20 53 6f 6e 67 20 20 20 20 06 00 00 00 04 00 ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff
ASCII: SP-808 0100....D161 Song    ....................................

[+] Match found at 0x5a92604 (LBA: 185491)
HEX:   53 50 2d 38 30 38 20 30 31 30 30 00 01 00 00 44 31 37 30 20 53 6f 6e 67 20 20 20 20 06 00 00 00 04 00 ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff
ASCII: SP-808 0100....D170 Song    ....................................

[+] Match found at 0x5aaa604 (LBA: 185683)
HEX:   53 50 2d 38 30 38 20 30 31 30 30 00 01 00 00 44 4e 65 77 20 53 6f 6e 67 20 20 31 31 04 00 00 00 04 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ff ff ff ff ff ff ff ff ff ff ff ff ff ff
ASCII: SP-808 0100....DNew Song  11....................................
➜  ZIP100 SP-808 DEMO disk 

```
