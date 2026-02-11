' This program extracts the firmware binary from Roland's Edirol A6 update
' http://www.users.on.net/~fzabkar/temp/RmA62bin.bas

#include "vbcompat.bi"

Dim infil As String
Dim outfil As String
' Dim f1 As Long
Common Shared f1 As Long
Dim f2 As Long
Dim i As UShort
Dim j As UShort
Dim str4var As String * 4
Dim MThd As Const String = "MThd"
Dim RmanfID As UByte = &H41
' Dim MdevID As UByte = &H10
Dim RmodID As UByte = &H7C
Dim Mdataset1 As UByte = &H12 
Dim bytvar As UByte
Dim wdvar As UShort
Dim dwvar As ULong
Dim uintvar As UInteger
Dim filsiz As UInteger
Dim MTrk As Const String = "MTrk"
Dim UARTclk As ULong
Dim deltaT As UByte
Dim event As UByte
Dim eventtyp As UByte
' Dim reclen As UShort
Common Shared reclen As UShort
Dim filofst As ULong
Dim eventadd( 1 To 3 ) As UByte
Dim memadd As ULong
Dim memstart As ULong
Dim cksm As UByte
Dim datapos As ULong
Dim datalen As UShort
Dim f7pos As ULong
Dim filnum As UByte
Dim totalfiles As UByte
Dim fileflag As UByte
Dim dwvar1 As ULong
Dim dwvar2 As ULong
Dim memsize As ULong
Dim octet( 1 To 7 ) As Ubyte
Dim maskbyt As UByte

' subroutine to calculate length of sysex records -- assumes max length of 0x3FFF (two bytes)

Declare Sub Sreclen()

Sub Sreclen()

	Dim bytvar As UByte

	reclen = 0
	Get #f1,, bytvar

	If bytvar < &H80 Then 
		reclen = bytvar
		Exit Sub
	End If

	reclen = reclen + (bytvar And &H7F) shl 7

	Get #f1,, bytvar

	If bytvar > &H7F Then 
		Print "Unexpected record length (> 0x3FFF)"
		reclen = &H4000
		Exit Sub
	End If

	reclen = reclen + bytvar

End Sub


If Command( 3 ) <> "" Then 
	  Print "Too many arguments"
        Goto usage
End If


infil = Command( 1 )

If Left( infil, 6 ) <> "infil=" Then
        Print "Input file not specified"
        Goto usage
End If


infil = Mid( infil, 7 )

If infil ="" Then Goto usage End If

If Not FileExists( infil ) Then
        Print "File not found: "; infil
        End
End If



outfil = Command( 2 )

If Left( outfil, 7 ) <> "outfil=" Then
        Print "Output file not specified"
        Goto usage
End If


outfil = Mid( outfil, 8 )

If outfil ="" Then Goto usage End If

' If FileExists( outfil ) Then
'        Print "Output file already exists: "; outfil
'        End
' End If


f1 = FreeFile
Open infil For Binary As #f1

f2 = FreeFile
Open outfil For Binary As #f2

Print "Extracting binary firmware data from "; infil; " and writing to "; outfil; " ..."
Print

' Check for MIDI marker "MThd"

Get #f1,, str4var

If str4var <> MThd Then
	Print "Unrecognised marker in header chunk -- should be """; MThd; """."
	Goto aborted
End If


' Check for header length = 00 00 00 06

Get #f1,, uintvar

If uintvar <> &H06000000 Then
	Print "Unexpected data length in header chunk (0x"; Hex( uintvar, 8 ); " -- should be 00 00 00 06"
	Goto aborted
End If


' Check for SMF type = 0x0000

Get #f1,, wdvar 

If wdvar <> 0 Then
	Print "Unexpected SMF type in header chunk (0x"; Hex( wdvar, 4 ); " -- should be 0x0000"
	Goto aborted
End If


' Check for Number of Tracks = 0x0001

Get #f1,, wdvar 

If wdvar <> &H0100 Then
	Print "Unexpected Number of Tracks in header chunk (0x"; Hex( wdvar, 4 ); " -- should be 0x0001"
	Goto aborted
End If


' Skip past PPQ and ignore it

Get #f1,, wdvar 


' Check for Track marker "MTrk"

Get #f1,, str4var

If str4var <> MTrk Then
	Print "Unrecognised marker in track chunk -- should be """; MTrk; """."
	Goto aborted
End If


' Check for correct file size -- big-endian

filsiz = 0

For i = 1 To 4
	Get #f1,, bytvar
	filsiz = (filsiz Shl 8) + bytvar
Next i

uintvar = Lof( f1 )

If filsiz <> ( uintvar - &H16 ) Then
	Print "Length of MIDI file (0x"; Hex( uintvar ); ") is inconsistent with track chunk (0x"; Hex( filsiz, 8 ); ") + 0x16"
	Goto aborted
End If

' Parse <delta_time> <event> records

' 00 FF 03 <len> <firmware model/version/date>
' 00 FF 02 <len> <copyright notice>
' 00 FF 51 <len> <UART clock rate>
' 10 F0 <len> 41 00 2B 12 <01 02 00> 00 00 00 00 00 <00 07 00> <cksm> F7 - start of file 1 of 8
' 10 F0 <len> 41 00 2B 12 <01 02 00> 00 00 00 00 00 <07 07 00> <cksm> F7 - start of file 8 of 8
' 10 F0 <len> 41 00 2B 12 <01 03 00> 00 00 00 00 00 <firmware model/version/date> <cksm> F7

' 10 F0 <len> 41 00 2B 12 <01 00 00> 00 00 00 00 00 ...
'      ... <00 00 01> <00 00 00 00 00> <00 00 01> <0C 00 00 00 00> <cksm> F7 
'                     <-- memstart -->            <---memsize --->
'                       (nibble mode)               (nibble mode)

' 10 F0 <len> 41 00 2B 12 <00 00 01> <5-byte mem addr (nibble mode)> <firmware payload> <cksm> F7
' 10 F0 <len> 41 00 2B 12 <01 01 00> 00 00 00 00 00 <4E> <cksm> F7 - only at end of file8
' 10 F0 <len> 41 00 2B 12 <01 02 00> 00 00 00 00 00 <00 07 7F> <cksm> F7 - end of file 1 of 8
' 10 F0 <len> 41 00 2B 12 <01 02 00> 00 00 00 00 00 <07 07 7F> <cksm> F7 - end of file 8 of 8
' 00 FF 2F 00 - end of track

Do Until EOF( f1 )
 Get #f1,, deltaT

' Expecting delta_time of 0x00 or 0x10

 Select Case As Const deltaT

 Case &H10

' Delta_time = 0x10 (16 UART clock ticks) -- now expecting Roland 0xF0 sysex Event

  Get #f1,, event

  If event <> &HF0 Then 
	Print "Unrecognised Sysex Event value (0x"; Hex( event, 2 ); ") -- was expecting 0xF0"
	Goto aborted
  Else

' Get length of sysex data

	Sreclen

	If reclen > &H3FFF Then Goto aborted End If

' Now expecting Roland's manufacturer ID (0x41)

	Get #f1,, bytvar

	If bytvar <> RmanfID Then
		Print "Unrecognised manufacturer ID (0x"; Hex( bytvar, 2 ); ") -- was expecting 0x"; Hex( RmanfID, 2)
		Goto aborted
	End If

' This model's firmware update format has no Device_ID

' Now expecting default MIDI Device_ID (0x10)

'	Get #f1,, bytvar

'	If bytvar <> MdevID Then
'		Print "Unrecognised Device ID (0x"; Hex( bytvar, 2 ); ") -- was expecting 0x"; Hex( MdevID, 2)
'		Goto aborted
'	End If

' Now expecting 0x00

	Get #f1,, bytvar

	If bytvar <> 0 Then
		Print "Unrecognised sysex event format"
		Goto aborted
	End If

' Now expecting Model ID (0x7C)

	Get #f1,, bytvar

	If bytvar <> RmodID Then
		Print "Unrecognised Model ID (0x"; Hex( bytvar, 2 ); ") -- was expecting 0x"; Hex( RmodID, 2)
		Goto aborted
	End If

' Now expecting "Data Set 1" command ID (0x12)

	Get #f1,, bytvar

	If bytvar <> Mdataset1 Then
		Print "Unrecognised command code -- (0x"; Hex( bytvar, 2 ); ") was expecting 0x12 (Data Set 1)"
		Goto aborted
	End If

' Checksum is computed from this point until 0xF7

	cksm = 0

' Get 3 event address bytes

	For i = 1 To 3
		Get #f1,, eventadd( i )
		cksm = cksm + eventadd( i )
	Next i

' Get 5-byte memory address in nibble mode

	memadd = 0

	For i = 1 To 5
		Get #f1,, bytvar
		cksm = cksm + bytvar
		memadd = (memadd Shl 4) + bytvar
	Next i

' Save current file position

	datapos = Seek( f1 )

' Now check for 0xF7 at end of packet

	f7pos = datapos + (reclen - &H0D)
	Get #f1, f7pos, bytvar

	If bytvar <> &HF7 Then
		Print "Unrecognised end-of-packet byte (0x"; Hex( bytvar, 2 ); ") -- was expecting 0xF7"
		Goto aborted
	End If

' Confirm that 7-bit checksum = 0x00 (from start of address bytes to checksum byte, inclusive)

	Seek f1, datapos
	datalen = reclen - &H0E

	For i = 1 To datalen + 1
		Get #f1,, bytvar
		cksm = cksm + bytvar
	Next i

	cksm = cksm And &H7F
	
	If cksm <> 0 Then
		Print "Non-zero checksum for sysex data."
		Goto aborted
	End If

' Assume this model has 3 sysex event address bytes
' Now parse the address bytes and decode Roland's sysex commands

' eventadd( 1 ) = 0x00 -> data
' eventadd( 1 ) = 0x01 -> metadata

	Select Case As Const eventadd( 1 )

	Case &H00

' Check for firmware binary data
' sysex event address = 00 00 01, otherwise abort

		If (eventadd( 2 ) <> 0) Or (eventadd( 3 ) <> 1) Then
			Print "Unrecognised sysex event address"
			Goto aborted
		End If

' Example showing how 7-bit octet encodes seven 8-bit bytes

'   00 16 5E 0A 4E 53 20 18  -- 7 data bytes + 1 mask byte
'   
'     00/00    16/16    5E/DE    0A/8A    4E/4E    53/53    20/20  -- 7-bit / 8-bit 
'    0000000  0010110  1011110  0001010  1001110  1010011  0100000 -- 7-bit data bytes
'   00000000 00010110 11011110 10001010 01001110 01010011 00100000 -- 8-bit data bytes
'   :        :        :        :        :        :        :
'   : .------'        :        :        :        :        :
'   : : .-------------'        :        :        :        :
'   : : : .--------------------'        :        :        :
'   : : : : .---------------------------'        :        :
'   : : : : : .----------------------------------'        :
'   : : : : : : .-----------------------------------------'
'   : : : : : : :
'   0 0 1 1 0 0 0 -- 7-bit mask byte
'       18

		Seek f1, datapos

' Check for integral number of octets
'  seven 8-bit bytes are encoded as eight 7-bit bytes

		If (datalen Mod 8) <> 0 Then
			Print "Firmware packet size is not a multiple of 8"
			Goto aborted
		End If

' Set file pointer in output file to target memory address

		Seek #f2,  (memadd + 1)

		For i = 1 To datalen Step 8

			For j = 1 To 7
				Get #f1,, octet( j )
			Next j

			Get #f1,, maskbyt

			For j = 1 To 7
				maskbyt = maskbyt Shl 1
				bytvar = octet( j ) Or ( maskbyt And &H80 )
				Put #f2,, bytvar
			Next j

		Next i

	Case &H01

' Check for metadata

		If eventadd( 3 ) <> 0 Then
			Print "Unrecognised sysex event address3"
			Goto aborted
		End If

		If memadd <> 0 Then
			Print "Unrecognised sysex event format"
			Goto aborted
		End If

		Select Case As Const eventadd( 2 )

		Case &H00

' sysex event address = 01 00 00 -- <00 00 01> <-- memstart --> <00 00 01> <---memsize --->

' Specifies memory start address and memory size -- 5-byte (nibble mode)

			Seek f1, datapos

			dwvar1 = 0

			For i = 1 To 3
				Get #f1,, bytvar
				dwvar1 = (dwvar1 Shl 8) + bytvar
			Next i


			memstart = 0

			For i = 1 To 5
				Get #f1,, bytvar
				memstart = (memstart Shl 4) + bytvar
			Next i



			dwvar2 = 0

			For i = 1 To 3
				Get #f1,, bytvar
				dwvar2 = (dwvar2 Shl 8) + bytvar
			Next i


			memsize = 0

			For i = 1 To 5
				Get #f1,, bytvar
				memsize = (memsize Shl 4) + bytvar
			Next i


			If (dwvar1 <> 1) Or (dwvar2 <> 1) Or (memsize = 0) Then
				Print "Unrecognised sysex memory parameters"
				Goto aborted
			End If

			Print "Memory start address = 0x"; Hex( memstart )
			Print "Memory size = 0x"; Hex( memsize )

		Case &H01

' sysex event address = 01 01 00 -- single byte of data at end of last file ???
'  don't know how to handle this, so do nothing

			Seek f1, (datapos + datalen)

		Case &H02

' sysex event address = 01 02 00 -- <current file number - 1> <total files - 1> <start/end of file>

			Seek f1, datapos

			Get #f1,, filnum
			Get #f1,, totalfiles
			Get #f1,, fileflag

			If fileflag = &H00 Then
				Print "Begin ";
			ElseIf fileflag = &H7F Then
				Print "Finished ";
			Else
				Print "Unrecognised sysex event format"
				Goto aborted
			End If

			Print "converting file #"; filnum + 1; " of"; totalfiles + 1

		Case &H03

' sysex event address = 01 03 00 -- firmware model/version/date sysex metadata

			Seek f1, datapos
			
			For i = 1 To datalen
				Get #f1,, bytvar
				Print Chr( bytvar );
			Next i

			Print

		Case Else
			Print "Unrecognised sysex event address2"
			Goto aborted
		End Select

	Case Else
		Print "Unrecognised sysex event address1"
		Goto aborted
	End Select

' skip over the checksum and 0xF7 bytes

	Seek #f1, (Seek( f1 ) + 2)

 End If


 Case &H00

' Delta_time = 0x00 -- now expecting 0xFF Meta Event

  Get #f1,, event

  If event <> &HFF Then 
	Print "Unrecognised Meta Event value (0x"; Hex( event, 2 ); ") -- was expecting 0xFF"
	Goto aborted
  Else
	Get #f1,, eventtyp
	Sreclen
	If reclen > &H3FFF Then Goto aborted End If

	Select Case As Const eventtyp

	Case &H03, &H02

' 0x03 = Firmware model/version/date
' 0x02 = Copyright notice

		For i = 1 To reclen
			Get #f1,, bytvar
			Print Chr( bytvar );
		Next i

		Print

	Case &H51

' 0x51 = UART clock rate (3 bytes)

		If reclen <> 3 Then
			Print "Unrecognised UART clock rate."
			Goto aborted
		Else
			UARTclk = 0

			For i = 1 To 3
				Get #f1,, bytvar
				UARTclk = (UARTclk Shl 8) + bytvar
			Next i

			Print "UART clock rate = "; UARTclk; " ticks per second"
		End If

	Case &H2F

' 0x2F =  End of Track

		If reclen = 0 Then
			Print "End of Track"
		Else
			Print "Unrecognised Meta Event type."
			Goto aborted
		End If

	Case Else
		Print "Unrecognised Meta Event type."
		Goto aborted

 	End Select

  End If

 Case Else
	Print "Unrecognised delta_time value (0x"; Hex( deltaT, 2 ); ") -- was expecting 0x00 or 0x10"
	Goto aborted
 End Select

Loop

Print "Conversion completed."

Close
End


usage:

Print
Print "Convert Roland Edirol A-6 MIDI firmware files to binary format."
Print
Print "Usage:  RMA62BIN infil=[""input filename""] outfil=[""output filename""]"
Print
Print "Example:  RMA62BIN infil=A6#1.mid outfil=A6_all.bin"
Print
Print "To extract firmware from all MIDI files into a single binary file ..."
Print
Print "for %i in (A6#?.mid) do RmA62bin.exe infil=%i outfil=A6_all.bin"

End


aborted:

filofst = Loc( f1 ) - 1
Print "Offset = 0x"; Hex( filofst )
Print "Conversion aborted."
Close
End
