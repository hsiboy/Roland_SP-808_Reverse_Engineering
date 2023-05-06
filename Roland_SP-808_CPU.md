# The SP-808 CPU

The Roland SP-808 groovebox uses a Hitachi HD6432653 CPU or H8S/2600

The Hitachi H8/2600 is an outdated microcontroller that was widely used in the 1990s and early 2000s. It is known for its simple architecture and low power consumption, but it also poses significant challenges when it comes to reverse engineering firmware.

One of the main difficulties in reverse engineering H8/2600 firmware is the lack of modern tools and resources. Unlike more modern processors, the H8/2600 does not have sophisticated debugging or tracing capabilities, making it much harder to understand how the firmware works.

Another challenge is the lack of documentation and support for the H8/2600. Since this processor is no longer in widespread use, finding technical information or help online can be difficult. This can be particularly frustrating for reverse engineers who are trying to understand the inner workings of a particular piece of hardware or software that uses the H8/2600.

In addition to these technical challenges, there are also legal and ethical considerations when it comes to reverse engineering firmware. In some cases, reverse engineering may be illegal or violate intellectual property rights. This can make it difficult for researchers or engineers who want to understand or improve upon existing technology.

Despite these challenges, reverse engineering H8/2600 firmware is still possible. It requires a combination of technical expertise, persistence, and creativity. Reverse engineers may need to develop their own tools or methods for analyzing firmware, and they may need to rely on manual analysis and experimentation to understand how the firmware works.

In conclusion, while reverse engineering firmware for the H8/2600 processor poses significant challenges, it is still possible with the right combination of skills, resources, and determination. As more and more technology becomes obsolete, the need for reverse engineering will only continue to grow, making this an important area of research and development.

## Specification

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

## Findings

Manufacturer manuals are readily available for the micro. Here's the software manual {TODO link to repo} . Here's the hardware manual. The Opensource for Renesas project has a gcc and binutils build, which appears to be originally from KPIT. 
Using objdump from that package decompiles correctly and understand all of the commands for H8, H8300, H8S/2000, and H8S/2600, each of which has a few added instructions.

** Note: The H8 line of CPUs is bigendian **

I can't find anything in the manuals that explains what address code execution starts. The manuals do explain that the chip has an 'advanced mode', and in that mode, address 0x00 contains an exception table with addresses to jump to. The first 4 bytes should have the address, but we appear to have a string in the Roland Firmware 🤔

The manu aexlains that the exception vector table starts at 0x00 and first exception is the restart exception. he CPU handles boot as an exception (power glitch?), so the first four bytes in the firmware, should be a 32 bit address that points to the first instruction, not an ascii string.

Therefore, Roland, have 'packaged' the firmware with a header and a footer (inlcuding padding bytes) and i need to find the SP-808 firmware within this envelope.

example of H8 code:

```asm

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
```asm
 400:	7a 07 00 ff 	mov.l	#0xfffc00,er7   ;Put 0x 00fffc00 into ER7
 404:	fc 00 
 406:	04 80       	orc	#0x80,ccr       ;OR 0x 80 with the control register
 408:	f8 1b       	mov.b	#0x1b,r0l       
 40a:	6a 88 fe bf 	mov.b	r0l,@0xfebf:16  ;Put 0x1B into address 0000febf
```
 Off to '0x0800'
```asm
 800:	01 10 6d f2 	stm.l	er2-er3,@-sp
 804:	1b 97       	subs	#4,r7
 806:	01 00 69 f0 	mov.l	er0,@r7
 80a:	0f 93       	mov.l	er1,er3
 80c:	0f 82       	mov.l	er0,er2
 80e:	46 0e       	bne	.+14 (0x81e)
 810:	1a 80       	sub.l	er0,er0
```

reset vector:

In advanced mode the top area starting at `H'00000000` is allocated to the exception vector table in units of 32 bits. 
In each 32 bits, the upper 8 bits are ignored and a branch address is stored in the lower 24 bits.
The exception vector table differs depending on the microcontroller.

The H8 supports normal (64KB addressing, 16 bits) and advanced mode (16MB addressing, 24 bits).
However, according to the Renesas technical documentation, certain instructions accept 32-bit pointer values where the upper 8 bits are "reserved".


Instruction | Encoding | Operand | Description
---|---|---|---
ADDI | 80 | R,S,N | Add immediate value to register
ADDIU | 81 | R,S,N | Add immediate value to register, unsigned
ANDI | C0 | R,S,N | AND immediate value with register
ANDII | C1 | R,S,N | AND immediate value with register, immediate unsigned
ANDIU | C2 | R,S,N | AND immediate value with register, unsigned
BEQ | 04 | R,S,J | Branch if equal
BGEZ | 05 | R,S,J | Branch if greater than or equal, zero extended
BGTZ | 06 | R,S,J | Branch if greater than zero
BLEZ | 07 | R,S,J | Branch if less than or equal, zero extended
BLTZ | 08 | R,S,J | Branch if less than zero
BNE | 0A | R,S,J | Branch if not equal
BREAK | 0F | N/A | Generate a software interrupt
CHK | 10 | R,N | Check if register is greater than or equal to zero
CLR | 18 | R | Clear register
CP | 1A | R,S | Compare register with immediate value
CP.S | 1B | R,S | Compare register with single-precision floating-point value
DADD | 90 | R,S,D | Add double-precision floating-point values
DADDI | 91 | R,S,D | Add immediate value to double-precision floating-point register
DADDIU | 92 | R,S,D | Add immediate value to double-precision floating-point register, unsigned
DDIVU | 93 | R,S,D | Divide double-precision floating-point values
DDIV | 94 | R,S,D | Divide double-precision floating-point values
DSLL | 12 | R,S | Shift left logical
DSLL32 | 13 | R,S | Shift left logical, 32 bits
DSLR | 14 | R,S | Shift right logical
DSUB | 98 | R,S,D | Subtract double-precision floating-point values
DSUBU | 99 | R,S,D | Subtract double-precision floating-point values, unsigned
DDIV | 9C | R,S,D | Divide double-precision floating-point values
DIV | 9E | R,S | Divide single-precision floating-point values
J | 02 | J | Jump to address
JAL | 03 | J | Jump and link to address
JALR | 09 | R,S | Jump and link register
LB | 20 | R,S | Load byte from memory
LBU | 21 | R,S | Load byte from memory, unsigned
LDC | 24 | R,S | Load double-precision floating-point value from memory
LDC2 | 25 | R,S | Load double-precision floating-point value from memory, 2-byte aligned
LDF | 26 | R,S | Load single-precision floating-point value from memory
LDF2 | 27 | R,S | Load single-precision floating-point value from memory, 2-byte aligned
LH | 22 | R,S | Load halfword from memory
LHU | 23 | R,S | Load halfword from memory, unsigned
LUI | 0F | R,N | Load upper immediate into register
LW | 28 | R,S | Load word from memory
LWC | 2C | R,S | Load word from memory, 2-byte aligned
LWC2 | 2D | R,S | Load word from memory, 4-byte aligned
LWL | 2A | R,S | Load word from memory, low byte
LWR | 2B | R,S | Load word from memory, high byte
MFC0 | 40 | R,N | Move from coprocessor 0
MFHI | 41 | R | Move from high register
MFLO | 42 | R | Move from low register
MOVN | 48 | R,S,N | Move if not equal
MOVZ | 49 | R,S,N | Move if not zero

