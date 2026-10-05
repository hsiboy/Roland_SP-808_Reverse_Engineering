# scripts/

Host-side utilities for probing a candidate storage device's **ATA IDENTIFY** response (used when
evaluating CF cards, CF/SD adapters, or HDDs as Zip-drive replacements). These are general PC-side
tools and are independent of the firmware toolchain (`firmware/`), the disk-image tools
(`Disks/Tools/`), and the IDA scripts (`IDA/`).

| Script | Purpose | Requires |
|--------|---------|----------|
| `cf_identify_serial.py` | Send ATA IDENTIFY over a serial port and decode Word 0 flags | `pyserial` |
| `cf_identify_ide.py` | Send ATA IDENTIFY via the `ata` library's IDE interface | `ata` |
| `ata_identify_scan.py` | Enumerate all buses/devices and dump each IDENTIFY response | `ata` |

Formerly `compactflash.py`, `compactflash_ide.py`, and `ECh.py` at the repo root. See
`Disks/CompactFlashCards.md` for the decoded Word 0 bit meanings and collected IDENTIFY data.
