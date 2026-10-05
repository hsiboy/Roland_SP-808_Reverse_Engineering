# Disks/Tools

Scripts for inspecting and extracting SP-808 / SP-808EX Zip-disk images.

## Extraction

**Use [`sp808_fat_extract.py`](sp808_fat_extract.py).**

The SP-808 disk is a **standard DOS MBR + FAT12 volume** (partition at sector 32, 32 KiB clusters).
Extraction is just reading FAT — there is no proprietary Roland directory format. `sp808_fat_extract.py`
parses the MBR + BPB, walks the real directory tree via the FAT cluster chain, and copies files out
intact.

```
python sp808_fat_extract.py <disk.img>              # list the tree
python sp808_fat_extract.py <disk.img> -x [outdir]  # extract
```

Verified against `../../Roland-SP808-Demo_Disk_100mb.img` (2026-10-05): 269 files /
75,214,236 bytes, every size matching an independent FAT driver (macOS `mount -t msdos`, per
`../SP-808_Demo_Disk_Analysis.md`), and against a synthetic FAT image round-trip.

> Note on "FAT12 vs FAT16": the partition type byte is `0x06` and some tools (incl. macOS, `file`)
> label the volume "FAT16", but with ~3070 clusters it is **FAT12** by the Microsoft `count-of-clusters`
> rule (< 4085). `sp808_fat_extract.py` auto-detects from the cluster count and reads it correctly.

The `.VS2` files hold Roland data (RDAC audio, etc.); decoding their *internal* structure is a
separate step (see the `unscramble` / `rdac_map` helpers), downstream of getting the bytes out.

## Removed (2026-10-05)

The following were deleted: they invented a non-existent proprietary directory record
("start-LBA @ offset 20, size @ offset 24") and produced impossible results — e.g. a 93,000 MB file
on a 96 MB disk — because those offsets land on FAT date/cluster/time fields:

`sp808_disc_extractor.py`, `sp808_disc_extract_v2.py`, `sp808_disc_extractor_v3.py` …`_v8.py`,
`sp808_directory.py`, `sp808_hunter.py`.

## Other helpers (unaudited)

`sp808_disc_analyse_all.py`, `sp808_disc_explorer.py`, `sp808_disc_manager.py`,
`sp808_disc_forensics.py`, `sp808_disc_checksum.py`, `sp808_disc_header_peek.py`,
`sp808_disk_inspect.py`, `sp808_disk_tool.py`, `sp808_disc_unscramble.py`, `sp808_debug_.py`,
`Sp808_disc_diff.py`, `Sp808_disc_export.py`, `Sp808_rdac_map.py` — retained as-is; not re-verified.
Prefer `sp808_fat_extract.py` for anything touching the directory/file layer.
