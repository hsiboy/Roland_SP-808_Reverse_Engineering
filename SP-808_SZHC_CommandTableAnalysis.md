# SP-808 SZHC Command Table Analysis

## Overview
During reverse engineering of the Roland SP-808's firmware, we discovered a significant table structure marked with "SZHC" that appears to define the ZIP drive validation sequence. ~~This table is crucial for understanding how the SP-808 authenticates and communicates with its storage device.~~

The A6 Firmware:

```asm
ROM_DATA:177A99 aSelf:          .ascii "SELF"<0>
ROM_DATA:177A9E aZip_0:         .ascii "ZIP "<0>
ROM_DATA:177AA3 aHd:            .ascii "HD  "<0>
ROM_DATA:177AA8 aCd:            .ascii "CD  "<0>
ROM_DATA:177AAD byte_177AAD:    .byte 0x2D                                            ; DATA XREF: sub_1080B6+162↑r
ROM_DATA:177AAE aSzhc:          .ascii "SZHC"
```

Device Types:

* SELF (possibly internal storage)
* ZIP (Iomega ZIP drive)
* HD (Hard Drive)
* CD (CD-ROM)


> [!NOTE]
> Could the "SZHC" string be a signature or bitmap? <br>
> S = SELF <br>
> Z = ZIP <br>
> H = HD <br>
> C = CD ?

<br>
---

This output is very revealing! Let's analyze what we see in function `sub_12E8E0`:

1. Device Identification Sequence:
   ```
   1. Check "IOMEGA  " (capitalized)
   2. If that fails, check "iomega  " (lowercase)
   3. Finally check for "ZIP"
   ```

2. Key Code Flow:
   ```assembly
   ; After IOMEGA check
   mov.b   r0l, r0l      ; Check result
   bne     loc_12EA5C    ; Branch if not IOMEGA
   
   ; After iomega check
   mov.b   r0l, r0l      ; Check result
   beq     loc_12EBB4    ; Branch if iomega found
   
   ; ZIP check follows
   ```

3. Data References:
   ```
   0x177aad: 0x2d535a48  ; Referenced in sub_1080B6
   ; Interesting: This looks like ASCII "-SZH" backwards!
   ; Could be related to the "SZHC" signature we saw
   ```

Some interesting patterns:
1. The string comparisons appear to be length-aware (pushing 8 for IOMEGA checks, 3 for ZIP)
2. There's case-insensitive fallback (tries IOMEGA then iomega)
3. Memory location 0x41E864 appears important in the validation process


## Table Location and Structure
Located at firmware offset `0x71AD0`, the table follows this format:
```
SZHC
06 00 00 00 00 00 00     // Command entry 1
06 1B 00 00 00 00 00     // START/STOP UNIT
06 1E 00 00 00 00 00     // PREVENT/ALLOW MEDIA REMOVAL
06 03 00 00 00 00 00     // REQUEST SENSE
IOMEGA  
iomega  
ZIP
06 12 00 00 00 00 00     // INQUIRY
```

## Significance
1. **Command Protocol**
   - Each command entry is 7 bytes long
   - Starts with `06` (possibly a marker or length field)
   - Followed by command byte and 5 parameter bytes
   - This format suggests a custom protocol between the MCU and EPSON ASIC

2. **Initialization Sequence**
   - The table appears to define the exact order of commands needed during device initialization
   - Commands match observed IDE/ATAPI bus traces
   - Includes critical validation commands

3. **Validation Process**
   - Table includes commands for:
     - Device identification (INQUIRY)
     - Media control (START/STOP, PREVENT/ALLOW)
     - Status checking (REQUEST SENSE)
   - Leads to key validation sequence: `5A 2F → 2F 5C FF D9`

## Hardware Implementation
- MCU (Hitachi H8S/2653) doesn't talk directly to IDE bus
- EPSON ASIC (SLA919F) acts as interface controller
- 7-byte command structure likely defines ASIC protocol
- No DMA support (DDRQ and DDRACK pins not connected)

## Why It's Important
1. **Authentication Mechanism**
   - Shows Roland implemented custom validation
   - Uses combination of standard ATAPI and vendor-specific commands
   - Requires specific responses to allow operation

2. **Hardware Architecture**
   - Reveals custom protocol between MCU and ASIC
   - Explains how SP-808 manages ZIP drive without direct IDE control

3. **Reverse Engineering Value**
   - Provides clear command sequence for drive emulation
   - Documents exact validation requirements
   - Maps to observed hardware behavior

## Validation Sequence
When correctly implemented, this sequence:
1. Initializes device communication
2. Verifies device identity
3. Configures media access
4. Performs vendor-specific validation
5. Enables normal operation

## Implications
Understanding this table structure is crucial for:
- Developing ZIP drive emulation
- Creating alternative storage solutions
- Understanding Roland's security approach
- Documenting historical hardware implementations

This discovery provides a clear roadmap for implementing compatible storage solutions while maintaining the SP-808's original functionality.
