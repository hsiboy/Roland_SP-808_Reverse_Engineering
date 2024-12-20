# SP808 Vs A6 firmware.

Looking at both outputs side by side, something very interesting emerges. The SP-808 firmware actually DOES contain "HD" in its device type list:

SP-808:
```
0x71ab5: ----
0x71abb: SELF
0x71ac0: ZIP 
0x71ac5: HD  
0x71aca: CD  
```

A6:
```
0x77a99: SELF
0x77a9e: ZIP 
0x77aa3: HD  
0x77aa8: CD  
```

The command tables are nearly identical too:
- Same sequence of commands
- Same parameters for each command
- Even the unknown commands (0x1a, 0xc0, 0x15, etc.) match

The key differences are:
1. Different string tables at the end:
   - SP-808: "Roland", "TS25E", "FAT12", "FAT16", "SP-808TS25E"
   - A6: "ECV02(A-6) ARCHIVE FILE"

2. Different base addresses:
   - SP-808: 0x71ad0
   - A6: 0x77aae

This suggests that the hardware lockout isn't in the SZHC table itself - both firmwares have "HD" as a valid device type. The difference must be in how this table is processed. 

TODO:
1. Where in the firmware these tables are referenced?
2. Any code that processes the device type strings?

The fact that both firmwares have identical command structures but different behaviors suggests the validation logic might be elsewhere in the code.
