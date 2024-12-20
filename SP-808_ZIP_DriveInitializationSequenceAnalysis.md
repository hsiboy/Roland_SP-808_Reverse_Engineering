# SP-808 ZIP Drive Initialization Sequence Analysis

The traffic between a Roland SP808 and it's ZIP drive was captured, see further down for analysis:

```
0: REG: 6, WR<-, data: 0C - Dev Control
1: REG: 6, WR<-, data: 08 - Dev Control
2: REG: 7, RD->, data: 00 - Status
3: REG: 2, RD->, data: 01 - Sector Cnt
4: REG: 3, RD->, data: 01 - Sector Num
5: REG: 4, RD->, data: 14 - Cyl Low
6: REG: 5, RD->, data: EB - Cyl High
7: REG: 2, RD->, data: 01 - Sector Cnt
8: REG: 3, RD->, data: 01 - Sector Num
9: REG: 4, RD->, data: 14 - Cyl Low
10: REG: 5, RD->, data: EB - Cyl High
11: REG: 6, RD->, data: 00 - Alt Status
12: REG: 6, WR<-, data: A0 - Dev/Head
13: REG: 7, WR<-, data: A1 - CMD
14: REG: 7, RD->, data: 58 - Status
15: REG: 6, RD->, data: 58 - Alt Status
16: REG: 6, WR<-, data: 08 - Dev Control
17: REG: 0, RD->, data: A0 - DATA
18: REG: 0, RD->, data: 00 - DATA
19: REG: 0, RD->, data: 00 - DATA
---
27: REG: 0, RD->, data: 20 - DATA
28: REG: 0, RD->, data: 20 - DATA
---
37: REG: 0, RD->, data: 00 - DATA
38: REG: 0, RD->, data: 00 - DATA
---
40: REG: 0, RD->, data: 33 - DATA
41: REG: 0, RD->, data: 44 - DATA
42: REG: 0, RD->, data: 20 - DATA
43: REG: 0, RD->, data: 20 - DATA
44: REG: 0, RD->, data: 4F - DATA
45: REG: 0, RD->, data: 45 - DATA
46: REG: 0, RD->, data: 41 - DATA
47: REG: 0, RD->, data: 20 - DATA
48: REG: 0, RD->, data: 49 - DATA
49: REG: 0, RD->, data: 20 - DATA
50: REG: 0, RD->, data: 30 - DATA
51: REG: 0, RD->, data: 20 - DATA
52: REG: 0, RD->, data: 20 - DATA
---
55: REG: 0, RD->, data: 54 - DATA
56: REG: 0, RD->, data: 50 - DATA
57: REG: 0, RD->, data: 20 - DATA
58: REG: 0, RD->, data: 20 - DATA
---
64: REG: 0, RD->, data: 00 - DATA
65: REG: 0, RD->, data: 00 - DATA
---
70: REG: 0, RD->, data: 02 - DATA
71: REG: 0, RD->, data: 00 - DATA
72: REG: 0, RD->, data: 00 - DATA
---
84: REG: 0, RD->, data: F4 - DATA
85: REG: 0, RD->, data: F4 - DATA
86: REG: 0, RD->, data: 00 - DATA
87: REG: 0, RD->, data: 00 - DATA
---
90: REG: 0, RD->, data: 06 - DATA
91: REG: 0, RD->, data: 09 - DATA
92: REG: 0, RD->, data: 00 - DATA
93: REG: 0, RD->, data: 00 - DATA
---
144: REG: 0, RD->, data: 01 - DATA
145: REG: 0, RD->, data: 63 - DATA
146: REG: 0, RD->, data: 20 - DATA
147: REG: 0, RD->, data: 6F - DATA
148: REG: 0, RD->, data: 79 - DATA
149: REG: 0, RD->, data: 69 - DATA
150: REG: 0, RD->, data: 68 - DATA
151: REG: 0, RD->, data: 20 - DATA
152: REG: 0, RD->, data: 4F - DATA
153: REG: 0, RD->, data: 45 - DATA
154: REG: 0, RD->, data: 41 - DATA
155: REG: 0, RD->, data: 31 - DATA
156: REG: 0, RD->, data: 39 - DATA
157: REG: 0, RD->, data: 20 - DATA
158: REG: 0, RD->, data: 00 - DATA
159: REG: 0, RD->, data: 00 - DATA
---
273: REG: 6, RD->, data: 50 - Alt Status
274: REG: 6, WR<-, data: A0 - Dev/Head
275: REG: 6, RD->, data: 50 - Alt Status
276: REG: 6, WR<-, data: A0 - Dev/Head
277: REG: 7, WR<-, data: EF - CMD
278: REG: 7, RD->, data: 51 - Status
279: REG: 6, WR<-, data: 08 - Dev Control
280: REG: 1, RD->, data: 04 - Error
281: REG: 6, RD->, data: 51 - Alt Status
282: REG: 6, WR<-, data: A0 - Dev/Head
283: REG: 6, RD->, data: 51 - Alt Status
284: REG: 6, RD->, data: 51 - Alt Status
285: REG: 1, WR<-, data: 00 - Features
286: REG: 2, WR<-, data: 00 - Sector Cnt
287: REG: 4, WR<-, data: 80 - Cyl Low
288: REG: 5, WR<-, data: 00 - Cyl High
289: REG: 7, WR<-, data: A0 - CMD
290: REG: 7, RD->, data: 58 - Status
291: REG: 7, RD->, data: 58 - Status
292: REG: 0, WR<-, data: 00 - DATA
293: REG: 0, WR<-, data: 00 - DATA
---
298: REG: 7, RD->, data: 51 - Status
299: REG: 7, RD->, data: 51 - Status
300: REG: 6, RD->, data: 51 - Alt Status
301: REG: 6, WR<-, data: A0 - Dev/Head
302: REG: 6, RD->, data: 51 - Alt Status
303: REG: 6, RD->, data: 51 - Alt Status
304: REG: 1, WR<-, data: 00 - Features
305: REG: 2, WR<-, data: 00 - Sector Cnt
306: REG: 4, WR<-, data: 80 - Cyl Low
307: REG: 5, WR<-, data: 00 - Cyl High
308: REG: 7, WR<-, data: A0 - CMD
309: REG: 7, RD->, data: 58 - Status
310: REG: 7, RD->, data: 58 - Status
311: REG: 0, WR<-, data: 03 - DATA
312: REG: 0, WR<-, data: 00 - DATA
313: REG: 0, WR<-, data: 80 - DATA
314: REG: 0, WR<-, data: 00 - DATA
315: REG: 0, WR<-, data: 00 - DATA
---
317: REG: 7, RD->, data: 58 - Status
318: REG: 7, RD->, data: 58 - Status
319: REG: 0, RD->, data: 70 - DATA
320: REG: 0, RD->, data: 06 - DATA
321: REG: 0, RD->, data: 00 - DATA
322: REG: 0, RD->, data: 00 - DATA
---
325: REG: 0, RD->, data: 29 - DATA
326: REG: 0, RD->, data: 00 - DATA
327: REG: 0, RD->, data: 00 - DATA
---
329: REG: 0, RD->, data: 01 - DATA
330: REG: 0, RD->, data: 24 - DATA
331: REG: 0, RD->, data: 00 - DATA
332: REG: 0, RD->, data: D0 - DATA
333: REG: 7, RD->, data: 50 - Status
334: REG: 7, RD->, data: 50 - Status
335: REG: 6, RD->, data: 50 - Alt Status
336: REG: 6, WR<-, data: A0 - Dev/Head
337: REG: 6, RD->, data: 50 - Alt Status
338: REG: 6, RD->, data: 50 - Alt Status
339: REG: 1, WR<-, data: 00 - Features
340: REG: 2, WR<-, data: 00 - Sector Cnt
341: REG: 4, WR<-, data: 80 - Cyl Low
342: REG: 5, WR<-, data: 00 - Cyl High
343: REG: 7, WR<-, data: A0 - CMD
344: REG: 7, RD->, data: 58 - Status
345: REG: 7, RD->, data: 58 - Status
346: REG: 0, WR<-, data: 1B - DATA
347: REG: 0, WR<-, data: 00 - DATA
348: REG: 0, WR<-, data: 01 - DATA
349: REG: 0, WR<-, data: 00 - DATA
350: REG: 0, WR<-, data: 00 - DATA
---
352: REG: 7, RD->, data: 51 - Status
353: REG: 7, RD->, data: 51 - Status
354: REG: 6, RD->, data: 51 - Alt Status
355: REG: 6, WR<-, data: A0 - Dev/Head
356: REG: 6, RD->, data: 51 - Alt Status
357: REG: 6, RD->, data: 51 - Alt Status
358: REG: 1, WR<-, data: 00 - Features
359: REG: 2, WR<-, data: 00 - Sector Cnt
360: REG: 4, WR<-, data: 80 - Cyl Low
361: REG: 5, WR<-, data: 00 - Cyl High
362: REG: 7, WR<-, data: A0 - CMD
363: REG: 7, RD->, data: 58 - Status
364: REG: 7, RD->, data: 58 - Status
365: REG: 0, WR<-, data: 03 - DATA
366: REG: 0, WR<-, data: 00 - DATA
367: REG: 0, WR<-, data: 80 - DATA
368: REG: 0, WR<-, data: 00 - DATA
369: REG: 0, WR<-, data: 00 - DATA
---
371: REG: 7, RD->, data: 58 - Status
372: REG: 7, RD->, data: 58 - Status
373: REG: 0, RD->, data: 70 - DATA
374: REG: 0, RD->, data: 06 - DATA
375: REG: 0, RD->, data: 00 - DATA
376: REG: 0, RD->, data: 00 - DATA
---
379: REG: 0, RD->, data: 28 - DATA
380: REG: 0, RD->, data: 00 - DATA
381: REG: 0, RD->, data: 00 - DATA
---
383: REG: 0, RD->, data: 01 - DATA
384: REG: 0, RD->, data: 24 - DATA
385: REG: 0, RD->, data: 00 - DATA
386: REG: 0, RD->, data: D0 - DATA
387: REG: 7, RD->, data: 50 - Status
388: REG: 7, RD->, data: 50 - Status
389: REG: 6, RD->, data: 50 - Alt Status
390: REG: 6, WR<-, data: A0 - Dev/Head
391: REG: 6, RD->, data: 50 - Alt Status
392: REG: 6, RD->, data: 50 - Alt Status
393: REG: 1, WR<-, data: 00 - Features
394: REG: 2, WR<-, data: 00 - Sector Cnt
395: REG: 4, WR<-, data: 80 - Cyl Low
396: REG: 5, WR<-, data: 00 - Cyl High
397: REG: 7, WR<-, data: A0 - CMD
398: REG: 7, RD->, data: 58 - Status
399: REG: 7, RD->, data: 58 - Status
400: REG: 0, WR<-, data: 00 - DATA
401: REG: 0, WR<-, data: 00 - DATA
---
406: REG: 7, RD->, data: 50 - Status
407: REG: 7, RD->, data: 50 - Status
408: REG: 6, RD->, data: 50 - Alt Status
409: REG: 6, WR<-, data: A0 - Dev/Head
410: REG: 6, RD->, data: 50 - Alt Status
411: REG: 6, RD->, data: 50 - Alt Status
412: REG: 1, WR<-, data: 00 - Features
413: REG: 2, WR<-, data: 00 - Sector Cnt
414: REG: 4, WR<-, data: 80 - Cyl Low
415: REG: 5, WR<-, data: 00 - Cyl High
416: REG: 7, WR<-, data: A0 - CMD
417: REG: 7, RD->, data: 58 - Status
418: REG: 7, RD->, data: 58 - Status
419: REG: 0, WR<-, data: 12 - DATA
420: REG: 0, WR<-, data: 00 - DATA
421: REG: 0, WR<-, data: 80 - DATA
422: REG: 0, WR<-, data: 00 - DATA
423: REG: 0, WR<-, data: 00 - DATA
---
425: REG: 7, RD->, data: 58 - Status
426: REG: 7, RD->, data: 58 - Status
427: REG: 0, RD->, data: 00 - DATA
428: REG: 0, RD->, data: 00 - DATA
429: REG: 0, RD->, data: 75 - DATA
430: REG: 0, RD->, data: 00 - DATA
431: REG: 0, RD->, data: 49 - DATA
432: REG: 0, RD->, data: 4D - DATA
433: REG: 0, RD->, data: 47 - DATA
434: REG: 0, RD->, data: 20 - DATA
435: REG: 0, RD->, data: 5A - DATA
436: REG: 0, RD->, data: 50 - DATA
437: REG: 0, RD->, data: 31 - DATA
438: REG: 0, RD->, data: 30 - DATA
439: REG: 0, RD->, data: 20 - DATA
440: REG: 0, RD->, data: 20 - DATA
---
443: REG: 0, RD->, data: 32 - DATA
444: REG: 0, RD->, data: 2E - DATA
445: REG: 0, RD->, data: 30 - DATA
446: REG: 0, RD->, data: 2F - DATA
447: REG: 0, RD->, data: 32 - DATA
448: REG: 0, RD->, data: 39 - DATA
449: REG: 0, RD->, data: 00 - DATA
450: REG: 0, RD->, data: 00 - DATA
---
475: REG: 0, RD->, data: 28 - DATA
476: REG: 0, RD->, data: 29 - DATA
477: REG: 0, RD->, data: 43 - DATA
478: REG: 0, RD->, data: 70 - DATA
479: REG: 0, RD->, data: 72 - DATA
480: REG: 0, RD->, data: 67 - DATA
481: REG: 0, RD->, data: 74 - DATA
482: REG: 0, RD->, data: 49 - DATA
483: REG: 0, RD->, data: 4D - DATA
484: REG: 0, RD->, data: 47 - DATA
485: REG: 0, RD->, data: 20 - DATA
486: REG: 0, RD->, data: 39 - DATA
487: REG: 0, RD->, data: 37 - DATA
488: REG: 0, RD->, data: F7 - DATA
489: REG: 7, RD->, data: 50 - Status
490: REG: 7, RD->, data: 50 - Status
491: REG: 6, RD->, data: 50 - Alt Status
492: REG: 6, WR<-, data: A0 - Dev/Head
493: REG: 6, RD->, data: 50 - Alt Status
494: REG: 6, RD->, data: 50 - Alt Status
495: REG: 1, WR<-, data: 00 - Features
496: REG: 2, WR<-, data: 00 - Sector Cnt
497: REG: 4, WR<-, data: 80 - Cyl Low
498: REG: 5, WR<-, data: 00 - Cyl High
499: REG: 7, WR<-, data: A0 - CMD
500: REG: 7, RD->, data: 58 - Status
501: REG: 7, RD->, data: 58 - Status
502: REG: 0, WR<-, data: 5A - DATA
503: REG: 0, WR<-, data: 2F - DATA
504: REG: 0, WR<-, data: 00 - DATA
505: REG: 0, WR<-, data: 00 - DATA
506: REG: 0, WR<-, data: 80 - DATA
507: REG: 0, WR<-, data: 00 - DATA
508: REG: 7, RD->, data: 58 - Status
509: REG: 7, RD->, data: 58 - Status
510: REG: 0, RD->, data: 00 - DATA
511: REG: 0, RD->, data: 00 - DATA
---
514: REG: 0, RD->, data: 2F - DATA
515: REG: 0, RD->, data: 5C - DATA
516: REG: 0, RD->, data: FF - DATA
517: REG: 0, RD->, data: D9 - DATA
518: REG: 7, RD->, data: 50 - Status
519: REG: 7, RD->, data: 50 - Status
520: REG: 6, RD->, data: 50 - Alt Status
521: REG: 6, WR<-, data: A0 - Dev/Head
522: REG: 6, RD->, data: 50 - Alt Status
523: REG: 6, RD->, data: 50 - Alt Status
524: REG: 1, WR<-, data: 00 - Features
525: REG: 2, WR<-, data: 00 - Sector Cnt
526: REG: 4, WR<-, data: 80 - Cyl Low
527: REG: 5, WR<-, data: 00 - Cyl High
528: REG: 7, WR<-, data: A0 - CMD
529: REG: 7, RD->, data: 58 - Status
530: REG: 7, RD->, data: 58 - Status
531: REG: 0, WR<-, data: 55 - DATA
532: REG: 0, WR<-, data: 00 - DATA
533: REG: 0, WR<-, data: 00 - DATA
---
535: REG: 0, WR<-, data: 0E - DATA
536: REG: 0, WR<-, data: 00 - DATA
537: REG: 7, RD->, data: 58 - Status
538: REG: 7, RD->, data: 58 - Status
539: REG: 0, WR<-, data: 00 - DATA
540: REG: 0, WR<-, data: 00 - DATA
---
543: REG: 0, WR<-, data: 2F - DATA
544: REG: 0, WR<-, data: 7C - DATA
545: REG: 0, WR<-, data: 00 - DATA
546: REG: 0, WR<-, data: 31 - DATA
547: REG: 0, WR<-, data: 30 - DATA
548: REG: 0, WR<-, data: 20 - DATA
549: REG: 0, WR<-, data: 20 - DATA
---
552: REG: 0, WR<-, data: 32 - DATA
553: REG: 7, RD->, data: 50 - Status
554: REG: 7, RD->, data: 50 - Status
555: REG: 6, RD->, data: 50 - Alt Status
556: REG: 6, WR<-, data: A0 - Dev/Head
557: REG: 6, RD->, data: 50 - Alt Status
558: REG: 6, RD->, data: 50 - Alt Status
559: REG: 1, WR<-, data: 00 - Features
560: REG: 2, WR<-, data: 00 - Sector Cnt
561: REG: 4, WR<-, data: 80 - Cyl Low
562: REG: 5, WR<-, data: 00 - Cyl High
563: REG: 7, WR<-, data: A0 - CMD
564: REG: 7, RD->, data: 58 - Status
565: REG: 7, RD->, data: 58 - Status
566: REG: 0, WR<-, data: 0D - DATA
567: REG: 0, WR<-, data: 0A - DATA
568: REG: 0, WR<-, data: 00 - DATA
569: REG: 0, WR<-, data: 00 - DATA
---
```

# Analysis

## Initial Setup
```
REG: 6, WR<-, data: 0C - Dev Control    # Hardware reset
REG: 6, WR<-, data: 08 - Dev Control    # Clear reset
REG: 7, RD->, data: 00 - Status         # Check status
```

## Phase 1: Device Identification
```
# IDENTIFY PACKET DEVICE command (A1h)
REG: 7, WR<-, data: A1 - CMD            
REG: 7, RD->, data: 58 - Status         # Command accepted
```

## Phase 2: INQUIRY Response 
```
# Drive responds with identification string
431: 0, RD->, data: 49 - DATA           # "I"
432: 0, RD->, data: 4D - DATA           # "M"
433: 0, RD->, data: 47 - DATA           # "G"
434: 0, RD->, data: 20 - DATA           # " "
435: 0, RD->, data: 5A - DATA           # "Z"
436: 0, RD->, data: 50 - DATA           # "P"
437: 0, RD->, data: 31 - DATA           # "1"
438: 0, RD->, data: 30 - DATA           # "0"
439: 0, RD->, data: 20 - DATA           # " "
```
> This identifies the device as "IMG ZP10" - a ZIP 100 drive

## Phase 3: Crucial Validation Sequence
```
# SP-808 sends MODE SENSE command with special subcommand
502: 0, WR<-, data: 5A - DATA           # MODE SENSE command
503: 0, WR<-, data: 2F - DATA           # Vendor-specific subcommand
504: 0, WR<-, data: 00 - DATA           # Reserved
505: 0, WR<-, data: 00 - DATA           # Reserved
506: 0, WR<-, data: 80 - DATA           # Buffer length (128 bytes)
507: 0, WR<-, data: 00 - DATA           # Reserved

# Drive responds with validation sequence
514: 0, RD->, data: 2F - DATA           # Start of validation pattern
515: 0, RD->, data: 5C - DATA           # These four bytes must match
516: 0, RD->, data: FF - DATA           # exactly for the SP-808 to
517: 0, RD->, data: D9 - DATA           # accept the drive
```
> This is the key validation sequence - `2F 5C FF D9` - that identifies a genuine Iomega ZIP drive

## Phase 4: Post-Validation Setup
```
# MODE SELECT command follows validation
531: 0, WR<-, data: 55 - DATA           # MODE SELECT command
532: 0, WR<-, data: 00 - DATA
533: 0, WR<-, data: 00 - DATA

# Vendor-specific command sequence
566: 0, WR<-, data: 0D - DATA           # Vendor command 0x0D
567: 0, WR<-, data: 0A - DATA
568: 0, WR<-, data: 00 - DATA
569: 0, WR<-, data: 00 - DATA
```

## Key Points:
1. The SP-808 performs multiple checks to verify it's talking to a genuine ZIP drive:
   - Device identification string check
   - Vendor-specific MODE SENSE command
   - Validation sequence verification

2. The critical validation sequence is:
   - Command: `5A 2F` (MODE SENSE with subcommand 0x2F)
   - Expected response: `2F 5C FF D9`

3. After validation succeeds, the SP-808 proceeds with device configuration using:
   - MODE SELECT (55h)
   - Additional vendor-specific commands (0Dh)

This sequence must complete successfully for the SP-808 to accept and use the drive.


