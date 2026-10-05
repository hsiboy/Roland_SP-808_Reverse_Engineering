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
