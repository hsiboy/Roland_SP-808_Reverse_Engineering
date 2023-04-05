The Roland SP-808 groovebox uses a Hitachi HD6432653 CPU or H8S/2600

Its a General-register machine, with Sixteen 16-bit general registers (also usable as sixteen 8-bit registers
or eight 32-bit registers).

A Maximum clock rate: 20 MHz
8/16/32-bit register-register add/subtract: 50 ns
16 × 16-bit register-register multiply: 200 ns
16 × 16 + 42-bit multiply and accumulate: 200 ns
32 ÷ 16-bit register-register divide: 1000 ns
Its instruction set is suitable for high-speed operation

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
• More general registers and control registers
* Eight 16-bit expanded registers, and one 8-bit and two 32-bit control registers, have been
added.
• Expanded address space
* Normal mode supports the same 64-kbyte address space as the H8/300 CPU.
* Advanced mode supports a maximum 16-Mbyte address space.
• Enhanced addressing
* The addressing modes have been enhanced to make effective use of the 16-Mbyte address
space.
• Enhanced instructions
* Addressing modes of bit-manipulation instructions have been enhanced.
* Signed multiply and divide instructions have been added.
* A multiply-and-accumulate instruction has been added.
* Two-bit shift instructions have been added.
* Instructions for saving and restoring multiple registers have been added.
* A test and set instruction has been added

These newly added instructions, mean that tools like binwalk and objdump fail.

It's worth noting that instructions on the H8S/2600 execute twice as fast as they did on the H8/300H.
