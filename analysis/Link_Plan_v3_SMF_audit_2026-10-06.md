# Link Plan v3 BIN to Roland SMF audit

**OBSERVED — PASS at firmware-payload level.** The generated set is in
`firmware/LinkPlan_v3_SMF_20261005T233407Z_977451bb/deployment/`.
`manifest.json` beside that directory contains MD5/SHA-256 hashes, file sizes,
send order, packet counts, address ranges, headers and metadata for every
generated MIDI file, including diagnostic and round-trip sets. The ZIP contains
only the eight deployment files and their verification manifests.

**OBSERVED:** The existing candidate BIN and stock BIN were read only and checked
again after conversion. No firmware bytes, v3 patches, existing converters,
original archives or database were changed. The new reproducible audit/converter
is `analysis/smf_v3_deployment_audit.py`; run with `python -B`.

## Round-trip proof

**OBSERVED:** Each archive's eight MIDI files was decoded in numeric order into
a zero-initialized `0xC0004` byte array, honoring every packet address. Those
bytes were encoded back into the original SMF event templates, written to disk,
read again and decoded. A separate fresh process using a stream-based parser
and different bit-unpacking implementation independently repeated the decode.

| Input archive | Original SMFs → BIN → regenerated SMFs → BIN | Whole SMF byte identity |
|---|---|---|
| `SP808EXv1001.zip` | **OBSERVED: PASS**, exact equality to stock BIN | **OBSERVED: PASS**, all eight files byte-identical |
| `SP-808EX_v.1001_for_SP-808.zip` | **OBSERVED: PASS**, exact equality to stock BIN | **OBSERVED: FAIL**, four-byte track-length fields repaired in all eight files; all other bytes identical |

**OBSERVED:** Both recovered stock images are 786,436 bytes:

```text
MD5     d744a9cd4a2790ac68d165fd7849b5d8
SHA-256 e00235dd95d1f74f3ae27c463db9ed65b0800685073f9fb16ab0fc989239493d
```

**OBSERVED:** The original sets contain 2,605 data packets. Their transmitted
address union covers 510,090 bytes; the remaining 276,346 bytes are zero in the
stock BIN. The exact BIN equality depends on representing omitted addresses as
zeros; it does not establish that a physical updater clears those addresses.

**UNRESOLVED:** Original archive provenance beyond the checked repository files
and physical updater handling of omitted regions have not been independently
authenticated or exercised.

## Existing repository path

| Component | Result |
|---|---|
| `firmware/bin2midi.py` | **OBSERVED: FAIL** strict SMF parsing: SysEx VLQ length excludes `F7`, which is then written outside the event. SMF event length must include it, as the original valid files demonstrate. |
| `firmware/bin2midi.py` | **OBSERVED:** Invents eight `0x18000`-based parts and 252-byte packets rather than retaining the original sparse 196-byte packet layout. Adds four padding bytes to each of parts 1–7. Omits original timing/version/end metadata. |
| `firmware/rolandext.py` | **OBSERVED:** Opens output in append mode (`ab`), so `seek(memadd)` does not place writes at the addressed location. The legacy encoder/decoder round trip produces 786,464 bytes, not 786,436, and fails exact equality. |
| `firmware/rolandext.py` | **OBSERVED:** Rejects original data address `00 00 01`, expects zero memory-type prefixes where original metadata contains `00 00 01`, accepts only one header variant, and does not reconstruct sparse gaps. |
| `firmware/Bin2Mid.md` embedded example | **OBSERVED:** Describes a different header, address format and nibble-per-byte payload packing than the valid original EX update. It was not used. |

**OBSERVED:** The archive named `SP-808EX_v.1001_for_SP-808.zip` has stale
`MTrk` lengths in all eight files and predominantly `41 00 7C 12` headers,
with an additional `41 10 00 7C 12` header variant. `SP808EXv1001.zip` has
consistent `41 10 00 2B 12` headers and correct track lengths. The generated
deployment candidate therefore uses the latter valid template without model-ID
substitution.

**UNRESOLVED:** Whether a particular original SP-808 updater accepts the EX
`2B` model header, or requires the `7C` framing seen in the other archive, is
not proven by payload round trips. This set preserves the valid EX transport;
it is not a hardware acceptance claim for the SP-808 conversion procedure.

## Fields and ordering

| Field | Treatment and evidence |
|---|---|
| SMF header | **OBSERVED:** Preserve `MThd`, length 6, format 0, one track, division `0x0030` (48 ticks/quarter). |
| SMF track | **OBSERVED:** Recalculate `MTrk` byte length from emitted events. |
| Timing and meta events | **OBSERVED:** Preserve delta 16 for SysEx, delta 0 for meta events, tempo `07 A1 20` (500,000 µs/quarter), track names, copyright and `00 FF 2F 00` end-of-track. |
| Roland framing | **OBSERVED:** `F0` + VLQ length + `41 10 00 2B 12` + address(3) + memory address(5 nibble bytes) + payload + checksum + `F7`. Length includes `F7` and excludes `F0` and the VLQ itself. All interior bytes are seven-bit. |
| Firmware data address | **OBSERVED:** Preserve `00 00 01`; the five memory nibble bytes identify the BIN offset, not its `0x100000` runtime address. No separate per-packet ordinal is present in the observed packets. |
| Payload packing | **OBSERVED:** Seven binary bytes become seven low-seven-bit bytes followed by a mask byte. Mask bits 6 through 0 hold the corresponding MSBs. Original full packets contain 196 binary/224 encoded bytes. |
| Packet checksum | **OBSERVED:** Recompute `(-sum(address + memory nibbles + encoded payload)) & 0x7F`. The checksum-inclusive sum is zero modulo 128. Header and `F7` are excluded. Every emitted packet is checked. |
| File numbering | **OBSERVED:** Preserve `01 02 00` metadata: `[index 0..7, total-minus-one 7, flag]`; flag 0 begins the file and `7F` ends it. Preserve file order #1 through #8 and ascending packet addresses. |
| Memory parameters | **OBSERVED:** Only file #1 contains `01 00 00`, payload `000001 0000000000 000001 0c00000000` (grouped as 3-byte type, 5 nibble bytes, 3-byte type, 5 nibble bytes): type prefixes 1, start 0, size `0xC0000`. Preserve this despite the BIN's extra four bytes and original packets extending through `0xC0004`. |
| Version metadata | **OBSERVED:** Preserve `01 03 00` text `SP-808EX Ver 1.001 2000/01/01`; it identifies the inherited template and is not a new version assignment for v3. |
| Final metadata | **OBSERVED:** File #8 retains `01 01 00`, zero memory address, payload `4E`, packet checksum `30`. |
| Final metadata meaning | **UNRESOLVED:** `Rvs82bin.bas` explicitly describes this as a single unknown byte and ignores it; `rolandext.py` also ignores it. No demonstrated aggregate-checksum algorithm was found. Do not describe `4E` as a proven firmware checksum or claim that it is valid for altered payloads. It is preserved exactly, not recomputed. |

## Generated v3 payload

**OBSERVED:** The candidate was validated against the checked v3 manifest before
conversion. Existing covered packets are regenerated from its bytes. Its
previously omitted code island is transmitted by 25 additional packets in file
#8, before the original trailer packet and completion markers. The added range
is BIN `[0x7D000,0x7E298)`; the last packet contains 56 bytes. This includes
zero padding between code blocks and three trailing zero bytes to complete a
seven-byte group, all already present in the unchanged candidate BIN. No bytes
outside that BIN or beyond `0xC0004` are emitted. Every nonzero candidate byte
has an explicit transmitted packet.

**OBSERVED:** File #8 now contains 348 data packets; the entire set contains
2,630. The independent decode of all eight files reconstructs the candidate
exactly, not merely its changed ranges:

```text
size    786436
MD5     9d38db7f4cc07f00c30c6022e073ed7d
SHA-256 bcb3d71755dd8b5ca16275af9dc0e490126b9a248fd6794e689fc824c0c2b95a
```

**UNRESOLVED:** Physical MIDI transfer, updater model acceptance, opaque final
metadata semantics and execution of v3 have not been tested. The proof here is
exact firmware-payload transport and valid generated SMF framing.
