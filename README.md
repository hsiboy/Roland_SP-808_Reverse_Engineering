# Roland SP-808 Reverse Engineering

Replacing the obsolete Iomega ZIP drive in Roland SP-808/SP-808EX samplers with modern ATAPI storage devices.

## Status: ✅ Working (April 2024)

Firmware patch successfully bypasses ZIP drive validation, enabling modern storage solutions including CompactFlash, SD cards via CF adapters, and ZuluIDE.

## Quick Start

### For SP-808 Owners

1. Download patched firmware from [Releases](../../releases)
2. Update your SP-808 using standard firmware update procedure
3. Install compatible storage device (see [Hardware Compatibility](../../wiki/Compact-Flash))
4. Format and use

### For Developers

Clone the repository and explore the firmware analysis, ATAPI protocol documentation, and hardware interface details in the [Wiki](../../wiki).

## Project Goals

The Roland SP-808 sampler (1998) uses an Iomega ZIP-100 drive for storage. ZIP drives are now obsolete, unreliable, and increasingly difficult to source. This project enables modern storage alternatives through:

- **Firmware modification**: Bypassing ZIP drive validation routines
- **Hardware documentation**: Understanding the ATAPI interface and system architecture
- **Tool development**: Utilities for disk image handling and audio extraction

## What Works

- ✅ CompactFlash cards (tested up to 32GB)
- ✅ SD cards via CF adapter
- ✅ ZuluIDE emulation
- ✅ Disk image mounting on macOS/Linux
- ✅ RDAC audio sample extraction

## Repository Structure

```
firmware/           Firmware binaries and analysis
hardware/           Datasheets, schematics, board photos
software/           Conversion tools and utilities
research/           Protocol analysis and reverse engineering notes
IDA/                IDA Pro projects
```

Detailed technical documentation has been moved to the [Wiki](../../wiki).

## Key Documentation

### Hardware
- [Hardware Overview](../../wiki/Hardware-Overview) - CPU, memory architecture, system design
- [ATAPI Interface](../../wiki/ATAPI-Interface) - IDE/ATAPI protocol implementation
- [ZIP Drive Interface](../../wiki/ZIP-Drive-Interface) - Original ZIP drive communication

### Firmware
- [Firmware Overview](../../wiki/Firmware-Overview) - Structure and distribution format
- [ZIP Drive Validation Bypass](../../wiki/ZIP-Drive-Validation-Bypass) - How the patch works
- [Command Tables](../../wiki/Command-Tables) - ATAPI command analysis

### Data Format
- [Disk Format](../../wiki/Disk-Format-Overview) - FAT16 filesystem structure
- [RDAC Audio Compression](../../wiki/RDAC-Audio-Compression) - Sample format and extraction
- [Mounting Disk Images](../../wiki/Mounting-Disk-Images) - macOS/Linux procedures

### Tools
- [Firmware Tools](../../wiki/Firmware-Tools) - MIDI to binary conversion
- [Python Utilities](../../wiki/Python-Utilities) - CompactFlash and IDE tools
- [RDAC Decoder](../../wiki/RDAC-Audio-Compression) - Audio sample extraction

## Technical Highlights

**CPU**: Hitachi H8S/2653 (16-bit, 20MHz, 64KB ROM, 4KB RAM)  
**Storage Interface**: ATAPI via Epson SLA919F ASIC  
**Audio Format**: Roland RDAC compression (MTP mode)  
**Disk Format**: DOS/MBR partition table, FAT16 filesystem

## Background

The SP-808 was designed around the Iomega ZIP-100 drive, which provided 100MB of removable storage in an era before flash memory. The firmware includes specific validation routines that check for genuine Iomega drives, preventing use of alternative storage devices.

This project bypasses those checks through targeted firmware modifications, documented hardware analysis, and development of supporting tools for disk management and data extraction.

## Contributing

Contributions welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Areas of interest:
- VS2 file format documentation (sequences, effects, pad banks)
- Additional storage device testing
- Firmware optimization
- Tool improvements

## Timeline

- **April 2024**: Firmware patch working, validation bypass confirmed
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
- [Original Discussion Thread](link-if-exists)

---

**Note**: This is a community reverse engineering project for preservation and compatibility purposes. All work respects intellectual property rights and is intended for personal, non-commercial use with hardware you own.
