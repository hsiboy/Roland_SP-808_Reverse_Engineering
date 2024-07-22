import sys
import os
import glob

MODEL_CONFIG = {
    'sp808': {
        'RmanfID': 0x41,
        'MdevID': 0x10,
        'RmodID': 0x2B,
        'Mdataset1': 0x12
    },
    'a6': {
        'RmanfID': 0x41,
        'MdevID': 0x10,
        'RmodID': 0x7C,
        'Mdataset1': 0x12
    },
    'vs880': {
        'RmanfID': 0x41,
        'MdevID': 0x10,
        'RmodID': 0x7C,
        'Mdataset1': 0x12
    },
    'integra7': {
        'RmanfID': 0x41,
        'MdevID': 0x10,
        'RmodID': 0x64,
        'Mdataset1': 0x12
    }
}

def get_sysex_record_length(file):
    reclen = 0
    bytvar = file.read(1)[0]
    
    if bytvar < 0x80:
        reclen = bytvar
        return reclen
    
    reclen = (bytvar & 0x7F) << 7
    bytvar = file.read(1)[0]
    
    if bytvar > 0x7F:
        print("Unexpected record length (> 0x3FFF)")
        reclen = 0x4000
        return reclen
    
    reclen += bytvar
    return reclen

def compute_checksum(data):
    cksm = 0
    for byte in data:
        cksm += byte
    cksm = 128 - (cksm % 128)
    return cksm & 0x7F

def process_file(infil, outfil, RmanfID, MdevID, RmodID, Mdataset1):
    with open(infil, 'rb') as f1, open(outfil, 'ab') as f2:  # 'ab' mode for appending binary data
        print(f"Extracting binary firmware data from {infil} and writing to {outfil} ...")
        print()

        MThd = b"MThd"
        MTrk = b"MTrk"
        
        if f1.read(4) != MThd:
            print(f"Unrecognised marker in header chunk -- should be \"{MThd.decode()}\".")
            aborted(f1)
            return
        
        uintvar = int.from_bytes(f1.read(4), byteorder='big')
        
        if uintvar != 0x00000006:
            print(f"Unexpected data length in header chunk (0x{uintvar:08X}) -- should be 00 00 00 06")
            aborted(f1)
            return
        
        wdvar = int.from_bytes(f1.read(2), byteorder='big')
        
        if wdvar != 0:
            print(f"Unexpected SMF type in header chunk (0x{wdvar:04X}) -- should be 0x0000")
            aborted(f1)
            return
        
        wdvar = int.from_bytes(f1.read(2), byteorder='big')
        
        if wdvar != 0x0001:
            print(f"Unexpected Number of Tracks in header chunk (0x{wdvar:04X}) -- should be 0x0001")
            aborted(f1)
            return
        
        f1.read(2)  # Skip past PPQ
        
        if f1.read(4) != MTrk:
            print(f"Unrecognised marker in track chunk -- should be \"{MTrk.decode()}\".")
            aborted(f1)
            return
        
        filsiz = int.from_bytes(f1.read(4), byteorder='big')
        uintvar = os.path.getsize(infil)
        
        if filsiz != (uintvar - 0x16):
            print(f"Length of MIDI file (0x{uintvar:X}) is inconsistent with track chunk (0x{filsiz:08X}) + 0x16")
            aborted(f1)
            return
        
        while True:
            if f1.tell() == uintvar:
                break
            
            deltaT = f1.read(1)[0]
            
            if deltaT == 0x10:
                event = f1.read(1)[0]
                
                if event != 0xF0:
                    print(f"Unrecognised Sysex Event value (0x{event:02X}) -- was expecting 0xF0")
                    aborted(f1)
                    return
                
                reclen = get_sysex_record_length(f1)
                
                if reclen > 0x3FFF:
                    aborted(f1)
                    return
                
                bytvar = f1.read(1)[0]
                
                if bytvar != RmanfID:
                    print(f"Unrecognised manufacturer ID (0x{bytvar:02X}) -- was expecting 0x{RmanfID:02X}")
                    aborted(f1)
                    return
                
                bytvar = f1.read(1)[0]
                
                if bytvar != MdevID:
                    print(f"Unrecognised Device ID (0x{bytvar:02X}) -- was expecting 0x{MdevID:02X}")
                    aborted(f1)
                    return
                
                bytvar = f1.read(1)[0]
                
                if bytvar != 0:
                    print("Unrecognised sysex event format")
                    aborted(f1)
                    return
                
                bytvar = f1.read(1)[0]
                
                if bytvar != RmodID:
                    print(f"Unrecognised Model ID (0x{bytvar:02X}) -- was expecting 0x{RmodID:02X}")
                    aborted(f1)
                    return
                
                bytvar = f1.read(1)[0]
                
                if bytvar != Mdataset1:
                    print(f"Unrecognised command code -- (0x{bytvar:02X}) was expecting 0x12 (Data Set 1)")
                    aborted(f1)
                    return
                
                cksm = 0
                eventadd = [f1.read(1)[0] for _ in range(3)]
                cksm += sum(eventadd)
                memadd = 0
                
                for _ in range(5):
                    bytvar = f1.read(1)[0]
                    cksm += bytvar
                    memadd = (memadd << 4) + bytvar
                
                datapos = f1.tell()
                f7pos = datapos + (reclen - 0x0D)
                f1.seek(f7pos)
                
                if f1.read(1)[0] != 0xF7:
                    print(f"Unrecognised end-of-packet byte (0x{bytvar:02X}) -- was expecting 0xF7")
                    aborted(f1)
                    return
                
                f1.seek(datapos)
                datalen = reclen - 0x0E
                
                for _ in range(datalen + 1):
                    bytvar = f1.read(1)[0]
                    cksm += bytvar
                
                cksm &= 0x7F
                
                if cksm != 0:
                    print("Non-zero checksum for sysex data.")
                    aborted(f1)
                    return
                
                if eventadd[0] == 0x00:
                    if eventadd[1] != 0 or eventadd[2] != 0:
                        print("Unrecognised sysex event address")
                        aborted(f1)
                        return
                    
                    f1.seek(datapos)
                    
                    if datalen % 8 != 0:
                        print("Firmware packet size is not a multiple of 8")
                        aborted(f1)
                        return
                    
                    f2.seek(memadd)
                    
                    for _ in range(0, datalen, 8):
                        octet = [f1.read(1)[0] for _ in range(7)]
                        maskbyt = f1.read(1)[0]
                        
                        for j in range(7):
                            maskbyt = (maskbyt << 1) & 0xFF
                            bytvar = octet[j] | (maskbyt & 0x80)
                            print(f"Writing byte {bytvar:02X} at file position {f2.tell()}")  # Debugging statement
                            f2.write(bytes([bytvar]))
                
                elif eventadd[0] == 0x01:
                    if eventadd[2] != 0:
                        print("Unrecognised sysex event address3")
                        aborted(f1)
                        return
                    
                    if memadd != 0:
                        print("Unrecognised sysex event format")
                        aborted(f1)
                        return
                    
                    if eventadd[1] == 0x00:
                        f1.seek(datapos)
                        dwvar1 = int.from_bytes(f1.read(3), byteorder='big')
                        memstart = 0
                        
                        for _ in range(5):
                            memstart = (memstart << 4) + f1.read(1)[0]
                        
                        dwvar2 = int.from_bytes(f1.read(3), byteorder='big')
                        memsize = 0
                        
                        for _ in range(5):
                            memsize = (memsize << 4) + f1.read(1)[0]
                        
                        if dwvar1 != 0 or dwvar2 != 0 or memsize == 0:
                            print("Unrecognised sysex memory parameters")
                            aborted(f1)
                            return
                        
                        print(f"Memory start address = 0x{memstart:X}")
                        print(f"Memory size = 0x{memsize:X}")
                    
                    elif eventadd[1] == 0x01:
                        f1.seek(datapos + datalen)
                    
                    elif eventadd[1] == 0x02:
                        f1.seek(datapos)
                        filnum = f1.read(1)[0]
                        totalfiles = f1.read(1)[0]
                        fileflag = f1.read(1)[0]
                        
                        if fileflag == 0x00:
                            print(f"Begin converting file #{filnum + 1} of {totalfiles + 1}")
                        elif fileflag == 0x7F:
                            print(f"Finished converting file #{filnum + 1} of {totalfiles + 1}")
                        else:
                            print("Unrecognised sysex event format")
                            aborted(f1)
                            return
                    
                    elif eventadd[1] == 0x03:
                        f1.seek(datapos)
                        
                        for _ in range(datalen):
                            print(chr(f1.read(1)[0]), end='')
                        
                        print()
                    
                    else:
                        print("Unrecognised sysex event address2")
                        aborted(f1)
                        return
                
                else:
                    print("Unrecognised sysex event address1")
                    aborted(f1)
                    return
                
                f1.seek(f1.tell() + 2)
            
            elif deltaT == 0x00:
                event = f1.read(1)[0]
                
                if event != 0xFF:
                    print(f"Unrecognised Meta Event value (0x{event:02X}) -- was expecting 0xFF")
                    aborted(f1)
                    return
                
                eventtyp = f1.read(1)[0]
                reclen = get_sysex_record_length(f1)
                
                if reclen > 0x3FFF:
                    aborted(f1)
                    return
                
                if eventtyp in [0x03, 0x02]:
                    for _ in range(reclen):
                        print(chr(f1.read(1)[0]), end='')
                    
                    print()
                
                elif eventtyp == 0x51:
                    if reclen != 3:
                        print("Unrecognised UART clock rate.")
                        aborted(f1)
                        return
                    
                    UARTclk = int.from_bytes(f1.read(3), byteorder='big')
                    print(f"UART clock rate = {UARTclk} ticks per second")
                
                elif eventtyp == 0x2F:
                    if reclen == 0:
                        print("End of Track")
                    else:
                        print("Unrecognised Meta Event type.")
                        aborted(f1)
                        return
                
                else:
                    print("Unrecognised Meta Event type.")
                    aborted(f1)
                    return
            
            else:
                print(f"Unrecognised delta_time value (0x{deltaT:02X}) -- was expecting 0x00 or 0x10")
                aborted(f1)
                return
        
        print("Conversion completed.")

def usage():
    print("\nConvert Roland MIDI firmware files to binary format.")
    print("\nUsage: python rolandext.py model=[model name] infil=[\"input filename\"] outfil=[\"output filename\"]")
    print("\nExample: python rolandext.py model=vs880 infil=VS880A-1.mid outfil=VS880A.bin")

def aborted(file):
    filofst = file.tell() - 1
    print(f"Offset = 0x{filofst:X}")
    print("Conversion aborted.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python rolandext.py model=[model name] infil=[\"input filename\"] outfil=[\"output filename\"]")
        sys.exit(1)
    
    model_arg = sys.argv[1]
    infil_arg = sys.argv[2]
    outfil_arg = sys.argv[3]
    
    if not model_arg.startswith("model="):
        print("Model not specified")
        usage()
        sys.exit(1)
    
    if not infil_arg.startswith("infil="):
        print("Input file not specified")
        usage()
        sys.exit(1)
    
    if not outfil_arg.startswith("outfil="):
        print("Output file not specified")
        usage()
        sys.exit(1)
    
    model = model_arg[6:].lower()
    infil = infil_arg[7:]
    outfil = outfil_arg[7:]
    
    if model not in MODEL_CONFIG:
        print(f"Unknown model: {model}")
        usage()
        sys.exit(1)
    
    if not infil or not outfil:
        usage()
        sys.exit(1)
    
    config = MODEL_CONFIG[model]
    
    infiles = glob.glob(infil)
    
    if not infiles:
        print(f"No input files found matching the pattern {infil}")
        sys.exit(1)
    
    for infil in infiles:
        process_file(infil, outfil, config['RmanfID'], config['MdevID'], config['RmodID'], config['Mdataset1'])
    
    print("All files processed successfully.")
