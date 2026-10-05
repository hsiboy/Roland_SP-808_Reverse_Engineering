# Roland SP-808 Hardware and Architecture Corrections --- October 2026

> **CURRENT CONSOLIDATED CORRECTION RECORD**
>
> This document supersedes the archived May 2026 hardware-corrections
> document. It separates manufacturer/documented facts, directly
> observed firmware or hardware evidence, inference, and unresolved
> questions.
>
> **Evidence labels**
>
> -   **OBSERVED** --- directly supported by firmware
>     bytes/instructions, schematic/service documentation, bus captures,
>     or physical hardware observation.
> -   **STRONGLY INFERRED** --- best explanation supported by multiple
>     independent observations.
> -   **HYPOTHESIZED** --- plausible interpretation requiring additional
>     verification.
> -   **UNRESOLVED** --- evidence is insufficient.
> -   **SUPERSEDED / CONTRADICTED** --- older project interpretation
>     should no longer be used.

**Date:** 4 October 2026\
**Scope:** SP-808 / SP-808EX hardware architecture, firmware mapping,
storage architecture, and relevant development-interface findings.

------------------------------------------------------------------------

## 1. Executive Summary

The following foundational hardware conclusions are retained:

-   **OBSERVED:** The SP-808 uses the Hitachi **HD6432653BA11F**, an
    H8S/2653-family MCU.
-   **OBSERVED:** The main-board CPU crystal X1 is **20.000 MHz**.
-   **OBSERVED:** The Sharp **LH28F800SUT** flash is an 8-Mbit device,
    i.e. **1 MiB** total capacity.
-   **OBSERVED:** The application flash image is mapped at runtime
    beginning at **0x100000**.
-   **OBSERVED:** The H8 application uses a 24-bit address space for the
    relevant external-memory map.
-   **OBSERVED:** The SP-808 contains physically distinct internal
    IDE/ATAPI and optional external SCSI hardware paths.
-   **OBSERVED:** The SLA919FF0J gate array has IDE control and
    DMA-related signals. The former claim that the design has "no DMA
    support / DDRQ and DDRACK not connected" is **CONTRADICTED** by the
    Roland schematic.
-   **CONTRADICTED:** The Iomega/ZIP recognition logic previously
    documented as a global "device validation flow" must not be applied
    to the internal IDE device. It belongs to the target-indexed
    external-style storage path.
-   **CONTRADICTED:** RAM word `0x4033E4` is not a ZIP/device-validation
    result variable.
-   **SUPERSEDED:** A6 HDD support no longer needs to be inferred from
    supposed device-type values. The A6 application contains a directly
    recovered ATA HDD driver.
-   **OBSERVED / STRONGLY INFERRED:** The application contains a
    separate H8 SCI1 proprietary serial interface exposed at the
    unpopulated CN7 footprint and configured for approximately **62,500
    baud**. Its relationship to Status+FX C Develop Monitor remains
    unresolved.

------------------------------------------------------------------------

## 2. MCU Identification

### 2.1 Device

**OBSERVED:** Roland's service documentation identifies main-board IC7
as:

`HD6432653BA11F`

This establishes the processor as the **Hitachi H8S/2653-family**
device. References in older project material to the H8S/2655 as the
installed MCU are **SUPERSEDED**.

The CPU core belongs to the H8S/2600 architecture.

### 2.2 Clock

**OBSERVED:** The Roland main-board schematic identifies crystal X1 as:

`20.000 MHz`

This is the documented SP-808 CPU clock source used in current
hardware/firmware correlation.

The same value independently produces the recovered SCI1 baud rate from
the actual SCI register programming; see §10.

### 2.3 Internal ROM and RAM

The H8S/2653 documentation describes on-chip ROM/RAM resources for the
relevant device variant.

These specifications should be described as **MCU/device
characteristics** rather than evidence that the internal ROM contents
have been recovered.

**OBSERVED:** The internal mask/OTP ROM contents are not available in
the current reverse-engineering corpus.

**Methodological rule:** do not equate the inherited `0x400xxx` service layer with internal ROM. Its provenance is unresolved. Application-visible service contracts are reconstructed from callers, shared state, register effects, and hardware behaviour. Internal-ROM extraction is not a prerequisite for the storage work.

------------------------------------------------------------------------

## 3. Flash Memory

### 3.1 Capacity

**OBSERVED:** Main-board flash is a Sharp `LH28F800SUT`.

The device capacity is:

-   8 Mbit
-   1 MiB total
-   commonly expressible as 1M × 8 or 512K × 16 depending on
    organization

The historical interpretation "8M = 8 MB" is **CONTRADICTED**.

### 3.2 Firmware image

The analysed SP-808EX firmware binary is approximately `0xC0004` bytes
including its container/header material, and therefore fits within the
1-MiB flash device.

Do not infer the electrical bus organization solely from firmware file
size.

------------------------------------------------------------------------

## 4. Application Runtime Mapping

### 4.1 Flash base

**OBSERVED:** The application firmware is coherently mapped at runtime
beginning at:

`0x100000`

This is no longer merely an IDA convenience or speculative relocation.

The mapping is supported by reset/vector analysis and by the extensive
coherent absolute code/data references recovered throughout the
application.

For the current firmware image, file-to-runtime mapping for application
contents follows the established firmware-container/header relationship;
individual calculations should continue to be checked against the actual
image layout.

### 4.2 Address-space interpretation

**OBSERVED:** The relevant H8S operating configuration uses 24-bit
addresses for the application-visible external map.

Therefore the working architectural address range is:

`0x000000–0xFFFFFF`

Do not describe the SP-808 application as using a flat 32-bit/4-GiB
physical address map merely because the CPU architecture contains 32-bit
registers or broader architectural capabilities.

### 4.3 Internal-ROM boundary

The low address region contains processor-internal resources including
unavailable ROM.

**UNRESOLVED:** The complete power-on execution sequence inside the
internal ROM.

This does not prevent reconstruction of the application-visible
`0x400xxx` service ABI.

------------------------------------------------------------------------

## 5. Startup RAM Initialization

Earlier project notes described the relocation of `0x17xxxx` data into
`0x40xxxx` RAM as unknown. That is **SUPERSEDED**.

**OBSERVED:** Application startup routine `0x12CC54` clears the
application RAM region and copies:

`0x17C454–0x17C880 → 0x403000–0x40342C`

Length:

`0x42D` bytes

The byte immediately after the destination, `0x40342D`, remains outside
that copied initialized-data range.

This mapping is important because apparent ROM and RAM addresses must
not be conflated without identifying the actual startup copy.

------------------------------------------------------------------------

## 6. Correction: `0x4033E4` Is Not Device Type / ZIP Validation State

The old interpretation of `0x4033E4` as a ZIP/device-validation result
is **CONTRADICTED**.

**OBSERVED:** Startup copies ROM bytes at `0x17C838–0x17C839` to RAM
`0x4033E4–0x4033E5`.

Those bytes are:

`2E E0`

which form word:

`0x2EE0 = 12000`

Adjacent RAM `0x4033E6–0x4033ED` is initialized from:

`3F F0 00 00 00 00 00 00`

which represents binary64 `1.0`.

**OBSERVED:** Later application arithmetic loads the word at `0x4033E4`,
adds 5, extends it, and divides by 10.

Consequently:

> `0x4033E4` belongs to numerical/application state and must not be used
> as evidence for ZIP recognition, device type, media type, or storage
> acceptance.

Any older documentation assigning storage semantics to this location is
superseded.

------------------------------------------------------------------------

## 7. SLA919FF0J Gate Array and IDE Hardware

### 7.1 Documentation status

The SLA919FF0J is a custom gate-array/ASIC used by the SP-808.

**UNRESOLVED:** No public programming datasheet has been established in
the project corpus.

This should be stated as "no public datasheet found," not "confirmed
private."

### 7.2 Schematic evidence

**OBSERVED:** The Roland main-board schematic exposes SLA919FF0J signals
including:

-   `IDECS`
-   `IDECS0`
-   `IDECS1`
-   `IDERD`
-   `IDEWR`
-   `IDE_A1`
-   `IDE_A2`
-   `IDE_A3`
-   `DMAR`
-   `DMAW`
-   `WAIT`
-   `INTO`
-   `RESET`

The internal 40-pin IDE connector carries standard ATA/ATAPI-related
signals including:

-   `DD00–DD15`
-   `DA0–DA2`
-   `CS0/CS1`
-   `DIOR`
-   `DIOW`
-   `DMARQ`
-   `DMACK`
-   `IORDY`
-   `INTRQ`
-   `RESET`
-   `IOCS16`
-   `PDIAG`
-   `DASP`

### 7.3 DMA correction

The old statement:

> "No DMA support (DDRQ, DDRACK not connected)"

is **CONTRADICTED** by the official schematic.

**OBSERVED:** Physical DMA-handshake and DMA-related resources exist in
the stock SP-808 hardware.

This does **not** by itself prove that a particular storage transaction
uses ATA bus-master DMA, nor that the A6 transfer engine maps one-to-one
onto a standard ATA DMA mode.

A distinction must be maintained between:

1.  physical DMA-capable signalling/resources;
2.  H8/gate-array memory-transfer channels;
3.  ATA protocol transfer mode.

------------------------------------------------------------------------

## 8. Internal IDE/ATAPI vs External SCSI Architecture

This is a major correction to the old "complete device validation flow."

### 8.1 Hardware separation

**OBSERVED:** Roland service documentation distinguishes:

-   an **internal IDE** Zip test; and
-   a separate **SCSI** test requiring the optional SP808-OP1 and an
    external SCSI Zip drive.

The optional SCSI board contains a dedicated NCR53CF92 SCSI controller.

Therefore the internal Zip and external target path are physically
distinct.

### 8.2 Internal physical IDE path

Bus captures of the stock internal drive show:

1.  IDE software reset assertion/release;
2.  signature reads including `14/EB`, the ATAPI packet signature;
3.  device select;
4.  `A1` IDENTIFY PACKET DEVICE;
5.  `EF` SET FEATURES attempts;
6.  `A0` PACKET commands;
7.  SCSI/ATAPI packet operations such as REQUEST SENSE, START/STOP,
    INQUIRY, MODE SENSE(10), MODE SELECT(10), and vendor commands.

**OBSERVED:** Stock internal Zip operation is therefore an
IDE/ATAPI-side path.

### 8.3 Target-indexed path

The visible target-indexed application backend uses:

-   target IDs;
-   per-target state;
-   SCSI-like command descriptor blocks;
-   INQUIRY;
-   MODE SENSE/SELECT;
-   READ CAPACITY;
-   READ(10)/WRITE(10);
-   controller registers around `0x800000–0x80000E`;
-   transfer hardware around `0x880000`.

The path recognizes Iomega/ZIP identity and has its own media-state
machinery.

**STRONGLY INFERRED:** This is the external SCSI-style backend
associated with the optional external storage architecture.

### 8.4 Historical validation-flow correction

The old documentation treated Iomega/ZIP recognition as a complete
global storage-device acceptance flow.

That interpretation is **CONTRADICTED**.

The Iomega/ZIP gate must not be projected onto the internal IDE/ATAPI
backend.

Consequently, bypassing the visible Iomega/ZIP target check is **not
established as an internal HDD-enablement patch**.

------------------------------------------------------------------------

## 9. Edirol A6 Control Case and HDD Support

Earlier documentation speculated that A6-specific device types such as
`0x07/0x08` represented HDD support. That inference is **SUPERSEDED** by
direct recovery of the A6 storage implementation.

### 9.1 Internal ATA driver

**OBSERVED:** A6 application firmware contains an application-side
internal ATA driver using hardware registers around:

`0x600000–0x60001C`

Recovered functionality includes:

-   reset/control sequencing;
-   signature probing;
-   handler registration;
-   `EC` IDENTIFY DEVICE;
-   IDENTIFY response processing;
-   cylinder/head/sector geometry;
-   a linear-addressing capability selector;
-   ATA read command `20`;
-   ATA write command `30`;
-   CHS addressing;
-   28-bit linear addressing;
-   sector-count and task-file programming;
-   asynchronous transfer handlers.

### 9.2 Routing

A6 retains the same upper storage-context/routing architecture used by
SP firmware but substitutes its application ATA backend for ordinary
internal filesystem I/O.

SP internal read/write paths call opaque services `0x4003A8/0x4003AC`.

A6 homologues instead call the recovered application ATA routines.

This is the central software differential relevant to HDD enablement.

### 9.3 Meaning for the project

> A6 HDD support is established by executable ATA-driver behaviour, not
> by inferred string or device-type values.

The existence of the A6 driver on hardware closely related to the SP-808
is the primary control case for the HDD transplant work.

------------------------------------------------------------------------

## 10. SCI1 / CN7 Proprietary Serial Interface

### 10.1 Physical connection

**OBSERVED:** The H8S/2653 pin `P31/TXD1` is routed as `TX1` to CN7. CN7
also exposes `RX1` and `XRST`.

**OBSERVED (physical unit):** CN7 is unpopulated on the examined
production PCB, but its pads show witness marks consistent with pogo-pin
contact.

**STRONGLY INFERRED:** CN7 was intended to be contacted by
production/development equipment.

### 10.2 SCI1 configuration

Application routine `0x107A72` programs SCI1:

``` text
SMR1 = 0x00
BRR1 = 0x09
SCR1 = 0xF0
```

`SCR1=F0` enables:

-   transmit-data-empty interrupt;
-   receive/error interrupt;
-   transmitter;
-   receiver.

It leaves multiprocessor and transmit-end interrupt enables clear.

Using the documented 20 MHz clock and the H8 normal asynchronous
formula:

``` text
baud = φ / [32 × 4^n × (BRR + 1)]
     = 20,000,000 / [32 × 1 × 10]
     = 62,500 baud
```

**STRONGLY INFERRED:** SCI1 operates at approximately **62,500 baud** in
this configuration.

### 10.3 Buffers and handlers

**OBSERVED:**

-   RX ring: `0x4102AA`, 512 bytes.
-   RX indices: `0x4104AA/0x4104AC`.
-   TX ring: `0x40FAAA`, 2048 bytes.
-   TX indices: `0x4104AE/0x4104B0`.

Handlers registered through `0x40020C`:

    Selector      Handler Behaviour
  ---------- ------------ ------------------------
     `0x150`   `0x107BCA` receive/error status
     `0x154`   `0x107BEE` receive byte into ring
     `0x158`   `0x107C2E` transmit queued byte

### 10.4 Wire grammar

Recovered transactions include:

``` text
82 10 8E
9D 9E
9D 05 ...        response
99 <arg> 9E
92 <addr21> <length> 9E
90 <addr21> <packed-data> 9E
95 ... 9E
96 ... 9E
```

The address-like argument is transmitted as three seven-bit chunks,
least-significant first:

``` text
arg & 0x7F
(arg >> 7) & 0x7F
(arg >> 14) & 0x7F
```

Arbitrary eight-bit data is encoded using low-seven-bit data bytes plus
a bitmap carrying the original high bits.

**OBSERVED:** In the inspected read path the SP sends a `92` request and
waits for a `90` response.

**STRONGLY INFERRED:** This is a proprietary request/reply protocol in
which the SP acts as a client/requester for the recovered
address-oriented operations.

### 10.5 Not ordinary MIDI

The normal MIDI implementation independently exhibits:

-   MIDI channel-status decoding;
-   running status;
-   realtime handling;
-   `F0/F7` SysEx;
-   Roland manufacturer byte `41`;
-   device/model checks;
-   modulo-128 checksum handling.

SCI1 instead has its own fixed-token grammar, `9E` termination, 21-bit
arguments, different arbitrary-byte encoding, and a 62.5-kbaud
configuration.

**STRONGLY INFERRED:** SCI1/CN7 is separate from the SP-808's ordinary
MIDI transport.

A MIDI-inspired historical design remains possible but is **UNRESOLVED**
and should not be treated as an architectural fact.

------------------------------------------------------------------------

## 11. Status+FX C Develop Monitor

Experimentally observed boot combinations include:

-   Status + FX C → Develop Monitor
-   Status + FX D → Diagnostic Mode

### 11.1 Diagnostic Mode

**OBSERVED:** The D-mode diagnostic decision is visible in application
startup.

`0x1258D8` uses button-query routine `0x1381BC`; the successful
diagnostic path calls `0x1463C6` and then application diagnostic entry
`0x123994`.

The application diagnostic implementation is therefore visible flash
code, although it uses opaque lower-level services.

### 11.2 Develop Monitor

**UNRESOLVED:** No equivalent C-mode detector has yet been located in
visible application code.

The contiguous logical button group suggests a possible C combination,
but the expected application-side test has not been recovered.

Possible architectures include:

1.  selection before the external application entry;
2.  selection inside an opaque startup service;
3.  a computed or otherwise unrecovered application path;
4.  a split design in which an early ROM component selects a replaceable
    flash implementation.

None is currently proven.

**Important correction:** absence of a readable `"Develop Monitor"`
ASCII string does not establish that the monitor resides in mask ROM.

### 11.3 Relationship to SCI1

**UNRESOLVED:** No connection between Status+FX C and the SCI1/CN7
protocol has been established.

The two investigations must remain separate until supported by
reachability evidence or hardware observation.

A useful low-risk experiment is passive capture of CN7 `TX1` during:

-   ordinary boot;
-   Status+FX C boot;
-   Status+FX D boot.

Decode at approximately 62,500 baud, 8N1. Static firmware predicts
`82 10 8E` as one recognizable SCI1 sequence.

------------------------------------------------------------------------

## 12. String-Address Differential Between SP-808 and A6

A historical `+0x5FDE` shift was observed for a class of
device-identification strings.

This remains useful as a **local correlation**, not as a global
relocation rule.

Examples from the current analysis include corresponding `SELF`, `ZIP`,
`HD`, `CD`, and `IOMEGA` strings in the two images with the same local
displacement.

**Rule:** never relocate arbitrary code/data between SP and A6 by adding
`0x5FDE`. Each correspondence requires independent structural
verification.

------------------------------------------------------------------------

## 13. Firmware Container / Update Format

The project contains evidence that Roland distributes firmware through
MIDI/SysEx-compatible update material and that the reconstructed binary
contains a header before the mapped application image.

However, exact historical claims about every header field and container
semantic should be retained only where independently verified from the
binary/update implementation.

**OBSERVED:** The current reverse engineering uses the established
application mapping at `0x100000`; the analysed binary includes
non-application header bytes before the mapped executable content.

**OBSERVED:** The application contains a MIDI SysEx firmware-update
receiver with explicit Roland manufacturer/model checking and checksum
handling.

Do not infer storage architecture from the update container format.

------------------------------------------------------------------------

## 14. Current Storage Architecture Summary

  -----------------------------------------------------------------------
  Layer                   SP-808                  Edirol A6
  ----------------------- ----------------------- -----------------------
  Main storage context    `0x401000`              `0x401000`

  Internal-device         opaque `0x400xxx`       recovered application
  implementation          services                ATA driver

  Internal hardware       lower layer / physical  `0x600000–0x60001C`
  register family         IDE-ATAPI observed      application-visible ATA

  Internal read           `0x4003A8`              application ATA read

  Internal write          `0x4003AC`              application ATA write

  Internal addressing     unavailable in opaque   CHS / 28-bit linear
                          layer                   

  External target         `0x800000–0x80000E`     same family
  controller                                      

  External transfer       `0x880000`              same family
  hardware                                        

  External protocol       target-indexed          target-indexed
                          SCSI-style              SCSI-style

  Ordinary external       Iomega/ZIP-oriented     Iomega/ZIP-oriented
  acceptance                                      

  HDD evidence            stock internal path     direct application ATA
                          remains                 HDD implementation
                          Zip/ATAPI-oriented      
  -----------------------------------------------------------------------

This separation is fundamental. Internal IDE/ATAPI observations and
external target-indexed SCSI-style logic must not be merged.

------------------------------------------------------------------------

## 15. Superseded Claims

The following historical claims must not be reintroduced as established
facts:

-   H8S/2655 is the installed SP-808 MCU.
-   8-Mbit flash means 8 MB.
-   `0x4033E4` is a ZIP/device-type/result variable.
-   the Iomega/ZIP target recognition gate is the global internal-drive
    whitelist.
-   bypassing that gate establishes internal HDD support.
-   the target-indexed backend and physical internal IDE/ATAPI backend
    are the same path.
-   the SLA919F/IDE hardware has no DMA-related signalling.
-   A6 HDD support is established by inferred device-type values
    `0x07/0x08`.
-   `0x17xxxx → 0x40xxxx` startup relocation is wholly unknown.
-   lack of readable Develop Monitor strings proves mask-ROM
    implementation.
-   SCI1/CN7 is ordinary MIDI.
-   SCI1/CN7 is already established as the Develop Monitor interface.
-   "no public SLA919F datasheet found" proves that no datasheet exists.

------------------------------------------------------------------------

## 16. Current Outstanding Questions

### Storage / A6 transplant

-   Can SP's runtime environment safely provide the descriptor state
    used through low RAM words `0x450/0x458`?
-   What owns selectors `0x48`, `0xA0`, and `0xB0` before a transplanted
    ATA driver registers them?
-   Are the corresponding transfer channels safe and compatible on stock
    SP hardware?
-   Can warm timeout recovery guarantee quiescence before reusing
    `0x5D0000` as ATA scratch?
-   What are the exact application-visible contracts of the remaining
    necessary opaque services?

### Develop Monitor / CN7

-   Where is Status+FX C detected?
-   Does C-mode execute the recovered SCI1 subsystem?
-   What is the peer at the other end of the CN7 proprietary protocol?
-   What does its 21-bit argument address?
-   What are commands `0x95`, `0x96`, and `0x99`?
-   What is the direction and role of `XRST`?
-   Is the monitor application-resident, internal-ROM-resident, or
    split?

### Inherited platform service layer

-   Exact implementations of the DRAM-resident `0x400xxx` service routines remain unavailable in the supplied application image.
-   Their provenance precedes the visible application entry and is unresolved.
-   A runtime DRAM dump can recover the resident bytes without first proving their source.
-   Internal MCU ROM remains a possible earlier bootstrap source, not an established source.

------------------------------------------------------------------------

## 17. Evidence Discipline

Future analysis should use this hierarchy:

1.  **Primary evidence:** firmware bytes and instructions, direct
    control flow, constants in context, strings in context, hardware
    experiments, official service documentation, applicable manufacturer
    manuals.
2.  **Derived technical evidence:** IDA boundaries/xrefs, reconstructed
    call graphs, structures, scripts, and differential maps, verified
    against primary evidence.
3.  **Existing semantic annotations:** hypotheses/navigation aids.
4.  **Historical project prose:** leads only.

For every important conclusion:

> **Evidence → domain context → hypothesis → attempted verification**

Existing function names, comments, older Markdown, and previous LLM
analysis must not be used as independent confirmation of a claim they
originally introduced.

------------------------------------------------------------------------

## 18. Current Bottom Line

The SP-808 hardware picture is now substantially clearer than in the May
2026 correction record.

The machine uses an H8S/2653 at 20 MHz, 1-MiB external flash mapped into
the application at `0x100000`, a custom SLA919FF0J gate array with real
IDE and DMA-related hardware signalling, an internal IDE/ATAPI Zip path,
and a physically separate optional external SCSI architecture.

The Edirol A6 control case establishes that closely related hardware can
run a full application-side ATA HDD driver while retaining the same
broad upper storage architecture. That executable differential---not the
historical ZIP string gate---is the relevant basis for the HDD
transplant.

Separately, the SP application contains a proprietary interrupt-driven
SCI1 protocol at approximately 62,500 baud, physically exposed on an
unpopulated CN7 footprint that shows pogo-contact evidence. It is
distinct from normal MIDI. Its peer and its relationship, if any, to
Status+FX C Develop Monitor remain unresolved.

Those boundaries should be preserved until new primary evidence moves
them.

## Addendum — historical ATAPI traces and format failure

Historical emulator/sniffer captures reinforce the corrected separation between the internal IDE/ATAPI path and the application-visible target-indexed backend. The internal path physically uses ATA PACKET with `5A/55/0D/23/A8/AA` among its operations; the target-indexed path uses the distinct `1A/15/06/25/28/2A` family.

A previously puzzling format experiment is now explained by application control flow. The formatter's first allocation table can occupy nine 512-byte blocks beginning at LBA `0x21`; if that write fails, later partition structures are skipped but block 0 is still written. Higher UI code can ignore the formatter's failure and display completion. Therefore the old sequence `WRITE(12) 0x21 x9 -> failure -> WRITE(12) 0 x1 -> apparent completion -> no usable space` is evidence of an incomplete format, not a successful format followed by a media-capacity rejection.

The exact emulator-side cause of that WRITE(12) failure remains unresolved and is not on the critical path for transplanting the A6 native ATA backend.

## 18. 5 October 2026 manufacturer-manual corrections

**Manufacturer source used for this update:** Renesas, *H8S/2655 Group Hardware Manual*,
Rev. 5.00 (2006-09), applicable to HD6432653/H8S/2653. Relevant sections:
MCU operating modes and memory map (pp. 75-79), interrupt vector table
(pp. 104-107), DTC (pp. 309-339, especially pp. 311, 322-335), TPU
(pp. 427-509, especially pp. 434-435, 464, 498-499), and Appendix B
internal I/O registers (especially pp. 930-931).


### 18.1 DTC and TPU resources are documented HD6432653 hardware

**CORRECTION / UPGRADE:** Low-memory words `0x450` and `0x458` are not merely
hypothesized Roland descriptor pointers. Renesas defines them as DTC vector
entries for TPU1 TGI1A (vector 40) and TPU2 TGI2A (vector 44).

The exact manufacturer mapping is:

```text
0450 -> TGI1A -> DTCERB bit1 -> FFFF31 bit1
0458 -> TGI2A -> DTCERC bit7 -> FFFF32 bit7
```

DTC register information resides in H8S on-chip RAM `FFF800-FFFBFF`.
The vector entries contain the lower address bits of those structures.

**CORRECTION / UPGRADE:** `FFFFC0` is TPU TSTR, with bits 1 and 2 controlling
TPU channels 1 and 2. `FFFFE8` is TGR1A and `FFFFF8` is TGR2A.
TGI1A/TGI2A are valid DTC activation sources. This manufacturer documentation
corroborates the recovered A6 timer-paced DTC ATA-transfer architecture.

**SUPERSEDED:** descriptions of the E/F register groups as unidentified custom
DMA channels, and descriptions of `450/458` as merely a possible
vector-associated table.

### 18.2 `F0DF` is software transfer state, not hardware DTC status

A6 instruction flow establishes bits 1/2 as software markers for outstanding
transfer activations. Both SP and A6 wait for these bits to clear before
changing the shared transfer environment.

SP routine `129764` performs that wait before stopping TPU1/2 via TSTR.
Therefore the previously identified timer conflict is guarded by a visible
quiescence protocol. The flags are not yet proved to be a whole-command mutex;
segment-boundary race analysis remains open.

### 18.3 `Drive Too Busy.` is not the `F0DF` failure path

The message is driven by `427C8A` bit 6 and has multiple application-level
producers involving buffer state, scheduling state, event state, and two
`<=00F0` remaining-margin checks. No identified producer tests `F0DF` bits
1/2. Treat the message as higher-level realtime storage-pressure evidence,
not as a DTC-arbitration timeout.

### 18.4 Correct description of `400xxx`

**SUPERSEDED:** wording that equates the `400xxx` service implementation with
internal MCU ROM.

**CURRENT:** `400xxx` is an inherited DRAM-resident platform service layer.
The supplied application image does not contain its resident implementation at
those addresses and the visible startup does not populate the service bodies.
SP startup installs four generated jump veneers at `400210`, `400214`,
`400218`, and `400364`, then calls pre-existing service entry `400348`.
A6 has the same inherited-environment pattern.

The source of that DRAM service layer is unresolved.

### 18.5 MCU ROM nuance

The manufacturer manual states that **Mode 6** is advanced expanded mode with
on-chip ROM enabled. For H8S/2653, 64 KiB of on-chip ROM occupies
`000000-00FFFF` in that mode; external addressing remains available.

This is an MCU architectural fact, not proof that the SP-808 is strapped to
Mode 6 or that this ROM populates `400xxx`. It does, however, invalidate any
reasoning that treats "external DRAM at 400000" as excluding an earlier
on-chip-ROM bootstrap.

### 18.6 Updated storage-transplant blockers

Remove these from the unresolved list as architectural mysteries:

- meaning of `450/458`;
- identity of `FFFF31 bit1` and `FFFF32 bit7`;
- identity of `FFFFC0`, `FFFFE8`, and `FFFFF8`;
- whether TGI1A/TGI2A can activate the DTC.

Retain as unresolved:

- exact segment-boundary safety of the `F0DF[1:2]` quiescence protocol;
- how A6 initializes the DTC register-information structures referenced by the pre-existing programmed `0450/0458` words, and what must be reproduced by a transplant;
- handler-routing initialization;
- provenance and implementation of inherited `400xxx` services;
- warm `5D0000` ownership/recovery safety.

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

