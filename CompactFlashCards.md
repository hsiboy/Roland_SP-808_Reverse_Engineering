
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

CF Card Pin Assignment

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

---



| PIO Mode | Cycle Time (nanoseconds) | Maximum Transfer Rate (MB/s) | Defining Standard |
|:--------:|:------------------------:|:----------------------------:|:-----------------:|
|  Mode 0  |  600                     |  3.3                         |  ATA              |
|  Mode 1  |  383                     |  5.2                         |  ATA              |
|  Mode 2  |  240                     |  8.3                         |  ATA              |
|  Mode 3  |  180                     |  11.1                        |  ATA-2            |
|  Mode 4  |  120                     |  16.7                        |  ATA-2            |


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
