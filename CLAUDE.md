# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Reverse engineering project for the Roland SP-808 sampler (1998). The primary goal is bypassing the ZIP-100 drive validation in firmware to enable modern ATAPI storage (CompactFlash, SD via CF adapter, ZuluIDE). **Status: Working as of April 2024.**

## Python Tools

### Firmware extraction from Roland MIDI update files

```bash
python firmware/rolandext.py model=sp808 infil="SP808*.mid" outfil=SP8EXall.bin
# Supported models: sp808, a6, vs880, integra7
```

The script decodes Roland's 7-bit-to-8-bit SysEx encoding in standard MIDI files and reconstructs the raw binary firmware.

### CompactFlash utilities

- `compactflash.py` — sends ATA IDENTIFY command over serial, decodes Word 0 flags
- `compactflash_ide.py` — same via `ata` library IDE interface
- `ECh.py` — ATA IDENTIFY device command analysis across all buses

### ZuluIDE configuration

`zuluide.ini` — drop in ZuluIDE root; configures it to emulate an Iomega ZIP 100 for the SP-808 (UDMA disabled, PIO 3, 512-byte block size).

## Architecture

### Hardware

- **MCU**: Hitachi H8S/2653 (HD6432653) — 16-bit, 20MHz, 64KB mask ROM, 4KB RAM, Operating Mode 6
- **IDE Controller**: Epson SLA919F ASIC — handles ATAPI, no DMA (pins 21/29 unconnected)
- **Flash**: Sharp LH28F800SUT-70 (1MB) — holds main firmware at `0x100000–0x1C0000`

### Memory map (runtime)

```
0x000000–0x00FFFF  On-chip ROM (boot/init)
0x100000–0x1C0000  External flash (firmware)
0x400000–0x4FFFFF  Runtime memory
0x403xxx           Device control registers
0x43Bxxx           Shadow registers
0x00FFEC00–0x00FFFBFF  On-chip RAM (4KB)
```

### Firmware binary layout

Firmware distributed as Roland SysEx-wrapped MIDI files. `rolandext.py` unpacks them. The resulting binary loads to flash at `0x8000` (IDA base address). Key offsets within `SP8EXall.bin`:

| Address | Content |
|---------|---------|
| `0x71AC0` | Device type strings: `ZIP `, `HD  `, `CD  ` |
| `0x71AF0` | Vendor ID strings: `IOMEGA  `, `iomega  ` |
| `0x71B90` | `Roland  ` vendor string |
| `0x71AD0` | SZHC command table |
| `0x4B520` | Device type validation code |
| `0x4B523` | **Patch location** — `0x05` → `0xFF` bypasses ZIP-only check |

### The patch

The SP-808 checks the connected device type against `0x05` (ZIP). Changing the comparison value at `0x4B523` to `0xFF` makes the check always fail, allowing any ATAPI device. The Edirol A6 (same hardware, accepts HDDs) was used to identify this location by firmware diffing.

The SZHC command table validation also requires that `MODE SENSE (0x5A)` with vendor subcommand `0x2F` returns `2F 5C FF D9`. ZuluIDE's `zuluide.ini` spoofs this response.

## IDA Pro Analysis

`IDA/SP808.idc` and `IDA/SP808_IDA_helper.idc` — IDC/Python scripts for IDA Pro.

Setup: load `SP8EXall.bin` as **Hitachi H8/300H**, base address `0x8000`. Run the helper script to auto-create named segments, vector table entries, SZHC table markers, and known string cross-references.

`IDA/H8.cfg` — processor config for IDA.

## Key Documentation Files

| File | Contents |
|------|----------|
| `RolandSP-808ZIPDriveValidationBypass.md` | Full analysis of the validation mechanism and patch |
| `Roland_SP-808_CPU.md` | H8S/2653 architecture, memory map, PCB pin observations |
| `Roland_SP-808_to_ZIP_Drive_sniff.md` | Full ATAPI bus trace of SP-808 ↔ ZIP drive |
| `SP-808_SZHC_CommandTableAnalysis.md` | SZHC command table structure |
| `SP-808_ZIP_DriveInitializationSequenceAnalysis.md` | Boot handshake sequence |
| `firmware/decoding_roland_A6_firmware.md` | MIDI SysEx encoding format internals |
| `HARDWARE_CORRECTIONS_2026-05.md` | Corrections to earlier hardware documentation |
| `CompactFlashCards.md` | Compatibility notes for CF cards |
| `Disks/SP-808_Demo_Disk_Analysis.md` | FAT16 disk structure analysis |

## Diagnostic / Hidden Modes

Access via button combos on power-on (documented in `things.md`):

- `Status + FX A` — MIDI Update
- `Status + FX B` — ZIP Update  
- `Status + FX C` — Develop Monitor
- `Status + FX D` — Diagnostic Mode
- `1/[5] + CLEAR` then power on — Save OS IMAGE to ZIP disk
- `2/[6] + CLEAR` then power on — Save OS FILE to ZIP disk

CN7 (unpopulated on PCB): TX1/RX1/XRST — potential H8/300 debug port (E6000 compatibility unconfirmed).
