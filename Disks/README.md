# SP-808 Storage Emulation — Findings from ATAPI2SD Development

## Background

These findings come from collaborative work with Konstantin (ATAPI2SD firmware author) 
to get a ZIP drive emulator working with the Roland SP-808EX. The emulator presents 
itself to the SP-808 as an Iomega ZIP 100 device, backed by a disk image on SD card.

This work predates the firmware gate patch and is independent of it. The emulator 
takes the ZIP (type 1) path through `device_classifier` and `device_probe` because 
it correctly responds to IOMEGA vendor string matching. The gate patch is needed for 
plain HDDs and CF adapters that do not identify as IOMEGA.

---

## Commands the SP-808 Issues (confirmed from bus traces)

The SP-808 uses the following ATAPI commands. Any storage emulator or replacement 
device must implement all of them:

| Command | Opcode | Notes |
|---------|--------|-------|
| IDENTIFY PACKET DEVICE | A1h | ATA command, not ATAPI packet |
| SET FEATURES | EFh | Subcommand 0x00 (undocumented/reserved in ATA-5); drive returns ABRT, SP-808 ignores and continues |
| REQUEST SENSE | 03h | Standard |
| START/STOP UNIT | 1Bh | Spin up |
| INQUIRY | 12h | Must return IOMEGA vendor string to pass device_classifier |
| MODE SENSE (10) | 5Ah | Page 0x2F (Iomega vendor page); response must include `2F 04 xx xx 00 03` |
| MODE SELECT (10) | 55h | Writes Iomega vendor page data back |
| Iomega vendor cmd | 0Dh | Proprietary; safe to return success |
| READ FORMAT CAPACITIES | 23h | Must return correct sector count |
| READ CAPACITY | 25h | Must return last LBA and block size |
| PREVENT/ALLOW REMOVAL | 1Eh | Standard |
| READ (12) | A8h | SP-808 uses (12) variant exclusively, not READ(10) |
| WRITE (12) | AAh | SP-808 uses (12) variant exclusively, not WRITE(10) |
| ZIP disk info | 06h | Iomega proprietary; page 2 query |

The use of READ(12) and WRITE(12) rather than the more common (10) variants is 
deliberate. The (12) variants have a 32-bit transfer length field, which while 
unnecessary for a 100MB ZIP disk, appears to be a fixed characteristic of Roland's 
implementation.

---

## Critical: Byte Count Register (DRQ chunk size)

**This was the hardest bug to find and the most important finding for any hardware 
replacement.**

The SP-808's EPSON SLA919F ASIC sets the ATAPI Byte Count Register to `0x0200` 
(512 bytes) before issuing a PACKET command. This tells the device the maximum 
number of bytes it wants to receive per DRQ cycle.

An ATAPI-compliant device must honour this limit. For a multi-sector read 
(e.g. READ(12) for 9 sectors = 4608 bytes), the device must transfer the data 
in 9 separate 512-byte DRQ cycles, not as a single 4608-byte burst.

When the ATAPI2SD emulator sent multi-sector responses as a single burst, the ASIC 
waited approximately 7 seconds and then issued a software reset (SRST), treating it 
as a timeout. This produced the characteristic ~1 second per operation slowdown 
observed with CF adapters.

**Real Iomega ZIP drives handle this correctly by design.** A real PATA HDD also 
handles this correctly — confirmed by the fact that PATA HDDs work in the hardware-
identical Edirol A6 without modification. CF-to-IDE adapters may not always honour 
the byte count register correctly, which would explain the CF adapter slowdown 
independent of any firmware gate issue.

Any storage replacement — emulator or hardware — must respond to DRQ cycles in 
512-byte chunks when the byte count register is set to 0x0200.

---

## Format Sequence

When the SP-808 formats a disk, it writes the following sectors:

- Sector 0: partition/boot record
- Sectors 32-33+: Roland filesystem structures  
- Multiple WRITE(12) commands in sequence, 9 or 64 sectors at a time

If WRITE(12) is not implemented or returns an error, the format appears to succeed 
from the user's perspective (the Roland shows "working") but nothing is written to 
the disk. On the next boot the Roland sees an unformatted disk and reports 
"No disk space" or "Disk full" immediately.

---

## Iomega Vendor-Specific Commands

### MODE SENSE page 0x2F / MODE SELECT

The SP-808 reads the Iomega vendor page via MODE SENSE (5Ah, page code 2Fh) and 
writes it back via MODE SELECT (55h). The response data contains 
`2F 04 xx xx 00 03` — the exact values in the two variable bytes differ between 
100MB and 250MB media configuration.

An emulator must implement page 0x2F in MODE SENSE and accept MODE SELECT without 
error. The exact values returned do not appear to be critically validated beyond 
determining media size tier.

### Command 0x0D

Iomega proprietary command. The SP-808 sends `0D 00 0A 00 00 00 00 00 00 00 00 00` 
during initialisation and also during the media-change polling cycle. Returning a 
success response (good status, no sense) is sufficient.

### Command 0xAA (ZIP disk info, page 2)

Sent as `06 00 02 00 40 00 00 00 00 00 00 00` during the initialisation sequence 
after classification. Returns drive configuration data. An emulator should return 
appropriate ZIP 100 page 2 data.

---

## Confirmed Working Configuration

ATAPI2SD emulator v0.2.7b6 with:
- Iomega ZIP 100 identity (INQUIRY, IDENTIFY, MODE SENSE responses)
- WRITE(12) (0xAA) implemented
- Byte count register honoured (512-byte DRQ chunks)
- READ FORMAT CAPACITIES (0x23) implemented  
- All commands above implemented

Result: full format, read, write, sample record and playback confirmed working on 
Roland SP-808EX.

---

## Relationship to the Firmware Gate Patch

The ATAPI2SD emulator works by presenting itself as an IOMEGA ZIP 100 device. It 
therefore passes through the ZIP (type 1) path in the SP-808 firmware without 
requiring the gate patch at 0x12AA14.

The gate patch at file offset 0x2AA14 (`46 10` → `40 00`) is needed for devices 
that do not identify as IOMEGA — plain PATA HDDs, CF adapters, SD adapters. These 
devices are classified as type 2 or type 3 (HDD) by `device_classifier` and are 
currently rejected at the gate in `device_probe`.

Once the gate patch is applied, these devices will follow the HDD post-classify path 
(`send_prevent_removal_hdd`, `send_format_unit_large_hdd`) rather than the Iomega 
path. The HDD path uses standard ATAPI commands only — no Iomega vendor commands — 
so plain HDDs should work without needing to emulate ZIP behaviour.

The byte count register requirement applies equally to all devices regardless of 
which firmware path they take. Any replacement storage must honour 512-byte DRQ 
chunks.
