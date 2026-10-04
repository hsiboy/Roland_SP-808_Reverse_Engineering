# Roland SP-808 Reverse Engineering

## NOT WORKING!! DO NOT FLASH

Replacing the obsolete Iomega ZIP drive in Roland SP-808/SP-808EX samplers with modern ATAPI storage devices.

## Status

| Area | Status |
|------|--------|
| Firmware patch (ZIP bypass) | ❌ *NOT* Working — validated on hardware (October 2026) |
| CompactFlash cards | ❌ Not Working |
| SD cards via CF adapter | ❌ Not Working |
| ZuluIDE emulation | ✅ Working (use `zuluide.ini`) |
| Disk image mounting (macOS/Linux) | ❌ Not Working |
| MIDI → binary extraction (`rolandext.py`) | ✅ Working |
| Binary → MIDI conversion (`bin2midi.py`) | ⚠️ Implemented, **not yet tested on hardware** |
| VS2 file format | ❌ Undocumented |
| CN7 debug UART | ⚠️ Testing on Hardware (October 2026) |
| Epson SLA919F ASIC protocol | ✅ Fully Understood |
| RDAC audio format | ⚠️ External decoder only (Randy Gordon's `rdac`) |

## Project Goals

The Roland SP-808 sampler (1998) uses an Iomega ZIP-100 drive for storage. ZIP drives are now obsolete, unreliable, and increasingly difficult to source. This project enables modern storage alternatives through:

- **Firmware modification**: Bypassing ZIP drive validation routines <-- its much much more involved!!
- **Hardware documentation**: Understanding the ATAPI interface and system architecture ✅
- **Tool development**: Utilities for firmware extraction, patching, and disk image handling - TODO

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



**Note**: This is a community reverse engineering project for preservation and compatibility purposes. All work respects intellectual property rights and is intended for personal, non-commercial use with hardware you own.
