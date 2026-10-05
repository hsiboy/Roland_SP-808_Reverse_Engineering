#!/usr/bin/env python3
"""
sp808_fat_extract.py — correct extractor for SP-808 / SP-808EX Zip-disk images.

The SP-808 stores data on a **standard DOS MBR + FAT16 volume** (confirmed in
Disks/SP-808_Demo_Disk_Analysis.md: the image mounts with `mount -t msdos`, and
every on-disk directory entry is a plain FAT 8.3 record). Files are extracted by
reading FAT16 — there is no proprietary Roland directory format.

This replaces the former sp808_disc_extractor*.py / sp808_directory.py / hunter
scripts, which invented a non-existent "start-LBA @20 / size @24" record and
produced impossible results (e.g. a 93,000 MB file on a 96 MB disk).

The *.VS2 files themselves hold Roland data (RDAC audio etc.); decoding their
internal format is a separate step — this tool just gets the bytes out intact.

Usage:
    python sp808_fat_extract.py <disk.img>              # list the tree
    python sp808_fat_extract.py <disk.img> -x [outdir]  # extract files

Pure standard library; works on any FAT12/FAT16 image.
"""
import sys
import os
import struct


def _u16(b, o): return struct.unpack_from("<H", b, o)[0]
def _u32(b, o): return struct.unpack_from("<I", b, o)[0]


class Fat:
    def __init__(self, path):
        self.f = open(path, "rb")
        self.part_start = self._find_partition()
        bs = self._read_sector(self.part_start, count=1, sector_size=512)
        # Boot sector / BPB
        self.bytes_per_sec = _u16(bs, 0x0B) or 512
        self.sec_per_clus = bs[0x0D] or 1
        self.reserved = _u16(bs, 0x0E)
        self.num_fats = bs[0x10] or 2
        self.root_entries = _u16(bs, 0x11)
        self.fat_size = _u16(bs, 0x16)
        total16 = _u16(bs, 0x13)
        self.total_sectors = total16 if total16 else _u32(bs, 0x20)

        self.fat_start = self.part_start + self.reserved
        self.root_start = self.fat_start + self.num_fats * self.fat_size
        self.root_sectors = (self.root_entries * 32 + self.bytes_per_sec - 1) // self.bytes_per_sec
        self.data_start = self.root_start + self.root_sectors

        clusters = (self.total_sectors - (self.data_start - self.part_start)) // self.sec_per_clus
        self.fat12 = clusters < 4085
        self.eoc = 0x0FF8 if self.fat12 else 0xFFF8
        self._fat = self._read_sector(self.fat_start, self.fat_size, self.bytes_per_sec)

    # -- low level ---------------------------------------------------------
    def _read_sector(self, lba, count, sector_size):
        self.f.seek(lba * sector_size)
        return self.f.read(count * sector_size)

    def _find_partition(self):
        self.f.seek(0)
        mbr = self.f.read(512)
        if mbr[0x1FE:0x200] == b"\x55\xAA":
            for i in range(4):
                e = 0x1BE + i * 16
                ptype = mbr[e + 4]
                start = _u32(mbr, e + 8)
                if ptype in (0x01, 0x04, 0x06, 0x0B, 0x0C, 0x0E) and start:
                    return start
        # No usable MBR entry: treat the image itself as the volume.
        return 0

    def _fat_next(self, clus):
        if self.fat12:
            off = clus + (clus // 2)
            val = _u16(self._fat, off)
            return (val >> 4) if (clus & 1) else (val & 0x0FFF)
        return _u16(self._fat, clus * 2)

    def _chain(self, first):
        clus, seen = first, set()
        while 2 <= clus < self.eoc and clus not in seen:
            seen.add(clus)
            yield clus
            clus = self._fat_next(clus)

    def _cluster_bytes(self, clus):
        lba = self.data_start + (clus - 2) * self.sec_per_clus
        return self._read_sector(lba, self.sec_per_clus, self.bytes_per_sec)

    def _read_file(self, first_clus, size):
        data = bytearray()
        for c in self._chain(first_clus):
            data += self._cluster_bytes(c)
            if len(data) >= size:
                break
        return bytes(data[:size]) if size else bytes(data)

    # -- directory walking -------------------------------------------------
    def _root_entries_bytes(self):
        return self._read_sector(self.root_start, self.root_sectors, self.bytes_per_sec)

    def _parse_dir(self, raw):
        for o in range(0, len(raw), 32):
            e = raw[o:o + 32]
            if len(e) < 32 or e[0] == 0x00:
                break
            if e[0] == 0xE5:
                continue
            attr = e[11]
            if attr == 0x0F:            # long-file-name component
                continue
            if attr & 0x08:             # volume label
                continue
            base = e[0:8].decode("ascii", "replace").rstrip()
            ext = e[8:11].decode("ascii", "replace").rstrip()
            name = base + ("." + ext if ext else "")
            first = (_u16(e, 20) << 16) | _u16(e, 26)
            size = _u32(e, 28)
            is_dir = bool(attr & 0x10)
            if name in (".", ".."):
                continue
            yield name, is_dir, first, size

    def walk(self, visitor, raw=None, path=""):
        raw = self._root_entries_bytes() if raw is None else raw
        for name, is_dir, first, size in self._parse_dir(raw):
            full = path + "/" + name if path else name
            visitor(full, is_dir, first, size)
            if is_dir and first >= 2:
                sub = b"".join(self._cluster_bytes(c) for c in self._chain(first))
                self.walk(visitor, sub, full)

    def summary(self):
        return (f"partition@{self.part_start}  {'FAT12' if self.fat12 else 'FAT16'}  "
                f"bps={self.bytes_per_sec} spc={self.sec_per_clus} "
                f"fat@{self.fat_start}x{self.num_fats} root@{self.root_start}({self.root_entries}) "
                f"data@{self.data_start}")


def main(argv):
    if len(argv) < 2:
        print(__doc__.strip().split("Usage:")[1])
        return 1
    img = argv[1]
    extract = len(argv) > 2 and argv[2] in ("-x", "--extract")
    outdir = (argv[3] if len(argv) > 3 else
              os.path.splitext(os.path.basename(img))[0] + "_extracted")

    fat = Fat(img)
    print(f"[*] {img}")
    print(f"[*] {fat.summary()}")
    files = dirs = total = 0

    def visit(full, is_dir, first, size):
        nonlocal files, dirs, total
        if is_dir:
            dirs += 1
            print(f"    <DIR>  {full}/")
            if extract:
                os.makedirs(os.path.join(outdir, full), exist_ok=True)
        else:
            files += 1
            total += size
            print(f"    {size:>10}  {full}")
            if extract:
                data = fat._read_file(first, size)
                dst = os.path.join(outdir, full)
                os.makedirs(os.path.dirname(dst) or ".", exist_ok=True)
                with open(dst, "wb") as out:
                    out.write(data)

    fat.walk(visit)
    print(f"[+] {files} files ({total:,} bytes), {dirs} dirs"
          + (f" -> {outdir}/" if extract else "  (list only; pass -x to extract)"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
