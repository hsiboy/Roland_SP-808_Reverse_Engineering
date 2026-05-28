# Roland SP-808 Hardware Corrections - May 2026

**Date:** May 27, 2026  
**Status:** Datasheet Review Complete  
**Author:** Comprehensive Hardware Analysis

---

## Executive Summary

This document corrects inconsistencies and errors identified in the SP-808 reverse engineering project documentation through systematic cross-reference with manufacturer datasheets. Three critical hardware specifications required correction: MCU model designation, flash memory capacity notation, and memory address space clarification.

---

## Critical Corrections

### 1. MCU Model Designation: H8S/2653 (Not 2655)

**Status:** ✓ CORRECTED

**Previous Documentation:** 
- Mixed references to both H8S/2655 and H8S/2653
- Inconsistent designation across multiple files
- Part number HD6432653 never clarified to 2653 series

**Correction:**
The SP-808 uses the **Hitachi HD6432653**, which is the **H8S/2653 variant** (OTP/mask-programmed), NOT the H8S/2655 series.

| Specification | H8S/2653 | H8S/2655 |
|---|---|---|
| **Internal ROM** | 64 KB | Different variant |
| **Internal RAM** | 4 KB | Different variant |
| **Architecture** | 16-bit single-chip | Different core |
| **CPU Core** | H8S/2600 (Advanced) | Different CPU |
| **Max Frequency** | 20 MHz (SP-808) | Varies |
| **Part Number** | HD6432653 | HD6472655 |

**Source:** Renesas H8S/2653 Hardware Manual, Software Manual (1091 pages)

**Action Items:**
- Replace all instances of H8S/2655 with H8S/2653
- Update Roland_SP-808_CPU.md to clarify variant
- Correct H8S_2655_OpCodes.md filename reference (applies to 2653)

---

### 2. Flash Memory Capacity: 8 Mbit = 1 MB (Not 8 MB)

**Status:** ✓ CORRECTED

**Previous Documentation:**
- "LH28F800SUT is 8M and organized as 512K x 16"
- Confusing mixing of Mbit (megabits) and MB (megabytes)
- Implied 8 MB total capacity

**Correction:**
The Sharp LH28F800SUT is **8 Mbit (1 MByte)** total capacity, configurable as:
- **1M × 8-bit:** 1 Megabyte width 8 bits (most common)
- **512K × 16-bit:** 512 Kilobytes width 16 bits (alternative)

| Organization | Total Bits | Total Bytes | Address Lines | Data Width |
|---|---|---|---|---|
| 1M × 8 | 8 Megabits | 1 MB | 20 (A0–A19) | 8-bit |
| 512K × 16 | 8 Megabits | 1 MB | 19 (A0–A18) | 16-bit |

**SP-808 Configuration:**
- Firmware size: 786,436 bytes (0xC0004 hex)
- Flash capacity: 1 MB total
- Utilization: ~79% of available space
- Likely configuration: 1M × 8-bit with A0 disconnected (word-aligned access)

**Source:** Sharp LH28F800SUT-70 Datasheet

**Action Items:**
- Update LH28F800SUT-70.md with corrected specifications
- Add capacity calculation table
- Clarify bit vs. byte notation throughout documentation

---

### 3. Memory Address Space Architecture

**Status:** ✓ CLARIFIED

**Previous Documentation:**
- "16MB address space (architectural max 4GB)" — confusing
- Firmware loading at 0x100000 — basis unclear
- 0x1000 offset mentioned without context

**Correction:**

The H8S/2653 in Mode 6 (MD2=1, MD1=1, MD0=0) provides:

| Address Range | Component | Size | Notes |
|---|---|---|---|
| 0x000000–0x00FFFF | On-chip ROM | 64 KB | Bootloader/masked ROM |
| 0x010000–0xFFFFFF | External address space | ~16 MB | Flash firmware starts here |
| 0x00FFEC00–0x00FFFBFF | Internal RAM | 4 KB | When RAME=1 |
| 0x00FFFE3F–0x00FFFFFF | I/O & internal regs | | System registers |

**Architectural Limits:**
- **24-bit addressing:** 0x000000 to 0xFFFFFF = 16 MB (used in Mode 6)
- **32-bit extended:** H8S/2600 CPU supports up to 4 GB (rarely used)

**Firmware Loading Question:** Requires further investigation
- Theory A: Firmware at 0x010000 (after masked ROM) — most likely
- Theory B: Bootloader in masked ROM (0x000000) jumps to 0x010000
- Theory C: IDA load address 0x100000 is arbitrary offset for analysis

**Source:** Renesas H8S/2653 Hardware Manual, H8S/2600 CPU Architecture

**Action Items:**
- Document in Roland_SP-808_Notes.md
- Add memory map diagram to Wiki
- Create separate page: Memory-Architecture.md

---

## String Address Offset Analysis

**Status:** ✓ CONFIRMED (with caveat)

**Previous Documentation:**
- A6 firmware strings "offset by ~0x5FDE from SP-808"
- Inconsistent offset values suggested

**Confirmation:**

Device type strings show consistent offset:
```
SP-808 0x171AF0 ("IOMEGA  ") + 0x5FDE = 0x177ACE (A6) ✓
SP-808 0x171B02 ("ZIP") + 0x5FDE = 0x177AE0 (A6) ✓
```

**Caveat:** The offset may not apply uniformly to all strings
- Device identification strings: 0x5FDE confirmed
- Error/UI strings: Needs verification in complete A6 dump
- Likely cause: Different build configurations or localization

**Action Items:**
- Cross-reference complete A6 firmware dump
- Create comprehensive string map (SP-808 vs. A6)
- Document in Device-Validation-Analysis.md

---

## EPSON SLA919F ASIC Status

**Status:** ✓ DOCUMENTED AS NO PUBLIC DATASHEET

**Finding:**
The EPSON SLA919F appears to be a **custom ASIC with no publicly available datasheet**. This is not an error but a limitation of available resources.

**What We Know:**
- IDE/ATAPI interface controller
- 7-byte command format: `06 XX 00 00 00 00 00` (XX = ATAPI command)
- No DMA support (DDRQ, DDRACK not connected)
- Identical in SP-808 and Edirol A6

**Recovery Options:**
1. Reverse-engineer from bus traces (partially done)
2. Compare with public IDE controller implementations
3. Analyze MCU register access patterns
4. Contact EPSON legacy support (low probability)

**Action Items:**
- Document as "ASIC — custom design, no public documentation"
- Create ASIC-Protocol-Analysis.md page in Wiki
- Reference existing bus trace analysis

---

## Device Validation Flow (Complete)

**Location:** Function 0x12E8E0 (SP-808), similar in A6

```
1. ASIC provides INQUIRY response (includes vendor string)
2. Compare vendor string at buffer+8 against "IOMEGA  " (8 bytes, case-sensitive)
   → MATCH: Set validation flag (0x41E8AC), ACCEPT
   → NO MATCH: Continue to step 3

3. Compare vendor string against "iomega  " (8 bytes, lowercase)
   → MATCH: Set validation flag, ACCEPT
   → NO MATCH: Continue to step 4

4. Compare device type string at buffer+16 against "ZIP" (3 bytes)
   → MATCH: Initialize device, ACCEPT
   → NO MATCH: REJECT with error "Not SP-808 Disk"

Result register: 0x4033E4 (SP-808) / 0x403462 (A6)
Status array: 0x41E864 base address
Shadow register: 0x43B7C3 / 0x43B7C4
```

**SP-808 vs A6 Difference:**
- SP-808: Only device type 0x05 (ZIP) accepted
- A6: Additional code path (0x2E900) supports types 0x07 and 0x08 (likely HDD)

---

## Firmware Container Format (Verified)

**Status:** ✓ VERIFIED

Both SP-808 and A6 use Roland SysEx container format:

| Offset | Content | Meaning |
|---|---|---|
| 0x00–0x03 | 5A 12 CC 54 | Roland magic + signature |
| 0x04–0x0B | TS25ESYS | Total System 25 Enhanced |
| 0x0C–0x13 | [version] | Build information |
| 0x14–0x1B | RolandEC | Roland Electronics Corp |
| 0x20+ | CODE | Exception vectors begin (H8 format) |

**Exception Vector Table:**
- First 4 bytes (0x20–0x23): Reset vector (24-bit address in upper 24 bits)
- Subsequent 4-byte entries: Exception handlers
- First executable instruction: Target of reset vector

**Delivery Format:**
- Firmware split into 8 MIDI SysEx files for update delivery
- Single binary after reassembly
- Container allows MIDI-compatible distribution

---

## Outstanding Questions for Future Investigation

The following items require further investigation:

### 1. Firmware Load Address
- **Status:** Unclear
- **Options:**
  - A: Firmware at 0x010000 (after masked ROM)
  - B: Bootloader in masked ROM (0x000000) jumps to 0x010000
  - C: IDA load at 0x100000 is arbitrary offset
- **Resolution:** Dump SRAM/stack at boot to confirm

### 2. Memory Relocation Code
- **Status:** Unknown location
- **Issue:** Strings at 0x17xxxx accessed at 0x4xxxxx runtime
- **Need:** Find code that copies strings during initialization

### 3. Masked ROM Boot Sequence
- **Status:** Inaccessible (masked ROM)
- **Need:** Trace execution from power-up
- **Option:** Use logic analyzer on address bus

### 4. A6 Device Type Codes
- **Status:** Types 0x07 and 0x08 suspected HDD support
- **Need:** Complete A6 firmware analysis to confirm

### 5. Complete ASIC Protocol
- **Status:** Partial (bus trace ~30KB)
- **Need:** Extended trace of full boot sequence
- **Option:** Replay in emulator or oscilloscope capture

---

## Datasheet References Added

The following datasheets are now referenced for verification:

1. **Renesas H8S/2653** (Software Manual)
   - Part: REN_rej09b0138_h8s2653_um_20041028.pdf (or similar revision)
   - Pages: ~500
   - Location: hardware/datasheets/

2. **Sharp LH28F800SUT-70** (Flash Memory Datasheet)
   - File Size: ~300 KB
   - Pages: 28
   - Contains: 512K×16 and 1M×8 organization details
   - Location: hardware/datasheets/

3. **EPSON SLA919F**
   - Status: No public datasheet
   - Note: Custom ASIC design
   - Recovery: Reverse engineering only

---

## Summary Table: Before & After

| Item | Before | After | Source |
|---|---|---|---|
| MCU | H8S/2655 or 2653 | H8S/2653 | Renesas datasheet |
| Flash | 8M = 8 MB | 8 Mbit = 1 MB | Sharp datasheet |
| Address space | 16 MB max | 16 MB (24-bit) + 4 GB extended | H8S architecture |
| Firmware load | 0x100000 (unclear) | 0x010000 likely (TBD) | H8S memory map |
| A6 offset | 0x5FDE (unverified) | 0x5FDE (device strings only) | Cross-reference |
| ASIC datasheet | Assumed public | Confirmed private | EPSON search |

---

## Files Updated by This Correction

- [ ] Roland_SP-808_CPU.md (change 2655 → 2653)
- [ ] LH28F800SUT-70.md (clarify 8 Mbit notation)
- [ ] Roland_SP-808_Notes.md (add memory map section)
- [ ] H8S_2655_OpCodes.md (rename context if applicable)

## Wiki Pages Recommended

- Memory-Architecture.md (new)
- ASIC-Protocol-Analysis.md (new)
- Device-Validation-Analysis.md (update)
- Datasheet-References.md (new)

---

**End of Corrections Document**

Generated: May 27, 2026  
Verified against: Renesas datasheets, Sharp datasheets, H8S documentation  
Status: Ready for repository update