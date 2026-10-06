<div align="center">

<img src="roland_sp808.jpg" alt="Roland SP-808 groove sampler" width="560">

# Roland SP‑808 / SP‑808EX — Reverse Engineering

**Teaching a 1998 Zip‑drive groovebox to speak to modern storage.**

Firmware, hardware and protocol analysis of the Roland SP‑808 / SP‑808EX — with the long‑term goal of
running CompactFlash, SD (via a CF adapter), ZuluIDE or an IDE HDD in place of the obsolete
Iomega ZIP‑100.

![MCU](https://img.shields.io/badge/MCU-Renesas_H8S%2F2653-0a7bbb)
![Flash](https://img.shields.io/badge/flash-1_MiB_LH28F800-6a737d)
![HDD mod](https://img.shields.io/badge/HDD_mod-experimental-e36209)
![Flashing](https://img.shields.io/badge/flashing-DO_NOT-critical)
![Analysis](https://img.shields.io/badge/analysis-evidence--disciplined-4078c0)

</div>

---

> ## ⚠️ NOT WORKING — DO NOT FLASH
>
> **No firmware modification in this repository is known to enable modern/internal storage on real
> hardware.** Any `*_LinkPlan_*` candidate image or MIDI update set here is an **untested experiment**
> (`runtime_validation: UNRESOLVED`) — *not* a release, and flashing it can brick your unit.
>
> The one thing that works today for real owners is **emulating a genuine ZIP‑100** — see the
> **🎛️ Using it today** section below.

---

## 📖 What this is

The SP‑808 (1998) was designed around an Iomega ZIP‑100 drive that is now obsolete, unreliable and hard
to source. The hardware is perfectly capable of driving a plain IDE device — the near‑identical
**Edirol A6** ships with HDD support — so the restriction is **purely firmware**.

This repo documents, from the ground up:

- the firmware for the Hitachi/Renesas **H8S/2653** MCU,
- the Epson/Roland **SLA919FF0J** IDE/ATAPI gate array and its bus traffic,
- the on‑disk **FAT** layout of SP‑808 Zip disks,
- and an ongoing attempt to **transplant the Edirol A6's native‑ATA HDD backend** into SP‑808 firmware.

> ### 🧭 Read first — evidence discipline
> This project deliberately separates **OBSERVED / STRONGLY INFERRED / HYPOTHESIZED / UNRESOLVED /
> SUPERSEDED** claims, and carries a lot of older, now‑corrected material. **Newer firmware/data‑flow
> reconstruction wins over inherited names and older prose.** Authoritative sources (newest dated):
>
> 📒 [Evidence Ledger](SP-808EX_Evidence_Ledger_2026-10-05_v11.md) ·
> 🏛️ [Architecture Reference](SP-808EX_Observed_Architecture_Technical_Reference_2026-10-05_v9.md) ·
> 🔧 [Hardware Corrections](Roland_SP-808_Hardware_Architecture_Corrections_2026-10-05_v4.md)
> &nbsp;|&nbsp; [`AGENTS.md`](AGENTS.md) (working rules) · [`CLAUDE.md`](CLAUDE.md) (working brief)
>
> Everything else — older revisions, `superseded/`, inherited IDA names — is a **lead, not a premise**.

---

## 📊 Status at a glance

| | Area | State |
|:--:|---|---|
| 🟢 | Firmware extraction (`rolandext.py`, decode) | Reproduces the stock image exactly (MD5 `d744a9cd…`) |
| 🟢 | IDA analysis of the H8S/2653 image | Working — see [`IDA/`](IDA/README.md) |
| 🟢 | On‑disk format | **Solved** — standard DOS/MBR + **FAT12**; extract with [`sp808_fat_extract.py`](Disks/Tools/sp808_fat_extract.py) |
| 🟡 | ZuluIDE emulating a ZIP‑100 (`zuluide.ini`) | Config provided; the practical path for owners (not independently hardware‑confirmed here) |
| 🟡 | A6 native‑ATA transplant (**Link Plan v3**) | Candidate image + MIDI set generated & byte/payload‑verified; **hardware execution UNRESOLVED** |
| 🔴 | Firmware patch enabling internal HDD/CF | **Not demonstrated** |

---

## 🎛️ Using it today

There is **no proven drop‑in CF/HDD firmware mod** yet. Two approaches actually work:

1. **Use a genuine ZIP‑100 drive** — the only configuration the stock firmware is known to accept.
2. **Emulate a ZIP‑100 with ZuluIDE** using [`zuluide.ini`](zuluide.ini) (PIO 3, UDMA off, 512‑byte
   blocks, ZIP identity + `MODE SENSE` page `0x2F` spoof). This presents the internal bay with
   something the stock firmware treats as a real ZIP, rather than relying on an unproven patch.

Enabling arbitrary IDE storage is an open research goal (the A6 transplant), **not** a finished feature.

---

## 🔩 The hardware

<div align="center">
<img src="media/hardware/IMG_20230430_120714_HDR~2.jpg" alt="SP-808 main board" width="720">
<br><em>SP‑808 main board — the H8S MCU, the SLA919FF0J IDE/ATAPI gate array, DRAM/flash and the 40‑pin ATA header.</em>
</div>

| Part | Detail |
|---|---|
| **MCU** | Hitachi/Renesas **H8S/2653** (`HD6432653BA11F`, H8S/2600 core), 20 MHz, advanced expanded mode. 64 KiB on‑chip ROM (`0x000000–0x00FFFF`), 1 KiB on‑chip RAM. 24‑bit address space. |
| **IDE/ATAPI** | Epson/Roland **SLA919FF0J** custom gate array (no public programming datasheet). |
| **Flash** | Sharp **LH28F800SUT‑70** — 8 Mbit = **1 MiB**; holds the H8 application image, mapped from `0x100000`. |
| **Storage (stock)** | Internal ATAPI **Iomega ZIP‑100**. |
| **Optional** | SP808‑OP1 external SCSI board (NCR53CF92) — a *separate* storage path. |

### Two storage paths — do not conflate them

- **Internal IDE/ATAPI** (the stock ZIP bay, via the SLA919FF0J): real ATA `PACKET` traffic — this is
  where a replacement CF/HDD/ZuluIDE actually sits. SP‑808 delegates it to opaque DRAM services
  (`0x400380 / 0x4003A8 / 0x4003AC`).
- **External SCSI** (optional SP808‑OP1): a target‑indexed SCSI‑style backend (`0x12Axxx`). This is
  where the explicit `IOMEGA`/`ZIP` identity gate lives — **patching it does not touch the internal
  drive.**

---

## 🧪 HDD enablement — Link Plan v3

The demonstrated route is that **Edirol A6 firmware drives an IDE HDD on SP‑808 hardware** via an
application‑resident native ATA backend. "Link Plan v3" transplants a **bounded, read‑only** slice of
that backend into SP flash: cold init → `EC` IDENTIFY → one `READ SECTORS` (LBA 0 → `0x5D0000`) → park
(no media writes, no mount/routing, normal SP operation not resumed).

**Verified — bytes only:** a [candidate image](firmware/SP8EXall_LinkPlan_v3_readonly_20261005T230456Z_23c5dcc8.bin)
and an [experimental MIDI deployment set](firmware/LinkPlan_v3_SMF_20261005T233407Z_977451bb/LinkPlan_v3_deployment.zip)
both reconstruct the same candidate — independently checked.

```text
Candidate image   MD5 9d38db7f4cc07f00c30c6022e073ed7d   (786,436 B / 0xC0004)
```

See the [design](analysis/Link_Plan_v3_2026-10-05.md), [verification report](analysis/SP8EXall_LinkPlan_v3_readonly_20261005T230456Z_23c5dcc8_verification.json)
and [SMF audit](analysis/Link_Plan_v3_SMF_audit_2026-10-06.md).

> ⚠️ **UNRESOLVED:** hardware updater acceptance and actual execution. **This is not a release — do not
> flash.** 🛠️ To repack a modified image, use the audited
> [`analysis/smf_v3_deployment_audit.py`](analysis/smf_v3_deployment_audit.py) — the older
> `firmware/bin2midi.py` and the `Bin2Mid.md` example emit malformed SMFs and must not be used.

---

## 🗂️ Repository map

```
├─ analysis/     Firmware RE: SZHC table, strings, Link Plan v2/v3, SMF audit, snapshot design
├─ protocols/    ATA/ATAPI & ZIP-drive references and full bus traces
├─ hardware/     CPU/flash/opcode references, datasheets, board notes
├─ Disks/        Disk-image & FAT analysis, CF compatibility, extraction tools
├─ firmware/     Firmware images, extraction/patch tools, candidate experiments
├─ scripts/      Host-side ATA IDENTIFY utilities
├─ IDA/          IDA Pro scripts & setup for the H8S/2653 image
├─ docs/ media/  Manuals and photos
└─ superseded/   Prior dated doc revisions — retained for audit trail, NOT current
```

The three authoritative dated docs plus `README.md`, `CLAUDE.md`, `AGENTS.md`, `TODO.md` and
`things.md` live in the repo root.

---

## 📚 Documentation

**Hardware** — [CPU & architecture](hardware/Roland_SP-808_CPU.md) ·
[flash](hardware/LH28F800SUT-70.md) · [notes & memory map](hardware/Roland_SP-808_Notes.md)

**Protocol** — [ATAPI reference](protocols/ATAPI.md) ·
[ZIP init](protocols/SP-808_and_ZIP_Drive.md) ·
[full IDE bus trace](protocols/Roland_SP-808_to_ZIP_Drive_sniff.md)

**Analysis** — [SZHC command table](analysis/SP-808_SZHC_CommandTableAnalysis.md) ·
[ZIP‑bypass study (mostly superseded)](analysis/RolandSP-808ZIPDriveValidationBypass.md) ·
[investigation findings](analysis/findings.md)

**Disks** — [demo‑disk / FAT structure](Disks/SP-808_Demo_Disk_Analysis.md) ·
[CompactFlash compatibility](Disks/CompactFlashCards.md) · [extraction tools](Disks/Tools/README.md)

**Firmware workflow** — [historical patch/convert notes](firmware/README.md)

---

## 🔘 Diagnostic & update modes

Hold on power‑on (full list in [`things.md`](things.md)):

| Combo | Mode |
|---|---|
| **Status + FX A** | MIDI Update |
| **Status + FX B** | ZIP Update |
| **Status + FX C** | Develop Monitor |
| **Status + FX D** | Diagnostic Mode |

> The MIDI firmware update is **Status + FX A** — *not* "hold SHIFT", as some older guides claim.

<details>
<summary>✨ Bonus: the boot splash, carved out of the ROM</summary>

<br>The SP‑808EX startup logo was reconstructed directly from firmware bitmaps —
see [`exports/sp808_boot_logo/`](exports/sp808_boot_logo/).
</details>

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) and [TODO.md](TODO.md). Highest‑value open items:

- **Link Plan v3 hardware validation** — does an original updater accept the regenerated EX set
  (model header `2B`, opaque final metadata `4E`), and what do the `EC` IDENTIFY / single read / park
  actually do on hardware?
- **Full SP integration** after the bounded experiment — warm `0x5D0000` ownership, transfer‑environment
  arbitration, retained SP functionality (preserve the programmed `0x450/0x458` vector words).
- **VS2 file format**, **CN7 debug UART / SCI1 capture**, **SLA919F protocol** — see `TODO.md`.

Please keep contributions to the project's evidence discipline — label claims, and don't present
untested work as proven.

---

## 🙏 Credits & disclaimer

RDAC audio decoding: Randy Gordon's external `rdac` project. H8S documentation: Hitachi/Renesas.
Original SP‑808 design: Roland (no affiliation).

Not endorsed by Roland. Firmware modification can brick your unit; nothing here is a guaranteed fix,
and the firmware‑patch route in particular is unverified. **Use at your own risk, on hardware you own,
for preservation and personal use.**

**Resources:** [Owner's Manual](docs/SP-808_OM.pdf) ·
[Service Manual](Roland-SP-808-808-Pro-Service-Manual.pdf) ·
[Original discussion thread](https://forum.hddguru.com/viewtopic.php?f=13&t=31086)
