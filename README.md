# Roland SP-808 Reverse Engineering

Replacing the obsolete Iomega ZIP drive in Roland SP-808/SP-808EX samplers with modern ATAPI storage devices.

## Status

| Area | Status |
|------|--------|
| Firmware patch (ZIP bypass) | ✅ Working — validated on hardware (April 2024) |
| CompactFlash cards | ✅ Tested up to 32GB |
| SD cards via CF adapter | ✅ Working |
| ZuluIDE emulation | ✅ Working (use `zuluide.ini`) |
| Disk image mounting (macOS/Linux) | ✅ Working |
| MIDI → binary extraction (`rolandext.py`) | ✅ Working |
| Binary → MIDI conversion (`bin2midi.py`) | ⚠️ Implemented, **not yet tested on hardware** |
| VS2 file format | ❌ Undocumented |
| CN7 debug UART | ❌ Not yet investigated |
| Epson SLA919F ASIC protocol | ⚠️ Partially mapped from bus traces |
| RDAC audio format | ⚠️ External decoder only (Randy Gordon's `rdac`) |

## Quick Start

### For SP-808 Owners

1. Extract the original firmware from the SP-808EX MIDI update files (see `firmware/README.md`)
2. Patch with `python firmware/patch_sp808.py SP8EXall.bin SP8EXall_patched.bin`
3. Convert back to MIDI with `python firmware/bin2midi.py SP8EXall_patched.bin SP8EX_patched`
4. **Run the round-trip test before flashing** (see `firmware/README.md`) — `bin2midi.py` has not yet been verified on hardware
5. Flash via MIDI (power on SP-808 holding SHIFT, send files #1–#8 in order)
6. Install a compatible storage device (CompactFlash, SD via CF adapter, or ZuluIDE)
7. Use `zuluide.ini` if using ZuluIDE

### For Developers

Clone the repository and explore the firmware analysis, ATAPI protocol documentation, and hardware interface details in the docs below.

## Project Goals

The Roland SP-808 sampler (1998) uses an Iomega ZIP-100 drive for storage. ZIP drives are now obsolete, unreliable, and increasingly difficult to source. This project enables modern storage alternatives through:

- **Firmware modification**: Bypassing ZIP drive validation routines
- **Hardware documentation**: Understanding the ATAPI interface and system architecture
- **Tool development**: Utilities for firmware extraction, patching, and disk image handling

## Repository Structure

```
firmware/           Firmware binaries, extraction and patching tools
  rolandext.py        MIDI SysEx → binary extraction
  patch_sp808.py      Apply ZIP bypass patch to firmware binary
  bin2midi.py         Binary → MIDI SysEx (for reflashing)
hardware/           Datasheets, schematics, board photos
IDA/                IDA Pro scripts for H8S/2653 firmware analysis
Disks/              Disk image analysis and RDAC map
```

Analysis and protocol documentation is in the root and named files.

## Key Documentation

### Hardware
- [CPU and Architecture](Roland_SP-808_CPU.md) - H8S/2653, memory map, PCB observations
- [Flash Memory](LH28F800SUT-70.md) - Sharp LH28F800SUT-70 specifications
- [Notes and Overview](Roland_SP-808_Notes.md) - Memory map, firmware load address

### Firmware
- [ZIP Drive Validation Bypass](RolandSP-808ZIPDriveValidationBypass.md) - The patch: how and why
- [SZHC Command Table](SP-808_SZHC_CommandTableAnalysis.md) - ATAPI command table structure
- [SP-808 vs A6 Firmware](firmware/SP808_Vs_A6_firmware.md) - Comparison that found the patch location
- [Firmware Workflow](firmware/README.md) - Extract → patch → flash procedure

### Protocol
- [ATAPI Protocol](ATAPI.md) - IDE/ATAPI reference
- [ZIP Drive Initialization](SP-808_and_ZIP_Drive.md) - Initialization sequence
- [Bus Trace](Roland_SP-808_to_ZIP_Drive_sniff.md) - Full IDE bus capture

### Data Format
- [Disk Structure](Disks/SP-808_Demo_Disk_Analysis.md) - FAT16 filesystem, VS2 filenames
- [Mounting Disk Images](disk_img.md) - macOS/Linux procedures
- [CompactFlash Notes](CompactFlashCards.md) - CF card compatibility

### IDA Pro
- [Using IDA](IDA/using_IDA.md) - Setup guide for H8S firmware analysis

## Technical Highlights

**CPU**: Hitachi H8S/2653 (16-bit, 20MHz, 64KB ROM, 4KB RAM)  
**Storage Interface**: ATAPI via Epson SLA919F ASIC  
**Audio Format**: Roland RDAC compression (MTP mode)  
**Disk Format**: DOS/MBR partition table, FAT16 filesystem

## Background

The SP-808 was designed around the Iomega ZIP-100 drive, which provided 100MB of removable storage in an era before flash memory. The firmware includes specific validation routines that check for genuine Iomega drives, preventing use of alternative storage devices.

This project bypasses those checks through targeted firmware modifications, documented hardware analysis, and development of supporting tools for disk management and data extraction.

## Contributing

Contributions welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) and [TODO.md](TODO.md) for open items.

Priority areas:

- **`bin2midi.py` hardware test** — the round-trip encode/decode is verified correct but the script has not been used to flash a real SP-808. If you try it, report the result.
- **VS2 file format** — filenames are known (`SONG0000VS2`, `EFFECT__VS2`, `PADBANK_VS2`, etc.), internal format is not documented.
- **CN7 debug port** — the unpopulated connector breaks out TX1/RX1/XRST from the H8S/2653. A logic analyser session during boot could reveal a debug UART.
- **Additional storage device testing** — report which CF cards, SD adapters, and ZuluIDE versions work or fail.
- **Epson SLA919F ASIC** — no public datasheet; vendor commands `0x06` and `0x0D` are partially mapped. Extended bus traces welcome.

## Timeline

- **June 2026**: Documentation audit; all hardware corrections applied; `bin2midi.py` written; base address resolved (`0x100000`)
- **April 2024**: Firmware patch working, validation bypass confirmed on hardware
- **January 2024**: ATAPI protocol analysis, command table mapping
- **2023**: Initial firmware extraction and reverse engineering
- **Earlier**: Hardware documentation, RDAC decoder integration

## Credits

- **Randy Gordon**: RDAC decoder ([github.com/randygordon/rdac](https://github.com/randygordon/rdac))
- **Hitachi/Renesas**: H8S/2600 documentation and toolchain
- **Roland Corporation**: Original SP-808 design (no affiliation with this project)


## Disclaimer

This project is not affiliated with or endorsed by Roland Corporation. Firmware modification may void warranties and carries inherent risks. Use at your own discretion.

## Resources

- [Roland SP-808 Owner's Manual](SP-808_OM.pdf)
- [Roland SP-808 Service Manual](Roland-SP-808-808-Pro-Service-Manual.pdf)
- [H8S/2600 Programming Manual](hardware/datasheets/)
- [Original Discussion Thread](https://forum.hddguru.com/viewtopic.php?f=13&t=31086)

---

**Note**: This is a community reverse engineering project for preservation and compatibility purposes. All work respects intellectual property rights and is intended for personal, non-commercial use with hardware you own.
