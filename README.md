# Roland_SP-808_Reverse_Engineering
A collection of gathered artifacts and original work, towards getting a modern ATAPI device working in a Roland SP-808

These are some findings during my trip down the rabbit hole that is a replacement for the Iomega Zip drive in the Roland SP-808 and SP-808ex samplers.

INQUIRY

The INQUIRY command may be used by a host computer to determine the configuration of the ATAPI Block
Device. ATAPI Block Devices respond with information that includes their type and specification level and
may include the vendor’s identification, model number and other useful information. 

SP-808 sends "ATAPI INQUIRY", but does not read allocated data and sends "IDENTIFY PACKET DEVICE" next.


[00:00:31 DEBUG D0 EF --] SET FEATURES ID - drive: A0
[00:00:31 DEBUG D0 EF --] Subcommand: 00, params: 02 | 01 | 80 | 00

** "Subcommand: 00" is not documented in ATA-5 specification, it is reserved.

[00:01:57 CONSOLE] Logging start...
[00:02:00 DEBUG D0 A0 5A] Software (SRST) Reset
[00:02:00 TRACE D0 A0 5A] Present dev: Master 
[00:02:00 DEBUG D0 A0 5A] 
[00:02:00 DEBUG D0 A1 --] IDENTIFY PACKET DEVICE
[00:02:00 TRACE D0 A1 --] ATA2 PIO-In xfer end

[00:02:00 DEBUG D0 EF --] SET FEATURES ID - drive: A0
[00:02:00 DEBUG D0 EF --] Subcomm: 03, params: 08 | 01 | 14 | eb
[00:02:00 DEBUG D0 EF --] PIO flow control Mode 0
[00:02:00 TRACE D0 A0 00] Pending Unit attention: 1, key=06, asc=29, ascq=00
[00:02:00 TRACE D0 A0 00] ACK Sense: sts=51, sense=6, asc=29
[00:02:00 DEBUG D0 A0 03] REQUEST SENSE: key=06, asc=29, ascq=00
[00:02:00 TRACE D0 A0 03] PKT data xfer end
[00:02:00 TRACE D0 A0 03] 
[00:02:00 DEBUG D0 A0 1B] START/STOP UNIT: LoEj: 0, start: 1, immed: 0
[00:02:00 TRACE D0 A0 12] Packet: 12 00 00 00 80 00 00 00 00 00 00 00, DMA: 0
[00:02:00 DEBUG D0 A0 12] ATAPI INQUIRY
[00:02:00 TRACE D0 A0 12] PKT data xfer end
[00:02:00 TRACE D0 A0 12] 
[00:02:00 TRACE D0 A0 5A] Packet: 5A 00 2F 00 00 00 00 00 80 00 00 00, DMA: 0
[00:02:00 DEBUG D0 A0 5A] MODE SENSE (10)
[00:02:00 DEBUG D0 A0 5A] MODE SENSE PC=0, PageCode=2f, alloc_len=80
[00:02:00 TRACE D0 A0 5A] Adding page: 2f, len=6
[00:02:00 TRACE D0 A0 5A] PKT data xfer end
[00:02:00 TRACE D0 A0 5A] 
[00:02:00 TRACE D0 A0 55] Packet: 55 00 00 00 00 00 00 00 0E 00 00 00, DMA: 0
[00:02:00 WARN  D0 A0 55] !! Unknown ATAPI CMD: 55 !!

* 55h MODE SELECT (10)
* 23h READ FORMAT CAPACITIES
* 0Dh ZIP vendor specific.


Eject is communicated between Roland and ZIP via one bit in the output of 06h - mode nonsense which is an Iomega vendor specific command.


ATAPI Byte Count Register handling.

The SP-808 puts a maximum number of bytes it wants to receive in one DRQ cycle to this register and the drive can send up to this limit. 

For exampe, here the Roland SP-808 requested one block(sector) here (len: 1), and everything worked as expected:

[00:05:52 TRACE D0 A0 A8] Packet: A8 00 00 00 00 00 00 00 00 01 00 00, DMA: 0
[00:05:52 DEBUG D0 A0 A8] READ (12), sector: 0, len: 1
[00:05:52 TRACE D0 A0 A8] Seeking -> 0
[00:05:52 TRACE D0 A0 A8] PKT data xfer end
[00:05:52 TRACE D0 A0 A8]
[00:05:52 TRACE D0 A0 A8] Packet: A8 00 00 00 00 20 00 00 00 01 00 00, DMA: 0
[00:05:52 DEBUG D0 A0 A8] READ (12), sector: 32, len: 1
[00:05:52 TRACE D0 A0 A8] Seeking -> 4000
[00:05:52 TRACE D0 A0 A8] PKT data xfer end
[00:05:52 TRACE D0 A0 A8] 

In this example, the Roland SP-808 requested 9 sectors (len: 9):
[00:05:52 TRACE D0 A0 A8] Packet: A8 00 00 00 00 21 00 00 00 09 00 00, DMA: 0
[00:05:52 DEBUG D0 A0 A8] READ (12), sector: 33, len: 9


However, we can see that it also set byte count to 0x200:
3900: REG: 4, WR<-, data: 00 - Cyl Low
3901: REG: 5, WR<-, data: 02 - Cyl High

This means that the Roland SP-808 wanted to receive data in 9 blocks of 512 bytes, not one block of 4608 bytes.
If you try and send it a single blcok of 4608 bytes, it waits for 7 seconds and then sends SRST to start from the begining.

[00:05:52 TRACE D0 A0 A8] Seeking -> 4200
[00:05:59 DEBUG D0 A0 A8] Software (SRST) Reset
[00:05:59 TRACE D0 A0 A8]
[00:05:59 DEBUG D0 A0 A8]

