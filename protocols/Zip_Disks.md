# Zip Disks

## Size and geometry and partition table of ZIP drives

Non-present disks have a capacity of 0 bytes (obviously).

```
100MB disks have a capacity of 100,663,296 bytes, i.e., 196,608 sectors
250MB disks have a capacity of 250,640,384 bytes, i.e., 489,532 sectors
LS120 disks have a capacity of 126,222,336 bytes, i.e., 246,528 sectors
```
Note: LS120 disk for comparision.

## Partition Table

The ATAPI Removable Drive (ARMD) specification developed by Compaq and Phoenix Technologies, describes ARMD media as big floppy disks. In this regard, they have no partition table.

This is also what WinNT and Windows95 expect: when a device reports itself as ATAPI FLOPPY, no partition table is read.

On the other hand, ZIP disks prepared by IOMEGA utilities actually have a partition table (usually having a single entry, the fourth, spanning the whole disk, so that access to such disks with partition table goes via mounting /dev/sda4). 
On disks for the Mac one has 6 partitions, and again the fourth can be mounted, with filesystemtype "hfs".

To reconcile these two points of view, early ATAPI2 ZIP drives come with a jumper (called the ARMD-jumper, or, more commonly, the A: jumper) that will hide the first 32 sectors of the disk.
In other words, with jumper we have a big floppy and no partition table; without jumper we have a small disk with DOS-type partition table. The jumper settings are given in the diagram below.

However, this is not done on older ATAPI and newer ATAPI3 ZIP drives. This means that a disk may be shifted on one machine and unshifted on another, and work in one environment and not in another.

This hiding the first 32 sectors turns the 100663296 byte (196608 sector) disk into a 100646912 byte (196576 sector) one.

Thus, in case you have problems with an ATAPI2 ZIP drive, either remove the (middle) jumper at the back of the drive and mount the partition, say /dev/hdb1, or leave the jumper and mount the full disk, say /dev/hdb.

## Drive A: Functionality

The following characteristics distinguish Zip ATAPI drives that have drive A: capability. These characteristics are described in more detail in relevant sections of this document.

- Each pin pair on the Configuration Jumper Block on the rear of the drive has been functionally defined, thus making the jumper block nonstandard.

- The ATA IDENTIFY PACKET DEVICE Command (A1h) has an updated Identify Drive Informatin.

Zip ATAPI drives that support Drive A: operation return 4002h in word 50 in lieu of 0000h (which is the value returned by Zip ATAPI drives without drive A: capability).

* New options are available for the MISCELLANEOUS CONTROL PACKET command (0Dh) to enable and disable drive

## A: operation

When the drive is configured in the Drive A: mode:

* The first 32 LBS'a of the disk are not accessible (i.e., the drive adds 32 to all LBA's specified in all commands).
* Disk capacity is reduced by 32 LBA's.
* The FORMAT UNIT PACKET Command (04h) writes a DOS partition on LBA-32.
* ATA IDENTIFY PACKET DEVICE Command (A1h) reports "Floppy" at word offset 34 (see also Table 5-5).

* When the host writes data to LBA 0 that the drive's firmware evaluates as a DOS boot record***, the drive then checks the data at offset 28; if offset 28 contains
00h, the drive changes the value to 80h. The drive also checks the data at offset 36; if offset 36 contains 00h, the drive changes it to 20h. The drive makes these
changes prior to writing the data to LBA 0 on the disk.

* When the host reads data from LBA 0 and the drive's firmware evaluates the retrieved data as a DOS boot record***, the drive then checks the data at offset 28; if offset 28 contains 80h, the drive changes it to 00h.
The drive also checks the data at offset 36; if offset 36 contains 20h, the drive changes it to 00h. The drive makes these changes before sending the data on to the
host.

* NON-SENSE PACKET Command (06h), Disk Status Page 02h, byte 63, bit-7, contains a one. (See Section 5.5.

*** The drive identifies a DOS boot record by looking for the following values:

```
- 55h at offset 510
- AAh at offset 411
- 29h at offset 38
```

## ENABLE/DISABLE DRIVE A: FUNCTION

Drive A: functionality is enabled by the Operation Subcode being set to EAh, with zeros in Byte 3:

```
Byte 0          Operation Code, 0Dh
Byte 1          Reserved
Byte 2          Operation Subcode (EAh)
Byte 3          Reserved (All bits = 0)
Byte 4-5                Reserved
Byte 6-11               PAD
```
Drive A: functionality is disabled by the Operation
Subcode being set to DAh, with zeros in Byte 3:
```
Byte 0          Operation Code, 0Dh
Byte 1          Reserved
Byte 2          Operation Subcode (DAh)
Byte 3          Reserved (All bits = 0)
Byte 4-5                Reserved
Byte 6-11               PAD
```
---------------------------------------------------
