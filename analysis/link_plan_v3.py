"""Build a Link Plan v3 specification and candidate image IN MEMORY only.

No patched firmware file is written. --write-plan writes Markdown/JSON plans.
The bounded H8S length decoder is checked against v2's 64 fixups/207 branches;
it is not a general disassembler or a hardware execution validator.
"""
from pathlib import Path
import hashlib
import json
import argparse
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
BASE = 0x100000
SP_MD5 = 'd744a9cd4a2790ac68d165fd7849b5d8'
A6_MD5 = '8a8983975680f5df54a41bc1683f5387'
BLOCKS = [(0x100578, 0x101436, 0x17D000), (0x12641C, 0x1266BC, 0x17DEBE)]
KEEP = [(0x100578, 0x100806), (0x100A58, 0x100D2A),
        (0x100F0E, 0x101436), (0x12641C, 0x1266BC)]
HELPERS = {0x126290: 0x12380A, 0x1262A2: 0x12381C,
           0x163122: 0x15833C, 0x16296C: 0x157B6A,
           0x135818: 0x1309CA, 0x13583C: 0x1309EE,
           0x15F4FE: 0x154CAE, 0x15F600: 0x154D9A}
PRIVATE = {0x4033E6: 0x4033AE, 0x4033E8: 0x4033B0,
           0x4033E9: 0x4033B1, 0x4033EA: 0x4033B2}


def hx(b): return b.hex(' ').upper()
def kept(a): return any(lo <= a < hi for lo, hi in KEEP)
def relocated(a):
    for lo, hi, dest in BLOCKS:
        if lo <= a < hi: return dest+a-lo
    raise ValueError(hex(a))


def decode_lengths(image):
    def length(a):
        i = a-BASE
        x, y = image[i:i+2]
        if x == 1:
            if y == 0x80: return 2
            z, w = image[i+2:i+4]
            if y in [0, 0x10, 0x20, 0x30, 0x40, 0x41]:
                if z == 0x78: return 10
                if z in [0x6E, 0x6F]: return 6
                if z in [0x6A, 0x6B]: return 8 if w >> 4 in [2, 10] else 6
                return 4
            return 4
        if x in [0x58, 0x5A, 0x5C, 0x5E, 0x6E, 0x6F, 0x79, 0x7B, 0x7C, 0x7D, 0x7E, 0x7F]: return 4
        if x in [0x6A, 0x6B]:
            h = y >> 4
            if h in [1, 9]: return 6
            if h in [3, 11]: return 8
            return 6 if h in [2, 10] else 4
        if x == 0x78: return 8
        if x == 0x7A: return 6
        return 2
    decoded = {}
    for lo, hi, _ in BLOCKS:
        a = lo
        while a < hi:
            n = length(a)
            decoded[a] = image[a-BASE:a-BASE+n]
            a += n
        assert a == hi
    return decoded


def relatives(decoded):
    result = []
    for a, r in decoded.items():
        if 0x40 <= r[0] <= 0x4F or r[0] == 0x55:
            t = a+2+int.from_bytes(r[1:2], 'big', signed=True)
        elif r[0] in [0x58, 0x5C]:
            t = a+4+int.from_bytes(r[2:4], 'big', signed=True)
        else: continue
        assert t in decoded
        result.append((a, t))
    return result


def census(decoded):
    fixups = []
    for a, r in decoded.items():
        if r[0] in [0x5E, 0x5A]: p, n = 1, 3
        elif r[0] == 0x7A and r[1] >> 4 == 0: p, n = 2, 4
        elif r[0] in [0x6A, 0x6B] and r[1] >> 4 in [2, 3, 10, 11]: p, n = 2, 4
        elif r[:3] == b'\x01\x00\x6B' and r[3] >> 4 in [2, 10]: p, n = 4, 4
        else: continue
        old = int.from_bytes(r[p:p+n], 'big')
        if old in HELPERS: kind, new = 'SP helper', HELPERS[old]
        elif old in PRIVATE: kind, new = 'private global', PRIVATE[old]
        elif any(lo <= old < hi for lo, hi, _ in BLOCKS): kind, new = 'copied code', relocated(old)
        else: continue
        replacement = r[:p]+new.to_bytes(n, 'big')+r[p+n:]
        fixups.append(dict(source=f'{a:06X}', relocated_site=f'{relocated(a):06X}',
                           operand_offset=p, operand_size=n,
                           donor_original_hex=hx(r), replacement_hex=hx(replacement),
                           old_target=f'{old:06X}', relocated_target=f'{new:06X}',
                           kind=kind, retained=kept(a), dependency=f'{kind}: {old:06X} -> {new:06X}',
                           evidence='OBSERVED operands; STRONGLY INFERRED integration',
                           rollback_link_step_hex=hx(r)))
    assert len(fixups) == 64
    assert Counter(f['kind'] for f in fixups) == {'copied code': 18, 'SP helper': 26, 'private global': 20}
    return fixups


def glue():
    rows, labels, branches = [], {}, []
    def emit(raw, asm):
        raw = bytes.fromhex(raw) if isinstance(raw, str) else raw
        a = 0x17E200+sum(len(r[1]) for r in rows)
        rows.append([a, raw, asm])
    def label(s): labels[s] = 0x17E200+sum(len(r[1]) for r in rows)
    def branch(op, name):
        branches.append((len(rows), name))
        emit(bytes([op, 0]), ('bra' if op == 0x40 else 'bne')+' '+name)
    def read_byte(a): emit(bytes([0x6A, 0x28])+a.to_bytes(4, 'big'), f'mov.b @{a:08X}:32,r0l')
    def read_status(): emit('6B 20 00 40 10 1E', 'mov.w @0040101E:32,r0')
    label('experiment')
    emit('18 88', 'sub.b r0l,r0l')
    emit('6A A8 00 40 10 01', 'mov.b r0l,@00401001:32 ; displaced cold-start clear')
    emit('5E 10 54 20', 'jsr @105420:24 ; bounded SP init shell')
    read_byte(0x401001)
    emit('A8 01', 'cmp.b #1,r0l')
    branch(0x46, 'identify_failed')
    read_status()
    branch(0x46, 'identify_failed')
    # One and only one read submission: LBA=0, sectors=1, buffer=5D0000.
    emit('7A 00 00 5D 00 00', 'mov.l #005D0000,er0')
    emit('01 00 6D F0', 'mov.l er0,@-er7 ; buffer argument')
    emit('1A 80', 'sub.l er0,er0 ; LBA 0')
    emit('F9 01', 'mov.b #1,r1l ; one sector')
    emit(bytes([0x5E])+relocated(0x100B2A).to_bytes(3, 'big'), f'jsr @{relocated(0x100B2A):06X}:24')
    emit('0B 97', 'adds #4,er7 ; remove buffer argument')
    label('read_wait')
    read_byte(0x401000)
    branch(0x46, 'read_wait')
    emit('6A 08 F0 DF', 'mov.b @FFFFF0DF:16,r0l')
    emit('E8 06', 'and.b #6,r0l')
    branch(0x46, 'read_wait')
    read_status()
    branch(0x46, 'read_failed')
    label('read_complete')
    branch(0x40, 'read_complete')
    label('identify_failed')
    branch(0x40, 'identify_failed')
    label('read_failed')
    branch(0x40, 'read_failed')
    for index, target in branches:
        a, raw, asm = rows[index]
        d = labels[target]-(a+2)
        assert -128 <= d <= 127 and not d & 1
        rows[index][1] = bytes([raw[0], d & 255])
    experiment = b''.join(r[1] for r in rows)
    assert len(experiment) <= 0x80
    cold = bytes.fromhex('1A 80 01 00 6B A0 00 40 33 AE 01 00 6B A0 00 40 33 B2')
    cold += bytes([0x5A])+relocated(0x10058C).to_bytes(3, 'big')
    return experiment, cold, rows, labels


def check_glue(rows, labels):
    """Check emitted test-control bytes with mocked A6 completion, not an ISA emulator."""
    code = {a: raw for a, raw, _ in rows}
    for initial_ready, initial_status, read_ok in [(0, 0, False), (0, 1, False),
                                                  (1, 1, False), (1, 0, False), (1, 0, True)]:
        init_ok = initial_ready == 1 and initial_status == 0
        pc, er0, r1l, z, read_calls, init_calls = 0x17E200, 0, 0, False, 0, 0
        stack, status, ready, polls = [], 0, 0, 0
        def value(a, n):
            nonlocal polls
            if a == 0x401001: return ready
            if a == 0x40101E: return status
            if a == 0x401000:
                polls += 1
                return 0x20 if polls == 1 else 0
            if a == 0xFFF0DF: return 2 if polls == 2 else 0
            raise AssertionError(hex(a))
        for _ in range(100):
            raw = code[pc]
            nxt = pc+len(raw)
            if raw == bytes.fromhex('18 88'): er0 &= ~255; z = True
            elif raw[:2] == bytes.fromhex('6A A8'): ready = er0 & 255
            elif raw[0] == 0x5E:
                target = int.from_bytes(raw[1:], 'big')
                if target == 0x105420:
                    init_calls += 1
                    ready, status = initial_ready, initial_status
                else:
                    assert target == relocated(0x100B2A)
                    assert init_ok and er0 == 0 and r1l == 1 and stack == [0x5D0000]
                    read_calls += 1
                    status = 0 if read_ok else 0x800E
            elif raw[:2] in [bytes.fromhex('6A 28'), bytes.fromhex('6B 20'), bytes.fromhex('6A 08')]:
                n = 2 if raw[0] == 0x6B else 1
                a = int.from_bytes(raw[2:], 'big')
                if len(raw) == 4: a |= 0xFF0000
                v = value(a & 0xFFFFFF, n)
                mask = (1 << (n*8))-1
                er0 = (er0 & ~mask) | v; z = not v
            elif raw == bytes.fromhex('A8 01'): z = (er0 & 255) == 1
            elif raw[:2] == bytes.fromhex('7A 00'): er0 = int.from_bytes(raw[2:], 'big'); z = not er0
            elif raw == bytes.fromhex('01 00 6D F0'): stack.append(er0)
            elif raw == bytes.fromhex('1A 80'): er0 = 0; z = True
            elif raw == bytes.fromhex('F9 01'): r1l = 1; z = False
            elif raw == bytes.fromhex('0B 97'): stack.pop()
            elif raw == bytes.fromhex('E8 06'): er0 = (er0 & ~255) | (er0 & 6); z = not (er0 & 255)
            elif raw[0] in [0x40, 0x46]:
                if raw[0] == 0x40 or not z:
                    nxt += int.from_bytes(raw[1:], 'big', signed=True)
                    if nxt == pc:
                        expected = 'identify_failed' if not init_ok else 'read_complete' if read_ok else 'read_failed'
                        assert pc == labels[expected] and read_calls == int(init_ok) and init_calls == 1
                        assert not stack
                        break
            else: raise AssertionError(raw.hex())
            pc = nxt
        else: raise AssertionError('glue did not park')


def build():
    sp = (ROOT/'firmware/SP8EXall.bin').read_bytes()
    a6 = (ROOT/'firmware/A6_all.bin').read_bytes()
    assert hashlib.md5(sp).hexdigest() == SP_MD5
    assert hashlib.md5(a6).hexdigest() == A6_MD5
    d = decode_lengths(a6)
    rel = relatives(d)
    assert len(rel) == 207
    retained_rel = [(a, t) for a, t in rel if kept(a)]
    assert all(kept(t) and relocated(t)-relocated(a) == t-a for a, t in retained_rel)
    fixes = census(d)
    kept_fixes = [f for f in fixes if f['retained']]
    assert len(kept_fixes) == 45
    assert all(f['kind'] != 'copied code' or kept(int(f['old_target'], 16)) for f in kept_fixes)
    for src, target, size in [(0x16296C, 0x157B6A, 0x3C), (0x163122, 0x15833C, 0x18)]:
        assert a6[src-BASE:src-BASE+size] == sp[target-BASE:target-BASE+size]
    candidate = bytearray(sp)
    mutations = []
    def mutation(site, new, dependency, evidence, donor=None):
        old = sp[site-BASE:site-BASE+len(new)]
        assert len(old) == len(new)
        candidate[site-BASE:site-BASE+len(new)] = new
        row = dict(site=f'{site:06X}', relocated_target=f'{site:06X}', file_offset=f'{site-BASE:06X}', length=len(new),
                   original_sp_hex=hx(old), replacement_hex=hx(new),
                   dependency=dependency, evidence=evidence, rollback_hex=hx(old),
                   rollback='Restore original_sp_hex; restore ALL plan spans, then cold power cycle')
        if donor: row['donor_range'] = donor
        mutations.append(row)
    for lo, hi in KEEP:
        dest = relocated(lo)
        payload = bytearray(a6[lo-BASE:hi-BASE])
        for f in kept_fixes:
            src = int(f['source'], 16)
            if lo <= src < hi:
                raw = bytes.fromhex(f['replacement_hex'])
                payload[src-lo:src-lo+len(raw)] = raw
                f['original_sp_hex'] = hx(sp[relocated(src)-BASE:relocated(src)-BASE+len(raw)])
                f['rollback_sp_hex'] = f['original_sp_hex']
        assert not any(sp[dest-BASE:dest-BASE+len(payload)])
        mutation(dest, payload, 'V2 affine placement; retained read-only experiment closure',
                 'OBSERVED source bytes and zero destination; HYPOTHESIZED experiment integration',
                 f'{lo:06X}-{hi:06X} exclusive end')
    experiment, cold, rows, labels = glue()
    check_glue(rows, labels)
    for site, payload, name in [(0x17E200, experiment, 'Boot-only cold init + one read + interrupt-enabled park'),
                                 (0x17E280, cold, 'Clear established eight private bytes; tail-enter A6 cold init')]:
        assert not any(sp[site-BASE:site-BASE+len(payload)])
        mutation(site, payload, name, 'HYPOTHESIZED test glue; exact emitted bytes')
    splices = [
        (0x125910, '79 00 00 81', '5A 17 E2 00', '17E200', 'Stop normal startup before diagnostic/filesystem routing'),
        (0x10546E, '5E 40 03 80', '5E 17 E2 80', '17E280', 'Replace internal backend cold-init call; A6 10058C -> 17D014'),
        (0x105472, '79 00 00 18 6B 80 FF E8 6B 80 FF F8', '79 00 00 50 6B 80 FF E8 6B 80 FF F8', 'FFFFE8/FFFFF8', 'Preserve A6 TGR1A/TGR2A=0050 after cold init'),
        (0x10547E, '6B 20 00 40 10 1E', '5A 10 55 62 00 00', '105562', 'Return through existing epilogue; skip legacy enumeration/4003B4'),
        (0x146DE2, '7A 05 00 40 33 AE', '7A 05 00 17 C8 02', '17C802', 'Reclaim private globals by reading callbacks from ROM initializer'),
    ]
    for site, expected, replacement, target, dependency in splices:
        assert sp[site-BASE:site-BASE+len(bytes.fromhex(expected))] == bytes.fromhex(expected)
        mutation(site, bytes.fromhex(replacement), dependency,
                 'OBSERVED SP bytes; STRONGLY INFERRED resource fix' if site in [0x105472, 0x146DE2]
                 else 'HYPOTHESIZED experiment control glue; OBSERVED splice boundaries')
        mutations[-1]['relocated_target'] = target
    # Exact low-vector reads and descriptor initializer are never rewritten.
    vector_reads = []
    for src, raw in d.items():
        if raw in [bytes.fromhex('6B 00 04 50'), bytes.fromhex('6B 00 04 58')]:
            dest = relocated(src)
            assert candidate[dest-BASE:dest-BASE+len(raw)] == raw
            vector_reads.append(dict(source=f'{src:06X}', relocated=f'{dest:06X}', bytes=hx(raw)))
    assert len(vector_reads) == 34
    lo, hi = 0x100FA8, 0x1010C4
    assert candidate[relocated(lo)-BASE:relocated(hi)-BASE] == a6[lo-BASE:hi-BASE]
    # Forbidden command roots/format block remain original SP padding zeros.
    for lo, hi in [(0x100806, 0x100A58), (0x100D2A, 0x100F0E)]:
        assert not any(candidate[relocated(lo)-BASE:relocated(hi)-BASE])
    # Layout mutation spans are disjoint; per-instruction fixups are annotations.
    covered = set()
    for r in mutations:
        span = set(range(int(r['site'], 16), int(r['site'], 16)+r['length']))
        assert not covered.intersection(span)
        covered.update(span)
    rolled = bytearray(candidate)
    for r in mutations:
        site = int(r['site'], 16)-BASE
        rolled[site:site+r['length']] = bytes.fromhex(r['rollback_hex'])
    assert bytes(rolled) == sp
    return dict(plan='Link Plan v3 - cold init/IDENTIFY + one 512-byte read, no routing',
                input_sp_md5=SP_MD5, input_a6_md5=A6_MD5,
                candidate_md5=hashlib.md5(candidate).hexdigest(),
                candidate_sha256=hashlib.sha256(candidate).hexdigest(),
                candidate_size=len(candidate), candidate_written=False,
                generation_blockers=[], runtime_validation='UNRESOLVED; experimental, not a safe release',
                fixup_counts=dict(Counter(f['kind'] for f in kept_fixes)),
                retained_relative_count=len(retained_rel), v2_relative_count=207,
                mutations=mutations, fixups=kept_fixes,
                retired_v2_fixups=[f for f in fixes if not f['retained']],
                unchanged_dtc_vector_reads=vector_reads,
                glue_labels={k:f'{v:06X}' for k,v in labels.items()},
                glue_listing=[dict(address=f'{a:06X}', bytes=hx(raw), instruction=asm) for a,raw,asm in rows])


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--write-plan', action='store_true')
    args = p.parse_args()
    plan = build()
    if args.write_plan:
        (ROOT/'analysis/Link_Plan_v3_manifest_2026-10-05.json').write_text(json.dumps(plan, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k:v for k,v in plan.items() if k not in ['mutations','fixups','retired_v2_fixups','unchanged_dtc_vector_reads','glue_listing']}, indent=2))


if __name__ == '__main__': main()
