# Roland SP-808EX firmware investigation findings

**Internal version:** 1.0  
**Report date:** 2026-10-05 (Europe/London)  
**Evidence collection:** investigation recorded in this conversation, initiated with environment date 2026-10-02  
**Primary target:** SP8EXall.bin in the currently open IDA database  
**Focus:** 0x174B40; surrounding data at 0x174B1C–0x174BC5; UI and timed-record consumers  
**Status:** technical research report; no firmware or IDA annotations applied

## 1. Purpose and principal findings

The project concerns reverse engineering of Roland SP-808/SP-808EX firmware, particularly removable-storage behavior and its surrounding UI and hardware interactions.

The investigation began because IDA did not consider the cursor address 0x174B40 part of a function. The evidence strongly supports the conclusion that this is appropriate: 0x174B40 begins the final six-byte timed-action record in a ROM sequence, rather than executable instructions.

The region 0x174B1C–0x174BC5 contains two formats:

1. Seven six-byte timed-action records at 0x174B1C–0x174B45.
2. Sixteen eight-byte pointer pairs at 0x174B46–0x174BC5. Each pair supplies a UI command-list pointer and an optional timed-action sequence pointer.

The UI command lists themselves use another eight-byte format. They are interpreted by the routine at 0x138560. Their first word contains a five-bit operation tag and an eleven-bit parameter. Their second word contains operation-dependent flags/parameters. Their final four bytes contain an operation-dependent payload. A masked tag of 0xF800 ends a list.

The constant 0x0001E848 (125,000) in the timed records is an elapsed-counter threshold. The consumer reads it unchanged and processes a record when the current counter minus the saved counter is strictly greater than the threshold. It is not established as a storage capacity, byte count, sample count, or duration in seconds.

The timed-record consumer begins at 0x155754. IDA does not currently define a function there. This is a separate case of executable code without a defined function boundary; it must not be confused with the data at 0x174B40.

## 2. Evidence classification and research constraints

This report uses these confidence categories:

- **Observed:** established from tool responses, firmware bytes, or returned disassembly.
- **Inferred:** strongly supported interpretation of those observations.
- **Hypothesized:** plausible interpretation requiring further verification.
- **Speculative:** possibility supported principally by domain context.

Evidence provenance is additionally identified where significant:

- **IDA observation:** returned by the IDA MCP tools.
- **Firmware observation:** obtained by reading the repository binary.
- **Firmware-derived reconstruction:** manually decoded instructions outside IDA-defined functions.
- **Existing project claim:** a repository annotation or previous interpretation, not independently established merely by its presence.

The SP-808 is a musical sampler/workstation with storage operations, front-panel controls, display behavior, audio/DSP hardware, and MIDI. This context is useful for ranking hypotheses, but does not replace instruction and data-flow evidence.

All IDA and repository investigation was read-only. No functions were created, bytes patched, comments added, types changed, or symbols renamed. This report is the only intended new artifact.

### 2.1 Tool limitations

The exposed IDA disassembly tool accepts addresses inside defined functions. It failed at 0x174B40 and at 0x155754 because no containing function was defined. There was no exposed arbitrary-memory or arbitrary-range disassembly tool.

Consequently:

- Defined-function instructions below were obtained directly from IDA.
- Instructions reconstructed around 0x155754 came from the matching repository firmware image, not a direct arbitrary-address disassembly response.
- Local bytes cannot prove that the current IDA database has no patches.
- Reference enumeration reflects the current IDA analysis. Absence of a reference does not exclude dynamically calculated addresses.
- This report consolidates the recorded investigation; it is not a fresh verification of every address against IDA on the report date.

## 3. Input identity and initial database inspection

### 3.1 Metadata returned by IDA

| Property | Value |
|---|---|
| Input filename/module | SP8EXall.bin |
| Input path | C:\wtf\Roland\sp-808\decompile\June_2026\SP8EXall.bin |
| Reported base | 0x0 |
| Reported size | 0x380000 |
| Input filesize | 0xC0004 |
| MD5 | d744a9cd4a2790ac68d165fd7849b5d8 |
| SHA-256 | e00235dd95d1f74f3ae27c463db9ed65b0800685073f9fb16ab0fc989239493d |
| CRC32 | 0xA3E8DB55 |
| Initial cursor address | 0x174B40 |
| Function containing cursor | None |

The initial response described the database range as 0x000000–0x37FFFF by adding the reported size to the reported base. This is an **arithmetic inference from metadata**, not a verified segment range. Later references include addresses above this interval, such as 0x43B9FC and hardware registers near 0xFFFFFE84. Do not treat the initial range as a complete memory map or verified minimum/maximum database address.

### 3.2 Processor identification

The initial instructions showed H8-family syntax, including extended er registers and stm.l/ldm.l. The initial report inferred H8/300H-compatible architecture from that syntax.

Existing project documentation identifies the target as H8S-family firmware for the H8S/2653 and describes the IDA module as h8s300a. Other repository documents describe H8/300H Advanced as the loading choice. These are project claims/navigation guidance. The metadata MCP response did not expose the actual configured processor module, and the exact module was not independently queried.

For this report, H8S-family is the supported working architecture; the initial syntax-based inference is not a precise processor identification.

### 3.3 First ten enumerated functions

| Start | Name returned by IDA | Size |
|---|---|---|
| 0x100020 | sub_100020 | 0x74 |
| 0x100094 | sub_100094 | 0x08 |
| 0x10009C | sub_10009C | 0x6E |
| 0x10010A | sub_10010A | 0x90 |
| 0x10019A | sub_10019A | 0x64 |
| 0x1001FE | sub_1001FE | 0x5E |
| 0x10025C | sub_10025C | 0x2E |
| 0x10028A | sub_10028A | 0x9A |
| 0x100324 | sub_100324 | 0x2A |
| 0x10034E | sub_10034E | 0x50 |

## 4. Firmware image match and address mapping

The repository file firmware/SP8EXall.bin was read without modification.

Observed properties:

- Size: 0xC0004 bytes.
- MD5: d744a9cd4a2790ac68d165fd7849b5d8.
- These match the input size and MD5 returned by IDA.

For the examined ROM area, the working mapping is:

    runtime ROM address = file offset + 0x100000

Examples:

| Runtime address | Repository file offset |
|---|---|
| 0x135DC4 | 0x35DC4 |
| 0x155754 | 0x55754 |
| 0x174B1C | 0x74B1C |
| 0x174B40 | 0x74B40 |
| 0x174B46 | 0x74B46 |
| 0x178414 | 0x78414 |

The mapping is corroborated by encoded operands and known string locations. It should not be generalized without checking to other firmware images, all segments, or the trailing bytes of the file.

## 5. Why 0x174B40 is not a function

### 5.1 Direct IDA observations

- get_function_by_address reported no containing function at 0x174B40.
- get_current_function reported the same when the cursor was there.
- disassemble_function failed at that address because no containing function was defined.
- get_xrefs_to returned no direct references to 0x174B40.
- Enumerating all functions returned 3,062 entries with no additional page.
- No functions were defined near or after 0x174B40.

The last three enumerated function starts were:

| Start | Size |
|---|---|
| 0x15870E | 0xBC |
| 0x1587CA | 0xF2 |
| 0x1588BC | 0x106 |

The last defined function contains:

    0x158990: rts
    0x1589C0: bra loc_15896C

Its trailing branch returns into its own body, rather than falling through toward 0x174B40. These boundaries do not prove that every later byte is data, but provide no control-flow evidence for execution at the target.

### 5.2 Classification

**Inferred, high confidence:** 0x174B40 is structured constant data: the four-byte delay field of the final timed record.

It is not supported as:

- a function entry;
- executable code missed by IDA;
- inline instructions;
- arbitrary padding;
- a code branch target.

The absence of a direct reference is explained by sequential consumption: the active record pointer advances six bytes at a time until it reaches 0x174B40.

## 6. Exact region layout

| Inclusive range | Size | Format |
|---|---:|---|
| 0x174B1C–0x174B45 | 42 bytes | Seven packed six-byte timed records |
| 0x174B46–0x174BC5 | 128 bytes | Sixteen eight-byte pointer pairs |
| 0x174BC6 onward | Not fully delimited | Nearby ASCII strings and subsequent data |

The zero word at 0x174B44 is the action field of the final timed record. It should not be treated as unexplained alignment padding.

### 6.1 Timed records

All fields are big-endian.

| Record start | Delay hexadecimal | Delay decimal | Action |
|---|---|---:|---|
| 0x174B1C | 0x00098968 | 625,000 | 0x8064 |
| 0x174B22 | 0x0001E848 | 125,000 | 0x0046 |
| 0x174B28 | 0x0003D090 | 250,000 | 0x8064 |
| 0x174B2E | 0x0001E848 | 125,000 | 0x0046 |
| 0x174B34 | 0x0003D090 | 250,000 | 0x8064 |
| 0x174B3A | 0x0001E848 | 125,000 | 0x0046 |
| 0x174B40 | 0x0001E848 | 125,000 | 0x0000 |

Raw target bytes:

    0x174B40: 00 01 E8 48 00 00

The terminal record has a nonzero delay and a zero action. The routine evaluates the delay before testing the action.

### 6.2 Pointer pairs

| Index | Pair start | +0: UI-list pointer | +4: timed-sequence pointer |
|---:|---|---|---|
| 0 | 0x174B46 | 0x174A04 | 0 |
| 1 | 0x174B4E | 0x174A44 | 0x174A6C |
| 2 | 0x174B56 | 0x174976 | 0x17498E |
| 3 | 0x174B5E | 0x174976 | 0 |
| 4 | 0x174B66 | 0x1748DA | 0x1749A0 |
| 5 | 0x174B6E | 0x1748DA | 0 |
| 6 | 0x174B76 | 0x174A04 | 0 |
| 7 | 0x174B7E | 0x174A24 | 0 |
| 8 | 0x174B86 | 0x174A8A | 0x174AA2 |
| 9 | 0x174B8E | 0x174AB4 | 0x174AA2 |
| 10 | 0x174B96 | 0x174ACC | 0x174AA2 |
| 11 | 0x174B9E | 0x174AE4 | 0x174AA2 |
| 12 | 0x174BA6 | 0x174B04 | 0x174AA2 |
| 13 | 0x174BAE | 0x1749AC | 0x1749D4 |
| 14 | 0x174BB6 | 0x1749EC | 0 |
| 15 | 0x174BBE | 0x1749EC | 0 |

The seven-record sequence at 0x174B1C is directly registered by a separate path; it is not among the timed-sequence pointers in these sixteen pairs.

## 7. References and callers

### 7.1 Exhaustive bounded reference check

Every byte address in 0x174B1C–0x174BC5 was queried through get_xrefs_to. Exactly three target addresses returned references:

| Source instruction | Target | IDA reference type | Containing function |
|---|---|---|---|
| 0x135DC4 | 0x174B1C | data | 0x135D84 |
| 0x135C36 | 0x174B46 | data | 0x135C1A |
| 0x135BFA | 0x174B4A | data | 0x135BEE |

A repository-firmware scan for all encoded 24-bit and 32-bit addresses in that interval found the same operands. The 24-bit byte sequences occur inside the four-byte operands, at 0x135DC7, 0x135C3D, and 0x135C01 respectively.

No code-type reference into the interval was returned. This is an exhaustive result for the inspected IDA references and encoded absolute operands, not a proof against unrecognized or computed references.

### 7.2 UI-list selection

Direct IDA disassembly:

    0x135C28: mov.l #ui_media_index, er6
    0x135C2E: mov.w @er6, r0
    0x135C30: exts.l er0
    0x135C32: shll.l #2, er0
    0x135C34: shll.l er0
    0x135C36: mov.l @((dword_174B44+2):32,er0), er0
    0x135C40: jsr sub_138560

The address expression evaluates to 0x174B46 + index*8.

The caller is:

    0x135BBA: bsr ui_msg_dispatch_mount

Existing names ui_media_index and ui_msg_dispatch_mount are annotations. The verified behavior is selection of a UI command-list pointer by an eight-byte index.

### 7.3 Timed-sequence selection

Direct IDA disassembly:

    0x135BEE: mov.w @ui_media_index:32, r0
    0x135BF4: exts.l er0
    0x135BF6: shll.l #2, er0
    0x135BF8: shll.l er0
    0x135BFA: mov.l @(off_174B4A:32,er0), er0
    0x135C04: jmp sub_155702

The address expression evaluates to 0x174B4A + index*8.

A caller at 0x135BA4 invokes this selector after zeroing the index. A zero timed-sequence pointer is passed to the registration routine, which ignores null input rather than clearing an existing sequence.

### 7.4 Direct registration of 0x174B1C

The routine at 0x135D84 calls the existing disk-state routine, tests its result, and compares two RAM words before selecting a path.

Relevant instructions:

    0x135D92: jsr disk_state_machine
    0x135D96: cmp.w #1, r0
    0x135D9A: bne loc_135DD0
    0x135DA6: mov.w @word_42722A:32, r0
    0x135DAC: mov.w @word_427228:32, r1
    0x135DB2: cmp.w r1, r0
    0x135DB4: bcc loc_135DBC
    0x135DBC: mov.w #0x4C, r0
    0x135DC0: jsr sub_1359AC
    0x135DC4: mov.l #wrong_media_size_entry.menu_control_flags, er0
    0x135DCA: jsr sub_155702
    0x135DCE: bra loc_135DF0
    0x135DF6: rts

The immediate operand at 0x135DC4 is 0x174B1C. The existing member name menu_control_flags does not describe the verified first field: the consumer treats the first four bytes as a delay threshold.

The caller is 0x135D0C: bsr sub_135D84, inside the routine at 0x135CB0. Its paths select calls based on the indexed state. The evidence connects this timed sequence with the storage/UI control path, but does not independently establish every semantic name on that path.

## 8. Timed-sequence registration, processing, and cleanup

### 8.1 Registration at 0x155702

Direct IDA disassembly:

    0x155706: mov.l er0, er6
    0x155708: beq loc_15571E
    0x15570A: mov.l er6, @dword_43B9FC:32
    0x155712: jsr sub_148D2E
    0x155716: mov.l er0, @dword_43BA00:32

Observed:

- 0x43B9FC holds the active/current sequence pointer.
- 0x43BA00 holds a counter timestamp.
- Nonzero input registers a sequence and takes a timestamp.
- Zero input leaves those globals unchanged.

### 8.2 Consumer at 0x155754

IDA returns no containing function here. The following is a **firmware-derived reconstruction**, not a direct IDA function-disassembly result.

Important instructions:

    0x15575C: mov.l #0x43B9FC, er3
    0x155762: jsr sub_148D2E
    0x155766: mov.l er0, er4
    0x155768: mov.l @er3, er5
    0x15576C: mov.w @(4:16,er5), r6
    0x155770: mov.l @0x43BA00:32, er1
    0x155778: sub.l er1, er0
    0x15577A: mov.l @er5, er5
    0x15577E: cmp.l er5, er0
    0x155780: bls 0x1557CE
    0x155782: mov.w r6, r6
    0x155784: beq 0x1557CA

Critical bytes:

| Address | Bytes | Reconstructed operation |
|---|---|---|
| 0x155768 | 01 00 69 35 | Load current record pointer |
| 0x15576C | 6F 56 00 04 | Load action word at +4 |
| 0x155778 | 1A 90 | Subtract previous timestamp |
| 0x15577A | 01 00 69 55 | Load four-byte threshold |
| 0x15577E | 1F D0 | Compare elapsed with threshold |
| 0x155780 | 43 4C | Unsigned lower-or-same branch |
| 0x155782 | 0D 66 | Test action word |
| 0x155784 | 47 44 | Branch if action is zero |

The consumer waits while elapsed <= threshold. It performs the action only when elapsed > threshold.

The subtraction uses 32-bit arithmetic; the reconstructed arithmetic is consistent with modulo-2^32 elapsed-counter subtraction. Long-interval behavior across counter wrap was not experimentally tested.

For a nonzero action:

- 0x155786 stores the captured current counter at 0x43BA00.
- 0x15578E tests bit 15 of the action.
- 0x155792 clears that bit on the set-bit path.
- The two paths issue different parameter writes and state toggles.
- The pointer then advances by six.

    0x1557BA: mov.l @er3, er0
    0x1557BE: add.l #6, er0
    0x1557C4: mov.l er0, @er3

A zero action branches to 0x1557CA and calls 0x155724. Because the time comparison occurs first, the final zero-action record supplies a real terminal delay.

Conceptual pseudocode, assuming an active valid record pointer:

    now = read_counter();
    record = current_record;
    action = read_be16(record + 4);
    elapsed = (uint32_t)(now - previous_timestamp);
    threshold = read_be32(record);

    if (elapsed <= threshold)
        return;

    if (action == 0) {
        clear_sequence_and_cleanup();
        return;
    }

    previous_timestamp = now;
    dispatch_action(action);
    current_record = record + 6;

The visible reconstructed body does not establish a safe null-pointer precondition check. Do not turn this conceptual pseudocode into executable replacement code without tracing invocation and activation conditions.

### 8.3 Action dispatch

| Action condition | Parameter write | Follow-up toggle |
|---|---|---|
| Bit 15 set | 0x125B36: group 7, parameter 10, value action & 0x7FFF | 0x126D56 |
| Bit 15 clear, nonzero | 0x125B36: group 7, parameter 11, value action | 0x126D82 |
| Entire action zero | No normal action dispatch | 0x155724 cleanup |

IDA records calls from undefined code:

- 0x15579E -> 0x125B36.
- 0x1557A2 -> 0x126D56.
- 0x1557B2 -> 0x125B36.
- 0x1557B6 -> 0x126D82.

These corroborate the reconstructed dispatch paths without defining a function.

The values in this sequence are:

- 0x8064: select first path with value 100.
- 0x0046: select second path with value 70.

Direct IDA tracing of 0x125B36 shows:

- It dispatches by group.
- Group 7 stores the supplied value in the indexed words based at 0x422124.
- It calls 0x125DE2 with the parameter index.
- Parameter 10 routes to 0x126D22.
- Parameter 11 routes to 0x126D3C.
- Those routines read words at 0x422138/0x42213A, index a word table at 0x1719A0, and pass the result through 0x108AEA with identifiers 0x105C/0x1060.

The physical meaning of that parameter table was not established.

Direct IDA tracing shows 0x126D56 and 0x126D82 toggle words at 0x422146 and 0x422148. They select 0x8001 or 0x4002 and call 0x108B7C with identifiers 0x1000 or 0x1004. That routine updates a hardware/shadow-register path involving 0xC01000 or 0xC00000 and associated RAM.

**Inferred:** the timed sequence controls two related hardware paths.

**Hypothesized:** in the sampler/workstation context, this could form an audible notification or another timed UI-associated hardware effect. An indicator or other control sequence remains a competing explanation. No physical output was observed, and no definitive audio or panel mapping was established.

### 8.4 Cleanup and activity query

At 0x155724:

- Read the active pointer.
- If zero, return.
- Otherwise clear 0x43B9FC.
- Call 0x14A284.

At 0x15573E:

- Read 0x43B9FC.
- Return a Boolean-like 1 or 0 according to whether it is nonzero.
- It does not read the pointed-to record.

The cleanup routine 0x14A284 restores parameters 10 and 11 through 0x125B36 using values derived from byte 0x43B7B2; the second value is scaled by 70/100. It also selects pointer-based state according to other globals. This is evidence of restoring shared state, not proof that zero action means a particular physical output is switched off.

### 8.5 Invocation lead

The firmware contains the 32-bit value 0x00155754 at 0x178414, among other pointer-like entries. No encoded direct jsr/jmp to 0x155754 was found in the raw scan. IDA returned no reference to 0x178414 or 0x178412.

**Hypothesized:** invocation may occur through a callback or dispatch table.

The enclosing table format and invocation mechanism were not established. This is a priority lead for a subsequent investigation.

## 9. Counter source and the 125,000 constant

### 9.1 Timestamp routine at 0x148D2E

Direct IDA observations:

- It saves interrupt/control state and sets mask bits.
- It loads a longword beginning at hardware address 0xFFFFFE84.
- It retries while the sampled low word is zero.
- It masks the upper word with 1.
- It adds the software extension at 0x427CC8.
- It restores control state and returns the result.

Relevant instructions:

    0x148D32: mov.l #0xFFFFFE84, er1
    0x148D42: mov.l @er1, er0
    0x148D46: or.w r0, r0
    0x148D48: beq loc_148D42
    0x148D4A: and.w #1, e0
    0x148D4E: mov.l @dword_427CC8:32, er1
    0x148D56: add.l er1, er0

The handler at 0x148D12 clears bit 0 at 0xFFFFFE85, increments the word at 0x427CC8, and returns with rte.

**Inferred:** this is an extended hardware-counter timestamp, including handling of a sampled status/extension condition.

### 9.2 Initialization evidence

The routine at 0x148B7E writes:

| Address | Value observed |
|---|---|
| 0xFFFFFE80 | 2 |
| 0xFFFFFE81–0xFFFFFE83 | 0 |
| 0xFFFFFE84 | 7 |
| 0xFFFFFE85 | 0 |
| 0xFFFFFE86 | word 0 |
| 0xFFFFFE88 | word 0xFFFF |

It also updates 0xFFFFFECA and sets bit 3 at 0xFFFFFFC0.

These are useful register/configuration facts. The exact applicable timer clock selection, device-specific register interpretation, and actual oscillator configuration were not independently established during this session.

### 9.3 Independent use of 125,000

The routine at 0x13B720 takes timestamps through 0x148D2E and contains:

    0x13B774: mov.l @er5, er0
    0x13B778: sub.l er4, er0
    0x13B77A: cmp.l #0x1E848, er0
    0x13B780: bls loc_13B730

The surrounding code processes input values and updates timestamps. This independently establishes another elapsed-counter budget using 125,000.

The existing name block_iter_125k is not needed for this conclusion; the subtraction and comparison provide the evidence.

### 9.4 Units and scope

Established for the investigated fields:

- Raw counter units.
- No conversion before comparison.
- Strictly greater-than threshold.
- Relative delays from the previous processed action.
- Terminal delay is also evaluated.

Not established:

- Seconds or milliseconds per threshold.
- That every occurrence of 125,000 elsewhere means time.
- Exact waveform or physical behavior generated by the actions.

Project documentation mentions a 20 MHz CPU. That alone does not establish the timer frequency or permit a reliable conversion to seconds.

## 10. Eight-byte UI command records

### 10.1 Core interpreter behavior

Direct IDA disassembly of 0x138560 establishes:

    0x13857A: mov.l er0, er6
    0x13857C: beq loc_13889C
    0x138580: mov.w @er6, r0
    0x138584: and.w #0x7FF, r0
    0x13858A: mov.w @(2:16,er6), r5
    ...
    0x1385AA: and.w #0xF800, r0
    ...
    0x138892: add.l #8, er6
    0x138898: jmp loc_138580

A null initial pointer returns. Records are processed sequentially in eight-byte steps.

| Offset | Size | Supported meaning |
|---|---:|---|
| +0 | 2 | Tag bits 15–11; operation parameter bits 10–0 |
| +2 | 2 | Operation-dependent parameter/flags |
| +4 | 4 | Operation-dependent payload |

Not every tag uses every field.

### 10.2 Common flags and positioning

Bit 15 of word +2 selects opposite argument combinations for calls to 0x40042C and 0x400450. The interpreter clears this bit from its working copy before operation-specific handling.

The exact display-mode meaning of these calls was not established. They are not safe to name as an inversion, font, layer, or color mode solely from the branch.

For applicable positioning operations, helper 0x1388AC:

- Uses the first word's low eleven bits and the second word's parameter.
- Tests bit 0x4000 in the second word to choose an alternate positioning call at 0x400438.
- Tests bit 0x2000 to apply origin-relative adjustment using globals at 0x42757B and 0x42757C.
- Otherwise passes packed positioning arguments to 0x400434.

**Inferred:** these are position and positioning-mode parameters for applicable operations. Word +2 is not uniformly a plain y coordinate.

### 10.3 Tag dispatch

The following is the observed dispatch structure; semantic descriptions are intentionally bounded.

| Masked tag | Relevant handling | Payload access |
|---|---|---|
| 0x0000 | Position helper 0x1388AC; call 0x400440 | Longword +4, matching records point to strings |
| 0x0800 | Call 0x400428 | Parameters from +0/+2 |
| 0x1000 | Choose 0x400454 or 0x400458 | Byte +4 selects path |
| 0x1800 | Call 0x400464 | Bytes +5 and +7 |
| 0x2000 | Call 0x40045C | Byte +5 |
| 0x2800 | Call 0x400460 | Byte +7 |
| 0x3000 | Call 0x400468 | Bytes +5 and +7 |
| 0x3800 | Call 0x40046C | Bytes +5 and +7 |
| 0x4000 | Call 0x400470 | Longword +4 |
| 0x4800 | Iterate pointer list and output entries | Longword +4 points to null-terminated pointer list |
| 0x5000 | Optional pointer handling; additional parameter processing | Longword +4 |
| 0x5800 | Call 0x138DBA | Bytes +5 and +7 |
| 0x6000 | Call 0x138EE8 | Longword +4 |
| 0x6800 | Position helper; call 0x40043C | Byte +4 |
| 0x7000 | Call 0x13904E | Bytes +5 and +7 |
| 0x7800 | Select 0x139664, 0x139652, or 0x1396C2 | Word +2 selects handler; word +6 is argument |
| 0x8000 | Optional pointer handling; additional parameter processing | Longword +4 |
| 0x8800 | Conditional call through 0x14752E/0x147526 | Byte +7 |
| 0xF000 | Recursive call to 0x138560 | Longword +4 is another list pointer |
| 0xF800 | Return/end list | No operation-specific payload handling |

The 0x5000 and 0x8000 paths use the optional pointer with 0x1383D6 and 0x15732A and carry out additional parameter-dependent processing.

Unknown tags follow the default progression path. Do not assume that the entire possible tag space has a defined operation.

### 10.4 Geometry evidence

The routines at 0x13904E and 0x138DBA unpack byte-sized coordinates and extents, combine them, perform bounds-related calculations, and call primitive routines. They also store origin/extent-like values around 0x42757A.

This supports geometry semantics for particular tags, especially 0x5800 and 0x7000. The exact primitive names, screen-coordinate conventions, and every flag were not proven.

The payload can be accessed as bytes +5/+7 rather than as a pointer. On this big-endian target, those are the low bytes of the two halfwords contained in the final longword.

### 10.5 Termination tag

Direct IDA evidence:

    0x138646: cmp.w #0xF800, r0
    0x13864A: beq loc_13889C

The compared value has already been masked with 0xF800. Therefore any first word whose masked tag is 0xF800 terminates interpretation; the low eleven bits need not be zero.

The common mode-selection preamble precedes this test. A terminator should not be described as necessarily having no side effects.

A zero first word is not the list terminator. It selects tag 0x0000, which can perform string output.

### 10.6 Concrete list at 0x174B04

| Record | Word +0 | Word +2 | Payload +4 |
|---|---|---|---|
| 0x174B04 | 0x7003 | 0x0006 | 0x00820014 |
| 0x174B0C | 0x0008 | 0x004C | 0x00174CD6 |
| 0x174B14 | 0xF800 | 0x0000 | 0 |

The pointer at 0x174B10 points to the ASCII string at 0x174CD6, “Wrong Media Size.”

**Inferred:** geometry setup followed by positioned text and termination. This interpretation rests on the tag consumer and string contents, not merely the prior string label.

Other pointer-table targets contain the same pattern of geometry commands, strings, optional commands, and termination.

## 11. Consumer map

| Routine/address | Verified or reconstructed role | Provenance |
|---|---|---|
| 0x135C1A | Select UI-list pointer from pair +0 | IDA disassembly |
| 0x135BEE | Select timed-sequence pointer from pair +4 | IDA disassembly |
| 0x135D84 | Directly supply sequence pointer 0x174B1C | IDA disassembly |
| 0x138560 | Interpret eight-byte UI records | IDA disassembly |
| 0x1388AC | Interpret applicable position parameters | IDA disassembly |
| 0x138DBA / 0x13904E | Consume geometry arguments extracted by UI interpreter | IDA disassembly |
| 0x155702 | Register timed pointer and timestamp | IDA disassembly |
| 0x155754 | Read six-byte timed records and dispatch actions | Firmware-derived reconstruction |
| 0x155724 | Clear active sequence and call cleanup | IDA disassembly |
| 0x15573E | Query active-pointer state only | IDA disassembly |
| 0x148D2E | Produce counter timestamp | IDA disassembly |
| 0x148D12 | Update software counter extension | IDA disassembly |
| 0x125B36 / 0x125DE2 | Store and dispatch action parameters | IDA disassembly |
| 0x126D22 / 0x126D3C | Translate selected parameters through table 0x1719A0 | IDA disassembly |
| 0x126D56 / 0x126D82 | Toggle associated control state | IDA disassembly |
| 0x14A284 | Restore shared parameters and select other state pointers | IDA disassembly |

Calls to addresses in RAM such as 0x400434, 0x400440, and 0x400450 could not be disassembled with the available function-only tool. Their ultimate implementations and runtime installation were not resolved.

This map distinguishes actual record readers from routines that only receive extracted values or inspect the active-pointer global.

## 12. Repository comparisons and existing claims

### 12.1 Matching timed sequence in A6 firmware

The exact 42-byte sequence at SP-808EX file offset 0x74B1C occurs in firmware/A6_all.bin at file offset 0x7B4DC.

**Observed:** byte-for-byte identity of the complete sequence.

**Inferred:** this representation is shared with related firmware.

Do not convert the A6 offset into a runtime address using the SP-808EX mapping without independently checking the A6 loading layout. The A6 consumer was not traced.

### 12.2 Similar timed sequences

The pointer pairs refer to sequences at:

- 0x17498E.
- 0x1749A0.
- 0x1749D4.
- 0x174A6C.
- 0x174AA2.

For example, 0x17498E begins with threshold 25,000/action 0x8064, followed by threshold 187,500/action 0x0046, and threshold 125,000/action zero.

0x174A6C begins with threshold 25,000/action 0x8064 and alternates related actions and thresholds before a terminal zero action.

These reinforce the six-byte representation and terminal-delay pattern. They do not establish physical output semantics.

### 12.3 Similar UI lists elsewhere

At 0x1239B2–0x1239B8, IDA shows a pointer to 0x1709A0 passed to 0x138560.

That list begins:

    [0x7012, 0x0006, 0x00640014]
    [0x001C, 0x0048, 0x001710A0]
    [0x0028, 0x0050, 0x001710A9]
    [0xF800, 0x0000, 0x00000000]

At 0x1359B6–0x1359BC, IDA shows a pointer to 0x17BD6E passed to the same interpreter.

That list begins:

    [0x5808, 0x0005, 0x00780016]
    [0x001C, 0x0048, 0x0017BB9B]
    [0x7800, 0x0000, 0x000000B1]
    [0xF800, 0x0000, 0x00000000]

The same interpreter has numerous additional callers throughout firmware. Its record format is therefore broader than this particular media-related table.

A raw geometry-record pattern 70 03 00 06 00 82 00 14 occurs at SP-808EX file offsets 0x74976, 0x74A8A, 0x74AB4, 0x74ACC, and 0x74B04. It also occurs at A6 file offsets 0x7B34E, 0x7B462, 0x7B48C, 0x7B4A4, and 0x80A8A.

### 12.4 Nearby strings

Firmware bytes show strings beginning at 0x174BC6, including:

- Insert.
- Destination Disk.
- Not SP-808 Disk.
- Copy FX Patches.
- Copy FX Canceled.
- Insert Source Disk.
- [EXIT] to Cancel.
- Copy Disk Canceled.
- Reading..
- Writing..
- This is SP-808 Disk.
- Not Source Disk.
- Not Destination Disk.
- This is Source Disk.
- Wrong Disk.
- (Write Protected.)
- Wrong Media Size.

Together with the selection paths, this supports an association with media handling, copy operations, and UI feedback. Mere adjacency does not establish which timed pattern produces which physical effect.

Existing helper scripts identify:

| Address | Existing label/text |
|---|---|
| 0x174BDF | str_err_not_sp808 / Not SP-808 Disk. |
| 0x174CB7 | str_err_wrong_disk / Wrong Disk. |
| 0x174CD6 | str_err_wrong_size / Wrong Media Size. |

Relevant sources:

- IDA/SP808_IDA_helper.py, string tables around lines 266–268 and 318–320.
- IDA/SP808.idc, around lines 277–279.
- IDA/SP808_IDA_helper.idc, around lines 536–538.

The scripts were read as text and never executed.

### 12.5 Other proposed formats and documentation limitations

IDA/SP808_IDA_helper.idc describes:

- Tables at 0x173368 and 0x1734B0 as eight-byte RAM-address/handler pairs.
- A descriptor at 0x171D00 as a seven-byte display format.

These are existing project claims and different candidate formats. Equal record size is not evidence of equal semantics.

hardware/datasheets/README.md identifies an H8S programming manual and related hardware manuals, but states that the specific H8S/2653 hardware manual is missing. No definitive timer-clock interpretation was established from those documents in this session.

## 13. Proposed C-like representations

These definitions describe the target byte layout only. Values are big-endian, records are packed, and target pointer fields are represented explicitly as 32-bit addresses. A host program must decode byte order rather than assume these are native host structures.

Unknown or tag-dependent semantics retain offset-based names.

```c
#include <stdint.h>

#pragma pack(push, 1)

typedef struct {
    uint32_t delay_ticks; /* +0: process when elapsed > this threshold */
    uint16_t field_04;    /* +4: zero ends sequence;
                            bit 15 selects action path */
} TimedRecord;           /* size 6 */

typedef struct {
    uint16_t field_00;    /* +0: tag = value & 0xF800;
                            parameter = value & 0x07FF */
    uint16_t field_02;    /* +2: tag-dependent flags/parameter */
    uint32_t field_04;    /* +4: pointer/value/packed payload;
                            some tags read bytes +4/+5/+7 or word +6 */
} UiRecord;              /* size 8 */

typedef struct {
    uint32_t ui_records;    /* +0: target address of UiRecord list */
    uint32_t timed_records; /* +4: target address of TimedRecord list,
                              or zero */
} PointerPair;             /* size 8 */

#pragma pack(pop)
```

No structure was applied to IDA. No universal x/y, width/height, frequency, tone, capacity, or callback interpretation is asserted for an unknown field.

## 14. Corrections and superseded interpretations

1. **0x174B40 is not merely an isolated numeric field before a pointer table.** It is the first field of the final six-byte timed record.
2. **0x174B44 is not unexplained padding.** It is that record's zero action.
3. **The first field at 0x174B1C is not established as menu control flags.** The verified consumption treats it as a four-byte elapsed-counter threshold.
4. **Earlier four-byte window labels were not all field boundaries.** The 125,000 fields in this sequence begin at 0x174B22, 0x174B2E, 0x174B3A, and 0x174B40. Windows beginning at 0x174B24 or 0x174B30 do not begin those fields.
5. **The initial database range was inferred, not verified.** Reported base/size do not establish the full segment layout.
6. **H8-family syntax does not identify the exact processor module.** H8S/2653 and h8s300a remain project context unless independently verified.
7. **Undefined code at 0x155754 is distinct from data at 0x174B40.** IDA's failure to define one does not imply the other is executable.
8. **125,000 is not assigned seconds.** The elapsed-counter use is established, but timer rate is unresolved.

## 15. Confidence assessment and follow-up tests

| Finding | Assessment |
|---|---|
| Target bytes are structured data rather than code | Inferred, high confidence |
| Seven six-byte timed records | Strongly supported by bytes and consumer reconstruction |
| Sixteen UI/timed pointer pairs | Strongly supported by bytes and two indexed loaders |
| UI interpreter uses eight-byte tagged records | Observed in IDA |
| Masked 0xF800 terminates a UI list | Observed in IDA |
| 125,000 is an elapsed-counter threshold here | Strongly supported |
| Actions operate two related hardware control paths | Inferred |
| Actions generate an audible notification | Hypothesized |
| Exact threshold duration in seconds | Unknown |
| 0x155754 invocation through callback table | Hypothesized |
| All possible computed references have been excluded | Not established |

Recommended read-only follow-up work:

1. Resolve the table surrounding 0x178414 and the invocation conditions of 0x155754. Confirm when the active pointer is valid and what schedules processing.
2. Independently verify the undefined routine's complete instruction stream with a read-only arbitrary-range disassembler. Preserve the absence of function definitions unless separately authorized.
3. Obtain authoritative H8S/2653 timer-register documentation and verify the board clock/configuration before converting thresholds into physical time.
4. Trace the implementations installed at 0x40042C, 0x400434, 0x400440, and 0x400450 to confirm UI primitive and mode semantics.
5. Trace table 0x1719A0 and the hardware paths reached through 0x108AEA/0x108B7C. Test competing audible-notification, indicator, and other-control hypotheses.
6. Compare the A6 consumer, not only the identical sequence bytes.
7. Correlate UI-state indices with user operations using independently traced event paths.
8. If physical hardware observations become available, correlate the pattern of thresholds and alternating actions with sound, indicators, and display events.

A useful falsification test for an audible-notification hypothesis is whether the same action paths are used exclusively for non-audio panel controls. A useful confirmation would be a traced connection to known sound-generation hardware or an observed sound matching the sequence timing.

## 16. Tools and reproducibility

IDA MCP tools actually used across the session:

- mcp__ida__get_metadata.
- mcp__ida__get_current_address.
- mcp__ida__get_current_function.
- mcp__ida__get_function_by_address.
- mcp__ida__list_functions.
- mcp__ida__get_xrefs_to.
- mcp__ida__disassemble_function.

Tool discovery used the available tool catalog. No mutation tools, decompilation tools, or connection-check tool were called.

Repository analysis used:

- rg filename/text searches.
- PowerShell text reads and command discovery.
- Python pathlib byte reads, hashlib MD5 verification, in-memory byte-pattern searches, and printed big-endian field decoding.

No repository analysis script was executed merely because it already existed. No analysis files, binaries, or IDA database objects were modified during evidence collection.

## 17. Internal revision history

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-10-05 | Initial consolidated technical report from this session; includes metadata, provenance, reconstructed layouts, timed/UI consumers, bounded reference inventory, cross-firmware comparisons, corrections, and testable follow-up hypotheses. |

## 18. Internal revision 1.1 - 2026-10-05

**Current appended revision:** 1.1. The version 1.0 header and sections above describe the original report and are preserved as historical material. This addition consolidates the independently checked SCI1 comparison, physical-format-I/O correlation, and ATA transfer-infrastructure startup comparison from the subsequent conversation. Its purpose is to support the SP native ATA-HDD transplant without converting unresolved platform assumptions into facts.

**Scope and provenance:** SP firmware was inspected through read-only IDA calls and raw repository bytes. A6 comparisons used raw A6_all.bin bytes when the open database was SP. Addresses in the binary correspond to file offset plus 0x100000. No IDA changes, firmware patches, or opaque 400xxx disassembly were performed. Physical packet observations below were supplied by the user, not newly measured by this investigation. Existing names were navigation aids only.

Verified image identities:

| Image | File length | MD5 | SHA-256 |
|---|---:|---|---|
| SP8EXall.bin | 0xC0004 | d744a9cd4a2790ac68d165fd7849b5d8 | e00235dd95d1f74f3ae27c463db9ed65b0800685073f9fb16ab0fc989239493d |
| A6_all.bin | 0xC0004 | 8a8983975680f5df54a41bc1683f5387 | d8d39cb6320cc937471b3d7f32a838d90894f152f875c4014768a67356f952b1 |

### 18.1 SCI1 client: SP/A6 correspondence

OBSERVED: The common serial-client implementation spans SP 0x107A72-0x107DCF and A6 0x1094F2-0x10980F. The broader SP region continues through 0x108023. Ranges in this table are half-open.

| SP range | A6 range | Instruction counts SP/A6 | Behaviour |
|---|---|---:|---|
| 107A72-107B3C | 1094F2-1095A0 | 46/46 | Register/queue initialization and handler registration |
| 107B3C-107B78 | 1095A0-1095DC | 15/15 | RX dequeue; FFFF when empty |
| 107B78-107B82 | 1095DC-1095E6 | 4/4 | Blocking receive |
| 107B82-107BCA | 1095E6-10962A | 18/18 | TX enqueue; wait when full |
| 107BCA-107BEE | 10962A-109646 | 10/10 | Error interrupt handler |
| 107BEE-107C2E | 109646-10967A | 15/15 | Receive interrupt handler |
| 107C2E-107C86 | 10967A-1096BE | 19/19 | Transmit interrupt handler |
| 107C86-107CB8 | 1096BE-1096F0 | 19/19 | Probe/identification sequence |
| 107CB8-107CCA | 1096F0-109702 | 6/6 | Send 82 10 8E |
| 107CCA-107D22 | 109702-10975A | 29/29 | Identification exchange |
| 107D22-107D3C | 10975A-109774 | 10/10 | Send 99 argument 9E |
| 107D3C-107DD0 | 109774-109810 | 53/57 | Packed block write |

The first 191 instructions correspond one-for-one by ordinal position. Differences are relocated code/data addresses, equivalent shorter hardware-address encodings, and branch displacements adjusted for instruction lengths. For instruction-level address reconstruction, apply each delta from the listed SP instruction start until the next breakpoint:

```text
SP start  A6-SP delta
107A72    1A80
107ABA    1A7C
107AC0    1A78
107AC8    1A74
107AD0    1A70
107AD8    1A6C
107B1E    1A6A
107B26    1A68
107B2E    1A64
107BC4    1A60
107BD6    1A5C
107BE0    1A58
107BFA    1A54
107C1C    1A50
107C24    1A4C
107C3C    1A48
107C6A    1A44
107C70    1A40
107C78    1A3C
107C80    1A38
```

The last delta remains applicable through the common writer prefix at SP 107D7C / A6 1097B4.

All directly referenced client RAM follows A6 = SP - 0x35E:

| Object | SP | A6 |
|---|---:|---:|
| TX buffer, 2048 bytes | 40FAAA | 40F74C |
| RX buffer, 512 bytes | 4102AA | 40FF4C |
| RX producer word | 4104AA | 41014C |
| RX consumer word | 4104AC | 41014E |
| TX producer word | 4104AE | 410150 |
| TX consumer word | 4104B0 | 410152 |
| Receive-error byte | 4104B2 | 410154 |
| TX-associated flag byte | 4104B3 | 410155 |
| Identification bytes | 4104B4-4104B8 | 410156-41015A |

Unchanged initialization/protocol constants: selectors 0150/0154/0158 through 40020C; mode 00; baud-register 09; initial status 40; final control F0; interrupt-priority OR 20 at FFFFFECE; delay comparison 100; probe comparison 1000; RX mask 01FF; TX mask 07FF; empty result FFFF; error masks C7/38; receive-status mask 87; transmit-status mask 7F.

The identification request sends 9D 9E, expects 9D 05, stores five received bytes, and receives one additional byte. The probe also sends 82 10 8E and 99 7F 9E. No consumer established what the five identification bytes mean. Treat 05 as an observed framing value, not a hardware identity.

Packed writes send 90, three low-first seven-bit address chunks, groups of up to seven low-seven-bit payload bytes with a trailing high-bit bitmap, then 9E. Address masks are 7F, 00003F80 and 001FC000. No concrete caller-supplied 21-bit address was recovered.

Example equivalent encodings: SP 107AB4 uses 6AA8FFFFFF82 while A6 109534 uses 3882; both write R0L to FFFFFF82. SP 107B18 uses 6A28FFFFFECE while A6 109584 uses 6A08FECE. SP 107BBC uses an absolute bit-set form and A6 109620 uses 7F82 7070. These shorten the code but retain the same effective addresses/bit operations. Branch differences 107BB8:58600008 versus 10961C:58600004 and 107C4C:58700030 versus 109694:58700020 preserve corresponding conditions/destinations.

### 18.2 Packed-writer differences

OBSERVED: SP uses ER6 as total-byte counter, R5H as bitmap mask, R5L as payload and E5 as group counter. A6 uses ER5, R6L, R6H and E6 respectively. Both retain ER3 as requested length and R4L as bitmap.

The post-prefix correspondence is:

```text
SP       A6          operation
107D80   1097B8      clear total count
107D82   1097BA      mask = 1
107D84   1097BC      clear bitmap
107D86   1097BE      clear group count
107D88   1097C0      branch to group test
107D8A   1097C2      load source pointer
107D90   1097C8-D2   byte load / pointer advance
107D92   1097CA      save advanced pointer
107D98   1097D4      test payload bit 7
107D9A   1097D6      conditional skip
107D9C   1097D8      OR mask into bitmap
107D9E   1097DA      strip bit 7
107DA0   1097DC      TX argument
107DA2   1097DE      send payload
107DA6   1097E2      increment total
107DA8   1097E4      compare requested length
107DAA   1097E6      terminate group if reached
107DAC   1097E8-EC   shift mask
107DAE   1097EE      increment group count
107DB0   1097F0      compare group with 7
107DB4   1097F4      loop
107DB6   1097F6      bitmap argument
107DB8   1097F8      send bitmap
107DBC   1097FC      compare total
107DBE   1097FE      next group if needed
107DC0   109800      terminator 9E
107DC2   109802      send terminator
107DC6   109806      restore registers
107DCA   10980A      restore registers
107DCE   10980E      return
```

SP loads through postincrement at 107D90 and then saves the pointer. A6 increments ER0, saves it at 1097CA, decrements ER0 and loads at 1097D2. Thus A6 saves the advanced stack pointer field before reading the source byte; SP saves it afterward. SP shifts R5H directly; A6 moves R6L through R0L for its shift. Ordinary output is strongly inferred equivalent; instruction timing/intermediate state differs. Both enter the first byte group without a preceding zero-length guard.

### 18.3 A6 returns and missing SP read/control routines

OBSERVED: A6 bytes 10980E, 109810 and 109812 are each 54 70 (RTS). The first is the common writer's return. The next unrelated indexed ROM-pointer lookup begins at 109814 and corresponds structurally to SP 108024, with bases 16BD18 versus 161BA4.

SP has eight intervening routines:

| SP range, half-open | Behaviour |
|---|---|
| 107DD0-107E18 | One-byte read |
| 107E18-107E78 | Two-byte read |
| 107E78-107F18 | Four-byte read |
| 107F18-107F54 | Seven-bit word encoder |
| 107F54-107FA0 | 92 read-request sender |
| 107FA0-107FD6 | Receive/reconstruct payload |
| 107FD6-107FFC | 95 command sender |
| 107FFC-108024 | 96 command sender |

No raw 24-/32-bit references, relative call/branch candidates, or IDA xrefs were found targeting either A6 109810 or 109812. Exact SP-function-to-stub correspondence is UNRESOLVED. Mapping the last two SP command routines to the two returns is only a layout-based hypothesis. Empty API functions are plausible, but unreachable filler/alignment is not excluded. Do not label the returns established intentional API stubs.

No external absolute calls/jumps, external relative-call candidates or ordinary entry-pointer references into the A6 client region were identified. Direct queue/global accesses remain inside it. Computed/platform/debugger entry remains possible; missing IDA function definitions make xrefs alone insufficient. Peer/purpose remains unresolved: no demonstrated factory-test, programming, ESP, or Develop Monitor connection follows from this comparison.

STRONGLY INFERRED: The common implementation is shared source or directly derived source, not merely independently similar protocol code. The 191 instruction pairs, queue algorithms, register saves, probe loops, identification storage order, grouping/edge cases and uniform RAM relocation support that conclusion. Exact source text/compiler configuration is not established.

### 18.4 User-observed internal ATAPI format traffic

User supplied these physical observations:

```text
QUICK: WRITE(12) AA, LBA 21, count 9; WRITE(12) AA, LBA 0, count 1
FULL additionally: 04 10 20 00 00 00 00 00 00 00 00 00
Validation: READ(12) A8 at LBA 0 and around 20/21
```

Application correlation: 1058CC constructs disk/partition records; 1064DE initializes a nonempty partition. With P = partition start and F = table length in 512-byte blocks:

| Logical range | Structure |
|---|---|
| 0 | Disk header and four partition entries |
| P | Partition boot/geometry/filesystem header |
| P+1 through P+F | First allocation table |
| P+1+F through P+2F | Second allocation table |
| P+1+2F through P+2F+20 | 32-block root directory |
| P+1+2F+20 onward | Data area |

For P=20 and F=9: first table 21-29; second 2A-32; root directory 33-52; data starts 53. These are logical block addresses, not references to the target-indexed 28/2A command backend.

Block zero: 105918-105924 supplies FA at offset 0 and 55 AA at 1FE/1FF. Four 16-byte entries are copied at 1BE+16*i by 105C06-105C38, then block zero is written at 105C40-105C4C. Mount reads partition start at 1C6+16*i (1056E2-105702) and length at 1CA+16*i (1056B2-1056D4). 1062BA reads block zero and validates FA/55/AA. The internal path can try 40023C transformation and record its selection in 401012; the exact opaque transformation was not disassembled.

P is calculated rather than universally hardcoded to 20. 105990-1059B0 uses the intermediate geometry field at +14 as the initial partition start; 1069B8 obtains that field from context 401008. Value 32 yields P=20.

1064DE constructs the partition header in RAM 5E0200: E9 at +00; word 003E at +01; literal Roland followed by two spaces at +03; block size 0200 at +0B; 40 at +0D; reserved count 1 at +0E; table-copy count 2 at +10; directory quantity 0200 at +11; media marker F8 at +15; F at +16; TS25E label at +2B; FAT12 or FAT16 literal at +36; signature 55 AA at +1FE/+1FF. Numeric service conversion byte order was not independently recovered from unavailable service bodies in this pass. 106352 reads/validates the partition-start block and checks these signatures and numerical fields.

At 106604-106646, with N = partition length:

```text
q = floor(N/64)
q <= FF5: F = floor(3*q/1024)+1; choose FAT12 literal
q >  FF5: F = floor(q/256)+1; choose FAT16 literal
F = min(F,128)
```

F=9 in the small-table branch for N=174784 through 196607. Example N=196576 gives q=3071 and F=9; this is a calculation, not a recovered capacity measurement from the trace. The table buffer at 5D0000 is cleared for F*512 bytes at 106704-106724 and starts F8 FF FF (small branch) or F8 FF FF FF (large). 106764 calculates P+1; 106768 supplies F as the write count. FAT interpretation is strongly inferred from actual markers, duplicated tables, allocation arithmetic, literals and consumers together.

### 18.5 Internal routing, failed writes and false completion

For a routing entry whose low nibble is zero:

```text
1064DE -> 106030 -> 105FB2 -> 10601C: 4003AC
read: 105F54 -> 105ED6 -> 105F40: 4003A8
```

At the internal boundary ER0 supplies logical block address, R1L block count and the stack supplies buffer pointer. The physical observation supplies the AA/A8 packet correlation; packet construction is not visible in application code. The alternate target-indexed branch calls 12B496/12B2F6 and is unnecessary to explain this internal path.

Mount computes first/second table starts at 105778-105794. 10A0BC selects those starts and checks F8 FF FF at 10A138-10A16A, with a fourth FF required for the large-table branch. This connects validation reads at 21 to the first table.

Three independent error-handling gaps are relevant:

1. At 10601C application calls 4003AC, adjusts the stack, then forces R0=1 at 106022. The immediate opaque result is discarded. The outer checked wrapper subsequently uses 105E80, which returns success when 401000=0, 426BFD=0 and word 40101E=0. Whether a packet failure is translated into persistent application error state is UNRESOLVED.
2. If the first-table checked write reports zero, 106778-10677A branches to 106852 and returns zero, skipping second-table, root-directory and partition-header writes. 1058CC tests that result at 105BE0-105BE2, clears the affected 16-byte intermediate partition record on failure, but still reaches the block-zero write. This strongly explains a failed 21/count9 followed by 0/count1. It predicts a cleared partition entry in the attempted block-zero payload.
3. 14F71A ignores both optional preliminary-operation result (call at 14F726) and formatter result (call at 14F72E). An explicit completion path at 151EA2 calls 14F71A, later sets R0L=0 at 151EC8 and calls 1544F6 at 151ECA without a format-result/status test. Index zero selects descriptor 17BCEE, which points to text 17C149, Completed. No ASCII DONE literal was found; do not equate a particular observed display label with this text without further UI correlation.

A nonzero preliminary-operation argument selects 10580E. Its internal branch calls readiness check 105E80 and then 4003A0, 40039C, 4003B8, 4003A4 at 105872/10587A/105882/10588A, stopping on a zero result. Which call constructs physical packet 04 10 20 ... and what that packet does remain UNRESOLVED. Do not assign meaning from opcode 04 alone.

Highest-value physical check: compare the captured nine-block payload with the table prefix and inspect the final block-zero entry. This discriminates a reported first-write failure from a failure entirely swallowed by the baseline service.

### 18.6 ATA transfer infrastructure: startup correspondence

OBSERVED startup chain:

| Operation | SP | A6 |
|---|---:|---:|
| Initial jump target | 12CC54 | 131478 |
| Application RAM clear loop | 12CC68-12CC78 | 13148C-13149C |
| Initialized-data copy | 12CC7A-12CC9E | 13149E-1314C2 |
| Install four service jumps | 12CCC4 | 1314E8 |
| Application startup | 1258D8 | 128C74 |
| Early setup | 12CD7E | 1315A2 |
| Transfer/setup switching routine | 12BE62 | 12F96E |
| Normal storage initialization | 105420 | 107056 |
| Internal backend call | 10546E -> 400380 | 1070B0 -> 10058C |

Both clear 403000-42BFFF. SP copies 42D bytes from 17C454-17C880 to 403000-40342C; A6 copies 3AF bytes from 18325E-18360C to 403000-4033AE. Neither initializes low words 450 or 458. No zero/default value for those words follows from these ranges.

Jump-installation tables:

| Entry | SP target | A6 target |
|---|---:|---:|
| 400210 | 1309CA | 135818 |
| 400214 | 1309EE | 13583C |
| 400218 | 10589C | 107768 |
| 400364 | 128F52 | 12C54C |

SP 1309CA/1309EE set/clear bit 7 in RAM 426DCA and hardware E00083, preserving CCR/EXR around interrupt masking. These table writes do not initialize low descriptor words.

Both application startup paths execute opaque 400348(1) and 4002E0 before early setup. Production of descriptor offsets by these services is only a hypothesis. The terminal jump to 400200 in the entry routine is after the application-startup call; it is not demonstrated to execute before normal storage initialization, since normal application startup continues into its loop.

### 18.7 Common 400340/344/34C/350 startup protocol

SP 12CD94 calls 12BE62 with R0=0; A6 1315B8 calls 12F96E with R0=0. Both poll FFFFF0DF until bits 1/2 are clear and clear bytes FFFFFF07/03/02/05/04/06, then execute:

| Service | Argument | SP call | A6 call |
|---|---|---:|---:|
| 40034C | R0=0 | 12BE86 | 12F98C |
| 400350 | R0=0 | 12BE8C | 12F992 |
| 400344 | original argument, here zero | 12BE92 | 12F998 |
| 400340 | no freshly prepared argument | 12BE9A | 12F9A0 |
| 40034C | R0=1 | 12BEA2 | 12F9A8 |
| 400350 | R0=1 | 12BEAA | 12F9B0 |

Do not assume R0=0 at 400340: preceding 400344 may change it. Later early setup repeats 400350(1), then 40034C(1), at SP 12CDDA/12CDE0 and A6 131604/13160A. All occur before normal internal-device initialization. Same application-visible setup interface is strongly inferred; descriptor-table initialization inside these opaque calls is unresolved.

### 18.8 First A6 descriptor consumption precedes handler registration

Cold-path ordering:

```text
128CF0 clear 401001
128CF6 call 107056
1070AA clear 401000
1070B0 call 10058C
1005AA-1005B0 FFFFF0DF &= F9 (clear bits 1/2)
1005B6 clear 401078
1005BC inspect 401001
1005C4 clear bit 6 at FFFFFED3
1005CA call 100FA8
```

100FA8 reads word 450; 100FAC zero-extends it; 100FAE adds FF0000. 10101A reads word 458; 10101E zero-extends it; 101020 adds FF0000:

```text
D_A = FF0000 + zero_extend(word[450])
D_B = FF0000 + zero_extend(word[458])
```

The unsigned 16-bit offsets constrain bases to FF0000-FFFFFF but do not recover exact addresses or prove room for the full descriptor.

Initializer contents:

| Relative offset | Descriptor A | Descriptor B |
|---|---|---|
| +0 | byte 2B | byte 89 |
| +1..+3 | 60 00 00 | not supplied here |
| +4 | byte 00 | byte 00 |
| +5..+7 | not supplied here | 60 00 00 |
| +8 | word 0202 | word 0202 |
| +A | word 0040 | word 0040 |

It then configures transfer-related hardware including FFFFFFC1, FFFFFFE0 onward and FFFFFFE8=0050. SP writes FFFFFFE8/F8=0018 after its 400380 call at 105472-10547A; these later writes do not establish the pre-init infrastructure.

Only after first descriptor consumption does A6 register through 40020C:

| Selector | Handler | Call |
|---|---:|---:|
| 48 | 12641C | 100648 |
| A0 | 1264BC | 100654 |
| B0 | 1265CA | 100660 |

Therefore these registration calls cannot produce the offsets used by the first read. A6 expects the baseline/platform environment to have supplied them earlier.

### 18.9 Bounded reference census and compatibility verdict

No direct SP application access to 450/458 was found. A6 direct accesses found were reads, not initializers:

```text
450: 100FA8 100FB8 100FC8 100FD8 100FE8 100FF6 101008
     1010E2 1010FA 101116 101130 101142
     12650E 126526 126542 12655C 12656E
458: 10101A 10102A 10103A 10104A 10105A 101068 10107A
     1011A0 1011B8 1011D4 1011EE 101200
     126600 126618 126634 12664E 126660
```

This census does not exclude computed accesses or opaque platform initialization. Raw 0450/0458 occurrences in binary data are not automatically references.

SP explicit application 40020C registrations use F0, 4C, 150/154/158 and 144. No explicit 48/A0/B0 registration was identified. The known 4C registration is at 12A934, with handler 123864. Absence of registration does NOT establish vacancy; earlier platform setup may own resources.

The proposed relationship is arithmetically consistent:

```text
400 + 2*(A0/4) = 450
400 + 2*(B0/4) = 458
400 + 2*(48/4) = 424
400 + 2*(4C/4) = 426
```

Selector-associated descriptor-table interpretation remains HYPOTHESIZED, not established by this identity alone.

Verdict: SP provides closely matching application-side setup calls/order. Usable descriptor values, their producer, selector ownership and transfer-channel availability remain UNRESOLVED. Native ATA transfer compatibility is plausible but unverified. Neither absence of references nor matched setup calls justifies declaring the transplant safe.

### 18.10 Minimum instrumentation and next decisions

No firmware modification is required to resolve descriptor values:

1. Read 16-bit words 450 and 458 on SP immediately before 10546E.
2. Compute D_A/D_B and capture at least 12 bytes at each base, checking that the full range is addressable and does not wrap into another object.
3. Capture the equivalent A6 snapshot immediately before 100FA8.

A read-only debugger snapshot is sufficient for values. A hardware/bus capture may observe A6 reads at 100FA8 and 10101A if those transactions are externally visible. To identify the producer, hardware write watchpoints or bus logging from reset must capture writes to 450/458. To resolve resource ownership, inspect existing platform entries for 48/A0/B0 without registering replacements. Valid words alone do not establish selector/channel availability.

Highest-value transplant question: does SP's baseline environment populate the same descriptor infrastructure before 10546E, and who currently owns it? This is the remaining static-to-runtime boundary highlighted by the startup comparison.

## 19. Appended internal revision history

| Version | Date | Change |
|---|---|---|
| 1.1 | 2026-10-05 | Appended SCI1 instruction correspondence and bounded reachability findings; unresolved A6 return/stub identity; internal format-block layout and nine-block calculation; failure/completion control flow; SP/A6 startup and descriptor-consumption order; selector ownership limits and minimum read-only instrumentation. Preserved version 1.0 content. |
