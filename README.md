# Roland SP-808 / SP-808EX Reverse Engineering

> # ⚠️ NOT WORKING — DO NOT FLASH
> No firmware modification in this repository is known to enable modern/internal storage on real
> hardware. Any `*_LinkPlan_*` candidate image is an **untested experiment**. Read the status box
> below before doing anything.

Reverse-engineering notes and tools for the Roland SP-808 / SP-808EX sampler (1998), with the
long-term goal of running modern ATAPI/IDE storage (CompactFlash, SD via a CF adapter, ZuluIDE, or an
IDE HDD) in place of the stock Iomega ZIP-100 drive.

> ### ⚠️ Status correction — please read before flashing anything
>
> **There is currently no firmware patch in this repository that is known to enable an internal
> HDD/CF drive on real hardware.** Earlier versions of this README claimed a ZIP-bypass patch was
> "working / validated on hardware (April 2024)." **That claim was not supported by evidence and has
> been retracted.**
>
> - `firmware/patch_sp808.py` flips one branch (`0x12AA14`, `bne`→`bra`) that gates on the drive's
>   device type. That gate lives in the firmware's **external, target-indexed SCSI-style backend**
>   (`0x12Axxx`). The current firmware/data-flow analysis finds that **bypassing it does not enable
>   the internal IDE/ATAPI drive**, which is driven by a different path. The patch has **never been
>   confirmed on hardware**, and the success path it reaches (`zip_device_init`) may still issue
>   Iomega-specific commands a plain HDD/CF will not answer.
> - Treat `patch_sp808.py` as an **experiment**, not a fix. Flashing it is unlikely to achieve the
>   goal and carries the normal risk of a bad flash.
>
> The route that is actually *demonstrated* (Edirol A6 firmware driving an IDE HDD on SP-808 hardware
> via a native ATA backend) is captured as **"Link Plan v2"** in `CLAUDE.md` and the authoritative
> docs below — it is a **transplant plan that has not yet been applied**.

## Document authority (read this first)

This repo deliberately separates **OBSERVED / STRONGLY INFERRED / HYPOTHESIZED / UNRESOLVED /
SUPERSEDED** evidence and contains a lot of older, now-corrected material. **When documents conflict,
newer firmware/data-flow reconstruction wins over inherited names and older prose.** The current
authoritative sources are the newest dated revisions of:

1. [`SP-808EX_Evidence_Ledger_2026-10-05_v11.md`](SP-808EX_Evidence_Ledger_2026-10-05_v11.md) — clean evidence ledger
2. [`SP-808EX_Observed_Architecture_Technical_Reference_2026-10-05_v9.md`](SP-808EX_Observed_Architecture_Technical_Reference_2026-10-05_v9.md) — consolidated architecture
3. [`Roland_SP-808_Hardware_Architecture_Corrections_2026-10-05_v4.md`](Roland_SP-808_Hardware_Architecture_Corrections_2026-10-05_v4.md) — hardware/correction record

[`AGENTS.md`](AGENTS.md) describes the evidence discipline all analysis must follow, and
[`CLAUDE.md`](CLAUDE.md) is the working brief. **Every other `.md` in the repo (including the tables
below and anything in `superseded/`) is a lead, not a premise.**

## What actually works today

| Area | Status |
|------|--------|
| MIDI → binary firmware extraction (`firmware/rolandext.py`) | Working — reproduces `SP8EXall.bin` (786,436 B, MD5 `d744a9cd4a2790ac68d165fd7849b5d8`) |
| ZuluIDE emulating a genuine Iomega ZIP-100 (`zuluide.ini`) | Configuration provided; targets the **stock internal ATAPI ZIP path** — not yet independently hardware-confirmed in this repo |
| IDA Pro firmware analysis (H8S/2653) | Working — see [`IDA/README.md`](IDA/README.md) |
| Internal HDD/CF via a **firmware patch** | **Not demonstrated** — see the status box above |
| A6 native-ATA transplant ("Link Plan v2") | Planned, **not applied**; unresolved runtime blockers remain (see `CLAUDE.md`) |
| `firmware/bin2midi.py` (binary → MIDI reflash) | Implemented; round-trip encode verified, **not yet used to flash real hardware** |

## Two storage paths — do not conflate them

The SP-808 has **two physically separate storage backends**, and most historical confusion comes from
mixing them up:

- **Internal IDE/ATAPI** (the stock ZIP-100 bay, via the Epson/Roland **SLA919FF0J** gate array):
  real ATA `PACKET` traffic. This is the path a replacement CF/HDD/ZuluIDE actually sits on. The
  SP-808 firmware delegates it to opaque DRAM services (`0x400380 / 0x4003A8 / 0x4003AC`).
- **External SCSI** (optional SP808-OP1 board, NCR53CF92): a target-indexed SCSI-style backend
  (`0x12Axxx`). This is where the explicit `IOMEGA`/`ZIP` identity gate lives — and what
  `patch_sp808.py` modifies. **Patching it does not touch the internal drive path.**

## Pragmatic options for real users right now

1. **Use a genuine ZIP-100 drive** (the only configuration the stock firmware is known to accept).
2. **Emulate a ZIP-100** with ZuluIDE using [`zuluide.ini`](zuluide.ini) (PIO 3, UDMA off, 512-byte
   blocks, ZIP identity + MODE SENSE page `0x2F` spoof). This presents the internal bay with something
   the stock firmware treats as a real ZIP, rather than relying on an unproven firmware patch.

There is **no proven drop-in CF/HDD firmware mod yet.** Enabling arbitrary IDE storage is an open
research goal (the A6 transplant), not a finished feature.

## Repository layout

```
firmware/   Firmware images, extraction/patch/reflash tools, encoding notes
hardware/   CPU/flash/opcode references, datasheets, board notes
protocols/  ATA/ATAPI and ZIP-drive protocol references and bus traces
analysis/   Firmware reverse-engineering analysis (SZHC table, strings, patch studies)
Disks/      Disk-image, filesystem, and CF/storage-media analysis
IDA/        IDA Pro scripts and setup for H8S/2653 analysis
superseded/ Prior dated doc revisions, retained for audit trail only — NOT current
```
The authoritative evidence ledger, architecture reference, and hardware-corrections record (the
three dated files listed under "Document authority") stay in the repo root alongside `CLAUDE.md`,
`AGENTS.md`, `README.md`, `TODO.md`, and `things.md`.

## Key documentation

### Hardware
- [CPU and Architecture](hardware/Roland_SP-808_CPU.md) — H8S/2653, memory map, PCB observations *(check against the corrections doc)*
- [Flash Memory](hardware/LH28F800SUT-70.md) — Sharp LH28F800SUT-70 (8 Mbit = 1 MiB)
- [Notes and Overview](hardware/Roland_SP-808_Notes.md) — memory map, firmware load address

### Firmware
- [Firmware Workflow](firmware/readme.md) — extract → (experimental) patch → reflash procedure
- [ZIP Drive Validation Bypass](analysis/RolandSP-808ZIPDriveValidationBypass.md) — **mostly SUPERSEDED** historical patch analysis
- [SZHC Command Table](analysis/SP-808_SZHC_CommandTableAnalysis.md) — ATAPI command-table structure
- [SP-808 vs A6 Firmware](firmware/SP808_Vs_A6_firmware.md) — cross-model comparison

### Protocol
- [ATAPI reference](protocols/ATAPI.md)
- [ZIP Drive Initialization](protocols/SP-808_and_ZIP_Drive.md)
- [Full IDE bus trace](protocols/Roland_SP-808_to_ZIP_Drive_sniff.md) — SP-808 ↔ internal ZIP

### Data format
- [Disk structure](Disks/SP-808_Demo_Disk_Analysis.md) — FAT16, VS2 filenames
- [Mounting disk images](Disks/disk_img.md)
- [CompactFlash notes](Disks/CompactFlashCards.md)

## Hardware at a glance

- **MCU**: Hitachi/Renesas **H8S/2653** (`HD6432653BA11F`, H8S/2600 core), 20 MHz, advanced expanded
  mode. On-chip ROM 64 KiB (`0x000000–0x00FFFF`); on-chip RAM 1 KiB (`0xFFF800–0xFFFBFF`). 24-bit
  address space.
- **IDE/ATAPI controller**: Epson/Roland **SLA919FF0J** gate array (no public programming datasheet
  found).
- **External flash**: Sharp **LH28F800SUT-70** — 8 Mbit = **1 MiB**, holds the H8 application image
  mapped from `0x100000`.
- **Optional external SCSI**: SP808-OP1 board, NCR53CF92 — a separate storage path.

## Diagnostic / update modes (hold on power-on)

| Combo | Mode |
|-------|------|
| Status + FX A | MIDI Update |
| Status + FX B | ZIP Update |
| Status + FX C | Develop Monitor |
| Status + FX D | Diagnostic Mode |

See [`things.md`](things.md) for the full button-combo list. **Note:** the MIDI firmware update is
entered with **Status + FX A**, *not* by holding SHIFT.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) and [TODO.md](TODO.md). Highest-value open items:

- **A6 native-ATA transplant (Link Plan v2)** — resolve the runtime blockers in `CLAUDE.md`
  (`0x5D0000` ownership, `0x450/0x458` DTC init, transfer-quiescence protocol).
- **Hardware test of `patch_sp808.py`** — if you try it, report exactly what happens (it is expected
  *not* to enable the internal drive; a clean negative result is still useful data).
- **VS2 file format**, **CN7 debug UART / SCI1 capture**, **SLA919F protocol** — see `TODO.md`.

## Disclaimer

Not affiliated with or endorsed by Roland. Firmware modification can brick your unit. Nothing here is
a guaranteed fix; the firmware-patch route in particular is unverified. Use at your own risk, on
hardware you own, for preservation and personal use.

## Resources

- [Owner's Manual](docs/SP-808_OM.pdf) · [Service Manual](Roland-SP-808-808-Pro-Service-Manual.pdf)
- RDAC audio decoder — Randy Gordon's external `rdac` project
- [Original discussion thread](https://forum.hddguru.com/viewtopic.php?f=13&t=31086)
