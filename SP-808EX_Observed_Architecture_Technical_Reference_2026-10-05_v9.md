Roland SP-808EX ESP and Firmware Architecture

Observed Technical Reference

Firmware: SP8EXall.bin \| Runtime ROM base: 0x100000 \| Evidence state:
4 October 2026

Scope: Application-visible architecture reconstructed from firmware
bytes, IDA control/data flow, and diagnostic behavior. Existing semantic
names are not treated as proof. Inherited platform services remain an opaque
lower-layer boundary.

Confidence vocabulary: OBSERVED = directly established by
bytes/instructions/diagnostic mapping; STRONGLY INFERRED = best
explanation with converging evidence; HYPOTHESIZED = plausible but not
yet discriminated; UNRESOLVED = evidence insufficient.

# 1. System architecture

H8S application firmware (external ROM @ 0x100000)

\|

+\-- baseline service ABI @ 0x400xxx \[implementation partly outside
image\]

\|

+\-- ESP host interface

control/status: 0xC00003, 0xC02000..0xC02005

PRAM0: 0xC00000 + 4\*i

PRAM1: 0xC01000 + 4\*i

RAM shadows: 0x4104C2 / 0x4110C2

\|

+\-- PRAM processing records

+\-- indirect operations involving IRAM0/IRAM1/GRAM/ERAM

OBSERVED: Diagnostic UI names the target DEVICE(ESP) and separately
reports PRAM0, PRAM1, IRAM0, IRAM1, GRAM and ERAM.

OBSERVED: PRAM0 and PRAM1 are directly mapped to 0xC00000 and 0xC01000
respectively for 768 tested four-byte entries per bank.

UNRESOLVED: Physical ESP chip identity, complete capacities, clocking,
instruction set, and exact meanings of the memory acronyms beyond their
firmware labels.

# 2. Address map

  ---------------------- ---------------------------------------------------------------------- ----------------------------------------------------------
  Address / range        Role                                                                   Evidence
  0x100000+              External H8 application ROM                                            OBSERVED
  0x400xxx               Baseline RAM/service ABI; selected entries overridden by application   OBSERVED interface; implementation partly unresolved
  0x401000               Shared storage/device parameter structure                              OBSERVED
  0x401016               32-bit extent used as inclusive terminal block in copy subsystem       STRONGLY INFERRED globally; observed consumer arithmetic
  0x4104C2               PRAM0 RAM shadow base                                                  OBSERVED
  0x4110C2               PRAM1 RAM shadow base                                                  OBSERVED
  0x411CC5               ESP control-byte shadow for C02003                                     OBSERVED
  0xC00000               PRAM0 bank base / common result-read port in special mode              OBSERVED
  0xC01000               PRAM1 bank base                                                        OBSERVED
  0xC00003 bit 7         ESP busy/readiness poll                                                OBSERVED
  0xC02003               ESP mode/control byte                                                  OBSERVED
  0xC02000..05           ESP control register group                                             OBSERVED
  0x15E470..0x15E754     247 x 3-byte configuration-type-1 PRAM image                           OBSERVED
  0x15A447               16-record diagnostic image -\> PRAM0                                   OBSERVED
  0x15A477               115-record diagnostic image -\> PRAM1                                  OBSERVED
  \~0x162078..0x1657xx   Named production-effects candidate region                              OBSERVED strings; structure HYPOTHESIZED
  ---------------------- ---------------------------------------------------------------------- ----------------------------------------------------------

# 3. Startup and 0x400xxx service boundary

OBSERVED: External ROM entry 0x100000 jumps to 0x12CC54. Startup clears
application RAM, copies 0x17C454..0x17C880 to 0x403000..0x40342D,
installs four absolute-JMP overrides, then calls code that immediately
uses pre-existing 0x400xxx services.

// 0x12CCC4 override installer, conceptual

for each {ram_entry, flash_target} until 0xFFFFFFFF:

\*(uint32_t\*)ram_entry = 0x5A000000 \| flash_target; // H8 absolute JMP

0x400210 -\> 0x1309CA

0x400214 -\> 0x1309EE

0x400218 -\> 0x10589C

0x400364 -\> 0x128F52

STRONGLY HYPOTHESIZED: Internal factory ROM or an earlier boot layer
establishes the baseline 0x400xxx service environment. ROM extraction is
not required for application-side ABI reconstruction.

# 4. ESP control and PRAM access

## 4.1 Ordinary PRAM write

// 0x108A7E, conceptual

selector -\> bank/offset

wait_ready();

shadow\[selector\] = W;

\*(volatile uint32_t\*)hardware_addr(selector) = W;

wait_ready();

OBSERVED: PRAM diagnostic writes byte-reversed index patterns to all 768
tested entries and reads them back successfully by contract.

## 4.2 Selected PRAM read / common port

// 0x1099A6, conceptual

C02003.bits\[1:0\] = 3;

wait(C00003.bit7 == 0);

\*(selected_PRAM_address) = 0; // selects read address in this mode

wait(C00003.bit7 == 0);

short_delay();

result = \*(uint32_t\*)0xC00000; // common readback port

C02003.bits\[1:0\] = 0;

OBSERVED: In this mode, the zero write is a read-selection transaction
rather than an ordinary overwrite.

## 4.3 PRAM loader

// 0x1097F6-family loader behavior

for (j = 0; j \< count; j++) {

a = rom\[3\*j+0\]; b = rom\[3\*j+1\]; c = rom\[3\*j+2\];

W = (a\<\<24) \| (b\<\<16) \| (c\<\<8);

PRAM\[start_index+j\] = W;

shadow\[start_index+j\] = W;

}

// unused tail is zeroed; control bit 4 is cleared during load and set
afterward

UNRESOLVED: C02003 bit 4 meaning. \"Execution enable\" is not
established.

# 5. Configuration-type-1 PRAM image

  ------------------------ -------------------
  Property                 Value
  ROM source               0x15E470
  Inclusive ROM range      0x15E470-0x15E754
  Record count             247 (0xF7)
  ROM record width         3 bytes
  PRAM bank                PRAM1
  Starting index           0x03C
  First hardware address   0xC010F0
  Last image index         0x132
  ------------------------ -------------------

OBSERVED: After loading indices 0x03C-0x132, the loader zeroes
0x133-0x2FF and later writes special word 0xF14E3700 at index 0x2F2.

## 5.1 Record field evidence from coefficient patching

ROM triple \[byte0, byte1, byte2\]

coefficient pair:

record N: byte0 = q15\[14:7\]

byte1 low 2 bits = scale code

remaining byte1/byte2 bits preserved

record N+1: byte0 low 7 bits = q15\[6:0\]

byte1 low 2 bits = same scale code

remaining fields preserved

q15 = (recordN.byte0 \<\< 7) \| (recordN1.byte0 & 0x7F)

STRONGLY INFERRED: Preserved fields include operand/reference-like
information. Candidate field A=(byte1\>\>2)\|((byte2&1)\<\<6) advances
consecutively across duplicated filter structures.

UNRESOLVED: Global record format. The fourth hardware byte is meaningful
under other update modes, so a three-byte ROM record is not necessarily
a complete hardware instruction.

# 6. Filter coefficient path

OBSERVED: 0x101D16 takes signed R0=f, signed E0=a, and ER1 destination,
and writes five consecutive binary32 values. All four identified callers
supply a=71.

F = binary32(selected_rate_value \* 1000)

x = binary32(f \* pi / F)

A = binary32(a / 100)

g = binary32(opaque_service_result(x))

h = binary32(1 / F)

t = binary32(2 \* F \* g)

B = ((h\*h) \* t) \* t

T = t / ((A\*x) / g)

D = binary32(2\*h\*T + B + 4)

out\[0\] = binary32(4 / D)

out\[1\] = binary32(-2 \* out\[0\])

out\[2\] = out\[0\]

out\[3\] = binary32((8 - 2\*B) / D)

out\[4\] = binary32((2\*h\*T - B - 4) / D)

STRONGLY INFERRED: This is a second-order filter coefficient generator.
The \[b,-2b,b\] numerator supports a high-pass interpretation for this
vector; a related vector has low-pass-like numerator coefficients with
the same final two terms.

HYPOTHESIZED: Opaque service 0x400584 is tangent-like. The unavailable
implementation prevents promoting this to observed.

## 6.1 Routing and destinations

Q.word68 \<= 200:

f = low16(unsigned(Q.word68) \* 100)

coeff\[5\] = sub_101D16(f, 71)

choose update order based on f vs cached previous f

for k in selected_order:

W = pack_coefficient(coeff\[k\]) // 0x10946E

write_packed_parameter(selA\[k\], W) // 0x108C12

write_packed_parameter(selB\[k\], W)

  --- -------- -------- -----------------
  k   selA     selB     PRAM1 addresses
  0   0x1118   0x1140   C01118 / C01140
  1   0x1120   0x114C   C01120 / C0114C
  2   0x1128   0x1154   C01128 / C01154
  3   0x1130   0x115C   C01130 / C0115C
  4   0x1138   0x1164   C01138 / C01164
  --- -------- -------- -----------------

## 6.2 Coefficient packing

// 0x10946E simplified structural view

normalize c into one of ranges (-1,1), (-2,2), (-4,4), (-16,16)

attach 2-bit scale code

n = integer(y \* 32768 + 1)

q = arithmetic_shift_right(low16(n), 1)

if (q == 0x4000) q = 0x3FFF

q &= 0x7FFF

W = ((q \<\< 17) & 0xFF000000)

\| ((q \<\< 18) & 0x00FC0000)

\| ((q \<\< 2) & 0x00000100)

\| scale_bits

OBSERVED: Hardware receives custom packed coefficients, not IEEE-754
binary32.

## 6.3 Special two-record update: 0x108C12

S0 = (oldS0 & 0x00FCFFFF) \| (W & 0xFF030000)

S1 = (oldS1 & 0x00FCFFFF)

\| ((W \<\< 6) & 0x3F030000)

\| (((W & 0xFFFF) \<\< 22) & 0xC0000000)

// hardware receives one packed W while C02003 bit0 is set

// software shadow predicts resulting fields in two neighbouring PRAM
records

OBSERVED: 0x108C12 sets control bit 0, waits for readiness, updates two
shadow words, sends one packed transaction to the selected PRAM address,
waits again, and clears the mode bit.

# 7. Temporary PRAM initialization operation

PRAM1\[0x03C\] = 0x00001400;

for (i=0; i\<115; i++) {

k = 0x03D + 6\*i;

Q = 0x474 \* i; // 0,1140,\...129960

write six-word base template at k;

P = encode_Q_mode10(Q); // 0x1097BE

special_update_bit1(k, P); // 0x108D06

}

wait(rate_dependent_interval);

clear PRAM1 indices 0x03C..0x2FF;

load selected normal PRAM image;

OBSERVED: The rate table used by the residence-time calculation contains
48000, 44100 and 32000. For default multiplier 1000, the shared-counter
waits are 60, 65 and 90 increments respectively.

STRONGLY INFERRED: This is an autonomous initialization operation
installed into ESP PRAM and allowed to run for a calculated interval
before removal.

HYPOTHESIZED: Q addresses another ESP-managed state store and the
operation clears/initializes state or history. Q unit and target memory
remain unresolved.

# 8. ESP diagnostic architecture

  ------- ------------- -----------------------------------------------------
  Name    Failure bit   Test mechanism
  PRAM0   0x0001        Direct 768-entry store/read
  PRAM1   0x0002        Direct 768-entry store/read
  IRAM0   0x0004        PRAM-driven functional test; common result
  IRAM1   0x0008        PRAM-driven functional test; common result
  GRAM    0x0010        PRAM-driven functional test; common result
  ERAM    0x0020        PRAM-driven fixed-Q functional tests; common result
  ------- ------------- -----------------------------------------------------

OBSERVED: Diagnostic image 0x15A447 loads 16 records into PRAM0 indices
0x000-0x00F; 0x15A477 loads 115 records into PRAM1 indices 0x000-0x072.

## 8.1 ERAM Q encoding

// same 18-bit quantity, two control modes

encode_mode10(0x1234) = 0x80341200 // 0x1097BE

encode_mode01(0x1234) = 0x40341200 // 0x109786

mode10 transaction -\> selector 0x107C (C0107C)

mode01 transaction -\> selector 0x1098 (C01098)

STRONGLY INFERRED: The mode-10 and mode-01 forms are write-like and
read-like operations on logical ERAM location 0x1234. This is supported
by their placement in the diagnostic around supplied data and result
checking.

UNRESOLVED: ERAM physical mapping, address unit, capacity and precise
operation semantics.

# 9. Numerical service ABI

  -------------------------- ----------------------------------------------- --------------------------------------------
  Entry                      Application-side contract                       Status
  0x40058C                   binary64 -\> opaque 32-bit representation O32   STRONGLY INFERRED conversion
  0x400584                   O32 -\> O32 unary operation                     OBSERVED interface; operation unresolved
  0x400588                   O32 -\> binary64                                STRONGLY INFERRED conversion
  0x40056C                   two O32 operands -\> O32                        OBSERVED interface
  0x400558/568/570/57C/580   other unary/binary O32 operations               OBSERVED call family; semantics unresolved
  -------------------------- ----------------------------------------------- --------------------------------------------

OBSERVED: Callers consume pointed results immediately and do not test
explicit completion/error status.

# 10. Storage subsystem boundary (condensed)

OBSERVED: Copy Disk reads/writes 0xC0 blocks per batch, 16 batches per
iteration, with 512 bytes per block and 0xC00 blocks per iteration.

STRONGLY INFERRED: 0x401016 is treated by Copy Disk as an inclusive
terminal block address: copy arithmetic repeatedly uses V+1. A
partition-building path uses V without +1, leaving an unresolved
one-block convention discrepancy.

// Copy iteration start

V = \*(uint32_t\*)0x401016;

start = max(0, (V + 1) - (iteration + 1) \* 0xC00);

// source snapshot

0x40FAA4 = V;

// destination compatibility check after refresh

if (\*(uint32_t\*)0x401016 != 0x40FAA4)

lower_state = 8;

OBSERVED: Copy UI workflow state at 0x427C4A is a 16-bit
sequencing/display state, not a media-size index. State 12 displays
Wrong Media Size after lower state 8 at the initial position.

# 11. Superseded interpretations

0x174Bxx as a media-capacity policy table: superseded. It contains
timed-action records and UI pointer pairs.

0x427C4A as a media index: superseded. It is Copy FX/Copy Disk workflow
state.

0x40AA at 0x1589C0 as a repeating DSP record header: superseded. It is
an H8 branch instruction.

0x1589D2-0x1599D1 as DSP coefficient/program data: superseded. It is a
16 x 256 D-Beam lookup bank.

0x1599D2 timing words as established 44.1/32 kHz stereo/mono modes:
superseded. They are hardware timing/config integers; exact mode
meanings remain unresolved.

0x400584/588/58C as direct DSP-register writes: superseded. They form an
opaque numerical service ABI.

# 12. Production effects region: current frontier

OBSERVED: IDA identifies plausible effect-name literals in the
0x162xxx-0x165xxx region, including DL:Hi-Pass, CH:SBF-325, RV:LrgHall,
DN:Limiter, SY:Beam #1 and SL:Slicer1. The region also contains
printable byte runs that may be binary data misidentified as strings.

HYPOTHESIZED: The region contains production effect records and/or PRAM
templates. No end-to-end trace from one named effect to ESP PRAM has yet
been established.

Highest-value next investigation: reconstruct this region from raw bytes
and xrefs, then trace one named effect through selection code, ROM
record/template, PRAM loader, and runtime patches.

# Appendix A. Key routines

  -------------------- ----------------------------------------------------------------
  Address              Role / current interpretation
  0x101D16             Five-coefficient second-order filter generator
  0x108170             ESP configuration transition / cleanup / load sequence
  0x1086FC             Temporary 115-template initialization operation
  0x108A7E             Ordinary PRAM word writer
  0x108C12             Special packed two-record coefficient update; control bit 0
  0x108D06             Special packed five-record/address-field update; control bit 1
  0x108E96             Common-port result read
  0x10946E             binary64 coefficient -\> ESP packed numerical field
  0x109786             18-bit Q encoder, control bits 01
  0x1097BE             18-bit Q encoder, control bits 10
  0x1097F6             PRAM ROM-image loader family
  0x109956             Bounded preliminary ESP readiness wait
  0x1099A6             Selected PRAM read via common port
  0x10C816             Filter parameter update and PRAM routing
  0x12D228             ESP diagnostic UI/test entry
  0x12D264             PRAM0 direct test
  0x12D2DC             PRAM1 direct test
  0x12D3C0             IRAM0 functional test
  0x12D4C8             IRAM1 functional test
  0x12D5D4             GRAM functional test
  0x12D398..0x12D736   ERAM setup and four functional checks
  0x12D96E             NG/OK result display helper
  -------------------- ----------------------------------------------------------------

# Appendix B. Working invariants

Existing IDA names/comments are navigation aids, not evidence.

Raw firmware bytes and direct instructions outrank derived semantics.

Hardware diagnostic labels are primary firmware evidence for
subsystem/memory names.

PRAM storage/readback behavior does not by itself prove conventional
instruction execution.

Runtime patching of preserved PRAM fields supports structured processing
records, but instruction semantics remain unresolved.

The inherited 0x400xxx platform service layer is treated as an opaque lower layer;
application-visible ABI reconstruction does not depend on obtaining it.

# 13. 3 October 2026 architecture update: executable ESP programs

This section supersedes the earlier record-format uncertainty in
Sections 5-7 where those passages conflict with the results below. The
three-byte production records are now best modeled as executable
instructions for a TC170C140-compatible Roland ESP architecture, with
SP-808-specific compatibility corrections.

## 13.1 ROM-to-ESP normalization

ROM bytes: a b c

H8 PRAM write: (a\<\<24) \| (b\<\<16) \| (c\<\<8)

Normalized ESP word: D = (c\<\<16) \| (b\<\<8) \| a

For ordinary arithmetic records, the low ten bits decompose into an
8-bit coefficient/immediate plus two shift bits, while bits 10-17 carry
the operand/address and the opcode is selected from the upper field. For
jumps, the same low ten bits behave as a single target immediate.

## 13.2 Production-image architecture

200 preset records map onto 25 processing types.

Each type has a distinct PRAM image and parameter handler; named presets
patch parameters of the type image rather than embedding a separate
program per preset.

All images load into PRAM1 beginning at index 0x03C.

The complete production corpus contains 8,381 records.

Runtime host patches alter coefficients, operands/fields, and ERAM
transaction fields without replacing the surrounding instruction
schedule.

## 13.3 Opcode census and compatibility status

  ------------- ------- ---------------------------------------------------------------
  Opcode        Count   Current technical status
  00            2637    Accumulator A arithmetic; includes all-zero records
  04            1015    Replace accumulator A
  08            151     IRAM store + replace A
  0C            27      Delayed-B IRAM store + replace A
  10            231     Accumulator B arithmetic
  14            304     Replace accumulator B
  18/1C         72      IRAM stores with B-family accumulator behavior
  30            530     Coefficient-register multiplication/modifiers
  34            2086    Special family: coefficient writes, ERAM, jumps, B0 extension
  40/44/48/4C   139     Raw/rectified IRAM store variants
  50            63      Condition-related; exact SP-808 semantics unresolved
  58/5C         1057    Saturated IRAM stores
  78/7C         69      Interpolation/store-negative-compatible family
  ------------- ------- ---------------------------------------------------------------

No production-image occurrences were found for direct GRAM 20/24/38/3C
or interpolation 60/64/68/6C/70/74 families. The diagnostic separately
proves that GRAM exists; opcode absence here is only a statement about
the 25 production programs.

## 13.4 Jump correction

SP-808 jump target:

target = D & 0x3FF

STRONGLY INFERRED: all 31 production jumps become forward, in-image
targets under this 10-bit rule. A low-byte-only interpretation
misdirects 22 jumps. Present jump subtypes are D0, D2 and D3. Published
condition meanings are decoder-derived context; exact SP-808 branch
latency and side effects remain to be validated.

## 13.5 Experimental 34/B0

OBSERVED: exactly one 34/B0 occurs in the corpus, in type 05 at PRAM
index 0x046. STRONGLY INFERRED: it receives the delayed ramp accumulator
and writes coefficient register 0 inside a bounded ramp/crossfade
sequence. A host-visible endpoint/status handshake is plausible but
remains HYPOTHESIZED. Do not generalize B1-BF.

## 13.6 ERAM runtime fields

Host Q/address pack:

P = mode \| ((Q & 0xFF)\<\<16) \| (Q & 0xFF00) \| ((Q\>\>16)&3)

Across five normalized ESP records:

E0 = read/write mode

E1 = Q bits 0..4

E2 = Q bits 5..9

E3 = Q bits 10..14

E4 = Q bits 15..17

OBSERVED: all initial production ROM images have zero ERAM fields. The
H8 decorates selected five-record groups at runtime. The tested
application scatter matched the TC170C140-compatible field layout in
2,010 comparisons with zero mismatch.

# 14. Updated storage architecture

Backend separation is now central to the HDD model: the internal device
path and the target-indexed packet path are distinct implementations
that converge only at the common volume/block routing layer. Evidence
from one path must not be projected onto the other without a
demonstrated bridge.

The application contains two relevant storage-facing layers: a baseline
service context at 0x401000 driven through opaque 0x400xxx services, and
a separately enumerated packet-target path implemented in visible
application code. The latter contains explicit Iomega Zip qualification.

## 14.1 Baseline service context at 0x401000

  -------- ------ --------------------------------------------------
  Offset   Type   Contract
  00       u8     busy/completion
  01       u8     service input; precise meaning unresolved
  04       u16    cylinders-like
  06       u16    heads
  08       u16    sectors per track
  0A       u32    mode-0 extent; representation differs from +16
  12       u8     sector-buffer representation transform selector
  14       u8     baseline service variant selector
  16       u32    inclusive terminal block in its application mode
  1E       u16    software result/status
  78       u8     service flags
  -------- ------ --------------------------------------------------

+14 == 0 -\> extent +0A; pre-read service 40039C; completion service
400394

+14 == 1 -\> extent +16; no 40039C; completion service 400398

+14 other !=0 -\> extent +16; no 40039C; completion service 400394

The exact producer/meaning of +14 is unresolved. The Zip(ATAPI)
diagnostic itself reads +0A unconditionally, so +0A must not be
simplistically labeled non-ATAPI.

## 14.2 Packet-target enumeration and Zip qualification

INQUIRY-like identification:

vendor == \"IOMEGA \" or \"iomega \"

product prefix == \"ZIP\"

-\> classification\[target\] = 1

acceptance:

(device_category & 0x1F) == 0

&& classification\[target\] == 1

-\> acceptance_state\[target\] = 2

This is a demonstrated qualification restriction in the visible
target-indexed path. It is not established as a restriction on the
internal IDE device.

STRONGLY INFERRED: this target-indexed implementation is the external
SCSI-style storage path. Supporting evidence is the 0-7 target model,
controller-local-ID exclusion, per-target state, phase/message
completion behavior, SCSI command vocabulary, and separate
controller/DMA architecture. Direct physical-port identification remains
unresolved.

OBSERVED: the Iomega/ZIP gate, classification arrays and READ
CAPACITY/READ(10)/WRITE(10) machinery described below belong to this
target-indexed backend, not to the opaque internal 0x400xxx backend.

## 14.3 Zip-specific setup and persistent state

  ------------------- ------------------------------ ----------------------------------------------------
  CDB                 Direction/length               Observed role
  1A 00 2F 00 12 00   device -\> RAM, 18             Recognition-time query; response not retained
  15 10 00 00 1A 00   RAM -\> device, 26             Fixed recognition-time configuration payload
  06 00 02 00 16 00   device -\> RAM, 22             Persistent media-state query
  0C 00 00 00 00 00   no data                        Optional format preparation
  04 10 20 00 00 00   RAM -\> device, 4 zero bytes   Class-1 format preparation, then readiness polling
  ------------------- ------------------------------ ----------------------------------------------------

Only the 0x06 exchange exports persistent fields directly consumed
later: one low nibble must be zero for normal transfers, while another
low nibble must equal 2 for higher-level media revalidation.

## 14.4 Capacity and normal block I/O

Capacity CDB:

25 00 00 00 00 00 00 00 00 00

response\[0..3\] -\> cached extent / last block

response\[4..7\] -\> cached block length

normal read:

28 00 A3 A2 A1 A0 00 N1 N0 00

normal write:

2A 00 A3 A2 A1 A0 00 N1 N0 00

STRONGLY INFERRED: the capacity exchange is READ CAPACITY(10)-compatible
and returns a last logical block plus block length. The scanner requires
512-byte blocks. Normal block wrappers do not directly check the Zip
classification; they require transport present, nonzero cached capacity
fields, zero transfer-blocking state, and successful completion.

## 14.5 Mount path

enumerate target

-\> identify/qualify Zip

-\> attempt Zip setup/state query

-\> cache capacity

-\> require block length 512

-\> create logical-volume descriptor

-\> read absolute sector 0

-\> require byte 0 == FA and bytes 1FE..1FF == 55 AA

-\> read selected partition boot sector

-\> validate allocation-table copies

The device-format commands are not prerequisites for this ordinary
mount/read/write path.

# 15. A6 as the HDD-support control implementation

PROJECT FACT: Edirol A6 firmware runs on the same SP-808 hardware and
operates an IDE HDD. Therefore the central engineering problem is no
longer whether the hardware can support HDD operation, but which A6
software behaviors differ from the SP-808 and can be reproduced with the
smallest patch while preserving SP-808 functionality.

OBSERVED differential: A6 accepts and operates the internal ATA HDD
through its application-resident 0x600xxx backend while its ordinary
target-addressed scan still retains the Iomega/ZIP qualification gate.
This separates internal-HDD enablement from target-path ZIP-gate bypass.

same hardware

\|

+\-- SP-808 firmware -\> Zip-qualified storage behavior

\|

+\-- A6 firmware -\> HDD-capable behavior

Differential target:

device discovery / acceptance

-\> capacity and media-state setup

-\> logical-volume creation

-\> block I/O

-\> filesystem

The A6 reconstruction now shows that the principal HDD-enabling
divergence lies below the common logical-volume router: SP-808 delegates
the internal branch to 0x400xxx services, whereas A6 routes it to its
application-resident ATA driver. The target-addressed Iomega/ZIP path is
a separate backend and should be preserved unless independently
targeted.

# 16. Revised supersession and implementation notes

Supersede any description of production PRAM images as passive
configuration graphs; treat them as executable ESP programs with runtime
decoration.

Use the 10-bit SP-808 jump target in disassembly, while marking branch
condition/latency provenance.

Represent 34/B0 as an SP-808 experimental extension with uncertain
status side effect.

Do not label 0x401014 ATAPI/SCSI/LBA/device type without a producer or
direct discriminating evidence.

Do not equate 0x401016 with the visible packet-target READ CAPACITY
response; they belong to different demonstrated data paths unless a
bridge is proven.

Do not treat the historical two-byte Iomega/ZIP acceptance patch as an
internal-HDD patch. It modifies the target-indexed, strongly inferred
external SCSI-style backend; A6 demonstrates internal HDD operation
through the separate internal ATA backend.

For HDD enablement, prioritize SP-808/A6 differential storage analysis
over further ESP semantic work.

# Appendix C. Current patch-oriented checkpoints

  ------------------ --------------------------------------------------------- -----------------------------------------
  Checkpoint         SP-808 established behavior                               A6 comparison needed
  Identification     Explicit IOMEGA/ZIP qualification on packet-target path   What HDD identity/category is accepted?
  Acceptance state   classification 1 + category 0 -\> state 2                 How is usable HDD state represented?
  Media state        Persistent nibbles from 0x06 query                        Equivalent guard fields or bypass?
  Capacity           READ-CAPACITY-style last block + 512 block length         Same command/representation?
  Block I/O          READ(10)/WRITE(10)-compatible, 512-byte                   Shared/homologous routines?
  Baseline ABI       0x400xxx + 0x401000 context                               Same ABI and overrides?
  Filesystem         Sector-0 + partition/boot/allocation validation           Shared format/mount structures?
  ------------------ --------------------------------------------------------- -----------------------------------------

# 17. A6 differential: application-resident ATA backend

The A6 control case materially resolves the internal-storage
architecture. A6 retains the shared storage context and upper routing
model but implements ordinary internal HDD I/O in application code
through the SLA919F task-file-like interface.

  --------------------- --------------------------------------------------------------------- -----------------------------------------------------------------------------------
  Function / object     A6 observation                                                        Architectural implication
  0x10058C              Internal initialization; installs three handlers through 0x40020C     Application can attach storage transfer handlers to existing lower-layer services
  0x100A58              ATA EC IDENTIFY DEVICE; response at 0x5D0000; geometry -\> 0x401000   Application owns HDD identification/geometry
  0x100B2A / 0x100D2A   ATA 20/30 block read/write                                            Native ATA block backend resides in application
  0x600002-0x60001C     Task-file-like register accesses                                      Direct bridge from H8 application to SLA919F IDE/ATA interface
  0x401000              Shared context base                                                   Upper storage ABI is preserved across SP-808 and A6
  --------------------- --------------------------------------------------------------------- -----------------------------------------------------------------------------------

A6 transfer payload handling is not implemented as an obvious polling
loop on 0x600000. Instead, the driver initializes and updates transfer
descriptors, registers event/data handlers, and uses fixed
processor/hardware control locations. This is consistent with a
hardware/service-assisted transfer engine; the exact lower-layer
mechanism remains unresolved.

# 18. Differential splice point: SP-808 versus A6

SP-808 A6

105ED6 read router 107E16 read router

internal -\> 4003A8 internal -\> 100B2A

105FB2 write router 107EEA write router

internal -\> 4003AC internal -\> 100D2A

descriptor base 40F57A descriptor base 40F516

stride 24, route on low nibble stride 24, route on low nibble

The routing functions are strongly inferred homologues: their descriptor
arithmetic, branch structure, argument forwarding, and return handling
correspond after masking relocated addresses/call targets. This locates
the principal product divergence below the common logical-volume routing
layer.

SP-808 application: no identified direct accesses to 0x600000-0x60001C
and no matching A6 ATA-driver implementation signatures.

A6 application: direct reset/signature/IDENTIFY/address/read/write logic
against 0x600xxx plus registered transfer handlers.

Working model: SP-808 delegates internal-device operations to the opaque
0x400xxx boundary; A6 adds an application ATA backend while retaining
opaque services for registration, delay, buffer transformation, and
other lower-layer support.

# 19. ATA-driver dependency boundary

The recovered A6 closure is bounded enough to analyze as a
transplantable subsystem, but it is not address-independent. It includes
ATA-specific helpers, three registered handlers, a small set of
relocated/common helpers, private writable state, transfer descriptors,
and three opaque service interfaces.

  ------------------------- ------------------------------------------------------------------------------------------------------
  Dependency class          Current result
  Opaque services           40020C handler registration; 4002C8 delay; 40023C identification-buffer transform
  Relocated SP helpers      126290-\>12380A; 1262A2-\>12381C; 135818-\>1309CA; 13583C-\>1309EE; 16296C-\>157B6A; 163122-\>15833C
  A6 ATA globals            4033E6-4033ED plus transfer counters/status/end-block state
  Transfer descriptors      selected by words at 000450/000458; records at FF0000 + selected value
  Shared transfer control   FFFFF0DF and fixed processor/hardware control locations
  ------------------------- ------------------------------------------------------------------------------------------------------

SP-808 compatibility analysis has already established one hard
relocation requirement: 0x4033E6-0x4033ED is live SP numerical
operand/result state and cannot be reused by an address-identical A6
transplant. A safe SP RAM allocation must be established before patch
construction.

SP-808 also waits for bits 1/2 of 0xFFFFF0DF to clear before changing
its transfer environment, although no application-side producer of those
bits has yet been identified. This supports a shared asynchronous
transfer-control contract, but the producer and exact bit semantics
remain unresolved.

# 20. Current implementation model

Physical IDE bus

\|

SLA919F

\|

+\-- task-file-like H8 window 0x600xxx

\|

+\-- transfer/descriptor machinery (partly unresolved)

SP-808 application A6 application

\| \|

common volume/filesystem routing common volume/filesystem routing

\| \|

opaque internal backend application ATA backend

400380/4003A8/4003AC 10058C/100B2A/100D2A + handlers

\| \|

ATAPI Zip behavior observed ATA HDD behavior demonstrated

Patch-oriented interpretation: preserve the SP-808 upper
filesystem/application and the target-indexed, strongly inferred
external SCSI-style path (including its Iomega/ZIP qualification);
investigate replacing only the internal backend with a relocated
A6-derived ATA subsystem. The historical two-byte target-path ZIP-gate
patch is therefore not a demonstrated prerequisite for the internal-HDD
objective. This is not yet a patch specification. Descriptor
compatibility, handler registration, transfer-control ownership, safe
RAM, code placement, and initialization hooks must be established first.

# 21. Immediate unresolved checks

Identify all SP-808 reads/writes and producers for words 0x000450 and
0x000458 and resolve the descriptor bases where possible.

Reconstruct all SP-808 accesses to 0xFFFFF0DF, especially ownership of
bits 1/2.

Characterize SP-808 use of 0x4033E6-0x4033ED and choose no replacement
RAM until a safe region is demonstrated.

Validate the observable 0x40020C handler-registration convention from
SP-808 callers.

Only after those checks, design relocation of the A6 ATA-specific
routines and retarget calls to established SP helper homologues.

# 22. 4 October 2026 storage-transplant architecture

The A6 control implementation now defines a bounded application-side ATA
backend rather than merely an isolated read/write driver. Differential
analysis shows that A6 replaces a coherent family of SP internal-device
service calls while preserving the SP upper
volume/filesystem/application structure.

SP upper storage/application logic \| descriptor low nibble / \\ 0
internal !=0 target-indexed \| \| \| +\-- external SCSI-style path
retained \| +\-- A6-derived ATA backend 100578-101436 \| +\-- task file
600002..60001C +\-- descriptors FF0000 + word\[450/458\] +\-- fixed
transfer endpoint 600000 +\-- events 48 / A0 / B0 +\-- handlers
12641C-1266BC

## 22.1 Internal backend differential

  --------------------------------------- ---------------------------------------
  SP operation                            A6 application replacement
  400380 initialization                   10058C family / complete ATA envelope
  4003A8 read                             100B2A
  4003AC write                            100D2A
  400394/400398 matched internal action   1006F8(E0)
  40039C                                  1006F8(10)
  4003A0                                  100806
  4003B8                                  1008A2
  4003A4                                  100A58
  4003B4 init                             eliminated
  4003B4 periodic                         E5/status producer
  4003BC matched helper                   eliminated / RTS
  --------------------------------------- ---------------------------------------

OBSERVED exception: A6 retains 0x400398 in the ROM-to-disk terminal
operation when 0x401014 is nonzero. SP diagnostic callback 0x124888 also
remains an unresolved legacy Zip(ATAPI) completion action and is outside
the normal native-HDD path.

## 22.2 Preparation and format operation

100806 -\> command 91, geometry-derived field 1006F8 -\> command 10
1008A2 -\> 512-byte pattern + geometry traversal + command 50 100A58 -\>
command EC / IDENTIFY

OBSERVED: 0x1008A2 uses 0x5D0000 as a 512-byte scratch pattern, supplies
data through the output-transfer descriptor/channel, waits for interrupt
completion, and updates a progress object. STRONGLY INFERRED using ATA
domain context: commands 0x91 and 0x50 correspond to INITIALIZE DEVICE
PARAMETERS and FORMAT TRACK. This operation is destructive and should
not be part of initial read-only hardware validation.

OBSERVED: A6 progress routines 0x15F4FE and 0x15F600 have supported SP
homologues at 0x154CAE and 0x154D9A. The transplant can therefore keep
SP UI/progress state rather than copying the A6 UI subtree.

# 23. Transfer environment and event architecture

SP already exposes an application-visible transfer-environment switch at
0x12BE62. It waits for FFFFF0DF bits 1/2 to clear, disables opaque
controls 0x40034C/0x400350, selects mode through 0x400344, and for mode
0 invokes 0x400340 before re-enabling the controls. STRONGLY INFERRED:
this serializes a shared transfer environment; exact opaque meanings
remain unresolved.

A6 uses descriptor offsets from words 0x450 and 0x458. Descriptor
addresses are 0xFF0000 + unsigned offset. The first descriptor is
strongly inferred device-to-RAM and the second RAM-to-device, both using
fixed endpoint 0x600000. Selector 0x48 handles command/status events;
A0/B0 are paired transfer events using FFFFFFC0 bits 1/2 and
corresponding E/F channel registers.

SP registers adjacent selector 0x4C and uses FFFFFF2E/2F bit 3. A6
selector 0x48 uses bit 2. STRONGLY INFERRED: these are adjacent
interrupt/event sources. Absence of SP application registrations for
0x48/A0/B0 is not evidence that they are free; baseline/platform setup
remains the key unresolved prerequisite.

OBSERVED: FFFFFFC0 is shared by other SP mechanisms and must not be
modeled as an ATA-exclusive register.

# 24. Storage context corrections

The application-visible context at 0x401000 remains shared between SP
and A6. A6 provides producers that clarify several fields, but field
semantics must be stated at the level supported by the firmware.

  ------------- ---------------------------------------------------------------------------
  Offset        Current status
  +00           busy/active byte
  +01           driver initialized/enabled
  +02           A6 linear-versus-CHS selector
  +03           remaining transfer-block count
  +04/+06/+08   A6 geometry: cylinders / heads / sectors-per-track, strongly inferred
  +0A           A6 geometry-derived block count
  +0E           transfer-buffer pointer
  +12           sector-buffer transform selector
  +14           device-signature/protocol variant selector; A6 probe can write 0 or 1
  +16           SP retained terminal-block consumer field; no A6 app producer established
  +1E           software result/status
  +78           status/event flags
  ------------- ---------------------------------------------------------------------------

CORRECTION: A6 initialization initially clears +14, but probe 0x10126A
can subsequently write either 0 or 1. Therefore native initialization
does not justify forcing +14 to zero. The A6 ROM-copy terminal logic
must retain its +14 conditional.

# 25. Relocation architecture and Link Plan v2

17D000-17DEBE A6 100578-101436 complete ATA envelope 17DEBE-17E15E A6
12641C-1266BC handlers 17E15E-17E200 gap/alignment 17E200-17E2AE
SP-specific adapters

OBSERVED: payload size is 0x120C (4,620 bytes), spanning
0x17D000-0x17E2AE including the 0xA2 gap. The complete relocation
requires 64 absolute fixups: 18 copied-code references, 26 SP helper
substitutions, and 20 private-state references. All 207 decoded relative
branches/BSRs remain internal to their copied block and keep their
displacement.

## 25.1 Private RAM and callback-table prerequisite

A6 private state SP relocation 4033E6 status word -\> 4033AE 4033E8
counter A -\> 4033B0 4033E9 counter B -\> 4033B1 4033EA selected_end -\>
4033B2

0x4033AE-0x4033B5 is not naturally free RAM: it is the first two entries
of a callback pointer table. The conditional reclaim requires changing
the sole identified application consumer at 0x146DE2 to use the ROM
initializer at 0x17C802. The eight reclaimed bytes must then be
initialized explicitly.

0x4033E6-0x4033ED cannot be reused because SP uses it as live numerical
state. 0x43BF48-0x43FFF7 is not proven free. 0x5D0000 is an active
filesystem/cache buffer and remains only a provisional ATA scratch
allocation whose warm ownership is unresolved.

## 25.2 Adapter layer

  --------- ---------------------------- -------------------------------------------------
  Address   Purpose                      Status
  17E200    cold initialization          PROVISIONAL: cold quiescence required
  17E240    reinitialization             PROVISIONAL: warm transfer ownership unresolved
  17E258    E0 command adapter           required by differential
  17E260    10 command adapter           required by differential
  17E268    periodic E5/status adapter   required by differential
  17E29A    ROM-copy +14 conditional     required by differential
  --------- ---------------------------- -------------------------------------------------

The periodic adapter preserves SP admission gates and bit-0 consumers,
but replaces the old status acquisition. It clears 0x401078 bit 0,
issues E5 through relocated 0x1006F8, returns zero on command failure,
reads 0x600004, sets bit 0 when the byte is not 0xFF, and resumes at SP
0x105E6C. The old bit-3 dispatch is bypassed because the A6 homologue
has none.

# 26. Runtime safety boundary before patching

UNRESOLVED: whether timeout/warm recovery can begin while an old
transfer still owns 0x5D0000 or DMA/event state. Cache-tag invalidation
is not cancellation.

UNRESOLVED: who establishes descriptor words 0x450/0x458 and whether
selectors 0x48/0xA0/0xB0 are available to the transplanted A6
registration sequence under SP startup.

UNRESOLVED: coordination with existing SP users of shared 0xFFFFFFC0 and
related transfer-environment services.

UNRESOLVED: runtime validation of the proposed ROM padding placement and
the 0x0050 transfer configuration. The latter is required to preserve
A6-observed state but its independent hardware necessity is not yet
proven.

OUT OF SCOPE for initial HDD support: diagnostic 0x124888→0x400398. It
belongs to a Zip(ATAPI) diagnostic callback and is not established as
part of normal HDD operation.

Implementation status: the static functional differential for normal
native ATA-HDD operation is sufficiently bounded to freeze feature
scope. A patched image should not yet be produced as a safe release: the
remaining work is validation of runtime infrastructure and ownership,
followed by staged hardware testing beginning with cold initialization,
IDENTIFY, and controlled reads before any destructive format path.

## Development / Factory Interface: SCI1 and CN7

### Physical interface

The H8S/2653's SCI1 transmit signal `P31/TXD1` is routed to `TX1` on
CN7; CN7 also exposes `RX1` and `XRST`. On the examined production
SP-808 PCB, CN7 is not populated with a connector, but the pads have
witness marks consistent with pogo-pin contact.

**Architectural interpretation:** CN7 has observed physical-contact evidence and is hypothesized to have
served as a production/development contact interface. Its exact fixture
or peer remains unresolved.

### SCI1 software stack

Application routine `107A72` configures SCI1 with:

``` text
SMR1 = 00
BRR1 = 09
SCR1 = F0
```

At the documented 20 MHz operating clock, normal asynchronous SCI timing
gives 62,500 baud. `SCR1=F0` enables TX-empty interrupts, RX/error
interrupts, transmitter, and receiver.

The application installs three SCI1 handlers through service `40020C`:

    Selector    Handler Role
  ---------- ---------- -----------------------
       `150`   `107BCA` receive/error status
       `154`   `107BEE` RX byte → ring buffer
       `158`   `107C2E` queued TX

Buffers: - RX ring: `4102AA`, 512 bytes; indices `4104AA/4104AC`. - TX
ring: `40FAAA`, 2048 bytes; indices `4104AE/4104B0`.

### Proprietary request/reply grammar

The higher-level protocol is binary and transaction-oriented rather than
MIDI:

``` text
82 10 8E                         handshake-like transmit
9D 9E                            identification request
9D 05 ...                        required identification response prefix
99 <arg> 9E                      control transaction
92 <addr21> <length> 9E          read/request transaction
90 <addr21> <packed data> 9E     data/write transaction
95 ... 9E / 96 ... 9E            additional control transactions
```

The 21-bit argument is encoded in three seven-bit chunks,
least-significant first. Arbitrary 8-bit data is transported as
low-seven-bit bytes plus a trailing bitmap carrying original high bits.

The inspected read path makes the SP the requester: it sends `92`, then
waits for a `90` response. The code therefore does not by itself
establish a local memory-monitor server.

### Separation from MIDI

The normal MIDI implementation is independently recognizable through
channel-status dispatch, running status, realtime handling, `F0/F7`
SysEx, Roland manufacturer/device/model checks, and modulo-128 checksum
logic. SCI1 has a different baud rate and different grammar and does not
reuse those MIDI mechanisms.

**STRONGLY INFERRED:** SCI1/CN7 is a separate proprietary 62,500-baud
serial communications facility.

### Relationship to Status+FX C

Status+FX D has a visible application-side boot decision in `1258D8` and
enters application diagnostic code at `123994`.

No equivalent Status+FX C detector has been established in the visible
application image. In particular, no `62 + 53` button-query path has
been recovered.

Therefore:

-   **UNRESOLVED:** where Status+FX C is detected.
-   **UNRESOLVED:** whether C executes the SCI1 subsystem.
-   **UNRESOLVED:** whether Develop Monitor is flash-resident,
    mask-ROM-resident, or split between them.

The lack of readable monitor strings is not evidence for mask-ROM
residency.

A passive 62,500-baud capture from CN7 `TX1` during normal, C-mode, and
D-mode boots is a direct way to test the SCI1/C-mode relationship.
`82 10 8E` is a known static fingerprint for the recovered SCI1 client.

# Historical internal-ATAPI trace correlation (2026-10-04 update)

Historical real-hardware/emulator captures independently confirm that the stock internal storage path is an ATA PACKET / ATAPI implementation. Its observed command family includes `A1` IDENTIFY PACKET DEVICE and `A0` PACKET carrying `03`, `1B`, `12`, `5A`, `55`, device-specific `0D`, `23`, `25`, `1E`, `A8` READ(12), and `AA` WRITE(12). This must remain distinct from the target-indexed application's `1A/15/06/25/28/2A` command family.

The filesystem formatter has now been correlated to an old failed-format trace. `1058CC` constructs block 0 and partition records; `1064DE` creates the per-partition header, two allocation tables, a 32-block root directory, and data-area layout. For an observed/example geometry with partition start `0x20` and calculated table length 9, the layout is: header `0x20`; table #1 `0x21..0x29`; table #2 `0x2A..0x32`; root directory `0x33..0x52`; data from `0x53`. The nine-block count is calculated from partition length, not a fixed Zip-size discriminator.

A failure writing table #1 causes `1064DE` to skip table #2, root directory and partition header. The caller clears the failed partition record but still writes block 0. This exactly explains the historical `WRITE(12) 0x21 x9` failure followed by `WRITE(12) 0 x1`. Higher UI orchestration can discard the formatter result and later select `Completed.`, so a completion display does not prove successful formatting.

The exact old-emulator DRQ-phase incompatibility remains unresolved and low priority. It is a legacy ATAPI-emulation question, not a blocker for the A6 native ATA-HDD transplant.

# 27. H8S/2653 silicon contract for the A6 ATA transfer engine

**Manufacturer source used for this update:** Renesas, *H8S/2655 Group Hardware Manual*,
Rev. 5.00 (2006-09), applicable to HD6432653/H8S/2653. Relevant sections:
MCU operating modes and memory map (pp. 75-79), interrupt vector table
(pp. 104-107), DTC (pp. 309-339, especially pp. 311, 322-335), TPU
(pp. 427-509, especially pp. 434-435, 464, 498-499), and Appendix B
internal I/O registers (especially pp. 930-931).


## 27.1 DTC vector and register-information architecture

The HD6432653 contains a hardware Data Transfer Controller in addition to its
DMAC. DTC transfer descriptors ("register information" in Renesas terminology)
reside in on-chip RAM `FFF800-FFFBFF`. DTC enable registers occupy
`FFFF30-FFFF35`.

For interrupt activation, the manufacturer's DTC vector table fixes:

```text
IRQ2   vector 18 -> DTC vector 0424 -> DTCEA5
TGI1A  vector 40 -> DTC vector 0450 -> DTCEB1 (FFFF31 bit 1)
TGI2A  vector 44 -> DTC vector 0458 -> DTCEC7 (FFFF32 bit 7)
```

The two-byte vector entry supplies the lower address bits of the register
information in on-chip RAM. This directly explains A6's reads from `450/458`
and its `FF0000 + word` address formation.

Therefore `450/458` are **documented H8S DTC vector entries**, not a
Roland-specific pointer-table hypothesis.

## 27.2 TPU mapping

```text
FFFFC0  TSTR     bit1=CST1, bit2=CST2
FFFFE0  TCR1
FFFFE1  TMDR1
FFFFE2  TIOR1
FFFFE4  TIER1
FFFFE5  TSR1
FFFFE6  TCNT1
FFFFE8  TGR1A

FFFFF0  TCR2
FFFFF1  TMDR2
FFFFF2  TIOR2
FFFFF4  TIER2
FFFFF5  TSR2
FFFFF6  TCNT2
FFFFF8  TGR2A
```

TGI1A and TGI2A are the TGR1A/TGR2A compare-match/input-capture sources and
both can activate the DTC. Consequently the recovered A6 `450/458`,
`FFFF31/32`, `FFFFE*/FFFFF*`, and TSTR-bit-1/2 sequences form one coherent
manufacturer-defined TPU+DTC mechanism.

**STRONGLY INFERRED:** A6 ATA block data movement is timer-paced H8S DTC
between RAM and the SLA919F-side fixed endpoint `600000`; it is not ATA
bus-master DMA.

## 27.3 Shared transfer arbitration

A6 software sets `F0DF` bit 1/2 while the corresponding DTC transfer activation
is outstanding. SP `12BE62` and A6 `12F96E` wait for both bits to clear before
changing the shared transfer environment.

SP `129764` performs this wait before writing `TSTR=21`, which stops TPU1/2,
and restores TSTR before returning the environment to mode 0. This changes the
resource-conflict assessment: the SP timer takeover is explicitly guarded by
transfer quiescence.

The flags are segment/activation markers, not a demonstrated whole-command
mutex. Segment-boundary race behavior remains to be proved.

## 27.4 Realtime overload message is a higher layer

`Drive Too Busy.` (`17C1CE`) is selected by message entry 9 when
`427C8A` bit 6 is consumed at `146E50`. Five explicit producers set that latch.
Two compare remaining record margins against `00F0`. None of the identified
producers tests `F0DF[1:2]`.

Working architecture:

```text
realtime buffer/scheduling pressure
        -> Drive Too Busy latch
        -> storage request scheduling / pending masks
        -> 401000 / 40101E command state
        -> backend
        -> F0DF[1:2] transfer activations
        -> TPU1/2 + DTC
        -> 600000
```

## 27.5 Inherited `400xxx` platform layer

The visible SP application startup does not load the executable service bodies
at `400xxx`. It only installs four generated absolute jumps at
`400210`, `400214`, `400218`, and `400364`, then reaches its first observed
service call `400348`. A6 behaves equivalently.

Accordingly:

- `400xxx` is an **inherited DRAM-resident platform service layer** in the SP
  memory map.
- its implementation is absent from the supplied application firmware image;
- its provenance precedes the visible application entry;
- internal MCU ROM is one architecturally possible earlier source, not an
  established source.

The Renesas manual documents Mode 6 as advanced expanded mode with on-chip ROM
enabled; on H8S/2653 the on-chip ROM is 64 KiB at `000000-00FFFF`. This is
relevant to reset/bootstrap investigation but does not establish the SP mode
pins or prove that this ROM populates `400xxx`.

A runtime dump of `400000-400FFF` is now a high-value evidence acquisition
step because it can expose the actual inherited service bytes even before
their provenance is known.

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

