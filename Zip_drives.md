# Zip Drives


The ATAPI (ATA Packet Interface) Zip drive is a type of removable storage device that follows the ATAPI protocol, which is an extension of the ATA (Advanced Technology Attachment) standard. The Zip drive was developed by Iomega Corporation and gained popularity as a high-capacity storage solution in the late 1990s and early 2000s.

1. Interface: The ATAPI Zip drive connects to the host computer using an IDE (Integrated Drive Electronics) interface, also known as ATA. It typically utilizes a 40-pin IDE connector for data and control signals.

2. Physical Media: The Zip drive uses removable Zip disks as the storage medium. Zip disks were available in various capacities, most commonly 100MB, 250MB, and later 750MB. These disks are similar in appearance to floppy disks but housed in a more robust and durable cartridge.

3. Command Set: The ATAPI Zip drive implements a command set that is compatible with the ATAPI specification. It utilizes various commands such as read, write, seek, format, eject, and others to perform operations on the Zip disks.

4. Capacity and Block Size: The capacity of an ATAPI Zip drive depends on the type of Zip disk used. The most common capacity was 100MB, but later models supported larger capacities such as 250MB and 750MB. The block size used for data transfer is typically 512 bytes.

5. Transfer Modes: The ATAPI Zip drive supports various transfer modes defined by the ATA/ATAPI standards, including PIO (Programmed Input/Output) modes and DMA (Direct Memory Access) modes. These modes determine the data transfer rates and the method by which data is exchanged between the drive and the host.

6. Plug-and-Play: The ATAPI Zip drive follows the Plug-and-Play standard, which allows the drive to be automatically detected and configured by the host operating system without the need for manual configuration or driver installation.

7. Compatibility: ATAPI Zip drives are designed to be compatible with a wide range of operating systems, including Windows, Macintosh, and Linux. They can be used as removable storage devices for data backup, file transfer, and archiving purposes.

Overall, the ATAPI Zip drive provided a convenient and high-capacity storage solution for personal computers during its prime. While it has become less prevalent in recent years, it remains a part of computing history and a notable example of removable storage technology.

---


## 40 pin IDE connector

| _ | _ | _ | _ | _  | _  | _  | _  | _  | #  | #  | _  | _  | _  | _  | _  | _  | _  | _  | _  |
|---|---|---|---|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
| 1 | 3 | 5 | 7 | 9  | 11 | 13 | 15 | 17 | 19 | 21 | 23 | 25 | 27 | 29 | 31 | 33 | 35 | 37 | 39 |
| 2 | 4 | 6 | 8 | 10 | 12 | 14 | 16 | 18 | X | 22 | 24 | 26 | 28 | 30 | 32 | 34 | 36 | 38 | 40 |

### Pinout

| Pin    | Function          |
|--------|-------------------|
| Pin 1  | Reset             |
| Pin 2  | Ground            |
| Pin 3  | Data 7            |
| Pin 4  | Data 8            |
| Pin 5  | Data 6            |
| Pin 6  | Data 9            |
| Pin 7  | Data 5            |
| Pin 8  | Data 10           |
| Pin 9  | Data 4            |
| Pin 10 | Data 11           |
| Pin 11 | Data 3            |
| Pin 12 | Data 12           |
| Pin 13 | Data 2            |
| Pin 14 | Data 13           |
| Pin 15 | Data 1            |
| Pin 16 | Data 14           |
| Pin 17 | Data 0            |
| Pin 18 | Data 15           |
| Pin 19 | Ground            |
| Pin 20 | Key.              |
| Pin 21 | DDRQ              |
| Pin 22 | Ground            |
| Pin 23 | I/O write         |
| Pin 24 | Ground            |
| Pin 25 | I/O read          |
| Pin 26 | Ground            |
| Pin 27 | IOCHRDY           |
| Pin 28 | Cable select      |
| Pin 29 | DDACK             |
| Pin 30 | Ground            |
| Pin 31 | IRQ               |
| Pin 32 | No connect        |
| Pin 33 | Addr 1            |
| Pin 34 | GPIO_DMA66_Detect |
| Pin 35 | Addr 0            |
| Pin 36 | Addr 2            |
| Pin 37 | Chip select 1P    |
| Pin 38 | Chip select 3P    |
| Pin 39 | Activity          |
| Pin 40 | Ground            |

----

## ASPI Commands

| Opcode |                  Name                 | Iomega Zip |
|:------:|:-------------------------------------:|:----------:|
| 00h    | Test Unit Ready                       |            |
| 01h    | Rewind                                |            |
| 02h    | Rezero Unit                           |	  TRUE    |
| 03h    | Request Sense                         |            |
| 04h    | FormatUnit		                         |            |
| 05h    | ReadBlkLimits		                     |            |
| 05h    | ReadSectorIDs		                     |    TRUE    |
| 06h    | NonSenseData		                       |    TRUE    |
| 07h    | ReassignBlocks		                     |    TRUE    |
| 08h    | Read			                             |            |
| 0Ah    | Write			                           |	          |
| 0Bh    | Seek			                             |            |
| 0Ch    | CartProtect	                         | 	 TRUE     |
| 10h    | WriteFilemarks		                     |            |
| 11h    | Space			                           |	          |
| 12h    | Inquiry		                           |	          |
| 15h    | ModeSelect                         	 |	          |
| 16h    | ReserveUnit		                       |	          |
| 17h    | ReleaseUnit		                       |	          |
| 19h    | Erase			                           |	          |
| 1Ah    | ModeSense		                         |	          |
| 1Bh    | LoadUnload		                         |	          |
| 1Bh    | StartStopUnit		                      |   TRUE |
| 1Dh    | SendDiagnostic		        | |
| 1Eh    | PreventAllow		|  TRUE |
| 22h    | TranslateLBA		|  TRUE |
| 24h    | FormatTest		|   TRUE |
| 25h    | ReadCapacity		| |
| 28h    | ReadMany		|   TRUE |
| 2Ah    | WriteMany		|   TRUE |
| 2Bh    | Locate			| |
| 2Bh    | SeekMany		|   TRUE |
| 2Fh    | Verify			|   TRUE |
| 34h    | ReadPosition		| |
| 35h    | SynchCache		|   TRUE |
| 37h    | ReadDefectData		|   TRUE |
| 3Bh    | WriteBuffer		| 	 TRUE |
| 3Ch    | ReadBuffer		|   TRUE |
| 3Eh    | ReadLong		|   TRUE |
| 3Fh    | WriteLong		|   TRUE |
| 43h    | ReadToc	| |
| E3h    | WriteFieldFormat	| 	 TRUE |

----

## Iomega Zip Drive Inquiry (12h) Data
The Iomega Zip drive is a SCSI direct access device with removable media. The data returned from an Inquiry
command is shown in below:

<table>
<thead>
  <tr>
    <th>Byte #</th>
    <th>Bit 7</th>
    <th>Bit 6</th>
    <th>Bit 5</th>
    <th>Bit 4</th>
    <th>Bit 3</th>
    <th>Bit 2</th>
    <th>Bit 1</th>
    <th>Bit 0</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>0</td>
    <td colspan="3">Peripheral qualifier (0)</td>
    <td colspan="5">Device type code (0)</td>
  </tr>
  <tr>
    <td>1</td>
    <td>RMB (1)</td>
    <td colspan="7">Device type modifier (0)</td>
  </tr>
  <tr>
    <td>2</td>
    <td colspan="2">ISO version (0)</td>
    <td colspan="3">ECMA version (0)</td>
    <td colspan="3">ANSI approved version (2)</td>
  </tr>
  <tr>
    <td>3</td>
    <td>AENC (0)</td>
    <td>TrmiOP (0)</td>
    <td colspan="2">Reserved</td>
    <td colspan="4">Response Data Format (2)</td>
  </tr>
  <tr>
    <td>4</td>
    <td colspan="8">Additional data length (117)</td>
  </tr>
  <tr>
    <td>5</td>
    <td colspan="8">Reserved</td>
  </tr>
  <tr>
    <td>6</td>
    <td colspan="8">Reserved</td>
  </tr>
  <tr>
    <td>7</td>
    <td>RelAdr (0)</td>
    <td>WBus32 (0)</td>
    <td>WBus16 (0)</td>
    <td>Sync (0)</td>
    <td>Linked (0)</td>
    <td>Reserved</td>
    <td>CmdQue (0)</td>
    <td>SftRe (0)</td>
  </tr>
  <tr>
    <td>8-15</td>
    <td colspan="8">Vendor identification string ("IOMEGA")</td>
  </tr>
  <tr>
    <td>16-31</td>
    <td colspan="8">Product identification string ("ZIP 100")</td>
  </tr>
  <tr>
    <td>32-35</td>
    <td colspan="8">Product revision level string ("N.38")</td>
  </tr>
  <tr>
    <td>36-55</td>
    <td colspan="8">Vendor-specific information string ("05/09/96")</td>
  </tr>
  <tr>
    <td>56-95</td>
    <td colspan="8">Reserved</td>
  </tr>
  <tr>
    <td>95-end</td>
    <td colspan="8">Vendor-specific data ("(c) Copyright IOMEGA 1995")</td>
  </tr>
</tbody>
</table>


The inquiry data returned (shown in parenthesises above) tells us that this is a direct access device with removable media. It conforms to the ANSI standard for SCSI-2, and the data format also conforms to SCSI-2. It does not support 32-bit or 16-bit Wide SCSI, synchronous data transfer, linked commands, or command queumg. 
The Vendor and Product identification fields confi1m the make and model, and the revision string reveals the product revision level. The vendor-specific fields contain a manufacture date and a copyright notice.
An inquiry with the EVPD flag set and a page code of OOH should return a list of vital product information code pages the drive supports.
However, the command fails with error codes indicating an illegal request. This device does not support the vital product data feature.

---- 

## Iomega Mode Page (1Ah)
Let's revisit the Iomega Zip drive for a simple example of mode page information. We 'll use the 6-byte Mode Sense command to query the
drive for default information, requesting all available mode pages. The CDB looks like this: 

<table>
<thead>
  <tr>
    <th>Byte #</th>
    <th>Bit 7</th>
    <th>Bit 6</th>
    <th>Bit 5</th>
    <th>Bit 4</th>
    <th>Bit 3</th>
    <th>Bit 2</th>
    <th>Bit 1</th>
    <th>Bit 0</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>0</td>
    <td colspan="8">Op Code (1Ah)</td>
  </tr>
  <tr>
    <td>1</td>
    <td colspan="3">Logical Unit Number (0)</td>
    <td>Reserved</td>
    <td>DBD (1)</td>
    <td colspan="3">Reserved</td>
  </tr>
  <tr>
    <td>2</td>
    <td colspan="2">PC (2)</td>
    <td colspan="6">Page Code (3Fh)</td>
  </tr>
  <tr>
    <td>3</td>
    <td colspan="8">Reserved</td>
  </tr>
  <tr>
    <td>4</td>
    <td colspan="8">Allocation Length</td>
  </tr>
  <tr>
    <td>5</td>
    <td colspan="8">Control Field</td>
  </tr>
</tbody>
</table>

The command returns the following data:

<table>
<thead>
  <tr>
    <th>Byte #</th>
    <th>Bit 7</th>
    <th>Bit 6</th>
    <th>Bit 5</th>
    <th>Bit 4</th>
    <th>Bit 3</th>
    <th>Bit 2</th>
    <th>Bit 1</th>
    <th>Bit 0</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>0</td>
    <td colspan="8">Mode Data Length (0x25)</td>
  </tr>
  <tr>
    <td>1</td>
    <td colspan="8">Medium Type (0)</td>
  </tr>
  <tr>
    <td>2</td>
    <td colspan="8">Device Specific Parameters (0)</td>
  </tr>
  <tr>
    <td>3</td>
    <td colspan="8">Block descriptor length (8)</td>
  </tr>
</tbody>
</table>

The Data length field tells us that 37 (0x25) bytes follow.
The 0 in the Medium type field tells us the information is for the default medium type (a zip disk). 
The block descriptor length tells us that a single 8-byte block descriptor follows .
For the Zip drive, a direct access device, the device-specific parameter consists of coded bit fields.

Zip Drive Device-Specific Parameter

| Bit 7 | Bits 5-6 | Bit 4 | Bits 0-3 |
|:-----:|:--------:|:-----:|:--------:|
| WP    | Reserved | DPO/FUA | Reserved |

The WP flag in Bit 7 indicates whether the medium is write-protected. 
The DPO/FUA flag indicates whether the unit supports certain caching options for read requests.
A block descriptor follows the header:

<table>
<thead>
  <tr>
    <th>Byte #</th>
    <th>Bit 7</th>
    <th>Bit 6</th>
    <th>Bit 5</th>
    <th>Bit 4</th>
    <th>Bit 3</th>
    <th>Bit 2</th>
    <th>Bit 1</th>
    <th>Bit 0</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>0</td>
    <td colspan="8">Density code (0)</td>
  </tr>
  <tr>
    <td>1-3</td>
    <td colspan="8">Number of blocks (0)</td>
  </tr>
  <tr>
    <td>4</td>
    <td colspan="8">Reserved</td>
  </tr>
  <tr>
    <td>5-6</td>
    <td colspan="8">Block length (0x200)</td>
  </tr>
</tbody>
</table>

The Density code is not defined for direct access devices, so it contains no useful information. 
Because the Number of blocks field is 0, we know that the information in this descriptor applies to all the remaining blocks on the medium.
The Block length is 512 (0x200) bytes, according to this descriptor. *Note* This field appears in big-endian order, as 0x20 0xOO in bytes 5 and 6. A common pitfall in SCSI programming on Intel platforms is forgetting to correct byte order when reading data fields.
Three mode pages follow the descriptor. 
The first is an error recovery page (01h), followed by a disconnect-reconnect page (02h) and a vendor specific page (2Fh). 

Let's look at the error recovery page.

<table>
<thead>
  <tr>
    <th>Byte #</th>
    <th>Bit 7</th>
    <th>Bit 6</th>
    <th>Bit 5</th>
    <th>Bit 4</th>
    <th>Bit 3</th>
    <th>Bit 2</th>
    <th>Bit 1</th>
    <th>Bit 0</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>0</td>
    <td>PS (0)</td>
    <td>Reserved</td>
    <td colspan="6">Page Code (01h)</td>
  </tr>
  <tr>
    <td>1</td>
    <td colspan="8">Page Length (6)</td>
  </tr>
  <tr>
    <td>2</td>
    <td>AWRE (1)</td>
    <td>ARRE (1)</td>
    <td>TB (0)</td>
    <td>RC (0)</td>
    <td>EER (1)</td>
    <td>PER (0)</td>
    <td>DTE (0)</td>
    <td>DCR (0)</td>
  </tr>
  <tr>
    <td>3</td>
    <td colspan="8">Read retry count (0)</td>
  </tr>
  <tr>
    <td>4</td>
    <td colspan="8">Correction span (0)</td>
  </tr>
  <tr>
    <td>5</td>
    <td colspan="8">Head offset count (0)</td>
  </tr>
  <tr>
    <td>6</td>
    <td colspan="8">Data strobe offset count (0)</td>
  </tr>
  <tr>
    <td>7</td>
    <td colspan="8">Reserved</td>
  </tr>
</tbody>
</table>

The PS field value of 0 tells us this page cannot be saved in non-volatile memory. The Zip drive does not support saved pages, therefore a Mode Sense query requesting saved pages will return an error.
The normal page length for error recovery data is 10 bytes. Note that the length returned by the Zip driv is only 6 bytes.
The third byte in this page contains an assortment of bit flags for error recovery options. Automatic read and write real location (AWRE and ARRE) is supported for defective data blocks. The Enable Early Recovery (EER) flag indicates that the device will use the most expedient error recovery method available. The other fields tell us that this device does not report recovered errors, terminate a data phase when an error occurs, or use error correction codes for recovery.

From a programmer's perspective, this is important information.
Knowing how a device deals with errors drives the kinds of error handling code you build into your software.


---- 



## ATA Commands

| Opcode |                  Name                 |  Transfer  | Parameters |       Standard       |
|:------:|:-------------------------------------:|:----------:|:----------:|:--------------------:|
| 00     | NOP                                   | none       | 8-bit      | ATA-1 to present     |
| 01     |                                       |            |            |                      |
| 02     |                                       |            |            |                      |
| 03     | CFA REQUEST EXTENDED ERROR CODE       | none       | 8-bit      | ATA-4 to present     |
| 04     |                                       |            |            |                      |
| 05     |                                       |            |            |                      |
| 06     | DATA SET MANAGEMENT                   | DMA        | 16-bit     | ACS-2 to present     |
| 07     | DATA SET MANAGEMENT XL                | DMA        | 16-bit     | ACS-4 to present     |
| 08     | DEVICE RESET                          | none       | 8-bit      | ATA-3 to ACS-3       |
| 09     |                                       |            |            |                      |
| 0A     |                                       |            |            |                      |
| 0B     | REQUEST SENSE DATA EXT                | none       | 16-bit     | ACS-2 to present     |
| 0C     |                                       |            |            |                      |
| 0D     |                                       |            |            |                      |
| 0E     |                                       |            |            |                      |
| 0F     |                                       |            |            |                      |
| 10     | RECALIBRATE                           | none       | 8-bit      | IBM PC/AT to ATA-3   |
| 11     | RECALIBRATE                           | none       | 8-bit      | IBM PC/AT to ATA-2   |
| 12     | GET PHYSICAL ELEMENT STATUS           | DMA        | 16-bit     | ACS-4 to present     |
| 12     | RECALIBRATE                           | none       | 8-bit      | IBM PC/AT to ATA-2   |
| 13     | RECALIBRATE                           | none       | 8-bit      | IBM PC/AT to ATA-2   |
| 14     | RECALIBRATE                           | none       | 8-bit      | IBM PC/AT to ATA-2   |
| 15     | RECALIBRATE                           | none       | 8-bit      | IBM PC/AT to ATA-2   |
| 16     | RECALIBRATE                           | none       | 8-bit      | IBM PC/AT to ATA-2   |
| 17     | RECALIBRATE                           | none       | 8-bit      | IBM PC/AT to ATA-2   |
| 18     | RECALIBRATE                           | none       | 8-bit      | IBM PC/AT to ATA-2   |
| 19     | RECALIBRATE                           | none       | 8-bit      | IBM PC/AT to ATA-2   |
| 1A     | RECALIBRATE                           | none       | 8-bit      | IBM PC/AT to ATA-2   |
| 1B     | RECALIBRATE                           | none       | 8-bit      | IBM PC/AT to ATA-2   |
| 1C     | RECALIBRATE                           | none       | 8-bit      | IBM PC/AT to ATA-2   |
| 1D     | RECALIBRATE                           | none       | 8-bit      | IBM PC/AT to ATA-2   |
| 1E     | RECALIBRATE                           | none       | 8-bit      | IBM PC/AT to ATA-2   |
| 1F     | RECALIBRATE                           | none       | 8-bit      | IBM PC/AT to ATA-2   |
| 20     | READ SECTOR(S)                        | PIO        | 8-bit      | IBM PC/AT to present |
| 21     | READ SECTOR(S) (without retry)        | PIO        | 8-bit      | IBM PC/AT to ATA-4   |
| 22     | READ LONG                             | PIO        | 8-bit      | IBM PC/AT to ATA-3   |
| 23     | READ LONG (without retry)             | PIO        | 8-bit      | IBM PC/AT to ATA-3   |
| 24     | READ SECTOR(S) EXT                    | PIO        | 16-bit     | ATA-6 to present     |
| 25     | READ DMA EXT                          | DMA        | 16-bit     | ATA-6 to present     |
| 26     | READ DMA QUEUED EXT                   | queued DMA | 16-bit     | ATA-6 to ATA8-ACS    |
| 27     | READ NATIVE MAX ADDRESS EXT           | none       | 16-bit     | ATA-6 to ACS-2       |
| 28     |                                       |            |            |                      |
| 29     | READ MULTIPLE EXT                     | PIO        | 16-bit     | ATA-6 to ACS-3       |
| 2A     | READ STREAM DMA EXT                   | DMA        | 16-bit     | ATA-7 to present     |
| 2B     | READ STREAM EXT                       | PIO        | 16-bit     | ATA-7 to present     |
| 2C     |                                       |            |            |                      |
| 2D     |                                       |            |            |                      |
| 2E     |                                       |            |            |                      |
| 2F     | READ LOG EXT                          | PIO        | 16-bit     | ATA-6 to present     |
| 30     | WRITE SECTOR(S)                       | PIO        | 8-bit      | IBM PC/AT to present |
| 31     | WRITE SECTOR(S) (without retry)       | PIO        | 8-bit      | IBM PC/AT to ATA-4   |
| 32     | WRITE LONG                            | PIO        | 8-bit      | IBM PC/AT to ATA-3   |
| 33     | WRITE LONG (without retry)            | PIO        | 8-bit      | IBM PC/AT to ATA-3   |
| 34     | WRITE SECTOR(S) EXT                   | PIO        | 16-bit     | ATA-6 to present     |
| 35     | WRITE DMA EXT                         | DMA        | 16-bit     | ATA-6 to present     |
| 36     | WRITE DMA QUEUED EXT                  | queued DMA | 16-bit     | ATA-6 to ATA8-ACS    |
| 37     | SET MAX ADDRESS EXT                   | none       | 16-bit     | ATA-6 to ACS-2       |
| 38     | CFA WRITE SECTORS WITHOUT ERASE       | PIO        | 8-bit      | ATA-4 to present     |
| 39     | WRITE MULTIPLE EXT                    | PIO        | 16-bit     | ATA-6 to ACS-3       |
| 3A     | WRITE STREAM DMA EXT                  | DMA        | 16-bit     | ATA-7 to present     |
| 3B     | WRITE STREAM EXT                      | PIO        | 16-bit     | ATA-7 to present     |
| 3C     | WRITE VERIFY                          | PIO        | 8-bit      | ATA-1 to ATA-3       |
| 3D     | WRITE DMA FUA EXT                     | DMA        | 16-bit     | ATA-7 to present     |
| 3E     | WRITE DMA QUEUED FUA EXT              | queued DMA | 16-bit     | ATA-7 to ATA8-ACS    |
| 3F     | WRITE LOG EXT                         | PIO        | 16-bit     | ATA-6 to present     |
| 40     | READ VERIFY SECTOR(S)                 | none       | 8-bit      | IBM PC/AT to present |
| 41     | READ VERIFY SECTOR(S) (without retry) | none       | 8-bit      | IBM PC/AT to ATA-4   |
| 42     | READ VERIFY SECTOR(S) EXT             | none       | 16-bit     | ATA-6 to present     |
| 43     |                                       |            |            |                      |
| 44     | ZERO EXT                              | none       | 16-bit     | ACS-4 to present     |
| 45     | WRITE UNCORRECTABLE EXT               | none       | 16-bit     | ATA8-ACS to present  |
| 46     |                                       |            |            |                      |
| 47     | READ LOG DMA EXT                      | DMA        | 16-bit     | ATA8-ACS to present  |
| 48     |                                       |            |            |                      |
| 49     |                                       |            |            |                      |
| 4A     | ZAC Management In                     | DMA        | 16-bit     | ACS-4 to present     |
| 4B     |                                       |            |            |                      |
| 4C     |                                       |            |            |                      |
| 4D     |                                       |            |            |                      |
| 4E     |                                       |            |            |                      |
| 4F     |                                       |            |            |                      |
| 50     | FORMAT TRACK                          | PIO        | 8-bit      | IBM PC/AT to ATA-3   |
| 51     | CONFIGURE STREAM                      | none       | 16-bit     | ATA-7 to present     |
| 52     |                                       |            |            |                      |
| 53     |                                       |            |            |                      |
| 54     |                                       |            |            |                      |
| 55     |                                       |            |            |                      |
| 56     |                                       |            |            |                      |
| 57     | WRITE LOG DMA EXT                     | DMA        | 16-bit     | ATA8-ACS to present  |
| 58     |                                       |            |            |                      |
| 59     |                                       |            |            |                      |
| 5A     |                                       |            |            |                      |
| 5B     | TRUSTED NON-DATA                      | none       | 8-bit      | ACS-2 to present     |
| 5C     | TRUSTED RECEIVE                       | PIO        | 8-bit      | ATA8-ACS to present  |
| 5D     | TRUSTED RECEIVE DMA                   | DMA        | 8-bit      | ATA8-ACS to present  |
| 5E     | TRUSTED SEND                          | PIO        | 8-bit      | ATA8-ACS to present  |
| 5F     | TRUSTED SEND DMA                      | DMA        | 8-bit      | ATA8-ACS to present  |
| 60     | READ FPDMA QUEUED                     | queued DMA | 16-bit     | ATA8-ACS to present  |
| 61     | WRITE FPDMA QUEUED                    | queued DMA | 16-bit     | ATA8-ACS to present  |
| 62     |                                       |            |            |                      |
| 63     | NCQ NON-DATA                          | none       | 16-bit     | ACS-3 to present     |
| 64     | SEND FPDMA QUEUED                     | queued DMA | 16-bit     | ACS-3 to present     |
| 65     | RECEIVE FPDMA QUEUED                  | queued DMA | 16-bit     | ACS-3 to present     |
| 66     |                                       |            |            |                      |
| 67     |                                       |            |            |                      |
| 68     |                                       |            |            |                      |
| 69     |                                       |            |            |                      |
| 6A     |                                       |            |            |                      |
| 6B     |                                       |            |            |                      |
| 6C     |                                       |            |            |                      |
| 6D     |                                       |            |            |                      |
| 6E     |                                       |            |            |                      |
| 6F     |                                       |            |            |                      |
| 70     | SEEK                                  | none       | 8-bit      | IBM PC/AT to ATA-6   |
| 71     | SEEK                                  | none       | 8-bit      | IBM PC/AT to ATA-2   |
| 72     | SEEK                                  | none       | 8-bit      | IBM PC/AT to ATA-2   |
| 73     | SEEK                                  | none       | 8-bit      | IBM PC/AT to ATA-2   |
| 74     | SEEK                                  | none       | 8-bit      | IBM PC/AT to ATA-2   |
| 75     | SEEK                                  | none       | 8-bit      | IBM PC/AT to ATA-2   |
| 76     | SEEK                                  | none       | 8-bit      | IBM PC/AT to ATA-2   |
| 77     | SET DATE & TIME EXT                   | none       | 16-bit     | ACS-3 to present     |
| 77     | SEEK                                  | none       | 8-bit      | IBM PC/AT to ATA-2   |
| 78     | ACCESSIBLE MAX ADDRESS CONFIGURATION  | none       | 16-bit     | ACS-3 to present     |
| 78     | SEEK                                  | none       | 8-bit      | IBM PC/AT to ATA-2   |
| 79     | SEEK                                  | none       | 8-bit      | IBM PC/AT to ATA-2   |
| 7A     | SEEK                                  | none       | 8-bit      | IBM PC/AT to ATA-2   |
| 7B     | SEEK                                  | none       | 8-bit      | IBM PC/AT to ATA-2   |
| 7C     | REMOVE ELEMENT AND TRUNCATE           | none       | 16-bit     | ACS-4 to present     |
| 7C     | SEEK                                  | none       | 8-bit      | IBM PC/AT to ATA-2   |
| 7D     | RESTORE ELEMENTS AND REBUILD          | none       | 16-bit     | ACS-5 to present     |
| 7D     | SEEK                                  | none       | 8-bit      | IBM PC/AT to ATA-2   |
| 7E     | REMOVE ELEMENT AND MODIFY ZONES       | none       | 16-bit     | ACS-5 to present     |
| 7E     | SEEK                                  | none       | 8-bit      | IBM PC/AT to ATA-2   |
| 7F     | SEEK                                  | none       | 8-bit      | IBM PC/AT to ATA-2   |
| 80     | Vendor Specific                       |            |            |                      |
| 81     | Vendor Specific                       |            |            |                      |
| 82     | Vendor Specific                       |            |            |                      |
| 83     | Vendor Specific                       |            |            |                      |
| 84     | Vendor Specific                       |            |            |                      |
| 85     | Vendor Specific                       |            |            |                      |
| 86     | Vendor Specific                       |            |            |                      |
| 87     | CFA TRANSLATE SECTOR                  | PIO        | 8-bit      | ATA-4 to present     |
| 88     | Vendor Specific                       |            |            |                      |
| 89     | Vendor Specific                       |            |            |                      |
| 8A     | Vendor Specific                       |            |            |                      |
| 8B     | Vendor Specific                       |            |            |                      |
| 8C     | Vendor Specific                       |            |            |                      |
| 8D     | Vendor Specific                       |            |            |                      |
| 8E     | Vendor Specific                       |            |            |                      |
| 8F     | Vendor Specific                       |            |            |                      |
| 90     | EXECUTE DEVICE DIAGNOSTIC             | none       | 8-bit      | IBM PC/AT to present |
| 91     | INITIALIZE DEVICE PARAMETERS          | none       | 8-bit      | IBM PC/AT to ATA-5   |
| 92     | DOWNLOAD MICROCODE                    | PIO        | 8-bit      | ATA-2 to present     |
| 93     | DOWNLOAD MICROCODE DMA                | DMA        | 8-bit      | ACS-2 to present     |
| 94     | STANDBY IMMEDIATE                     | none       | 8-bit      | ATA-1 to ATA-3       |
| 95     | IDLE IMMEDIATE                        | none       | 8-bit      | ATA-1 to ATA-3       |
| 96     | MUTATE EXT                            | none       | 16-bit     | ACS-5 to present     |
| 96     | STANDBY                               | none       | 8-bit      | ATA-1 to ATA-3       |
| 97     | IDLE                                  | none       | 8-bit      | ATA-1 to ATA-3       |
| 98     | CHECK POWER MODE                      | none       | 8-bit      | ATA-1 to ATA-3       |
| 99     | SLEEP                                 | none       | 8-bit      | ATA-1 to ATA-3       |
| 9A     | Vendor Specific                       |            |            |                      |
| 9B     |                                       |            |            |                      |
| 9C     |                                       |            |            |                      |
| 9D     |                                       |            |            |                      |
| 9E     |                                       |            |            |                      |
| 9F     | ZAC Management Out                    | DMA        | 16-bit     | ACS-4 to present     |
| A0     | PACKET                                | packet     | 8-bit      | ATA-3 to ACS-3       |
| A1     | IDENTIFY PACKET DEVICE                | PIO        | 8-bit      | ATA-3 to ACS-3       |
| A2     | SERVICE                               | varies     | 8-bit      | ATA-3 to ATA8-ACS    |
| A3     |                                       |            |            |                      |
| A4     |                                       |            |            |                      |
| A5     |                                       |            |            |                      |
| A6     |                                       |            |            |                      |
| A7     |                                       |            |            |                      |
| A8     |                                       |            |            |                      |
| A9     |                                       |            |            |                      |
| AA     |                                       |            |            |                      |
| AB     |                                       |            |            |                      |
| AC     |                                       |            |            |                      |
| AD     |                                       |            |            |                      |
| AE     |                                       |            |            |                      |
| AF     |                                       |            |            |                      |
| B0     | SMART                                 | PIO        | 8-bit      | ATA-3 to present     |
| B1     | Device Configuration Overlay          | PIO        | 8-bit      | ATA-6 to ACS-2       |
| B2     | SET SECTOR CONFIGURATON EXT           | none       | 16-bit     | ACS-4 to present     |
| B3     |                                       |            |            |                      |
| B4     | Sanitize Device                       | none       | 16-bit     | ACS-2 to present     |
| B5     |                                       |            |            |                      |
| B6     | NV Cache                              | DMA        | 16-bit     | ATA8-ACS to ACS-2    |
| B7     | Reserved for CFA                      |            |            |                      |
| B8     | Reserved for CFA                      |            |            |                      |
| B9     | Reserved for CFA                      |            |            |                      |
| BA     | Reserved for CFA                      |            |            |                      |
| BB     | Reserved for CFA                      |            |            |                      |
| BC     |                                       |            |            |                      |
| BD     |                                       |            |            |                      |
| BE     |                                       |            |            |                      |
| BF     |                                       |            |            |                      |
| C0     | CFA ERASE SECTORS                     | none       | 8-bit      | ATA-4 to ACS-2       |
| C1     | Vendor Specific                       |            |            |                      |
| C2     | Vendor Specific                       |            |            |                      |
| C3     | Vendor Specific                       |            |            |                      |
| C4     | READ MULTIPLE                         | PIO        | 8-bit      | ATA-1 to ACS-3       |
| C5     | WRITE MULTIPLE                        | PIO        | 8-bit      | ATA-1 to ACS-3       |
| C6     | SET MULTIPLE MODE                     | none       | 8-bit      | ATA-1 to ACS-3       |
| C7     | READ DMA QUEUED                       | queued DMA | 8-bit      | ATA-4 to ATA8-ACS    |
| C8     | READ DMA                              | DMA        | 8-bit      | ATA-1 to present     |
| C9     | READ DMA (without retry)              | DMA        | 8-bit      | ATA-1 to ATA-4       |
| CA     | WRITE DMA                             | DMA        | 8-bit      | ATA-1 to present     |
| CB     | WRITE DMA (without retry)             | DMA        | 8-bit      | ATA-1 to ATA-4       |
| CC     | WRITE DMA QUEUED                      | queued DMA | 8-bit      | ATA-4 to ATA8-ACS    |
| CD     | CFA WRITE MULTIPLE WITHOUT ERASE      | PIO        | 8-bit      | ATA-4 to present     |
| CE     | WRITE MULTIPLE FUA EXT                | PIO        | 16-bit     | ATA-7 to ACS-3       |
| CF     |                                       |            |            |                      |
| D0     |                                       |            |            |                      |
| D1     | CHECK MEDIA CARD TYPE                 | none       | 8-bit      | ATA-6 to ACS-2       |
| D2     |                                       |            |            |                      |
| D3     |                                       |            |            |                      |
| D4     |                                       |            |            |                      |
| D5     |                                       |            |            |                      |
| D6     |                                       |            |            |                      |
| D7     |                                       |            |            |                      |
| D8     |                                       |            |            |                      |
| D9     |                                       |            |            |                      |
| DA     | GET MEDIA STATUS                      | none       | 8-bit      | ATA-3 to ATA-7       |
| DB     | ACKNOWLEDGE MEDIA CHANGE              | none       | 8-bit      | ATA-1 to ATA-2       |
| DC     | BOOT - POST-BOOT                      | none       | 8-bit      | ATA-1 to ATA-2       |
| DD     | BOOT - PRE-BOOT                       | none       | 8-bit      | ATA-1 to ATA-2       |
| DE     | MEDIA LOCK                            | none       | 8-bit      | ATA-1 to ATA-7       |
| DF     | MEDIA UNLOCK                          | none       | 8-bit      | ATA-1 to ATA-7       |
| E0     | STANDBY IMMEDIATE                     | none       | 8-bit      | ATA-1 to present     |
| E1     | IDLE IMMEDIATE                        | none       | 8-bit      | ATA-1 to present     |
| E2     | STANDBY                               | none       | 8-bit      | ATA-1 to present     |
| E3     | IDLE                                  | none       | 8-bit      | ATA-1 to present     |
| E4     | READ BUFFER                           | PIO        | 8-bit      | ATA-1 to present     |
| E5     | CHECK POWER MODE                      | none       | 8-bit      | ATA-1 to present     |
| E6     | SLEEP                                 | none       | 8-bit      | ATA-1 to present     |
| E7     | FLUSH CACHE                           | none       | 8-bit      | ATA-4 to present     |
| E8     | WRITE BUFFER                          | PIO        | 8-bit      | ATA-1 to present     |
| E9     | READ BUFFER DMA                       | DMA        | 8-bit      | ACS-2 to present     |
| E9     | WRITE SAME                            |            | 8-bit      | ATA-1 to ATA-2       |
| EA     | FLUSH CACHE EXT                       | none       | 8-bit      | ATA-6 to present     |
| EB     | WRITE BUFFER DMA                      | DMA        | 8-bit      | ACS-2 to present     |
| EC     | IDENTIFY DEVICE                       | PIO        | 8-bit      | ATA-1 to present     |
| ED     | MEDIA EJECT                           | none       | 8-bit      | ATA-1 to ATA-7       |
| EE     | IDENTIFY DEVICE DMA                   | DMA        | 8-bit      | ATA-3                |
| EF     | SET FEATURES                          | none       | 8-bit      | ATA-1 to present     |
| F0     | Vendor Specific                       |            |            |                      |
| F1     | SECURITY SET PASSWORD                 | PIO        | 8-bit      | ATA-3 to present     |
| F2     | SECURITY UNLOCK                       | PIO        | 8-bit      | ATA-3 to present     |
| F3     | SECURITY ERASE PREPARE                | none       | 8-bit      | ATA-3 to present     |
| F4     | SECURITY ERASE UNIT                   | PIO        | 8-bit      | ATA-3 to present     |
| F5     | SECURITY FREEZE LOCK                  | none       | 8-bit      | ATA-3 to present     |
| F6     | SECURITY DISABLE PASSWORD             | PIO        | 8-bit      | ATA-3 to present     |
| F7     | Vendor Specific                       |            |            |                      |
| F8     | READ NATIVE MAX ADDRESS               | none       | 8-bit      | ATA-4 to ACS-2       |
| F9     | SET MAX ADDRESS                       | none       | 8-bit      | ATA-4 to ACS-2       |
| FA     | Vendor Specific                       |            |            |                      |
| FB     | Vendor Specific                       |            |            |                      |
| FC     | Vendor Specific                       |            |            |                      |
| FD     | Vendor Specific                       |            |            |                      |
| FE     | Vendor Specific                       |            |            |                      |
| FF     | Vendor Specific                       |            |            |                      |
