# Roland SP-808

The microcontroller is a 16-bit Hitachi/Renesas HD6432653 [128-pin, 19.66 MHz], (H8S/2653) which has 64K mask ROM and 4K SRAM. 
FWIW, it has a UART port which is accessible via connector CN7. TODO - Sniff TTY, as there are some interesting strings in the ROM, that are not shown on display.

The flash memory has a capacity of 1MB and is organised as 512K x 16. The SP-808 reads data from the ZIP disk in 512 blocks, coincidence? 

https://4donline.ihs.com/images/VipMasterIC/IC/RNSA/RNSAS06856/RNSAS06856-1.pdf

The SP-808 firmware, was supplied as 8 midi files. 

The following DOS command converts all 8 MIDI files and writes the result to a single BIN file:

```for %i in (SP8EX#?.mid) do Rmid2bin.exe infil=%i outfil=SP8EXall.bin```

## Flash Memory Map (H8S/2653 Mode 6)

| Address Range | Content | Notes |
|---|---|---|
| `0x000000–0x00FFFF` | On-chip mask ROM | 64 KB, inaccessible — contains boot/init code |
| `0x010000–0x0FFFFF` | External address space | Unused or reserved |
| `0x100000–0x17C883` | External flash — active firmware | H8S vectors + code + strings |
| `0x17C884–0x1BFFDF` | External flash — zero padding | Empty (flash erased state) |
| `0x1BFFE0–0x1C0003` | External flash — Roland trailer | Repeated Roland container header + 4 null bytes |
| `0x400000–0x4FFFFF` | Runtime RAM (external) | Device registers, shadow regs |
| `0x00FFEC00–0x00FFFBFF` | On-chip RAM | 4 KB, when RAME=1 in SYSCR |

### Firmware Load Address

The external flash is mapped at `0x100000`. The binary file maps directly to this address:
- Binary offset 0 → runtime `0x100000`
- Binary offset `0x20` → runtime `0x100020` (first exception vector)
- Binary offset `0x7C883` → runtime `0x17C883` (end of active content)

The reset vector at binary offset `0x20` reads `01 10 6D F2`. Lower 24 bits = `0x106DF2`, which is binary offset `0x6DF2` at runtime `0x106DF2`. This is the entry point for the firmware initialisation code.

**IDA Pro:** Load `SP8EXall.bin` with base address `0x100000` (not `0x8000`).

### Roland Container Format

The binary is wrapped in a Roland header at both the start (offset `0x00`) and end (offset `0xBFFE0`):
```
5A 12 CC 54  54 53 32 35  45 53 59 53  ...  52 6f 6c 61  6e 64 45 43
|-- sig --|  |------- "TS25ESYS" ------| ... |------- "RolandEC" -------|
```

The first 0x20 bytes and last 0x24 bytes of the binary are this container and are not H8S code.

