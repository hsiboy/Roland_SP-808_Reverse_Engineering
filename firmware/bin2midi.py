#!/usr/bin/env python3
"""
SP-808 Binary to MIDI SysEx Converter

Converts a patched firmware binary back into the 8 MIDI SysEx files the SP-808
expects for a firmware update. This is the inverse of rolandext.py.

WARNING: This script has not been verified on real hardware. Before flashing,
always round-trip test one output file:

    python rolandext.py model=sp808 infil="SP8EX_patched#1.mid" outfil=verify.bin
    cmp -n 98304 SP8EXall_patched.bin verify.bin   # should report no differences

Usage:
    python bin2midi.py <input_binary> <output_prefix>

Example:
    python bin2midi.py SP8EXall_patched.bin SP8EX_patched

This produces: SP8EX_patched#1.mid ... SP8EX_patched#8.mid

Flash procedure:
    1. Connect MIDI interface to SP-808 MIDI IN
    2. Power on SP-808 while holding SHIFT (display shows "MIDI UPDATE")
    3. Send each file in order (#1 through #8)
    4. Wait for "Completed" message before sending the next file

Algorithm notes:
    - 7-bit encoding verified against rolandext.py's decoder (which is known-working)
    - SysEx format: F0 41 10 00 2B 12 [addr(3)] [memadd(5-nibbles)] [7bit-data] [cksm] F7
    - Firmware split: 7 files of 0x18000 bytes + 1 file of 0x18004 bytes = 0xC0004 total
    - Packet size: 252 binary bytes → 288 7-bit bytes per SysEx packet
"""

import sys
import struct

# SP-808 Roland SysEx identifiers (from rolandext.py MODEL_CONFIG['sp808'])
MANF_ID    = 0x41   # Roland
DEV_ID     = 0x10   # Default MIDI device ID
MODEL_ID   = 0x2B   # SP-808 model ID
CMD_DATA1  = 0x12   # Data Set 1

# SP-808 firmware is exactly 0xC0004 bytes, split across 8 MIDI files
FILE_SIZES = [0x18000] * 7 + [0x18004]

# Must be a multiple of 7; 252 = 36 × 7 → 288 7-bit encoded bytes per packet
BYTES_PER_PACKET = 252


def encode_7bit(data: bytes) -> bytes:
    """
    Encode binary data into Roland's 7-bit SysEx packing format.

    Every 7 binary bytes become 8 output bytes:
      - 7 bytes with the MSB cleared (the lower 7 bits of each input byte)
      - 1 mask byte whose bits 6..0 hold the MSBs of input bytes 0..6

    This is the exact inverse of rolandext.py's decode loop:
        maskbyt = (maskbyt << 1) & 0xFF
        bytvar  = octet[j] | (maskbyt & 0x80)

    Reference example from Rvs82bin.bas:
        Input : 00 16 DE 8A 4E 53 20  (7 bytes)
        Output: 00 16 5E 0A 4E 53 20  18  (7 + 1 mask byte)
        Mask  : bits 6..0 = MSBs of bytes 0..6 = 0,0,1,1,0,0,0 = 0x18
    """
    if len(data) % 7 != 0:
        raise ValueError(f"encode_7bit: input length {len(data)} is not a multiple of 7")

    out = bytearray()
    for i in range(0, len(data), 7):
        chunk = data[i:i + 7]
        mask = 0
        for j, byte in enumerate(chunk):
            mask |= ((byte >> 7) & 1) << (6 - j)
        for byte in chunk:
            out.append(byte & 0x7F)
        out.append(mask)
    return bytes(out)


def roland_checksum(data: bytes) -> int:
    """Roland 7-bit checksum: (128 - sum(data) % 128) & 0x7F"""
    return (128 - (sum(data) % 128)) & 0x7F


def encode_nibbles(value: int, count: int = 5) -> bytes:
    """Encode an integer as `count` nibble bytes, most-significant first."""
    return bytes([(value >> (4 * (count - 1 - i))) & 0x0F for i in range(count)])


def varlength(n: int) -> bytes:
    """Encode n as a MIDI variable-length quantity (max 2 bytes = 0x3FFF)."""
    if n < 0x80:
        return bytes([n])
    if n < 0x4000:
        return bytes([0x80 | (n >> 7), n & 0x7F])
    raise ValueError(f"varlength: {n} exceeds 0x3FFF")


def sysex_event(event_addr: bytes, mem_addr: int, payload: bytes) -> bytes:
    """
    Build one complete MIDI track event containing a Roland SysEx data packet.

    Format (excluding delta-time):
        F0 [reclen] 41 10 00 2B 12 [addr(3)] [memadd(5-nibbles)] [payload] [cksm] F7

    reclen covers everything from 0x41 up to and including cksm (F7 excluded).
    """
    mem_nibbles = encode_nibbles(mem_addr)
    cksm_input = event_addr + mem_nibbles + payload
    cksm = roland_checksum(cksm_input)

    body = bytes([MANF_ID, DEV_ID, 0x00, MODEL_ID, CMD_DATA1]) + \
           event_addr + mem_nibbles + payload + bytes([cksm])

    return bytes([0x10, 0xF0]) + varlength(len(body)) + body + bytes([0xF7])


def metadata_event(sub_addr: int, payload: bytes) -> bytes:
    """Build a metadata SysEx event (event address 01 XX 00, memadd = 0)."""
    event_addr = bytes([0x01, sub_addr, 0x00])
    mem_nibbles = bytes(5)  # all zeros
    cksm_input = event_addr + mem_nibbles + payload
    cksm = roland_checksum(cksm_input)

    body = bytes([MANF_ID, DEV_ID, 0x00, MODEL_ID, CMD_DATA1]) + \
           event_addr + mem_nibbles + payload + bytes([cksm])

    return bytes([0x10, 0xF0]) + varlength(len(body)) + body + bytes([0xF7])


def build_midi_file(track_data: bytes) -> bytes:
    """Wrap track bytes in a standard SMF type-0 MIDI file."""
    header = struct.pack('>4sIHHH', b'MThd', 6, 0, 1, 0x0060)
    track  = struct.pack('>4sI', b'MTrk', len(track_data)) + track_data
    return header + track


def bin_to_midi(input_file: str, output_prefix: str) -> None:
    try:
        with open(input_file, 'rb') as f:
            firmware = f.read()
    except FileNotFoundError:
        print(f"Error: cannot read '{input_file}'")
        sys.exit(1)

    expected_size = sum(FILE_SIZES)
    if len(firmware) != expected_size:
        print(f"Warning: expected {expected_size:#x} bytes, got {len(firmware):#x} bytes")

    total_files = len(FILE_SIZES)
    file_offset = 0

    for file_num, file_size in enumerate(FILE_SIZES):
        track = bytearray()
        chunk = firmware[file_offset:file_offset + file_size]

        # --- File-start marker (event addr 01 02 00) ---
        # Payload: [file_index, total_files-1, 0x00]
        track += metadata_event(0x02, bytes([file_num, total_files - 1, 0x00]))

        # --- Memory parameters (event addr 01 00 00) ---
        # Payload: [000 memstart(5-nibbles) 000 memsize(5-nibbles)]
        mem_params = (
            bytes(3) +
            encode_nibbles(file_offset) +
            bytes(3) +
            encode_nibbles(file_size)
        )
        track += metadata_event(0x00, mem_params)

        # --- Firmware data packets (event addr 00 00 00) ---
        bin_pos = file_offset
        remaining = chunk

        while remaining:
            packet_bin = remaining[:BYTES_PER_PACKET]
            remaining  = remaining[BYTES_PER_PACKET:]

            # Pad to next multiple of 7 for clean 7-bit encoding.
            # Any extra zeros written past the current file's boundary will be
            # overwritten correctly by the next file's first packet.
            pad = (7 - len(packet_bin) % 7) % 7
            padded = packet_bin + bytes(pad)
            encoded = encode_7bit(padded)

            track += sysex_event(bytes([0x00, 0x00, 0x00]), bin_pos, encoded)
            bin_pos += len(packet_bin)

        # --- File-end marker (event addr 01 02 00) ---
        # Payload: [file_index, total_files-1, 0x7F]
        track += metadata_event(0x02, bytes([file_num, total_files - 1, 0x7F]))

        # --- End of track ---
        track += bytes([0x00, 0xFF, 0x2F, 0x00])

        midi_bytes = build_midi_file(bytes(track))
        out_path = f"{output_prefix}#{file_num + 1}.mid"
        with open(out_path, 'wb') as f:
            f.write(midi_bytes)
        print(f"Written: {out_path} ({len(midi_bytes):,} bytes)")

        file_offset += file_size

    print(f"\nCreated {total_files} MIDI files.")
    print("\nVerify before flashing (round-trip test on file #1):")
    print(f"  python rolandext.py model=sp808 infil=\"{output_prefix}#1.mid\" outfil=verify.bin")
    print(f"  cmp -n {FILE_SIZES[0]} {input_file} verify.bin")


def main():
    if len(sys.argv) != 3:
        print("Usage: python bin2midi.py <input_binary> <output_prefix>")
        print("Example: python bin2midi.py SP8EXall_patched.bin SP8EX_patched")
        sys.exit(1)

    bin_to_midi(sys.argv[1], sys.argv[2])


if __name__ == '__main__':
    main()
