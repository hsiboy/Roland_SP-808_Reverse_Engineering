# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Reverse engineering project for the Roland SP-808 / SP-808EX sampler (1998). The goal is to run
modern ATAPI/IDE storage (CompactFlash, SD via CF adapter, ZuluIDE, or an IDE HDD) in place of the
stock Iomega ZIP-100 drive.

**Current objective:** transplant the Edirol A6's application-resident native ATA backend into the
SP-808 firmware (see "HDD enablement" below). This supersedes the earlier belief that a small
ZIP-check patch alone enabled arbitrary ATAPI devices.

### Document authority (read this first)

This project deliberately separates **OBSERVED / STRONGLY INFERRED / HYPOTHESIZED / UNRESOLVED /
SUPERSEDED** evidence, and contains a lot of older, now-corrected material. When documents conflict,
**newer firmware/data-flow reconstruction wins over inherited semantic names and older prose.**

The current authoritative sources, in order, are the most recent dated revisions of:

1. `SP-808EX_Evidence_Ledger_*.md` — the clean evidence ledger (currently `..._2026-10-05_v11*.md`).
2. `SP-808EX_Observed_Architecture_Technical_Reference_*.md` — consolidated architecture (currently `..._2026-10-05_v9*.md`).
3. `Roland_SP-808_Hardware_Architecture_Corrections_*.md` — hardware/correction record (currently `..._2026-10-05_v4*.md`).

`AGENTS.md` describes the evidence discipline all analysis must follow. Treat **every other `.md` in
the repo (including the older dated revisions and the tables below) as leads, not premises.** Existing
IDA names/comments are navigation aids, not evidence; do not use agreement between an IDA name, a
helper script, and a Markdown note as independent confirmation when they may share one origin.

## Python Tools

### Firmware extraction from Roland MIDI update files

```bash
python firmware/rolandext.py model=sp808 infil="SP808*.mid" outfil=SP8EXall.bin
# Supported models: sp808, a6, vs880, integra7
```

The script decodes Roland's 7-bit-to-8-bit SysEx encoding in standard MIDI files and reconstructs the
raw binary firmware. The current reference image `SP8EXall.bin` is 786,436 bytes (`0xC0004`), MD5
`d744a9cd4a2790ac68d165fd7849b5d8`: a 32-byte container header followed by the executable image from
file offset `0x20`.

> **Repacking caveat (SMF audit, 2026-10-06).** `rolandext.py` is reliable only for *decoding* the
> original update set; its re-encode path has an append-mode bug (produces 786,464 B, not 786,436).
> `firmware/bin2midi.py` and the `firmware/Bin2Mid.md` example produce **malformed** SMFs (bad SysEx
> length, invented packet layout, dropped metadata) — do not use them. To build a MIDI update set
> from a modified image, use the audited `analysis/smf_v3_deployment_audit.py`
> (see `analysis/Link_Plan_v3_SMF_audit_2026-10-06.md`).

### CompactFlash / ATA IDENTIFY utilities (`scripts/`)

Host-side tools for querying a candidate storage device's ATA IDENTIFY response:

- `scripts/cf_identify_serial.py` — sends ATA IDENTIFY over serial, decodes Word 0 flags (was `compactflash.py`)
- `scripts/cf_identify_ide.py` — same via the `ata` library IDE interface (was `compactflash_ide.py`)
- `scripts/ata_identify_scan.py` — ATA IDENTIFY (`ECh`) device scan across all buses (was `ECh.py`)

### ZuluIDE configuration

`zuluide.ini` — drop in ZuluIDE root; configures it to emulate an Iomega ZIP 100 for the SP-808
(UDMA disabled, PIO 3, 512-byte block size). This targets the stock **internal ATAPI** Zip path.

## Architecture

### Hardware

- **MCU**: Hitachi/Renesas **H8S/2653** (`HD6432653BA11F`, H8S/2600 core), 20.000 MHz crystal (X1),
  advanced expanded mode. On-chip ROM 64 KiB at `0x000000–0x00FFFF`; on-chip RAM `0xFFF800–0xFFFBFF`.
  Architectural address space is **24-bit** (`0x000000–0xFFFFFF`) — not a flat 32-bit/4-GiB map.
  (Older notes saying H8S/2655 are SUPERSEDED.)
- **IDE/ATAPI controller**: Epson/Roland **SLA919FF0J** custom gate array. The schematic exposes real
  IDE control **and DMA-related** signals (`IDECS*/IDERD/IDEWR/DMAR/DMAW/WAIT`, plus the 40-pin ATA
  connector incl. `DMARQ/DMACK/IORDY/INTRQ`). The old "no DMA, DDRQ/DDRACK not connected" claim is
  **CONTRADICTED**. No public SLA919F programming datasheet has been found (not "confirmed private").
- **Flash**: Sharp **LH28F800SUT-70** — 8 **Mbit** = **1 MiB** total (old "8 MB" claim SUPERSEDED).
  Holds the H8 application image mapped at runtime from `0x100000`.
- **Optional external SCSI**: SP808-OP1 board with an NCR53CF92 controller — a **physically separate**
  storage path from the internal IDE/ATAPI drive.

### Memory map (runtime, 24-bit)

```
0x000000–0x00FFFF   On-chip MCU ROM (Mode 6; contents NOT in the analysis corpus — architectural only)
0x100000+           External flash: H8 application image (IDA base 0x100000; file_off + 0x100000)
0x400000+           External DRAM: inherited platform service layer + application RAM/state
0x400xxx            Inherited DRAM-resident "platform service" ABI (impl. absent from image; provenance UNRESOLVED)
0x401000            Shared storage-service context structure (geometry/extent/status fields)
0x4033E4            Numerical state (word 12000 + binary64 1.0) — NOT a device-type/ZIP variable
0x4104C2 / 0x4110C2 ESP PRAM0 / PRAM1 RAM shadows
0x5D0000            Active filesystem/cache buffer (also A6 ATA IDENTIFY/format scratch)
0x600000–0x60001C   SLA919F task-file-like ATA window (used by A6's internal ATA backend)
0x800000–0x80000E   External SCSI-style target controller registers
0x880000            External target transfer hardware
0xC00000 / 0xC01000 ESP PRAM0 / PRAM1 banks; 0xC02000–0xC02005 ESP control; 0xC00003 bit7 = busy/ready
0xFFF800–0xFFFBFF   On-chip RAM / DTC register information
0xFFFF30–0xFFFF35   DTC enable registers; 0x0450/0x0458 = DTC vector entries (TGI1A/TGI2A)
0xFFFFC0            TPU TSTR (bit1=TPU1, bit2=TPU2); 0xFFFFE0.. TPU1; 0xFFFFF0.. TPU2
```

### Firmware binary layout (leads, not premises)

| Address | Content | Status |
|---------|---------|--------|
| `0x71AC0` | Device-type strings: `ZIP `, `HD  `, `CD  ` | string present |
| `0x71AF0` | Vendor ID strings: `IOMEGA  `, `iomega  ` | string present |
| `0x71B90` | `Roland  ` vendor string | string present |
| `0x71AD0` | SZHC command table | string/table present |
| `0x4B520` / `0x4B523` | Former "device type validation / patch location" | **SUPERSEDED** — see below |

The SP↔A6 `+0x5FDE` string-address shift is a **local** correlation aid only, never a global
relocation rule; verify each correspondence structurally.

## HDD enablement — current understanding

> **The historical two-byte ZIP-gate patch is NOT a demonstrated internal-HDD fix.**

- The explicit `IOMEGA`/`ZIP` identity/acceptance gate lives in the **external, target-indexed
  SCSI-style backend** (`0x12Axxx/0x12Bxxx`, command family `1A/15/06/25/28/2A`, targets 0–7). Bypassing
  it does not enable the internal drive.
- The **internal IDE/ATAPI** Zip path (real ATA PACKET traffic: `A1` IDENTIFY PACKET, `A0` PACKET
  carrying `03/1B/12/5A p2F/55/0D/23/25/1E/A8/AA`) is delegated by SP-808 to **opaque DRAM services**
  `0x400380 / 0x4003A8 / 0x4003AC`. These two backends must not be merged.
- The former patch at file offset `0x4B523` (runtime ~`0x14B523`) was based on reading `0x4033E4` as a
  ZIP device-type compared against `5`. That is **CONTRADICTED**: `0x14B51C` loads `0x4033E4`, adds 5,
  divides by 10 (`0x14B51E` lies inside the operand); `0x4033E4` is numerical state, not a device type.
- **The route that is actually demonstrated:** Edirol A6 firmware runs on SP-808 hardware and operates
  an IDE HDD through an **application-resident native ATA backend** (`0x10058C / 0x100A58 / 0x100B2A /
  0x100D2A`; commands `EC/20/30/91/50/E5`) over the SLA919F task-file window `0x600002–0x60001C`. Data
  movement is **timer-paced H8S DTC** (TPU1/TPU2 → TGI1A/TGI2A, DTC vectors at `0x450/0x458`, endpoint
  `0x600000`) — **not** ATA bus-master DMA.
- **Plan ("Link Plan v2", not yet applied):** relocate A6's bounded ATA envelope (`0x100578–0x101436`
  plus handlers `0x12641C–0x1266BC`) into SP flash around `0x17D000`, with ~64 absolute fixups, splicing
  at the shared logical-volume router (`0x105ED6→0x4003A8` read, `0x105FB2→0x4003AC` write). Keep the SP
  upper filesystem and the external Zip path intact. **Do not patch yet** — unresolved runtime blockers:
  warm ownership of `0x5D0000`, init of the `0x450/0x458` DTC descriptors and selectors `0x48/0xA0/0xB0`,
  the `0xFFFFF0DF[1:2]` transfer-quiescence protocol, and shared `0xFFFFFFC0` users.
- **Status update — a v3 candidate now exists (2026-10-05/06), still NOT applied/flashed:** a
  conservative variant ("cold init + `EC` IDENTIFY + one `READ SECTORS` of LBA 0 → `0x5D0000`, no media
  writes, then park") has been generated as a candidate image
  (`firmware/SP8EXall_LinkPlan_v3_readonly_*.bin`, reconstruct MD5 `9d38db7f…`) plus a MIDI deployment
  set (`firmware/LinkPlan_v3_SMF_*`). Both are independently **byte/payload-verified** against the
  manifest; the omitted code island `[0x7D000,0x7E298)` is transmitted by 25 added packets in file #8.
  Design/manifest/generator/audits live in `analysis/Link_Plan_v3_*`. **Runtime/hardware execution is
  UNRESOLVED — not a release, do not flash.** Generating these artifacts does not resolve the v2
  blockers above.

### MODE SENSE / SZHC spoof

The stock internal ATAPI init includes `MODE SENSE(10) 0x5A` page `0x2F`; `zuluide.ini` spoofs the
vendor response so a ZIP emulator passes. This belongs to Zip **emulation** fidelity, not to the A6
native-ATA HDD transplant.

## IDA Pro Analysis

`IDA/SP808.idc` and `IDA/SP808_IDA_helper.idc` — IDC/Python scripts for IDA Pro.

Setup: load `SP8EXall.bin` as **H8S advanced-mode** (project uses the `h8s300a` startup; the MCU is
H8S/2653 / H8S/2600 core), base address `0x100000` (the executable image begins at file offset `0x20`).
Run the helper script to auto-create named segments, vector table entries, SZHC table markers, and
known string cross-references. Keep analysis **read-only** by default.

`IDA/H8.cfg` — processor config for IDA.

## Key Documentation Files

| File | Contents |
|------|----------|
| `SP-808EX_Evidence_Ledger_*.md` | **Authoritative** clean evidence ledger (use newest revision) |
| `SP-808EX_Observed_Architecture_Technical_Reference_*.md` | **Authoritative** consolidated architecture |
| `Roland_SP-808_Hardware_Architecture_Corrections_*.md` | **Authoritative** hardware/correction record |
| `AGENTS.md` | Evidence discipline / inference rules for this project |
| `analysis/RolandSP-808ZIPDriveValidationBypass.md` | Historical ZIP-check analysis — mostly SUPERSEDED |
| `hardware/Roland_SP-808_CPU.md` | H8S architecture, memory map, PCB pin notes (check against corrections doc) |
| `protocols/Roland_SP-808_to_ZIP_Drive_sniff.md` | Full ATAPI bus trace of SP-808 ↔ internal ZIP drive |
| `analysis/SP-808_SZHC_CommandTableAnalysis.md` | SZHC command table structure |
| `analysis/SP-808_ZIP_DriveInitializationSequenceAnalysis.md` | Boot handshake sequence |
| `firmware/decoding_roland_A6_firmware.md` | MIDI SysEx encoding format internals |
| `Disks/CompactFlashCards.md` | Compatibility notes for CF cards |
| `Disks/SP-808_Demo_Disk_Analysis.md` | FAT16 disk structure analysis |

## Diagnostic / Hidden Modes

Access via button combos on power-on (documented in `things.md`):

- `Status + FX A` — MIDI Update
- `Status + FX B` — ZIP Update  
- `Status + FX C` — Develop Monitor
- `Status + FX D` — Diagnostic Mode
- `1/[5] + CLEAR` then power on — Save OS IMAGE to ZIP disk
- `2/[6] + CLEAR` then power on — Save OS FILE to ZIP disk

Diagnostic (D) mode is application-resident: the boot decision is visible at `0x1258D8` (button query
`0x1381BC`, logical codes `63`+`53`) and enters diagnostic code at `0x123994`. The **Develop Monitor
(C) detector has not been located** in the visible application image; its location and whether it uses
the SCI1 subsystem are UNRESOLVED.

CN7 (unpopulated on PCB, but pads show pogo-contact witness marks): `TX1/RX1/XRST` route the H8S **SCI1**
interface. Firmware configures SCI1 (`SMR1=00, BRR1=09, SCR1=F0`) for a **proprietary ~62,500-baud
request/reply protocol** (tokens `82/8E/90/92/95/96/99/9D/9E`, 21-bit arguments) — distinct from MIDI.
Its peer and any link to the Develop Monitor are UNRESOLVED. A passive 62,500-baud 8N1 capture of `TX1`
across normal / C-mode / D-mode boots is the suggested low-risk experiment (`82 10 8E` is a known
fingerprint).
