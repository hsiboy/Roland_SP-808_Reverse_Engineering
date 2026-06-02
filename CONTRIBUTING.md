# Contributing

This is a community reverse engineering project for preservation and compatibility. Contributions of all kinds are welcome.

## Areas of Interest

- **VS2 file format** — sequences, effects settings, pad banks. The filenames are known (`SONG0000VS2`, `EFFECT__VS2`, etc.) but the internal binary format is undocumented.
- **Additional storage device testing** — report which CF cards, SD adapters, and ZuluIDE configurations work or fail.
- **UART/debug port** — the unpopulated CN7 connector exposes TX1/RX1/XRST from the H8S/2653. If you capture output during boot, document it.
- **ASIC protocol** — the Epson SLA919F has no public datasheet. Extended bus traces, especially for vendor commands `0x06` and `0x0D`, would help complete the picture.
- **A6 firmware** — the Edirol A6 uses the same hardware. A full analysis of A6 firmware device types `0x07` and `0x08` would confirm HDD support paths.

## What to Include

For bug reports or corrections: describe the discrepancy, cite which file it's in, and where you found the correct information (datasheet, bus trace, hardware measurement).

For new documentation: include source references (datasheet page numbers, bus trace line numbers, firmware offsets) so findings can be independently verified.

For code changes: verify against `rolandext.py` round-trip tests before submitting changes to the firmware tools.

## Repo Structure

See [README.md](README.md) for the current file layout.

## No Affiliation

This project has no affiliation with Roland Corporation. All work is intended for personal, non-commercial use with hardware you own.
