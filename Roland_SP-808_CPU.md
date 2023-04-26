The Roland SP-808 groovebox uses a Hitachi HD6432653 CPU or H8S/2600

Its a General-register machine, with Sixteen 16-bit general registers (also usable as sixteen 8-bit registers
or eight 32-bit registers).

* A Maximum clock rate: 20 MHz
* 8/16/32-bit register-register add/subtract: 50 ns
* 16 × 16-bit register-register multiply: 200 ns
* 16 × 16 + 42-bit multiply and accumulate: 200 ns
* 32 ÷ 16-bit register-register divide: 1000 ns
* Its instruction set is suitable for high-speed operation

It has sixty-nine basic instructions
* 8/16/32-bit move/arithmetic and logic instructions
* Unsigned/signed multiply and divide instructions
* Multiply-and accumulate instruction
* bit-manipulation instructions
• Two CPU operating modes
- Normal mode: 64-kbyte address space
- Advanced mode: 16-Mbyte address space

It should be noted that people have stated that the is backaward compatible with the Hitachi H8/300H CPU family

In comparison to the H8/300 CPU, the H8S/2600 CPU has the following enhancements:
* More general registers and control registers
* Eight 16-bit expanded registers, and one 8-bit and two 32-bit control registers, have been
added.
* Expanded address space
* Normal mode supports the same 64-kbyte address space as the H8/300 CPU.
* Advanced mode supports a maximum 16-Mbyte address space.
* Enhanced addressing
* The addressing modes have been enhanced to make effective use of the 16-Mbyte address
space.
* Enhanced instructions
* Addressing modes of bit-manipulation instructions have been enhanced.
* Signed multiply and divide instructions have been added.
* A multiply-and-accumulate instruction has been added.
* Two-bit shift instructions have been added.
* Instructions for saving and restoring multiple registers have been added.
* A test and set instruction has been added

These newly added instructions, mean that tools like binwalk and objdump fail, but see not below.

It's worth noting that instructions on the H8S/2600 execute twice as fast as they did on the H8/300H.

Manuals are readily available for the micro. Here's the software manual {TODO link to repo} . Here's the hardware manual. The Opensource for Renesas project has a gcc and binutils build, which appears to be originally from KPIT. 
Using objdump from that package decompiles correctly and understand all of the commands for H8, H8300, H8S/2000, and H8S/2600, each of which has a few added instructions.

** Note: The H8 line of CPUs is bigendian **

I can't find anything in the manuals that explains what address code execution starts. The manuals do explain that the chip has an 'advanced mode', and in that mode, address 0x00 contains an exception table with addresses to jump to. The first 4 bytes should have the address, but we appear to have a string in the Roland Firmware 🤔
The manu aexlains that the exception vector table starts at 0x00 and first exception is the restart exception. he CPU handles boot as an exception (power glitch?), so the first four bytes in the firmware, should be a 32 bit address that points to the first instruction, not an ascii string.

Therefore, Roland, have 'packaged' the firmware with a header and a footer (inlcuding padding bytes) and i need to find the SP-808 firmware within this envelope.

example of H8 code:

```
   0:	00 00       	nop	
   2:	04 00       	orc	#0x0,ccr
   4:	ff ff       	mov.b	#0xff,r7l
   6:	ff ff       	mov.b	#0xff,r7l
   8:	ff ff       	mov.b	#0xff,r7l
   a:	ff ff       	mov.b	#0xff,r7l
   c:	ff ff       	mov.b	#0xff,r7l
   e:	ff ff       	mov.b	#0xff,r7l
```
   First instruction, is the restart exception vector and it points to `0x0400`
```
 400:	7a 07 00 ff 	mov.l	#0xfffc00,er7   ;Put 0x 00fffc00 into ER7
 404:	fc 00 
 406:	04 80       	orc	#0x80,ccr       ;OR 0x 80 with the control register
 408:	f8 1b       	mov.b	#0x1b,r0l       
 40a:	6a 88 fe bf 	mov.b	r0l,@0xfebf:16  ;Put 0x1B into address 0000febf
```
 Off to '0x0800'
```
 800:	01 10 6d f2 	stm.l	er2-er3,@-sp
 804:	1b 97       	subs	#4,r7
 806:	01 00 69 f0 	mov.l	er0,@r7
 80a:	0f 93       	mov.l	er1,er3
 80c:	0f 82       	mov.l	er0,er2
 80e:	46 0e       	bne	.+14 (0x81e)
 810:	1a 80       	sub.l	er0,er0
```
 
