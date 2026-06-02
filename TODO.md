# TODO

Generated from full project review, June 2026. Updated after remediation pass.

---

## Primary Goal Assessment

The core objective — bypassing ZIP drive validation to enable modern ATAPI storage — **has been achieved** (April 2024). The round-trip toolchain (extract → patch → flash) is now fully documented and implemented.

---

## Resolved (June 2026 remediation)

- **`reset_vector.md`** — wrong chip name (H8S/2655 → H8S/2653) corrected.
- **`Roland_SP-808_CPU.md`** — opening line ambiguity ("HD6432653 or H8S/2653") fixed.
- **`LH28F800SUT-70.md`** — capacity table added, Mbit/MB confusion clarified.
- **`Roland_SP-808_Notes.md`** — memory map section and firmware load address analysis added.
- **`H8S_2655_OpCodes.md`** — renamed to `H8S_2653_OpCodes.md`.
- **IDA `SP808_IDA_helper.idc`** — `BASE_ADDRESS` corrected from `0x8000` to `0x100000`; address calculation formula fixed throughout.
- **`SP808-Dec24_update.md`** — MODE SENSE 0x2F response discrepancy resolved. Bus trace confirms correct response is `2F 5C FF D9`; conflicting code snippet annotated.
- **Firmware base address** — confirmed `0x100000` from reset vector analysis (vector at file offset `0x20` = `01 10 6D F2`, lower 24 bits = `0x106DF2` = file offset `0x6DF2` at runtime). Documented in `Roland_SP-808_Notes.md`.
- **`firmware/patch_sp808.py`** — extracted from `RolandSP-808ZIPDriveValidationBypass.md` into a runnable script.
- **`firmware/bin2midi.py`** — written from scratch with correct 7-bit encoding (verified against `rolandext.py`'s decoder). Replaces the broken nibble-splitting version in `Bin2Mid.md`.
- **`firmware/README.md`** — full extract → patch → flash workflow documented.
- **`README.md`** — removed broken references to `software/`, `research/`, wiki links, and non-existent Releases. Replaced with local file links.
- **`CONTRIBUTING.md`** — created.
- **`hardware/datasheets/README.md`** — index created with notes on what each PDF covers and what's missing.
- **`interestingStrings.md`** — filled in SP-808 and A6 columns with confirmed data from analysis docs.
- **`HARDWARE_CORRECTIONS_2026-05.md`** — all checklist items marked done; load address row updated; document marked as archived.

---

## Still Open — Requires Hardware Access

These items cannot be resolved by code or documentation work alone:

### CN7 UART / debug port
The unpopulated CN7 connector breaks out TX1 (pin 32), RX1 (pin 33), and XRST (pin 31) from the H8S/2653 serial port 1. Multiple docs note "TODO - Sniff TTY". A logic analyser or USB-serial adapter on these pins during boot would reveal whether diagnostic strings are emitted. If the port is compatible with H8/300 debug tools (E6000), it could enable single-step debugging.

### Memory relocation code
Strings present at `0x17xxxx` in the flash binary are accessed from `0x4xxxxx` runtime RAM addresses in the device register map. The initialisation code that copies them has not been located. Finding it would confirm the full boot sequence and explain the RAM layout.

### VS2 file format
`SONG0000VS2`, `EFFECT__VS2`, `PADBANK_VS2`, `SAMPLE__VS2`, `TAKE0000VS2`, `WAVELISTVS2`, `PADBANK_VS2` filenames are known from disk analysis but the internal binary format is undocumented. Requires a disk image and hex analysis.

### A6 device types 0x07 and 0x08
`HARDWARE_CORRECTIONS_2026-05.md` noted the A6 firmware has code paths for device types beyond ZIP (suspected HDD types). A full A6 firmware analysis to confirm is outstanding.

### Complete Epson SLA919F ASIC protocol
No public datasheet. Vendor commands `0x06` and `0x0D` are partially mapped from the bus trace but not fully understood. Extended bus traces of the full boot sequence would help.

### Masked ROM boot sequence
The on-chip ROM (`0x000000–0x00FFFF`) initialises hardware and jumps to the external flash at `0x100000`. Its contents cannot be read without decapping or a debug trace. A logic analyser capture of the address bus during cold boot would show the jump sequence.

---

## Still Open — Documentation / Housekeeping

### `bin2midi.py` hardware verification
The round-trip encode/decode test confirms correct encoding but does not substitute for a real flash. Someone needs to flash a patched SP-808 using `bin2midi.py` output and confirm it boots. Until then, the script carries its `WARNING` header.

### RDAC audio format documentation
The README credits Randy Gordon's external `rdac` project but there is no documentation of the Roland RDAC compression format in this repo. A brief doc describing the format structure and pointing to the decoder would help contributors.

### Repo restructuring
The root directory has ~20 markdown files with no grouping. A suggested layout:
```
protocols/    ATAPI.md, PIO_Mode.md, Programming_ATA_And_ATAPI.md,
              SP-808_and_ZIP_Drive.md, Roland_SP-808_to_ZIP_Drive_sniff.md
hardware/     Roland_SP-808_CPU.md, Roland_SP-808_Notes.md, LH28F800SUT-70.md,
              H8S_2653_OpCodes.md, H8_300-Op-Codes.md, FX.md
disks/        (merge with Disks/) disk_img.md, disks.md, Zip_Disks.md,
              Zip_drives.md, CompactFlashCards.md, Compact_Flash.md
analysis/     SP-808_SZHC_CommandTableAnalysis.md, RolandSP-808ZIPDriveValidationBypass.md,
              SP-808_ZIP_DriveInitializationSequenceAnalysis.md, interestingStrings.md,
              SP-808EX_strings.md, A6_firmware_strings.txt, SP808-Dec24_update.md
```
Not done because moving files would break internal links across docs.

### `Compact_Flash.md` vs `CompactFlashCards.md`
These two files cover similar ground (CF card pin tables, ATA modes). They should be merged or clearly differentiated in scope.

### `SP-808EX_strings.md`
Large raw string dump. Needs a summary section explaining what was found and cross-referencing the relevant analysis docs.
