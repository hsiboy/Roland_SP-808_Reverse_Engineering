# SP-808 / A6 investigation handoff — 2026-10-05

This is a factual continuity note, not a new evidence ledger. Findings below summarize the preceding investigation; revalidate disputed claims against primary bytes, IDA and the Renesas manual. No firmware or database edits were made during that investigation. This handoff is the only requested write.

## Objective and constraints
Transplant the Edirol A6 native ATA HDD backend into SP-808 firmware while retaining SP functionality. Current investigation concerns handler discipline, 400208 result flow, MCU resource conflicts, DTC descriptors, F0DF and the 400xxx ABI surface.
Read AGENTS.md. Use domain context to generate hypotheses, not as proof. Label results OBSERVED / STRONGLY INFERRED / HYPOTHESIZED / UNRESOLVED. Existing semantic names and historical conclusions are hypotheses unless independently supported. Do not disassemble or infer implementations inside 400xxx. Search :8, sign-extended :16, :24/:32 and register-loaded addressing. Do not modify firmware, symbols or IDA.

## Documentation reconciliation still required
The latest discovered documents are:
- SP-808EX_Evidence_Ledger_2026-10-05_v11.md
- SP-808EX_Observed_Architecture_Technical_Reference_2026-10-05_v9.md
- Roland_SP-808_Hardware_Architecture_Corrections_2026-10-05_v4.md
These versions were not yet read/reconciled when this handoff was saved. The analysis previously read Oct-4 versions v9/v7/v2 respectively. Do not attribute findings to the newer documents without reading them.

## Evidence and tooling
OBSERVED: Images are firmware/SP8EXall.bin and firmware/A6_all.bin, each 0xC0004 bytes; runtime mapping is 0x100000 + file offset.
OBSERVED: SP MD5 d744a9cd4a2790ac68d165fd7849b5d8; SHA256 e00235dd95d1f74f3ae27c463db9ed65b0800685073f9fb16ab0fc989239493d.
OBSERVED: Connected IDA database is SP, not A6.
Analysis ranges: SP 100020–1589C2; A6 100020–1634AA. A6's earlier 159174 cutoff was erroneous. Excluded startup data: SP 12CCFA–12CD7E; A6 13151E–1315A2.
An in-memory GNU h8300 opcode decoder plus constant propagation supplemented read-only IDA access. GNU source: https://raw.githubusercontent.com/RTEMS/sourceware-mirror-binutils-gdb/master/include/opcode/h8300.h . No analysis script was saved to the repository.
Decoder limitations: some CCR/EXR STC formatting needs independent validation; computed-pointer coverage is incomplete; A6 enclosing-function labels are approximate for uncalled leaves. A 24-bit pattern search is insufficient.
Use IDA/H8.cfg (header calls it H8S.cfg) names; this cfg omits TPU/DTC names, so manufacturer names fill omissions. Use TGR1A, TGR2A, TIOR3H etc, not invented names.
Manual: hardware/datasheets/REN_rej09b0331_2655hm_MAH_20060914.pdf; media/datasheets/HD6432653.pdf. Primary online reference: https://www.renesas.com/en/document/mah/h8s2655-group-hardware-manual .

## Corrections that must survive
OBSERVED: SP application DOES touch TPU1/TPU2: function 105420 calls 400380 at 10546E, loads word 0x18 at 105472, writes TGR1A at 105476 and TGR2A at 10547A using :16 addressing. The earlier “SP never touches TPU1/TPU2” conclusion is contradicted.
OBSERVED: SP 129764 writes whole-byte TSTR=0x21 at 129874, stopping TPU1/2/3/4 while leaving TPU0/5 enabled.
OBSERVED: Identified SP FFF0DF application writers affect bit 0 only; none targeting bits 1/2 were found.
OBSERVED: No identified SP DTCERA–F/DTVECR access or IRQ2-specific application operation. This does not establish absence inside opaque services.
UNRESOLVED: No fixed-address/known-pointer application access to FFF800–FFFBFF was identified in either image. Initial ER7 assignment was not established. Symbolically derived A6 DTC descriptor addresses remain runtime-dependent.
OBSERVED: A6 TGI1A handler RTE is 1265C8, not 1265C6.
OBSERVED (manual): In interrupt mode 3, after ANDC #BF,CCR leaves I=1/UI=0, enabled ICR control-level-1 interrupts can execute; EXR mask is bypassed/regarded as zero. Do not apply a strict greater-than-interrupted-EXR rule in this state.
UNRESOLVED: Actual runtime SYSCR mode and relevant ICR/IPRF/IPRG settings were not established; inherited/reset assumptions are insufficient.
UNRESOLVED: Segment-boundary waiter topology verdict remains UNRESOLVED. No known nested ISR path to the waiter was demonstrated, but NMI/inherited roots and SCI0's saved successor remain unresolved.
UNRESOLVED: 400000–400FFF is external DRAM. Source of its executable service layer has not been established. Do not assume internal MCU ROM. Startup application writes four JMP override entries only.

## Registered handler return discipline
OBSERVED: All 21 supplied handlers have one identified exit. All exit RTE except SP 13C5C0 and A6 1417DE, which use RTS to transfer to the saved SCI0 successor.
SP: 12382E saves R0.w, restores 123860, RTE 123862; 107BCA saves ER0, restores 107BE8, RTE 107BEC; 107BEE saves ER0–1, restores 107C28, RTE 107C2C; 107C2E saves ER0–1, restores 107C80, RTE 107C84; 123864 saves ER0–1, restores 12398E, RTE 123992; 13C5C0 pushes ER0 twice, replaces one stack slot with successor, pops once at 13C5F4, RTS 13C5F8; 148D12 saves R0.w, restores 148D2A, RTE 148D2C; 148C04 saves ER0, restores 148C4C, RTE 148C50; 148C52 saves ER0, restores 148C8A, RTE 148C8E.
A6: 1262B4 saves R0.w, restores 1262E6, RTE 1262E8; 10962A saves ER0, restores 109640, RTE 109644; 109646 saves ER0–1, restores 109674, RTE 109678; 10967A saves ER0–1, restores 1096B8, RTE 1096BC; 1262EA saves ER0–1, restores 126416, RTE 12641A; 1417DE pushes ER0 twice, replaces successor slot, pops at 141802, RTS 141806; 12641C saves ER0–1, restores 1264B6, RTE 1264BA; 1264BC saves ER0–1 and ER6, restores ER6 at 1265C0 and ER0–1 at 1265C4, RTE 1265C8; 1265CA saves ER0–1 and ER6, restores ER6 at 1266B2 and ER0–1 at 1266B6, RTE 1266BA; 152C84 saves R0.w, restores 152C9A, RTE 152C9C; 152B84 saves ER0, restores 152BC8, RTE 152BCC; 152BCE saves ER0, restores 152C02, RTE 152C06.
OBSERVED: No unsaved general-register use was identified in these handler bodies beyond balanced ER7 stack use. Word-only R0 handlers do not use E0. Opaque callees/successors are outside this claim.
STRONGLY INFERRED: Return discipline supports direct entry/tail dispatch.
HYPOTHESIZED/UNRESOLVED: Actual 40020C JMP trampoline implementation.

## 400208 saved successor
OBSERVED SP: selector 0x144 loaded 12D9A4; call 12D9A8; result stored to 427758 at 12D9AC. ER1 is then loaded with 13C5C0 at 12D9B4; selector 144 at 12D9BA; 40020C at 12D9BE. Saved result is not the registration ER1.
Second query: selector 144 at 13B83A, call 13B83E, store 427758 at 13B842.
Sole identified fixed reader: 13C5C8. Handler pushes ER0 twice, loads saved value, writes it to @(4,ER7) at 13C5D0, handles SCI0, pops original ER0 at 13C5F4, RTS 13C5F8 consumes successor.
OBSERVED A6: selector 144 at 140BD8; call 140BDC; store 41F188 at 140BE0; RTS 140BE8. Sole identified fixed reader 1417E6, store successor stack slot 1417EE, pop 141802, RTS 141806.
OBSERVED: No identified comparison, ER1 reload or ordinary JSR of the saved value.
UNRESOLVED: Runtime successor address and behavior; unknown-pointer readers are not ruled out.

## SP 129764 window
OBSERVED direct callers: 1082EC (10827C), 1083E8 (1083AE), 10B564 (10B49C), 10B76E (10B744).
129868 calls waiter 12BE62 with mode 1; 12986C saves TSTR and timer-8 TCR B0/B1; 129874 writes TSTR=21; 129876–129880 masks B0/B1 with F8; 129882 calls 12380A to save CCR/EXR into 422016/17; 129886 ORC #C0,CCR; 129888 loads ER0=1F0000; 12988E calls 4005C4; 129892–1298AA prepares length 1FC900–1F0000, ER1=ER6, ER0=1F0000; 1298AC calls 4005D4; 1298B0 removes stack argument; 1298B2 calls 12381C to restore CCR/EXR; 1298B6 restores TSTR; 1298B8/BA restores 8-bit timers; 1298BE calls waiter mode 0.
OBSERVED: Outside this window SP explicitly configures TPU0/3/5, has TPU3 handlers/counter readers, TPU5 delay/compare handling, and the TPU1/2 TGR writes noted above. No TPU4 access identified.
UNRESOLVED: Dependencies of 4005C4/4005D4.

## A6 segment gaps and waiter
OBSERVED: A6 waiter 12F96E saves R6; 12F972 reads FFF0DF, ANDs 6, loops while nonzero. SP 12BE62/12BE66 equivalent.
OBSERVED: TGI1A clears UI at 1264CA, clears F0DF bit 1 at 1264CC, stops TSTR1 at 1264D2, clears TSR1 TGFA at 1264D6. Continuing path polls DTCERC7 at 126580, stops timer 126586, clears TIER1 bit0 12658A, zeroes TCNT1 126590, sets DTCERB1 126594, sets TIER1 bit0 126598, tests F0DF0 12659C, conditionally starts TSTR1 1265A4, sets F0DF1 1265A8. RTE 1265C8.
OBSERVED: TGI2A clears UI 1265D8, F0DF2 1265DA, TSTR2 1265E0, TSR2 TGFA 1265E4; polls DTCERB1 126672, stops timer 126678, clears TIER2 12667C, zeroes TCNT2 126682, sets DTCERC7 126686, sets TIER2 12668A, tests F0DF0 12668E, conditionally starts timer 126696, sets F0DF2 12669A; RTE 1266BA.
OBSERVED: No scheduler call or EXR change in these continuing rearm paths.
UNRESOLVED: Whether a nested context can reach the waiter during both-clear gaps. Foreground cannot execute there without context switching; known inspected handlers showed no waiter/scheduler path, but incomplete interrupt topology prevents SAFE verdict.
Manual modes after I=1/UI=0: mode0 NMI only; mode1 NMI + enabled ICR level1; mode2 NMI + IPR greater than EXR; mode3 NMI + enabled ICR level1 with EXR mask bypassed.
TPU1: ICRB4/IPRF bits2–0; TPU2: ICRB3/IPRG bits6–4. SP 148BD8/DE/E0 and A6 152B62/66/68 OR 03 into IPRG, affecting TPU3 low field, not TPU2.

## DTC descriptors
OBSERVED: 100FA8 constructs P=FF0000+word[450], Q=FF0000+word[458].
P setup writes: +0=2B (100FB6); +4=00 (100FC6); +1=60 (100FD6); +2=00 (100FE6); +3=00 (100FF4); +8.word=0202 (101006); +A.word=0040 (101018).
Q setup writes: +0=89 (101028); +4=00 (101038); +5=60 (101048); +6=00 (101058); +7=00 (101066); +8.word=0202 (101078); +A.word=0040 (10108A).
P+5..7 and Q+1..3 are not written by setup.
Later P source-pointer bytes at 1010F8/101114/10112E and 126524/126540/12655A; Q pointer bytes at 1011B6/1011D2/1011EC and 126616/126632/12664C. Those routines also reset +8/+A words. Total 34 symbolic descriptor writes.
UNRESOLVED: Actual word[450/458] contents and descriptor placement; no application writer to those vector words established.

## F0DF census
OBSERVED SP bit0 writers only: clear 106E24,12E2DC; set 106E80,12E2F4,12E344. Waiter read 12BE66. No application bit1/2 writer found with :16 or resolved indirect forms.
OBSERVED A6: 1005B0 whole-byte AND F9 clears bits1/2; 101176/1265A8 set1;1264CC clear1;101234/12669A set2;1265DA clear2. Clear0:108E40,128820,128910,1289FA,132576. Set0:108E82,1288AE,12899E,128B16,13258E,1325DE. 128ADA ORs runtime R0l into byte; operand unresolved.
UNRESOLVED: Effects of unresolved pointers and opaque code. No additional resolved indirect or overlapping wide writer identified.

## ABI surface
OBSERVED direct sites and STRONGLY INFERRED locally resolved register targets are tabulated below.
Identified surface: 109 SP / 105 A6 distinct addresses including four startup writes/table values; 101 common, 8 SP-only, 4 A6-only.
SP-only:400394,40039C,4003A0,4003A4,4003B4,4003B8,4003BC,4005A0.
A6-only:400264,400268,40026C,4002B0.
A6-only usage:1304A6 calls4002B0; function130516 loads4002B0 intoER6 at13051E and has five inferred indirect calls13052A/2E/36/46/58; direct400264 at13053C,40026C at13054E,400268 at13055E.
STRONGLY INFERRED: Traced ATA closure (100578–101436 plus 12641C–1266BC and application callees) needs40020C,40023C,4002C8; geometry/UI helper adds400450,400468,40046C. None of the four identified A6-only entries is required by this traced closure. This is not proof that common service implementations are compatible.
OBSERVED startup override table: SP12CCFA pairs400210→1309CA,400214→1309EE,400218→10589C,400364→128F52; A613151E pairs400210→135818,400214→13583C,400218→107768,400364→12C54C.
UNRESOLVED: Entire runtime ABI; 244 SP /331 A6 register-indirect call/jump sites remained unresolved. No identified direct data reads from400xxx. Exclude floating constants40400000 and CMP400000 from ABI loads.

## Continuation priorities
1. Read/reconcile the three newest reference versions.
2. Keep corrections above explicit; do not inherit obsolete “TPU1/2 untouched”, “strict EXR nesting in mode3”, or “internal ROM service source” claims.
3. If resuming topology investigation, recover runtime SYSCR/ICR/IPR and inherited/NMI/SCI0 successor roots before declaring safety.
4. Revalidate full register coverage if an exhaustive absence claim is needed; unresolved generic pointer accesses remain.
5. A runtime dump of external DRAM400000–400FFF could recover the actual populated service bytes; boot provenance still needs primary evidence.

## Retained ABI census

Counts: C=direct call, I=locally inferred indirect call, J=jump, L=register address load, T=startup table address occurrence, W=startup write. I targets are STRONGLY INFERRED; direct occurrences are OBSERVED.

### SP

| Address | Counts |
|---|---|
| 0x40020c | {"C":6,"J":1,"L":1,"I":3} |
| 0x400348 | {"C":18} |
| 0x40058c | {"C":19} |
| 0x400584 | {"C":7} |
| 0x400588 | {"C":20} |
| 0x400580 | {"C":3} |
| 0x40057c | {"C":3} |
| 0x400568 | {"C":4} |
| 0x400558 | {"C":1} |
| 0x40056c | {"C":1} |
| 0x400570 | {"C":1} |
| 0x4003a8 | {"C":8} |
| 0x4003ac | {"C":7} |
| 0x40023c | {"C":4} |
| 0x400220 | {"C":46,"L":3,"I":9} |
| 0x400224 | {"C":21} |
| 0x400234 | {"C":10,"L":2,"I":16} |
| 0x400238 | {"C":17} |
| 0x40022c | {"C":10,"L":2,"I":10} |
| 0x400228 | {"L":2,"C":27,"I":2} |
| 0x400380 | {"C":4} |
| 0x4003b4 | {"C":2} |
| 0x4005a0 | {"C":1} |
| 0x40042c | {"C":83,"L":3,"I":9} |
| 0x400434 | {"C":82,"L":5,"I":21} |
| 0x400440 | {"C":66,"L":4,"I":13} |
| 0x4002c8 | {"C":27,"L":6,"I":16} |
| 0x400230 | {"C":10} |
| 0x4003a0 | {"C":1} |
| 0x40039c | {"C":2} |
| 0x4003b8 | {"C":1} |
| 0x4003a4 | {"C":1} |
| 0x400398 | {"C":7} |
| 0x400394 | {"C":2} |
| 0x400448 | {"C":85,"L":5,"I":19,"J":1} |
| 0x40043c | {"C":58,"L":8,"I":13} |
| 0x4004d0 | {"C":5} |
| 0x4004ac | {"C":3,"L":1,"I":3} |
| 0x4004b8 | {"L":5,"I":12,"C":14} |
| 0x4004b4 | {"C":3,"L":1,"I":1} |
| 0x400204 | {"C":2} |
| 0x4003dc | {"L":3,"I":13,"C":8} |
| 0x4003ec | {"L":1,"I":4,"C":1,"J":1} |
| 0x400404 | {"C":5} |
| 0x400400 | {"C":1} |
| 0x40046c | {"C":18} |
| 0x4003e8 | {"C":8,"L":3,"I":11,"J":1} |
| 0x400490 | {"C":5} |
| 0x4002ec | {"C":4} |
| 0x400450 | {"C":21,"L":2,"I":2} |
| 0x40045c | {"C":12,"L":1,"I":1} |
| 0x400470 | {"C":33,"L":5,"I":17,"J":1} |
| 0x4004cc | {"C":1} |
| 0x400468 | {"C":9} |
| 0x4003d4 | {"C":19,"J":1} |
| 0x4003d8 | {"C":5} |
| 0x4002e0 | {"C":3} |
| 0x400460 | {"C":16,"L":3,"I":11} |
| 0x4005c4 | {"C":1} |
| 0x4005d4 | {"C":1} |
| 0x40035c | {"C":4} |
| 0x400360 | {"C":6} |
| 0x40034c | {"C":3} |
| 0x400350 | {"C":3} |
| 0x400344 | {"C":1} |
| 0x400340 | {"C":1} |
| 0x400200 | {"J":1} |
| 0x400208 | {"C":2} |
| 0x4005bc | {"C":2} |
| 0x4004a4 | {"C":2} |
| 0x400304 | {"J":1} |
| 0x400414 | {"L":2,"I":6,"C":6} |
| 0x400410 | {"C":7} |
| 0x40044c | {"C":5} |
| 0x400438 | {"C":4} |
| 0x400480 | {"C":4} |
| 0x4003cc | {"J":1,"C":8} |
| 0x4003c0 | {"C":11} |
| 0x400428 | {"C":4} |
| 0x400454 | {"C":7} |
| 0x40048c | {"C":2} |
| 0x400494 | {"C":1} |
| 0x400498 | {"C":1} |
| 0x4003f4 | {"C":4,"J":1} |
| 0x400458 | {"C":3} |
| 0x400464 | {"C":3} |
| 0x4003d0 | {"C":3,"J":1} |
| 0x4003c8 | {"C":1} |
| 0x400478 | {"C":1,"L":1,"I":4} |
| 0x4003e4 | {"C":1} |
| 0x4003e0 | {"C":1} |
| 0x4002e4 | {"C":2} |
| 0x4004a8 | {"C":1} |
| 0x400484 | {"C":7,"L":1} |
| 0x4004b0 | {"C":1} |
| 0x4004c0 | {"C":1} |
| 0x4004c8 | {"J":1} |
| 0x400488 | {"C":5} |
| 0x400358 | {"C":1} |
| 0x400354 | {"C":1} |
| 0x4004bc | {"C":1} |
| 0x400424 | {"C":1} |
| 0x40040c | {"C":2} |
| 0x400418 | {"C":4} |
| 0x4003bc | {"C":2} |
| 0x400210 | {"T":1,"W":1} |
| 0x400214 | {"T":1,"W":1} |
| 0x400218 | {"T":1,"W":1} |
| 0x400364 | {"T":1,"W":1} |

### A6

| Address | Counts |
|---|---|
| 0x4002c8 | {"L":6,"I":17,"J":1,"C":40} |
| 0x40020c | {"L":2,"I":6,"C":5,"J":1} |
| 0x40023c | {"C":5} |
| 0x400348 | {"C":23} |
| 0x40058c | {"C":19} |
| 0x400584 | {"C":7} |
| 0x400588 | {"C":20} |
| 0x400580 | {"C":3} |
| 0x40057c | {"C":3} |
| 0x400568 | {"C":4} |
| 0x400558 | {"C":1} |
| 0x40056c | {"C":1} |
| 0x400570 | {"C":1} |
| 0x400220 | {"C":50,"L":3,"I":7} |
| 0x400224 | {"C":23} |
| 0x400234 | {"C":14,"L":1,"I":13} |
| 0x400238 | {"C":17,"L":1,"I":2} |
| 0x40022c | {"C":15,"L":2,"I":10} |
| 0x400228 | {"L":1,"C":33} |
| 0x400230 | {"C":12} |
| 0x40042c | {"C":86,"L":2,"I":6} |
| 0x400434 | {"C":90,"L":18,"I":101} |
| 0x400440 | {"C":104,"L":15,"I":68} |
| 0x400448 | {"C":98,"L":6,"I":16} |
| 0x40043c | {"C":76,"L":7,"I":18,"J":1} |
| 0x4003d4 | {"C":60,"L":1,"J":1} |
| 0x4003d8 | {"C":7} |
| 0x4004d0 | {"C":4} |
| 0x4004ac | {"C":5} |
| 0x4004b4 | {"C":3} |
| 0x4004b8 | {"C":42,"L":4,"I":37} |
| 0x400450 | {"C":31,"L":1,"I":2} |
| 0x40046c | {"C":16} |
| 0x4003dc | {"C":8,"L":3,"I":13} |
| 0x4003e8 | {"C":5,"L":3,"I":11,"J":1} |
| 0x400404 | {"C":5} |
| 0x400490 | {"C":3} |
| 0x400460 | {"C":20,"L":3,"I":6} |
| 0x40045c | {"C":12,"L":2,"I":3} |
| 0x400454 | {"C":8} |
| 0x400470 | {"C":37,"L":6,"I":17} |
| 0x4004cc | {"C":1} |
| 0x400204 | {"C":1} |
| 0x4003ec | {"L":1,"I":4,"C":2,"J":1} |
| 0x400400 | {"C":1} |
| 0x4002e0 | {"C":2} |
| 0x4005c4 | {"C":1} |
| 0x4005d4 | {"C":1} |
| 0x40035c | {"C":4} |
| 0x400360 | {"C":6} |
| 0x40034c | {"C":3} |
| 0x400350 | {"C":3} |
| 0x400344 | {"C":1} |
| 0x400340 | {"C":1} |
| 0x4002b0 | {"C":1,"L":1,"I":5} |
| 0x400264 | {"C":1} |
| 0x40026c | {"C":1} |
| 0x400268 | {"C":1} |
| 0x400200 | {"J":1} |
| 0x400380 | {"C":2} |
| 0x4003a8 | {"C":2} |
| 0x4003ac | {"C":3} |
| 0x400398 | {"C":1} |
| 0x400468 | {"C":8} |
| 0x40044c | {"C":4} |
| 0x4004a4 | {"C":2} |
| 0x400304 | {"J":1} |
| 0x400414 | {"L":2,"I":6,"C":7} |
| 0x400410 | {"C":8} |
| 0x400438 | {"C":3} |
| 0x400480 | {"C":3} |
| 0x4003cc | {"J":1,"C":9} |
| 0x4003c0 | {"C":13} |
| 0x400428 | {"C":4} |
| 0x40048c | {"C":2} |
| 0x400494 | {"C":1} |
| 0x400498 | {"C":1} |
| 0x4003f4 | {"C":4,"J":1} |
| 0x400458 | {"C":3} |
| 0x400464 | {"C":3} |
| 0x4003d0 | {"C":3,"J":1} |
| 0x4003c8 | {"C":1} |
| 0x400478 | {"C":3,"L":1} |
| 0x4003e4 | {"C":1} |
| 0x4003e0 | {"C":1} |
| 0x4002e4 | {"C":2} |
| 0x4002ec | {"C":2} |
| 0x4004a8 | {"C":1} |
| 0x400484 | {"C":8} |
| 0x4004b0 | {"C":1} |
| 0x400208 | {"C":1} |
| 0x4004c0 | {"C":1} |
| 0x4004c8 | {"J":1} |
| 0x400358 | {"C":1} |
| 0x400354 | {"C":1} |
| 0x400488 | {"C":4} |
| 0x4004bc | {"C":1} |
| 0x400424 | {"C":1} |
| 0x40040c | {"C":2} |
| 0x400418 | {"C":4} |
| 0x4005bc | {"C":1} |
| 0x400210 | {"T":1,"W":1} |
| 0x400214 | {"T":1,"W":1} |
| 0x400218 | {"T":1,"W":1} |
| 0x400364 | {"T":1,"W":1} |

## Retained register access sites

OBSERVED decoded accesses; symbolic resolution is STRONGLY INFERRED. Enclosing functions require revalidation. Long TIER3 reads overlap TSR3/TCNT3. Unresolved indirect/opaque accesses are excluded.


SP: address / register / operation / instruction

100644 TIER5 R 100644 btst #0x0,@FFFEA4:16
10064C TIER5 RW 10064C bset #0x0,@FFFEA4:16
100662 TSTR R 100662 mov.b @FFFFC0:8,r1l
100666 TSTR W 100666 mov.b r1l,@FFFFC0:8
100668 TSYR R 100668 mov.b @FFFFC1:8,r1l
10066C TSYR W 10066C mov.b r1l,@FFFFC1:8
100670 TCR5 W 100670 mov.b r1l,@FFFEA0:16
100676 TMDR5 W 100676 mov.b r5l,@FFFEA1:16
10067C TIOR5 W 10067C mov.b r6l,@FFFEA2:16
100682 TCNT5 W 100682 mov.w r4,@FFFEA6:16
10068A TGRA5 W 10068A mov.w r4,@FFFEA8:16
100692 TGRB5 W 100692 mov.w r0,@FFFEAA:16
100696 TSR5 R 100696 mov.b @FFFEA5:16,r4l
10069C TSR5 W 10069C mov.b r4l,@FFFEA5:16
1006A0 TIER5 R 1006A0 mov.b @FFFEA4:16,r4l
1006A6 TIER5 W 1006A6 mov.b r4l,@FFFEA4:16
1006AA TSTR R 1006AA mov.b @FFFFC0:8,r4l
1006AE TSTR W 1006AE mov.b r4l,@FFFFC0:8
100AB8 TSTR R 100AB8 mov.b @FFFFC0:8,r1l
100ABC TSTR W 100ABC mov.b r1l,@FFFFC0:8
100ABE TSYR R 100ABE mov.b @FFFFC1:8,r1l
100AC2 TSYR W 100AC2 mov.b r1l,@FFFFC1:8
100AFE TSTR R 100AFE mov.b @FFFFC0:8,r4l
100B02 TSTR W 100B02 mov.b r4l,@FFFFC0:8
105476 TGRA1 W 105476 mov.w r0,@FFFFE8:16
10547A TGRA2 W 10547A mov.w r0,@FFFFF8:16
123832 TCNT5 R 123832 mov.w @FFFEA6:16,r0
12383C TIER5 R 12383C mov.b @FFFEA4:16,r0l
123842 TIER5 W 123842 mov.b r0l,@FFFEA4:16
12384E TGRA5 W 12384E mov.w r0,@FFFEA8:16
12385C TGRB5 W 12385C mov.w r0,@FFFEAA:16
12386A ISR RW 12386A bclr #0x3,@FFFF2F:8
12386E IER RW 12386E bclr #0x3,@FFFF2E:8
12986C TSTR R 12986C mov.b @FFFFC0:8,r4h
129874 TSTR W 129874 mov.b r0l,@FFFFC0:8
1298B6 TSTR W 1298B6 mov.b r4h,@FFFFC0:8
12A7FC IER RW 12A7FC bset #0x3,@FFFF2E:8
12A802 IER RW 12A802 bclr #0x3,@FFFF2E:8
148B82 TCR3 W 148B82 mov.b r0l,@FFFE80:32
148B88 TMDR3 W 148B88 mov.b r0h,@FFFE81:32
148B8E TIORH3 W 148B8E mov.b r0h,@FFFE82:32
148B94 TIORL3 W 148B94 mov.b r0h,@FFFE83:32
148B9C TIER3 W 148B9C mov.b r0l,@FFFE84:32
148BA2 TSR3 W 148BA2 mov.b r0h,@FFFE85:32
148BAA TCNT3 W 148BAA mov.w r0,@FFFE86:32
148BB4 TGRA3 W 148BB4 mov.w r0,@FFFE88:32
148BE6 TSTR RW 148BE6 bset #0x3,@FFFFC0:32
148BF2 TIER3 W 148BF2 mov.b r0l,@FFFE84:32
148C08 TSR3 RW 148C08 bclr #0x1,@FFFE85:32
148C46 TGRB3 W 148C46 mov.w r0,@FFFE8A:32
148C56 TSR3 RW 148C56 bclr #0x2,@FFFE85:32
148C84 TGRC3 W 148C84 mov.w r0,@FFFE8C:32
148C92 TCNT3 R 148C92 mov.w @FFFE86:32,e0
148CA6 TGRB3 W 148CA6 mov.w r0,@FFFE8A:32
148CBA TGRC3 W 148CBA mov.w r0,@FFFE8C:32
148D14 TSR3 RW 148D14 bclr #0x0,@FFFE85:32
148D42 TIER3 R 148D42 mov.l @er1,er0
148D76 TIER3 R 148D76 mov.l @er1,er0
148D92 TIER3 R 148D92 mov.l @er1,er2

A6: address / register / operation / instruction

100580 IER RW 100580 bset #0x2,@FFFF2E:8
100586 IER RW 100586 bclr #0x2,@FFFF2E:8
1005CE IER RW 1005CE bclr #0x2,@FFFF2E:8
10066C IER RW 10066C bset #0x2,@FFFF2E:8
10108C TSYR R 10108C mov.b @FFFFC1:8,r0l
101090 TSYR W 101090 mov.b r0l,@FFFFC1:8
101094 TCR1 W 101094 mov.b r0l,@FFFFE0:8
101098 TMDR1 W 101098 mov.b r0l,@FFFFE1:8
10109C TIOR1 W 10109C mov.b r0l,@FFFFE2:8
1010A0 TIER1 W 1010A0 mov.b r0l,@FFFFE4:8
1010A6 TGRA1 W 1010A6 mov.w r0,@FFFFE8:16
1010AC TCR2 W 1010AC mov.b r0l,@FFFFF0:8
1010B0 TMDR2 W 1010B0 mov.b r0l,@FFFFF1:8
1010B4 TIOR2 W 1010B4 mov.b r0l,@FFFFF2:8
1010B8 TIER2 W 1010B8 mov.b r0l,@FFFFF4:8
1010BE TGRA2 W 1010BE mov.w r0,@FFFFF8:16
1010C8 DTCERC R 1010C8 btst #0x7,@FFFF32:8
1010CE DTCERB R 1010CE btst #0x1,@FFFF31:8
101154 TSTR RW 101154 bclr #0x1,@FFFFC0:8
101158 TIER1 RW 101158 bclr #0x0,@FFFFE4:8
10115E TCNT1 W 10115E mov.w r0,@FFFFE6:16
101162 DTCERB RW 101162 bset #0x1,@FFFF31:8
101166 TIER1 RW 101166 bset #0x0,@FFFFE4:8
101172 TSTR RW 101172 bset #0x1,@FFFFC0:8
101186 DTCERC R 101186 btst #0x7,@FFFF32:8
10118C DTCERB R 10118C btst #0x1,@FFFF31:8
101212 TSTR RW 101212 bclr #0x2,@FFFFC0:8
101216 TIER2 RW 101216 bclr #0x0,@FFFFF4:8
10121C TCNT2 W 10121C mov.w r0,@FFFFF6:16
101220 DTCERC RW 101220 bset #0x7,@FFFF32:8
101224 TIER2 RW 101224 bset #0x0,@FFFFF4:8
101230 TSTR RW 101230 bset #0x2,@FFFFC0:8
10156A TIER5 R 10156A btst #0x0,@FFFEA4:16
101572 TIER5 RW 101572 bset #0x0,@FFFEA4:16
101586 TSTR R 101586 mov.b @FFFFC0:8,r0l
10158A TSTR W 10158A mov.b r0l,@FFFFC0:8
10158C TSYR R 10158C mov.b @FFFFC1:8,r0l
101590 TSYR W 101590 mov.b r0l,@FFFFC1:8
101594 TCR5 W 101594 mov.b r0l,@FFFEA0:16
10159A TMDR5 W 10159A mov.b r0l,@FFFEA1:16
1015A0 TIOR5 W 1015A0 mov.b r0l,@FFFEA2:16
1015A6 TCNT5 W 1015A6 mov.w r0,@FFFEA6:16
1015AE TGRA5 W 1015AE mov.w r0,@FFFEA8:16
1015B6 TGRB5 W 1015B6 mov.w e0,@FFFEAA:16
1015BA TSR5 R 1015BA mov.b @FFFEA5:16,r0l
1015C0 TSR5 W 1015C0 mov.b r0l,@FFFEA5:16
1015C4 TIER5 R 1015C4 mov.b @FFFEA4:16,r0l
1015CA TIER5 W 1015CA mov.b r0l,@FFFEA4:16
1015CE TSTR R 1015CE mov.b @FFFFC0:8,r0l
1015D2 TSTR W 1015D2 mov.b r0l,@FFFFC0:8
1019C0 TSTR R 1019C0 mov.b @FFFFC0:8,r0l
1019C4 TSTR W 1019C4 mov.b r0l,@FFFFC0:8
1019C6 TSYR R 1019C6 mov.b @FFFFC1:8,r0l
1019CA TSYR W 1019CA mov.b r0l,@FFFFC1:8
101A06 TSTR R 101A06 mov.b @FFFFC0:8,r0l
101A0A TSTR W 101A0A mov.b r0l,@FFFFC0:8
1262B8 TCNT5 R 1262B8 mov.w @FFFEA6:16,r0
1262C2 TIER5 R 1262C2 mov.b @FFFEA4:16,r0l
1262C8 TIER5 W 1262C8 mov.b r0l,@FFFEA4:16
1262D4 TGRA5 W 1262D4 mov.w r0,@FFFEA8:16
1262E2 TGRB5 W 1262E2 mov.w r0,@FFFEAA:16
1262F0 ISR RW 1262F0 bclr #0x3,@FFFF2F:8
1262F4 IER RW 1262F4 bclr #0x3,@FFFF2E:8
126422 ISR RW 126422 bclr #0x2,@FFFF2F:8
126426 IER RW 126426 bclr #0x2,@FFFF2E:8
1264D2 TSTR RW 1264D2 bclr #0x1,@FFFFC0:8
1264D6 TSR1 RW 1264D6 bclr #0x0,@FFFFE5:8
126580 DTCERC R 126580 btst #0x7,@FFFF32:8
126586 TSTR RW 126586 bclr #0x1,@FFFFC0:8
12658A TIER1 RW 12658A bclr #0x0,@FFFFE4:8
126590 TCNT1 W 126590 mov.w r0,@FFFFE6:16
126594 DTCERB RW 126594 bset #0x1,@FFFF31:8
126598 TIER1 RW 126598 bset #0x0,@FFFFE4:8
1265A4 TSTR RW 1265A4 bset #0x1,@FFFFC0:8
1265E0 TSTR RW 1265E0 bclr #0x2,@FFFFC0:8
1265E4 TSR2 RW 1265E4 bclr #0x0,@FFFFF5:8
126672 DTCERB R 126672 btst #0x1,@FFFF31:8
126678 TSTR RW 126678 bclr #0x2,@FFFFC0:8
12667C TIER2 RW 12667C bclr #0x0,@FFFFF4:8
126682 TCNT2 W 126682 mov.w r0,@FFFFF6:16
126686 DTCERC RW 126686 bset #0x7,@FFFF32:8
12668A TIER2 RW 12668A bset #0x0,@FFFFF4:8
126696 TSTR RW 126696 bset #0x2,@FFFFC0:8
12E1A6 IER RW 12E1A6 bset #0x3,@FFFF2E:8
12E1AC IER RW 12E1AC bclr #0x3,@FFFF2E:8
152B1C TCR3 W 152B1C mov.b r0l,@FFFE80:16
152B20 TMDR3 W 152B20 mov.b r0h,@FFFE81:16
152B24 TIORH3 W 152B24 mov.b r0h,@FFFE82:16
152B28 TIORL3 W 152B28 mov.b r0h,@FFFE83:16
152B2E TIER3 W 152B2E mov.b r0l,@FFFE84:16
152B32 TSR3 W 152B32 mov.b r0h,@FFFE85:16
152B38 TCNT3 W 152B38 mov.w r0,@FFFE86:16
152B40 TGRA3 W 152B40 mov.w r0,@FFFE88:16
152B6C TSTR RW 152B6C bset #0x3,@FFFFC0:8
152B74 TIER3 W 152B74 mov.b r0l,@FFFE84:16
152B88 TSR3 RW 152B88 bclr #0x1,@FFFE85:16
152BC4 TGRB3 W 152BC4 mov.w r0,@FFFE8A:16
152BD2 TSR3 RW 152BD2 bclr #0x2,@FFFE85:16
152BFE TGRC3 W 152BFE mov.w r0,@FFFE8C:16
152C0A TCNT3 R 152C0A mov.w @FFFE86:16,e0
152C1C TGRB3 W 152C1C mov.w r0,@FFFE8A:16
152C2E TGRC3 W 152C2E mov.w r0,@FFFE8C:16
152C86 TSR3 RW 152C86 bclr #0x0,@FFFE85:16
152CB2 TIER3 R 152CB2 mov.l @er1,er0
152CE6 TIER3 R 152CE6 mov.l @er1,er0
152D02 TIER3 R 152D02 mov.l @er1,er2
