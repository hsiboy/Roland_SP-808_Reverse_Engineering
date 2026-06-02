# Interesting Firmware Strings

Strings found in the SP-808EX, SP-808, and Edirol A6 firmware binaries.
Offsets are file offsets into the assembled binary (add `0x100000` for runtime addresses).
A6 strings are offset from SP-808 by `+0x5FDE` for device/vendor strings (confirmed);
offset for other string classes is unverified.

Sources: `SP-808EX_strings.md`, `firmware/SP808_Vs_A6_firmware.md`, `A6_firmware_strings.txt`,
`SP-808_SZHC_CommandTableAnalysis.md`.

| String | SP-808EX (offset) | SP-808 (offset) | A6 (offset) | Notes |
|:-------|:-----------------:|:---------------:|:-----------:|:------|
| `TS25ESYSTEMPRMxxBAK` | ✓ `0x71aa0` | ✓ (same) | — | System parameter backup filename |
| `SELF` | ✓ `0x71abb` | ✓ `0x71abb` | ✓ `0x77a99` | Device type: internal |
| `ZIP ` | ✓ `0x71ac0` | ✓ `0x71ac0` | ✓ `0x77a9e` | Device type: ZIP drive |
| `HD  ` | ✓ `0x71ac5` | ✓ `0x71ac5` | ✓ `0x77aa3` | Device type: hard drive |
| `CD  ` | ✓ `0x71aca` | ✓ `0x71aca` | ✓ `0x77aa8` | Device type: CD-ROM |
| `-SZHC` | ✓ | ✓ | ✓ `0x77aad` | SZHC table terminator/signature |
| `IOMEGA  ` | ✓ `0x71af0` | ✓ `0x71af0` | ✓ `0x77ace` | Vendor validation string (8 chars) |
| `iomega  ` | ✓ `0x71af9` | ✓ `0x71af9` | ✓ `0x77ad7` | Vendor validation (lowercase fallback) |
| `ZIP` | ✓ | ✓ | ✓ | Product validation string |
| `Roland  ` | ✓ `0x71b90` | ✓ `0x71b90` | — | Roland vendor string; A6 uses different branding |
| `TS25E` | ✓ | ✓ | — | System identifier |
| `FAT12` | ✓ | ✓ | — | Filesystem type string |
| `FAT16` | ✓ | ✓ | — | Filesystem type string |
| `SP-808TS25E` | ✓ | ✓ | — | Combined system string |
| `ECV02(A-6) ARCHIVE FILE` | — | — | ✓ | A6-specific archive identifier |
| `SYSTEM__VS2` | ✓ | ✓ | — | VS2 filesystem: system file |
| `SONGLISTVS2` | ✓ | ✓ | — | VS2 filesystem: song list |
| `SP808   PRG` | ✓ | ✓ | — | VS2 filesystem: program file |
| `SAMPLE__VS2` | ✓ | ✓ | — | VS2 filesystem: sample data |
| `PADBANK_VS2` | ✓ | ✓ | — | VS2 filesystem: pad bank |
| `WAVELISTVS2` | ✓ | ✓ | — | VS2 filesystem: wave list |
| `TAKE0000VS2` | ✓ | ✓ | — | VS2 filesystem: take/recording |
| `EFFECT__VS2` | ✓ | ✓ | — | VS2 filesystem: effects |
| `EFFECT1_VS2` | ✓ | ✓ | — | VS2 filesystem: effects bank 1 |
| `Not SP-808 Disk.` | ✓ `0x74bdf` | ✓ `0x74bdf` | — | Disk validation error |
| `Wrong Media Size.` | ✓ `0x74cd6` | ✓ `0x74cd6` | — | Disk validation error |
| `SP808 100MB Disk.` | ✓ `0x75233` | ✓ `0x75233` | — | Disk type identifier |
| `SP808EX 250MB Disk.` | ✓ `0x75245` | ✓ `0x75245` | — | Disk type identifier |

**Legend:** ✓ = confirmed present, — = absent or unknown, `(same)` = same offset as SP-808EX.