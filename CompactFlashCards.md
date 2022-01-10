
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