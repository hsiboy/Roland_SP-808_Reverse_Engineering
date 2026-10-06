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
> **OBSERVED / documented physical control case:** Complete Edirol A6 application firmware has
> operated an IDE HDD on SP-808 hardware through its native ATA backend. That supports the
> transplant direction; it does not establish success of the SP firmware patch.
>
> **OBSERVED — current experiment:** A **Link Plan v3 candidate BIN** has been generated from the
> checked manifest and independently verified. Eight experimental SMFs reconstruct that BIN
> exactly. **UNRESOLVED:** Hardware updater acceptance and execution remain untested. V3 performs
> cold initialization/IDENTIFY and one 512-byte read, then parks; normal SP operation is not resumed.

## Document authority (read this first)

This repo deliberately separates **OBSERVED / STRONGLY INFERRED / HYPOTHESIZED / UNRESOLVED /
SUPERSEDED** evidence and contains a lot of older, now-corrected material. **When documents conflict,
newer firmware/data-flow reconstruction wins over inherited names and older prose.** The current
authoritative sources are the newest dated revisions of:

1. [`SP-808EX_Evidence_Ledger_2026-10-05_v11.md`](SP-808EX_Evidence_Ledger_2026-10-05_v11.md) — clean evidence ledger
2. [`SP-808EX_Observed_Architecture_Technical_Reference_2026-10-05_v9.md`](SP-808EX_Observed_Architecture_Technical_Reference_2026-10-05_v9.md) — consolidated architecture
3. [`Roland_SP-808_Hardware_Architecture_Corrections_2026-10-05_v4.md`](Roland_SP-808_Hardware_Architecture_Corrections_2026-10-05_v4.md) — hardware/correction record

Authority depends on the claim: the references above consolidate architecture evidence; the
[checked v3 manifest](analysis/Link_Plan_v3_manifest_2026-10-05.json) and
[candidate verification report](analysis/SP8EXall_LinkPlan_v3_readonly_20261005T230456Z_23c5dcc8_verification.json)
establish exact patch bytes; the [SMF audit](analysis/Link_Plan_v3_SMF_audit_2026-10-06.md) and its
verification reports establish payload transport. Hardware success requires hardware observations.

[`AGENTS.md`](AGENTS.md) describes the evidence discipline, and [`CLAUDE.md`](CLAUDE.md) is the
working brief. Older status statements in CLAUDE, TODO and the firmware workflow have not all been
updated to v3 or the SMF audit. Archived documents and inherited IDA names are leads, not independent
evidence. A newer date alone does not establish a claim; follow its primary evidence and scope.

## What actually works today

| Area | Status |
|------|--------|
| Original SMFs → BIN → regenerated SMFs → BIN | **OBSERVED: PASS** with the audited converter: exact 786,436-byte stock image, MD5 `d744a9cd4a2790ac68d165fd7849b5d8`. All eight regenerated `SP808EXv1001.zip` SMFs are also byte-identical to their originals. |
| Legacy `firmware/rolandext.py` | **OBSERVED: FAIL** current audit: append-mode output defeats addressed writes, and original packet/metadata forms are rejected. It is a decoder, not a re-encoder. Do not use it as the verification oracle. |
| ZuluIDE emulating a genuine Iomega ZIP-100 (`zuluide.ini`) | Configuration provided; targets the **stock internal ATAPI ZIP path** — not yet independently hardware-confirmed in this repo |
| IDA Pro firmware analysis (H8S/2653) | Working — see [`IDA/README.md`](IDA/README.md) |
| Internal HDD/CF via a **firmware patch** | **Not demonstrated** — see the status box above |
| A6 native-ATA transplant (Link Plan v3) | **OBSERVED:** Candidate generated; 11 mutation spans and 45 fixups independently verified. No generation blocker remains for the checked inputs. **UNRESOLVED:** Hardware execution, IDENTIFY/read results and later integration with normal SP functionality. |
| V3 SMF conversion | **OBSERVED: PASS** exact candidate payload reconstruction using `analysis/smf_v3_deployment_audit.py`. Legacy `firmware/bin2midi.py` emits malformed SysEx lengths; the `firmware/Bin2Mid.md` example uses incompatible framing/packing. **UNRESOLVED:** Physical updater acceptance. |

## Link Plan v3 artifacts and limits

**OBSERVED:** The [v3 specification](analysis/Link_Plan_v3_2026-10-05.md) defines a cold-init,
IDENTIFY and single ATA READ SECTORS experiment: **LBA 0, count 1, destination `0x5D0000`**.
It preserves A6's runtime DTC-vector handling, changes the SP shell's TGR1A/TGR2A immediate from
`0x0018` to `0x0050`, and relocates the established private globals. The test parks afterward.
It excludes media-writing command producers, formatting, `1008A2`, and normal filesystem routing.

- [Verified candidate BIN](firmware/SP8EXall_LinkPlan_v3_readonly_20261005T230456Z_23c5dcc8.bin)
- [Candidate mutation/fixup verification](analysis/SP8EXall_LinkPlan_v3_readonly_20261005T230456Z_23c5dcc8_verification.json)
- [Experimental SMF bundle](firmware/LinkPlan_v3_SMF_20261005T233407Z_977451bb/LinkPlan_v3_deployment.zip)
- [Per-file hashes, ordering and conversion manifest](firmware/LinkPlan_v3_SMF_20261005T233407Z_977451bb/manifest.json)
- [Independent SMF verification](firmware/LinkPlan_v3_SMF_20261005T233407Z_977451bb/independent_verification.json)
- [SMF framing, metadata and legacy-tool audit](analysis/Link_Plan_v3_SMF_audit_2026-10-06.md)

**OBSERVED:** Candidate BIN identity, also reproduced by decoding the generated SMFs:

```text
Size:    786436 bytes (0xC0004)
MD5:     9d38db7f4cc07f00c30c6022e073ed7d
SHA-256: bcb3d71755dd8b5ca16275af9dc0e490126b9a248fd6794e689fc824c0c2b95a
```

**OBSERVED:** The SMFs preserve the valid Roland EX templates, regenerate packet checksums and
track lengths, and add 25 packets for v3 code in an originally omitted zero-filled range. The
archive named `SP-808EX_v.1001_for_SP-808.zip` has the same firmware payload but stale track lengths
and different model headers; it was not used as the deployment template.

**UNRESOLVED:** Acceptance of the preserved EX model header `2B` by an original SP-808 updater,
the meaning/payload dependency of final metadata byte `4E` (preserved exactly), and physical updater
handling of omitted zero-filled ranges. Exact payload reconstruction does not prove update
acceptance. No hardware execution result is recorded, and v3 does not yet preserve normal SP
operation; that remains the broader transplant objective.

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
- [Link Plan v3](analysis/Link_Plan_v3_2026-10-05.md) — checked read-only experiment specification; its original “not written” status predates candidate generation
- [SMF conversion audit](analysis/Link_Plan_v3_SMF_audit_2026-10-06.md) — current payload proof and transport uncertainties
- [Historical Firmware Workflow](firmware/readme.md) — legacy tool instructions are superseded by the SMF audit
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

- **V3 experimental transport and observation** — establish updater model-header/final-metadata
  requirements and a way to observe IDENTIFY, the one-sector read, and the final park state.
- **Full SP integration after the bounded experiment** — establish warm `0x5D0000` ownership,
  transfer-environment arbitration and retained SP functionality. Preserve the programmed
  `0x450/0x458` vector words and A6's descriptor initialization; rewriting those words is not a v3 prerequisite.
- **VS2 file format**, **CN7 debug UART / SCI1 capture**, **SLA919F protocol** — see `TODO.md`.

## Disclaimer

Not affiliated with or endorsed by Roland. Firmware modification can brick your unit. Nothing here is
a guaranteed fix; the firmware-patch route in particular is unverified. Use at your own risk, on
hardware you own, for preservation and personal use.

## Resources

- [Owner's Manual](docs/SP-808_OM.pdf) · [Service Manual](Roland-SP-808-808-Pro-Service-Manual.pdf)
- RDAC audio decoder — Randy Gordon's external `rdac` project
- [Original discussion thread](https://forum.hddguru.com/viewtopic.php?f=13&t=31086)
