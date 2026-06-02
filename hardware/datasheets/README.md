# Datasheets

| File | Document | Relevance |
|------|----------|-----------|
| `h8s26p.pdf` | Renesas H8S/2600 Series, H8S/2000 Series Programming Manual | Instruction set, addressing modes, exception handling. Primary reference for disassembly and IDA analysis. |
| `REN_rej09b0138_h8s2357_MAS_20041028.pdf` | Renesas H8S/2357 Group Hardware Manual | Hardware manual for a related H8S/2300 variant. Register map, bus control, and I/O peripheral details are partially applicable to the H8S/2653. Use the H8S/2653-specific manual where available. |
| `REN_rej09b0331_2655hm_MAH_20060914.pdf` | Renesas H8S/2655 Group Hardware Manual | **Note**: The SP-808 uses the H8S/**2653**, not 2655. This manual is included for cross-reference only; the 2655 is a different variant. Prefer H8S/2653 documentation for hardware specifics. |

## Missing Datasheets

- **H8S/2653 Hardware Manual** — the definitive reference for the actual SP-808 MCU. Not included; download from Renesas/Hitachi archives if available.
- **Epson SLA919F** — the IDE/ATAPI ASIC on the SP-808 PCB. No public datasheet is known to exist. Protocol has been partially reverse-engineered from bus traces (see `Roland_SP-808_to_ZIP_Drive_sniff.md`).
- **Sharp LH28F800SUT-70** — the 1MB flash chip. See `LH28F800SUT-70.md` in the repo root for specifications from the datasheet.
