"""Audit original Roland SMFs and generate template-preserving v3 SMFs.

No existing firmware or converter is changed. Run with python -B.
"""
import contextlib
import datetime
import hashlib
import importlib.util
import io
import json
import struct
import uuid
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SIZE = 0xC0004


def digest(data):
    return dict(size=len(data), md5=hashlib.md5(data).hexdigest(),
                sha256=hashlib.sha256(data).hexdigest())


def vlq(data, pos):
    value = 0
    for _ in range(4):
        octet = data[pos]
        pos += 1
        value = (value << 7) | (octet & 127)
        if octet < 128:
            return value, pos
    raise ValueError('Invalid VLQ')


def emit_vlq(value):
    result = [value & 127]
    while value >> 7:
        value >>= 7
        result.insert(0, 128 | (value & 127))
    return bytes(result)


def nibbles(value):
    return bytes((value >> shift) & 15 for shift in (16, 12, 8, 4, 0))


def from_nibbles(data):
    assert all(x < 16 for x in data)
    value = 0
    for x in data:
        value = value * 16 + x
    return value


def parse(data, allow_stale_track_length=False):
    assert data[:4] == b'MThd'
    assert struct.unpack('>IHH', data[4:12]) == (6, 0, 1)
    assert data[14:18] == b'MTrk'
    assert allow_stale_track_length or int.from_bytes(data[18:22], 'big') == len(data) - 22
    pos = 22
    events = []
    while pos < len(data):
        start = pos
        delta, pos = vlq(data, pos)
        kind = data[pos]
        pos += 1
        if kind == 255:
            subtype = data[pos]
            pos += 1
            length, pos = vlq(data, pos)
            payload = data[pos:pos + length]
            pos += length
            assert len(payload) == length
            e = dict(kind='meta', subtype=subtype, payload=payload)
        else:
            assert kind == 240
            length, pos = vlq(data, pos)
            body = data[pos:pos + length]
            pos += length
            assert len(body) == length and body[-1] == 247
            assert all(x < 128 for x in body[:-1])
            if body[:3] == bytes.fromhex('41 10 00'):
                header_size = 5
            else:
                assert body[:2] == bytes.fromhex('41 00')
                header_size = 4
            assert body[header_size - 1] == 18
            assert sum(body[header_size:-1]) % 128 == 0
            address = body[header_size:header_size + 3]
            memory = from_nibbles(body[header_size + 3:header_size + 8])
            payload = body[header_size + 8:-2]
            e = dict(kind='sysex', header=body[:header_size], address=address,
                     memory=memory, payload=payload, checksum=body[-2],
                     sysex_length=length)
        e.update(raw=data[start:pos], delta=delta)
        events.append(e)
    assert events[-1]['raw'] == bytes.fromhex('00 ff 2f 00')
    return events


def decode_set(files, allow_stale_track_length=False):
    output = bytearray(SIZE)
    covered = bytearray(SIZE)
    file_details = []
    previous_end = 0
    for index, (name, data) in enumerate(files):
        events = parse(data, allow_stale_track_length)
        details = dict(name=name, **digest(data), ppqn=int.from_bytes(data[12:14], 'big'),
                       data_packets=0, metadata=[], headers=[], ranges=[],
                       declared_track_length=int.from_bytes(data[18:22], 'big'),
                       actual_track_length=len(data) - 22,
                       track_length_status='PASS' if int.from_bytes(data[18:22], 'big') == len(data) - 22 else 'FAIL')
        flags = []
        for e in events:
            if e['kind'] == 'meta':
                details['metadata'].append(dict(smf_meta=e['subtype'],
                                               payload_hex=e['payload'].hex(), delta=e['delta']))
                continue
            header = e['header'].hex(' ')
            if header not in details['headers']:
                details['headers'].append(header)
            if e['address'][0] != 0:
                assert e['memory'] == 0
                details['metadata'].append(dict(address=e['address'].hex(' '),
                                               payload_hex=e['payload'].hex(), delta=e['delta']))
                if e['address'] == bytes.fromhex('01 02 00'):
                    assert e['payload'][:2] == bytes([index, 7])
                    flags.append(e['payload'][2])
                continue
            assert e['address'] in (bytes.fromhex('00 00 00'), bytes.fromhex('00 00 01'))
            assert len(e['payload']) % 8 == 0
            unpacked = bytearray()
            for group in range(0, len(e['payload']), 8):
                mask = e['payload'][group + 7]
                for j in range(7):
                    unpacked.append(e['payload'][group + j] +
                                    (128 if mask & (64 >> j) else 0))
            start = e['memory']
            end = start + len(unpacked)
            assert start >= previous_end and end <= SIZE
            assert not any(covered[start:end])
            output[start:end] = unpacked
            covered[start:end] = b'\x01' * len(unpacked)
            previous_end = end
            details['data_packets'] += 1
            if details['ranges'] and details['ranges'][-1]['end'] == start:
                details['ranges'][-1]['end'] = end
            else:
                details['ranges'].append(dict(start=start, end=end))
        assert flags == [0, 127]
        details['status'] = 'PASS'
        file_details.append(details)
    return bytes(output), covered, file_details


def packet(template, address, binary):
    assert len(binary) % 7 == 0
    encoded = bytearray()
    for offset in range(0, len(binary), 7):
        group = binary[offset:offset + 7]
        encoded.extend(x & 127 for x in group)
        encoded.append(sum((x >> 7) << (6 - j) for j, x in enumerate(group)))
    checksum_data = template['address'] + nibbles(address) + encoded
    body = template['header'] + checksum_data + bytes([(-sum(checksum_data)) & 127, 247])
    return emit_vlq(template['delta']) + b'\xf0' + emit_vlq(len(body)) + body


def regenerate(files, firmware, extra_packets=None):
    results = []
    extra_packets = extra_packets or []
    inserted = False
    for index, (name, original) in enumerate(files):
        track = bytearray()
        for e in parse(original, allow_stale_track_length=True):
            if e['kind'] == 'sysex' and e['address'][0] == 0:
                if index == 7 and e['memory'] >= 0xBFFDA and not inserted:
                    for start, binary in extra_packets:
                        track.extend(packet(e, start, binary))
                    inserted = True
                length = len(e['payload']) // 8 * 7
                track.extend(packet(e, e['memory'], firmware[e['memory']:e['memory'] + length]))
            else:
                track.extend(e['raw'])
        results.append((name, original[:18] + len(track).to_bytes(4, 'big') + track))
    assert not extra_packets or inserted
    return results


def write_files(directory, files):
    directory.mkdir()
    for name, data in files:
        with (directory / name).open('xb') as f:
            f.write(data)


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Quiet(io.TextIOBase):
    def write(self, value):
        return len(value)


def main():
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '_' + uuid.uuid4().hex[:8]
    directory = ROOT / 'firmware' / ('LinkPlan_v3_SMF_' + stamp)
    directory.mkdir()
    source_path = ROOT / 'firmware/SP8EXall.bin'
    candidate_path = ROOT / 'firmware/SP8EXall_LinkPlan_v3_readonly_20261005T230456Z_23c5dcc8.bin'
    source = source_path.read_bytes()
    candidate = candidate_path.read_bytes()
    assert digest(source)['md5'] == 'd744a9cd4a2790ac68d165fd7849b5d8'
    manifest_path = ROOT / 'analysis/Link_Plan_v3_manifest_2026-10-05.json'
    checked = json.loads(manifest_path.read_bytes())
    assert digest(candidate)['md5'] == checked['candidate_md5']
    assert digest(candidate)['sha256'] == checked['candidate_sha256']
    expected = bytearray(source)
    for mutation in checked['mutations']:
        start = int(mutation['file_offset'], 16)
        before = bytes.fromhex(mutation['original_sp_hex'])
        assert source[start:start + len(before)] == before
        expected[start:start + len(before)] = bytes.fromhex(mutation['replacement_hex'])
    assert bytes(expected) == candidate
    report = dict(schema_version=1, evidence_status='OBSERVED', source=digest(source),
                  candidate=digest(candidate), candidate_path=str(candidate_path.relative_to(ROOT)),
                  checked_manifest=digest(manifest_path.read_bytes()), archives=[],
                  converter_audit={}, runtime_validation='UNRESOLVED; not transmitted to hardware')
    templates = None
    coverage = None
    for archive_name in ('SP808EXv1001.zip', 'SP-808EX_v.1001_for_SP-808.zip'):
        archive_path = ROOT / 'firmware' / archive_name
        with zipfile.ZipFile(archive_path) as z:
            names = sorted(n for n in z.namelist() if n.lower().endswith('.mid'))
            assert len(names) == 8
            originals = [(n, z.read(n)) for n in names]
        binary, coverage, details = decode_set(originals, allow_stale_track_length=True)
        assert binary == source
        regenerated = regenerate(originals, binary)
        roundtrip_dir = directory / ('roundtrip_' + archive_path.stem)
        write_files(roundtrip_dir, regenerated)
        reread = [(name, (roundtrip_dir / name).read_bytes()) for name, _ in regenerated]
        recovered, _, generated_details = decode_set(reread)
        assert recovered == binary == source
        whole_exact = reread == originals
        assert all(x[1][:18] + x[1][22:] == y[1][:18] + y[1][22:] for x, y in zip(reread, originals))
        bin_path = roundtrip_dir / 'recovered.bin'
        with bin_path.open('xb') as f:
            f.write(recovered)
        report['archives'].append(dict(archive=archive_name, archive_hashes=digest(archive_path.read_bytes()),
                                       original_files=details, regenerated_files=generated_details,
                                       original_extracted_bin=digest(binary), regenerated_extracted_bin=digest(recovered),
                                       firmware_payload_exact=True, whole_smf_files_exact=whole_exact,
                                       implicit_zero_bytes=len(coverage) - sum(coverage), status='PASS'))
        if archive_name == 'SP808EXv1001.zip':
            assert whole_exact
            templates = originals
    legacy_dir = directory / 'legacy_converter_test'
    legacy_dir.mkdir()
    legacy_encoder = load_module('legacy_encoder', ROOT / 'firmware/bin2midi.py')
    with contextlib.redirect_stdout(Quiet()):
        legacy_encoder.bin_to_midi(str(source_path), str(legacy_dir / 'legacy'))
    legacy_files = sorted(legacy_dir.glob('*.mid'))
    try:
        decode_set([(p.name, p.read_bytes()) for p in legacy_files])
        raise RuntimeError('Legacy converter unexpectedly passed strict validation')
    except AssertionError:
        report['converter_audit']['bin2midi_strict_smf_status'] = 'FAIL'
    legacy_decoder = load_module('legacy_decoder', ROOT / 'firmware/rolandext.py')
    legacy_bin = legacy_dir / 'legacy_decoder.bin'
    with contextlib.redirect_stdout(Quiet()):
        for p in legacy_files:
            legacy_decoder.process_file(str(p), str(legacy_bin), 0x41, 0x10, 0x2B, 0x12)
    legacy_result = legacy_bin.read_bytes()
    report['converter_audit'].update(legacy_output_bin=digest(legacy_result),
                                     legacy_payload_exact=legacy_result == source,
                                     legacy_generated_files=[dict(name=p.name, **digest(p.read_bytes()),
                                                                  status='FAIL', purpose='diagnostic only; not deployment')
                                                             for p in legacy_files])
    assert legacy_result != source
    # Original omissions are explicitly zero-filled in the stock BIN. Supply
    # only the uncovered v3 island, using original 196-byte packet maximum.
    missing = [i for i, (x, y) in enumerate(zip(candidate, coverage)) if x and not y]
    extra_packets = []
    if missing:
        start = missing[0]
        finish = missing[-1] + 1
        finish += (7 - (finish - start) % 7) % 7
        assert not any(coverage[start:finish])
        for pos in range(start, finish, 196):
            extra_packets.append((pos, candidate[pos:min(pos + 196, finish)]))
    deployment_files = regenerate(templates, candidate, extra_packets)
    deployment_dir = directory / 'deployment'
    write_files(deployment_dir, deployment_files)
    reread = [(name, (deployment_dir / name).read_bytes()) for name, _ in deployment_files]
    recovered, candidate_coverage, details = decode_set(reread)
    assert recovered == candidate
    assert all(covered or not value for value, covered in zip(candidate, candidate_coverage))
    with (directory / 'candidate_recovered.bin').open('xb') as f:
        f.write(recovered)
    assert candidate_path.read_bytes() == candidate and source_path.read_bytes() == source
    for detail in details:
        detail['path'] = 'deployment/' + detail['name']
        detail['send_order'] = details.index(detail) + 1
    report['deployment'] = dict(template_archive='SP808EXv1001.zip', files=details,
                                extra_packets=[dict(address=pos, decoded_length=len(data))
                                               for pos, data in extra_packets],
                                firmware_payload_exact=True, recovered_bin=digest(recovered),
                                candidate_unchanged=True, source_unchanged=True, status='PASS',
                                opaque_final_metadata=dict(address='01 01 00', payload='4e',
                                                           action='Preserved exactly from original',
                                                           semantic_status='UNRESOLVED'))
    report['overall_status'] = 'PASS: original/template round trips and v3 deployment payload; existing converters fail'
    with (directory / 'manifest.json').open('x', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
        f.write('\n')
    print(json.dumps(dict(directory=str(directory.relative_to(ROOT)),
                          deployment_files=len(details), extra_packets=len(extra_packets),
                          recovered_hashes=digest(recovered),
                          legacy_result_size=len(legacy_result), status=report['overall_status']), indent=2))


if __name__ == '__main__':
    main()
