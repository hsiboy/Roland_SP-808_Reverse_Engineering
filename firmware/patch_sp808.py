#!/usr/bin/env python3
"""
SP-808 Firmware Patcher

Patches SP-808 firmware to accept any classified ATAPI device, not just
Iomega ZIP drives (device type 1).

Background
----------
The device classifier (sub_12AE88 / device_classifier) reads the drive's
IDENTIFY response and writes a type code to external RAM at 0x426C82:

    1 = ZIP  (IOMEGA vendor string matched)
    2 = HDD, geometry < 0x951229
    3 = HDD, geometry >= 0x951229

After classification, device_probe (sub_12A956) gates on that type code at
IDA address 0x12AA12:

    cmp.b  #1, r0l       ; 0x12AA12 - is it ZIP?
    bne    loc_12AA26    ; 0x12AA14 - reject if not

Only type 1 (ZIP) reaches the success/init path. Types 2 and 3 are silently
rejected.


device_probe (sub_12A956)
    ├── Zero device_type_by_slot[slot]
    ├── Zero slot_flag_A, slot_flag_B, slot_device_flags, slot_flag_D, slot_flag_E, slot_media_accepted
    ├── Check ide_init_done → 0x8001 + abort if not ready
    ├── atapi_cmd_sequence_full (sub_12AA72)   ; SZHC table from entry 0 (06 00...)
    ├── atapi_cmd_sequence_partial (sub_12AAF2) ; SZHC table from entry 1 (START/STOP UNIT)
    ├── Check device_status_reg == 0x8003 → abort if no device
    ├── atapi_cmd_sequence_full (sub_12AA72)   ; repeat full sequence
    ├── device_classifier                       ; assigns type 1/2/3 to device_type_by_slot[slot]
    ├── Check slot_device_flags & 0x1F
    │       0 → read device_type_by_slot[slot]
    │               == 1 → set slot_media_accepted = 2, e5 = 1 → proceed
    │               != 1 → clear slot_media_accepted → abort   ← PATCH TARGET 0x2AA14
    │       5 → clear slot_media_accepted → abort
    │       other → clear slot_media_accepted → abort
    └── If slot_media_accepted set (e5 == 1):
            atapi_cmd_sequence_full (sub_12AA72)
            atapi_cmd_sequence_partial (sub_12AAF2)
            zip_device_init (sub_12B150)        ; needs investigation for HDD compat
            zero device_status_reg
            return 1 (success)
        else:
            return 0 (failure)

            NOTE: The name zip_device_init is just a placeholder - it may need to do different things for HDD vs ZIP, which is probably the next thing to investigate once the patch is tested.
The patch
---------
Change the conditional branch at 0x12AA14 from:

    bne  loc_12AA26   ; 46 10  - branch away if not ZIP

to:

    bra  loc_12AA16   ; 40 00  - always fall through to success path

This allows any classified device (types 1, 2, 3) to proceed, regardless
of whether it matched the IOMEGA vendor string.

File offset: IDA address 0x12AA14 - load base 0x100000 = 0x2AA14

Usage
-----
    python patch_sp808.py <input_firmware> <output_firmware>

Example
-------
    python patch_sp808.py SP8EXall.bin SP8EXall_patched.bin

After patching, convert back to MIDI SysEx and flash via:
    python bin2midi.py SP8EXall_patched.bin SP8EX_patched
"""

import sys
import hashlib


PATCHES = [
    {
        'name': 'Device type gate (device_probe)',
        'offset': 0x2AA14,
        'original': bytes([0x46, 0x10]),
        'patch':    bytes([0x40, 0x00]),
        'description': (
            'At IDA 0x12AA14, changes "bne loc_12AA26" (46 10) to '
            '"bra loc_12AA16" (40 00). '
            'Removes the ZIP-only gate in device_probe so that HDD device '
            'types 2 and 3 (assigned by device_classifier) proceed to the '
            'device init path instead of being silently rejected.'
        ),
    },
]

KNOWN_MD5 = 'd744a9cd4a2790ac68d165fd7849b5d8'  # SP8EXall.bin (786,436 bytes)


def md5(data):
    return hashlib.md5(data).hexdigest()


def main():
    if len(sys.argv) != 3:
        print("Usage: python patch_sp808.py <input_firmware> <output_firmware>")
        print("Example: python patch_sp808.py SP8EXall.bin SP8EXall_patched.bin")
        sys.exit(1)

    input_file  = sys.argv[1]
    output_file = sys.argv[2]

    try:
        with open(input_file, 'rb') as f:
            firmware = bytearray(f.read())
    except FileNotFoundError:
        print(f"Error: cannot find '{input_file}'")
        sys.exit(1)

    print(f"Loaded:       {input_file} ({len(firmware):,} bytes)")
    actual_md5 = md5(firmware)
    print(f"MD5 original: {actual_md5}")

    if actual_md5 != KNOWN_MD5:
        print(f"\nWarning: MD5 does not match known good firmware.")
        print(f"  Expected: {KNOWN_MD5}")
        print(f"  Found:    {actual_md5}")
        answer = input("Continue anyway? (y/N): ").strip().lower()
        if answer != 'y':
            print("Aborting.")
            sys.exit(1)

    applied = 0
    for patch in PATCHES:
        offset   = patch['offset']
        original = patch['original']
        new_bytes = patch['patch']
        actual   = bytes(firmware[offset:offset + len(original)])

        if actual != original:
            print(f"\nWarning: patch '{patch['name']}' at 0x{offset:06X}")
            print(f"  Expected: {original.hex()}")
            print(f"  Found:    {actual.hex()}")
            answer = input("Apply anyway? (y/N): ").strip().lower()
            if answer != 'y':
                print("Skipping.")
                continue

        firmware[offset:offset + len(new_bytes)] = new_bytes

        print(f"\nApplied: {patch['name']}")
        print(f"  File offset: 0x{offset:06X}  (IDA 0x{offset + 0x100000:08X})")
        print(f"  Original:    {original.hex()}")
        print(f"  Patched:     {new_bytes.hex()}")
        print(f"  Description: {patch['description']}")
        applied += 1

    if applied == 0:
        print("\nNo patches applied. Exiting.")
        sys.exit(0)

    with open(output_file, 'wb') as f:
        f.write(firmware)

    print(f"\nWritten:      {output_file}")
    print(f"MD5 patched:  {md5(firmware)}")
    print("\nNext step: python bin2midi.py SP8EXall_patched.bin SP8EX_patched")


if __name__ == '__main__':
    main()
