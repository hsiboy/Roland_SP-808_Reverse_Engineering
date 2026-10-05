"""Emit a REVIEW-ONLY H8S snapshot listing; never patch an image.

Default DRAM address 43C000 is an UNPROVEN example, NOT a safe reservation.
Instruction encodings follow GNU h8300.h and the H8S manuals.
Run with --self-test for byte-level/model checks; no hardware validation.
"""
from pathlib import Path
import hashlib
import argparse

BASE = 0x100000
HOOK = 0x12CC54
CAVE = 0x1B0000
EXAMPLE_DEST = 0x43C000
SIZE = 0xA38
MD5 = 'd744a9cd4a2790ac68d165fd7849b5d8'


def build(dest=EXAMPLE_DEST, cave=CAVE):
    if dest & 1 or not 0x400000 <= dest <= 0x600000 - SIZE:
        raise ValueError('Need an even DRAM candidate; range is not ownership proof')
    rows, labels, fixups = [], {}, []
    def emit(raw, asm):
        raw = bytes.fromhex(raw) if isinstance(raw, str) else raw
        rows.append([cave + sum(len(r[1]) for r in rows), raw, asm])
    def addr(a): return a.to_bytes(4, 'big')
    def long_store(reg, off):
        emit(bytes([1, 0, 0x6B, 0xA0 | reg]) + addr(dest + off),
             f'mov.l er{reg}, @{dest+off:08X}:32')
    def long_load(reg, off):
        emit(bytes([1, 0, 0x6B, 0x20 | reg]) + addr(dest + off),
             f'mov.l @{dest+off:08X}:32, er{reg}')
    def control(op, cr, off):
        emit(bytes([1, 0x40 | cr, 0x6B, 0xA0 if op == 'stc' else 0x20])
             + addr(dest + off), f'{op}.w {"ccr" if cr == 0 else "exr"}, @{dest+off:08X}:32'
             if op == 'stc' else f'ldc.w @{dest+off:08X}:32, {"ccr" if cr == 0 else "exr"}')
    def immediate(reg, value):
        emit(bytes([0x7A, reg]) + addr(value), f'mov.l #{value:08X}, er{reg}')
    def byte_read(a, name):
        if a >= 0xFFFF00:
            emit(bytes([0x28, a & 255]), f'mov.b @{name}:8, r0l')
        else:
            emit(bytes([0x6A, 8]) + (a & 65535).to_bytes(2, 'big'),
                 f'mov.b @{name}:16, r0l')
    def byte_append():
        emit('68 D8', 'mov.b r0l, @er5')
        emit('0B 05', 'adds #1, er5')
    def branch(op, target):
        fixups.append((len(rows), target))
        emit(bytes([op, 0]), f'{"beq" if op == 0x47 else "bne"} {target}')
    def label(name): labels[name] = cave + sum(len(r[1]) for r in rows)
    def eep(name):
        label(name)
        emit('7B D4 59 8F', 'eepmov.w')
        emit('0D 44', 'mov.w r4, r4')
        branch(0x46, name)  # Resume remaining bytes if NMI interrupted the move.

    # No register/flag/stack modification before saving the original CCR.
    control('stc', 0, 0xA04)
    emit('04 C0', 'orc #C0, ccr')
    control('stc', 1, 0xA06)
    emit('01 41 04 07', 'orc #07, exr')
    for reg, off in [(0, 0xA08), (4, 0xA0C), (5, 0xA10), (6, 0xA14), (7, 0xA00)]:
        long_store(reg, off)

    # Header/peripherals sampled before the two bulk memory moves.
    immediate(5, dest + 0xA18)
    for a, name in [(0xFFFF39, 'SYSCR'), (0xFFFEC1, 'ICRB'),
                    (0xFFFEC9, 'IPRF'), (0xFFFECA, 'IPRG'),
                    (0xFFFF31, 'DTCERB'), (0xFFFF32, 'DTCERC'),
                    (0xFFFFC0, 'TSTR')]:
        byte_read(a, name)
        byte_append()
    emit('F8 00', 'mov.b #00, r0l')
    byte_append()  # D+A1F status=0, then ER5=D+A20.
    immediate(6, 0xFFFFE0)
    emit('79 08 00 02', 'mov.w #0002, e0 ; two TPU channels')
    label('tpu_channel')
    emit('FC 03', 'mov.b #03, r4l')
    emit('7B 5C 59 8F', 'eepmov.b ; TCRn/TMDRn/TIORn, three byte reads')
    emit('0B 06', 'adds #1, er6 ; skip reserved FFFFE3/FFFFF3')
    emit('F8 00', 'mov.b #00, r0l')
    byte_append()  # Output reserved slot is zero, never read from I/O.
    emit('FC 02', 'mov.b #02, r4l')
    emit('7B 5C 59 8F', 'eepmov.b ; TIERn/TSRn, two byte reads')
    emit('79 04 00 03', 'mov.w #0003, r4')
    label('tpu_words')
    emit('6D 60', 'mov.w @er6+, r0 ; TCNTn/TGRnA/TGRnB')
    emit('69 D0', 'mov.w r0, @er5')
    emit('0B 85', 'adds #2, er5')
    emit('1B 54', 'dec.w #1, r4')
    branch(0x46, 'tpu_words')
    emit('0B 96', 'adds #4, er6 ; next channel at +10')
    emit('1B 58', 'dec.w #1, e0')
    branch(0x46, 'tpu_channel')

    immediate(5, dest)
    emit('1A E6', 'sub.l er6, er6')
    emit('79 04 06 00', 'mov.w #0600, r4')
    eep('copy_rom')
    emit(bytes([0x6A, 0x28]) + addr(dest + 0xA18), f'mov.b @{dest+0xA18:08X}:32, r0l')
    emit('73 08', 'btst #0, r0l')
    # BEQ must observe BTST directly: an intervening MOV would replace Z.
    branch(0x47, 'ram_disabled')
    immediate(6, 0xFFF800)
    emit('79 04 04 00', 'mov.w #0400, r4')
    eep('copy_ram')  # ER5 is D+600 following copy_rom.
    emit('F8 02', 'mov.b #02, r0l')
    branch(0x40, 'commit')
    label('ram_disabled')
    emit('F8 01', 'mov.b #01, r0l')
    label('commit')
    emit(bytes([0x6A, 0xA8]) + addr(dest + 0xA1F), f'mov.b r0l, @{dest+0xA1F:08X}:32')
    for reg, off in [(0, 0xA08), (4, 0xA0C), (5, 0xA10), (6, 0xA14)]:
        long_load(reg, off)
    control('ldc', 1, 0xA06)
    control('ldc', 0, 0xA04)
    emit('01 20 6D F0', 'stm.l er0-er2, @-er7 ; displaced original instruction')
    emit(bytes([0x5A]) + (HOOK + 4).to_bytes(3, 'big'), f'jmp @{HOOK+4:06X}:24')
    for index, target in fixups:
        a, raw, asm = rows[index]
        displacement = labels[target] - (a + 2)
        assert -128 <= displacement <= 127 and displacement % 2 == 0
        rows[index][1] = bytes([raw[0], displacement & 255])
        if raw[0] == 0x40:
            rows[index][2] = f'bra {target}'
    blob = b''.join(r[1] for r in rows)
    splice = bytes([0x5A]) + cave.to_bytes(3, 'big')
    return rows, blob, splice


def validate_image(blob):
    image = (Path(__file__).resolve().parents[1] / 'firmware/SP8EXall.bin').read_bytes()
    assert hashlib.md5(image).hexdigest() == MD5
    assert image[HOOK-BASE:HOOK-BASE+4] == bytes.fromhex('01 20 6D F0')
    assert not any(image[CAVE-BASE:CAVE-BASE+len(blob)])
    return image


def model_check(dest):
    """Narrow byte interpreter, not an independent H8S CPU/ISA validator.

    Checks output bounds, raw word captures, flag-dependent branches, state
    restoration, no snapshot stack writes, and EEPMOV remaining-count retry.
    Assumes any simulated NMI preserves the working registers.
    """
    rows, blob, _ = build(dest)
    instruction = {a: raw for a, raw, _ in rows}
    peripherals = [0xFFFF39, 0xFFFEC1, 0xFFFEC9, 0xFFFECA,
                   0xFFFF31, 0xFFFF32, 0xFFFFC0]
    for a in [0xFFFFE0, 0xFFFFF0]:
        peripherals += [a+i for i in [0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11]]
    for rame in [0, 1]:
        for interrupt_move in [False, True]:
            mem = {a: (a*17+3) & 255 for a in range(0x600)}
            mem.update({a: (a*13+9) & 255 for a in range(0xFFF800, 0xFFFC00)})
            mem.update({a: (a*7+5) & 255 for a in peripherals})
            mem[0xFFFF39] = 0x30 | rame
            original_rom = bytes(mem[a] for a in range(0x600))
            original_ram = bytes(mem[a] for a in range(0xFFF800, 0xFFFC00))
            original_peripheral = dict((a, mem[a]) for a in peripherals)
            mem.update({dest+i: 0xAA for i in range(SIZE)})
            er = [0x13579B00+i*0x10001 for i in range(8)]
            er[7] = 0xFFF900
            original_er = er[:]
            ccr, exr = 0x25, 0x02
            original_ccr, original_exr = ccr, exr
            writes, reads = [], []
            pc, moved_partial, steps = CAVE, False, 0
            def read(a, n):
                a &= 0xFFFFFF
                reads.extend(range(a, a+n))
                return int.from_bytes(bytes(mem[a+i] for i in range(n)), 'big')
            def write(a, n, v):
                a &= 0xFFFFFF
                writes.extend(range(a, a+n))
                for i, x in enumerate((v & ((1 << (8*n))-1)).to_bytes(n, 'big')):
                    mem[a+i] = x
            def flags(v, width):
                nonlocal ccr
                ccr = (ccr & ~0x0E) | (4 if not v else 0) | (8 if v & (1 << (width-1)) else 0)
            while True:
                steps += 1
                assert steps < 500
                raw = instruction[pc]
                next_pc = pc+len(raw)
                if raw == b'\x01\x41\x04\x07': exr |= 7
                elif raw[:2] in [b'\x01\x40', b'\x01\x41']:
                    cr = raw[1] & 1
                    a = int.from_bytes(raw[4:], 'big')
                    if raw[3] == 0xA0:
                        v = exr if cr else ccr
                        write(a, 2, v*0x101)
                    elif cr:
                        exr = read(a, 2) >> 8
                    else:
                        ccr = read(a, 2) >> 8
                elif raw == b'\x04\xC0': ccr |= 0xC0
                elif raw[:2] == b'\x01\x00':
                    r = raw[3] & 7
                    a = int.from_bytes(raw[4:], 'big')
                    if raw[3] & 0x80: write(a, 4, er[r])
                    else: er[r] = read(a, 4)
                    flags(er[r], 32)
                elif raw[0] == 0x7A:
                    er[raw[1]] = int.from_bytes(raw[2:], 'big')
                    flags(er[raw[1]], 32)
                elif raw[0] == 0x28:
                    v = read(0xFFFF00 | raw[1], 1)
                    er[0] = (er[0] & ~255) | v
                    flags(v, 8)
                elif raw[:2] in [b'\x6A\x08', b'\x6A\x28']:
                    a = int.from_bytes(raw[2:], 'big')
                    if len(raw) == 4: a |= 0xFF0000
                    v = read(a, 1)
                    er[0] = (er[0] & ~255) | v
                    flags(v, 8)
                elif raw[0] in [0xF8, 0xFC]:
                    r = raw[0] - 0xF8
                    er[r] = (er[r] & ~255) | raw[1]
                    flags(raw[1], 8)
                elif raw == b'\x68\xD8':
                    write(er[5], 1, er[0] & 255)
                    flags(er[0] & 255, 8)
                elif raw[:2] == b'\x6A\xA8':
                    write(int.from_bytes(raw[2:], 'big'), 1, er[0] & 255)
                    flags(er[0] & 255, 8)
                elif raw[0] == 0x0B:
                    r = raw[1] & 7
                    er[r] += {0: 1, 0x80: 2, 0x90: 4}[raw[1] & 0xF0]
                elif raw[:2] == b'\x6B\x00':
                    v = read(0xFF0000 | int.from_bytes(raw[2:], 'big'), 2)
                    er[0] = (er[0] & ~65535) | v
                    flags(v, 16)
                elif raw == b'\x69\xD0':
                    write(er[5], 2, er[0] & 65535)
                    flags(er[0] & 65535, 16)
                elif raw == b'\x6D\x60':
                    v = read(er[6], 2)
                    er[6] += 2
                    er[0] = (er[0] & ~65535) | v
                    flags(v, 16)
                elif raw == b'\x1A\xE6': er[6] = 0; flags(0, 32)
                elif raw[:2] in [b'\x79\x04', b'\x79\x08']:
                    v = int.from_bytes(raw[2:], 'big')
                    if raw[1] == 4: er[4] = (er[4] & ~65535) | v
                    else: er[0] = (er[0] & 65535) | (v << 16)
                    flags(v, 16)
                elif raw in [b'\x1B\x54', b'\x1B\x58']:
                    if raw[1] == 0x54:
                        v = ((er[4] & 65535)-1) & 65535
                        er[4] = (er[4] & ~65535) | v
                    else:
                        v = ((er[0] >> 16)-1) & 65535
                        er[0] = (er[0] & 65535) | (v << 16)
                    flags(v, 16)
                elif raw in [b'\x7B\xD4\x59\x8F', b'\x7B\x5C\x59\x8F']:
                    mask = 65535 if raw[1] == 0xD4 else 255
                    count = er[4] & mask
                    n = count
                    if raw[1] == 0xD4 and interrupt_move and not moved_partial:
                        n = 17
                        moved_partial = True
                    for i in range(n): write(er[5]+i, 1, read(er[6]+i, 1))
                    er[5] += n; er[6] += n
                    er[4] = (er[4] & ~mask) | (count-n)
                elif raw == b'\x0D\x44': flags(er[4] & 65535, 16)
                elif raw == b'\x73\x08':
                    ccr = (ccr & ~4) | (0 if er[0] & 1 else 4)
                elif raw[0] in [0x40, 0x46, 0x47]:
                    take = raw[0] == 0x40 or (raw[0] == 0x47) == bool(ccr & 4)
                    if take: next_pc += int.from_bytes(raw[1:], 'big', signed=True)
                elif raw == bytes.fromhex('01 20 6D F0'):
                    # Verify immediately BEFORE replaying the original stack write.
                    assert er == original_er and ccr == original_ccr and exr == original_exr
                    assert all(dest <= a < dest+SIZE for a in writes)
                    assert not any(a in [0xFFFFE3, 0xFFFFF3] for a in reads)
                    assert bytes(mem[dest+i] for i in range(0x600)) == original_rom
                    if rame:
                        assert bytes(mem[dest+0x600+i] for i in range(0x400)) == original_ram
                    else:
                        assert all(mem[dest+0x600+i] == 0xAA for i in range(0x400))
                    assert read(dest+0xA00, 4) == original_er[7]
                    assert mem[dest+0xA1F] == (2 if rame else 1)
                    assert all(mem[a] == v for a, v in original_peripheral.items())
                    for i, a in enumerate(peripherals[:7]):
                        assert mem[dest+0xA18+i] == original_peripheral[a]
                    for base, out in [(0xFFFFE0, 0xA20), (0xFFFFF0, 0xA2C)]:
                        for i in [0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11]:
                            assert mem[dest+out+i] == original_peripheral[base+i]
                        assert mem[dest+out+3] == 0
                    break
                else: raise AssertionError(raw.hex())
                pc = next_pc
    print('MODEL CHECKS PASSED: RAME on/off; uninterrupted/interrupted EEPMOV; state/write bounds')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dest', type=lambda s: int(s, 0), default=EXAMPLE_DEST)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    rows, blob, splice = build(args.dest)
    validate_image(blob)
    if args.self_test:
        model_check(args.dest)
    print('UNPROVEN DRAM CANDIDATE; REVIEW ONLY; DO NOT APPLY')
    print(f'D={args.dest:06X}; footprint={SIZE:X}; stub={len(blob)} bytes; splice={splice.hex(" ")}')
    for a, raw, asm in rows:
        print(f'{a:06X}  {raw.hex(" "):<26}  {asm}')
    print('Full stub hex:')
    for i in range(0, len(blob), 16):
        print(blob[i:i+16].hex(' '))


if __name__ == '__main__':
    main()
