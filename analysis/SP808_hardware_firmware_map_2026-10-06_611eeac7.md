# SP-808 hardware ↔ firmware map

**OBSERVED:** Hardware blocks are read from [the block diagram](../media/sp808-block_diagram.png). Stock SP firmware MD5: d744a9cd4a2790ac68d165fd7849b5d8. All addresses are hexadecimal runtime addresses; BIN offset = runtime − 100000. A6 and v3 references are named explicitly.

**OBSERVED:** Examples were checked using read-only IDA on the matching SP database. The companion JSON includes returned disassembly excerpts and input hashes. Existing semantic names remain navigation aids. This is an interface map, not an exhaustive instruction/address-form census. Empty xrefs do not prove absence.

**STRONGLY INFERRED:** The hardware maps to several firmware layers: H8 control code, executable ESP processing records, inherited DRAM services and device interfaces. Locating a high-level caller does not recover its low-level service implementation.

| Diagram block | Firmware anchors | Interface | Mapping status |
|---|---|---|---|
| CPU — IC7 HD6432653 | 100000 → 12CC54: application entry and startup<br>12CCC4: installs four DRAM JMP veneers<br>100A8C / 100AB0: TPU0 timing setup<br>105420: stock storage-init shell | TPU0: TCR0/TMDR0/TIOR0H/L/TIER0/TSR0/TCNT0/TGR0A–D at FFFFD0–FFFFDE<br>TSTR FFFFC0; TSYR FFFFC1 | OBSERVED |
| Application flash — IC9 LH28F800SUT | Stock SP ROM image: 100000–1C0003 in the corpus<br>100000 contains JMP 12CC54<br>V3 copied code/glue: 17D000–17E297 | Runtime address = BIN offset + 100000 | OBSERVED |
| CPU DRAM — IC8 TMS418169A | 12CC54: application RAM clear and initializer copy<br>12CCC4: writes 400210/214/218/364 JMP veneers | 403000–42BFFF: documented startup-clear interval<br>401000: shared storage context; 5D0000: active storage buffer<br>4104C2 / 4110C2: ESP PRAM shadows<br>400000–400FFF: inherited executable service layer | STRONGLY INFERRED |
| I/F gate array — IC13 SLA919FF0J | SP internal init 105420 → 400380<br>SP internal read 105ED6 → 4003A8; write 105FB2 → 4003AC<br>A6 10058C / 100A58 / 100B2A: native ATA init/IDENTIFY/read | A6 task-file-like window 600002–60001C; data endpoint 600000 | STRONGLY INFERRED |
| Internal Zip drive | 105420 / 105ED6 / 105FB2: init/read/write routes<br>1058CC / 1064DE: filesystem-format callers (not low-level ATA drivers) | 400380 / 4003A8 / 4003AC: opaque DRAM service entry addresses, not hardware registers<br>401000 context; 5D0000 buffer | STRONGLY INFERRED |
| LCD unit | 138560: eight-byte UI command interpreter<br>138DBA / 13904E: coordinate/extent consumers<br>138534: brackets 40046C with 400450 calls | Caller-visible drawing/service family 40043C / 400450 / 40045C / 400460 / 400468 / 40046C<br>42757A–42757F: geometry state | STRONGLY INFERRED |
| Panel and switch boards — switches / LEDs | 137FAA / 1381BC: logical-button lookup/query<br>1258D8: diagnostic boot decision queries button codes through 1381BC | 1756D8: 80-entry two-byte mapping table (documented)<br>400494: group query; 1381BC tests a returned matrix bit | STRONGLY INFERRED |
| Panel faders | No exact acquisition/calibration routine established | Candidate H8 A/D interface: ADDRA/B/C/D FFFF90/92/94/96; ADCSR FFFF98; ADCR FFFF99 | HYPOTHESIZED |
| Beam board / D-Beam | 12EAF0: selects two calibration curve rows<br>12E626: consumes selected curve and processed input byte<br>12EDCC: calibration callback | 1589D2–1599D1: sixteen 256-byte curves<br>426D50 / 426D54: selected row pointers | STRONGLY INFERRED |
| Pedal input | No exact reader/debounce/event path established | No established register mapping | UNRESOLVED |
| MIDI board | 13C5C0: SCI0 forwarding/chained handler<br>1761BE: documented MIDI identity response bytes | SCI0: SMR0/BRR0/SCR0/TDR0/SSR0/RDR0/SCMR0 at FFFF78–FFFF7E<br>427758: saved handler successor used by 13C5C0 | STRONGLY INFERRED |
| DSP — IC11 TC170C140AF (ESP) | 108A7E: host PRAM word writer<br>1097F6 family: ROM-record loader; 1099A6: selected read<br>108C12 / 108D06: packed record/parameter updates<br>101D16 → 10C816 → 108C12: coefficient-to-hardware chain<br>12D228 / 12D264 / 12D2DC: diagnostics | PRAM0 C00000; PRAM1 C01000; controls C02000–C02005<br>C00003 bit 7 readiness; shadows 4104C2 / 4110C2<br>Type-1 ROM image 15E470–15E754; PRAM1 starts at index 03C | STRONGLY INFERRED |
| DSP DRAM — IC12 LH62800K | 12D398–12D736: documented ERAM setup/functional checks<br>1097BE / 108D06: 18-bit Q fields in ESP records | ERAM exercised indirectly through ESP programs; no direct H8 base assigned | HYPOTHESIZED |
| Clock generator — IC19 TC9246F | No exact IC19 programming routine established<br>100A8C / 100AB0 are confirmed TPU0 programming, not an identified IC19 driver | No established register mapping | UNRESOLVED |
| Main-board A/D–D/A — IC23 / IC24 AK4520 | ESP coefficient/effect code maps to processing, not an identified AK4520 control driver | No established register mapping | UNRESOLVED |
| Analog input VR, output mute and phones selection | No exact IC35 mute or IC33/IC35 selection routine established | No established register mapping | UNRESOLVED |
| Option-board SCSI — IC4 NCR53CF92 | 12Axxx / 12Bxxx: target-indexed command backend<br>12A934: registers IRQ3 selector 4C → 123864<br>123864: controller ISR; 12B2F6 / 12B496: routed block operations<br>12A956 / 12AA14: probe/ZIP classification gate | 800000–80000E: controller register window<br>880000: documented external transfer endpoint<br>IER/ISR bit 3; 426BF8 and subsequent transfer state | STRONGLY INFERRED |
| Option-board digital I/O and extra D/A | No exact per-chip driver established | No established register mapping | UNRESOLVED |

## Evidence and boundaries by block

### CPU — IC7 HD6432653

**OBSERVED:** The diagram identifies IC7 as the H8S CPU. All listed routines execute H8 instructions; 100AB0 programs TPU0 and starts TSTR bit 0.

**OBSERVED — mapping:** 100000 → 12CC54: application entry and startup; 12CCC4: installs four DRAM JMP veneers; 100A8C / 100AB0: TPU0 timing setup; 105420: stock storage-init shell.

**UNRESOLVED:** TPU0's downstream physical role is not established. Do not equate it with clock-generator IC19 or infer a sample-rate selection from timing constants.

Evidence: Technical Reference §3; Evidence Ledger §19.3; Fresh IDA: Timing config.

### Application flash — IC9 LH28F800SUT

**OBSERVED:** The diagram shows CPU-bus flash. The checked BIN holds H8 code, tables, strings and ESP records; its first instruction jumps to startup.

**OBSERVED — mapping:** Stock SP ROM image: 100000–1C0003 in the corpus; 100000 contains JMP 12CC54; V3 copied code/glue: 17D000–17E297.

**UNRESOLVED:** The complete updater/flash-programming implementation is not established here. The first 32 bytes include executable entry code and metadata; do not subtract 0x20 from mapped firmware addresses.

Evidence: Technical Reference §3 and address map; Link Plan v3; Firmware hashes.

### CPU DRAM — IC8 TMS418169A

**OBSERVED:** Firmware accesses and executes external DRAM addresses; diagram IC8 is connected to the CPU bus.

**STRONGLY INFERRED — mapping:** 12CC54: application RAM clear and initializer copy; 12CCC4: writes 400210/214/218/364 JMP veneers.

**UNRESOLVED:** Exact chip-select geometry/aliasing is not proven. The source that populates inherited 400xxx executable services is unresolved; it is not part of the supplied SP application BIN.

Evidence: Evidence Ledger §§32.1,38 and final programmed-vector clarification; Technical Reference §27.5.

### I/F gate array — IC13 SLA919FF0J

**OBSERVED:** Diagram connects the gate array to Zip, LCD, switch/LED and audio-related paths. SP callers use opaque services; A6 accesses the ATA-like window directly.

**STRONGLY INFERRED — mapping:** SP internal init 105420 → 400380; SP internal read 105ED6 → 4003A8; write 105FB2 → 4003AC; A6 10058C / 100A58 / 100B2A: native ATA init/IDENTIFY/read.

**UNRESOLVED:** Only the storage-side interface has a concrete application mapping here. The gate array's LCD, panel and audio subinterfaces are not assigned undocumented register meanings.

Evidence: Hardware Corrections §§7–9; Technical Reference §§17–19; Internal IDE bus capture.

### Internal Zip drive

**OBSERVED:** Physical internal-bus traces contain A1 IDENTIFY PACKET, A0 PACKET, A8 READ(12), AA WRITE(12). Application read/write call chains correlate with the internal backend.

**STRONGLY INFERRED — mapping:** 105420 / 105ED6 / 105FB2: init/read/write routes; 1058CC / 1064DE: filesystem-format callers (not low-level ATA drivers).

**UNRESOLVED:** Stock packet construction and transfer-engine code inside 400xxx remain unavailable. Do not assign the external IOMEGA/ZIP gate at 12AA14 to this drive path.

Evidence: Evidence Ledger historical ATAPI trace/formatter addendum; Technical Reference §18; Hardware Corrections §8.

### LCD unit

**OBSERVED:** UI records pass byte-sized geometry to drawing-like service calls. Diagram routes LCD through the gate array.

**STRONGLY INFERRED — mapping:** 138560: eight-byte UI command interpreter; 138DBA / 13904E: coordinate/extent consumers; 138534: brackets 40046C with 400450 calls.

**UNRESOLVED:** Exact primitive names, LCD bus/register addresses, screen-coordinate conventions and controller protocol are unproven. High-level UI mapping does not identify low-level LCD writes.

Evidence: Evidence Ledger §4.2; findings §10 (lead corroborated by fresh IDA); Fresh IDA: UI primitive caller; UI geometry.

### Panel and switch boards — switches / LEDs

**OBSERVED:** 1381BC derives a group and bit from the lookup result, calls 400494, masks that bit and returns Boolean. Diagram switches/LEDs connect to the gate array.

**STRONGLY INFERRED — mapping:** 137FAA / 1381BC: logical-button lookup/query; 1258D8: diagnostic boot decision queries button codes through 1381BC.

**UNRESOLVED:** Individual physical-button labels, scan-register implementation and LED write paths have not been established by this map. Do not assume drawing functions scan inputs.

Evidence: Evidence Ledger Develop Monitor / Boot-mode dispatch; Fresh IDA: Panel button query.

### Panel faders

**OBSERVED:** The diagram draws the fader connection directly to the CPU.

**HYPOTHESIZED — mapping:** No exact acquisition/calibration routine established.

**UNRESOLVED:** H8 ADC acquisition is plausible, but no fader-channel assignment or firmware acquisition path was recovered. Empty fixed-address IDA xrefs do not establish absence; loaded-pointer and inherited-service paths remain possible.

Evidence: Block diagram; IDA/H8.cfg register names only (not semantic proof).

### Beam board / D-Beam

**OBSERVED:** 12EAF0 multiplies two byte indices by 256, adds 1589D2 and stores two pointers. The documented callback records connect calibration to D BEAM SETUP / Auto Setup Sens?. Diagram links beam board to CPU.

**STRONGLY INFERRED — mapping:** 12EAF0: selects two calibration curve rows; 12E626: consumes selected curve and processed input byte; 12EDCC: calibration callback.

**UNRESOLVED:** Physical input acquisition pins, ADC/timer assignment and IR emitter/detector control are not established. These are processed calibration curves, not DSP program records.

Evidence: Evidence Ledger §19.1–19.2; Fresh IDA: D-Beam mapping.

### Pedal input

**OBSERVED:** Diagram shows the pedal signal entering the CPU.

**UNRESOLVED — mapping:** No exact reader/debounce/event path established.

**UNRESOLVED:** CPU port, electrical interpretation, debounce and application action mapping are untraced. A direct CPU wire does not establish an ADC input.

Evidence: Block diagram.

### MIDI board

**OBSERVED:** Fresh 13C5C0 instructions read RDR0, poll SSR0 bit 7, write TDR0, clear SSR0 bit 7 and RTS through a saved successor. Independent firmware protocol evidence includes MIDI status, running status and SysEx parsing.

**STRONGLY INFERRED — mapping:** 13C5C0: SCI0 forwarding/chained handler; 1761BE: documented MIDI identity response bytes.

**UNRESOLVED:** Complete MIDI parser/ISR ownership remains incomplete. 13C5C0 is a forwarding/chaining hook, not evidence that this one routine implements all MIDI. SCI1/CN7 is a separate interface.

Evidence: Evidence Ledger SCI1 is distinct from MIDI; Handoff handler/result-flow audit; Fresh IDA: SCI0 handler.

### DSP — IC11 TC170C140AF (ESP)

**OBSERVED:** 108A7E computes C00000/C01000 plus masked selector offset and writes the supplied longword; it maintains corresponding RAM shadows. Firmware diagnoses DEVICE(ESP). Diagram labels IC11 TC170C140AF. Later production corpus reconstruction finds 25 type images and 8,381 records.

**STRONGLY INFERRED — mapping:** 108A7E: host PRAM word writer; 1097F6 family: ROM-record loader; 1099A6: selected read; 108C12 / 108D06: packed record/parameter updates; 101D16 → 10C816 → 108C12: coefficient-to-hardware chain; 12D228 / 12D264 / 12D2DC: diagnostics.

**UNRESOLVED:** Register-to-IC11 correspondence is strongly supported, not individually traced on the bus here. Complete opcode timing, opcode 50 and 34/B0 details remain unresolved. Apply the later executable-ESP interpretation over older descriptor-only prose.

Evidence: Technical Reference §§4,13 and Appendix A; Evidence Ledger ESP diagnostics/production updates; Fresh IDA: PRAM writer; Block diagram.

### DSP DRAM — IC12 LH62800K

**OBSERVED:** The diagram connects IC12 to the DSP rather than directly to the CPU bus. Firmware has distinct indirect ERAM tests and address-field updates.

**HYPOTHESIZED — mapping:** 12D398–12D736: documented ERAM setup/functional checks; 1097BE / 108D06: 18-bit Q fields in ESP records.

**UNRESOLVED:** ERAM-to-IC12 physical correspondence is plausible but unproven. Do not equate IC12 with the main CPU DRAM or assert which audio/sample buffers reside here.

Evidence: Technical Reference §§8,13.6; Block diagram.

### Clock generator — IC19 TC9246F

**OBSERVED:** Diagram connects the CPU-side control path to the clock generator and its output toward audio hardware.

**UNRESOLVED — mapping:** No exact IC19 programming routine established; 100A8C / 100AB0 are confirmed TPU0 programming, not an identified IC19 driver.

**UNRESOLVED:** Control pins/protocol and sample-clock selection are untraced. Values 850/880/870/860 at 1599D2 are timer parameters; their association with this chip or audio rates is not established.

Evidence: Block diagram; Evidence Ledger §19.3; Fresh IDA: Timing config.

### Main-board A/D–D/A — IC23 / IC24 AK4520

**OBSERVED:** Diagram places two AK4520 converters on the audio path, with digital connections toward the gate-array/DSP side.

**UNRESOLVED — mapping:** ESP coefficient/effect code maps to processing, not an identified AK4520 control driver.

**UNRESOLVED:** Codec initialization, serial control, digital routing and converter-specific H8 writes have not been mapped. H8 ADDRA/ADCSR are MCU peripherals, not these audio codecs.

Evidence: Block diagram; Technical Reference ESP architecture.

### Analog input VR, output mute and phones selection

**OBSERVED:** Diagram shows input VR controls, MUTE IC35 4053 and SEL IC33/IC35 4053 paths to master, aux and phones outputs.

**UNRESOLVED — mapping:** No exact IC35 mute or IC33/IC35 selection routine established.

**UNRESOLVED:** Analog potentiometer paths do not imply H8-readable controls. CPU/ASIC control wiring, mute polarity and output-selection firmware require schematic/control-flow tracing.

Evidence: Block diagram.

### Option-board SCSI — IC4 NCR53CF92

**OBSERVED:** 123864 clears ISR/IER bit 3 and reads/writes 800002–800006, advances buffer state and calls transfer helpers. Target-indexed firmware uses SCSI-style CDBs. Diagram puts an NCR53CF92 and separate Zip device on SP808-OP1.

**STRONGLY INFERRED — mapping:** 12Axxx / 12Bxxx: target-indexed command backend; 12A934: registers IRQ3 selector 4C → 123864; 123864: controller ISR; 12B2F6 / 12B496: routed block operations; 12A956 / 12AA14: probe/ZIP classification gate.

**UNRESOLVED:** Exact register-to-chip bus decode and full 880000 transfer-hardware implementation are not newly proven here. The option-board Zip label is separate from the main-board internal Zip path.

Evidence: Evidence Ledger §§9,32.3; Technical Reference §§14.2–14.5; Fresh IDA: SCSI ISR; Block diagram.

### Option-board digital I/O and extra D/A

**OBSERVED:** Diagram labels D.OUT I/F IC2 TC9271F, D.IN I/F IC3 LC8905V and D/A IC7/8/9 AK4324, with digital paths into the main board.

**UNRESOLVED — mapping:** No exact per-chip driver established.

**UNRESOLVED:** Option detection, digital lock/status, clock-source selection and individual channel routing/control paths are not assigned routines. Do not map the SCSI driver to all option-board hardware merely because it shares a board.

Evidence: Block diagram.

## What the v3 experiment occupies

**OBSERVED:** V3 adds A6 ATA routines at 17D000 onward and configures IRQ2 plus TPU1/TPU2 → DTC descriptors → 600000. SP 105476/10547A already write TGR1A/TGR2A; v3 changes the shell immediate from 0018 to 0050. These are CPU-internal transfer resources; the data endpoint belongs to the external storage interface. V3 does not reroute ordinary filesystem I/O.

**UNRESOLVED:** A successful cold-init/read test would establish that bounded storage path; it would not establish panel, DSP, audio routing or normal SP functionality after transplant.

## Mapping boundaries

- **OBSERVED:** CPU DRAM and DSP DRAM are separate diagram blocks. ESP PRAM is not a general CPU sample-memory map.
- **OBSERVED:** 400xxx denotes executable DRAM services, not MMIO registers or proven internal-ROM services.
- **STRONGLY INFERRED:** SCI0 corresponds to MIDI; SCI1/CN7 is a separate proprietary interface not drawn as the MIDI board.
- **OBSERVED:** Main-board internal Zip and option-board SCSI Zip are separate physical paths.
- **UNRESOLVED:** TPU0 timing constants do not identify an IC19/sample-rate driver; H8 ADC names do not identify AK4520 control code.

## Source navigation

- [SP-808EX_Evidence_Ledger_2026-10-05_v11.md](../SP-808EX_Evidence_Ledger_2026-10-05_v11.md)
- [SP-808EX_Observed_Architecture_Technical_Reference_2026-10-05_v9.md](../SP-808EX_Observed_Architecture_Technical_Reference_2026-10-05_v9.md)
- [Roland_SP-808_Hardware_Architecture_Corrections_2026-10-05_v4.md](../Roland_SP-808_Hardware_Architecture_Corrections_2026-10-05_v4.md)
- [analysis/CODEX_HANDOFF_2026-10-05.md](../analysis/CODEX_HANDOFF_2026-10-05.md)
- [analysis/findings.md](../analysis/findings.md)
- [analysis/Link_Plan_v3_2026-10-05.md](../analysis/Link_Plan_v3_2026-10-05.md)
- [IDA/H8.cfg](../IDA/H8.cfg)
- [protocols/Roland_SP-808_to_ZIP_Drive_sniff.md](../protocols/Roland_SP-808_to_ZIP_Drive_sniff.md)

Sources include historical passages and later corrections. Use Technical Reference §13 for executable ESP records and the final programmed-vector clarification for 450/458. Earlier uncertainty on those points is superseded. Diagram wiring alone does not establish bus decode.
