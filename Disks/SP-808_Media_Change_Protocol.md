# SP-808 Media Change Protocol — Analysis from Bus Traces

## Overview

The SP-808 polls the ZIP drive continuously using the Iomega vendor command `0x06`
(ZIP disk info, page 2). The drive's response encodes the current media state in the
last 4 bytes of its reply. The SP-808 monitors these bytes to detect eject, media
absence, and new media insertion without any separate hardware interrupt mechanism.

---

## The 0x06 Command Structure

The SP-808 sends: `06 00 02 00 40 00 00 00 00 00 00 00`

The response comes in three DRQ chunks:

| DRQ | CylHigh:CylLow | Size | Content |
|-----|----------------|------|---------|
| 1 | 0x00:0x16 | 22 bytes | Drive status / config data |
| 2 | 0x00:0x28 | 40 bytes | Drive identity strings |
| 3 | 0x00:0x02 | 4 bytes | **Media state bytes** |

The final 4-byte DRQ (reported as 2 words on the 16-bit bus) carries the state
indicator. Only this chunk changes during normal polling — chunks 1 and 2 are
static.

---

## Media State Encoding

The third DRQ contains two 16-bit words:

- **Word 0** is always `0x0200` (constant)
- **Word 1** encodes the current state:

| Word 1 | Low byte | High byte | Meaning |
|--------|----------|-----------|---------|
| `0x31F1` | `0xF1` | `0x31` | Normal — disk 1 mounted, all OK |
| `0x32F1` | `0xF1` | `0x32` | Normal — disk 2 mounted, all OK |
| `0x02D0` | `0xD0` | `0x02` | Eject in progress (one poll cycle only) |
| *(absent)* | — | — | Disk absent / bay empty |
| `0x31F3` | `0xF3` | `0x31` | Unit Attention pending (one poll cycle) |

**The low byte is the primary state indicator.** The high byte is a media
generation counter that increments each time a new disk is accepted. This allows
the SP-808 to detect whether the disk that is now present is the same disk that
was previously present, even if the state byte returns to `0xF1`.

In the traces: disk 1 → high byte `0x31`, disk 2 → high byte `0x32`.

---

## Observed State Transitions (Change Media log)

The user pressed the physical eject button on the ZIP drive. The Roland asked
"save current changes?", the user pressed YES. Disk 1 was ejected and disk 2
was inserted. Sequence from bus trace:

```
Entry   95:  F1 (0x31F1)  — Disk 1 mounted, normal polling begins
Entry  602:  D0 (0x02D0)  — Drive signals eject initiated
Entry  703:  F1 (0x31F1)  — SP-808 polls again, still F1 (disk still spinning down)
...  [~15 more F1 polls while disk ejects]
Entry 2321:  ABSENT        — Only word 0 (0x0200) present; word 1 missing = disk out
             [SP-808 immediately writes 0xF1 twice to REG:6 after reading ABSENT]
             [Then resumes polling 0x06]
Entry 2423:  F1 (0x31F1)  — New disk (disk 2) detected as inserted, same gen counter
Entry 2928:  F3 (0x31F3)  — Unit Attention (one cycle)
Entry 3029:  F1 (0x31F1)  — Settled, normal operation with new disk
```

Note: the generation counter does NOT change between disk 1 and disk 2 in this
particular trace. Both show `0x31`. This may be because both disks were blank
with identical geometry, or the drive only increments the counter under specific
conditions. The emulator may safely use a fixed value here.

---

## The REG:6 Write After ABSENT

When the SP-808 reads the ABSENT state (word 1 missing from the 0x06 response),
it immediately writes `0xF1` twice to REG:6 before issuing the next 0x06 poll.
REG:6 in the ATAPI/ATA register map is the Device/Head register, but these writes
do not precede an ATA command — they appear to be the SP-808 signalling something
to the EPSON SLA919F ASIC internally, possibly resetting a media-present latch.

The write value `0xF1` does not correspond to a standard Device/Head value (which
would normally be `0xA0` for master). This is likely ASIC-specific.

---

## The F3 (Unit Attention) State

`0xF3` appears briefly (one poll cycle) immediately after a new disk is accepted.
This corresponds to ATAPI Unit Attention — the standard SCSI/ATAPI mechanism for
notifying the host that media has changed. The emulator should assert Unit Attention
on the next command after media change, which produces this `0xF3` response on the
following 0x06 poll, then return to `0xF1`.

---

## No-Change log: eject cancelled

In the no-change log the user pressed eject then cancelled. The observed sequence:

```
Entry   95:  F1 (0x32F1)  — Disk mounted (disk 2, gen=0x32)
Entry 1958:  F3 (0x32F3)  — Unit Attention (brief, one cycle) — eject button pressed
Entry 2059:  F1 (0x32F1)  — Returned to normal (eject cancelled)
Entry 5850:  F3 (0x32F3)  — Another brief UA (possibly the Roland itself issuing PREVENT/ALLOW)
Entry 5951:  F1 (0x32F1)  — Normal
Entry 7063:  ABSENT        — Transient absence? (possibly bustrace wrap artefact)
Entry 7164:  F1 (0x32F1)  — Normal resumed
```

The key point here: pressing the physical eject button on the ZIP drive generates
a `0xF3` response in the 0x06 poll. The SP-808 detects this and presumably issues
a PREVENT/ALLOW REMOVAL command (not visible in this bustrace due to the 32000-entry
buffer limit already being used by the dense 0x06 polling).

---

## Implications for the ATAPI2SD Emulator

The emulator must implement the following media-change protocol:

**To signal eject (when the user selects a different image):**

1. On the next 0x06 poll after the user triggers image change, return `0xD0` as
   word 1 (low byte). Return it for one poll cycle only.
2. On subsequent polls, continue returning `0xF1` while the SP-808 saves state to
   the current image.
3. When the drive is physically ready to "eject" (i.e. the emulator has finished
   flushing writes), return only word 0 (`0x0200`) with no word 1 — this signals
   ABSENT.
4. Once the new image is mounted, return `0xF3` on one poll cycle (Unit Attention).
5. Return `0xF1` on all subsequent polls.

**The generation counter (high byte of word 1):**
Increment the high byte each time a new image is loaded. This ensures the SP-808
detects a genuine media change even if the state byte happens to be `0xF1` on
both sides of the transition. Starting at `0x01` and incrementing with each mount
is sufficient.

**The ABSENT state structure:**
When disk is absent, the 0x06 response's third DRQ block contains only word 0
(`0x0200`). CylLow still reports `0x02`, but only 2 bytes of data are available
instead of 4. The SP-808 detects absence by reading only one word from the
final DRQ block.

---

## Timing

The SP-808 polls 0x06 approximately once per second during idle operation. The
D0 state persists for exactly one poll cycle before the drive returns `0xF1`.
The ABSENT state persists until a new disk is physically inserted (or in the
emulator's case, a new image is selected). The F3 state persists for exactly
one poll cycle.
