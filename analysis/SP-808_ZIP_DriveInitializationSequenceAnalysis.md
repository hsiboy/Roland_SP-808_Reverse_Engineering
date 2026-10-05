# SP-808 ZIP Drive Initialisation — Bus Trace Analysis

Raw IDE bus traffic captured between a Roland SP-808 and an Iomega ZIP 100
drive during boot. Register numbers refer to the ATAPI task file as seen via
the EPSON SLA919F ASIC.

Register map:
- REG 0 = Data
- REG 1 = Error (read) / Features (write)
- REG 2 = Sector Count / Interrupt Reason
- REG 3 = Sector Number / LBA Low
- REG 4 = Cylinder Low / Byte Count Low
- REG 5 = Cylinder High / Byte Count High
- REG 6 = Device/Head (write) / Alternate Status (read)
- REG 7 = Command (write) / Status (read)

---

## Annotated trace

```
; ── PHASE 1: Hardware reset ─────────────────────────────────────────────────

0:  REG:6 WR 0C   ; Dev Control: SRST=1 (assert software reset)
1:  REG:6 WR 08   ; Dev Control: SRST=0 (release reset), nIEN=1
2:  REG:7 RD 00   ; Status: BSY=0, DRDY=0 — drive not yet ready

; ── PHASE 2: Signature check — is this ATAPI? ───────────────────────────────
; After reset, an ATAPI device posts a signature in the task file registers.
; CylLow=0x14, CylHigh=0xEB is the ATAPI packet device signature.

3:  REG:2 RD 01   ; Sector Count
4:  REG:3 RD 01   ; Sector Number
5:  REG:4 RD 14   ; Cyl Low  = 0x14 ┐
6:  REG:5 RD EB   ; Cyl High = 0xEB ┘ ATAPI signature confirmed
7:  REG:2 RD 01
8:  REG:3 RD 01
9:  REG:4 RD 14   ; signature read again (firmware polling)
10: REG:5 RD EB
11: REG:6 RD 00   ; Alt Status

; ── PHASE 3: IDENTIFY PACKET DEVICE (A1h) ───────────────────────────────────
; Returns 256 words (512 bytes) of drive identification data.
; This is NOT an INQUIRY command — INQUIRY is an ATAPI packet command (0x12)
; sent later. IDENTIFY PACKET DEVICE is an ATA command sent directly.

12: REG:6 WR A0   ; Dev/Head: select device 0
13: REG:7 WR A1   ; CMD: IDENTIFY PACKET DEVICE
14: REG:7 RD 58   ; Status: DRDY=1, DRQ=1 — data ready
15: REG:6 RD 58   ; Alt Status
16: REG:6 WR 08   ; Dev Control: clear interrupt

; IDENTIFY response data (256 words, shown as selected bytes):
; Words are read big-endian pairs from REG:0.

17: REG:0 RD A0   ; Word 0 high: device type = 0xA0xx (ATAPI, packet size 0)
18: REG:0 RD 00

; Words 10-19: Serial number (20 ASCII bytes, byte-swapped)
; --- (words 1-9 omitted) ---
27: REG:0 RD 20   ; serial number bytes (spaces)
28: REG:0 RD 20

; Words 23-26: Firmware revision (8 ASCII bytes, byte-swapped)
; --- omitted ---

; Words 27-46: Model number (40 ASCII bytes, byte-swapped)
; Bytes at offsets 40-51 (word positions 20-25):
40: REG:0 RD 33   ; ┐
41: REG:0 RD 44   ; │
42: REG:0 RD 20   ; │  Model number fragment (byte-swapped):
43: REG:0 RD 20   ; │  "3D  OEA I 0  " — artefact of byte-swap;
44: REG:0 RD 4F   ; │  actual string reads differently when
45: REG:0 RD 45   ; │  de-swapped word by word
46: REG:0 RD 41   ; │
47: REG:0 RD 20   ; │
48: REG:0 RD 49   ; │
49: REG:0 RD 20   ; │
50: REG:0 RD 30   ; │
51: REG:0 RD 20   ; ┘

; Firmware revision (byte-swapped)
55: REG:0 RD 54   ; 'T'
56: REG:0 RD 50   ; 'P'
57: REG:0 RD 20
58: REG:0 RD 20

; Word 49: capabilities
64: REG:0 RD 00
65: REG:0 RD 00

; Word 53
70: REG:0 RD 02
71: REG:0 RD 00
72: REG:0 RD 00

; Words 60-61: total LBA sectors (not valid for ATAPI, usually 0)
84: REG:0 RD F4
85: REG:0 RD F4
86: REG:0 RD 00
87: REG:0 RD 00

; PIO timing
90: REG:0 RD 06
91: REG:0 RD 09
92: REG:0 RD 00
93: REG:0 RD 00

; Additional model/firmware bytes (words 72+):
144: REG:0 RD 01
145: REG:0 RD 63   ; firmware version fragment
146: REG:0 RD 20
147: REG:0 RD 6F
148: REG:0 RD 79
149: REG:0 RD 69
150: REG:0 RD 68
151: REG:0 RD 20
152: REG:0 RD 4F
153: REG:0 RD 45
154: REG:0 RD 41
155: REG:0 RD 31
156: REG:0 RD 39
157: REG:0 RD 20
158: REG:0 RD 00
159: REG:0 RD 00
; --- (remainder of 512-byte response omitted) ---

; ── PHASE 4: SET FEATURES (EFh) — attempt, returns error ────────────────────

273: REG:6 RD 50   ; Alt Status: DRDY=1
274: REG:6 WR A0   ; Dev/Head
275: REG:6 RD 50
276: REG:6 WR A0
277: REG:7 WR EF   ; CMD: SET FEATURES
278: REG:7 RD 51   ; Status: ERR=1 — ZIP drive rejects SET FEATURES
279: REG:6 WR 08
280: REG:1 RD 04   ; Error register: ABRT (command aborted)

; ── PHASE 5: ATAPI PACKET commands via PACKET (A0h) ─────────────────────────
; From here all commands are ATAPI packet commands.
; Each exchange: set up byte count in CylLow/CylHigh, write A0 to CMD,
; wait for DRQ, then write the 6-byte (zero-padded to 12) packet to REG:0.

; --- REQUEST SENSE (03h) ---
281: REG:6 RD 51
282: REG:6 WR A0
; ... (status polling) ...
285: REG:1 WR 00   ; Features
286: REG:2 WR 00   ; Interrupt Reason
287: REG:4 WR 80   ; Byte Count Low = 0x80 (128 bytes)
288: REG:5 WR 00   ; Byte Count High
289: REG:7 WR A0   ; CMD: PACKET
290: REG:7 RD 58   ; Status: DRQ=1 — send packet
291: REG:7 RD 58
292: REG:0 WR 00   ; Packet byte 0: command = 0x00 (Test Unit Ready? pad)
293: REG:0 WR 00
; ... (remaining packet bytes omitted) ...

; --- REQUEST SENSE response ---
298: REG:7 RD 51   ; Status after first packet
; ... (status polling) ...
304: REG:1 WR 00
305: REG:2 WR 00
306: REG:4 WR 80
307: REG:5 WR 00
308: REG:7 WR A0   ; CMD: PACKET
309: REG:7 RD 58
310: REG:7 RD 58
311: REG:0 WR 03   ; Packet byte 0: REQUEST SENSE (03h)
312: REG:0 WR 00
313: REG:0 WR 80   ; Allocation length
314: REG:0 WR 00
315: REG:0 WR 00
; ... ---

; REQUEST SENSE response:
317: REG:7 RD 58
318: REG:7 RD 58
319: REG:0 RD 70   ; Response code = 0x70 (current error, fixed format)
320: REG:0 RD 06   ; Sense key = 0x06 (Unit Attention)
321: REG:0 RD 00
322: REG:0 RD 00
; ...
325: REG:0 RD 29   ; ASC = 0x29 (Power on / reset occurred)
326: REG:0 RD 00
327: REG:0 RD 00
; ...
329: REG:0 RD 01
330: REG:0 RD 24
331: REG:0 RD 00
332: REG:0 RD D0
; Sense: Unit Attention, POWER ON RESET — expected after reset.

; --- START/STOP UNIT (1Bh) — spin up ----------------------------------------
333: REG:7 RD 50   ; Status: DRDY=1, no error
; ... (PACKET setup) ...
343: REG:7 WR A0   ; CMD: PACKET
344: REG:7 RD 58
345: REG:7 RD 58
346: REG:0 WR 1B   ; Packet byte 0: START/STOP UNIT (1Bh)
347: REG:0 WR 00
348: REG:0 WR 01   ; LoEj=0, Start=1 (spin up)
349: REG:0 WR 00
350: REG:0 WR 00
; ... ---

; REQUEST SENSE again after START/STOP:
352: REG:7 RD 51   ; ERR=1 — another sense cycle needed
; ... (PACKET setup) ...
362: REG:7 WR A0
363: REG:7 RD 58
364: REG:7 RD 58
365: REG:0 WR 03   ; REQUEST SENSE (03h)
366: REG:0 WR 00
367: REG:0 WR 80
368: REG:0 WR 00
369: REG:0 WR 00
; ...
373: REG:0 RD 70   ; Response code
374: REG:0 RD 06   ; Sense key = Unit Attention again
; ...
379: REG:0 RD 28   ; ASC = 0x28 (Medium may have changed)
; Sense: Unit Attention, MEDIUM CHANGED — normal after spin-up.

; --- PREVENT/ALLOW MEDIUM REMOVAL (1Eh) — lock media ────────────────────────
; ... (PACKET setup) ...
397: REG:7 WR A0
398: REG:7 RD 58
399: REG:7 RD 58
400: REG:0 WR 00   ; pad / TEST UNIT READY
401: REG:0 WR 00
; ... ---

; --- INQUIRY (12h) ───────────────────────────────────────────────────────────
; Returns 96 bytes of device identification.
; This is the ATAPI INQUIRY command, distinct from IDENTIFY PACKET DEVICE.

; ... (PACKET setup) ...
416: REG:7 WR A0
417: REG:7 RD 58
418: REG:7 RD 58
419: REG:0 WR 12   ; Packet byte 0: INQUIRY (12h)
420: REG:0 WR 00
421: REG:0 WR 80   ; Allocation length
422: REG:0 WR 00
423: REG:0 WR 00
; ...

; INQUIRY response:
427: REG:0 RD 00   ; Peripheral device type = 0x00 (direct access)
428: REG:0 RD 00   ; RMB=0
429: REG:0 RD 75   ; ATAPI version
430: REG:0 RD 00

; Vendor identification (bytes 8-15, 8 chars):
431: REG:0 RD 49   ; 'I'  ┐
432: REG:0 RD 4D   ; 'M'  │
433: REG:0 RD 47   ; 'G'  │  Vendor = "IMG " (byte-swapped pairs)
434: REG:0 RD 20   ; ' '  │  de-swapped: "IMG "... but firmware checks
435: REG:0 RD 5A   ; 'Z'  │  for "IOMEGA  " — this is a different ZIP
436: REG:0 RD 50   ; 'P'  │  variant. The classifier checks vendor at
437: REG:0 RD 31   ; '1'  │  offset +8 of the INQUIRY response buffer
438: REG:0 RD 30   ; '0'  │  stored at 0x5C0000.
439: REG:0 RD 20   ; ' '  ┘

; Product identification (bytes 16-31, 16 chars):
; ... ---
443: REG:0 RD 32   ; '2'
444: REG:0 RD 2E   ; '.'
445: REG:0 RD 30   ; '0'
446: REG:0 RD 2F   ; '/'
447: REG:0 RD 32   ; '2'
448: REG:0 RD 39   ; '9'
449: REG:0 RD 00
450: REG:0 RD 00

; Copyright/additional data:
475: REG:0 RD 28   ; '('
476: REG:0 RD 29   ; ')'
477: REG:0 RD 43   ; 'C'
478: REG:0 RD 70   ; 'p'
479: REG:0 RD 72   ; 'r'
480: REG:0 RD 67   ; 'g'  → "(C)prgt"
481: REG:0 RD 74   ; 't'
482: REG:0 RD 49   ; 'I'
483: REG:0 RD 4D   ; 'M'
484: REG:0 RD 47   ; 'G'  → "IMG"
485: REG:0 RD 20   ; ' '
486: REG:0 RD 39   ; '9'
487: REG:0 RD 37   ; '7'  → "97"
488: REG:0 RD F7   ; end/pad

; ── PHASE 6: MODE SENSE (5Ah) with Iomega vendor page 0x2F ──────────────────
; This is a vendor-specific MODE SENSE page used by Iomega ZIP drives.
; The SP-808 sends this as part of zip_device_init (IDA 0x12B150).
; The response pattern 2F 5C FF D9 is stored in firmware at IDA 0x077B32.
; Whether the firmware strictly validates this response or merely sends
; the command unconditionally is an open question — critical for determining
; whether zip_device_init will stall when talking to a plain HDD.

; ... (PACKET setup) ...
499: REG:7 WR A0
500: REG:7 RD 58
501: REG:7 RD 58
502: REG:0 WR 5A   ; Packet byte 0: MODE SENSE (5Ah)
503: REG:0 WR 2F   ; Page code = 0x2F (Iomega vendor-specific)
504: REG:0 WR 00
505: REG:0 WR 00
506: REG:0 WR 80   ; Allocation length = 128
507: REG:0 WR 00

; MODE SENSE response:
510: REG:0 RD 00
511: REG:0 RD 00
; ...
514: REG:0 RD 2F   ; ┐
515: REG:0 RD 5C   ; │  Iomega vendor page response: 2F 5C FF D9
516: REG:0 RD FF   ; │  Present in all known genuine ZIP drives.
517: REG:0 RD D9   ; ┘  A plain HDD will not return this pattern.

; ── PHASE 7: MODE SELECT (55h) and vendor commands ───────────────────────────
; Post-validation configuration. MODE SELECT sets drive parameters.
; The 0x0D vendor command is Iomega-specific.

; ... (PACKET setup) ...
529: REG:7 WR A0
530: REG:7 RD 58
531: REG:0 WR 55   ; Packet byte 0: MODE SELECT (55h)
532: REG:0 WR 00
533: REG:0 WR 00
; ...
535: REG:0 WR 0E
536: REG:0 WR 00

; MODE SELECT parameter data:
539: REG:0 WR 00
540: REG:0 WR 00
; ...
543: REG:0 WR 2F   ; mode page 0x2F (Iomega vendor page)
544: REG:0 WR 7C
545: REG:0 WR 00
546: REG:0 WR 31   ; '1'
547: REG:0 WR 30   ; '0'
548: REG:0 WR 20   ; ' '  → "10 " — likely capacity-related
549: REG:0 WR 20   ; ' '
; ...
552: REG:0 WR 32   ; '2'

; Vendor-specific command 0x0D (Iomega proprietary):
; ... (PACKET setup) ...
563: REG:7 WR A0
564: REG:7 RD 58
565: REG:7 RD 58
566: REG:0 WR 0D   ; Packet byte 0: Iomega vendor command 0x0D
567: REG:0 WR 0A
568: REG:0 WR 00
569: REG:0 WR 00
; ...
```

---

## Summary

| Phase | Commands | Notes |
|-------|----------|-------|
| 1 | Dev Control reset | Hardware reset/release |
| 2 | Task file read | ATAPI signature check (0x14/0xEB) |
| 3 | IDENTIFY PACKET DEVICE (A1h) | ATA command, returns 512 bytes of drive data |
| 4 | SET FEATURES (EFh) | Rejected by ZIP drive (ABRT) |
| 5 | REQUEST SENSE (03h) | Unit Attention / power-on reset — expected |
| 5 | START/STOP UNIT (1Bh) | Spin up |
| 5 | REQUEST SENSE (03h) | Unit Attention / medium changed — expected |
| 5 | PREVENT/ALLOW REMOVAL (1Eh) | Lock media |
| 5 | INQUIRY (12h) | Returns vendor/product strings used by device_classifier |
| 6 | MODE SENSE (5Ah) page 0x2F | Iomega vendor page; response 2F 5C FF D9 |
| 7 | MODE SELECT (55h) | Drive configuration |
| 7 | Vendor command 0Dh | Iomega proprietary |

---

## Implications for HDD compatibility

Phases 1-5 use standard ATAPI commands that any compliant device should
handle. Phase 6 onwards is specific to Iomega ZIP drives:

The `5A 2F` MODE SENSE with the `2F 5C FF D9` response and the `0x0D` vendor
command in Phase 7 are Iomega proprietary. A plain HDD or CF adapter will not
respond to these correctly.

These commands are issued from `zip_device_init` (IDA 0x12B150), which is
called on the success path after the type gate in `device_probe`. The gate
patch at 0x12AA14 allows HDD device types through to `zip_device_init`, but
whether that function stalls or fails gracefully when the drive does not
respond to the Iomega-specific commands is the primary open question for
hardware testing.

If `zip_device_init` polls for a specific response and times out on failure,
a second patch or a stub replacing that function may be required.
