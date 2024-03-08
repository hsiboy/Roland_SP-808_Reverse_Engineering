The Renesas H8S/2655 harware manual explains that:

> The top area starting at H'00000000 is allocated to the exception vector table in units of 32 bits. In each 32 bits, the upper 8 bits are ignored and a branch address is stored in the lower 24 bits.

The first 64 bytes of the firmware file looks like this:

```
00000000  5a 12 cc 54 54 53 32 35  45 53 59 53 00 13 03 e9  |Z..TTS25ESYS....|
00000010  00 01 01 00 00 0c 00 00  52 6f 6c 61 6e 64 45 43  |........RolandEC|
00000020  01 10 6d f2 01 20 6d f4  18 88 6a 88 f0 de 6a a8  |..m.. m...j...j.|
00000030  00 40 34 63 6a a8 00 40  34 62 7a 06 00 40 34 2e  |.@4cj..@4bz..@4.|
```

Taking the statement in the manual at face value, that means that the first 4 bytes (32 bits) at H'00000000

```
00000000  5a 12 cc 54 ...
```

contain the the 24 bits of the vector address we're interesting in:

```
5a 12 cc 54

In Binary (32 bits):
01011010 00010010 11001100 01010100

Lower 24 bits (binary):
xxxxxxxx 00010010 11001100 01010100

Lower 24 bits (hex): 12 CC 54
```

Therefore our code should start at H'0012CC54, but, the whole firmware is only `C0004` long! so clearly that's not the value we want.

If we inspect the file futher, we find the last 64 bytes are:

```
000bffd0  00 00 00 00 00 00 00 00  00 00 ff ff ff ff ff ff  |................|
000bffe0  5a 12 cc 54 54 53 32 35  45 53 59 53 00 13 03 e9  |Z..TTS25ESYS....|
000bfff0  00 01 01 00 00 0c 00 00  52 6f 6c 61 6e 64 45 43  |........RolandEC|
000c0000  00 00 00 00                                       |....|
000c0004
```
That looks very familliar doesnt it!

So, perhaps our vector is at `H'00000020`?

```
00000020  01 10 6d f2 01 20 6d f4  18 88 6a 88 f0 de 6a a8  |..m.. m...j...j.|
```

That would give us `10 6D F2` which is again, still bigger than `C0004`, unless of course, the whole file needs to be offset by `100000`? 

> [!NOTE]
> We don't know what the memory map is, and IDA doesn't/can't help us, so we will have to make some assumptions.

---



eye balling the firmware in a hex viewer, i can see that the file is zero padded from `7C883` to `BFFD0A`

```
0007c870  20 4f 55 54 00 54 48 52  55 00 00 42 6e 0a ff ff  | OUT.THRU..Bn...|
0007c880  ff ff ff 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
0007c890  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
* Zero padded...
000bffd0  00 00 00 00 00 00 00 00  00 00 ff ff ff ff ff ff  |................|
000bffe0  5a 12 cc 54 54 53 32 35  45 53 59 53 00 13 03 e9  |Z..TTS25ESYS....|
000bfff0  00 01 01 00 00 0c 00 00  52 6f 6c 61 6e 64 45 43  |........RolandEC|
000c0000  00 00 00 00                                       |....|
000c0004
```


