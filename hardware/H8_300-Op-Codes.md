# H8/300H Opcodes


All opcodes are multiples of 2 bytes (2,4,6,8,10 bytes), all opcodes should be always located at even addresses (ie. bit0 of jump address/disp operands should be always 0).
```
Register Encoding
  0..7  8bit Registers R0H..R7H  (bit8-15)     ;\RxB
  8..F  8bit Registers R0L..R7L  (bit0-7)      ;/
  0..7  16bit Registers R0..R7   (bit0-15)     ;\Rx
  8..F  16bit Registers E0..E7   (bit16-31)    ;/
  0..7  32bit Registers ER0..ER7 (bit0-31)     ;-ERx (in normal opcodes)
  8..F  32bit Registers ER0..ER7 (bit0-31)     ;-ERx (in opcodes marked *m,*s)
```
## H8/300H Main Opcodes
```
  Opcode             Native                  Nocash             States IxHUNZVC
  0..                --> Misc 0xxx
  1..                --> Misc 1xxx
  2dnn               MOV.B @aa:8,RdB         MOV.B RdB,[FFaa]        4 ----nz0-
  3snn               MOV.B Rs,@aa:8          MOV.B [FFaa],Rs         4 ----nz0-
  4cnn               --> Jumps (relative 8bit range)
  5..                --> Jumps (various) and unsigned mul/div
  6..                --> Misx 6xxx
  7..                --> Misc 7xxx
  8dnn               ADD.B #nn:8,RdB         ADD.B RdB,nn            2 --h-nzvc
  9dnn               ADDX  #nn:8,RdB         ADC.B RdB,nn            2 --h-nzvc
  Adnn               CMP.B #nn:8,RdB         CMP.B RdB,nn            2 --h-nzvc
  Bdnn               SUBX  #nn:8,RdB         SBC.B RdB,nn            2 --h-nzvc
  Cdnn               OR.B  #nn:8,RdB         OR.B  RdB,nn            2 ----nz0-
  Ddnn               XOR.B #nn:8,RdB         XOR.B RdB,nn            2 ----nz0-
  Ednn               AND.B #nn:8,RdB         AND.B RdB,nn            2 ----nz0-
  Fdnn               MOV.B #nn:8,RdB         MOV.B RdB,nn            2 ----nz0-
```
## H8/300H Misc 0xxx
```
  0000               NOP                     NOP                     2 --------
  01..               --> Misc 01xx ;Memory Load/Store (32bit ERn) etc.
  020d               STC.B CCR,RdB           MOV.B RdB,CCR           2 --------
  030s               LDC.B RsB,CCR           MOV.B CCR,RsB           2 xxxxxxxx
  04nn               ORC   #nn:8,CCR         OR.B  CCR,nn            2 xxxxxxxx
  05nn               XORC  #nn:8,CCR         XOR.B CCR,nn            2 xxxxxxxx
  06nn               ANDC  #nn:8,CCR         AND.B CCR,nn            2 xxxxxxxx
  07nn               LDC.B #nn:8,CCR         MOV.B CCR,nn            2 xxxxxxxx
  08sd               ADD.B RsB,RdB           ADD.B RdB,RsB           2 --h-nzvc
  09sd               ADD.W Rs,Rd             ADD.W Rd,Rs             2 --h-nzvc
  0A..               --> Increment/Add
  0B..               --> Increment/Add
  0Csd               MOV.B RsB,RdB           MOV.B RdB,RsB           2 ----nz0-
  0Dsd               MOV.W Rs,Rd             MOV.W Rd,Rs             2 ----nz0-
  0Esd               ADDX  RsB,RdB           ADC.B RdB,RsB           2 --h-nzvc
  0F0d               DAA   RdB               DAA.B RdB               2 --U-nzUc
  0Fsd            *s MOV.L ERs,ERd           MOV.L ERd,ERs           2 ----nz0-
```
## H8/300H Misc 01xx ;Memory Load/Store (32bit ERn) etc.
```
  010069md           MOV.L @ERm,ERd          MOV.L ERd,[ERm]         8 ----nz0-
  014069m0           LDC.W @ERm,CCR          MOV.W CCR,[ERm]         6 xxxxxxxx
  010069ms        *m MOV.L ERs,@ERm          MOV.L [ERm],ERs         8 ----nz0-
  014069m0        *m STC.W CCR,@ERm          MOV.W [ERm],CCR         6 --------
  01006B0dnnnn       MOV.L @aa:16,ERd        MOV.L ERd,[nnnn]       10 ----nz0-
  01406B00nnnn       LDC.W @aa:16,CCR        MOV.W CCR,[nnnn]        8 xxxxxxxx
  01006B2d00nnnnnn   MOV.L @aa:24,ERd        MOV.L ERd,[nnnnnn]     12 ----nz0-
  01406B2000nnnnnn   LDC.W @aa:24,CCR        MOV.W CCR,[nnnnnn]     10 xxxxxxxx
  01006B8snnnn       MOV.L ERs,@aa:16        MOV.L [nnnn],ERs       10 ----nz0-
  01406B80nnnn       STC.W CCR,@aa:16        MOV.W [nnnn],CCR        8 --------
  01006BAs00nnnnnn   MOV.L ERs,@aa:24        MOV.L [nnnnnn],ERs     12 ----nz0-
  01406BA000nnnnnn   STC.W CCR,@aa:24        MOV.W [nnnnnn],CCR     10 --------
  01006Dmd           MOV.L @ERm+,ERd         MOV.L ERd,[ERm+]       10 ----nz0-
  01406Dm0           LDC.W @ERm+,CCR         MOV.W CCR,[ERm+]        8 xxxxxxxx
  01006Dms        *m MOV.L ERs,@-ERm         MOV.L [ERm-],ERs       10 ----nz0-
  01406Dm0        *m STC.W CCR,@-ERm         MOV.W [ERm-],CCR        8 --------
  01006Fmdnnnn       MOV.L @(d:16,ERm),ERd   MOV.L ERd,[ERm+nnnn]   10 ----nz0-
  01406Fm0nnnn       LDC.W @(d:16,ERm),CCR   MOV.W CCR,[ERm+nnnn]    8 xxxxxxxx
  01006Fmsnnnn    *m MOV.L ERs,@(d:16,ERm)   MOV.L [ERm+nnnn],ERs   10 ----nz0-
  01406Fm0nnnn    *m STC.W CCR,@(d:16,ERm)   MOV.W [ERm+nnnn],CCR    8 --------
  010078m06B2d00..   MOV.L @(d:24,ERm),ERd   MOV.L ERd,[ERm+nnnnnn] 14 ----nz0-
  014078m06B2000..   LDC.W @(d:24,ERm),CCR   MOV.W CCR,[ERm+nnnnnn] 12 xxxxxxxx
  010078m06BAs00..*? MOV.L ERs,@(d:24,ERm)   MOV.L [ERm+nnnnnn],ERs 14 ----nz0-
  014078m06BA000..   STC.W CCR,@(d:24,ERm)   MOV.W [ERm+nnnnnn],CCR 12 --------
  0180               SLEEP                   HALT                    2 --------
  01C050sd           MULXS.B RsB,Rd          SMUL.B Rd,RsB          16 ----nz--
  01C052sd           MULXS.W Rs,ERd          SMUL.W ERd,Rs          24 ----nz--
  01D051sd           DIVXS.B RsB,Rd          SDIV.B Rd,RsB          16 ----nz--
  01D053sd           DIVXS.W Rs,ERd          SDIV.W ERd,Rs          24 ----nz--
  01F064sd           OR.L    ERs,ERd         OR.L   ERd,ERs          4 ----nz0-
  01F065sd           XOR.L   ERs,ERd         XOR.L  ERd,ERs          4 ----nz0-
  01F066sd           AND.L   E?Rs,ERd        AND.L  ERd,ERs          4 ----nz0-
```
## H8/300H Misc 1xxx
```
  10..               --> Shift/Rotate (shift left)
  11..               --> Shift/Rotate (shift right)
  12..               --> Shift/Rotate (rotate left)
  13..               --> Shift/Rotate (rotate right)
  14sd               OR.B  RsB,RdB           OR.B  RdB,RsB           2 ----nz0-
  15sd               XOR.B RsB,RdB           XOR.B RdB,RsB           2 ----nz0-
  16sd               AND.B RsB,RdB           AND.B RdB,RsB           2 ----nz0-
  17..               --> Not/Neg/Extend
  18sd               SUB.B RsB,RdB           SUB.B RdB,RsB           2 --h-nzvc
  19sd               SUB.W Rs,Rd             SUB.W Rd,Rs             2 --h-nzvc
  1A..               --> Decrement/Subtract
  1B..               --> Decrement/Subtract
  1Csd               CMP.B RsB,RdB           CMP.B RdB,RsB           2 --h-nzvc
  1Dsd               CMP.W Rs,Rd             CMP.W Rd,Rs             2 --h-nzvc
  1Esd               SUBX  RsB,RdB           SBC.B RdB,RsB           2 --h-nzvc
  1F0d               DAS   RdB               DAS.B RdB               2 --U-nzU?
  1Fsd            *s CMP.L ERs,ERd           CMP.L ERd,ERs           2 --h-nzvc
```
## H8/300H Shift/Rotate (Shift Logical/Arithmetic, Rotate through Carry or not)
```
  100d               SHLL.B RdB              SHL.B RdB               2 ----nz0c
  101d               SHLL.W Rd               SHL.W Rd                2 ----nz0c
  103d               SHLL.L ERd              SHL.L ERd               2 ----nz0c
  108d               SHAL.B RdB              SAL.B RdB               2 ----nzvc
  109d               SHAL.W Rd               SAL.W Rd                2 ----nzvc
  10Bd               SHAL.L ERd              SAL.L ERd               2 ----nzvc
  110d               SHLR.B RdB              SHR.B RdB               2 ----0z0c
  111d               SHLR.W Rd               SHR.W Rd                2 ----0z0c
  113d               SHLR.L ERd              SHR.L ERd               2 ----0z0c
  118d               SHAR.B RdB              SAR.B RdB               2 ----nz0c
  119d               SHAR.W Rd               SAR.W Rd                2 ----nz0c
  11Bd               SHAR.L ERd              SAR.L ERd               2 ----nz0c
  120d               ROTXL.B RdB             RCL.B RdB               2 ----nz0c
  121d               ROTXL.W Rd              RCL.W Rd                2 ----nz0c
  123d               ROTXL.L ERd             RCL.L ERd               2 ----nz0c
  128d               ROTL.B RdB              ROL.B RdB               2 ----nz0c
  129d               ROTL.W Rd               ROL.W Rd                2 ----nz0c
  12Bd               ROTL.L ERd              ROL.L ERd               2 ----nz0c
  130d               ROTXR.B RdB             RCR.B RdB               2 ----nz0c
  131d               ROTXR.W Rd              RCR.W Rd                2 ----nz0c
  133d               ROTXR.L ERd             RCR.L ERd               2 ----nz0c
  138d               ROTR.B RdB              ROR.B RdB               2 ----nz0c
  139d               ROTR.W Rd               ROR.W Rd                2 ----nz0c
  13Bd               ROTR.L ERd              ROR.L ERd               2 ----nz0c
```
## H8/300H Not/Neg/Extend
```
  170d               NOT.B RdB               NOT.B RdB               2 ----nz0-
  171d               NOT.W Rd                NOT.W Rd                2 ----nz0-
  173d               NOT.L Rd                NOT.L ERd               2 ----nz0-
  175d               EXTU.W Rd               UMOV Rd,RdL ;or Ed,EdL? 2 ----0z0-
  177d               EXTU.L ERd              UMOV ERd,Rd             2 ----0z0-
  178d               NEG.B RdB               NEG.B RdB               2 --h-nzvc
  179d               NEG.W Rd                NEG.W Rd                2 --h-nzvc
  17Bd               NEG.L Rd                NEG.L ERd               2 --h-nzvc
  17Dd               EXTS.W Rd               SMOV Rd,RdL ;or Ed,EdL? 2 ----nz0-
  17Fd               EXTS.L ERd              SMOV ERd,Rd             2 ----nz0-
```

## H8/300H Increment/Add and Decrement/Subtract
```
  0A0d               INC.B RdB               INC.B RdB,1             2 ----nzv-
  1A0d               DEC.B RdB               DEC.B RdB,1             2 ----nzv-
  0Asd            *s ADD.L E?Rs,ERd          ADD.L ERd,ERs           2 --h-nzvc
  1Asd            *s SUB.L ERs,ERd           SUB.L ERd,ERs           2 --h-nzvc
  0B0d               ADDS  #1,ERd            INC.S ERd,1             2 --------
  1B0d               SUBS  #1,ERd            DEC.S ERd,1             2 --------
  0B5d               INC.W #1,Rd             INC.W Rd,1              2 ----nzv-
  1B5d               DEC.W #1,Rd             DEC.W Rd,1              2 ----nzv-
  0B7d               INC.L #1,ERd            INC.L ERd,1             2 ----nzv-
  1B7d               DEC.L #1,ERd            DEC.L ERd,1             2 ----nzv-
  0B8d               ADDS  #2,ERd            INC.S ERd,2             2 --------
  1B8d               SUBS  #2,ERd            DEC.S ERd,2             2 --------
  0B9d               ADDS  #4,ERd            INC.S ERd,4             2 --------
  1B9d               SUBS  #4,ERd            DEC.S ERd,4             2 --------
  0BDd               INC.W #2,Rd             INC.W Rd,2              2 ----nzv-
  1BDd               DEC.W #2,Rd             DEC.W Rd,2              2 ----nzv-
  0BFd               INC.L #2,ERd            INC.L ERd,2             2 ----nzv-
  1BFd               DEC.L #2,ERd            DEC.L ERd,2             2 ----nzv-
```

## H8/300H Jump Opcodes and Unsigned Mul/Div
```
  50sd               MULXU.B RsB,Rd          UMUL.B Rd,RsB          14 ----nz--
  51sd               DIVXU.B RsB,Rd          UDIV.B Rd,RsB          14 ----nz--
  52sd               MULXU.W Rs,ERd          UMUL.W ERd,Rs          22 ----nz--
  53sd               DIVXU.W Rs,ERd          UDIV.W ERd,Rs          22 ----nz--
  5470               RTS                     RET                  8,10 --------
  55nn               BSR d:8                 CALL $+/-nn           6,8 --------
  5670               RTE                     RETI                   10 xxxxxxxx
  57n0               TRAPA #n:2              TRAP 0..3 ;[0010h+n*2] 14 1x------
  58c0nnnn           --> Jumps (relative 16bit range)
  59s0               JMP @ERs                JMP  ERs                4 --------
  5Annnnnn           JMP @aa:24              JMP  nnnnnn             6 --------
  5Baa               JMP @@aa:8              JMP  [FFaa]          8,10 --------
  5C00nnnn           BSR d:16                CALL $+/-nnnn        8,10 --------
  5Ds0               JSR @ERs                CALL ERs              6,8 --------
  5Ennnnnn           JSR @aa:24              CALL nnnnnn          8,10 --------
  5Faa               JSR @@aa:8              CALL [FFaa]          8,12 --------
```

## H8/300H Relative Jump Opcodes (8bit/16bit range)
```
  4cnn               Bcc d:8                 Jcc   $+/-nn            4 --------
  58c0nnnn           Bcc d:16                Jcc   $+/-nnnn          6 --------
The 4bit condition code can be:
  0  BRA or BT    JMP        ;always/true
  1  BRN or BF    -          ;never/false
  2  BHI          JA         ;unsigned-above
  3  BLS          JBE        ;unsigned-below-equal
  4  BCC or BHS   JNC or JAE ;unsigned-above-equal
  5  BCS or BLO   JC  or JB  ;unsigned-below
  6  BNE          JNZ or JNE ;not equal/zero
  7  BEQ          JZ  or JE  ;equal/zero
  8  BVC          JNO        ;signed-no overflow
  9  BVS          JO         ;signed-n-overflow
  A  BPL          JNS        ;signed-n-plus
  B  BMI          JS         ;signed-n-minus
  C  BGE          JGE        ;signed-n-greater-eq
  D  BLT          JL         ;signed-n-less
  E  BGT          JG         ;signed-n-greater
  F  BLE          JLE        ;signed-n-less-equal
  ```
  
Destination address should be equal (although, the opcodes are weirdly using byte offsets, hence limiting 8bit range to even 7bit range).
The execution time for condition=false is unknown. 
The time for BRN (always false) is said to be equal to two NOPs (but unknown why one would use that opcode, and if it does refer to the BRN opcode with 8bit and/or 16bit range).

## H8/300H Misc 6xxx
```
  60nd               BSET   RnB,RdB          SET   RdB.RnB           2 --------
  61nd               BNOT   RnB,RdB          NOT   RdB.RnB           2 --------
  62nd               BCLR   RnB,RdB          CLR   RdB.RnB           2 --------
  63nd               BTST   RnB,RdB          TST   RdB.RnB           2 -----z--
  64sd               OR.W   Rs,Rd            OR.W  Rd,Rs             2 ----nz0-
  65sd               XOR.W  Rs,Rd            XOR.W Rd,Rs             2 ----nz0-
  66sd               AND.W  Rs,Rd            AND.W Rd,Rs             2 ----nz0-
  67nd            *i B{I}ST #nn:8,RdB        MOV   RdB.n,{not} C     2 --------
  68md               MOV.B  @ERm,RdB         MOV.B RdB,[ERm]         4 ----nz0-
  68ms            *m MOV.B  RsB,@ERm         MOV.B [ERm],RsB         4 ----nz0-
  69md               MOV.W  @ERm,Rd          MOV.W Rd,[ERm]          4 ----nz0-
  69ms            *m MOV.W  Rs,@ERm          MOV.W [ERm],Rs          4 ----nz0-
  6A0dnnnn           MOV.B  @aa:16,RdB       MOV.B RdB,[aaaa]        6 ----nz0-
  6A2d00nnnnnn       MOV.B  @aa:24,RdB       MOV.B RdB,[aaaaaa]      8 ----nz0-
  6A4dnnnn           MOVFPE @aa:16,RdB       MOV.B RdB,[periph:aaaa] * ----nz0-
  6A8snnnn           MOV.B  RsB,@aa:16       MOV.B [aaaa],RsB        6 ----nz0-
  6AAs00nnnnnn       MOV.B  RsB,@aa:24       MOV.B [aaaaaa],RsB      8 ----nz0-
  6ACsnnnn           MOVTPE RsB,@aa:16       MOV.B [periph:aaaa],RsB * ----nz0-
  6B0dnnnn           MOV.W  @aa:16,Rd        MOV.W Rd,[aaaa]         6 ----nz0-
  6B2d00nnnnnn       MOV.W  @aa:24,Rd        MOV.W Rd,[aaaaaa]       8 ----nz0-
  6B8snnnn           MOV.W  Rs,@aa:16        MOV.W [aaaa],Rs         6 ----nz0-
  6BAs00nnnnnn       MOV.W  Rs,@aa:24        MOV.W [aaaaaa],Rs       8 ----nz0-
  6Cmd               MOV.B  @ERm+,RdB        MOV.B RdB,[ERm+]        6 ----nz0-
  6Cms            *m MOV.B  RsB,@-ERm        MOV.B [ERm-],RsB        6 ----nz0-
  6Dmd               MOV.W  @ERm+,RdB        MOV.W RdB,[ERm+]        6 ----nz0-
  6Dms            *m MOV.W  RsB,@-ERm        MOV.W [ERm-],RsB        6 ----nz0-
  6Emdnnnn           MOV.B  @(d:16,ERm),RdB  MOV.B RdB,[ERm+nnnn]    6 ----nz0-
  6Emsnnnn        *m MOV.B  RsB,@(d:16,ERm)  MOV.B [ERm+nnnn],RsB    6 ----nz0-
  6Fmdnnnn           MOV.W  @(d:16,ERm),Rd   MOV.W Rd,[ERm+nnnn]     6 ----nz0-
  6Fmsnnnn        *m MOV.W  Rs,@(d:16,ERm)   MOV.W [ERm+nnnn],Rs     6 ----nz0-
```
## H8/300H Misc 7xxx
```
  70nd               BSET  #nn:8,RdB         SET   RdB.n             2 --------
  71nd               BNOT  #nn:8,RdB         NOT   RdB.n             2 --------
  72nd               BCLR  #nn:8,RdB         CLR   RdB.n             2 --------
  73nd               BTST  #nn:8,RdB         TST   RdB.n             2 -----z--
  74nd            *i B{I}OR  #nn:8,RdB       OR    C,{not} RdB.n     2 -------c
  75nd            *i B{I}XOR #nn:8,RdB       XOR   C,{not} RdB.n     2 -------c
  76nd            *i B{I}AND #nn:8,RdB       AND   C,{not} RdB.n     2 -------c
  77nd            *i B{I}LD  #nn:8,RdB       MOV   C,{not} RdB.n     2 -------c
  78m06A2d00nnnnnn   MOV.B @(d:24,ERm),RdB   MOV.B RdB,[ERm+nnnnnn] 10 ----nz0-
  78m06AAs00nnnnnn   MOV.B RsB,@(d:24,ERm)   MOV.B [ERm+nnnnnn],RsB 10 ----nz0-
  78m06B2d00nnnnnn   MOV.W @(d:24,ERm),Rd    MOV.W Rd,[ERm+nnnnnn]  10 ----nz0-
  78m06BAs00nnnnnn*? MOV.W Rs,@(d:24,ERm)    MOV.W [ERm+nnnnnn],Rs  10 ----nz0-
  79..               --> Immediate (16bit)
  7A..               --> Immediate (32bit)
  7B5C498F           EEPMOV.B              MOV [ER6+],[ER5+],R4L- 8+4n --------
  7BD4598F           EEPMOV.W              MOV [ER6+],[ER5+],R4-  8+4n --------
  7C..               --> Bit Operations (Memory at ERm)
  7D..               --> Bit Operations (Memory at ERm)
  7E..               --> Bit Operations (Memory at FFaa)
  7F..               --> Bit Operations (Memory at FFaa)
  ```
The EEPMOV opcodes were originally intended to write to an EEPROM, but they can be used as generic memory transfers with number of bytes in R4L or R4. EEPMOV.B is blocking IRQs and NMIs. EEPMOV.W is also blocking IRQs, however, EEPMOV.W gets aborted upon NMI (without resuming the transfer upon return, so software must manually retry if R4=nonzero after executing EEPMOV.W in combination with NMI sources).

## H8/300H Immediate 16bit/32bit
```
  790dnnnn           MOV.W #nnnn:16,Rd       MOV.W Rd,nnnn           4 ----nz0-
  791dnnnn           ADD.W #nnnn:16,Rd       ADD.W Rd,nnnn           4 --h-nzvc
  792dnnnn           CMP.W #nnnn:16,Rd       CMP.W Rd,nnnn           4 --h-nzvc
  793dnnnn           SUB.W #nnnn:16,Rd       SUB.W Rd,nnnn           4 --h-nzvc
  794dnnnn           OR.W  #nnnn:16,Rd       OR.W  Rd,nnnn           4 ----nz0-
  795dnnnn           XOR.W #nnnn:16,Rd       XOR.W Rd,nnnn           4 ----nz0-
  796dnnnn           AND.W #nnnn:16,Rd       AND.W Rd,nnnn           4 ----nz0-
  7A0dnnnnnnnn       MOV.L #nnnnnnnn:32,E?Rd MOV.L E?Rd,nnnnnnnn     6 ----nz0-
  7A1dnnnnnnnn       ADD.L #nnnnnnnn:32,ERd  ADD.L ERd,nnnnnnnn      6 --h-nzvc
  7A2dnnnnnnnn       CMP.L #nnnnnnnn:32,ERd  CMP.L ERd,nnnnnnnn      6 --h-nzvc
  7A3dnnnnnnnn       SUB.L #nnnnnnnn:32,ERd  SUB.L ERd,nnnnnnnn      6 --h-nzvc
  7A4dnnnnnnnn       OR.L  #nnnnnnnn:32,ERd  OR.L  ERd,nnnnnnnn      6 ----nz0-
  7A5dnnnnnnnn       XOR.L #nnnnnnnn:32,ERd  XOR.L ERd,nnnnnnnn      6 ----nz0-
  7A6dnnnnnnnn       AND.L #nnnnnnnn:32,ERd  AND.L ERd,nnnnnnnn      6 ----nz0-
```

## H8/300H Bit Operations
```
  7Cm074n0        *i B{I}OR  #nn:8,@ERm      OR    C,{not} [ERm].n   6 -------c
  7Cm075n0        *i B{I}XOR #nn:8,@ERm      XOR   C,{not} [ERm].n   6 -------c
  7Cm076n0        *i B{I}AND #nn:8,@ERm      AND   C,{not} [ERm].n   6 -------c
  7Cm077n0        *i B{I}LD  #nn:8,@ERm      MOV   C,{not} [ERm].n   6 -------c
  7Dm060n0           BSET    RnB,@ERm        SET   [ERm].RnB         8 --------
  7Dm061n0           BNOT    RnB,@ERm        NOT   [ERm].RnB         8 --------
  7Dm062n0           BCLR    RnB,@ERm        CLR   [ERm].RnB         8 --------
  7Dm063n0           BTST    RnB,@ERm        TST   [ERm].RnB         8 -----z--
  7Dm067n0        *i B{I}ST  #nn:8,@ERm      MOV   [ERm].n,{not} C   8 --------
  7Dm070n0           BSET    #nn:8,@ERm      SET   [ERm].n           8 --------
  7Dm071n0           BNOT    #nn:8,@ERm      NOT   [ERm].n           8 --------
  7Dm072n0           BCLR    #nn:8,@ERm      CLR   [ERm].n           8 --------
  7Dm073n0           BTST    #nn:8,@ERm      TST   [ERm].n           8 -----z--
  7Eaa74n0        *i B{I}OR  #nn:8,@aa:8     OR    C,{not} [FFaa].n  6 -------c
  7Eaa75n0        *i B{I}XOR #nn:8,@aa:8     XOR   C,{not} [FFaa].n  6 -------c
  7Eaa76n0        *i B{I}AND #nn:8,@aa:8     AND   C,{not} [FFaa].n  6 -------c
  7Eaa77n0        *i B{I}LD  #nn:8,@aa:8     MOV   C,{not} [FFaa].n  6 -------c
  7Faa60n0           BSET    RnB,@aa:8       SET   [FFaa].RnB        8 --------
  7Faa61n0           BNOT    RnB,@aa:8       NOT   [FFaa].RnB        8 --------
  7Faa62n0           BCLR    RnB,@aa:8       CLR   [FFaa].RnB        8 --------
  7Faa63n0           BTST    RnB,@aa:8       TST   [FFaa].RnB        8 -----z--
  7Faa67n0        *i B{I}ST  #nn:8,@aa:8     MOV   [FFaa].n,{not} C  8 --------
  7Faa70n0           BSET    #nn:8,@aa:8     SET   [FFaa].n          8 --------
  7Faa71n0           BNOT    #nn:8,@aa:8     NOT   [FFaa].n          8 --------
  7Faa72n0           BCLR    #nn:8,@aa:8     CLR   [FFaa].n          8 --------
  7Faa73n0           BTST    #nn:8,@aa:8     TST   [FFaa].n          8 -----z--
```
Nintendo uses undocumented opcode 7Eaa73n0 instead of official 7Faa73n0. 
Unknown if both are working. 
Unknown if all other opcodes in 7EaaXXn0 range do also act like 7FaaXXn0, and perhaps also 7Cm0XXn0 like 7Dm0XXn0 (nintendo uses the offical 7D/7F for SET/NOT/CLR, so weirdness may apply for TST only).

## H8/300H Encoding Notes
```
  *i   optional inverted source operand (when setting bit3 in the "n" digit)
  *s   must have bit3 set in "s" digit
  *m   must have bit3 set in "m" digit
  *?   must have bit3 set-or-not-set (has conflicting info in official specs)
  E?Rs meant to be ERs (although official specs omit the E in some cases)
  E?Rd meant to be ERd (although official specs omit the E in some cases)
  xxxS meant to be Silent, no flags affected (although specs say Sign Extend)
  xxxX meant to mean Carry, or meant to mean nothing specific in other cases
```

## H8/300H Pseudo Opcodes

The official "PUSH/POP.W/L Rn" opcodes are normal MOV.W/L opcodes with ER7 (SP) and post-increment or pre-decrement.
```
  6DFn               PUSH.W Rn    ;MOV.W [ER7-],Rn
  6D7n               POP.W  Rn    ;MOV.W Rn,[ER7+]
  01006DFn           PUSH.L ERn   ;MOV.L [ER7-],ERn
  01006D7n           POP.L  ERn   ;MOV.L ERn,[ER7+]
```
Although not officially defined, one could also implement `PUSH/POP.W CCR`.
There are no `PUSH/POP.B` opcodes (because that would misalign the stack).

## H8/300H N/A
```
  ---N/A---          MOV.L @aa:8,ERd         MOV.L ERd,[FFaa]        - ----nz0-
  ---N/A---          MOV.L ERs,@aa:8         MOV.L [FFaa],ERs        - ----nz0-
  ---N/A---          MOV.W @aa:8,Rd          MOV.W Rd,[FFaa]         - ----nz0-
  ---N/A---          MOV.W Rs,@aa:8          MOV.W [FFaa],Rs         - ----nz0-
  ---N/A---          SUB.B #nn:8,RdB         SUB.B RdB,nn            - --h-nzvc
```


