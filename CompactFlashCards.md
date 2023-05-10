
Compact Flash storage devices can operate in three modes:
* PC Card Memory Mode
* PC Card I/O Mode
* True IDE Mode
Compact Flash devices must support operation in all three modes, but they only operate in a single mode at any given time.
The CF card senses (using pin #9) if it's connected to IDE or PCMCIA, and switches modes accordingly.
if connected to IDE, it uses "True IDE" mode, and becomes a hardware-level PATA IDE device.
Connected to PCMCIA, things get a little more complex, as the CF card takes on the role of both IDE controller and IDE device, using PC Card I/O mode. As such, CF cards needs to support several different PCMCIA access modes, different register locations, etc.


IDE drivers use the ATA command `IDENTIFY DEVICE` to get all kinds of information from the device.

The first word of the device reply (word 0, 'General configuration') is `848Ah` for removable type CF cards, and `044Ah` or `0040h` for fixed type CF cards.

ATA-4 standard (1998) says that bit 15 in word 0 shall be 0 for ATA devices (page 95), but can be 1 (848Ah) for CF compatible cards (page 52).

It also says that ATAPI devices shall not respond to `IDENTIFY DEVICE`, but reply to `IDENTIFY PACKET DEVICE` instead (page 41)
* ATA-3 standard ( 1997 ) says it must be 0 for ATA devices and 1 for ATAPI devices (page 49)
* ATA-2 standard ( 1996 ) says it is 'reserved for non-magnetic devices' (page 37)
* ATA-1 standard ( 1994 ) says it is 'reserved for non-magnetic devices' (page 44)
* CF specification v3.0 ( 2004 ) says word 0 standard is 848Ah, but can alternatively be 044Ah or 0040h to "turn off removable media". ( page 130 )

bit 7 set indicates that a device is removable media. This did not change since the original ATA-1 specification.
(Additionally bit 6 could be set to specifically mark a disk as fixed, but this was removed in ATA-6 standard (2002) so I guess modern drivers use bit 7.)

A CF card's reply can not be changed manually except on a few old cards where the manufacturer (Sandisk, Lexar) provided tools to ‘flip the removable bit’.
However, I've read that some modern CF cards sense if they are connected to a proper IDE bus, and change their type to fixed.

Many CF cards are set to report as removable media, but not all, and it's hard to know in advance. ('Industrial' level cards are usually fixed type)
The information is stored on CF card's CIS (Central information structure) and communicated by the ATA controller inside the card when replying to the ATA IDENTIFY DEVICE command.

---

## CF Card Pin Assignment

| Pin Number | Signal Name | Pin Type | Pin Number | Signal Name | Pin Type |
|:--:|:--:|:--:|:--:|:--:|:--:|
|1 | GND | Ground | 26| -CD1 | O |
|2 | D03 | I/O | 27 | D11| I/O |
|3 |D04 | I/O | 28 | D12 | I/O |
|4 |D05 | I/O | 29 | D13 | I/O |
|5 |D06 | I/O | 30 | D14 | I/O |
|6 |D07 | I/O | 31 | D15 | I/O |
|7 |-CE1 -CS0 |I |32|-CE2 -CS1|I|
|8 |A10| I |33 |-VS1 |O|
|9 |-OE -ATASEL| I |34| -IORD| I|
|10| A09| I| 35| -IOWR| I|
|11| A08| I| 36| -WE| I|
|12| A07| I| 37|RDY/-BSY -IREQ|INTRQ|O|
|13| VCC| Power| 38 |VCC| Power|
|14| A06| I |39| -CSEL| I|
|15| A05| I |40| -VS2| O|
|16| A04| I |41| RESET-RESET| I|
|17| A03| I |42| -WAIT IORDY| O|
|18| A02| I |43|-INPACK DMARQ|O|
|19| A01| I |44|-REG -DMACK|I|
|20| A00| I |45|BVD2 -SPKR -DASP|I/O|
|21| D00| I/O| 46|BVD1 -STSCHG -PDIAG|I/O|
|22| D01| I/O| 47| D08| I/O|
|23| D02| I/O| 48| D09| I/O|
|24| WP -IOIS16| O| 49 |D10| I/O|
|25| -CD2| O| 50| GND| Ground| 



## CF Card Signal Descriptions

|Signal Name| Mode| Type| Pin Number| Description|
|:--:|:--:|:--:|:--:|:--:|
|BVD2|PC Card Memory Mode|I/O| 45| This output line is always driven to a high state in Memory Mode since a battery is not required for this product.|
|-SPKR|PC Card I/O Mode| " | " | This output line is always driven to a high state in I/O Mode since this product produces no audio.|
|-DASP|True IDE Mode| " | " | In the True IDE Mode, this input/output is the Disk Active/Slave Present signal in the Master/Slave handshake protocol.|
|-CD1, -CD2|PC Card Memory Mode|I/O| 26, 25| These Card Detect pins are connected to ground on the card. They are used by the host to determine that the card is fully inserted into the socket.|
|-CD1, -CD2|PC Card I/O Mode| " | " |This signal is the same as Memory Mode.|
|-CD1, -CD2|True IDE Mode| " | " |These signals are not used in IDE Mode.|
|D15-D00|PC Card Memory Mode|I/O|31-27, 49-47, 6-2, 23-21|These lines carry the data, commands, and host and the controller. D00 is the LSB of the LSB of the Odd Byte of the Word.|
|D15-D00|PC Card I/O Mode| " | " |This signal is the same as the PC Card Memory Mode signal.|
| D15-D00|True IDE Mode| " | " |In True IDE Mode, all Task File operations occur in byte mode on the low order bus D00-D07 while all data transfers are 16 bit using D00-D15.|
|-IOWR|PC Card Memory Mode|I| 35| This signal is not used in this mode.|
|-IOWR|PC Card I/O Mode|" | " |The I/O Write strobe pulse is used to clock I/O data onto the data bus and into the controller registers. The clocking occurs on the negative to positive edge of the signal (trailing edge).|
|-IOWR|True IDE Mode| " | " |In True IDE Mode, this signal has the same function as in PC Card I/O Mode.|
|-IORD|PC Card Memory Mode| I |34 |This signal is not used in this mode.|
|-IORD|PC Card I/O Mode| " | " |This is an I/O Read strobe generated by the host. This signal gates I/O data onto the bus from the CF Card.
|-IORD|True IDE Mode| " | " |In True IDE Mode, this signal has the same function as in PC Card I/O Mode.|
|-WE|PC Card Memory Mode|I |36| This is a signal driven by the host and used for strobing memory write data into the registers. It is also used for writing the configuration registers.|
|-WE|PC Card I/O Mode| " | " |In PC Card I/O Mode, this signal is used for writing the configuration registers.|
|-WE|True IDE Mode| " | " |In True IDE Mode, this input signal is not used and should be connected to VCC.|
|-OE|PC Card Memory Mode|I| 9| This is an Output Enable strobe generated by the host interface. It is used to read data from the CF Card in PC Card Memory Mode and to read the CIS and configuration registers.|
|-OE|PC Card I/O Mode| " | " |In PC Card I/O Mode, this signal is used to read the CIS and configuration registers.|
|-ATASEL|True IDE Mode| " | " |To enable True IDE Mode, this input should be grounded by the host.|
|RDY/-BSY|PC Card Memory Mode|O| 37| In Memory Mode, this signal is set high when the CF Card is ready to accept a new data transfer operation and held low when the CF Card is busy. The host must provide a pull-up resistor. At power up and at reset, the RDY/-BSY signal is held low (busy) until the CF Card completes its power up or reset function. No access of any type should be made to the CF Card during this time. The RDY/-BSY signal is held high (disabled from being busy) when the CF Card is powered up with RESET continuously disconnected or asserted high.|
|-IREQ|PC Card I/O Mode| " | " |After the CF Card has been configured for I/O operation, this signal is used as the active low interrupt request. This line is strobed low to generate a pulse mode interrupt or held low for a level mode interrupt.|
|INTRQ|True IDE Mode| " | " |In True IDE Mode, this signal is the active high interrupt request to the host.|
|A10-A0|PC Card Memory Mode|I | 8, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20| These address lines along with the -REG signal are used to select the following: the I/O port address registers within the CF Card, the memory mapped port address registers within the CF Card, a byte in the CIS and the Configuration Control and Status Registers.|
|A10-A0|PC Card I/O Mode| " | " |This signal is the same as the PC Card Memory Mode signal.|
|A2-A0|True IDE Mode| " |18, 19, 20| In True IDE Mode only, A2:A0 are used to select the one of eight registers in the Task File. The remaining address lines should be grounded.|
|-CE1, -CE2|PC Card Memory Mode|I |7, 32 |These input signals are used both to select the CF Card and to indicate to the CF Card whether a byte or a word operation is being performed. -CE2 always accesses the odd byte of the word. -CE1 accesses the even byte or the odd byte of the word depending on A0 and -CE2. A multiplexing scheme based on A0, -CE1, -CE2 allows 8-bit hosts to access alldata on D0-D7.|
|-CE1, -CE2|PC Card I/O Mode| " | " |This signal is the same as the PC Card Memory Mode signal.|
|-CS0, -CS1|True IDE Mode| " | " |In the True IDE Mode, -CS0 is the chip select for the task file registers while -CS1 is used to select the Alternate Status Register and the CF Card Control Register.|
|-CSEL|PC Card Memory Mode|I| 39| This signal is not used in this mode.|
|-CSEL|PC Card I/O Mode|"|"|This signal is not used for this mode.|
|-CSEL|True IDE Mode|"|"|This internally pulled up signal is used to configure the card as a Master or Slave. When the pin is grounded, the card is configured as a Master. When the pin is open, the card is configured as a Slave.|
|-REG|PC Card Memory Mode|I| 44 |Attribute Memory Select - This signal distinguishes between accesses to Common Memory (high) and Register Attribute Memory (low).|
|-REG|PC Card I/O Mode|"|"|The signal must also be active (low) during I/O Cycles when the I/O address is on the bus.|
|-DMACK|True IDE Mode|"|"|In True IDE Mode this input signal is used by host in response to DMARQ to initiate DMA transfers.|
|WP|PC Card Memory Mode|O| 24| Write Protect - The CF Card does not have a write protect switch; therefore, this signal is held low after the completion of the reset initialization sequence.|
|-IOIS16|PC Card I/O Mode|"|"|A low signal indicates that a 16 bit or odd byte only operation can be performed at the addressed port.|
|-IOCS16|True IDE Mode|"|"|Not defined in IDE Mode.|
|-INPACK|PC Card Memory Mode|O |43 |This signal is not used in this mode.
|-INPACK|PC Card I/O Mode|"|"|Input Acknowledge - The Input Acknowledge signal is asserted by the CF Card when it is selected and responding to an I/O read cycle at the address that is on the bus. The host uses this signal to control the enable of any input data buffers between the CF Card and the host’s CPU.
|DMARQ|True IDE Mode|"|"|In True IDE Mode this signal is asserted by the CF Card when it is ready to transfer data to/from the host. Data direction is controlled by -IORD and -IOWR. This signal is used in a handshake manner with -DMACK.
|BVD1|PC Card Memory Mode|I/O| 46| This signal is asserted high as since a battery is not used with this product.|
|-STSCHG|PC Card I/O Mode| " | " |Status Changed - This signal is asserted low to alert the host to changes in the RDY/-BSY and Write Protect states. Its use is controlled by the Configuration and Status Register.|
|-PDIAG|True IDE Mode|"|"|In True IDE Mode, this input/output signal is the Pass Diagnostic signal in the Master/Slave handshake protocol.|
|-WAIT|PC Card Memory Mode|O| 42| This signal is not used by the CF Card, and is pulled up toVCC through a 4.7K ohm resistor.|
|-WAIT|PC Card I/O Mode|" |"|This signal is not used by the CF Card, and is pulled up to VCC through a 4.7K ohm resistor.|
|IORDY|True IDE Mode| "|"|This signal is not used by the CF Card, and is pulled up to VCC through a 4.7K ohm resistor.|
|GND|PC Card Memory Mode|GND| 1, 50| Ground|
|GND|PC Card I/O Mode|"|"|"|
|GND|True IDE Mode|"|"|"|
|VCC|PC Card Memory Mode|VCC| 13, 38| +5 V or 3.3V power|
|VCC|PC Card I/O Mode|"|"|+5 V or 3.3V power|
|VCC|True IDE Mode|"|"|+5 V or 3.3V power|
|RESET|PC Card Memory Mode|I| 41| When RESET is high, this signal resets the CF Card. The CF Card is reset only at power up if this signal is left high or open from power-up. The CF Card can also be reset when the soft reset bit in the Configuration Option Register is set.|
|RESET|PC Card I/O Mode|"|"|This signal is the same as the PC Card Memory Mode signal.|
|-RESET|True IDE Mode|"|"|In the True IDE Mode this input pin is the active low hardware reset from the host.|
|-VS1 -VS2|PC Card Memory Mode|O 33, 40| -VS1 is grounded so that the card CIS can be read at 3.3 volts. -VS2 is reserved for a secondary voltage and is not connected..
|-VS1 -VS2|PC Card I/O Mode| "|"|This signal is the same for all models.|
|-VS1 -VS2|True IDE Mode|"|"|This signal is not used in IDE Mode."


---

## Mechanical dimensions CompactFlash Type II
|Parameter| Value|
|:--:|:--:|
|Length |36.40 ± 0.15 mm| 
|Width |42.80 ± 0.10 mm |
|Height (including label area)| 5.00 mm |

---


| PIO Mode | Cycle Time (nanoseconds) | Maximum Transfer Rate (MB/s) | Defining Standard |
|:--------:|:------------------------:|:----------------------------:|:-----------------:|
|  Mode 0  |  600                     |  3.3                         |  ATA              |
|  Mode 1  |  383                     |  5.2                         |  ATA              |
|  Mode 2  |  240                     |  8.3                         |  ATA              |
|  Mode 3  |  180                     |  11.1                        |  ATA-2            |
|  Mode 4  |  120                     |  16.7                        |  ATA-2            |

---


|Word.Bit|      Description|
|:------:|:---------------:|
|0.15    |  0 = reserved for non magnetic drives |
|0.14    |  1 = format speed tolerance gap required | 
|0.13    |  1 = track offset option available |
|0.12    |  1 = data strobe offset option available |
|0.11    |  1 = rotational speed tolerance is > 0.5% |
|0.10    |  1 = disc transfer rate > 10 Mbit/sec |
|0.9     |  1 = disc transfer rate <= 10 Mbit/sec but > 5 Mbit/sec |
|0.8     |  1 = disc transfer rate <= 5 Mbit/sec |
|0.7     |  1 = removable cartridge drive |
|0.6     |  1 = fixed drive |
|0.5     |  1 = spindle motor control option implemented |
|0.4     |  1 = head switch time > 15 usec |
|0.3     |  1 = not MFM encoded |
|0.2     |  1 = soft sectored |
|0.1     |  1 = hard sectored |
|0.0     |  0 = ATA reserved (should be zero) |

The Iomega Zip drive reports a value of `0x80A0` in word 0.

`80A0 = 1000 0000 1010 0000`

If we use the above bit definitions, then the following apply for the Zip drive:

* magnetic drive
* removable cartridge drive
* spindle motor control option implemented



|                   CF Card                 | identify[0] | identify[7] | identify[8] | identify[82] | identify[83] | pwrmgt fails | soft rst fails |
|:-----------------------------------------:|:-----------:|:-----------:|:-----------:|:------------:|:------------:|:------------:|:--------------:|
| A-Data 2GB x266                           | 044A        | 003D        | 5EA0        | 7008         | 400C         | ?            | ?              |
| A-Data 8GB x266                           | 044A        | 005F        | 7E70        | 7008         | 400C         | Yes          | Yes            |
| A-Data 16GB 'speedy'                      | 044A        | 01E3        | FE0D        | 0000         | 0000         | ?            | ?              |
| A-Data 32GB 'speedy'                      | 044A        | 03C8        | 0000        | 0001         | 0000         | ?            | ?              |
| Apacer 200x 8GB CF Card                   | 848A        | 00F0        | 7EC0        | 0001         | 0000         | ?            | ?              |
| Kingston Elite Pro 133X 16GB (CF/16GB-S2) | ?           | ?           | ?           | ?            | ?            | unsupported  | unsupported    |
| Lexar 128MB 12x                           | 848A        | 0003        | D800        | 0000         | 0000         | ?            | ?              |
| Lexar 512MB 40x                           | 848A        | 000F        | 49E0        | 0000         | 0000         | ?            | ?              |
| Memory Corp industrial 512MB              | 044A        | 000F        | B040        | 0000         | 0000         | ?            | ?              |
| Sandisk 1GB                               | 848A        | 001E        | 8BE0        | 0000         | 4004         | ?            | ?              |
| Sandisk Ultra II 2GB                      | 848A        | 003D        | 0FE0        | 0000         | 4004         | ?            | ?              |
| SimpleTech 256MB                          | 848A        | 0007        | CA00        | 0000         | 0000         | ?            | ?              |
| Toshiba 512MB Xtra                        | 848A        | 000F        | 45F0        | 0000         | 0000         | ?            | ?              |
| Toshiba industrial 512MB                  | 044A        | 0007        | A400        | 0000         | 0000         | ?            | ?              |
| Transcend 2GB 133x                        | 044A        | 003B        | BD40        | 7009         | 400C         | ?            | ?              |
| Hitachi HMS360604D5CF00 HDD               | 848A        | 007A        | 1000        | 7069         | 500C         | ?            | No             |
| IBM IC25N020ATCS04 HDD                    | 045A        | 0000        | 0000        | 746B         | 49A8         | ?            | No             |
| IBM IC25N080ATMR04 HDD                    | 045A        | 0000        | 0000        | 746B         | 7FE8         | ?            | No             |
| Seagate ST660211FX HDD                    | 0C5A        | 00B2        | D160        | 7069         | 500D         | ?            | No             |
| Toshiba MK1003GAL HDD                     | 0040        | 0000        | 0000        | 7C6B         | 5908         | ?            | No             |
| Toshiba MK2003GAH HDD                     | 0040        | 0000        | 0000        | 7C6B         | 5908         | ?            | No             |
| Toshiba MK2004GAL HDD                     | 0040        | 0000        | 0000        | 7C6B         | 5908         | ?            | No             |
| Toshiba MK4004GAH HDD                     | 0040        | 0000        | 0000        | 7C6B         | 5908         | ?            | No             |
| Toshiba MK2006GAL HDD                     | 0040        | 0000        | 0000        | 746B         | 7D09         | ?            | No             |
| Toshiba MK8007GAH HDD                     | 0040        | 0000        | 0000        | 746B         | 7F09         | ?            | No             |
| Toshiba MK8011GAH HDD                     | 0040        | 0000        | 0000        | 306B         | 5000         | ?            | No             |
