# Strings from SP-808ex firmware, cleaned.

Interesting observation. The SP-808 service manual says this about flash memory:

> If the flash memory (IC9 of the main board) becomes failure
> either in terms of software or hardware, the following message
> appears on screen:

```
<< EMERGENCY >>
SYSTEM is BROKEN !
Please consult quali -
fied Roland Service.
```
Those string do not exist in the dumped firmware!


```
00003 TTS25ESYS
00018 RolandEC
2cd22 [[Section Address:

Startup Animation / Logo?

58aba "&*.26:>BFJNRVZ^bfjnrvz
58bad  "&(*.0268:>@BFHJNPRVXZ^`bfhjnprvxz~
58ca1  "$&(*,.02468:<>@BDFHJLNPRTVXZ\^`bdfhjlnprtvxz|~
58d95  "#$&()*,.0234689:<>@BCDFHIJLNPRSTVXYZ\^`bcdfhijlnprstvxyz|~
58e89  "#$%&()*,-.02345689:<=>@BCDEFHIJLMNPRSTUVXYZ\]^`bcdefhijlmnprstuvxyz|}~
58f7d  !"#$%&()*+,-.012345689:;<=>@ABCDEFHIJKLMNPQRSTUVXYZ[\]^`abcdefhijklmnpqrstuvxyz{|}~
59071  !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxxyz{|}~
59169  !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvvwwxxyyzz{{||}}~~
59261  !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnnooppqqrrssttuuvvwwxxyyzz{{||}}~~
59354   !"#$%&'(()*+,-./001234567889:;<=>?@@ABCDEFGHHIJKLMNOPPQRSTUVWXXYZ[\]^_``abcdefghijjkkllmmnnooppqqrrssttuuvvwwxxyyzz{{||}}~~
59444   !"#$%&'(()*+,-./001234567889:;<=>?@@ABCDEFGHHIJKLMNOPPQRSTUVWXXYYZZ[[\\]]^^__``aabbccddeeffgghhiijjkkllmmnnooppqqrrssttuuvvwwxxyyzz{{||}}~~
59534   !"#$%&'(()*+,-./001234567889:;<=>?@@ABCDEFFGGHHIIJJKKLLMMNNOOPPQQRRSSTTUUVVWWXXYYZZ[[\\]]^^__``aabbccddeeffgghhiijjkkllmmnnooppqqrrssttuuvvwwxxyyzz{{||}}~~
59624   !"#$%&'(()*+,-./00123445566778899::;;<<==>>??@@AABBCCDDEEFFGGHHIIJJKKLLMMNNOOPPQQRRSSTTUUVVWWXXYYZZ[[\\]]^^__``aabbccddeeffgghhiijjkkllmmnnooppqqrrssttuuvvwwxxyyzz{{||}}~~
59714   !""##$$%%&&''(())**++,,--..//00112233445566778899::;;<<==>>??@@AABBCCDDEEFFGGHHIIJJKKLLMMNNOOPPQQRRSSTTUUVVWWXXYYZZ[[\\]]^^__``aabbccddeeffgghhiijjkkllmmnnooppqqrrssttuuvvwwxxyyzz{{||}}~~
59813   !!""##$$%%&&''(())**++,,--..//00112233445566778899::;;<<==>>??@@AABBCCDDEEFFGGHHIIJJKKLLMMNNOOPPQQRRSSTTUUVVWWXXYYZZ[[\\]]^^__``aabbccddeeffgghhiijjkkllmmnnooppqqrrssttuuvvwwxxyyzz{{||}}~~
59913   !!""##$$%%&&''(())**++,,--..//00112233445566778899::;;<<==>>??@@AABBCCDDEEFFGGHHIIJJKKLLMMNNOOPPQQRRSSTTUUVVWWXXYYZZ[[\\]]^^__``aabbccddeeffgghhiijjkkllmmnnooppqqrrssttuuvvwwxxyyzz{{||}}~~
59a4c 333333?
59a65 vSCSI Check...
59a74 SCSI:Disabled
59a82 ID  ********
59a90  EXT.ID 
59a99 INTERNAL
59aa2 VSNGLISTVS2
59aae VSNG0000VS2
61f52  !#$&()+,-./123456789;<=?ABCEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~
61ffa SYSPATCH00
62078 DL:Digi?  
620f4 DL:Tape!  
62172 DL:3hSPACE
621f0 DL:Analog+
62268 DL:Hi-Pass
6235a DL:RSS Alt
623d8 DL:Snd OnS
624ca DL:Dub-Box
625bc IS:HiCancl
6263a IS:Low-Phs
626b8 CC:VoCancl
6273a CH:HifiCho
627ae CH:CE1+Dly
62826 CH:CE1/Vib
6289e CH:CE3/+-E
62916 CH:SBF-325
6298c CH:SDD/3+4
629f6 CH:RSSrund
62a73 PT:ST Dtun
62ae7 PT:OctDown
62b5b PT:TriadCd
62bd0 FL:HardJet
62c46 FL:Hi-Band
62cbc FL:SBF-#3 
62d32 FL:Step/Bm
62da8 FL:Measure
62e1e WA:TrigWah
62e94 WA:Cyclic 
62f0a WA:Envelop
62ffc PH:4Stage 
63074 PH:See-Saw
630ec PH:2LFO'80
63164 PH:Step/Bm
631dc LF:RingMd1
632ce LF:RingMd2
633c0 LF:Clipin'
63446 LF:DrmDist
634cc LF:Bullhrn
635be LF:RateBit
6363c LF:BadTune
636aa LF:Vinyl33
6372a LF:SP disk
637aa RV:MidRoom
6384c RV:LrgHall
638ee RV:Cathdrl
63990 RV:SoftAmb
63a32 RV:RoomAmb
63ad4 RV:LrgClub
63b76 RV:ClubFlr
63c18 RV:LngCave
63cba RV:Garage 
63d5c RV:Plate  
63dfe RV:Gated  
63ea0 RV:Revers 
63f42 RV:Duckin'
63fe4 DN:DanceEQ
64076 DN:Loudnes
64108 DN:Hard+GT
6419a DN:TotalCp
6422c DN:Limiter
642be DN:Enhance
64350 SY:Beam #1
64442 SY:Beam #2
64534 SY:StepBs1
64626 SY:StepBs2
64718 SY:StepTk1
6480a SY:StepTk2
648fc SY:StepTk3
649ee SY:StepTk4
64ae0 SY:StepTk5
64bd2 SY:StepTk6
64cc4 SY:70Step1
64db6 SY:70Step2
64ea8 SY:80Step1
64f9a SY:80Step2
6508c SY:StpWind
6517e SL:Slicer1
651fa SL:Slicer2
65276 SL:+Delay 
652f2 01>Iso&Fil
65370 02>Ct.Canc
653f2 03>CompEtc
65484 04)Rev&Gat
65526 05>TapeEch
655a4 06>ezDelay
65620 07>DlayRSS
6569e 08>AnlgD&C
65716 09>DigiCho
6578a 10>4btun C
657f4 11>Flng325
6586a 12>FlngBx2
658df 13>Pit-Sft
65954 14>80sPhas
659cc 15>2xA.Wah
65a42 16>2xDist 
65ac8 17>Records
65b48 18>Radio  
65bb6 19>Lo-Fi  
65c34 20>AnlgSyn
65d26 21>GuitarM
65dd0 22>VocalM 
65e82 23>VoTrans
65f12 24>MicSim 
65fb4 25>Vocoder
66052 GT:RockLed
660fc GT:LA Lead
661a6 GT:MetalLd
66250 GT:MetalJt
662fa GT:CleanRm
663a4 GT:DlyRiff
6644e GT:BluesDv
664f8 GT:Liverpo
665a2 GT:Country
6664c VO:BullHn2
666f6 VO:VocalFx
667a8 VO:JazzVo.
6685a VO:RockVo.
6690c VO:Narrat.
669be VO:BigChrs
66a70 VO:Club DJ
66b22 VO:AMRadio
66bd4 GT:D.Clean
66c86 GT:Acoustc
66d38 BS:D.Bass 
66dea VT:M to Fm
66e7a VT:Fm to M
66f0a VT:MaleDuo
66f9a VT:Fem.Duo
6702a VT:Robot  
670ba VC:Mono   
67158 VC:Stereo 
67526 Line
675c2 MS:10
67664 MS:10
67706 MS:Mini
677a8 MS:Mini
6784a MS:St.Mic 
678ec MS:Ambienc
6798e SY:V-Synth
67a80 SY:StepV#1
67b72 SY:StepV#2
67c64 SY:Marimba
67d56 SY:EthnoLd
67e48 SY:Bubble 
67f3a RV:LngCave
67fdc RV:Garage 
6807e RV:Plate  
68120 RV:Gated  
681c2 RV:Revers 
68264 RV:Duckin'
68306 DN:DanceEQ
68398 DN:Loudnes
6842a DN:Hard+GT
684bc DN:TotalCp
6854e DN:Limiter
685e0 DN:Enhance
68672 SY:Beam #1
68764 SY:Beam #2
68856 SY:StepBs1
68948 SY:StepBs2
68a3a SY:StepTk1
68b2c SY:StepTk2
68c1e SY:StepTk3
68d10 SY:StepTk4
68e02 SY:StepTk5
68ef4 SY:StepTk6
68fe6 SY:70Step1
690d8 SY:70Step2
691ca SY:80Step1
692bc SY:80Step2
693ae SY:StpWind
694a0 SL:Slicer1
6951c SL:Slicer2
69598 SL:+Delay 
69614 01>Iso&Fil
69692 02>Ct.Canc
69714 03>CompEtc
697a6 04)Rev&Gat
69848 05>TapeEch
698c6 06>ezDelay
69942 07>DlayRSS
699c0 08>AnlgD&C
69a38 09>DigiCho
69aac 10>4btun C
69b16 11>Flng325
69b8c 12>FlngBx2
69c01 13>Pit-Sft
69c76 14>80sPhas
69cee 15>2xA.Wah
69d64 16>2xDist 
69dea 17>Records
69e6a 18>Radio  
69ed8 19>Lo-Fi  
69f56 20>AnlgSyn
6d6f7 Iso
6d6fc Isolator    
6d70f Fil
6d714 Filter      
6d727 PLBs
6d72c Low Booster 
6d744 Tape Echo   
6d75c EZ Delay    
6d774 NoiseSuppres
6d78c Comp/Limiter
6d79f Enh
6d7a4 Enhancer    
6d7bc 3-Band EQ   
6d7cf Rev
6d7d4 Reverb+Gate 
6d7ec Vintage Flng
6d804 4ButtonChors
6d81c '80s Phaser 
6d82f FFlg
6d834 St. Flanger 
6d847 Cho
6d84c St. Chorus  
6d864 Delay RSS   
6d877 pWah
6d87c St. Auto Wah
6d894 Distortion  
6d8ac PitchShifter
6d8bf Dsk
6d8c4 V-Phono Disk
6d8d7 Rad
6d8dc V-Radio     
6d8f4 Bit/RateDown
6d90c Synth Common
6d91f LFO
6d924 Synth LFO   
6d937 VCO
6d93c Vtl.VCO+Ring
6d954 Virtual VCF 
6d96c Virtual VCA 
6d984 Simple Delay
6d99c Chorus/Flang
6d9b4 CenterCancel
6d9cc Analog Delay
6d9e4 AnalogChorus
6d9f7 VoT
6d9fc VoiceTrans. 
6da14 Simple Delay
6da2c Stereo Link 
6da3f MSA
6da44 MicSim. Ch.A
6da57 MSB
6da5c MicSim. Ch.B
6da6f Lmt
6da74 Limiter    
6da87 Psf
6da8c PitchShifter
6daa4 Chorus      
6dab7 LC/S
6dabc Comp/Sustain
6dad4 Auto Wah    
6dae7 ZDrv
6daec Driver      
6daff JSim
6db04 AmpSimulator
6db1c Chorus/Flang
6db2f Voc
6db34 Vocoder(10) 
6db47 Dly
6db4c Stereo Delay
6db7e Level High
6db89 Lev Hi
6db9c Level Mid 
6dba7 LevMid
6dbba Level Low 
6dbc5 Lev Lo
6dbd8 AntiPhs Md
6dbe3 AP-MSw
6dbf5 6     Level
6dc01 AP-MLv
6dc14 AntiPhs Lo
6dc1f AP-LSw
6dc31 6     Level
6dc3d AP-LLv
6dc50 Type      
6dc5b Type  
6dc6e Slope(oct)
6dc79 Slope 
6dc8a 5<CutOffFreq
6dc97 CutOff
6dcaa Resonance 
6dcb5 Reso  
6dcc8 Gain      
6dcd3 Gain  
6dce6 BoostLevel
6dcf1 Boost 
6dd04 Mode      
6dd0f Mode  
6dd22 RepeatRate
6dd2d Rate  
6dd40 Intensity 
6dd4b Intens
6dd5e Bass      
6dd69 Bass  
6dd7c Treble    
6dd87 Treble
6dd9a Head S Pan
6dda5 HS Pan
6ddb7 Head M Pan
6ddc3 HM Pan
6ddd5 Head L Pan
6dde1 HL Pan
6ddf3 Tape Dist.
6ddff Dist  
6de12 W/F Rate  
6de1d WFRate
6de30 W/F Depth 
6de3b WFDept
6de4e FX Level  
6de59 FX Lev
6de6c Dry Level 
6de77 DryLev
6de8a Mode      
6de95 Mode  
6dea8 Time      
6deb3 Time  
6dec6 L-R Shift 
6ded1 Shift 
6dee2 L-R Order 
6deef Order 
6df02 Feedback  
6df0d FeedBk
6df20 Tempo Sync
6df2b TempoS
6df3c 5TLoDampFreq
6df49 LoDFrq
6df5c LoDampGain
6df67 LoD-Gn
6df7a HiDampFreq
6df85 HiDFrq
6df98 HiDampGain
6dfa3 HiD-Gn
6dfb6 FX Level  
6dfc1 FX Lev
6dfd4 Dry Level 
6dfdf DryLev
6dff2 Threshold 
6dffd Thresh
6e010 Release   
6e01b Releas
6e02e Threshold 
6e039 Thresh
6e04c Attack    
6e057 Attack
6e06a Release   
6e075 Releas
6e088 Ratio     
6e093 Ratio 
6e0a6 Out Level 
6e0b1 OutLev
6e0c4 Sens      
6e0cf Sens  
6e0e2 Frequency 
6e0ed Freq  
6e100 Mix Level 
6e10b MixLev
6e11e Out Level 
6e129 OutLev
6e13c Low Type  
6e147 LoType
6e15a Low Gain  
6e165 LoGain
6e178 Low Freq  
6e183 LoFreq
6e196 Low Q     
6e1a1 Lo Q  
6e1b4 Mid Gain  
6e1bf MidGin
6e1d2 Mid Freq  
6e1dd MidFrq
6e1f0 Mid Q     
6e1fb Mid Q 
6e20e High Type 
6e219 HiType
6e22c High Gain 
6e237 HiGain
6e24a High Freq 
6e255 HiFreq
6e268 High Q    
6e273 High Q
6e286 Out Level 
6e291 OutLev
6e2a4 Room Size 
6e2af RmSize
6e2c2 Rev Time  
6e2cd Time  
6e2e0 Pre Delay 
6e2eb PreDly
6e2fe Diffusion 
6e327 Densty
6e33a Early Ref.
6e345 ElyRef
6e358 LoDampFreq
6e363 LoDFrq
6e376 LoDampGain
6e381 LoD-Gn
6e394 HiDampFreq
6e39f HiDFrq
6e3b2 HiDampGain
6e3bd HiD-Gn
6e3d0 HiCutFreq 
6e3db HiCut 
6e3ee GT Switch 
6e3f9 GT Sw 
6e40b 6GT Mode   
6e417 GT Md 
6e42a GT Thresh 
6e435 GT Thr
6e448 GT Attack 
6e453 GT Atk
6e466 GT Hold   
6e471 GT Hld
6e484 GT Release
6e48f GT Rel
6e4a2 FX Level  
6e4ad FX Lev
6e4c0 Dry Level 
6e4cb DryLev
6e4de FX Mode   
6e4e9 Mode  
6e4fc Rate      
6e507 Rate  
6e518 6JDepth     
6e525 Depth 
6e538 Manual    
6e543 Manual
6e556 Feedback  
6e561 FeedBk
6e574 CH-R Modu.
6e57f R Modu
6e590 Phase CH-L
6e59d PhaseL
6e5ae       CH-R
6e5bb PhaseR
6e5cc Tempo Sync
6e5d9 TempoS
6e5ec Input     
6e5f7 Input 
6e60a ModeButton
6e615 Mode  
6e626 Dry/FX Bal
6e633 Dry/FX
6e646 Shift Mode
6e651 Mode  
6e662 CenterFreq
6e66f CntFrq
6e682 Resonance 
6e68d Reso  
6e6a0 LFO1 Rate 
6e6ab Rate 1
6e6bc     Depth
6e6c9 Depth1
6e6dc      Phase
6e6e7 Phase1
6e6f8     T.Sync
6e705 Sync 1
6e718 LFO2 Rate 
6e723 Rate 2
6e736      Depth
6e741 Depth2
6e754      Phase
6e75f Phase2
6e770 Model Type
6e77d Type  
6e790 Manual    
6e79b Manual
6e7ae Depth     
6e7b9 Depth 
6e7cc Rate      
6e7d7 Rate  
6e7e8 Resonance 
6e7f5 Reso  
6e808 LFO Phase 
6e813 LFOPhs
6e826 Cross FB  
6e831 X-FB  
6e844 Cross Mix 
6e84f X-Mix 
6e862 Tempo Sync
6e86d TempoS
6e880 Rate      
6e88b Rate  
6e89e Depth     
6e8a9 Depth 
6e8bc LFO Phase 
6e8c7 Phase 
6e8da Bass      
6e8e5 Bass  
6e8f8 Treble    
6e903 Treble
6e916 Cross Mix 
6e921 X-Mix 
6e934 FX Level  
6e93f FX Lev
6e952 Dry Level 
6e95d DryLev
6e970 Time      
6e97b Time  
6e98e Feedback  
6e999 FeedBk
6e9ac RSS Shift 
6e9b7 RssSft
6e9ca L-R Shift 
6e9d5 LR Sft
6e9e8 Tempo Sync
6e9f3 TempoS
6ea04 LoDampFreq
6ea11 LoDFrq
6ea24 LoDampGain
6ea2f LoD-Gn
6ea42 HiDampFreq
6ea4d HiDFrq
6ea60 HiDampGain
6ea6b HiD-Gn
6ea7e FX Level  
6ea89 FX Lev
6ea9c     Mono.D
6eaa7 Mono D
6eaba     RSS D 
6eac5 RSS D 
6ead8 Dry Level 
6eae3 DryLev
6eaf6 FilterType
6eb01 Type  
6eb14 Frequency 
6eb1f Freq  
6eb32 Peak      
6eb3d Peak  
6eb50 Trig.Sens 
6eb5b Sens  
6eb6e Polarity  
6eb79 Polar 
6eb8c LFO Rate  
6eb97 Rate  
6eba8     Depth 
6ebb5 LFODep
6ebc8     Phase 
6ebd3 LFOPhs
6ebe6     T.Sync
6ebf1 LFOSyn
6ec04 Gain      
6ec0f Gain  
6ec22 Tone      
6ec2d Tone  
6ec40 Out Level 
6ec4b OutLev
6ec5e StereoLink
6ec69 LinkSw
6ec7b 6Grade     
6ec87 Grade 
6ec9a L ch Pitch
6eca5 PitchL
6ecb8      Fine 
6ecc3 Fine L
6ecd6 R ch Pitch
6ece1 PitchR
6ecf4      Fine 
6ecff Fine R
6ed12 FX Level  
6ed1d FX Lev
6ed30 Dry Level 
6ed3b DryLev
6ed4e Input     
6ed59 Input 
6ed6c SignalDist
6ed77 Dist  
6ed8a Freq.Range
6ed95 Range 
6eda8 Disk Type 
6edb3 Disk  
6edc6 NoiseTotal
6edd1 NzTotl
6ede4    Scratch
6edef ScrtNz
6ee02    Dust   
6ee0d DustNz
6ee20    Hiss   
6ee2b HissNz
6ee3e W/F Total 
6ee49 WFTotl
6ee5c    Wow    
6ee67 Wow   
6ee7a    Flutter
6ee85 Fluttr
6ee98    Random 
6eea3 Random
6eeb6 FX Level  
6eec1 FX Lev
6eed4 Dry Level 
6eedf DryLev
6eef2 Tuning    
6eefd Tune  
6ef10 NoiseLevel
6ef1b Noise 
6ef2e Freq.Range
6ef39 Range 
6ef4c FX Level  
6ef57 FX Lev
6ef6a Dry Level 
6ef75 DryLev
6ef88 PreFilter 
6ef93 PreFlt
6efa5 SampleRate
6efb1 SampRt
6efc4 Down to...
6efcf Bit   
6efe2 PostFilter
6efed PstFlt
6efff FX Level  
6f00b FX Lev
6f01e Dry Level 
6f029 DryLev
6f03c Trigger In
6f047 TrigIn
6f059 Velocity  
6f065 Velo. 
6f078 NoteNumber
6f083 Note  
6f095 Portamento
6f0a1 PortSW
6f0b3 Porta Time
6f0bf PortTm
6f0d2 Bend Range
6f0dd Bend  
6f0f0 Mod.  
6f0fb Md Oc1
6f10e Mod.  
6f119 Md Oc2
6f12c Mod.  
6f137 Md TVF
6f14a Mod.  
6f155 Md TVA
6f168 Fade Time 
6f173 Fade T
6f186 Rate      
6f191 Rate  
6f1a2 Waveform  
6f1af WaveFm
6f1c2 Tempo Sync
6f1cd TempoS
6f1e0 Oc1 Pt. KF
6f1eb KF Oc1
6f1fd 6Oc1 Wave  
6f209 Wave 1
6f21c Oc1 PulseW
6f227 PWid.1
6f23a Oc1 PWM   
6f245 PWM  1
6f258 Oc1 Coarse
6f263 Cors 1
6f276 Oc1 Fine  
6f281 Fine 1
6f294 Oc1 Vib   
6f29f Vib  1
6f2b2 Oc1 X-Mod 
6f2bd X-Mod1
6f2d0 Oc2 Pt. KF
6f2db KF Oc2
6f2ed 6Oc2 Wave  
6f2f9 Wave 2
6f30c Oc2 PulseW
6f317 PWid.2
6f32a Oc2 PWM   
6f335 PWM  2
6f348 Oc2 Coarse
6f353 Cors 2
6f366 Oc2 Fine  
6f371 Fine 2
6f384 Oc2 Vib   
6f38f Vib  2
6f3a2 RingM Src1
6f3ad Ring 1
6f3be Src2
6f3cb Ring 2
6f3dc Osc1  
6f3e9 Oc1 In
6f3fc Osc2  
6f407 Oc2 In
6f41a Noise 
6f425 NoizIn
6f438 ExtIn 
6f443 Ext In
6f456 RingM 
6f461 RingIn
6f474 FilterType
6f47f Type  
6f492 Slope(oct)
6f49d Slope 
6f4ae CutOff Frq
6f4bb CutOff
6f4ce Resonance 
6f4d9 Reso  
6f4ec Env.Depth 
6f4f7 Env.Dp
6f50a    Attack 
6f515 Attack
6f528    Decay  
6f533 Decay 
6f546    Sustain
6f551 Sustin
6f564    Release
6f56f Releas
6f582 LFO Depth 
6f58d LFO Dp
6f5a0 ExtLev.Flw
6f5ab ExtFlw
6f5be CutOff KF 
6f5c9 COF KF
6f5db 6VeloSens  
6f5e7 V.Sens
6f5fa Initi.Gain
6f605 InitGn
6f618 Env.Depth 
6f623 Env.Dp
6f636    Attack 
6f641 Attack
6f654    Decay  
6f65f Decay 
6f672    Sustain
6f67d Sustin
6f690    Release
6f69b Releas
6f6ae LFO Depth 
6f6b9 LFO Dp
6f6cc ExtLev.Flw
6f6d7 ExtFlw
6f6ea VeloSens  
6f6f5 V.Sens
6f708 Mode      
6f713 Mode  
6f724 4(Time      
6f731 Time  
6f744 Feedback  
6f74f FeedBk
6f762 Tempo Sync
6f76d TempoS
6f77e 5TFX Level  
6f78b FX Lev
6f79e Dry Level 
6f7a9 DryLev
6f7bc Mode      
6f7c7 Mode  
6f7d8 Mod LR Phs
6f7e5 ModPhs
6f7f6 Rate      
6f803 Rate  
6f814 6xDepth     
6f821 Depth 
6f834 Manual    
6f83f Manual
6f852 Resonance 
6f85d Reso  
6f870 Tempo Sync
6f87b TempoS
6f88e Position  
6f899 Posit.
6f8ab vLo-F Limit
6f8b7 Lo Lim
6f8ca Hi-F Limit
6f8d5 Hi Lim
6f8e8 RepeatRate
6f8f3 Rate  
6f906 Intensity 
6f911 Intens
6f924 Echo Level
6f92f Echo  
6f942 Dry Level 
6f94d DryLev
6f960 CE Mode   
6f96b Mode  
6f97c Intensity 
6f989 Intens
6f99c Depth(VIB)
6f9a7 Depth 
6f9ba Rate (VIB)
6f9c5 Rate  
6f9d8 Direct Out
6f9e3 Direct
6f9f5 OutputMode
6fa01 OutMod
6fa12 Robot Sw. 
6fa1f Robot 
6fa31 Pitch     
6fa3d Pitch 
6fa50 Formant   
6fa5b Form. 
6fa6e Dry/FX Bal
6fa79 Dry/FX
6fa8c Mode      
6fa97 Mode  
6faa8 Time      
6fab5 Time  
6fac8 Feedback  
6fad3 FeedBk
6fae6 Tempo Sync
6faf1 TempoS
6fb02 FX Level  
6fb0f FX Lev
6fb22 Dry Level 
6fb2d DryLev
6fb40 A/B Link  
6fb4b Link  
6fb5d MicConv.  
6fb69 MicCnv
6fb7b   TypeIn  
6fb87 MicIn 
6fb9a       Out 
6fba5 MicOut
6fbb8   Phase   
6fbc3 OutPhs
6fbd4 Bass Cut  
6fbe1 BasCut
6fbf3   Freq    
6fbff BC Frq
6fc12 Distance  
6fc1d Dista.
6fc2f   Prox.Fx.
6fc3b ProxFx
6fc4e   Time    
6fc59 Time  
6fc6c Limiter   
6fc77 Limit.
6fc89   Freq    
6fc95 LM Frq
6fca8   Level   
6fcb3 LM Lev
6fcc6   Thresh  
6fcd1 LM Thr
6fce4   Attack  
6fcef LM Atk
6fd02   Release 
6fd0d LM Rel
6fd20 Mode      
6fd2b Mode .
6fd3e LMT Level 
6fd49 LmtLev
6fd5c     Thresh
6fd67 LmtThr
6fd7a     Releas
6fd85 LmtRel
6fd98 DES Sens  
6fda3 DesSns
6fdb6     Freq  
6fdc1 DesFrq
6fdd4 Pitch     
6fddf Pitch 
6fdf2 Fine      
6fdfd Fine  
6fe10 FX Level  
6fe1b FX Lev
6fe2e DryLevel  
6fe39 DryLev
6fe4c CH-R Modu.
6fe57 R Modu
6fe68 Rate      
6fe75 Rate  
6fe88 Depth     
6fe93 Depth 
6fea6 FX Level  
6feb1 FX Lev
6fec4 DryLevel  
6fecf DryLev
6fee2 Attack    
6feed Attack
6ff00 Level     
6ff0b Level 
6ff1e Sustain   
6ff29 Sustin
6ff3c Tone      
6ff47 Tone  
6ff5a FilterType
6ff65 Type  
6ff78 Frequency 
6ff83 Freq  
6ff96 Peak      
6ffa1 Peak  
6ffb4 Trig.Sens 
6ffbf Sens  
6ffd2 Polarity  
6ffdd Polar 
6fff0 LFO Rate  
6fffb Rate  
7000c     Depth 
70019 LFODep
7002c     T.Sync
70037 LFOSyn
7004a Type      
70055 Type  
70068 Gain      
70073 Gain  
70086 Level     
70091 Level 
700a4 Tone      
700af Tone  
700c2 High Gain 
700cd Hi Gin
700e0 Mid Gain  
700eb MidGin
700fe Low Gain  
70109 Lo Gin
7011c Type      
70127 Type  
70138 Mode      
70145 Mode  
70156 Mod LR Phs
70163 ModPhs
70174 Rate      
70181 Rate  
70192 Depth     
7019f Depth 
701b2 Manual    
701bd Manual
701d0 Resonance 
701db Reso  
701ee Tempo Sync
701f9 TempoS
7020c Envelope  
70217 Env.  
70228 Pan       
70235 Pan   
70246 Hold      
70253 Hold  
70265 6Mic Sens. 
70271 MicSns
70284 SynthInLev
7028f SynLev
702a2 V.Char. 1 
702ad Char 1
702c0 V.Char. 2 
702cb Char 2
702de V.Char. 3 
702e9 Char 3
702fc V.Char. 4 
70307 Char 4
7031a V.Char. 5 
70325 Char 5
70338 V.Char. 6 
70343 Char 6
70356 V.Char. 7 
70361 Char 7
70374 V.Char. 8 
7037f Char 8
70392 V.Char. 9 
7039d Char 9
703b0 V.Char.10 
703bb Char10
703ce MicMix Lev
703d9 MM Lev
703ec MicMix Pan
703f7 MM Pan
70409 MicMix HPF
70415 MM HPF
70428 Time      
70433 Time  
70446 L-R Shift 
70451 Shift 
70462 2jFeedback  
7046f FeedBk
70482 Tempo Sync
7048d TempoS
7049e 5TFX Level  
704ab FX Lev
704be Dry Level 
704c9 DryLev
704dc  THRU
704e2  MAX 
704e8  MIN 
704ee 1:  S
704f4 2:  M
704fa 3:  L
70500 4:S+M
70506 5:M+L
7050c 6:S+L
70512 7:ALL
70518 MONO
7051d   ST
70522  ALT
70527 ST-1
7052c ST-2
70531 L>>R
70536 L<<R
7053b 1.5:1
70541   2:1
70547   4:1
7054d 100:1
70553 SHELV
70559  PEAK
7055f GATE
70564 DUCK
70579 NORM
7057e  INV
70583 HI-B
705a4 4STG
705a9 8STG
705ae DOWN
705b3   UP
705d5  OSC1
705db  OSC2
705e1 NOISE
705e7 EXTIN
705ed CHORS
705f3   VIB
705f9 FLANG
705ff DR-20
70605 SML.D
7060b HED.D
70611 MIN.C
70617  FLAT
7061d VOC.D
70623 LRG.D
70629 SML.C
7062f LRG.C
70635 VNT.C
70643 METAL
70649    DS
7064f    OD
70655 SMALL
7065b BLTIN
70661 2STAK
70667 3STAK
7066d SHARP
70673  SOFT
70679  LONG
70cb7 PQRST
70cea PAD 1@s
70cf2 PAD 2Ax
70cfa PAD 3B}
70d02 PAD 4C
70d0a PAD 5;s
70d12 PAD 6<x
70d1a PAD 7=}
70d22 PAD 8>
70d2a PAD 96s
70d32 PAD107
70d3a PAD118
70d42 PAD129
70d4a PAD131
70d52 PAD142
70d5a PAD153
70d62 PAD164
70d6a ST  A
70d72 ST  B
70d7a ST  C
70d82 ST  D
70d8a HOLD ?l
70d92 PAD S:l
70d9a CLIP 5l
70da2 BANK 0l
70daa LOC 1
70db2 LOC 2
70dba LOC 3
70dc2 LOC 4
70dca CLEAR
70dd2 PLAYL
70dda TO-> 
70de2 SCRUB
70dea SONG 
70df2 SYSTE
70dfa SAMPL
70e02 TRIM 
70e0a LEVEL
70e12 UNDO 
70e1a REGIO
70e22 MARK 
70e2a FX  D
70e32 FX IN
70e3a MUTE 
70e42 CRS L
70e4a CRS D!^
70e52 CRS R b
70e5a ROW  .l
70e62 S.MOD/l INFO 
70e72 EXIT 
70e78 Y CRS U
70e82 ENTER
70e88 P.TRG*l
70e92 PITCH+q
70e9a EFFEC
70ea2 ON/OF-l
70eaa SHIFT
70eb2 V.PCH#c
70eba TOP
70ec2 REW
70eca FF
70ed2 STOP
70eda PLAY
70ee2 REC
70eea FX  A
70ef2 FX  B
70efa FX  C
70f1e NGOKTEST Completed. Insert Zip Disk.Error(Compare). Error(Busy).    Error(No Drive).Error(Option).  Now Testing...  P.OutPhoneSmpFsMute MASAUXMIXOFF4432p
70fd6 LockedUnlock*FREQ*N.C.OFF ON  (M)
70ffc OP-1
71001 -----
7100f InSel
71015 OPT 
7101a COAX
7101f  -> 
71028 LCD Contrast
71039 Switch
71040 Fader
7104a D-Beam
71051 MIDI
71056 Zip(ATAPI)
71061 Analog I/O
7106c Initialize
71077 SCSI
7107c Digital I/O
71088 Encoder
71090 Foot Sw.
71099 Device
710a0 Scanning
710a9 SP808-OP1..
710b5 TEST OK.
710be Push [o] Key.
710cc MENU
710d1 Push [>] Key.
710df Contrast =
710ea Push [<<][>>] Key.
710fd SWITCH
71104 [-----]
7110c Remain:
71114 FADER
71127 D-BEAM
71136 SoftTHRU Mode
71144 [UNDO]:LoopTEST
71154 ANALOG I/O
7115f P.Out:    SmpFs:  k
71173 Phone:    Mute :
71184 INITIALIZE
7118f [UNDO]:Initialize
711a1 [REC] :Exit
711ad SCSI(ID=6)
711b8 DIGITAL I/O
711c4 IN:---- (STAT:******)
711da SmpFs:??k CT:** CP:*
711ef ENCODER
711f7 Value:  
71200 FOOT SW
71208 Status
7120f [    ]
71216 DEVICE(RAM)
71222 [o]:ESP
7122a CPU RAM:
71233 DRAM   :
7123c Loop TEST: ??
7124a Initializing..
71259 KEEP POWER ON!
71268 SAVE SYSPROG
71275 IMAGE
7127b FILE 
71281 Ver.
71286   Saving... 
71293 Insert DISK.
712a0  Completed. 
716a9 ~~~~~}}}|||{{{zzyyxxwwvvuttsrrqpponmllkjihgfedcba`_^]\[ZYXVUTSRPONMKJIHFEDBA?>=;:9764310.-+*('%$"!
71736 !"$%'(*+-.0134679:;=>?ABDEFHIJKMNOPRSTUVXYZ[\]^_`abcdefghijkllmnoppqrrsttuvvwwxxyyzz{{{|||}}}~~~~~
717e1 }{ywusqomkigeca_][YWUSQOMKIGECA?=;97531/-+)'%#!
71831  #%')+-/03579;=?@CEGIKMOPSUWY[]_`cegikmopsuwy{}
71aa0 TS25ESYSTEMPRMxxBAK
71ab6 ----
71abb SELF
71ac0 ZIP 
71ac5 HD  
71aca CD  
71acf -SZHC
71af0 IOMEGA  
71af9 iomega  
71b90 Roland  
71b99 TS25E      
71ba5 FAT12   
71bae FAT16   
71bb7 SP-808TS25E
71bc3 SYSTEM__VS2
71bcf SONGLISTVS2
71bdb SP808   PRG
71be7 SAMPLE__VS2
71bf3 PADBANK_VS2
71bff WAVELISTVS2
71c0b TAKE0000VS2
71c17 EFFECT__VS2
71c23 EFFECT1_VS2
71c83   LPF
71c89   BPF
71c8f   HPF
71c95 NOTCH
71d3a DEVICE(ESP)
71d46 [o]:MENU
71d4f PRAM0 --  PRAM1 --
71d62 IRAM0 --  IRAM1 --
71d75 GRAM  --  ERAM  --
71dc0 Data Invalid!      
71dd4 Waiting SYS-EX...
71de6 Receiving...( / )
71df8 MIDI UPDATE
71e04 Update System?(Y/N)
71e18  Ver  .   ->  .    
71e2c (CheckSum:        )
71e40 Apr 26 2000
71e4c 16:52:37
71e85 TS25ESYS  Saving... 
72424 Sens L(C5)
7242f      R(C6)
7243a V-SynthPatch
72447 TriggerType
72453 Upper/Lower        %
72468 PitchWidth
72473 Beam ID
7247b D BEAM SETUP
724b4 Auto Setup Sens?
72636 Bank is Protected.
72649 COPY
7264e Source
7265c ERASE
72662 Target
72669 RENUMBER
72672 From
7275e Name    [          ]
72773 FootSwAssign
72780 BeamAsgn Upper(L)
72792          Lower(R)
727a4 BANK PARAM
727af TURN BANK PROTECTION
7282e Tempo
72a70 INTERNAL
72a79  EXT.MTC
72a82      OFF
72a8b MIDI CLK
72a94      MTC
72a9d     30
72aa4 29.97N
72aab 29.97D
72ab2     25
72ab9     24
72ac0    OFF
72ac7 MASTER
72ace  SLAVE
730f2 EMPTY
730f8 GUIDE
730fe TOP(
73117 Song Edit Menu
73126 Select Song?
73133 Set Song Param?
73143 Tempo Map?
7314e Paste?
73155 Move?
7315b Insert?
73163 Adjust Timing?
73172 Locator?
7317b Create New Song?
7318c Delete Song?
73199 Song Protection
731a9 Name  [
731b1 Tr.VoiceReserve
731c1 SyncSource
731cc     Out
731d4 MTC Type
731dd   Error Level
731eb   Offset   :  :  :
731fe MMC Mode
73207 FadeSw Track A
73216        Track B
73225        Track C
73234        Track D
73243 Pad To Track
73250 SONG PARAMETER
7325f TURN SONG PROTECTION
73274 ]onDisk
7327c  T-MAP 
73284 T-Sign
7328b Tempo
73291 Tempo ->
7329a LOCATOR
732a2 CREATE NEW SONG
732b6 Name [
732c1 TrackA
732cc Base
738d8 ***-**-**
738e2  ****-**
738eb Track
738f1 In Time  [
738fc Out Time [
7391b PASTE
73921 Paste To
7392a Repeat Times
73937 MOVE
7393c Move To
73944 ERASE
7394a DELETE
73951 INSERT
73958 Insert To
73962 Start
73968 Duration
73971 ADJUST TIMING
7397f Split Event.
7398c Lev.
73996 WaveOffset
739a1 WaveEnd
73ac4 System Edit Menu
73ad5 Set System Param?
73ae7 Set MIDI Param?
73af7 Keep Mst.Fil&Iso?
73b09 Init SystemParam?
73b1b Cleanup Disk?
73b29 Format Disk?
73b36 Copy Fx Only?
73b44 Copy Disk All?
73b53 Load Ext. Sample?
73b65 Load Ext. Song?
73b75 Convert Disk?
73b83 Sample Edit Menu
73b94 Set Sample Param?
73ba6 Divide?
73bae Delete?
73bb6 Create Reversal?
73bc7 Stretch Time?
73bd5 Change Pitch?
73be3 Normalize?
73bee Set Bank Param?
73bfe Copy Bank?
73c09 Erase Bank?
73c15 Renumber?
73c1f Bank Protection
73c2f Can't Execute.
73c3e (Not Expanded)
73c4d Copy is Prohibited.
73cb7  Change?
73cc0  (YES/NO)
73cd0 FX INFO
741f2 StM1:
741f8 StM2:
741fe FX CTRL
74206 Boost:
7420d CutOff:
74215 Reso:
7421b LowVol:
74223 MidVol:
7422b HiVol:
74232 StM Lo:
7423a StM Hi:
74242 CTRL SYS FX
743db FX INFO
743f5 FILTER INFO
74407 ISOLATOR INFO
74472 (Now Invalid)
74480 FX LOCATION
7448c PatchLoc
74495 Mixer...[
746ba Fil&Iso   
746d1 FX SW.
746d8 (b)FILTER
746e2 (b)ISOLATOR
747bc SAVE EFFECTS PATCH
747cf Patch
747d5 New Name
747de KEEP POWER ON!
747ed (b)FILTER/ISOLATOR
74800 Keep current settings,
748ca FILTER
748d1 ISOLATOR
74bc6 Insert
74bcd Destination Disk.
74bdf Not SP-808 Disk.
74bf0 Copy FX Patches.
74c01 Copy FX Canceled.
74c13 Insert Source Disk.
74c27 [EXIT] to Cancel.
74c39 Copy Disk Canceled.
74c4d Last
74c52 Reading..
74c5c Writing..
74c66 This is SP-808 Disk.
74c7b Not Source Disk.
74c8c Not Destination Disk.
74ca2 This is Source Disk.
74cb7 Wrong Disk.
74cc3 (Write Protected.)
74cd6 Wrong Media Size.
75098 Ext.ID
750a2 INTERNAL
750af ALL BANKS
750b9 BANK
750c2 EFFECT__VS2
750ce EFFECT1_VS2
750da Disk is NOT Ready.
750ed Wrong Disk.
750f9 (Write Protected.)
7510c Not SP-808 Disk.
7511d Wrong Sample Rate.
75130 COPY DISK ALL
7513e To Drive
75147 Verify
7514e Verify Error.
7515c [EXIT] to Cancel
7516d From Drive
75178 Source
7517f   Name  [          ]
75194 To Int.
7519c LOAD EXT SAMPLE
751ac No Data Exist!
751bb LOAD EXT SONG
751c9 FromDrive
751d3 Source      SONG
751e4 Name [            ]
751f8 COPY FX ONLY
75205 Source Patch
75212 Patch
75218 DISK CONVERT
75225 Please Insert
75233 SP808 100MB Disk.
75245 SP808EX 250MB Disk.
75259 100MB Disk.
75265 250MB Disk.
75642 Locked!    
7564e Checking...
7565a Digital
75665 D.In Unlock!
75672 Use Analog In?
75681 Wrong Sample Rate!
75694 (Analog In Selected)
756ca A/D JIG TEST
75f62 SP-808 0100
75f6e VSNG0000VS2
75f91 pVSNGLISTVS2
75f9e SAVE
75fa3 Overwrite ALL
75fb1 SONG
75fb6 EFFECTS Patch
75fc4 SAVE SONG
75fce Overwrite
75fd8 Save As New
75fe4 Now Saving...
75ff2 Can't Make New Song.
76007 Disk Read Error.
76018 Error.
7601f You lose old data of
76034 the SONG and FX Patch.
7604b Preset FX patch used.
76061 Overwrite song only,
76076 SHUTDOWN
7607f Overwrite SONG
7608e You lose
76097 old SONG data.
760a6 To No.
760b1 Name
760b6 SELECT SONG
760c2 SELECT>
760ca (Cur.Song Not Saved)
760df DELETE SONG
760eb DELETE>
760f3 Can't delete
76100 current song.
762c4 SEND/RETURN 
762d6 INS   MASTER
762e8 INS   RECORD
762fa INS  AUX-OUT
7630c MIC/L PRE-EQ
7631e MIC/LIN POST
76330 Tr.A  PRE-EQ
76342 Tr.A POST-EQ
76354 Tr.B  PRE-EQ
76366 Tr.B POST-EQ
76378 Tr.C  PRE-EQ
7638a Tr.C POST-EQ
7639c Tr.D  PRE-EQ
763ae Tr.D POST-EQ
763c0 --(FX PATCH)
763d2 OFF         
76722 A  B  C  D 
7684a MMC TEST
76853 5:REW   6:FF    7:EXIT
7686a 1:STOP  2:PLAY  3:REC
76880 MMC TEST (Recordable)
7693e TEST
76943 BEAM PULSE
7694e BeamPeriod
76959 BeamPulseWidth
76c92 Mark
76c97 Pad 
76c9e  Clip
76ca4 BANK
76ca9 Select One.
76cb5 Overwrite OK?
76cc3 Clip 
76cc9  Pad
76d12 DELETE
76d19 TargetPad
76e14 END POINT
76e1e  AUTO 0.5
76e28  AUTO 1.0
76e32  AUTO 1.5
76e3c  AUTO 2.0
76e46    MANUAL
76eac ****
76eb9 Type
76ebe Source
76ec5     To
76ecc Threshold
76ed6 Trim
76edb DIVIDE
76ee2 Bank  -
76eea Canceled.
76ef4 Hit ENTER to Divide
76f08 Can't Execute.
76f17 (Check End Point.)
76f42 Overwrite?
7705c NORMALIZE
77066 Source
7706d Bank  -
771c8    GATE
771d0 TRIGGER
771d8    DRUM
771e0       OFF
771ea START-END
771f4  LOOP-END
771fe *********
77298 ********
772a4 ***.**
772ab GROUP-
772b2     OFF
772ba PadPlay
772c2 LoopMode
772cb StartPoint
772d6 LoopPoint
772e0 Length(
772e8 End)
772ed BPM BaseNote
7730c Level
77312 MuteGroup
7731c SAMPLE PARAM
77329 Hit ENTER to Set
7733a No Sample
77344 in this Bank.
77442 Source
77449     To
77450 Grade
77456 NewPitch
7745f P.Fine
77466 CHANGE PITCH
77473 Bank  -
7751a CREATE REVERSAL
7752a Source
77531 Bank  -
77570 StartP
77577  LoopP
7757e Length
7775c  16 
77761   8 
77766   4 
7776b   2 
77770   1 
77775 1/2 
7777a 1/4 
7777f 1/8 
77784 1/16
77789 ****
7778e  TEMPO
77795 LENGTH
7779c ------
777a6 ***.*
777ac Can't Execute.
777bb (Out of 50-150%)
777cc Source
777d3     To
777da Ratio
777e0 NewBPM
777e7 Match/w
77800 Type
77805 TIME STRETCH
77812 Bank  -
7781a SAMPLE__VS2
77826 SAMPLE__BAK
77832 SAMPLE__BK2
779c4 STEREO
779cb   MONO
779d2 MANUAL
779d9  LEV.1
779e0  LEV.2
779e7  LEV.3
779ee  LEV.4
779f5  LEV.5
779fc  LEV.6
77a03  LEV.7
77a0a  LEV.8
77a11    PAD
77a1f   OFF
77a25  20ms
77a2b  40ms
77a31  80ms
77a37 160ms
77a3d 320ms
77af2 GATE
77af7 TRIG
77afc DRUM
77b01     OFF
77b09 ON(S-E)
77b11 ON(L-E)
77c3c REMAIN
77c43 Type
77c48 Start/w
77c50 PreTrig
77c58 FxLoc.
77c5f SAMPLING
77c68 Select Pad.
77c74 Overwrite?
77c7f Can't Make
77c8a New Wave.
77c94 Pad Play
77c9d Loop
77ca2 Auto Trim
77cac Auto Divide
77cb8 Remain
77cbf Waiting Signal...
77cd1 Now Sampling...
77ce4 Bank
77ce9 Cenceled.
77cf3 Try Again.
78196 XXLR
7819b METER
781a1 [CH]
781a6 A B C D
781b1 [AUX]
781ba INFORMATION
781c6 Disp
781cb Contrast
781d4 Remain
781df  MEAS 
781e6 BEAT
781eb TICK
781f0 HOUR
781f5 MIN.
781fa SEC.
781ff FRAME
7837a PASTE
78380 INSERT
78387 ERASE
7838d DELETE
78394 PLAY LIST
78652 (ON 
78657  BPM  
78661 (OFF)
78667 BPM TUNE
78670 BPM RATE
78679 VARI PITCH
78684 BPM SET
7926a Select Track.
79278 Audio REC
79283 Track
79289 Event REC
79293 (Realtime)
7935a SEQ TEST 3
7936d Offset
79374 PreLoad
79405 (New Song  01
79810  SEQ TEST 
7981b Track
79821  SEQ TEST 2 
7984e DISC SLEEP..
7987c EFFECT__VS2
79888 Now Checking..
79a1c Cnt1M
79a22 Cnt2M
79a28 [PAD]
79a2e (MTC)
79a34 MEAS
79a5c  OFF
79be2 Hit Pad
79bea to REC start.
79bf8 REMAIN
79bff Start/w
79c07 Quantize
79c10 AutoPunch
79c1a Loc.
79c27 AUDIO
79c30 Type
79c35 Memory Full.
79c42 No Memory for UNDO.
79c56 Continue?
79c60 Disk Full.
79c6b Memory & Disk Full.
79d4e 44.1
79d53   32
79d58 QUICK
79d5e FULL 
7a10a KEEP POWER ON!
7a119 Wrong Disk.
7a125 (Write Protected.)
7a138 Format     k:[     ]
7a14d ...Not SP-808 Disk.
7a161 Format Now?
7a16d Eject,(Not Saved)
7a17f Eject Canceled.
7a18f Song is Protected.
7a1a2 Can't Save! EJECT?
7a1b5 SYSTEM UPDATE
7a1c3 Update System?(Y/N)
7a1d7 Ver  .   ->  .
7a1e6 SYS PARAM INITIALIZE
7a1fb Initialize
7a206 System Parameters?
7a219 (Y/N)
7a436  1STEP
7a43d SINGLE
7a444 REPEAT
7a44b   MEAS
7a452 SngPLY
7a626 Paral.
7a62d Series
7a634  SONG
7a63a EXTN
7a63f LINK
7a648 STEP MOD
7a651 Trig
7a657 EndStep
7a660 Value
7a667 CopyFrom
7a670 Step
7a679 Gate.T
7a683 [Enter].
7a7b0 SMPL
7a7b5 MEAS
7a92e  MULTI
7a935 SINGLE
7a93c   AUTO
7a97c STEP REC
7a985 REMAIN
7a98c Step
7a991 Usage Info.
7a9a1 Back
7a9a6 PHRASE TIE REST Step
7a9bb Select Track
7a9c8 NewPhrase
7a9d2 Creating Phrase...
7a9e5 No Disk Space
7a9f3 for New Phrase.
7ab88  OFF
7ab8d ONCE
7ab92   ON
7ab97  INT   (REC)
7aba4  INT(ALWAYS)
7abb1 MIDI   (REC)
7abbe MIDI(ALWAYS)
7abcb DP-2
7abd0  GPI
7abd5  PLAY/STOP
7abe0     DAMPER
7abeb SAMPL TRIG
7abf6  FX ON/OFF
7ac01  PUNCH I/O
7ac0c   MEASURE
7ac16 TIME CODE
7ac20 JUMP
7ac25 NULL
7ac2a MIC/LINE
7ac33 DIGITAL1
7ac3c DIGITAL2
7ac45 SOURCE
7ac4c  TRACK
7acaa  10sec
7acb5 msec
7acba InputSource
7acc6 Mon(PrePunch)
7acd4 Metro.
7acdb Metro.Level
7ace7 PreviewLength
7acf5 ScrubLength
7ad01 SongSave Confirm
7ad12 FSW Func
7ad1b FSW Type
7ad24 TimeDisp.
7ad2e ShiftLock
7ad38 KnobControl
7ad44 D.CopyProtect
7ad52 SYSTEM COMMON
7ad60 INIT SYS-PARAM
7ad6f Initialize all
7ad7e System Parameters.
7adee    QUICK
7adf7 STANDARD
7aec8 44.1
7aecd   32
7aed2 QUICK
7aed8  FULL
7aee2 CLEANUP DISK
7aeef Type
7aef4 You CANNOT Undo.
7af05 TargetDrive
7af11 SamplingRate
7af1e FormatType
7af29 FORMAT DISK
7af35 Erase ALL data,
7af45 Protected Banks
7af55 Exist.FORMAT SURE?
7b0bc Pads Rx Ch.
7b0c8 RxNote(Pad1)
7b0d5 Pads Tx Ch.
7b0e1 FX Ctrl Ch.
7b0ed Mixer,D-Beam
7b0fa Metronome Ch.
7b108    Accent Note
7b117       Velocity
7b126    Normal Note
7b135 Out/Thru Select
7b145 MIDI
7b2e8 PRE-F
7b2ee PST-F
7b710 REC(orPLAY)
7b71c   PLAY-ONLY
7b728   AUTO
7b72f MANUAL
7b7dc THRU(
7b7e2 LINE)
7b7e8 REC(orPLAY)
7b7f4     AUX
7b7fc PAD CUE
7b804 Track D
7b8b2 TRACK  
7b8ba Level
7b8c6 Balance
7b8ce Merge-L&R
7b8e2 MidQ
7b8f7 FaderCtrl
7b906 PadsLevel
7b910 MIX COMMON
7b91b Master
7b922 Rec Att    dB
7b930 FxLoc.
7b937 FX-Signal
7b941 PreFx Att
7b94e Return
7b955 Send Ch.Mute
7b962 AUX In&Out
7b970 Out Lev
7b97c OutJackMode
7bb7c ARE YOU SURE?
7bb8a Wait a Moment...
7bb9b Now Working...
7bbaa Disk Medium Error.
7bbbd 1abc1ABC2def2DEF3ghi3GHI4jkl4JKL5mno5MNO6pqr6PQR7stu7STU8vwx8VWX9yz#9YZ#0.,!0.,!()?+()?+        
7bea6 (Now OFF 
7beb0  Turn ON)
7bebd (Now ON 
7bec6  Turn OFF)
7c120 [ENTER] to Do.
7c12f Can't Undo
7c13a while Playing.
7c149 Completed.
7c154 Memory Full.
7c161 Disk Full.
7c16c No Disk Space.
7c17b Metronome ON
7c188 Metronome OFF
7c196 Song is Protected.
7c1a9 Save Current Song?
7c1bc (Overwrite Only.)
7c1ce Drive Too Busy.
7c1de Invalid.(Digital In)
7c1f3 Invalid.(MTC Slave)
7c207 No Memory for UNDO.
7c21b Continue?
7c225 MTC Sync.
7c22f master -> SLAVE
7c23f slave -> MASTER
7c24f Pre-Punch Monitor
7c261 track -> SOURCE
7c271 source -> TRACK
7c281 Pad to Track
7c292 OFF.
7c297 PADs are Full.
7c2a6 Use Next Bank?
7c2b5 TEST
7c2e7 ESP TEST
7c2f4  OFF
7c312 0.1s
7c32f 20.2s
7c34d 20.5s
7c36b   1s
7c389   2s
7c3a7   4s
7c3c5   8s
7c3e3  16s
7c68e NARROW
7c695 MEDIUM
7c69c   WIDE
7c6a3 HEIGHT
7c6aa   L<>R
7c866 STOP
7c86b SEND
7c870  OUT
7c875 THRU
bffe3 TTS25ESYS
bfff8 RolandEC
```
