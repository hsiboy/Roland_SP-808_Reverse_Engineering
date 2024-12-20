# SP-808 SZHC Command Table Analysis

## Overview
During reverse engineering of the Roland SP-808's firmware, we discovered a significant table structure marked with "SZHC" that appears to define the ZIP drive validation sequence. This table is crucial for understanding how the SP-808 authenticates and communicates with its storage device.

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
