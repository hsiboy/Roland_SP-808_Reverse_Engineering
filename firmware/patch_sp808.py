#!/usr/bin/env python3
"""
SP-808 Firmware Patcher

Patches SP-808 firmware to accept any ATAPI device (not just Iomega ZIP drives).
The single-byte patch at 0x4B523 changes the device-type comparison value from
0x05 (ZIP) to 0xFF (impossible), causing the check to always fail and allowing
any device to pass.

Usage:
    python patch_sp808.py <input_firmware> <output_firmware>

Example:
    python patch_sp808.py SP8EXall.bin SP8EXall_patched.bin

After patching, convert back to MIDI and flash via:
    python bin2midi.py SP8EXall_patched.bin SP8EX_patched
"""

import sys
import hashlib


PATCHES = [
    {
        'name': 'Device Type Check',
        'offset': 0x4B523,
        'original': bytes([0x05]),
        'patch': bytes([0xFF]),
        'description': (
            'Changes device-type comparison from 0x05 (ZIP) to 0xFF (impossible value). '
            'The branch at 0x4B520 rejects any device not matching 0x05; making the '
            'comparison always false allows all ATAPI devices through.'
        ),
    }
]


def main():
    if len(sys.argv) != 3:
        print("Usage: python patch_sp808.py <input_firmware> <output_firmware>")
        print("Example: python patch_sp808.py SP8EXall.bin SP8EXall_patched.bin")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        with open(input_file, 'rb') as f:
            firmware = bytearray(f.read())
    except FileNotFoundError:
        print(f"Error: cannot find '{input_file}'")
        sys.exit(1)

    print(f"Loaded: {input_file} ({len(firmware)} bytes)")
    print(f"MD5 (original): {hashlib.md5(firmware).hexdigest()}")

    applied = 0
    for patch in PATCHES:
        offset = patch['offset']
        original = patch['original']
        new_value = patch['patch']

        actual = bytes(firmware[offset:offset + len(original)])
        if actual != original:
            print(f"\nWarning: patch '{patch['name']}' at 0x{offset:06X}")
            print(f"  Expected: {original.hex()}")
            print(f"  Found:    {actual.hex()}")
            answer = input("Apply anyway? (y/N): ").strip().lower()
            if answer != 'y':
                print("Skipping.")
                continue

        for i, byte in enumerate(new_value):
            firmware[offset + i] = byte

        print(f"\nApplied: {patch['name']}")
        print(f"  Offset:      0x{offset:06X}")
        print(f"  Original:    {original.hex()}")
        print(f"  Patched:     {new_value.hex()}")
        print(f"  Description: {patch['description']}")
        applied += 1

    if applied == 0:
        print("\nNo patches applied.")
        sys.exit(0)

    with open(output_file, 'wb') as f:
        f.write(firmware)

    print(f"\nWritten: {output_file}")
    print(f"MD5 (patched): {hashlib.md5(firmware).hexdigest()}")
    print("\nNext step: python bin2midi.py SP8EXall_patched.bin SP8EX_patched")


if __name__ == '__main__':
    main()
