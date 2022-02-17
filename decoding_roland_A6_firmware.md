The following is my initial look into the A6 OS. 

It isn't entirely relevant per se to the original goal, but it may preserve the grooundwork for future SP-808/A-6 hackers, and helps to get things clear in my head.


The MIDI files that hold the A6 OS update are interesting in their simplicity. I love the way Roland used an existing functionality to update the hardware.. MIDI interface = free serial interface!

the MIDI standard is simple and Roland haven't deviated from SMF (Standard MIDI File).

The Hitachi Processor is apparently upward compatible with H8/300H instruction set. What I've found id there are many ways to configure the CPU. CPU has 8 sections, I assume one MIDI file per section.

I parsed the MIDI file of the first MIDI file.

- The header chunk is standard MIDI and checks out. Nothing interesting there.

- There is a single track.

- The Track chunk also checks out, and has the same format through each file, except for the last one which is slightly different at the end.

- The Track itself consists of a list of Track events. These are separated by a time Delta value (Variable length value) and one of 3 main types of Events: MIDI Event, Meta Event and System Exclusive Event. Think of it as a list like this:

in [x] ticks,
we are going to do [x].
in [x] ticks
we are going to do [y].
in [x] ticks
we are going to say "xyz".

etc...


-The A6 OS has 3 Meta events to start with. each consist of the time delta of 0x0, 0xFF that denotes it is a Meta event, The type of meta event, the size (in variable length encoding), and the data.

event 1 (Track name):

Code:
```
00 FF 03 20 53 50 2D 38 30 38 20 56 65 72 20 31 2E 30 31 30 20 6D 6D 6D 20 64 64 20 79 79 79 79 20 31 2F 38
```

where:
0x00 = 0x0 time delta value
0xFF = Denotes this is a Meta Event
0x03 = Denotes this meta event is the Sequence/Track name
0x20 = The length of Data is 32 bytes
the rest = "SP-808 Ver 1.010 mmm dd yyyy 1/8"

event 2 is (copyright notice)

Code:
```
00 FF 02 20 28 43 29 31 39 39 35 2D 31 39 39 38 20 52 6F 6C 61 6E 64 20 43 6F 72 70 6F 72 61 74 69 6F 6E 2E
```

where:
0x00 = 0x0 time delta value
0xFF = Denotes this is a Meta Event
0x02 = Denotes this meta event is the Copyright notice.
0x20 = The length of Data is 32 bytes
the rest = "(C)1995-1998 Roland Corporation."

event 2 sets up the Tempo and the delta time is based off this value.

Code:
```
00 FF 51 03 07 A1 20
```

where:
0x00 = 0x0 time delta value
0xFF = Denotes this is a Meta Event
0x51 = Denotes this meta event is setting the Tempo
0x03 0x07 0xA1 0x20 = Set tempo to 50000 Microseconds per Quarter Note


After these 3 events, there are 348 System Exclusive events (SysEx).

SysEx events can be used in a couple of different ways, but here they are used like this:

[delta time value] [SysEx byte 0xF0] [length of Data in variable length encoding] [Data]

a quick note on Variable length Encoding. It allows one to specify a size in as many bytes as you need, but no more, and no more than 4 (to everything below a 32bit ceiling)
basically, you can use the low 7 bits of the byte for your value. If you dont have enough, you set the highest bit to 1, and continue with the next byte. if the highest bit is 0, you know it is the last byte of the length. Because you are expecting a length byte/bytes, AND you know if high bit is 0... you know when length value stops. Brilliant!

Each is made up of :

Code:
```
10 F0 <size> <DATA bytes> F7
```

0x10 = time delta (time from previous event. Guessing this could be a baud rate of sorts for file transfer
0xF0 = SysEv
0xF7 = stop byte or you could say end of DATA.

here is a list of the sizes of DATA bytes in each event in each MIDI file

A6-1.MID :

1 event 0x11
1 event 0x33
1 event 0x1E
344 events 0x816E
1 event 0x11

A6-2 to A6-7 have the same:

1 event 0x11
1 event 0x33
344 events 0x816E
1 event 0x11

A6-1.MID :

1 event 0x11
1 event 0x33
1 event 0x812E
336 events 0x816E
1 event 0x8126
1 event 0x0F
1 event 0x11


I have run oout of time today to add the rest of the research, but quickly.. I am thinking the first events setup processor firmware upgrade, the large chunks are the firmware, and the end is either checksup or some end routine.
I stripped the MIDI control bytes out of the first MIDI file and I am thinking the result of all data bytes as a blob is more than likely each part of the H8 CPU firmware (OS).

I tried disassembling based around H8s/300H instructions but I think there is a bit more work to do for disassembling such as finding the vector table, properly setting up the address space in the disassembler etc..
I havent looked at the blob a whole lot yet, but it does show some clear patterns. Here is the first few SysEx events (truncated a bit, with the MIDI stuff stripped away):

Code:
```
41 00 7C 12 01 02 00 00 00 00 00 00 00 07 00 76 F7
41 00 7C 12 01 03 00 00 00 00 00 00 53 50 2D 38 30 38 20 56 65 72 20 31 2E 30 31 30 20 6D 6D 6D 20 64 64 20 79 79 79 79 20 68 68 3A 6D 6D 3A 73 73 38 F7
41 00 7C 12 01 00 00 00 00 00 00 00 00 00 01 00 00 00 00 00 00 00 01 0C 00 00 00 00 71 F7
41 00 7C 12 00 00 01 00 00 00 00 00 5A 13 14 78 54 53 32 00 35 45 53 59 53 00 5D 00 03 72 61 04 0F 00 00 20 0C 00 00 52 6F 6C 61 00 6E 64 45 43 01 10 6D 00 72..
41 00 7C 12 00 00 01 00 00 00 0C 04 5C 00 01 30 0D 06 79 08 20 7F 7F 46 3C 19 66 30 7D 01 40 16 17 76 0F 42 40 0A 60 68 08 28 16 53 46 06 0C 58 16 58 47 02 0A..
41 00 7C 12 00 00 01 00 00 01 08 08 00 08 0D 60 6E 18 00 0A 09 79 00 00 01 1A 0E 00 4B 04 10 10 40 78 6A 02 09 70 5E 14 09 6A 09 35 70 5E 01 20 6D 76 54 60 70..
41 00 7C 12 00 00 01 00 00 02 04 0C 6E 68 00 08 70 28 6E 00 68 00 08 18 08 6E 68 45 00 09 79 00 00 01 1A 00 0D 4B 04 10 10 40 78 01 6A 09 70 5E 14 09 6A 1A 09..
41 00 7C 12 00 00 01 00 00 03 01 00 33 64 14 0D 0C 58 55 2A 2A 0D 06 1D 60 46 16 04 6A 2D 00 40 33 64 0C 02 58 55 1A 0D 06 1D 60 41 46 06 79 00 7F 7F 40 06 08..
41 00 7C 12 00 00 01 00 00 03 0D 04 68 08 28 16 46 5A 19 18 55 40 10 0D 50 17 70 01 0F 61 0A 01 68 19 29 29 7F 47 08 0B 55 79 25 40 00 04 4D 6A 79 25 00 08 04..
41 00 7C 12 00 00 01 00 00 04 09 08 0D 50 17 70 0F 61 0A 2A 01 78 7F 68 18 40 76 74 0D 50 17 70 7A 01 00 08 00 00 04 0A 61 0A 01 05 68 19 29 7F 46 26 17 18 75..
41 00 7C 12 00 00 01 00 00 05 05 0C 40 0E 0D 50 17 70 7A 02 16 00 00 00 08 0A 06 01 18 08 68 68 01 20 6D 28 76 01 10 6D 73 54 70 00 6A 28 00 40 10 01 47 00 04..
41 00 7C 12 00 00 01 00 00 06 02 00 0B 56 79 26 00 10 4D 00 40 5C 00 0C 3E 0D 00 40 58 70 00 3C 5E 12 62 08 10 04 40 7A 06 00 40 50 02 0C 7A 01 00 12 64 00 1C..
41 00 7C 12 00 00 01 00 00 06 0E 04 40 08 19 00 6B 20 00 02 40 10 1E 01 20 6D 76 00 01 10 6D 73 54 70 01 00 10 6D 74 0D 05 7A 04 10 00 40 10 00 6E 48 00 00 01..
41 00 7C 12 00 00 01 00 00 07 0A 08 00 40 10 1E 78 01 5C 04 00 0B 0A 0D 00 47 42 10 79 00 20 00 6B 20 00 12 60 00 0C 78 03 5C 00 08 0B 76 0D 00 47 2E 79 00 00..
41 00 7C 12 00 00 01 00 00 08 06 0C 79 40 00 20 5C 00 09 08 4C 6B 20 00 60 00 0C 50 78 11 68 68 79 00 00 68 11 5C 00 09 3A 6B 20 45 00 60 00 0E 5C 00 0B 00 20..
41 00 7C 12 00 00 01 00 00 09 03 00 7F 00 69 70 0D 40 79 4A 60 7F 00 6F 70 00 02 24 5A 10 0A 2C 01 00 6F 00 62 00 0E 78 01 6E 68 49 00 03 19 00 6B 20 00 02 40..
41 00 7C 12 00 00 01 00 00 09 0F 04 00 02 69 30 18 08 68 0A 68 40 28 6A 30 00 60 40 00 1C 73 30 47 44 5C 02 00 07 76 01 00 6F 60 00 00 0E 7A 10 00 00 01 00 00..
```

when I get time later I am going to have a closer look at the CPU manual and instruction set. Kind of starting make a little headway :)


