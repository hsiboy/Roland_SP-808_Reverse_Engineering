# SP-808 SZHC Command Table Analysis

## Location

SP-808 firmware, IDA 0x171ACF (file offset 0x071ACF).

A6 firmware equivalent at 0x177AAD (offset ~0x5FDE higher, consistent with
the general string block offset between the two builds).

---

## Structure

The block at 0x171ACF contains the device type strings and ATAPI command
table used during IDE device initialisation. The layout is:

```
0x171ABB  "SELF"<0>          ; device type string
0x171AC0  "ZIP "<0>          ; device type string
0x171AC5  "HD  "<0>          ; device type string
0x171ACA  "CD  "<0>          ; device type string
0x171ACF  "-SZHC"            ; signature (no null terminator)

0x171AD4  06 00 00 00 00 00 00   ; SZHC command entry 0: reset/null
0x171ADB  06 1B 00 00 00 00 00   ; SZHC command entry 1: START/STOP UNIT
0x171AE2  06 1E 00 00 00 00 00   ; SZHC command entry 2: PREVENT/ALLOW MEDIA REMOVAL
0x171AE9  06 03 00 00 00 00 00   ; SZHC command entry 3: REQUEST SENSE

0x171AF0  "IOMEGA  "<0>      ; vendor string (upper case)
0x171AF9  "iomega  "<0>      ; vendor string (lower case)
0x171B02  "ZIP"<0>           ; product string
```

The 4-entry command table ends at 0x171AF0. The vendor and product strings
that follow are separate data used by `device_classifier` for string
comparison, not part of the command table itself.

---

## Command entry format

Each entry is 7 bytes:

| Offset | Field   | Description                        |
|--------|---------|------------------------------------|
| 0      | marker  | Always `0x06`                      |
| 1      | command | ATAPI command byte                 |
| 2-6    | params  | Command parameters (usually zero)  |

The `0x06` marker is not an ATAPI command length field. It appears to be a
protocol marker used by the EPSON SLA919F ASIC interface layer. The MCU does
not talk directly to the IDE bus; all IDE communication is mediated by the
ASIC, and this 7-byte format defines the MCU-to-ASIC command structure.

---

## SZHC signature

The 5-byte string `-SZHC` immediately precedes the command table. The most
likely interpretation is that each character maps to a supported device type:

| Char | Device type |
|------|-------------|
| S    | SELF        |
| Z    | ZIP         |
| H    | HD          |
| C    | CD          |

The leading `-` byte is referenced directly by `sub_1080B6` as a data value
(`0x2D`), suggesting the full 5-byte sequence serves as a combined signature
and device-type bitmap rather than a plain ASCII label.

---

## Device type codes

The firmware assigns numeric codes to device types after classification:

| Code | String | Meaning                              |
|------|--------|--------------------------------------|
| 0    | —      | Uninitialized / no device            |
| 1    | ZIP    | Iomega ZIP (vendor string matched)   |
| 2    | HD     | HDD, geometry value < 0x951229      |
| 3    | HD     | HDD, geometry value >= 0x951229     |

CD (`C`) and SELF (`S`) appear in the string table and signature but have no
corresponding classification path in the SP-808 firmware as analysed. They
may be present due to shared code heritage with the A6, which has SCSI/CD
support.

---

## How the command table is used

`device_probe` (IDA 0x12A956) calls two functions that walk the command table:

- `atapi_cmd_sequence_full` (0x12AA72): starts at entry 0 (0x171AD4).
- `atapi_cmd_sequence_partial` (0x12AAF2): starts at entry 1 (0x171ADB,
  START/STOP UNIT), skipping the reset/null entry.

Both functions pass a pointer into the table and a length of 7 to
`atapi_command_handler` (0x12B712), which sends the command via the ASIC
and checks the response.

---

## Hardware context

- MCU: Hitachi H8S/2653 — does not drive the IDE bus directly.
- ASIC: EPSON SLA919F — mediates all IDE communication.
- No DMA: DDRQ and DDRACK pins on the ASIC are not connected.
- The 7-byte command format is the MCU-to-ASIC protocol, not raw ATAPI.

---

## What this is not

The SZHC table is not an authentication or security mechanism. It is a
straightforward initialisation sequence: reset, spin up, lock media, sense
status. The vendor string checks (`IOMEGA`, `ZIP`) that follow in
`device_classifier` are device identification, not validation. Both the
IOMEGA-match path and the non-match (HDD geometry) path are accept paths
that write a type code and return success.

The actual ZIP-only restriction is enforced one level up in `device_probe`,
at IDA 0x12AA14, where a `bne` rejects any classified device that is not
type 1. That is the patch target.
