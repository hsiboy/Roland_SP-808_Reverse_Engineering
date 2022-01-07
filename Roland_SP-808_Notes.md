# Roland SP-808

The microcontroller is a 16-bit Hitachi/Renesas HD6432653 [128-pin, 19.66 MHz], (H8S/2653) which has 64K mask ROM and 4K SRAM. 
FWIW, it has a UART port which is accessible via connector CN7.

The flash memory has a capacity of 1MB and is organised as 512K x 16. That's a lot of code.

https://4donline.ihs.com/images/VipMasterIC/IC/RNSA/RNSAS06856/RNSAS06856-1.pdf

The following DOS command converts all 8 MIDI files and writes the result to a single BIN file:

```for %i in (SP8EX#?.mid) do Rmid2bin.exe infil=%i outfil=SP8EXall.bin```

SalvationData USB (host) to IDE https://www.drivestar.biz/index.php?main_page=product_info&products_id=4915


