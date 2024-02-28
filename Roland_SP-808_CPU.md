# The SP-808 CPU

The Roland SP-808 groovebox uses a Hitachi HD6432653 or H8S/2655 Series MCU.

The "Quick Reference Guide to Hitachi Semiconductor Devices" lists it as H8S/2653 HD6432653 64k ROM and 4k RAM running at 5V with 20MHz clock.

Refer to the H8S/2600 Series and H8S/2000 Series Programming Manual for a detailed description of the instruction set.
Refer to the H8S/2655 Series manual for hardware specification.

The Hitachi H8/2655 series is an outdated microcontroller that was widely used in the 1990s and early 2000s. The H8S/2655 series, in particular, was designed to offer a balance between performance, power consumption, and integrated peripherals, making them a versatile choice for embedded systems.

While it is known for its simple architecture and low power consumption, it poses significant challenges when it comes to reverse engineering its firmware.

One of the main difficulties in reverse engineering H8/2600 firmware is the lack of modern tools and resources. Unlike more modern processors, the H8/2600 does not have sophisticated debugging or tracing capabilities, making it much harder to understand how the firmware works.

Another challenge is the lack of documentation and support for the H8/2600. Since this processor is no longer in widespread use, finding technical information or help online can be difficult. This can be particularly frustrating for reverse engineers who are trying to understand the inner workings of a particular piece of hardware or software that uses the H8/2600.

## Looking at the PCB

PIN 83 STBY is held high.

PIN 82 NMI (Non Maskable Interupt) is held high, which means NMI is not being used.

MIDI is communicated via pin 61 (P3<sub>0</sub> / RXD<sub>0</sub>) and pin 59 (P3<sub>2</sub> / TXD<sub>0</sub>) 

---

> [!TIP]
> The MCU isnt directly handling the IDE interface, this is being handled by an EPSON ASIC (SLA919F), and the MCU communicates with it.

On the PCB, the pins (MD2 to MD0) that control the MCU Operating Mode are set as follows:

PIN | NAME | H/L
-- | -- | -- 
123 | MD<sub>0</sub> | Low
124 | MD<sub>1</sub> | High
125 | MD<sub>2</sub> | High

Which means the CPU is running in Mode 6 - "On-chip ROM enabled, expansion mode". 

This means the MCU is running in Advanced mode!

---

## Mode 6

The address space is 16 Mbytes in modes 4 to 7 (advanced modes).
The on-chip ROM of H8S/2655 contains 128 kbytes, but only 56 kbytes are available in modes 2 and 3 (normal modes).
The address space is divided into eight areas for modes 4 to 7.

In Advanced mode, Linear access is provided to a 16-Mbyte maximum address space (architecturally a maximum 16-Mbyte program area and a maximum 4-Gbyte data area, with a maximum of 4 Gbytes for program and data areas combined). 

> [!NOTE]
> While the CPU’s architecture allows for 4 Gbytes of address space, the H8S/2655 Group can actually accesses a maximum of 16 Mbytes.

Modes 1, 2, and 4 to 6 are externally expanded modes that allow access to external memory and peripheral devices.

The external expansion modes allow switching between 8-bit and 16-bit bus modes. After program execution starts, an 8-bit or 16-bit address space can be set for each area, depending on the bus controller setting. If 16-bit access is selected for any one area, 16-bit bus mode is set; if 8-bit access is selected for all areas, 8-bit bus mode is set.

> [!NOTE]
> The functions of each pin depend on the operating mode.

The extended registers (E0 to E7) can be used as 16-bit registers, or as the upper 16-bit segments of 32-bit registers or address registers.

All instructions and addressing modes can be used in Advanced Mode.

In Mode 6:

* Ports A, B and C function as input ports immediately after a reset. They can each be set to output addresses by setting the corresponding bits in the data direction register (DDR) to 1. 
* Port D functions as a data bus, and part of port F carries bus control signals.
* The initial bus mode after a reset is 8 bits, with 8-bit access to all areas.

The pin functions of ports A to F vary depending on the operating mode. This Table shows their functions in each operating mode.

|Port | Mode 6|
| --- | --- |
|Port A<sub>7-0</sub> | P*/A|
|Port B | P*/A|
|Port C | P*/A|
|Port D | D|
|Port E | P*/D|
|Port F<sub>7</sub> | P*/C*|
|Port F<sub>6-3</sub> | C|
|Port F<sub>2-0</sub>| P*/C|

Legend:
- P: I/O port
- A: Address bus output
- D: Data bus I/O
- C: Control signals, clock I/O


In advanced mode the top area starting at H'00000000 is allocated to the exception vector table in units of 32 bits. In each 32 bits, the upper 8 bits are ignored and a branch address is stored in the lower 24 bits:

```
           ┌──────────────────────────────────┐
H'00000000 │            Reserved              │
           │----------------------------------│
           │----                          ----│
           │ Power-on reset exception vector  │
           │----                          ----│
H'00000003 ├──────────────────────────────────┤
H'00000004 │             Reserved             │
           │----------------------------------│
           │----                          ----│
           │   Manual reset exception vector  │
           │----                          ----│
H'00000007 ├──────────────────────────────────┤
H'00000008 │----                          ----│
           │----                          ----│
H'0000000B │----                          ----│
           │    (Reserved for system use)     │
H'0000000C │----                              │
           │----                          ----│
           │----                          ----│
           ├──────────────────────────────────┤
H'00000010 │             Reserved             │
           │----------------------------------│
           │----                          ----│
           │        Exception vector 1        │
           │----                          ----│
           ├──────────────────────────────────┤
           │                                  │
           │                   ,-'"`-._,-'"`-─┘
           └─`-._,-'"`"`-._,-'"`

```
*Exception Vector Table (Advanced Mode)*


For details of the exception vector table, see section 4, Exception Handling in the Hardware Manual.

---

## ROM (PROM)

The H8S/2653 has 64 kbytes of on-chip ROM (PROM or mask ROM). The ROM is connected to the H8S/2600 CPU by a 16-bit data bus. The CPU accesses both byte data and word data in one state, making possible rapid instruction fetches and high-speed processing.
The on-chip ROM is enabled or disabled by setting the mode pins (MD2, MD1, and MD0) and bit EAE in BCRL.

---

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

> [!IMPORTANT]
> The H8 line of CPUs is bigendian

I can't find anything in the manuals that explains what address code execution starts at. The manuals do explain that the chip has an 'advanced mode', and in that mode, address 0x00 contains an exception table with addresses to jump to. The first 4 bytes should have the address, but we appear to have a string in the Roland Firmware 🤔

The manual explains that the exception vector table starts at 0x00 and first exception is the restart exception. The CPU handles boot as an exception (power glitch?), so the first four bytes in the firmware, should be a 32 bit address that points to the first instruction, not an ascii string.

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

