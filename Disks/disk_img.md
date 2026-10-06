# Inspecting SP‑808 Zip disk images

SP‑808 / SP‑808EX media is nothing exotic from a host's point of view: a raw image of a Zip disk is a
**standard DOS/MBR volume with a FAT filesystem**, so it mounts and reads on any modern PC. The dumps
below show that from two angles — the partition layout, and the Roland project files inside — using a
ZIP‑250 image and an SP‑808EX demo disk.

> To pull the files out programmatically (without mounting), use
> [`Tools/sp808_fat_extract.py`](Tools/sp808_fat_extract.py); for the on‑disk structure in depth see
> [`SP-808_Demo_Disk_Analysis.md`](SP-808_Demo_Disk_Analysis.md).

## Partition layout

`fdisk -l` on a 250 MB Zip image shows an ordinary DOS disklabel with a single partition that starts at
**sector 32** (the first 32 sectors hold the MBR and alignment padding) and spans the rest of the disk:

```
pi@DLT9PYZTZ1:~$ fdisk -l /mnt/g/image/Zip250/ZIP250_0.img
Disk /mnt/g/image/Zip250/ZIP250_0.img: 239 MiB, 250640384 bytes, 489532 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0x00000000

Device                            Boot Start    End Sectors  Size Id Type
/mnt/g/image/Zip250/ZIP250_0.img1         32 489530  489499  239M  6 FAT16
```

The partition **type byte** here is `0x06`, which tooling labels "FAT16" — but the *actual* FAT width
is decided by the cluster count, not that byte. A 100 MB SP‑808 disk (with 32 KiB clusters) works out to
only ~3,070 clusters, which is **FAT12** by the Microsoft count‑of‑clusters rule; a larger 250 MB volume
like this one has enough clusters to be genuine FAT16. (The 100 MB demo disk is confirmed FAT12 in
[`SP-808_Demo_Disk_Analysis.md`](SP-808_Demo_Disk_Analysis.md).)

## What the SP‑808 writes to it

Mounted on a PC (here drive `I:`, volume label `SP-808TS25E`), the filesystem is plain FAT. The key thing
to notice is that **`SONG0000.VS2` is a *directory*, not a file** — each song/project is a folder, with a
top‑level `SONGLIST.VS2` indexing them:

```
I:\>tree /f
Folder PATH listing for volume SP-808TS25E
Volume serial number is 0000-5A39
I:.
│   SONGLIST.VS2
│
└───SONG0000.VS2
        PADBANK_.VS2
        SAMPLE__.BAK
        SAMPLE__.VS2
        EFFECT__.VS2
        EFFECT1_.VS2
        VSNG0000.VS2
        VSNGLIST.VS2
```

Inside a song folder, the `.VS2` files hold the project's components. Their **internal binary formats are
undocumented** (an open item — see [`../TODO.md`](../TODO.md)), but the names map cleanly onto SP‑808
concepts:

| File | Apparent role |
|---|---|
| `SONGLIST.VS2` | index of songs on the disk |
| `PADBANK_.VS2` | pad‑bank assignments |
| `SAMPLE__.VS2` / `SAMPLE__.BAK` | sample data (plus a backup copy) |
| `EFFECT__.VS2` / `EFFECT1_.VS2` | effects settings / patches |
| `VSNG0000.VS2` / `VSNGLIST.VS2` | sequence (song) data and its list |
| `TAKE####.VS2` *(on recorded disks)* | recorded audio takes / phrases |

## File sizes

`dir /s` confirms the layout and gives the component sizes — note the round, block‑aligned sizes
(1 KiB, 25 KiB, 32 KiB, 96 KiB), typical of fixed‑size Roland structures:

```
I:\>dir /s
 Volume in drive I is SP-808TS25E
 Volume Serial Number is 0000-5A39

 Directory of I:\

01/01/1997  12:00    <DIR>          SONG0000.VS2
01/01/1997  12:00               322 SONGLIST.VS2
               1 File(s)            322 bytes

 Directory of I:\SONG0000.VS2

01/01/1997  12:00    <DIR>          .
01/01/1997  12:00    <DIR>          ..
01/01/1997  12:01             1,024 PADBANK_.VS2
01/01/1997  12:01            32,768 SAMPLE__.BAK
01/01/1997  12:01            32,768 SAMPLE__.VS2
01/01/1997  12:01            25,600 EFFECT__.VS2
01/01/1997  12:01            25,600 EFFECT1_.VS2
01/01/1997  12:01            98,304 VSNG0000.VS2
01/01/1997  12:01             1,024 VSNGLIST.VS2
               7 File(s)        217,088 bytes

     Total Files Listed:
               8 File(s)        217,410 bytes
               3 Dir(s)     250,183,680 bytes free
```

The `01/01/1997` timestamps are the SP‑808's default clock, not real modification dates.
