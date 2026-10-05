Roland SP-808 / SP-808EX Reverse Engineering Evidence Ledger and Clean
Project State

Rebuilt 2 October 2026 • Updated 4 October 2026 • Firmware-first •
Provenance-strict

# Purpose and governing rule

This document is a clean evidence ledger for the SP-808/SP-808EX
reverse-engineering project. It consolidates primary hardware/file facts
and the independently re-walked firmware findings obtained in the
current H8S database. It deliberately separates observation from
inference and records superseded claims so that old LLM or human
assumptions do not become circular evidence.

Core rule: firmware and primary evidence first; existing interpretation
second. A plausible semantic explanation is useful only when its
evidence chain remains visible.

  ---------------------- ----------------------------------------------------------------------------------------------------------------- ----------------------------------------------------------
  Status                 Meaning                                                                                                           Use
  OBSERVED / CONFIRMED   Directly established by bytes, instructions/data flow, schematic/manual evidence, or recorded physical testing.   May be used as a premise.
  STRONGLY INFERRED      Multiple independent observations converge on a semantic interpretation.                                          May guide work, but retain the evidence chain.
  HYPOTHESIZED           Plausible explanation requiring further verification.                                                             Use to design tests; do not rename facts around it.
  UNRESOLVED             Evidence is missing or contradictory.                                                                             Do not bridge the gap with assumptions.
  SUPERSEDED             An older project claim is contradicted or materially corrected by newer evidence.                                 Keep only as history/warning; do not reuse as a premise.
  ---------------------- ----------------------------------------------------------------------------------------------------------------- ----------------------------------------------------------

# 1. Reproducible target and environment

Target firmware: SP8EXall.bin.

File size: 786,436 bytes (0xC0004). Recorded MD5:
d744a9cd4a2790ac68d165fd7849b5d8.

Container/header observations: 32-byte header; executable content begins
at file offset 0x20; runtime mapping used by the project is runtime =
file_offset + 0x100000.

IDA Pro 9.0, H8 processor module, H8S advanced-mode target. Current
startup selection is h8s300a; project hardware documentation identifies
the MCU as H8S/2653 / H8S/2600-core.

The current IDA input and repository firmware were independently
reported as matching; the latest investigation also reported matching
SHA-256 between the inspected repository image and open database.

Analysis must remain read-only by default. Existing names/comments/types
are navigation aids, not evidence.

# 2. Primary hardware and product context

These facts are legitimate context for inference, but product context
must not be used as a substitute for code/data-flow evidence.

The SP-808 is a musical sampler/workstation with samples, pads/banks,
projects, MIDI, audio recording/playback, front-panel UI, removable
storage, and optional SCSI functionality.

Project service-manual/schematic work identifies the main MCU as
Hitachi/Renesas H8S/2653 and the storage interface gate array as
SLA919FF0J.

The schematic establishes a conventional ATA/ATAPI electrical interface
with IDE register selects, chip selects, DIOR/DIOW, IORDY, INTRQ, RESET,
DD0-DD15 and DMA handshake signals.

A6 firmware was physically run on SP-808 hardware with an IDE HDD,
demonstrating that the board hardware can operate an HDD; this does not
by itself establish what stock SP-808EX firmware accepts.

Recorded CF-adapter behavior: unit boots/runs but operations are heavily
delayed; formatting appeared to complete but no files were written. The
historical test\'s exact firmware/patch state was not recorded and
therefore limits interpretation.

# 3. Methodological correction: what went wrong in the old analysis

The project contained a particularly instructive failure mode. Nearby
strings and regular-looking numeric values were visually grouped into a
supposed \"media-size policy table.\" From that, 0x427C4A was described
as a media-size/UI index and values 25,000 / 125,000 / 250,000 / 625,000
were treated as Zip-size thresholds. Independent consumer analysis
falsified that structure interpretation.

The constants do not numerically match the known Zip 100/250 media
capacities in raw 512-byte blocks, KiB, or bytes; resemblance was not
sufficient evidence.

The region actually contains multiple structures with different record
widths. Structure boundaries must be derived from consumers, not visual
adjacency.

This example should remain in the project as a contamination warning:
plausible pattern recognition can become a self-reinforcing false
narrative when semantic names, documentation and TODOs all inherit the
same original guess.

# 4. Correct reconstruction of the 0x174Bxx region

## 4.1 Six-byte timed-action records

OBSERVED: the sequence at 0x174B1C-0x174B45 is seven packed six-byte
records:

typedef struct {

uint32_t delay_ticks;

uint16_t control;

} TimedRecord; // 6 bytes, big-endian target

  ---------- ------------- ---------
  Address    delay_ticks   control
  0x174B1C   625000        0x8064
  0x174B22   125000        0x0046
  0x174B28   250000        0x8064
  0x174B2E   125000        0x0046
  0x174B34   250000        0x8064
  0x174B3A   125000        0x0046
  0x174B40   125000        0x0000
  ---------- ------------- ---------

The installer at 0x155702 stores a descriptor pointer and captures a
counter from 0x148D2E. The consumer around 0x15575C subtracts the saved
counter, compares elapsed ticks directly with the record longword,
performs the control action after the threshold, and advances the
descriptor pointer by exactly six bytes. A zero control terminates the
sequence. Conversion from counter ticks to seconds remains
unestablished.

Independent corroboration: another consumer compares an elapsed value
from the same counter source against 125000.

SUPERSEDED: these particular occurrences are not media-capacity
thresholds.

## 4.2 Eight-byte UI records and pointer pairs

typedef struct {

uint16_t field_00; // tag = field_00 & 0xF800; parameter = field_00 &
0x07FF

uint16_t field_02;

uint32_t field_04;

} UiRecord; // 8 bytes

typedef struct {

uint32_t display_records;

uint32_t timed_records;

} PointerPair; // 8 bytes

The UI interpreter at 0x138560 advances by eight bytes and interprets
operation tags from the high bits of field_00. The Copy Disk table
begins at 0x174B46 and contains sixteen pointer pairs. The first pointer
selects display data; the second optionally selects a timed-action
descriptor.

# 5. 0x427C4A: corrected semantics

STRONGLY INFERRED, high confidence: 0x427C4A is a 16-bit workflow state
word shared by Copy FX Patches and Copy Disk. It is not a media-capacity
classification variable.

Five identifiable store instructions write the word (0x135A1E, 0x135A5A,
0x135ADA, 0x135B9E, 0x135BDC). Recovered callers produce states 0-15.
Consumers dispatch operation sequencing, display descriptors, timed
feedback and progress behavior.

## 5.1 Copy FX states

  ------- ----------------------------
  State   Observed display meaning
  0       Insert / Destination Disk.
  1       Not SP-808 Disk.
  2       Copy FX Patches.
  3       Copy FX Canceled.
  4       Copy FX Canceled.
  ------- ----------------------------

## 5.2 Copy Disk states

  ------- ---------------------------------------------
  State   Observed display meaning
  0       Last / Reading..
  1       This is SP-808 Disk.
  2       Insert Source Disk.
  3       Insert Source Disk.
  4       Insert / Destination Disk.
  5       Insert / Destination Disk.
  6       Last / Reading..
  7       Last / Writing..
  8       Not Source Disk.
  9       Not Destination Disk.
  10      This is Source Disk.
  11      Wrong Disk. / (Write Protected.)
  12      Wrong Media Size.
  13      Additional descriptor + \[EXIT\] to Cancel.
  14      Copy Disk Canceled.
  15      Copy Disk Canceled.
  ------- ---------------------------------------------

Critical correction: state 12 selects the \'Wrong Media Size.\' screen.
That does not make 0x427C4A itself a media-size value. The variable is
the higher-level Copy workflow state.

# 6. Copy Disk transfer mechanics

0x107822 reads 16 batches of 0xC0 blocks into memory beginning at
0x440000.

Each batch advances memory by 0x18000 bytes and the block address by
0xC0, mechanically establishing 512 bytes per transferred block.

Each copy iteration spans 0xC00 blocks.

0x1078C8 performs the corresponding writes.

The start position is calculated as max(0, \[0x401016\] + 1 -
(iteration + 1) \* 0xC00).

# 7. Lower disk state 8 and the real \'Wrong Media Size\' path

OBSERVED: byte 0x40FA8B is a lower-level disk-status/state byte. Within
0x107728, destination checking can set this byte to state 8 when a saved
source value and the current disk value differ.

mov.l \@0x40FAA4, er0

mov.l \@0x401016, er1

cmp.l er1, er0

beq equal

mov.b #8, r0l

mov.b r0l, \@er6 ; er6 = 0x40FA8B

The comparison is equality-only: either a larger or smaller differing
value triggers state 8. There is no threshold or ordering comparison
here.

0x107822 initializes 0x40FAA4 to 0xFFFFFFFF and, after successful source
reading, snapshots the current 0x401016 into 0x40FAA4.

Therefore 0x40FAA4 is a saved source-media parameter, not a fixed
supported-capacity constant.

At the higher Copy Disk layer, lower state 8 maps to workflow state 12
(\'Wrong Media Size.\') when iteration position is zero.

When iteration position is already nonzero, an earlier branch maps the
same lower state 8 to workflow state 9 (\'Not Destination Disk.\').

STRONGLY INFERRED: lower state 8 is a source/destination storage-extent
incompatibility status used during disk copying.

# 8. 0x401016: what is established and what is not

Evidence boundary: the original producer of 0x401016 is not recoverable
from the code bytes currently loaded in this database.

All ten direct IDA references found to 0x401016 are reads; additional
structure-based references are also reads.

0x401016 is a longword at offset 0x16 in a parameter structure beginning
at 0x401000.

A mode byte at 0x401014 selects between longword 0x401016 and
alternative longword 0x40100A.

Routines around 0x1069BC and 0x106A50 independently implement:
byte\[0x401014\] != 0 -\> 0x401016; otherwise -\> 0x40100A.

The structure also supplies words at offsets 4, 6 and 8. 0x10686A
exports those words plus the selected longword into data used for disk
partition construction.

STRONGLY INFERRED: 0x401016 is an alternative storage extent/geometry
parameter for the RAM-service backend.

For Copy Disk specifically, consumers treat 0x401016 as an inclusive
terminal block position: arithmetic uses 0x401016 + 1 and computes
ceil((0x401016 + 1) / 0xC00).

The producer, original units, byte-order conversion, normalization and
count-vs-terminal representation are NOT established.

# 9. Parallel storage-backend evidence

STRONGLY INFERRED: the nonzero-nibble, target-indexed backend is the
external SCSI-style storage path, distinct from the internal IDE/ATAPI
backend. Evidence includes target IDs 0-7, exclusion of the controller
local ID, per-target state, phase/message completion machinery, SCSI
command vocabulary, and the separate controller/DMA architecture.
Physical-port identity remains to be tied down directly, so this is not
promoted to OBSERVED.

OBSERVED: the Iomega/ZIP classifier, acceptance gate, 0x426C42/0x426C62
capacity arrays, and 0x12Axxx/0x12Bxxx command machinery belong to this
target-indexed path. No demonstrated data/control-flow bridge makes that
qualification gate a restriction on the internal
0x400380/0x4003A8/0x4003AC backend.

Routine 0x106A1C distinguishes two backend paths using the low nibble of
a per-device byte at 0x40F57A + device\*0x24.

  ---------- ---------------------------- ---------------------------------------------------------------------------------------------------------------------------
  Selector   Source                       Observed representation handling
  nonzero    0x426C42 + 4\*(selector-1)   Array-backed quantity; 0x10686A increments it by 1 before geometry calculations.
  zero       0x401016 or 0x40100A         RAM-service structure; selected quantity is passed onward without that increment in the same partition-construction path.
  ---------- ---------------------------- ---------------------------------------------------------------------------------------------------------------------------

The array at 0x426C42 has an identifiable producer: 0x12B150 receives an
eight-byte command response into 0x5C0000 and copies its first four
bytes unchanged into the selected array entry. The command descriptor
includes byte 0x25, consistent with the independently reconstructed READ
CAPACITY path. However, no transfer from 0x426C42 into 0x401016 has been
established. Treat these as parallel backend paths unless future
evidence connects them.

# 10. Device probe and acceptance findings retained from the corrected walk

These findings were re-walked on the corrected H8S database before the
newer workflow-state investigation. They should remain evidence-tagged
rather than treated as untouchable truth.

The response buffer at 0x5C0000 used by the classifier has SCSI/ATAPI
INQUIRY-layout accesses: vendor at offset 8 and product at offset 0x10.

The earlier 0x951229 \'geometry/capacity\' interpretation was corrected:
the code assembles six low nibbles from INQUIRY revision/vendor-specific
bytes into a 24-bit fingerprint-like value.

Device-type byte 0x426C82 is written with classifications including 1, 2
and 3; the classifier itself falls through to success after successful
command handling.

In device_probe, the type is compared with 1. The historical two-byte
branch patch forces the non-Zip classification onto the accept path at
this layer.

The accept sequence includes a command at 0x12B150 whose eight-byte
response is copied into per-slot longword arrays at 0x426C42 and
0x426C62.

These facts do not prove that the two-byte patch is a complete storage
solution; filesystem/state/backend behavior remains separate.

# 11. Filesystem and disk-state findings

The 0x107xxx region contains filesystem-layer behavior, including
directory-entry handling and volume-related operations.

sub_1071CA was observed writing the fixed VS2-family directory/file
names and constructing a 0x800-entry take table.

Within 0x107728, the SP-808TS25E signature path runs only in a
particular lower disk state and can transition the disk-status byte to
state 7 on match or state 2 on mismatch.

0x107728 is a state machine, not a single accept/reject check. Observed
lower state values include 1, 2, 4, 5, 6, 7 and 8.

Source-media identity checking is distinct from the size-related
comparison: filesystem data yields identity words saved into 0x40FA9E
and compared against current identity values.

# 12. Runtime services at 0x400xxx: current hard boundary

Calls to addresses such as 0x400380, 0x4003A8 and 0x4003B4 sit directly
on storage-information paths, but the current database contains no
loaded instruction bytes for these services. Zero-valued database bytes
at those RAM addresses are not evidence of executable zero-filled
routines.

0x105420 calls RAM services while refreshing storage information.

0x105E0A also calls 0x4003B4 during polling.

Because the service implementation is absent, neither 0x4003B4 nor its
callees can yet be called the writer of 0x401016.

Creating IDA functions at those addresses would not recover missing
bytes.

Highest-value missing evidence: determine how executable/service content
for the 0x400xxx region is supplied at runtime.

# 13. Superseded / prohibited-as-premise claims

  ----------------------------------------------------------------------- ----------------- --------------------------------------------------------------------------------------------------------------------------------------
  Old claim                                                               Current status    Why
  0x427C4A is ui_media_index / media-size classification.                 SUPERSEDED        Recovered writers/readers show a shared Copy FX / Copy Disk workflow state word with values 0-15.
  25k/125k/250k/625k near Wrong Media Size are Zip capacity thresholds.   SUPERSEDED        Consumer decodes them as elapsed-counter thresholds in six-byte timed-action records.
  0x174Bxx is one media-size policy table.                                SUPERSEDED        It contains distinct structures: UI records, timed records and pointer pairs with different strides.
  Wrong Media Size proves a supported-capacity whitelist.                 UNSUPPORTED       Observed path is source snapshot 0x40FAA4 != current 0x401016 during Copy Disk. General whitelist behavior has not been established.
  0x401016 is raw READ CAPACITY last LBA.                                 NOT ESTABLISHED   Producer is missing; parallel backend path has different representation handling.
  0x426C42 is copied into 0x401016.                                       NOT ESTABLISHED   No data-flow connection has been found.
  The historical two-byte device-probe patch is a complete HDD/CF fix.    NOT ESTABLISHED   It addresses one acceptance branch; downstream filesystem, state, backend and timing behavior remain separate.
  Zero bytes at 0x400xxx can be disassembled to recover services.         FALSE PREMISE     Those service bytes are not loaded in the current database.
  ----------------------------------------------------------------------- ----------------- --------------------------------------------------------------------------------------------------------------------------------------

# 14. Current evidence-backed model

device / backend-specific storage information

\|

+\--\> array-backed path at 0x426C42\[\...\] \[producer identifiable\]

\|

+\--\> RAM-service structure at 0x401000 \[producer missing\]

\|

+\--\> mode byte 0x401014

+\--\> alternative longwords 0x40100A / 0x401016

\|

+\--\> partition/geometry construction

\|

+\--\> Copy Disk block planning

\| uses 0x401016 + 1

\|

source Copy Disk read \-\-\-\-\-\-\-\-\-\-\-\-\-\-\--+\--\> snapshot
0x401016 -\> 0x40FAA4

\|

destination refresh -\> current 0x401016
\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--+

\|

equality comparison

\|

mismatch -\> lower disk state 8

\|

higher workflow state 12

\|

\"Wrong Media Size.\"

# 15. Highest-value next investigations

Determine how runtime service code/data for the 0x400xxx region is
supplied. Search flash initialization, copy, relocation, decompression,
mask-ROM interaction, or other mechanisms without assuming a simple
memcpy.

If 0x4003B4 implementation bytes can be recovered, trace its writers
into the 0x401000 parameter structure and establish the exact
producer/representation of 0x401016.

Only after producer recovery decide whether 0x401016 corresponds to READ
CAPACITY, ATA IDENTIFY, filesystem-derived geometry, a normalized
extent, or another backend-specific quantity.

Keep the Copy Disk source/destination equality behavior separate from
any broader question of what media sizes stock firmware accepts for
normal operation.

For hardware validation, preserve the existing plan to compare
known-good Zip and failing HDD/CF bus behavior, especially around
command traffic and WAIT/IORDY behavior, after the firmware flashing
pipeline is validated.

# 16. Rules for cleaning the repository

Do not delete incorrect historical claims silently. Mark them SUPERSEDED
and link them to the evidence that corrected them.

Rename symbols only after an evidence-backed semantic interpretation is
stable. Prefer neutral address-based names while meaning is unresolved.

Every semantic claim in a reference document should carry provenance:
firmware/data flow, schematic/manual, hardware experiment, inherited
project claim, or inference.

Do not use agreement among an IDA name, helper script and Markdown note
as independent confirmation when they may share one origin.

For structures, record stride/field boundaries from consumer
instructions before assigning field names.

For constants, establish source, units and use. Numeric resemblance is
not semantics.

When a producer is absent from the image, say so. Do not infer an
invisible transfer merely because it would complete the story.

Maintain a short \'current evidence\' document like this one and move
speculative exploration into separate investigation notes.

# 17. Open questions ledger

  --------------------------- ----------------------------------------------------------------------------------------------------- ----------
  Question                    Evidence needed                                                                                       Priority
  Runtime 0x400xxx services   Where do their executable bytes/data come from, and can 0x4003B4 be recovered?                        Highest
  0x401016 producer           What writes the 0x401000 parameter structure; what are the units and representation?                  Highest
  Backend selector            What does low nibble of 0x40F57A + device\*0x24 identify physically/logically?                        High
  Mode byte 0x401014          What selects 0x40100A versus 0x401016 and what do the two alternatives represent?                     High
  General media-size policy   Outside Copy Disk, does stock firmware impose a supported-size whitelist?                             High
  Format path                 Does formatting initialize SP-808TS25E/VS2 correctly on non-Zip media through the relevant backend?   High
  Timing/WAIT issue           What causes the historical approximately one-second global slowdown with CF?                          High
  Mask ROM boundary           Exact on-chip ROM extent and patchability boundary.                                                   Medium
  Timed counter units         Convert 0x148D2E counter ticks to real time from verified timer clock/configuration.                  Medium
  --------------------------- ----------------------------------------------------------------------------------------------------- ----------

# 18. Recommended status statement for the project

The project has corrected a major false narrative around the \'Wrong
Media Size\' UI path. 0x427C4A is a Copy workflow state word, and the
nearby 25k/125k/250k/625k values are timed-action thresholds, not
demonstrated media capacities. The actual Copy Disk size-related
rejection occurs when a current storage parameter at 0x401016 differs
from a snapshot taken after reading the source disk. Consumers treat
0x401016 like an inclusive terminal block position during copy planning,
but its producer and backend representation are not present in the
currently loaded firmware code. The next evidence-bearing step is to
recover or explain the runtime 0x400xxx storage services rather than
infer the missing provenance.

# Appendix A. Evidence provenance used for this rebuild

This ledger was rebuilt from the project\'s prior clean-reference
document plus the independent read-only Codex/IDA investigations
discussed in the current session. Where those sources conflict, newer
instruction/data-flow reconstruction is preferred over inherited
semantic interpretation. No web-derived technical claims were added.

Prior clean project reference: hardware/schematic facts, firmware
metadata, corrected-core walk, physical observations and historical open
questions.

Independent investigation of 0x174Bxx: six-byte timed records,
eight-byte UI records, pointer-pair layout and counter consumer.

Independent investigation of 0x427C4A: writer/reader inventory, Copy
FX/Copy Disk state machine, display/timed dispatch and transfer
mechanics.

Follow-up investigation of lower disk state 8: equality mismatch between
saved source 0x40FAA4 and current 0x401016.

Follow-up investigation of 0x401016: 0x401000 parameter structure,
backend selection, representation difference, absent producer and
0x400xxx evidence boundary.

# 19. October 2026 update: D-Beam, numerical runtime, and external hardware path

Status: This section supersedes earlier speculative interpretations of
the 0x1589C0-0x159Axx region and extends the 0x400xxx service model. All
findings below come from read-only instruction/data-flow reconstruction.

## 19.1 Correct structural map at 0x1589C0-0x159A73

  ------------------- ---------------------------- --------------------------------------------------------------------------------------------------------------------------------------------
  Range               Structure                    Evidence / status
  0x1589C0-0x1589C1   H8 instruction bytes 40 AA   OBSERVED: backward BRA inside preceding function; not a data/header record.
  0x1589C2-0x1589D1   16 one-byte integers         OBSERVED: indexed with a masked 4-bit value; contents equal nibble popcount.
  0x1589D2-0x1599D1   16 x 256-byte lookup rows    OBSERVED: row index x256 plus input-byte offset; byte output. STRONGLY INFERRED: D-Beam calibration/sensitivity curves.
  0x1599D2-0x1599D9   4 big-endian uint16 values   OBSERVED: 0x0352, 0x0370, 0x0366, 0x035C (850, 880, 870, 860); selected by bounded index 0-3 and used for hardware-register configuration.
  0x1599DA-0x159A61   17 binary64 constants        OBSERVED: IEEE-754 binary64 representation established by arithmetic consumers, not numeric resemblance.
  0x159A62-0x159A65   0E 20 80 76                  UNRESOLVED.
  0x159A66-0x159A73   SCSI Check\... string        OBSERVED: separately referenced; establishes boundary after constant pool.
  ------------------- ---------------------------- --------------------------------------------------------------------------------------------------------------------------------------------

SUPERSEDED: the earlier claim that 0x40AA is a repeated record header.
It occurs once here and is executable H8 code.

SUPERSEDED: the interpretation of 0x1589D2-0x1599D1 as
DSP/velocity/coefficient records. Its consumers establish byte transfer
curves, and firmware UI/callback evidence ties calibration to D BEAM
SETUP / Auto Setup Sens?.

SUPERSEDED: the four words at 0x1599D2 are not established as the four
44.1/32 kHz stereo/mono audio modes. Their physical units and peripheral
identity remain unresolved.

## 19.2 D-Beam mapping path

OBSERVED: 0x12EAF0 calculates two row pointers as 0x1589D2 + unsigned
calibration_index x 256 and stores them at 0x426D50/0x426D54. Known
producers use default row 5 or calibration results 0-14; the local
pointer calculation itself has no bounds check.

OBSERVED: 0x12E626 selects one of those row pointers, adds a processed
input byte, and loads the mapped byte. Calibration callback 0x12EDCC is
linked by firmware records to the literals D BEAM SETUP and Auto Setup
Sens?. STRONGLY INFERRED, high confidence: the sixteen rows are D-Beam
sensitivity/calibration transfer curves for two channels.

## 19.3 Hardware timing table at 0x1599D2

OBSERVED: 0x100A8C accepts an unsigned index below 4, loads N from the
four-word table, supplies the constant 26, and calls 0x100AB0. The
latter configures hardware registers including FFFFFFD6=0, FFFFFFD8=2N,
FFFFFFDA=2N-52, FFFFFFDC=N, and FFFFFFDE=N-52, together with
control-byte programming.

STRONGLY INFERRED: these are timing/compare parameters. UNRESOLVED:
clock source, physical units, exact peripheral function, and the
semantic meaning of the four table indices.

## 19.4 Binary64 pool and filter-like numerical family

OBSERVED: consumers of 0x1599DA-0x159A61 implement binary64
sign/exponent/fraction arithmetic, including the 11-bit exponent, bias
0x3FF, exponent 0x7FF handling, sign-bit manipulation, rounding, and
two-longword operands. The pool includes 1000, pi, 1, 2, 20, 0.5, -1, 0,
100, 4, 8, -4, -12, 10, approximately 0.6, approximately 0.8, and 2pi.

For 0x100B0A, let s be the selected binary32 table value, f the signed
16-bit input, and g the result of an opaque encode/operate/decode
sequence. Ignoring explicit intermediate binary32 rounding boundaries,
the recovered shape is x = pi\*f/(1000\*s), then output\[0\] =
output\[1\] = g/(1+g), and output\[2\] = (1-g)/(1+g).

STRONGLY INFERRED: 0x100B0A and neighbouring routines form a
filter-coefficient calculation family; complementary numerator patterns
support paired filter behavior.

HYPOTHESIZED: the opaque unary operation is tangent-like. Its
implementation has not been recovered.

CORRECTION: the third 0x100B0A output is (1-g)/(1+g), not (g-1)/(g+1).

UNRESOLVED: 0x100B0A itself has no identified direct caller; indirect
reachability remains possible.

## 19.5 Opaque numerical services in the baseline 0x400xxx ABI

The application uses a systematic encode -\> operation -\> decode
pattern around baseline service entries 0x400558, 0x400568, 0x40056C,
0x400570, 0x40057C, 0x400580, 0x400584, 0x400588 and 0x40058C. The
intermediate four-byte representation is designated O32 because IEEE
binary32 packing is not established.

0x40058C: caller supplies a binary64 value and output pointer; a
four-byte O32 result is consumed.

0x400584: caller supplies O32 in ER0 and an output pointer; produces
O32. Calling it tangent remains HYPOTHESIZED.

0x400588: caller supplies O32 and an output pointer; destination is
subsequently consumed as binary64.

No identified call site checks a success/error return or completion flag
before immediately consuming the pointed result.

## 19.6 Demonstrated numerical-result path to external hardware

OBSERVED: related, actively called numerical routines 0x10192E and
0x101D16 feed results through 0x10C816 into 0x108C12. 0x108C12 computes
a destination based at 0xC00000 or 0xC01000 plus (incoming_selector &
0x0FFC), maintains RAM mirrors, changes control at 0xC02003, polls bit 7
at 0xC00003, and writes a longword to the selected external address.

OBSERVED: this establishes an external hardware-programming path for the
numerical family.

UNRESOLVED: the architectural identity of the 0xC00000/0xC01000
hardware, its coefficient/register layout, whether it is the audio DSP
interface, and whether DSP program words are present in SP8EXall.bin.

## 19.7 Revised 0x400xxx architecture boundary

The earlier statement that the 0x400xxx region was simply an absent
storage-service boundary is too narrow. Application evidence now shows
baseline services used by storage, input sampling, and numerical
conversion/operation paths. The implementation source remains
unavailable in the current external image, but the application-visible
ABI can be reconstructed from callers.

STRONGLY HYPOTHESIZED: an earlier/internal firmware layer establishes a
baseline RAM service environment before the external application runs;
the external firmware later installs selected absolute-jump overrides.
This architecture remains a hypothesis about provenance, not a recovered
internal-ROM implementation.

# 20. Revised highest-value next investigation

Trace one actively used numerical output from 0x101D16 through 0x10C816
into 0x108C12. Recover the exact destination selectors, neighbouring
words/registers, write ordering, RAM mirrors, and any readback/poll
protocol. The objective is to establish the actual coefficient/register
layout and hardware consumption contract before applying any DSP-family
interpretation.

Only after that host-side contract is established should candidate
payloads/register layouts be compared with external Roland DSP
architectural work. Do not use the falsified 0x1589D2 lookup-bank
interpretation as DSP evidence.

# Appendix B. Provenance for October update

Independent read-only Codex/IDA investigation completed 2 October 2026:
structural reconstruction of 0x1589C0-0x159A73; D-Beam calibration
consumers; 0x1599D2 hardware-register consumer; binary64 arithmetic
helpers; 0x100B0A numerical reconstruction; 0x400558-0x40058C caller
inventory; and active numerical-result path through 0x10C816/0x108C12 to
0xC00000/0xC01000 hardware space.

# 21. ESP architecture and diagnostic memory map

OBSERVED: Firmware diagnostic UI identifies the device as DEVICE(ESP)
and reports PRAM0, PRAM1, IRAM0, IRAM1, GRAM and ERAM independently.

OBSERVED: PRAM0 maps to CPU-visible hardware bank 0xC00000 and PRAM1
maps to 0xC01000. The diagnostic writes and reads 768 four-byte entries
in each bank.

OBSERVED: PRAM selected-read mode sets C02003 bits 1:0 to 11, writes
zero to the selected bank/address, then reads the returned longword from
C00000 as a common readback port.

STRONGLY INFERRED: IRAM0, IRAM1, GRAM and ERAM are exercised indirectly
by loading PRAM records, patching record fields, allowing hardware
processing, and testing a common hardware-generated result. The CPU does
not perform the functional comparison itself.

  ---------- -------------------------------------------------- --------------------------------------
  ESP name   Application-visible interface                      Established behavior
  PRAM0      0xC00000 + 4\*i                                    Direct store/read test, i=0..767
  PRAM1      0xC01000 + 4\*i                                    Direct store/read test, i=0..767
  IRAM0      PRAM program + data at C00008                      Indirect four-pattern verification
  IRAM1      PRAM program + data at C010D4                      Indirect four-pattern verification
  GRAM       PRAM program + data at C0110C                      Indirect four-pattern verification
  ERAM       PRAM program; Q operand encoded at C0107C/C01098   Indirect fixed-location verification
  ---------- -------------------------------------------------- --------------------------------------

## 21.1 PRAM image loader and record representation

OBSERVED: The PRAM loader expands each three-byte ROM record \[a,b,c\]
to one four-byte hardware/shadow word W=(a\<\<24)\|(b\<\<16)\|(c\<\<8).
For configuration type 1, ROM 0x15E470 contains 247 records loaded to
PRAM1 starting at index 0x3C.

ROM record j: addr = 0x15E470 + 3\*j

PRAM1 index: 0x03C + j

hardware: 0xC01000 + 4\*(0x03C + j)

shadow: 0x4110C2 + 4\*(0x03C + j)

W = (a \<\< 24) \| (b \<\< 16) \| (c \<\< 8)

STRONGLY INFERRED: The loaded PRAM image is a structured
numerical-processing template. Runtime filter coefficients occupy fields
spanning adjacent records while other operand/reference-like fields are
preserved.

UNRESOLVED: Whether PRAM records are conventional executable
instructions or descriptors for an active hardware
sequencer/configuration graph. No program counter, branch semantics or
complete instruction set has yet been recovered.

## 21.2 Runtime coefficient update contract

OBSERVED: 0x101D16 generates five binary32 values. The first three form
\[b,-2b,b\]. 0x10C816 converts them to the ESP packed format and writes
each coefficient to paired PRAM1 destinations via 0x108C12.

  --- ----------------- ---------------------
  k   PRAM1 selectors   Hardware addresses
  0   0x1118 / 0x1140   0xC01118 / 0xC01140
  1   0x1120 / 0x114C   0xC01120 / 0xC0114C
  2   0x1128 / 0x1154   0xC01128 / 0xC01154
  3   0x1130 / 0x115C   0xC01130 / 0xC0115C
  4   0x1138 / 0x1164   0xC01138 / 0xC01164
  --- ----------------- ---------------------

// application-visible contract

write_packed_parameter(uint16 selector, uint32 W)

offset = selector & 0x0FFC

bank = selector & 0x1000

hardware = (bank ? 0xC01000 : 0xC00000) + offset

shadow = (bank ? 0x4110C2 : 0x4104C2) + offset

STRONGLY INFERRED: The five-value vectors are second-order filter
coefficients. The high-pass/low-pass interpretation is supported by
coefficient relationships and independent normalization checks; the
exact executed recurrence remains hypothesized until ESP record
semantics are decoded.

## 21.3 Address-like PRAM operands and temporary initialization program

OBSERVED: 0x1086FC installs 115 six-word structures in PRAM1. Instance i
begins at index 0x3D+6\*i and embeds Q=0x474\*i through packed
transaction 0x1097BE -\> 0x108D06. Q is 18 bits.

for (i = 0; i \< 115; i++) {

k = 0x3D + 6\*i;

Q = 0x474 \* i;

PRAM1\[k+0..k+5\] = {0,0,0x00AC3700,0,0,0};

P = 0x80000000 \| ((Q & 0xFF)\<\<16) \| (Q & 0xFF00) \| ((Q\>\>16)&3);

special_update_bit1(PRAM1, k, P); // 0x108D06

}

// leave resident for rate-dependent interval, then clear PRAM1
0x03C..0x2FF

STRONGLY INFERRED: Q is an address/position in a hardware-managed space
distinct from PRAM. The temporary program is an autonomous
initialization operation rather than a passive CPU lookup table.

HYPOTHESIZED: The operation initializes or clears processing
state/history across another ESP memory space. Exact target and units
remain unresolved.

## 21.4 ESP diagnostic as semantic anchor

OBSERVED: Diagnostic ROM images 0x15A447 (16 records to PRAM0) and
0x15A477 (115 records to PRAM1) are loaded before IRAM/GRAM/ERAM tests.
Test-data fields are patched in PRAM records; service 0x4002C8 is
invoked; common-port result zero is required.

OBSERVED: For ERAM, Q=0x1234 is encoded by both 0x1097BE and 0x109786.
They carry the same 18-bit quantity but control bits 31:30 differ: 10
versus 01.

Q = 0x1234

0x1097BE(Q) -\> 0x80341200 -\> 0x108D06 @ selector 0x107C

0x109786(Q) -\> 0x40341200 -\> 0x108D06 @ selector 0x1098

STRONGLY INFERRED: The two formats are write-like and read-like
operations on an ERAM location, based on their placement around supplied
test data and the common result path.

# 22. Production effects region: new investigation target

OBSERVED: IDA displays many plausible effect-name strings in
approximately 0x162078-0x1657xx, including DL:Hi-Pass, CH:SBF-325,
RV:LrgHall, DN:Limiter, SY:Beam #1 and SL:Slicer1. Printable garbage
also appears between names, so IDA string creation must not be treated
as proof of text boundaries.

HYPOTHESIZED: This region contains production effect records/program
templates rather than diagnostic payloads. This has not yet been traced
to PRAM and remains the highest-value next investigation.

Next: reconstruct record boundaries from raw bytes and xrefs, then trace
one named effect from selection through its ROM structure into the ESP
PRAM loader and runtime parameter patches.

# Appendix C. Provenance for ESP update

Independent read-only Codex/IDA investigations completed 2 October 2026:
PRAM loader and filter-record analysis; temporary initialization-program
analysis; ESP diagnostic mapping for PRAM0/PRAM1/IRAM0/IRAM1/GRAM/ERAM.
No external DSP architecture information was used in those passes.

# 23. 3 October 2026 consolidated update: production ESP ISA

This section supersedes the earlier uncertainty about whether the
production PRAM images are passive configuration data. The host-side
loader, runtime patchers, complete production-image census, diagnostic
evidence, and independent JP-8000/TC170C140 comparison now support an
executable-ISA interpretation.

## 23.1 Production preset/image architecture

OBSERVED: 200 preset records cover 25 processing types. Each type
selects a distinct PRAM image and a distinct top-level parameter
handler.

OBSERVED: every production image is loaded into PRAM1 beginning at index
0x03C; unused tail entries are cleared through 0x2FF, and the loader
writes 0xF14E3700 at index 0x2F2.

OBSERVED: ROM records are three bytes and are written as H8 longwords
(a\<\<24)\|(b\<\<16)\|(c\<\<8). For ESP decoding the useful normalized
word is D=(c\<\<16)\|(b\<\<8)\|a.

OBSERVED: all 199 consecutive preset boundaries agree with the recovered
type-length table.

STRONGLY INFERRED: named presets are a user-facing parameter layer over
25 executable processing templates; handlers patch selected fields of
the loaded program at runtime.

## 23.2 TC170C140-compatible instruction architecture

STRONGLY INFERRED: the SP-808 production images use the same or a very
closely related Roland ESP instruction architecture as the
JP-8000/TC170C140 family. This is not based only on matching opcode
numbers: host coefficient patches land on the expected coefficient/shift
fields, arithmetic pipelines remain coherent, and the five-record ERAM
address scatter mechanically matches the published ESP field layout.

  ------------------- ---------------------------------------- -----------------------------------------------------------------------
  Opcode family       SP-808 production use                    Current interpretation
  00/04/10/14         Arithmetic / accumulator operations      Compatible with ESP MAC/replace families
  08/0C/18/1C         IRAM stores plus accumulator operation   Compatible
  30                  530 records                              Coefficient-register multiplication/modifier family
  34                  2086 records                             Special operations: coefficient writes, ERAM, jumps, one B0 extension
  40/44/48/4C/58/5C   IRAM store variants                      Compatible with raw/rectified/saturated store families
  50                  63 records                               Condition-related operation; exact SP-808 semantics unresolved
  78/7C               69 records                               Compatible with interpolation/store-negative family
  ------------------- ---------------------------------------- -----------------------------------------------------------------------

OBSERVED census: all 8,381 production records decode mechanically under
the validated normalization. The only explicit published-decoder
rejection is the single type-05 opcode-34/B0 record; jump target width
is the other demonstrated compatibility correction.

## 23.3 SP-808 ISA corrections/extensions

STRONGLY INFERRED: jump target = D & 0x3FF. All 31 production jumps then
target forward locations inside their loaded image; the published
low-byte-only rule misdirects 22 of them.

OBSERVED: jump subtypes present are 34/D0, 34/D2 and 34/D3. Published
condition meanings are useful decoder context but remain externally
derived until independently validated on SP-808.

OBSERVED: opcode 34/B0 occurs exactly once, at type 05 index 0x046.

STRONGLY INFERRED: 34/B0 participates in a bounded ramp/crossfade
sequence and writes delayed accumulator A into coefficient register 0. A
possible host-visible endpoint/status side effect remains HYPOTHESIZED.

OBSERVED: opcode 50 occurs 63 times across 13 types. Its exact SP-808
condition semantics remain UNRESOLVED.

OBSERVED: direct GRAM opcodes 20/24/38/3C and interpolation families
60/64/68/6C/70/74 do not occur in the 25 production images; absence from
production images does not imply absence from the ISA.

## 23.4 ERAM runtime decoration

OBSERVED: all initial production ROM records have zero ERAM-control
fields.

OBSERVED: the H8 runtime patcher distributes an 18-bit Q/address value
across five consecutive ESP records and sets read/write mode bits.

OBSERVED: 2,010 tested application comparisons of this five-record
scatter matched the TC170C140-compatible ERAM field layout with zero
mismatch.

CONSEQUENCE: a static ROM disassembler must distinguish the pristine ROM
instruction from runtime-decorated ERAM transactions; complete ERAM
behavior cannot be reconstructed from ROM records alone.

# 24. 3 October 2026 consolidated update: storage service context

The 0x401000 region is now reconstructed as an application-visible
shared storage-service context. It is not simply an IDE/ATAPI
hardware-register map. The application exposes consumers much more
clearly than producers; several fields are populated behind the opaque
0x400xxx service boundary.

  -------- ------- --------------------------------------------------------------------------------------- ------------------------------
  Offset   Width   Evidence-backed role                                                                    Status
  +00      byte    Busy/completion byte; zero participates in successful completion                        OBSERVED / STRONGLY INFERRED
  +01      byte    Service input cleared before initialization/recovery                                    UNRESOLVED semantics
  +04      word    Cylinder-like geometry quantity                                                         STRONGLY INFERRED
  +06      word    Heads                                                                                   STRONGLY INFERRED
  +08      word    Sectors per track                                                                       STRONGLY INFERRED
  +0A      long    Mode-0 extent; end-of-device diagnostic treats it like an exclusive boundary            Representation unresolved
  +12      byte    Sector-buffer representation/transform selector                                         STRONGLY INFERRED
  +14      byte    Baseline storage-service variant selector                                               STRONGLY INFERRED
  +16      long    Inclusive terminal 512-byte block address in its application mode                       STRONGLY INFERRED
  +1E      word    Application-maintained software result/status                                           OBSERVED
  +78      byte    Service flags: bit0 activity; bit6 protection/access condition; bit3 event unresolved   Mixed
  -------- ------- --------------------------------------------------------------------------------------- ------------------------------

## 24.1 0x401014 variant behavior

+14 == 0 -\> select +0A; call 0x40039C before sector-zero read;
completion/media-control 0x400394

+14 == 1 -\> select +16; skip 0x40039C; completion/media-control
0x400398

+14 other !=0 -\> select +16; skip 0x40039C; completion/media-control
0x400394

UNRESOLVED: the producer and exact device/protocol meaning of +14. It
must not be renamed ATAPI/SCSI/LBA/device-type without direct evidence.
The application first dispatches between baseline storage and separately
enumerated packet targets using a different logical-volume descriptor,
so +14 is not that top-level backend selector.

## 24.2 Geometry and extent corrections

OBSERVED: +06 and +08 participate in CHS arithmetic; formatter code
writes the exported heads/sectors-per-track values into sector-zero/boot
structures and uses 512-byte sectors.

STRONGLY INFERRED: +16 is inclusive-terminal because multiple
independent full-copy consumers explicitly add one before treating it as
a block count.

OBSERVED: the +0A diagnostic subtracts 64 and tests extent_mode0-64
through extent_mode0-1, consistent with an exclusive extent/count
representation.

OBSERVED: formatter/partition construction uses the selected extent
without adding one. This is a genuine representation discrepancy to
explain, not evidence that the stronger +16 inclusive-terminal
observations are wrong.

SUPERSEDED: 0x401016 must not be described as a proven raw READ CAPACITY
result; its original producer remains behind the service boundary.

# 25. Explicit Iomega Zip path and normal block-I/O contract

The separately enumerated packet-target path contains explicit Iomega
Zip identification and qualification. This establishes a concrete
software restriction above the ordinary block-transfer layer.

## 25.1 Recognition and acceptance

INQUIRY-like exchange

-\> vendor bytes +08..+0F == \"IOMEGA \" or \"iomega \"

-\> product bytes +10.. == \"ZIP\"

-\> classification\[target\] = 1

acceptance requires:

(device_category & 0x1F) == 0

&& classification\[target\] == 1

-\> acceptance_state\[target\] = 2

OBSERVED: this path therefore rejects a generic direct-access device
that does not present the expected Iomega/ZIP identity, before normal
filesystem use.

## 25.2 Zip-specific setup/state exchanges

  ---------- ------------------- -------------------------------- ------------------------------------------------------------
  Routine    CDB                 Transfer                         Application-visible consequence
  0x12B950   1A 00 2F 00 12 00   18 bytes device -\> RAM          Response discarded; setup/query attempt
  0x12B9C8   15 10 00 00 1A 00   26 bytes RAM -\> device          Fixed configuration payload; return not an acceptance gate
  0x12BBF0   06 00 02 00 16 00   22 bytes device -\> RAM          Exports two persistent media-state nibbles
  0x12BC8E   0C 00 00 00 00 00   No data                          Format-preparation path only
  0x12BD02   04 10 20 00 00 00   Four zero bytes RAM -\> device   Class-specific format preparation then readiness check
  ---------- ------------------- -------------------------------- ------------------------------------------------------------

OBSERVED: the first three recognition-time commands are attempted
unconditionally after Zip recognition, but their return values are not
used as acceptance gates. Only 0x12BBF0 exports persistent response
fields directly consumed by later operation checks.

## 25.3 Capacity and ordinary transfer path

READ-CAPACITY-style CDB:

25 00 00 00 00 00 00 00 00 00

response\[0..3\] -\> cached terminal block

response\[4..7\] -\> cached block length

later requirements:

block length == 512

cached terminal block != 0

cached block length != 0

normal READ: 28 00 A3 A2 A1 A0 00 N1 N0 00

normal WRITE: 2A 00 A3 A2 A1 A0 00 N1 N0 00

STRONGLY INFERRED: in this target-indexed path the first returned long
is a READ CAPACITY(10)-style last logical block and the second is block
length. No chain has been demonstrated from this response to 0x401014 or
0x401016.

OBSERVED: the normal block wrappers do not directly test Zip
classification. They require transport availability, nonzero cached
extent and block length, a zero transfer-blocking/media restriction
byte, and successful completion. Higher-level revalidation additionally
requires acceptance state 2 and a media-state low nibble of 2.

## 25.4 Physical Zip format is not a mount prerequisite

OBSERVED: the 0x0C command and class-1 modified 0x04 operation occur on
an optional format-preparation path. They do not precede the ordinary
scan-to-mount path or normal READ(10)/WRITE(10)-style sector I/O.
Therefore the minimum software contract for ordinary operation does not
include a demonstrated requirement to physically format the device.

## 25.5 Backend separation and relevance to the HDD objective

STRONGLY INFERRED: the target-indexed 0x12Axxx/0x12Bxxx implementation
is the external SCSI-style storage backend. Its target addressing,
local-ID exclusion, phase/message machinery, per-target state, SCSI
command set, and separate controller/DMA architecture distinguish it
from the physically observed internal IDE/ATAPI path.

OBSERVED: A6 operates an internal ATA HDD through its
application-resident 0x600xxx backend while retaining the ordinary
external target-path Iomega/ZIP qualification gate. Therefore generic
internal-HDD acceptance and bypass of the target-path ZIP identity gate
are separate engineering problems.

SUPERSEDED: the historical two-byte target-path Iomega/ZIP branch patch
must not be presented as a demonstrated route to internal HDD support.
It may alter acceptance on the target-addressed path, but current
evidence places the internal-HDD splice at the internal backend beneath
the common volume router.

# 26. A6 differential-reverse-engineering strategy

HARDWARE/EXPERIMENTAL FACT supplied by the project: Roland/Edirol A6
firmware runs on SP-808 hardware and operates an IDE HDD, while
replacing SP-808 application functionality with A6 behavior. This makes
the A6 firmware a control implementation for HDD support on the same
hardware platform.

PROJECT GOAL: preserve SP-808 functionality while identifying and
patching the smallest software delta required to permit HDD operation.
The investigation should therefore pivot from proving generic hardware
capability to differential analysis of SP-808 versus A6 storage
discovery, qualification, capacity/state setup, and convergence into
ordinary block I/O.

Do not assume the A6 uses a wholly different storage stack;
independently reconstruct it first.

Compare device enumeration, identification/acceptance, capacity
acquisition, media-state construction, logical-volume creation, and
normal block I/O.

Determine whether A6 calls the same baseline 0x400xxx service ABI or
installs different overrides.

Highest-value outcome: identify the earliest point at which A6
accepts/configures an HDD and then converges into code structurally
equivalent to the SP-808 512-byte block layer.

Do not patch until the behavioral delta can be stated and falsified.

# 27. Current highest-value open questions

A6: what exact application-side state permits HDD discovery, capacity
acquisition, mount, and write?

A6 versus SP-808: are the normal READ/WRITE and filesystem layers
shared, homologous, or replaced?

Does A6 use the same 0x400xxx baseline service ABI and, if so, which
service variants/overrides differ?

Can the A6 internal ATA backend be relocated into SP-808 while leaving
the target-addressed Iomega/ZIP qualification path unchanged?

What is the exact meaning/producer of 0x401014 and the distinction
between +0A and +16 in the baseline service context?

Which acceptance/media-state guards are confined to the target-addressed
backend, and are any analogous guards present on the internal-volume
path?

ESP: exact opcode-50 semantics, 34/B0 side effect, and branch latency
remain useful but are no longer the critical path to HDD enablement.

# Appendix D. Supersession notes for the 3 October update

SUPERSEDED: production PRAM images as merely passive configuration
graphs. Current evidence strongly supports executable ESP programs.

SUPERSEDED: published ESP low-byte jump targets for SP-808. Use the
strongly inferred 10-bit target D&0x3FF.

SUPERSEDED: any generic-HDD framing of the SP-808 target-indexed storage
path. It explicitly identifies and qualifies Iomega Zip devices.

SUPERSEDED: treating the historical two-byte Iomega/ZIP acceptance patch
as a demonstrated internal-HDD enablement patch. The gate is in the
target-indexed, strongly inferred external SCSI-style backend; A6
demonstrates internal ATA HDD operation through a different backend
while that gate remains present.

SUPERSEDED: treating 0x401000 as a hardware-register block. It is an
application-visible shared service context.

RETAINED: 0x400xxx implementations remain an opaque inherited DRAM-resident platform-service boundary
unless independently recovered; application-visible contracts are still
valid evidence.

# 28. A6 application-side ATA backend: independently recovered differential

Evidence update, 3 October 2026. This section records the A6
control-case reconstruction and the subsequent mechanical comparison
against SP8EXall.bin. Existing semantic names/comments were not treated
as proof.

OBSERVED: A6 contains an application-resident internal storage driver
that directly accesses the SLA919F task-file-like window at
0x600002-0x60001C. The recovered path issues ATA commands EC (IDENTIFY
DEVICE), 20 (read), 30 (write), plus initialization commands including
EF and 10.

OBSERVED: the A6 internal driver uses the same application-visible
context base 0x401000 used by SP-808 storage code. A6 derives +0A as
cylinders × heads × sectors/track and supports CHS or a 28-bit
linear-address construction.

OBSERVED: A6 registers three handler pointers through opaque service
0x40020C: selector 0x48 -\> 0x12641C, 0xA0 -\> 0x1264BC, and 0xB0 -\>
0x1265CA.

OBSERVED: ordinary A6 filesystem routing uses a 0x24-byte volume
descriptor. Low nibble zero routes to the internal application ATA
driver; nonzero routes to the external target-addressed path.

STRONGLY INFERRED: 0x401014 is associated with an internal-device
signature/protocol variant. A6 0x10126A contains an intended 14/EB test
and +14=1 assignment, while physical SP-808 traces independently show
14/EB after reset for the ATAPI Zip. The A6 branch is unreachable in the
examined flow, so a simple ATA/ATAPI enumeration is not yet established.

  -------------------------- --------------------------------------------------------------------------------------- ---------------------------------------------------
  A6 component               Role / evidence                                                                         Current status
  10058C                     Internal initialization; reset/qualification, handler registration, IDENTIFY sequence   A6-specific application implementation
  100A58                     ATA IDENTIFY DEVICE (EC), transform 512-byte response, populate geometry/context        A6-specific
  100B2A                     Internal block read; ATA command 20; CHS/28-bit address setup                           A6-specific
  100D2A                     Internal block write; ATA command 30; CHS/28-bit address setup                          A6-specific
  10126A                     Reset/signature/status qualification                                                    A6-specific; 14/EB alternate branch unreachable
  12641C / 1264BC / 1265CA   Registered event/data-transfer handlers                                                 A6-specific
  40020C / 4002C8 / 40023C   Handler registration / delay / identification-buffer transform                          Opaque service interfaces retained in both images
  -------------------------- --------------------------------------------------------------------------------------- ---------------------------------------------------

# 29. SP-808 versus A6 routing-layer correspondence

OBSERVED: no direct SP-808 application accesses to 0x600000-0x60001C
were identified, and none of the recorded A6 ATA-driver signatures
matched exactly.

OBSERVED: address-masked routing signatures match exactly twice in
SP-808: A6 read router 0x107E16 corresponds to SP-808 0x105ED6; A6 write
router 0x107EEA corresponds to SP-808 0x105FB2.

OBSERVED: both products compute volume × 0x24, read the descriptor first
byte, and route on its low nibble. The descriptor base relocates from A6
0x40F516 to SP-808 0x40F57A.

OBSERVED: on the internal branch, SP-808 forwards the same argument
pattern to opaque services 0x4003A8/0x4003AC that A6 forwards to
application routines 0x100B2A/0x100D2A.

STRONGLY INFERRED: A6 preserves the shared upper storage-routing
contract but substitutes an application-resident ATA HDD backend for the
SP-808 opaque internal-device backend. This is an interface
correspondence, not proof that the implementations behind
0x4003A8/0x4003AC are homologous.

  ------------------------------------- ----------------------------------------- ---------------------------------------
  Layer                                 SP-808                                    A6
  Internal read route                   105ED6 -\> 4003A8                         107E16 -\> 100B2A
  Internal write route                  105FB2 -\> 4003AC                         107EEA -\> 100D2A
  Internal initialization               105468 clear context; 10546E -\> 400380   10058C application ATA initialization
  Direct SLA919F ATA task-file access   None identified in application image      0x600002-0x60001C
  Volume descriptor                     0x40F57A, stride 0x24                     0x40F516, stride 0x24
  ------------------------------------- ----------------------------------------- ---------------------------------------

# 30. A6 ATA dependency closure and transplant constraints

Live IDA revalidation confirmed all 22 defined functions in the
recovered closure. Six handler/helper bodies remain undefined as IDA
functions but are supported by raw firmware analysis. One address
correction is recorded: the long write to 0x4033EA begins at 0x100D5A;
the previous 0x100D5C attribution is SUPERSEDED because it lies inside
that instruction.

OBSERVED: the closure contains eight root routines, twenty application
helpers, and three opaque 0x400xxx services.

OBSERVED: supported relocated SP-808 helper homologues are A6 126290 -\>
SP 12380A; 1262A2 -\> 12381C; 135818 -\> 1309CA; 13583C -\> 1309EE;
16296C -\> 157B6A; 163122 -\> 15833C. The final two are whole-function
byte-identical.

OBSERVED: A6-private writable ATA state includes 0x4033E6-0x4033ED.
Interim SP-808 analysis establishes that all eight bytes are live
numerical operand/result state; therefore this range is not available
for an address-identical transplant.

OBSERVED: SP-808 waits for 0xFFFFF0DF bits 1/2 to clear before changing
its transfer environment, while no SP application writes to those bits
have yet been identified.

STRONGLY INFERRED: 0xFFFFF0DF bits 1/2 participate in asynchronous
lower-level transfer synchronization. Ownership/producer remains
unresolved pending completion of the SP infrastructure analysis.

UNRESOLVED: words at 0x000450 and 0x000458 select transfer-descriptor
storage via FF0000 + word value in A6. Their SP-808 compatibility and
producer are under active investigation.

# 31. Revised HDD patch hypothesis

Current evidence no longer favors a dormant application-side HDD driver
in SP-808. The working patch hypothesis is a relocation/transplant of
the bounded A6 ATA backend beneath the existing SP-808
logical-volume/filesystem layer, while retaining the SP-808 application
and external Zip path. This remains a hypothesis until descriptor,
handler-registration, transfer-control, RAM-allocation, and
initialization compatibility are demonstrated.

SP-808 filesystem / volume routing

\|

+\-- external target path \[retain\]

\|

+\-- internal path

current: 400380 / 4003A8 / 4003AC

candidate replacement: relocated A6 ATA subsystem

-\> SLA919F 0x600xxx

-\> ATA HDD

# 32. 4 October 2026: corrected transfer environment and relocation prerequisites

This section records the storage-transplant findings established after
the initial A6 closure. It supersedes earlier assumptions about spare
RAM, transfer-channel ownership, and the role of 0x4033E4. The governing
rule remains: application-visible behavior is reconstructed from callers
and bytes; unavailable 0x400xxx implementation is treated as an opaque
ABI boundary.

## 32.1 Corrected startup copy and 0x4033E4

OBSERVED: startup at 0x12CC54 clears 0x403000-0x42BFFF, then copies ROM
0x17C454-0x17C880 to RAM 0x403000-0x40342C (length 0x42D).

OBSERVED: RAM 0x4033E4-0x4033E5 receives ROM bytes 2E E0, i.e. word
12000. RAM 0x4033E6-0x4033ED receives binary64 1.0.

CONTRADICTED/SUPERSEDED: the historical claim that 0x4033E4 is a Zip
device type, and the claim that 0x14B51E compares it with 5. The
instruction beginning 0x14B51C loads 0x4033E4, adds 5, divides by 10,
and jumps to 0x4003EC; 0x14B51E lies inside the address operand.

OBSERVED: 0x4033E6-0x4033ED is live numerical state in SP and cannot
host A6 private ATA state.

## 32.2 Shared transfer-environment services

12BE62(mode): wait until (FFFFF0DF & 06) == 0 clear
FFFFFF07/03/02/05/04/06 40034C(0); 400350(0); 400344(mode) if mode == 0:
400340(); 40034C(1); 400350(1)

STRONGLY INFERRED: 0x12BE62 serializes switching of a shared transfer
environment. Mode 0 restores the environment with controls enabled; mode
1 leaves it disabled after 0x400344(1). Exact opaque-service semantics
remain unresolved.

OBSERVED: storage paths use this switch around target operations;
successful internal initiations can leave mode 1 until completion/error
restores mode 0.

OBSERVED: 0xFFFFFFC0 is shared by several SP mechanisms. It is not an
ATA-exclusive register. A6 transfer channels use bits 1/2, while SP code
also masks/restores the byte around other operations.

## 32.3 Event selectors and descriptor words

OBSERVED: SP registers selector 0x4C to handler 0x123864; that handler
clears bit 3 at 0xFFFFFF2F/0xFFFFFF2E and accesses the 0x800xxx
controller. A6 selector 0x48 uses adjacent bit 2 and reads 0x60000E.

STRONGLY INFERRED: selectors 0x48 and 0x4C are adjacent interrupt/event
sources. Absence of SP application registration for 0x48/0xA0/0xB0 does
not prove vacancy; baseline/platform ownership remains unresolved.

SUPERSEDED by section 38: words 0x450 and 0x458 are manufacturer-defined H8S DTC vector entries for TGI1A and TGI2A. A6 reads them as unsigned offsets and forms the corresponding on-chip-RAM register-information addresses.

## 32.4 RAM placement findings

REJECTED as proven-free RAM: 0x43BF48-0x43FFF7. Linker arithmetic makes
0x43BF48 the exclusive end of application BSS, but stack/computed opaque
accesses and baseline workspace remain unresolved.

OBSERVED: 0x5D0000 is an active filesystem/cache buffer, not unused RAM.
It is nevertheless the A6 IDENTIFY/format scratch address. Cold use is
plausible; warm ownership is unresolved.

STRONGLY INFERRED, conditional reclaim: 0x4033AE-0x4033B5 can hold the
eight A6 private bytes if the sole identified callback-table consumer at
0x146DE2 is redirected from RAM table base 0x4033AE to its ROM
initializer 0x17C802. The eight bytes must then be explicitly
initialized.

A6 private state relocation: 4033E6 status word -\> 4033AE 4033E8
counter A -\> 4033B0 4033E9 counter B -\> 4033B1 4033EA selected_end -\>
4033B2

# 33. A6 transfer machinery and complete ATA envelope

The A6 dependency census expanded the transplant from selected ATA
routines to a complete contiguous application-side envelope. This is now
preferred because later differential work independently required every
previously omitted gap.

OBSERVED: A6 descriptor setup at 0x100FA8 uses word 0x450 for a
device-to-RAM descriptor and word 0x458 for a RAM-to-device descriptor.
The fixed device endpoint is 0x600000; application code does not
directly treat 0x600000 as an ordinary programmed-I/O data register.

STRONGLY INFERRED: A0/B0 are paired transfer-completion events. A0 uses
the 0x450 descriptor, private counter 0x4033E8, FFFFFFE4/E5/E6 and
FFFFFFC0 bit 1; B0 uses 0x458, counter 0x4033E9, FFFFFFF4/F5/F6 and C0
bit 2. Corresponding FFFFF0DF request bits are cleared on completion.

OBSERVED: the complete A6 application envelope 0x100578-0x101436 plus
handlers 0x12641C-0x1266BC is now implicated by demonstrated SP↔A6
differentials. The earlier 0x260 bytes of excluded gaps are required
code: 0x10076C command-plus-delay, 0x100806 command-91 preparation, and
0x1008A2 command-50 geometry operation.

## 33.1 Geometry preparation / format chain

SP internal chain A6 replacement 4003A0 100806 40039C 1006F8(0010)
4003B8 1008A2 4003A4 100A58

OBSERVED: 0x100806 requires initialized context, derives a field from
(word\[401006\]-1)&0xF, and issues command 0x91.

OBSERVED: 0x1008A2 fills 0x5D0000-0x5D01FF with a 256-word pattern,
traverses geometry-indexed records, issues command 0x50, supplies data
through the existing output-transfer machinery, waits for interrupt
completion, and updates progress after each outer iteration.

STRONGLY INFERRED using ATA domain context: command 0x91 corresponds to
INITIALIZE DEVICE PARAMETERS and command 0x50 to FORMAT TRACK. The
firmware-derived description above does not depend on those names.

OBSERVED: A6 progress setup 0x15F4FE has supported SP homologue
0x154CAE; A6 progress update 0x15F600 has supported SP homologue
0x154D9A. Copying A6 UI state is unnecessary.

# 34. 0x4003B4 differential and periodic ATA status

OBSERVED: SP calls 0x4003B4 at 0x1054F4 during initialization status
assessment and at 0x105E5A in the periodic internal-device path. A6
contains neither a direct call encoding nor literal pointer to 0x4003B4.

OBSERVED: the A6 initialization homologue omits both the service call
and SP bit-6 state-4 override.

OBSERVED: the A6 periodic homologue preserves SP
deadline/state/hardware/busy gates, then clears 0x401078 bit 0, issues
command 0xE5 through 0x1006F8, returns 0 on command failure, reads byte
0x600004, and sets bit 0 when that byte is not 0xFF.

STRONGLY INFERRED using ATA domain context: 0xE5 is CHECK POWER MODE and
0x600004 is the returned Sector Count task-file byte. Keep the
firmware-level statement (test 0x600004 != 0xFF) distinct from the ATA
semantic interpretation.

REQUIRED BY DIFFERENTIAL: bypass SP 0x105E5E-0x105E68 bit-3 dispatch in
this periodic path. A6 has no corresponding dispatch. Retain SP bit-0
latch/release consumers 0x14D73A/0x14D758, which structurally correspond
to A6 0x15747C/0x15749A.

# 35. Complete opaque-service differential for native ATA operation

  ----------------- ----------------------------------------------------- --------------------------------------------------------------------
  SP service        Matched A6 behavior                                   Native-HDD consequence
  400394 / 400398   1006F8(E0) at matched internal paths                  Replace per demonstrated call site; do not globally alias services
  40039C            1006F8(10)                                            Replace matched internal calls
  4003A0            100806                                                Relocated envelope
  4003B8            1008A2                                                Relocated envelope; destructive geometry operation
  4003A4            100A58                                                IDENTIFY routine already in envelope
  4003B4            Eliminated in init; E5/status producer periodically   Required differential
  4003BC            Matched A6 helper is RTS                              Eliminate matched helper behavior
  ----------------- ----------------------------------------------------- --------------------------------------------------------------------

OBSERVED exception: SP diagnostic callback 0x124888 still calls
0x400398. It belongs to a Zip(ATAPI) diagnostic flow after a destructive
save/write/read/restore test; no normal
boot/mount/read/write/format/recovery route was identified. Leave it
unchanged and out of scope for native-HDD support.

IMPORTANT CORRECTION: SP 0x12E34A calls 0x400398 unconditionally in the
Save SysProg ROM-to-disk operation. The conditional on 0x401014 exists
in A6, not SP. A6 uses 1006F8(E0) when +14==0 and retains 400398 when
+14!=0.

CORRECTION to an intermediate conclusion: A6 probe 0x10126A can write 0
or 1 to 0x401014. The initialization clear alone does not guarantee
zero. A transplant must preserve this producer/classification and the A6
ROM-copy conditional.

# 36. Link Plan v2: static specification

Link Plan v2 is a read-only specification, not a patched firmware. It
supersedes v1 placement and shim assumptions. It copies both A6 blocks
completely and places all SP-specific glue after them.

  ------------------ ------------------ ----------------
  Source             Destination        Bytes
  A6 100578-101436   SP 17D000-17DEBE   0x0EBE
  A6 12641C-1266BC   SP 17DEBE-17E15E   0x02A0
  SP adapters        17E200-17E2AE      0x00AE
  Payload total                         0x120C (4,620)
  Address span       17D000-17E2AE      0x12AE (4,782)
  ------------------ ------------------ ----------------

OBSERVED: 64 absolute fixups are required: 18 copied-code references, 26
SP-helper substitutions, and 20 private-state references. All 207
decoded relative branches/BSRs stay within their copied block and
preserve displacement.

REQUIRED: helper substitutions include 126290→12380A, 1262A2→12381C,
163122→15833C, 16296C→157B6A, 135818→1309CA, 13583C→1309EE, plus
progress 15F4FE→154CAE and 15F600→154D9A.

REQUIRED: redirect 0x146DE2 callback-table base 0x4033AE to ROM
initializer 0x17C802 before reusing 0x4033AE-0x4033B5 as ATA private
state.

REQUIRED BY DIFFERENTIAL: internal reads route to relocated 0x100B2A;
writes to 0x100D2A; matched E0/10/preparation operations route to their
relocated routines/adapters; 0x1054F4 jumps past the obsolete
4003B4/bit6 block; 0x105E5A jumps to the E5 adapter; matched 4003BC
helper begins with RTS; ROM-copy 0x12E34A routes through the A6-style
+14 conditional adapter.

REQUIRED to preserve A6-observed transfer configuration: change SP
0x105472 immediate 0x0018 to 0x0050 so SP does not overwrite the
A6-selected E8/F8 configuration. Independent hardware necessity of
0x0050 remains unresolved.

## 36.1 Adapter status and safety

PROVISIONAL: cold adapter at 0x17E200 explicitly clears relocated
private state, clears 0x401001, invalidates cache association 0x4034D8,
then enters relocated A6 init. It is valid only under cold quiescence;
interrupt masking does not stop DMA.

PROVISIONAL: reinit adapter at 0x17E240 does not clear private state and
invalidates the 0x5D0000 cache association only after A6 init. It does
not prove an outstanding transfer has relinquished the buffer.

UNRESOLVED blockers before a hardware patch can be called safe:
warm-transfer quiescence; 0x5D0000 ownership; baseline
availability/initialization of 0x450/0x458 descriptors and selectors
0x48/0xA0/0xB0; coordination with shared 0xFFFFFFC0 users; runtime
validity of ROM placement and transfer configuration.

# 37. Current implementation status

STRONGLY INFERRED: A6 implements an application-side ATA compatibility
backend that replaces a coherent family of SP opaque internal-device
operations while preserving much of the SP upper storage/application
control flow. The functional differential for normal native ATA-HDD
operation is now bounded well enough to freeze static feature scope. The
next work is runtime-prerequisite validation, not further speculative
expansion of the old opaque backend.

Do not patch yet. Link Plan v2 is mechanically coherent but still has
explicit runtime safety conditions.

Do not globally redirect 0x400398: one A6 ROM-copy alternative retains
it, and the SP Zip diagnostic remains intentionally untouched.

Initial hardware validation should avoid the destructive 0x1008A2
geometry/command-50 path. First milestones should be cold init,
IDENTIFY/context sanity, controlled reads on expendable media, interrupt
completion, and absence of hangs/resets.

## 2026-10-04 --- Develop Monitor / SCI1 / CN7 investigation

### Boot-mode dispatch

**OBSERVED:** Application entry `100000` jumps to `12CC54`, which
initializes application RAM, installs four service trampolines through
`12CCC4`, and calls `1258D8`.

**OBSERVED:** The visible application diagnostic decision in `1258D8`
queries logical button codes `63` and `53` through `1381BC`; on success
it calls `1463C6` and then application diagnostic entry `123994`. The
diagnostic implementation is therefore application-resident, although it
uses opaque services.

**OBSERVED:** `1381BC` searches the 80-entry two-byte table at `1756D8`,
calls opaque service `400494` with the resulting matrix group, and tests
the selected bit. Logical codes `60–63` map contiguously to group 2 bits
0--3; code `53` maps to group 5 bit 0.

**HYPOTHESIZED:** Given the experimentally reported Status+FX D
combination, `60–63` may correspond to FX A--D, which would make
Status+FX C the `62 + 53` combination. The table alone does not
establish physical labels.

**OBSERVED:** No corresponding `62 + 53` test has been located in the
visible application boot dispatcher. The immediate `R0=62` occurrence at
`133148` calls `14717E`, not the button-query routine.

**UNRESOLVED:** The Status+FX C detector and complete C-specific
control-flow frontier. Plausible locations remain pre-application
selection, selection inside an opaque startup service, or a computed
application path. Absence of readable "Develop Monitor" text is not
evidence for mask-ROM residency.

### SCI1 hardware and configuration

**OBSERVED:** The main-board schematic routes the H8S/2653 SCI1 transmit
signal `P31/TXD1` to `TX1` on the unpopulated CN7 footprint. CN7 also
exposes `RX1` and `XRST`. The production PCB examined by the researcher
has no fitted CN7 connector but shows physical witness marks consistent
with pogo-pin contact.

**OBSERVED:** Routine `107A72` initializes the SCI1 register bank.
Relevant writes are `SMR1=00`, `BRR1=09`, and finally `SCR1=F0`. It
registers handlers through `40020C` at selectors `150`, `154`, and
`158`.

**OBSERVED:** `SCR1=F0` enables transmit-data-empty interrupts,
receive/error interrupts, transmitter, and receiver; multiprocessor and
transmit-end interrupt enables are clear. SCI1 uses normal asynchronous
framing under the recovered configuration. `107A72` does not write
SCMR1; normal operation therefore depends on inherited/reset state.

**STRONGLY INFERRED:** With the documented 20 MHz operating clock and
the H8 normal asynchronous SCI formula, `SMR1=00`, `BRR1=09` produces
**62,500 baud**: `20,000,000 / (32 × 1 × (9+1)) = 62,500`.

**OBSERVED:** SCI1 uses a 512-byte RX ring at `4102AA` with indices
`4104AA/4104AC`, and a 2048-byte TX ring at `40FAAA` with indices
`4104AE/4104B0`. `107B3C` returns a received byte or `FFFF` when empty;
`107B78` waits for a byte; `107B82` queues transmit data. `107BEE`
receives and queues bytes; it is not a command dispatcher.

### SCI1 proprietary protocol

**OBSERVED:** The recovered SCI1 protocol uses a fixed-token
request/reply grammar: - `107CB8`: transmits `82 10 8E`. - `107CCA`:
transmits `9D 9E`, requires response prefix `9D 05`, stores five
following identification bytes, and consumes one additional byte. -
`107D22`: transmits `99`, one argument byte, `9E`. - `107F54`: transmits
`92`, three packed argument chunks, encoded length, `9E`. - `107DD0`,
`107E18`, `107E78`: request lengths 1, 2, or 4, wait for `90`, and
reconstruct returned values. - `107D3C`: transmits `90`, three argument
chunks, packed block data, `9E`. - `107FD6`: transmits `95`, one byte
argument, encoded word, `9E`. - `107FFC`: transmits `96`, two byte
arguments, encoded word, `9E`.

**OBSERVED:** The address-like argument is encoded as three seven-bit
chunks, least-significant first: `arg & 0x7F`, `(arg >> 7) & 0x7F`,
`(arg >> 14) & 0x7F`. Exactly 21 argument bits are carried.

**OBSERVED:** Arbitrary block bytes are made seven-bit-clean by sending
up to seven low-seven-bit bytes followed by a bitmap containing their
original high bits. Word encoding uses two low-seven-bit bytes plus a
high-bit bitmap. No checksum accumulator/verifier has been identified in
this subsystem.

**STRONGLY INFERRED:** The SP-808 is the requester/client in the
inspected read path: it sends a `92` request and waits for a `90`
response. The recovered code is not an incoming arbitrary-address
monitor command interpreter.

**UNRESOLVED:** Peer identity, the address space represented by the
21-bit argument, and exact semantics of commands `95`, `96`, and `99`.

### SCI1 is distinct from MIDI

**OBSERVED:** The established MIDI implementation has MIDI-specific
status-class dispatch (`80–EF`), channel extraction, running status,
separate realtime handling, `F0/F7` SysEx framing, Roland manufacturer
byte `41`, device/model checks, and modulo-128 checksum machinery.

**OBSERVED:** The SCI1 subsystem instead uses complete-byte transaction
tokens such as `82`, `8E`, `90`, `92`, `95`, `96`, `99`, `9D`, and
terminator `9E`; it has no identified MIDI channel decoding, running
status, realtime interleaving, `F0/F7` framing, Roland
manufacturer/device checks, or MIDI checksum machinery.

**OBSERVED:** The raw MIDI identity response at `1761BE` is
`F0 7E 10 06 02 41 2B 01 00 00 00 02 00 00 F7`, structurally distinct
from SCI1's `9D 05 ...` identification exchange.

**STRONGLY INFERRED:** SCI1 is a **separate proprietary 62,500-baud
serial request/reply protocol**, not the SP-808's ordinary MIDI
transport.

**HYPOTHESIZED:** Its seven-bit-clean payload representation may reflect
a MIDI-inspired design convention, but historical derivation is
unresolved and should not be used architecturally.

### CN7 interpretation

**OBSERVED:** CN7 is unpopulated on the examined production board, while
its pads show witness marks consistent with pogo-pin contact.

**STRONGLY INFERRED:** CN7 was intended to be physically contacted by
production/development equipment. This is stronger than treating it
merely as an unused expansion footprint.

**HYPOTHESIZED:** The SCI1 protocol may communicate with
factory/development fixture equipment attached through CN7.

**UNRESOLVED:** Whether Status+FX C activates SCI1, whether `XRST` is
involved in the protocol, and whether the peer is fixture equipment, a
programmable subsystem, or another development target.

**Methodological constraint:** Do not merge the CN7/SCI1 investigation
with Develop Monitor merely because both are development-adjacent. A
direct reachability or hardware observation is required.

### High-value validation

A passive capture of CN7 `TX1` during ordinary boot, Status+FX C, and
Status+FX D can test the relationship without transmitting into the
unit. Decode at 62,500 baud, 8N1. The recovered `82 10 8E` sequence is a
useful fingerprint if `107C86` executes.

# 2026-10-04 — Historical ATAPI emulator traces and formatter correlation

## Provenance

**OBSERVED — contemporaneous correspondence (2023):** Rabbit Hole Computing was developing writable 100 MB Zip emulation for ZuluIDE and acquired an SP-808 specifically to test bespoke ATAPI-host behavior. Earlier independent work used a custom CPLD/ARM ATAPI emulator with bus-sniffer firmware. These records are useful experimental provenance, but statements in email prose remain historical reports unless supported by the captured bus traffic.

**UNRESOLVED:** A later filename containing `vs840` does not by itself establish the host model of that capture.

## Internal SP-808 ATAPI sequence confirmed by historical traces

**OBSERVED:** Successful-enough initialization traces show the internal device path issuing, in order, SRST, `A1` IDENTIFY PACKET DEVICE, `EF` SET FEATURES variants, ATA `A0` PACKET transactions carrying REQUEST SENSE `03`, START/STOP `1B`, INQUIRY `12`, MODE SENSE(10) `5A` page `2F`, MODE SELECT(10) `55`, vendor/device-specific `0D`, READ FORMAT CAPACITIES `23`, READ CAPACITY `25`, PREVENT/ALLOW `1E`, and normal READ(12) `A8` / WRITE(12) `AA` block traffic.

**OBSERVED:** This differs mechanically from the application-visible target-indexed backend, which uses MODE SENSE(6) `1A`, MODE SELECT(6) `15`, vendor `06`, READ CAPACITY `25`, READ(10) `28`, and WRITE(10) `2A`. This strengthens the two-backend model and supersedes attempts to identify the visible target path as the implementation of the physically sniffed internal Zip traffic.

**OBSERVED:** One historical emulator identified itself differently from literal `IOMEGA ... ZIP` yet progressed beyond INQUIRY into page-2F setup, capacity queries and READ(12). Therefore the internal ATAPI path must not be assigned the literal IOMEGA/ZIP acceptance gate recovered for the target-indexed backend.

## Formatter-to-bus correlation

**OBSERVED:** Static analysis now explains the historical formatting writes. `1058CC` builds the disk header/partition records and `1064DE` initializes each nonempty partition. For partition start `P` and allocation-table length `F`:

```text
P              partition boot/filesystem header
P+1 .. P+F     allocation table #1
P+1+F .. P+2F  allocation table #2
next 32 blocks root directory
remainder       data area
```

For the examined geometry `P=0x20`, `F=9`, giving allocation table #1 at `0x21..0x29`, allocation table #2 at `0x2A..0x32`, root directory at `0x33..0x52`, and data from `0x53` onward. Block 0 contains the disk header and four 16-byte partition entries, with `FA` at offset 0 and `55 AA` at offsets `1FE..1FF`.

**OBSERVED:** `F` is calculated from partition length; nine blocks is not a magic media-size constant. The small-table branch produces a FAT-like initial `F8 FF FF` and the firmware contains literal `FAT12   ` / `FAT16   ` identifiers. The duplicated tables, reserved bytes and consumers strongly support FAT12/FAT16 allocation-table semantics.

**OBSERVED:** The historical bus trace attempted `WRITE(12)` at LBA `0x21`, count `9`. When that first table write reports failure, `1064DE` skips the second table, root directory and partition-header writes. `1058CC` clears the failed partition's intermediate record but nevertheless proceeds to write logical block 0.

**STRONGLY INFERRED:** The observed sequence `WRITE(12) LBA 0x21 count 9 -> failure -> WRITE(12) LBA 0 count 1` is the application-predicted failed-first-allocation-table path, not a successful quick format.

**OBSERVED:** Higher-level format orchestration can discard formatter failure. `14F71A` does not require the result of `1058CC`; a traced completion path selects the literal `Completed.` without testing formatter success or `40101E`. Thus a completion UI is not evidence that media writes succeeded.

**UNRESOLVED / LOW PRIORITY:** The precise device-side reason the old emulator failed the multi-block WRITE(12), including exact DRQ phase behavior. This is relevant to faithful Zip emulation but is not a prerequisite for the A6-native ATA HDD transplant.

## Project consequence

The historical failure should no longer be used as evidence for a capacity whitelist or generic HDD rejection. It is explained by the stock internal ATAPI formatter attempting filesystem writes that the emulator did not successfully complete. The HDD project should remain focused on transplanting the A6 application-side native ATA backend rather than making the legacy SP ATAPI backend accept HDDs.

# 38. 5 October 2026: H8S/2653 manual reconciliation, inherited service layer, and transfer arbitration

**Manufacturer source used for this update:** Renesas, *H8S/2655 Group Hardware Manual*,
Rev. 5.00 (2006-09), applicable to HD6432653/H8S/2653. Relevant sections:
MCU operating modes and memory map (pp. 75-79), interrupt vector table
(pp. 104-107), DTC (pp. 309-339, especially pp. 311, 322-335), TPU
(pp. 427-509, especially pp. 434-435, 464, 498-499), and Appendix B
internal I/O registers (especially pp. 930-931).


This section supersedes earlier MCU-resource interpretations where they conflict.

## 38.1 Manufacturer-documented DTC mapping

**DOCUMENTED MCU ARCHITECTURE:** The HD6432653 includes both a DMAC and a
Data Transfer Controller (DTC). DTC register information is stored in on-chip
RAM rather than in a conventional directly addressed peripheral register bank.
The manual identifies the DTC register-information region as
`0xFFF800-0xFFFBFF` in advanced mode. DTC enable registers are
`0xFFFF30-0xFFFF35` and DTVECR is `0xFFFF37`.

**DOCUMENTED MCU ARCHITECTURE:** For interrupt-activated DTC operation, each
activation source has a two-byte DTC vector-table entry. The manual's table 8.4
gives exact entries:

| Activation source | CPU vector | DTC vector entry | DTC enable bit |
|---|---:|---:|---|
| IRQ2 | 18 | `0x0424` | DTCEA5 |
| TGI1A / TPU1 compare A | 40 | `0x0450` | DTCEB1 = `FFFF31` bit 1 |
| TGI2A / TPU2 compare A | 44 | `0x0458` | DTCEC7 = `FFFF32` bit 7 |

The vector entry contains the lower address bits of DTC register information
located in on-chip RAM; in advanced mode this corresponds to the
`0xFFxxxx` address formation observed in A6.

**UPGRADED TO DOCUMENTED + OBSERVED:** A6 words `0x450` and `0x458` are not
an arbitrary Roland descriptor-pointer table. They are the manufacturer-defined
DTC vector entries for TGI1A and TGI2A. A6's use of `FF0000 + word[450/458]`
is the expected advanced-mode reconstruction of the on-chip-RAM DTC
register-information address.

## 38.2 TPU1/TPU2 mapping and A6 ATA transfer mechanism

**DOCUMENTED MCU ARCHITECTURE:** `FFFFC0` is TPU Timer Start Register TSTR;
bit 1 starts/stops TPU channel 1 and bit 2 starts/stops TPU channel 2.
`FFFFE0-FFFFEA` is TPU1, including `TGR1A=FFFFE8`.
`FFFFF0-FFFFFA` is TPU2, including `TGR2A=FFFFF8`.
TGI1A and TGI2A are the corresponding TGR1A/TGR2A compare-match/input-capture
sources, and both are valid DTC activation sources.

**STRONGLY INFERRED, now manufacturer-corroborated:** The A6 native ATA data
path uses TPU1/TGI1A and TPU2/TGI2A to pace H8S DTC transfers between the
fixed SLA919F-side endpoint `0x600000` and RAM. This is not ATA bus-master DMA.
The remaining uncertainty is the exact gate-array-side meaning of `0x600000`,
not the H8S timer/DTC mechanism.

**DOCUMENTED MCU ARCHITECTURE:** On terminal DTC conditions the corresponding
DTC enable bit is cleared and the activation-source interrupt can be presented
to the CPU; on non-terminal transfers the DTC can consume/clear the activation
source while remaining enabled. Therefore the A6 CPU handlers must not be
described as servicing every timer compare event.

## 38.3 F0DF arbitration and `Drive Too Busy.`

**OBSERVED:** A6 sets `FFFFF0DF` bit 1 when the TGI1A/DTC transfer activation
is outstanding and bit 2 for the TGI2A/DTC direction. Completion handlers
clear these bits and may re-arm them for another segment.

**OBSERVED:** SP `12BE62` and A6 homologue `12F96E` both wait until
`(FFFFF0DF & 0x06) == 0` before changing the shared transfer environment.

**OBSERVED:** SP routine `129764` calls `12BE62(1)` before saving TSTR and
writing `TSTR=0x21`, which stops TPU1/TPU2, then restores TSTR and calls
`12BE62(0)`. Thus the previously identified TPU1/TPU2 interference is guarded
by an explicit transfer-quiescence wait, not an unguarded timer stop.

**STRONGLY INFERRED:** `F0DF[1:2]` are software markers for outstanding
transfer-engine activations and participate in a shared transfer-quiescence
protocol. They are not a complete storage-command mutex.

**OBSERVED:** `"Drive Too Busy."` at ROM `17C1CE` is displayed through record
`17BE06`, table entry 9, and consumer `146E50`, which consumes
`427C8A` bit 6. Five explicit setters of that latch were identified
(`1275D2`, `127A42`, `127D44`, `149244`, `155810`). Two producers use
remaining-margin comparisons `record[6]-record[2] <= 0x00F0` and
`record[6]-record[A] <= 0x00F0`.

**NEGATIVE RESULT:** No identified `"Drive Too Busy."` producer directly tests
`F0DF` bits 1/2. The message belongs to a higher-level realtime
buffer/scheduling-pressure mechanism, not an established failure return from
the transfer-environment wait.

## 38.4 `0x400xxx` provenance correction

**OBSERVED:** `0x400000` upward is external memory in the SP system mapping;
the visible application treats `0x400xxx` as executable DRAM-resident platform
services plus nearby shared state.

**OBSERVED:** Visible SP startup does not populate the service bodies before
its first call into them. It generates only four absolute-jump veneers:

| Destination | Generated jump target |
|---|---:|
| `400210` | `1309CA` |
| `400214` | `1309EE` |
| `400218` | `10589C` |
| `400364` | `128F52` |

The first observed service call on this application-entry path is
`1258EC -> 400348`. A6 has the same startup structure and likewise depends on
an inherited environment.

**CORRECTION:** `0x400xxx` should no longer be described as "internal ROM
services." The correct current description is **inherited DRAM-resident
platform service layer, provenance unresolved**. Its executable bytes are
absent from the supplied application image/database but must already exist
before the visible application calls them.

**DOCUMENTED MCU CONTEXT, NOT SP MODE-PIN PROOF:** The HD6432653 manual states
that Mode 6 is advanced expanded mode with on-chip ROM enabled and a 16-Mbyte
address space; the H8S/2653 provides 64 KiB of on-chip ROM at
`0x000000-0x00FFFF` in that mode. This makes an earlier boot/service source in
on-chip ROM architecturally possible, but the SP's physical mode selection and
the writer/source of the inherited `0x400xxx` layer have not been established
by the current evidence.

**TEST PRIORITY:** A post-boot runtime dump of `0x400000-0x400FFF` would
recover the actual service entry/code bytes resident in DRAM. If entries branch
outside that page, expand the capture. A reset-to-application-entry write trace
would be required to establish provenance.

## 38.5 Transplant consequence

Link Plan v2 remains the mechanically authoritative relocation/fixup census,
but its integration semantics are superseded pending v3. The manufacturer
manual removes major ambiguity around `450/458`, `FFFF31/32`, TSTR, TPU1/2 and
the TGI1A/TGI2A DTC mechanism. Remaining integration questions are narrower:
segment-boundary arbitration/races, explicit initialization of DTC vector
entries/register information, handler routing, warm scratch-buffer safety, and
the inherited platform-service contracts actually required by the transplant.

## 5 October 2026 clarification: programmed DTC vectors and common SP/A-6 hardware

**CORRECTION:** The DTC vector *addresses* `0x0450` (TGI1A) and `0x0458`
(TGI2A) are fixed by the H8S architecture, but the 16-bit words stored there
are part of Roland's programmed HD6432653 on-chip ROM image. They are not
universal hardwired descriptor values and are not application-writable RAM.

**OBSERVED / PHYSICAL CONTROL CASE:** A6 application firmware has been run on
SP-808 hardware and successfully operated an IDE HDD. The relevant SP-808 and
A-6 PCB/schematic implementation is established as identical 1:1 for this
hardware path. Therefore the successful A6 ATA/DTC path used the SP-808
machine's existing MCU on-chip-ROM vector words and common hardware resources.

**STRONGLY INFERRED:** On the demonstrated SP-808 hardware, the programmed
words at `0450/0458` are compatible with A6's construction of DTC
register-information addresses as `0xFF0000 + word[0450/0458]`, and with its
descriptor placement/use in H8S on-chip RAM. The transplant does **not** need
to establish or rewrite `0450/0458`.

**SCOPE:** This compatibility conclusion applies to the demonstrated/common
SP-808/A-6 hardware and its MCU ROM contents. It must not be generalized to an
HD6432653 carrying a different on-chip-ROM image without evidence.

**UPDATED TRANSPLANT QUESTION:** The remaining issue is not "who initializes
the DTC vector words?" Roland's programmed MCU ROM does. The integration work
must instead preserve/use the existing vector contents, initialize the
referenced DTC register-information structures as A6 expects, establish the
required interrupt handlers/enables, configure TPU1/TPU2, and avoid resource
conflicts.

**UPDATED `400xxx` INTERPRETATION:** Because the A6 application runs on the
same relevant hardware and inherits the same pre-application platform
environment, retained A6 calls into `400xxx` are increasingly consistent with
a common Roland platform-service ABI already available on SP hardware.
The provenance and implementation bytes of that DRAM-resident layer remain
unresolved; this does not justify assigning unobserved semantics to individual
services.

