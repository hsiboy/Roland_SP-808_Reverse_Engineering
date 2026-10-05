# SP-808 entry-state snapshot design - 2026-10-05

**UNRESOLVED / NO-GO for application:** No unused DRAM destination has been established. This document supplies an exact conditional implementation, not a verified non-destructive patch. `43C000` is an explicitly UNPROVEN example address. No firmware binary or IDA database was changed. No output/exfiltration mechanism is included.

## Evidence and choice of hook

**OBSERVED:** Stock `firmware/SP8EXall.bin` is 0xC0004 bytes, MD5 `d744a9cd4a2790ac68d165fd7849b5d8`. Runtime address equals file offset + 100000. Bytes at 100000 are `5A 12 CC 54`, an absolute jump to application entry. IDA xrefs to 12CC54 were empty; the raw header jump is the primary entry evidence.

**OBSERVED:** At 12CC54 the first instruction is `01 20 6D F0` / `STM.L ER0-ER2,@-ER7`. At 12CC58 follows the ER3 push. The visible startup clears 403000-42BFFF, initializes 403000 from ROM, installs four service veneers, then calls 1258D8. Its first identified inherited-service call is 1258EC -> 400348. These instructions were read through IDA and checked against the image bytes; no 400xxx body was examined.

**STRONGLY INFERRED:** Hook 12CC54 best preserves the inherited state: before application stack saves, application RAM clearing, peripheral initialization, and application storage initialization. It is an application-entry snapshot, not a post-storage-init runtime snapshot. It does not establish the later scheduler/interrupt settings.

**STRONGLY INFERRED, conditional:** Replace exactly that first four-byte instruction with an absolute JMP to the stub. Restore registers and flags, execute the displaced STM.L, JMP 12CC58. This introduces no extra call frame, stack allocation, or stack write during capture. ER7 is the exact application-entry value; the inherited stack contents are copied before the displaced application push. The continuation receives the same registers/flags/stack layout as stock, except for elapsed time and independently progressing hardware.

**OBSERVED:** 1B0000-1B011F is all zero in this exact image, lies in the long padding run after active content, and is before the trailer. This is the proposed code placement. **UNRESOLVED:** Inherited loader/checksum acceptance and execution of this padding address on hardware have not been validated. Zero bytes prove padding content, not every boot-layer contract.

## Destination investigation

**OBSERVED:** The latest ledger section 32.4 explicitly rejects 43BF48-43FFF7 as proven-free RAM. 43BF48 is an application-BSS exclusive-end value in the startup/linker data at 12CD6C; stack, computed accesses and inherited workspace remain unresolved. No direct xref to 43BF48 was returned by IDA. No literal 43C000 occurrence was found in either three-byte or four-byte pattern scans of SP. These negative searches do NOT establish vacancy; they do not cover register-derived addressing or opaque services.

**OBSERVED:** The latest documents identify 5D0000 as a live filesystem/cache buffer. 4033E6-4033ED is live numerical state. The conditionally reclaimable callback-table region 4033AE-4033B5 is only eight bytes, insufficient for this snapshot.

**HYPOTHESIZED:** D=43C000 is a convenient aligned candidate inside the previously discussed BSS-to-43FFF7 gap. Required range is 43C000-43CA37 inclusive, 0xA38 (2616) bytes. **UNRESOLVED:** Its accessibility at entry, non-aliasing, stack separation, inherited-service/DMA ownership, and survival through normal SP execution. It must not be treated as unused or safe. Reading ER7 later would not establish the earlier writes were safe; a stack pointer above the block would not bound downward stack growth.

**UNRESOLVED:** Consequently the requested fully non-destructive, evidence-backed destination cannot presently be supplied. A reserved range established by the inherited memory/stack contract or a bounded ownership trace is required to promote this design. No invented safe address is used in the conclusion.

## Snapshot layout

All offsets are hexadecimal from D. Word/long values are big-endian.

| Offset | Size | Contents |
|---|---:|---|
| 000-5FF | 600 | CPU-visible bytes from 000000-0005FF, including programmed 450/458 words |
| 600-9FF | 400 | FFF800-FFFBFF, only when captured SYSCR.RAME=1 |
| A00 | 4 | Entry ER7 |
| A04 | 2 | STC.W CCR save; high byte is the original CCR |
| A06 | 2 | STC.W EXR save; high byte is the original EXR |
| A08/A0C/A10/A14 | 4 each | Original ER0/ER4/ER5/ER6, also used for restoration |
| A18 | 1 | SYSCR |
| A19 | 1 | ICRB |
| A1A/A1B | 1 each | IPRF/IPRG |
| A1C/A1D | 1 each | DTCERB/DTCERC |
| A1E | 1 | TSTR |
| A1F | 1 | Status: 0=in progress, 1=ROM/registers complete but on-chip RAM disabled, 2=both ranges complete |
| A20-A2B | C | TPU1: TCR1, TMDR1, TIOR1, zero placeholder, TIER1, TSR1, TCNT1.word, TGR1A.word, TGR1B.word |
| A2C-A37 | C | TPU2, identical arrangement |

**OBSERVED (encoding/layout):** The zero slots correspond to unimplemented FFFFE3/FFFFF3; neither address is read. Register names follow the repository's current `IDA/H8.cfg` (its header calls it H8S.cfg). TGR1B/TGR2B are included, not merely the previously audited compare-A registers.

## Capture behavior and limits

**OBSERVED (code):** First save CCR to DRAM without clobbering a general register; set CCR.I/UI; save EXR; set EXR.I2-I0 to 7. Save ER0, ER4-ER6 and ER7 directly to DRAM. ER1-ER3 are untouched. Capture controller/TPU registers, then low memory, then enabled on-chip RAM. Restore ER0/ER4-ER6, EXR and CCR, replay the displaced STM.L, and resume.

**OBSERVED (manual):** SYSCR.RAME controls on-chip RAM mapping. The RAM copy is skipped when it is clear. Reserved I/O addresses are not read. TPU counters/general registers use word reads; byte control registers use byte reads. EEPMOV.B is used only for short contiguous byte-register groups; EEPMOV.W copies memory with the manual's remaining-count retry sequence. CPU masking does not freeze DTC activation. NMI can interrupt EEPMOV.W. [Renesas hardware manual](https://www.renesas.com/en/document/mah/h8s2655-group-hardware-manual), sections 5.5.2-5.6.3, 10.2 and 18.3.

**STRONGLY INFERRED, conditional:** Ordinary maskable interrupt handlers are excluded during the main capture in all four interrupt-control modes by CCR.I/UI plus EXR mask 7. NMI remains possible outside the short EEPMOV.B blocks. Original interrupt state is restored; no SYSCR, ICR/IPR, DTCER, TSTR, TIER or timer register is written. No software DTC activation or transfer-environment waiter is invoked.

**UNRESOLVED:** Active timers/DTC/DMAC and NMI can change source state during capture. This is a sequential observational snapshot, not an atomic image. CPU masking delays servicing and adds boot latency; it does not guarantee an entirely timing-neutral startup. NMI register-save discipline, inherited trace/debug state, and active hardware at entry are not established. Completion status means copies completed, not global consistency or proven-safe ownership. On the RAME=0 path 600-9FF is untouched and invalid; no claim that on-chip RAM was captured is made.

## Exact conditional splice

**OBSERVED (bytes); HYPOTHESIZED deployment:**

| Runtime / file offset | Expected original | Proposed replacement |
|---|---|---|
| 12CC54 / 2CC54 | 01 20 6D F0 | 5A 1B 00 00 |
| 1B0000-1B011F / B0000-B011F | 0x120 (288) zero bytes | 288-byte stub below |

The only image edits in this conditional plan are these two spans, 292 bytes total. The container entry, service veneers, and trailer need no edits for this design. Original hash and original bytes must match. Updating D requires regenerating all embedded DRAM operands, not just changing the first destination load. `analysis/sp_snapshot_design.py --dest 0xADDRESS` emits a new review listing; it never modifies an image. It does not certify the new destination. No binary patch or update package was produced.

**UNRESOLVED:** This is a compact 288-byte implementation with a minimal four-byte absolute-jump splice, not a proven globally shortest H8S program. Guard/status/retry and stack-free preservation are retained because they matter for this capture.

## Validation

**OBSERVED:** `python -B analysis/sp_snapshot_design.py --self-test` passes image-hash/splice/cave checks and a narrow byte-interpreter model for RAME=0/1 and uninterrupted/interrupted EEPMOV.W. Checks cover exact ROM/RAM copies, register output layout, original ER7, restored general registers/CCR/EXR before the displaced STM, no reserved I/O reads, no peripheral writes, and capture writes confined to D..D+A37. **UNRESOLVED:** The interpreter shares encoding assumptions with the emitter; this is not independent assembler/disassembler, full CPU, timing, bus or hardware validation. Instruction encodings were compared to the [GNU h8300 opcode definitions](https://raw.githubusercontent.com/RTEMS/sourceware-mirror-binutils-gdb/master/include/opcode/h8300.h). In particular EEPMOV.B is 7B 5C 59 8F; the older local opcode note's 7B 5C 49 8F is not used.

## Exact H8S listing and bytes for UNPROVEN D=43C000

**HYPOTHESIZED implementation, exact emitted bytes; not a flash-ready recommendation.** Numeric I/O source addresses: SYSCR=FFFF39; ICRB=FFFEC1; IPRF/G=FFFEC9/A; DTCERB/C=FFFF31/32; TSTR=FFFFC0. TPU source pointer starts FFFFE0 and advances to FFFFF0 without reading the +3 holes. :8 addresses map to the top I/O page; :16 FECx operands sign-extend and the bus uses the low 24 bits.

```text
1B0000  01 40 6B A0 00 43 CA 04     stc.w ccr, @0043CA04:32
1B0008  04 C0                       orc #C0, ccr
1B000A  01 41 6B A0 00 43 CA 06     stc.w exr, @0043CA06:32
1B0012  01 41 04 07                 orc #07, exr
1B0016  01 00 6B A0 00 43 CA 08     mov.l er0, @0043CA08:32
1B001E  01 00 6B A4 00 43 CA 0C     mov.l er4, @0043CA0C:32
1B0026  01 00 6B A5 00 43 CA 10     mov.l er5, @0043CA10:32
1B002E  01 00 6B A6 00 43 CA 14     mov.l er6, @0043CA14:32
1B0036  01 00 6B A7 00 43 CA 00     mov.l er7, @0043CA00:32
1B003E  7A 05 00 43 CA 18           mov.l #0043CA18, er5
1B0044  28 39                       mov.b @SYSCR:8, r0l
1B0046  68 D8                       mov.b r0l, @er5
1B0048  0B 05                       adds #1, er5
1B004A  6A 08 FE C1                 mov.b @ICRB:16, r0l
1B004E  68 D8                       mov.b r0l, @er5
1B0050  0B 05                       adds #1, er5
1B0052  6A 08 FE C9                 mov.b @IPRF:16, r0l
1B0056  68 D8                       mov.b r0l, @er5
1B0058  0B 05                       adds #1, er5
1B005A  6A 08 FE CA                 mov.b @IPRG:16, r0l
1B005E  68 D8                       mov.b r0l, @er5
1B0060  0B 05                       adds #1, er5
1B0062  28 31                       mov.b @DTCERB:8, r0l
1B0064  68 D8                       mov.b r0l, @er5
1B0066  0B 05                       adds #1, er5
1B0068  28 32                       mov.b @DTCERC:8, r0l
1B006A  68 D8                       mov.b r0l, @er5
1B006C  0B 05                       adds #1, er5
1B006E  28 C0                       mov.b @TSTR:8, r0l
1B0070  68 D8                       mov.b r0l, @er5
1B0072  0B 05                       adds #1, er5
1B0074  F8 00                       mov.b #00, r0l
1B0076  68 D8                       mov.b r0l, @er5
1B0078  0B 05                       adds #1, er5
1B007A  7A 06 00 FF FF E0           mov.l #00FFFFE0, er6
1B0080  79 08 00 02                 mov.w #0002, e0 ; two TPU channels
1B0084  FC 03                       mov.b #03, r4l
1B0086  7B 5C 59 8F                 eepmov.b ; TCRn/TMDRn/TIORn, three byte reads
1B008A  0B 06                       adds #1, er6 ; skip reserved FFFFE3/FFFFF3
1B008C  F8 00                       mov.b #00, r0l
1B008E  68 D8                       mov.b r0l, @er5
1B0090  0B 05                       adds #1, er5
1B0092  FC 02                       mov.b #02, r4l
1B0094  7B 5C 59 8F                 eepmov.b ; TIERn/TSRn, two byte reads
1B0098  79 04 00 03                 mov.w #0003, r4
1B009C  6D 60                       mov.w @er6+, r0 ; TCNTn/TGRnA/TGRnB
1B009E  69 D0                       mov.w r0, @er5
1B00A0  0B 85                       adds #2, er5
1B00A2  1B 54                       dec.w #1, r4
1B00A4  46 F6                       bne tpu_words
1B00A6  0B 96                       adds #4, er6 ; next channel at +10
1B00A8  1B 58                       dec.w #1, e0
1B00AA  46 D8                       bne tpu_channel
1B00AC  7A 05 00 43 C0 00           mov.l #0043C000, er5
1B00B2  1A E6                       sub.l er6, er6
1B00B4  79 04 06 00                 mov.w #0600, r4
1B00B8  7B D4 59 8F                 eepmov.w
1B00BC  0D 44                       mov.w r4, r4
1B00BE  46 F8                       bne copy_rom
1B00C0  6A 28 00 43 CA 18           mov.b @0043CA18:32, r0l
1B00C6  73 08                       btst #0, r0l
1B00C8  47 16                       beq ram_disabled
1B00CA  7A 06 00 FF F8 00           mov.l #00FFF800, er6
1B00D0  79 04 04 00                 mov.w #0400, r4
1B00D4  7B D4 59 8F                 eepmov.w
1B00D8  0D 44                       mov.w r4, r4
1B00DA  46 F8                       bne copy_ram
1B00DC  F8 02                       mov.b #02, r0l
1B00DE  40 02                       bra commit
1B00E0  F8 01                       mov.b #01, r0l
1B00E2  6A A8 00 43 CA 1F           mov.b r0l, @0043CA1F:32
1B00E8  01 00 6B 20 00 43 CA 08     mov.l @0043CA08:32, er0
1B00F0  01 00 6B 24 00 43 CA 0C     mov.l @0043CA0C:32, er4
1B00F8  01 00 6B 25 00 43 CA 10     mov.l @0043CA10:32, er5
1B0100  01 00 6B 26 00 43 CA 14     mov.l @0043CA14:32, er6
1B0108  01 41 6B 20 00 43 CA 06     ldc.w @0043CA06:32, exr
1B0110  01 40 6B 20 00 43 CA 04     ldc.w @0043CA04:32, ccr
1B0118  01 20 6D F0                 stm.l er0-er2, @-er7 ; displaced original instruction
1B011C  5A 12 CC 58                 jmp @12CC58:24
```

## Contiguous stub bytes

```text
01 40 6B A0 00 43 CA 04 04 C0 01 41 6B A0 00 43
CA 06 01 41 04 07 01 00 6B A0 00 43 CA 08 01 00
6B A4 00 43 CA 0C 01 00 6B A5 00 43 CA 10 01 00
6B A6 00 43 CA 14 01 00 6B A7 00 43 CA 00 7A 05
00 43 CA 18 28 39 68 D8 0B 05 6A 08 FE C1 68 D8
0B 05 6A 08 FE C9 68 D8 0B 05 6A 08 FE CA 68 D8
0B 05 28 31 68 D8 0B 05 28 32 68 D8 0B 05 28 C0
68 D8 0B 05 F8 00 68 D8 0B 05 7A 06 00 FF FF E0
79 08 00 02 FC 03 7B 5C 59 8F 0B 06 F8 00 68 D8
0B 05 FC 02 7B 5C 59 8F 79 04 00 03 6D 60 69 D0
0B 85 1B 54 46 F6 0B 96 1B 58 46 D8 7A 05 00 43
C0 00 1A E6 79 04 06 00 7B D4 59 8F 0D 44 46 F8
6A 28 00 43 CA 18 73 08 47 16 7A 06 00 FF F8 00
79 04 04 00 7B D4 59 8F 0D 44 46 F8 F8 02 40 02
F8 01 6A A8 00 43 CA 1F 01 00 6B 20 00 43 CA 08
01 00 6B 24 00 43 CA 0C 01 00 6B 25 00 43 CA 10
01 00 6B 26 00 43 CA 14 01 41 6B 20 00 43 CA 06
01 40 6B 20 00 43 CA 04 01 20 6D F0 5A 12 CC 58
```

## Go / no-go

| Requirement | Result |
|---|---|
| Entry hook and original bytes | OBSERVED; suitable control-flow hook |
| Pre-stack capture and replay plan | STRONGLY INFERRED; supported by the checked byte model |
| Exact candidate code/bytes | OBSERVED emitted artifact; independent execution validation UNRESOLVED |
| Unused DRAM reservation and retention | UNRESOLVED; blocker |
| Atomic timer/DTC snapshot | UNRESOLVED; not provided by this design |
| Non-destructive deployment | NO-GO until DRAM ownership and inherited execution constraints are established |
