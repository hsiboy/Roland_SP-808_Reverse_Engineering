# An Introduction To Programming With ATA And ATAP

the standard translated geometry for all Zip drives is 512 cylinders, 12 heads,
and 32 sectors per track. LBA translation of the drive geometry results in a
translated geometry of 97 cylinders, 32 heads, and 63 sectors per track. Zip
drives using standard Zip disk geometry will be unable to read the


If you're familiar with computer maintenance procedures, you're probably familiar with IDE (Integrated Drive Electronics), the typical standard for connecting hard drives and CD-ROM drives to a PC. ATA (AT Attachment) is essentially the same thing as IDE; just a different name.

Most motherboards today have two IDE controllers built-in, designated as the primary and the secondary IDE controller. These two IDE controllers use the following standard I/O addresses:

Primary IDE controller: 1F0h to 1F7h and 3F6h to 3F7h
Secondary IDE controller: 170h to 177h and 376h to 377h

Each I/O address corresponds to a register on the IDE controller. The following is a list of each I/O address used by ATA controllers and the corresponding regiuster. (I/O addys given are for the primary IDE controller, obviously, but they correspond to the same secondary IDE controller addresses. Thus, for example, the secondary IDE controller's data register is at 170h, the secondary controller's error and features register is at 171h, and so on):

| Command | Type | Description |
| --- | --- | --- |
|`1F0`| Read and Write | Data Register|
|`1F1`| Read | Error Register|
|`1F1`| Write | Features Register|
|`1F2`| Read and Write | Sector Count Register|
|`1F3`| Read and Write | LBA Low Register|
|`1F4`| Read and Write | LBA Mid Register|
|`1F5`| Read and Write | LBA High Register|
|`1F6`| Read and Write | Drive/Head Register|
|`1F7`| Read | Status Register|
|`1F7`| Write | Command Register|
|`3F6`| Read | Alternate Status Register|
|`3F6`| Write | Device Control Register|

The status register is an 8-bit register which contains the following bits, listed in order from left to right:

| Bit | Description |
| --- | --- |
|`BSY`| Busy|
|`DRDY`| Device Ready|
|`DF`| Device Fault|
|`DSC`| Seek Complete|
|`DRQ`| Data transfer Request|
|`CORR`| Data Corrected|
|`IDX`| Index mark|
|`ERR`| Error|

The error register is also an 8-bit register, and contains the following bits, again listed in order from left to right:
| Bit| Description |
| --- | --- |
|`BBK`| Bad Block|
|`UNC`| Uncorrectable data error|
|`MC`| Media Changed|
|`IDNF`| ID mark Not Found|
|`MCR`| Media Change Requested|
|`ABRT`| Command Aborted|
|`TK0NF`| Track 0 Not Found|
|`AMNF`| Address Mark Not Found|

ATA commands are issued by writing the commands to the command register. More specifically, ATA commands are issued using the following steps:

1. Poll the status register until it indicates the device is not busy (BUSY will be set to 0)
2. Disable interrupts.
3. Poll the status register until it indicates the device is ready (DRDY will be set to 1)
4. Issue the command by outputting the command opcode to the command register
5. Re-enable interrupts.

The following program is a relatively simple assembler program to run the `ATA "IDENTIFY DRIVE"` command, and print out the results of this command to the screen.


```asm
MOV DX, 1F7h ;status register
LOOP1:
IN AL, DX ;sets AL to status register (which is 8 bits)

;If the first bit of the status register (BUSY) isn't 0, the device is busy,
;so keep looping until it isn't.

AND AL, 10000000xB
JNE LOOP1

;----------------------------------------------------------------------------

;Clear interrupts so something doesn't interrupt the drive or controller
;while this program is working.
CLI

;----------------------------------------------------------------------------

MOV DX, 1F7h ;status register again
LOOP2:
IN AL, DX ;sets AL to status register again

;If the second bit of the status register (DRDY) isn't 1, the device isn't
;ready, so keep looping until it is.

AND AL, 01000000xB
JE LOOP2

;----------------------------------------------------------------------------

MOV DX, 1F6h ;device/head register
MOV AL, 0 ;0 selects device 0 (master). 10h would select device 1 (slave).
OUT DX, AL ;selects master device

MOV DX, 1F7h ;command register
MOV AL, 0ECh ;"IDENTIFY DRIVE" command
OUT DX, AL ;sends the command!

;----------------------------------------------------------------------------

MOV DX, 1F7h ;status register
LOOP3:
IN AL, DX

AND AL, 00001000xB ;if DRQ is not high, the device doesn't have data for us
JE LOOP3 ;yet, so keep looking until it does!

;----------------------------------------------------------------------------

MOV DX, 1F0h ;data register
MOV DI, OFFSET buff ;points DI to the buffer we're using
MOV CX, 256 ;256 decimal. This controls the REP command.
CLD ;clear the direction flag so INSW increments DI (not decrements it)
REP INSW

;----------------------------------------------------------------------------

;We now have the string data in buff, so let's re-enable interrupts.

STI

;----------------------------------------------------------------------------

;...And now we can display the contents of buff!

MOV ES, SEG buff
MOV BX, OFFSET buff
MOV CX, 256 ;256 decimal
MOV AH, 2 ;"display output" option for INT 21
LOOP4:
MOV DL, [BX] ;moves the contents of the byte from "buff" into DL
INT 21h
INC BX
LOOPNZ LOOP4 ;does this 256 times, because CX was set to 256

mov ah,004C  ;terminate program
int 21h

buff db 256 DUP(?) ;buffer to hold the drive identification info
```

# ATAPI

ATAPI (ATA Packet Interface) is an extension to ATA which essentially allows SCSI commands (commands used to control SCSI devices) to be sent to ATA devices. ATAPI is used specifically for CD-ROM drives, which, when they first started appearing for computers, were almost universally SCSI. Because SCSI controllers were expensive and clunky, the SCSI command set was eventually adopted for IDE, and typical CD-ROM drives today use ATAPI. ATAPI basically uses "packets" (similar to the packet concept of computer networking as it applies to TCP/IP, for example) to send and receive data and commands. Properly speaking, ATAPI is part of the EIDE (Enhanced IDE) standard.

A packet sent to an ATAPI device which contains a command is called a command packet. These command packets are written to the data register via the ATA interface, and that's how ATAPI devices receive their commands. The command packet has a 12-byte standard format, and the first byte of the command packet contains the actual operation code. (The remaining 11 bytes supply parameter info for the command.) Note that although the command packet is 12 bytes long, the packet is sent to the ATAPI device through word writes, not byte writes. A "word" in PC assembly language is 2 bytes, so you'll actually send the 12-byte command packet in only 6 write operations.

The "operation code" value you place in the ATAPI command packet is actually a SCSI command code. You do not use ATA commands with ATAPI devices; ATAPI devices use SCSI commands. For example, the SCSI command to eject a CD-ROM drive tray is the "START/STOP UNIT" command, which is SCSI command 1Bh. Similarly, to get an ATAPI CD-ROM drive to eject, you'd send it a command packet with 1Bh for an operation code.

ATAPI contains several commands, but the most fundamental of these is the PACKET command, which has an ATAPI opcode of A0h. The first step in sending a command to an ATAPI device is to send it the PACKET command over the regular ATA command register, just as the program above sends the IDENTIFY DEVICE command. Once this PACKET command is sent, the ATAPI interface goes into a condition called HPD0: Check_Status_A State, which means that the ATA controller is to wait for 400 nanoseconds, then poll the status register until the BSY bit is zero. If the BSY bit is one, the host is supposed to keep polling the status register until the BSY bit clears.

Once the BSY bit does clear (and DRQ is set to one), the ATAPI interface changes to HPD1: Send_Packet State. In this state, the host is supposed to send the command packet to the ATA controller's data register, one byte at a time. When all the bytes of the command packet have been sent, the host is to either transition to HPD2: Check_Status_B State (if nIEN is set to one), or to HPD3: INTRQ_Wait State (if nIEN is set to zero). Note that nIEN is the second-rightmost bit of the ATA Device Control Register. You will note that this register is write-only, so you should write to this register to set nIEN before you begin sending the ATAPI packet.

If the host does transition to HPD3: INTRQ_Wait State, all it's supposed to do is wait for INTRQ to be asserted. When INTRQ is asserted, then the host shall transition to HPD2: Check_Status_B State.

The HPD2: Check_Status_B State is where things get a little hairy. This is where you check the status register, but there are a lot of condition bits you're supposed to check. First of all, the ATAPI spec specifies that "When entering this state from the HP1 ... state, the host shall wait one PIO transfer cycle time before reading the Status register. The wait may be accomplished by reading the Alternate Status register and ignoring the result."

Once that's done, start checking the status register. First of all, if BUSY is set to 1, the host is not to leave the HPD2 state. The host is supposed to remain in HPD2 until BUSY clears to zero.

Once BUSY is zero, check DRQ. If DRQ is set to one, then the host shall transition to yet another state, called the HPD4: Transfer_Data State. However, the only time you'd need to enter HPD4 is if DRQ is 1 during the HPD2 State. If DRQ is zero now, you can skip HPD4 altogether.

If both BUSY and DRQ are zero, then, the command is probably complete. Technically, there are a few other things you're supposed to check, but we won't worry about those now.

The following is an ugly program in assembler to eject a CD-ROM drive. I haven't cleaned up the code as nicely as I should, but it does work as long as you run it in real mode (what Win9x users would call "DOS mode").

```asm
MOV DX, 177h ;status register
LOOP1:
IN AL, DX ;sets AL to status register (which is 8 bits)

;If the first bit of the status register (BUSY) isn't 0, the device is busy,
;so keep looping until it isn't.

AND AL, 10000000xB
JNE LOOP1

;----------------------------------------------------------------------------

;Clear interrupts so something doesn't interrupt the drive or controller
;while this program is working.
CLI

;----------------------------------------------------------------------------

MOV DX, 177h ;status register again
LOOP2:
IN AL, DX ;sets AL to status register again

;If the second bit of the status register (DRDY) isn't 1, the device isn't
;ready, so keep looping until it is.

AND AL, 01000000xB
JE LOOP2

;----------------------------------------------------------------------------

MOV DX, 176h ;device/head register
MOV AL, 0 ;0 selects device 0 (master). 10h would select device 1 (slave).
OUT DX, AL ;selects master device

;IMPORTANT: Set nIEN before you send the PACKET command!
;Let's set nIEN to 1 so we can skip the INTRQ_Wait state.

MOV DX, 3F6h ;Device Control register
MOV AL, 00001010xB ;nIEN is the second bit from the right here
OUT DX, AL ;nIEN is now one!

MOV DX, 177h ;command register
MOV AL, 0A0h ;PACKET command
OUT DX, AL ;sends the command!

;After sending the PACKET command, the host is to wait 400 nanoseconds before
;doing anything else.
MOV CX,0FFFFh
WAITLOOP:
LOOPNZ WAITLOOP

;----------------------------------------------------------------------------

MOV DX, 177h ;status register again
LOOP3:
IN AL, DX ;sets AL to status register again

;Poll until BUSY bit is clear.

AND AL, 10000000xB
JNE LOOP3

;Also, poll until DRQ is one.
MOV DX, 177h ;status register again
LOOP4:
IN AL, DX
AND AL, 00001000xB
JE LOOP4

;----------------------------------------------------------------------------
;NOW WE START SENDING THE COMMAND PACKET!!!

MOV CX, 6 ;do this 6 times because it's 6 word writes (a word is 2 bytes)
MOV DS, SEG buff
MOV SI, OFFSET buff
;DS:SI now points to the buffer which contains our ATAPI command packet
CLD ;clear direction flag so SI gets incremented, not decremented

COMPACKLOOP: ;command packet sending loop
MOV DX, 170h ;data register

;Because we're going to need to write a word (2 bytes), we can't just use an
;8-bit register like AL. For this operation, we'll need to use the full width
;of the 16-bit accumulator AX. We'll use the LODSW opcode, which loads AX
;with whatever DS:SI points to. Not only this, but if the direction flag is
;cleared (which we did a few lines above with the CLD instruction), LODSW
;also auto-increments SI.
LODSW
OUT DX, AX ;send the current word of the command packet!!!

MOV DX, 3F6h ;Alternate Status Register
IN AL, DX ;wait one I/O cycle

LOOPNZ COMPACKLOOP

;----------------------------------------------------------------------------

;Once again, let's read the Alternate Status Register and ignore the result,
;since the spec says so.

MOV DX, 3F6h
IN AL, DX

;Okay... That's done.
;Time to poll the status register until BUSY is 0 again.

MOV DX, 177h ;status register
LOOP5:
IN AL, DX

AND AL, 10000000xB
JNE LOOP5

;BUSY is zero here.
;We're also supposed to check DRQ, but hey, screw it.

STI

;----------------------------------------------------------------------------

mov ah,004C  ;terminate program
int 21h

buff db 1Bh, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0
```

# LBA mode

## Notes on CHS and LBA Addressing.

On a PC (at least the early ones),  sectors are defined is terms of Cylinders, Heads & Sectors (CHS format). Parameters in early MS-DOS versions were passed via software interrupt INT 13H for sector reads and writes. INT 13H  designates sectors in a somewhat convoluted way (for historical reasons), parameters passed are always as follows:-

```
AH = 02h
AL = number of sectors to read/written (must be nonzero)
CH = low eight bits of cylinder number
CL = sector number 1-63 (bits 0-5)
high two bits of cylinder (bits 6-7, hard disk only)
DH = head number
DL = drive number (bit 7 set for hard disk)
ES:BX -> data buffer
```

Because only 16 heads are allowed with this format, the maxium size for a hard disk is 512MB.
This wasnt a problem for early 8 bit systems since disk capacity was always less than 512MB. 
To allow for higher disk capacities with later version of MSDOS, the PC's BIOS utilized the so called "LBA" sector addressing mode. In this case sectors are numbered on the disk as just one long number. Starting at 0 and working upwards. There are no tracks or heads.

First the drive must be told what format sectors will be addressed in. This is done by sending a key bit to the IDE Drive "Head Register". If bit 6 of this register is set to 0 then the drive expects all information to arrive in LBA mode. If bit 6 is a 1, then the drive expects all sector information to arrive in CHS format.
   

<table>
<thead>
  <tr>
    <th>Bit 7</th>
    <th>Bit 6</th>
    <th>Bit 5</th>
    <th>Bit 4</th>
    <th>Bit 3</th>
    <th>Bit2</th>
    <th>Bit 1</th>
    <th>Bit 0</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>Always 1</td>
    <td>LBA/CHS mode</td>
    <td>Always 1</td>
    <td>M/Slave</td>
    <td colspan="4">Heads 0-15</td>
  </tr>
</tbody>
</table>

if you are sending LBA or true CHS information to a drive for single sector read/write, it actually does not matter which format the drive uses/expects. In the CHS format there would just be "holes" in the LBA format array.  Where all this becomes critical is when we go to MSDOS where as sector read/write command may require a block of up to 80H contiguous sectors to be processed.  In this case the disk cannot have sector "holes".  When one track of sectors is read the next sector comes from the next head up. When all heads are used only then do we go to the next track.  In any BIOS its critical that this process is toughly tested out.  The software must religiously either follow this process or via a formula translate a LBA address number into a CHS number. 

# Registers

## IDE read/write and register description

The IDE device appears to the AT bus as a set of registers. The register selection is done with the /CS0, CS1 and A0, A1, A2 lines. Reading/writing is done with the /RD and /WR signals. I have used the 8255 port A signals to make read/write cycles on the IDE bus. What I do is the following:

### read cycle:

1. put the port B and C of the 8255 in input modus.
2. set an address and /CS0 and /CS1 signal on the port A of the 8255.
3. activate the /RD of the IDE bus by setting the equivalent bit in the port A of the 8255.
4. read the data from port B (and C) of the 8255.
5. deactivate the /RD signal on the IDE bus by resetting the equivalent bit of port A of the 8255.Back to contents

### write cycle:

1. put the port B and C of the 8255 in output modus.
2. set an address and /CS0 and /CS1 signal on the port A of the 8255.
3. set a data word (or byte) on port B (and C) of the 8255.
4. activate the /WR of the IDE bus by setting the equivalent bit in the port A of the 8255.
5. deactivate the /WR signal on the IDE bus by resetting the equivalent bit of port A of the 8255.

The only difference between 8 bits and 16 bits transfers is the following:

- In an 8-bit transfer I use only the port B of the 8255 for data transfer. When writing I put data only on the lower byte of the IDE bus; the upper byte is ignored anyway by the IDE device. When reading I read only port B of the 8255; I never even bother to look at the upper byte.

- In an 16-bit transfer, read/write to both the upper and the lower byte of the IDE bus.

The IDE device appears as the following registers:

### Data I/O register

| /CS0 | /CS1 | A2 | A1 | A0 |
| --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 0 | 0 |


This is the data I/O register. This is in fact the only 16-bits wide register of the entire IDE interface. It is used for all data block transfers from and to the IDE device.

### Error information register

| /CS0 | /CS1 | A2 | A1 | A0 |
| --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 0 | 1 |

This is the error information register when read; the write precompensation register when written. Read this register when an error is indicated in the IDE status register (see below for the IDE status register).

### Sector counter register.

| /CS0 | /CS1 | A2 | A1 | A0 |
| --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 1 | 0 |


This register could be used to make multi-sector transfers. You'd have to write the number of sectors to transfer in this register. You can use this register to pass the parameter the timeout for idle modus command.

### Start Sector Register

| /CS0 | /CS1 | A2 | A1 | A0 |
| --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 1 | 1 |

This register holds the start sector of the current track to start reading/writing to. 
For each transfer, write the start sector in this register. Note that the sector count starts at 1 and not 0 and it runs up to 256, not 255, so writing 00H results in sector number 256. Warning, all other counting in the IDE interface starts at 0.

### Cylinder Number

| /CS0 | /CS1 | A2 | A1 | A0 |
| --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 0 | 0 |

Low byte of the cylinder number. This register holds low byte of the cylinder number for a disk transfer.

| /CS0 | /CS1 | A2 | A1 | A0 |
| --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 0 | 1 |

High two bits of the cylinder number. The traditional IDE interface allows only cylinder numbers in the range 0..1023. This register gets the two upper bits of this number. Write the cylinder number's upper two bits into this register before each transfer.

### head & device select

| /CS0 | /CS1 | A2 | A1 | A0 |
| --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 1 | 0 |

Head and device select register. The bits 3..0 of this register hold the head number (0..15) for a transfer. bit 4 is to be written 0 for access to the IDE master device, and 1 for access to the IDE slave device. bits 7..5 are fixed at 101B in the traditional interface.

### Command / Status Register.

| /CS0 | /CS1 | A2 | A1 | A0 |
| --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 1 | 1 |

command/status register. When written the IDE device regards the data you write to this register as a command. When read you get the status of the IDE device. Reading this register also clears any interrupts from the IDE device to the controller.

| /CS0 | /CS1 | A2 | A1 | A0 |
| --- | --- | --- | --- | --- |
| 1 | 0 | 1 | 1 | 0 |

2nd status register/interrupt and reset register. When read this register gives you the same status byte as the primary status register. The only difference is that reading this register does not clear the interrupt from the IDE device when read. When written you can enable/disable the interrupts the IDE device generates; Also you can give a software reset to the IDE device.

| /CS0 | /CS1 | A2 | A1 | A0 |
| --- | --- | --- | --- | --- |
| 1 | 0 | 1 | 1 | 1 |

Active status of the IDE device. In this register (read-only) you can find out if the IDE master or slave is currently active and find the currently selected head number. 
Also used find out if the floppy (ZIP) is currently in the drive.

Some of these registers have bitwise meanings. I'll elaborate on that here:


### head and device register:

A write register that sets the master/slave selection and the head number.


```

bits 3..0: head number [0..15]
bit  4   : master/slave select: 0=master,1=slave
bits 7..5: fixed at 101B. This is in fact the bytes/sector
           coding. In old (MFM) controllers you could specify if
           you wanted 128,256,512 or 1024 bytes/sector. In the
           IDE world only 512 bytes/sector is supported. This bit
           pattern is a relic from the MFM controllers age. The
           bit 6 of this pattern could in fact be used to access
           a disk in LBA mode.
```
           
### Status register:

Both the primary and secondary status register use the same bit coding. The register is a read register.

```
bit 0    : error bit. If this bit is set then an error has
           occurred while executing the latest command. The error
           status itself is to be found in the error register.
bit 1    : index pulse. Each revolution of the disk this bit is
           pulsed to '1' once. I have never looked at this bit, I
           do not even know if that really happens.
bit 2    : ECC bit. if this bit is set then an ECC correction on
           the data was executed. I ignore this bit.
bit 3    : DRQ bit. If this bit is set then the disk either wants
           data (disk write) or has data for you (disk read).
bit 4    : SKC bit. Indicates that a seek has been executed with
           success. I ignore this bit.
bit 5    : WFT bit. indicates a write error has happened. I do
           not know what to do with this bit here and now. I've
           never seen it go active.
bit 6    : RDY bit. indicates that the disk has finished its
           power-up. Wait for this bit to be active before doing
           anything (execpt reset) with the disk. I once ignored
           this bit and was rewarded with a completely unusable
           disk.
bit 7    : BSY bit. This bit is set when the disk is doing
           something for you. You have to wait for this bit to
           clear before you can start giving orders to the disk.
```


### interrupt and reset register:

This register has only two bits that do something (that I know of). It is a write register.

bit 1    : IRQ enable. If this bit is '0' the disk will give and
           IRQ when it has finished executing a command. When it
           is '1' the disk will not generate interrupts.
bit 2    : RESET bit. If you pulse this bit to '1' the disk will
           execute a software reset. The bit is normally '0'. I
           do not use it because I have full software control of
           the hardware /RESET line.

### Active status register:

This is a read register. I have -up till now- ignored this register. I have only one IDE device (a disk) on my contraption.
bit 0    : master active. If this bit is set then the master IDE
           device is active.
bit 1    : slave active. If this bit is set then the slave IDE
           device is active.
bits 5..2: complement of the currently active disk head.
bit 6    : write bit. This bit is set when the device is writing.
bit 7    : in a PC environment this bit indicates if a floppy is
           present in the floppy drive. Here it has no meaning.

### error register:

The error register indicates what went wrong when a command execution results in an error. The fact that an error has occurred is indicated in the status register, the explanation is given in the error register. This is a read register.
bit 0    : AMNF bit. Indicates that an address mark was not
           found. What this means I not sure of. I have never
           seen this happen.
bit 1    : TK0NF bit. When this bit is set the drive was not able
           to find track 0 of the device. I think you will have
           to throw away the disk if this happens.
bit 2    : ABRT bit. This bit is set when you have given an
           indecent command to the disk. Mostly wrong parameters
           (wrong head number etc..) cause the disk to respond
           with error flag in the status bit set and the ABRT bit
           set. I have gotten this error a lot when I tried to
           run the disk with interrupts. Something MUST have been
           wrong with my interface program. I have not (yet)
           found what.
bit 3    : MCR bit. indicated that a media change was requested.
           What that means I do not know. I've ignored this bit
           till now.
bit 4    : IDNF bit. Means that a sector ID was not found. I have
           never seen this happen, I guess it means that you've
           requested a sector that is not there.
bit 5    : MC bit. Indicates that the media has been changed. I
           ignore this bit.
bit 6    : UNC bit. Indicates that an uncorrectable data error
           happened. Some read or write errors could provoke
           this. I have never seen it happen.
bit 7    : reserved.






## Disk size limitations on the IDE bus and LBA mode

At first (MSDOS versions till 3.3) the disk interface was not able to access more than 32MB on one volume. That was a limitation of the MSDOS file system rather than of the disk interface. The same DOS version that was unable to access bigger partitions than 32MB *WAS* able to access 650MB CDROMs. The limit came from the fact that each disk sector (512 bytes) was registered in the FAT in a 16-bits word. The total partition size was limited by the fact that only 65536 sectors could be addressed. The partition size was thus limited to 65536 x 512 bytes = 32 MBytes.

Later -as the disks became larger- the disk interface itself ran into its limits. The interface I describe here has room for 16 heads, 256 sectors per track and only 1024 cylinders. With the standard sector size of 512 bytes that leaves you a maximum disk size of 16 x 256 x 1024 x 512 = 2048 MBytes. That is a real limitation of the IDE interface as I describe it here. It can not access more than some 2 GBytes of disk space.

This was overcome by introducing the so-called LBA mode. In LBA mode the sectors are simply numbered from 0 to -big-. The lowest byte of the LBA sector number is written into the sector number register, the middle 16 bits of the LBA sector number are written in the cylinder number registers (low and high, all 16 bits are used). The highest 4 bits of the LBA sector number are written in the head and device register. That gives you 28 bits of LBA sector number. The sector size was again fixed at 512bytes, so in LBA modus you have access to: 2^28 x 512 = 1.37 E 11 (some 137.4 gigabytes) of disk space. This LBA modus has been made mandatory for all new disks (in the ATA-3 spec.) That should keep the disk makers busy for some while to come... If you want to connect a disk larger than 2 GBytes to this IDE interface you too will have to use the LBA modus. How to do that: the bit 6 of the head and device register is set to indicate that LBA modus is used (the fixed pattern of 101B in the bits 7..5 of the head and device register is to be changed into 111B). All other manipulation of the IDE interface is the same for Sector/Head/Cylinder modus and LBA modus.

All other limits in the MSDOS/Windows-whatever disk interface must be due to the BIOS implementation or the file system used. I can find no reason in the IDE definition for 512 MB limits or 8 GB limits at all.



IDE registers usage

1. Before doing anything with a device you have to wait till it indicates that it is ready (RDY bit in the status register)
2. Next you load the parameters of a command into the appropriate registers. For read/write commands that comes down to writing the cylinder/head/sector numbers into the registers.

3. You issue a read or write command.
4. You wait till the device signals that it is ready for data transfer (DRQ in the status register).
5. Feed the device data (for write) or get the data from the device (for read). In case of a write you could wait for the operation to complete and read the status register to find out what has become of your data.
6. Finish!! That's all folks! The IDE interface is a surprisingly simple thing to get to work. If only I had an IDE disk and this kind of information when I was still programming my MSX-computer I'd have had a harddisk connected to it in no time.


## IDE commands

Note: When giving a command you first have to wait for device ready, next put the command parameters in the registers and only then can you give a command (by writing a command byte to the command register). The disk will start executing the command right after you've written the command into the command register.

IDE command:    Description:
------------    ------------

1XH             recalibrate the disk. NB: 1XH means that the lower
                nibble of the command byte is a don't care. All
                commands 10H..1FH will result in a recalibrate
                disk command being executed. This command has no
                parameters. You simply write the command code to
                the command register and wait for ready status to
                become active again.

20H             Read sector with retry. NB: 21H = read sector
                without retry. For this command you have to load
                the complete circus of cylinder/head/sector
                first. When the command completes (DRQ goes
                active) you can read 256 words (16-bits) from the
                disk's data register.

30H             Write sector (with retry; 31H = without retry).
                Here too you have to load cylinder/head/sector.
                Then wait for DRQ to become active. Feed the disk
                256 words of data in the data register. Next the
                disk starts writing. When BSY goes not active you
                can read the status from the status register.

7XH             Seek. This normally does nothing on modern IDE
                drives. Modern drives do not position the head if
                you do not command a read or write.

ECH             Identify drive. This command prepares a buffer
                (256 words) with information about the drive. If
                you want the details either look closely at the
                interface program I will add at the end of this
                description or get the ATA-3 document. To use it:
                simply give the command, wait for DRQ and read
                the 256 words from the drive. I have found that
                the modern drives I used give nice information
                about number of heads,sectors,cylinders etc...
                One of the disks I tried (a Miniscribe 8051A)
                gave wrong answers in this buffer. The disk is
                actually a 4 heads/28 sectors disk. It should be
                used in a translated modus with 5 heads/17
                sectors. In the ident drive response it reported
                as 4 heads/28 sectors and it will NOT work in
                that modus. Two other disks (a Quantum 127 MB
                disk and a Western Digital 212 MB disk) report
                nicely. If not for the Miniscribe I would use the
                parameters reported to auto-config the interface
                to match the disk configuration.

E0H             Spins down the drive at once. No parameters. My
                Miniscribe 8051A does not respond to this
                command, the other disks do execute this command.

E1H             Spins up the drive again. Same remarks as E0H
                command.

E2H and E3H     Auto-power-down the disk. Write in the sector
                count register the time (5 seconds units) of
                non-activity after which the disk will spin-down.
                Write the command to the command register and the
                disk is set in an auto-power-save modus. The disk
                will automatically spin-up again when you issue
                read/write commands. E2H will spin-down, E3H will
                keep the disk spinning after the command has been
                given. Example: write 10H in the sector count
                register, give command E2H and the disk will
                spin-down after 80 seconds of non-activity. BTW:
                You can use this command easily on a PC disk too.
                The harddisk of the computer I am working on now
                gets this exact command at boot. That saves a lot
                of noise when I'm typing long stories like this
                one.

F2H and F3H     The same as E2H and E3H, only the unit in the
                sector count register is interpreted as 0.1 sec
                units. I have not tried this command. I think it
                will work (the E0H/E1H/E2H/E3H commands work, why
                should this one not work?)
                
                
                
------

Part of the CD-ROM ATAPI function set. If the IDE device only supports packets with 12 bytes length the last 4 bytes are not sent. The great majority of tested devices use 12 byte.

```
  0x1B,0x00,0x00,0x00,0x02,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, // idx=0 Open tray
  0x1B,0x00,0x00,0x00,0x03,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, // idx=16 Close tray
  0x1B,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, // idx=32 Stop unit
  0x47,0x00,0x00,0x10,0x28,0x05,0x4C,0x1A,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, // idx=48 Start PLAY
  0x4B,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, // idx=64 PAUSE play
  0x4B,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,0x00,0x00,0x00,0x00,0x00,0x00,0x00, // idx=80 RESUME play
  0x43,0x02,0x00,0x00,0x00,0x00,0x00,0xFF,0xFF,0x00,0x00,0x00,0x00,0x00,0x00,0x00, // idx=96 Read TOC
  0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, // idx=112 unit ready
  0x5A,0x00,0x01,0x00,0x00,0x00,0x00,0xFF,0xFF,0x00,0x00,0x00,0x00,0x00,0x00,0x00, // idx=128 mode sense
  0x42,0x02,0x40,0x01,0x00,0x00,0x00,0xFF,0xFF,0x00,0x00,0x00,0x00,0x00,0x00,0x00, // idx=144 rd subch.  
  0x03,0x00,0x00,0x00,0xFF,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, // idx=160 req. sense
  0x4E,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00  // idx=176 Stop disk
  ```
  
  ------


```C
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>

int main() {
  // Get the list of all block devices.
  char *block_devices = getenv("BLOCK_DEVICES");
  if (block_devices == NULL) {
    perror("getenv");
    exit(1);
  }

  // Iterate over the list of block devices.
  char *device;
  for (device = strtok(block_devices, ":"); device != NULL; device = strtok(NULL, ":")) {
    // Open the device file.
    int fd = open(device, O_RDWR);
    if (fd < 0) {
      perror("open");
      continue;
    }

    // Send the IDENTIFY command.
    char cmd = 0xEC;
    write(fd, &cmd, 1);

    // Read the response.
    char response[512];
    read(fd, response, 512);

    // Decode word 0 into English.
    char vendor_id[8];
    memcpy(vendor_id, response, 8);
    vendor_id[8] = '\0';
    char product_id[16];
    memcpy(product_id, response + 8, 16);
    product_id[16] = '\0';
    char revision_id[8];
    memcpy(revision_id, response + 24, 8);
    revision_id[8] = '\0';

    // Print the results.
    printf("Device: %s\n", device);
    printf("Vendor ID: %s\n", vendor_id);
    printf("Product ID: %s\n", product_id);
    printf("Revision ID: %s\n", revision_id);

    // Close the device file.
    close(fd);
  }

  return 0;
}
```
 
---

```C
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <libusb-1.0/libusb.h>

int main() {
  // Get the list of all USB devices.
  struct libusb_device **devices;
  int num_devices = libusb_get_device_list(NULL, &devices);
  if (num_devices < 0) {
    perror("libusb_get_device_list");
    exit(1);
  }

  // Iterate over the list of USB devices.
  for (int i = 0; i < num_devices; i++) {
    struct libusb_device *device = devices[i];

    // Get the device descriptor.
    struct libusb_device_descriptor descriptor;
    int err = libusb_get_device_descriptor(device, &descriptor);
    if (err < 0) {
      perror("libusb_get_device_descriptor");
      continue;
    }

    // Check if the device is a storage device.
    if (descriptor.bDeviceClass != LIBUSB_CLASS_STORAGE) {
      continue;
    }

    // Open the device.
    int fd = libusb_open(device, 0);
    if (fd < 0) {
      perror("libusb_open");
      continue;
    }

    // Send the IDENTIFY command.
    char cmd = 0xEC;
    write(fd, &cmd, 1);

    // Read the response.
    char response[512];
    read(fd, response, 512);

    // Decode word 0 into English.
    char vendor_id[8];
    memcpy(vendor_id, response, 8);
    vendor_id[8] = '\0';
    char product_id[16];
    memcpy(product_id, response + 8, 16);
    product_id[16] = '\0';
    char revision_id[8];
    memcpy(revision_id, response + 24, 8);
    revision_id[8] = '\0';

    // Print the results.
    printf("Device: %04x:%04x:%04x\n", descriptor.idVendor, descriptor.idProduct, descriptor.bcdDevice);
    printf("Vendor ID: %s\n", vendor_id);
    printf("Product ID: %s\n", product_id);
    printf("Revision ID: %s\n", revision_id);

    // Close the device.
    libusb_close(fd);
  }

  // Free the list of devices.
  libusb_free_device_list(devices, 1);

  return 0;
}
```
