# Roland SP-808 — HDD/CF Storage Mod

Reverse engineering and firmware patching to enable non-Zip IDE storage on the
Roland SP-808 groovebox.

The SP-808 uses an Iomega Zip drive as its primary storage. The hardware is
fully capable of driving a plain IDE HDD or CF adapter — the identical Edirol
A6 hardware ships with HDD support. The restriction is purely firmware.

> **Experimental candidate images — DO NOT FLASH.** Files named
> `SP8EXall_LinkPlan_v*_*.bin` here are the A6 native-ATA transplant experiment
> (see `../analysis/Link_Plan_v3_*.md`). Their *bytes* are independently verified
> against the manifest and they are regenerable with `../analysis/link_plan_v3.py`,
> but `runtime_validation` is **UNRESOLVED** — never hardware-tested, not a release.
> Flashing one is at your own risk and may brick the unit.

---

## Current Status

A candidate 2-byte change has been identified at `0x12AA14` that removes a
ZIP-only device-type gate. **It is an experiment, not a working fix.**

> **Important:** this gate lives in the firmware's **external, target-indexed
> SCSI-style backend** (`0x12Axxx`), which is a *separate* storage path from the
> internal IDE/ATAPI bay the ZIP drive actually uses. The current firmware
> data-flow analysis (see `../CLAUDE.md` and the authoritative docs in the repo
> root) finds that **bypassing this gate is not expected to enable the internal
> drive.** The patch has **never been confirmed on hardware**, and the success
> path it reaches (`zip_device_init`) may still issue Iomega-specific commands a
> plain HDD/CF will not answer.

This page documents the older `patch_sp808.py` gate experiment and the legacy
tool workflow; it is **historical**. The forward path for real HDD support is the
Edirol A6 native-ATA transplant — now at **Link Plan v3** (`../analysis/Link_Plan_v3_*`),
for which a candidate image and a MIDI deployment set exist but remain
**experimental and untested on hardware** (not applied, not a release).

---

## How It Works

The SP-808 firmware classifies attached IDE devices into three types:

| Type | Meaning                              |
|------|--------------------------------------|
| 1    | ZIP (IOMEGA vendor string matched)   |
| 2    | HDD, small (geometry < 0x951229)    |
| 3    | HDD, large (geometry >= 0x951229)   |

The classifier (`device_classifier`, IDA 0x12AE88) correctly identifies and
types any drive, including plain HDDs and CF adapters. However, the calling
function (`device_probe`, IDA 0x12A956) contains a gate that rejects anything
that is not type 1:

```asm
cmp.b  #1, r0l       ; is device type ZIP?
bne    loc_12AA26    ; reject if not  ← patch target
```

The patch changes this `bne` (branch if not ZIP) to `bra` (branch always),
allowing types 2 and 3 through.

| File offset | Original   | Patched    | Effect                     |
|-------------|------------|------------|----------------------------|
| `0x2AA14`   | `46 10`    | `40 00`    | `bne +0x10` → `bra +0x00` |

---

## Quick Start

### Requirements

- SP-808 firmware update ZIP: `SP-808EX_v.1001_for_SP-808.zip`
- Python 3
- MIDI interface connected to SP-808 MIDI IN
- `rolandext.py` (decode) and `patch_sp808.py` (this repo); for repacking use
  `../analysis/smf_v3_deployment_audit.py` (see Step 3 — **not** `bin2midi.py`)

### Step 1 — Extract firmware binary

```bash
for f in SP8EX'#'?.mid; do python rolandext.py model=sp808 infil="$f" outfil=SP8EXall.bin; done
```

Produces `SP8EXall.bin` (786,436 bytes, MD5: `d744a9cd4a2790ac68d165fd7849b5d8`).

### Step 2 — Apply patch

```bash
python patch_sp808.py SP8EXall.bin SP8EXall_patched.bin
```

The script verifies the input MD5, confirms patch bytes before writing, and
prints the output MD5.

### Step 3 — Convert a modified image back to a MIDI update set

> **Do not use `bin2midi.py` for this.** The 2026-10-06 SMF audit found it emits
> malformed SysEx (bad length framing, invented packet layout, dropped metadata),
> and `rolandext.py`'s re-encode path has an append-mode bug (wrong output size).
> Use the audited converter `../analysis/smf_v3_deployment_audit.py`, which
> regenerates a valid Roland EX update set and independently verifies that decoding
> it reconstructs the input image byte-for-byte. See
> `../analysis/Link_Plan_v3_SMF_audit_2026-10-06.md`.

### Step 4 — Apply (experimental)

A generated set is sent through the stock Roland **MIDI Update** mode (entered with
**Status + FX A** on power-on; see `../things.md`). **This is experimental — see the
DO NOT FLASH notice at the top of this page.** No candidate in this repo has been
validated on hardware, and updater acceptance of a re-generated set is UNRESOLVED.

---

## Known Issues / Next Steps

The success path after the gate calls `zip_device_init` (IDA 0x12B150), which
was written for ZIP drives and may issue Iomega-specific ATAPI commands. If it
does, a plain HDD or CF adapter will not respond correctly and init may stall.
This requires investigation once the gate patch is tested.

The unit also exhibits a ~1 second lag per operation when a CF adapter is
attached with unpatched firmware. Whether this is caused by the gate rejection
loop, a timeout in the mask ROM ATAPI primitive, or something else is not yet
determined.

See the authoritative evidence ledger and architecture reference in the repo
root (listed in `../README.md` → "Document authority") for the full, current
findings and open-inquiry list.

---

## Repository Contents

| File                  | Description                                          |
|-----------------------|------------------------------------------------------|
| `patch_sp808.py`      | Applies the gate patch to `SP8EXall.bin`             |
| `rolandext.py`        | Extracts firmware binary from Roland MIDI SysEx files|
| `bin2midi.py`         | **SUPERSEDED / broken** repacker (SMF audit) — use `../analysis/smf_v3_deployment_audit.py` |

---

## Hardware

- MCU: Hitachi/Renesas H8S/2653 (`HD6432653BA11F`, H8S/2600 core), 20 MHz
- IDE ASIC: EPSON/Roland SLA919FF0J gate array
- External flash: Sharp LH28F800SUT-70, 8 Mbit = 1 MiB
- On-chip mask ROM: `0x000000–0x00FFFF` (not patchable); the patchable application
  image is the external flash mapped from `0x100000`.

IDA Pro setup: load `SP8EXall.bin` as **H8S advanced mode** with base address
`0x100000` (executable image begins at file offset `0x20`). Run
`../IDA/SP808_IDA_helper.idc` after loading.

---

## References

- H8S/2653 Hardware Manual (Renesas)
- EPSON SLA919F datasheet
- Iomega Zip ATAPI specification
