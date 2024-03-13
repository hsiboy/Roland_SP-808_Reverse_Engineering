// Auto-Disassembly script for Roland SP8080 and Edirol A6 ROMs.
//
// This is based on Acamus's Auto Disassembler.
// edited for compatibility with ida 7.x by Professor_jonny
// and ammeded for the Roland/Edirol by hsiboy
//
// vim:foldmethod=syntax foldnestmax=1 sw=2 et smarttab smartindent ft=c
//


#include <idc.idc>
#include <memcpy.idc>

#define H8_ROM_START   0x00000000
#define H8_CODE_OFFSET 0x00010000
#define H8_CODE_LENGTH 0x000C0004

// Set a name for a location if there is not already a manual name set.
#define SafeMakeName(ea, name) if (name) SafeMakeNameEx(ea, name, SN_NOWARN)
#define SafeMakeNameEx(ea, name, opts) if (ea != BADADDR && !HasName(ea)) MakeNameEx(ea, name, opts);
#define HasName(ea) !(Name(ea) == "" || strstr(Name(ea), "off_") == 0 || strstr(Name(ea), "unk_") == 0 || strstr(Name(ea), "sub_") == 0 || strstr(Name(ea), "byte_") == 0 || strstr(Name(ea), "word_") == 0 || strstr(Name(ea), "dword_") == 0)


static MakeNameSequence(ea, name) {
  auto i, fullname;
  for (i = 1; i < 5000; i++) {
    fullname = form("%s_%d", name, i);
    if (LocByName(fullname) == BADADDR) {
      SafeMakeName(ea, fullname);
      return;
    }
  }
}




static H8RegisterNames() {
    // Interrupt controller - 8 bit
  SafeMakeName(0xFEC0, "INTC_ICRA");
  SafeMakeName(0xFEC1, "INTC_ICRB");
  SafeMakeName(0xFEC2, "INTC_ICRC");

  SafeMakeName(0xFEC4, "INTC_IPRA");
  SafeMakeName(0xFEC5, "INTC_IPRB");
  SafeMakeName(0xFEC6, "INTC_IPRC");
  SafeMakeName(0xFEC7, "INTC_IPRD");
  SafeMakeName(0xFEC8, "INTC_IPRE");
  SafeMakeName(0xFEC9, "INTC_IPRF");
  SafeMakeName(0xFECA, "INTC_IPRG");
  SafeMakeName(0xFECB, "INTC_IPRH");
  SafeMakeName(0xFECC, "INTC_IPRI");
  SafeMakeName(0xFECD, "INTC_IPRJ");
  SafeMakeName(0xFECE, "INTC_IPRK");

// Bus controller - 8 bit
  SafeMakeName(0xFED0, "ABWCR");
  SafeMakeName(0xFED1, "ASTCR");
  SafeMakeName(0xFED2, "WCRH");
  SafeMakeName(0xFED3, "WCRL");
  SafeMakeName(0xFED4, "BCRH");
  SafeMakeName(0xFED5, "BCRL");
  SafeMakeName(0xFED6, "MCR");
  SafeMakeName(0xFED7, "DRAMCR");
  SafeMakeName(0xFED8, "RTCNT");
  SafeMakeName(0xFED9, "RTCOR");
  
  SafeMakeName(0xFEE0, "MAR0AH");
  SafeMakeName(0xFEE1, "MAR0AH");
  SafeMakeName(0xFEE2, "MAR0AL");
  SafeMakeName(0xFEE3, "MAR0AL");
  SafeMakeName(0xFEE4, "IOAR0A");
  SafeMakeName(0xFEE5, "IOAR0A");
  SafeMakeName(0xFEE6, "ETCR0A");
  SafeMakeName(0xFEE7, "ETCR0A");
  SafeMakeName(0xFEE8, "MAR0BH");
  SafeMakeName(0xFEE9, "MAR0BH");
  
  SafeMakeName(0xFEEA, "MAR0BL");
  SafeMakeName(0xFEEB, "MAR0BL");
  SafeMakeName(0xFEEC, "IOAR0B");
  SafeMakeName(0xFEED, "IOAR0B");
  SafeMakeName(0xFEEE, "ETCR0B");
  SafeMakeName(0xFEEF, "ETCR0B");
  SafeMakeName(0xFEF0, "MAR1AH");
  SafeMakeName(0xFEF1, "MAR1AH");
  SafeMakeName(0xFEF2, "MAR1AL");
  SafeMakeName(0xFEF3, "MAR1AL");
  SafeMakeName(0xFEF4, "IOAR1A");
  SafeMakeName(0xFEF5, "IOAR1A");
  SafeMakeName(0xFEF6, "ETCR1A");
  SafeMakeName(0xFEF7, "ETCR1A");
  SafeMakeName(0xFEF8, "MAR1BH");
  SafeMakeName(0xFEF9, "MAR1BH");
  SafeMakeName(0xFEFA, "MAR1BL");
  SafeMakeName(0xFEFB, "MAR1BL");
  SafeMakeName(0xFEFC, "IOAR1B");
  SafeMakeName(0xFEFD, "IOAR1B");
  SafeMakeName(0xFEFE, "ETCR1B");
  SafeMakeName(0xFEFF, "ETCR1B");

  SafeMakeName(0xFF00, "DMAWER");
  SafeMakeName(0xFF01, "DMATCR");
  SafeMakeName(0xFF02, "DMACR0A");
  SafeMakeName(0xFF03, "DMACR0B");
  SafeMakeName(0xFF04, "DMACR1A");
  SafeMakeName(0xFF05, "DMACR1B");
  SafeMakeName(0xFF06, "DMABCRH");
  SafeMakeName(0xFF07, "DMABCRL");

  SafeMakeName(0xFF2C, "ISCRH");
  SafeMakeName(0xFF2D, "ISCRL");
  SafeMakeName(0xFF2E, "IER");
  SafeMakeName(0xFF2F, "ISR");

  SafeMakeName(0xFF30, "DTCER");
  SafeMakeName(0xFF31, "DTCER");
  SafeMakeName(0xFF32, "DTCER");
  SafeMakeName(0xFF33, "DTCER");
  SafeMakeName(0xFF34, "DTCER");
  SafeMakeName(0xFF35, "DTCER");

  SafeMakeName(0xFF38, "SBYCR");
  SafeMakeName(0xFF39, "SYSCR");
  SafeMakeName(0xFF3A, "SCKCR");
  SafeMakeName(0xFF3B, "MDCR");
  SafeMakeName(0xFF3C, "MSTPCRH");
  SafeMakeName(0xFF3D, "MSTPCRL");

  SafeMakeName(0xFF46, "PCR");
  SafeMakeName(0xFF47, "PMR");
  SafeMakeName(0xFF48, "NDERH");
  SafeMakeName(0xFF49, "NDERL");
  SafeMakeName(0xFF4A, "PODRH");
  SafeMakeName(0xFF4B, "PODRL");
  SafeMakeName(0xFF4C, "NDRH");
  SafeMakeName(0xFF4D, "NDRL");
  SafeMakeName(0xFEB0, "P1DDR");
  SafeMakeName(0xFEB1, "P2DDR");
  SafeMakeName(0xFF3C, "MSTPCR");
  SafeMakeName(0xFFB0,"TCR0");
  SafeMakeName(0xFFB2, "TCSR0");
  SafeMakeName(0xFFB4, "TCORA0");

  SafeMakeName(0xFF78, "SMR0");
  SafeMakeName(0xFF79, "BRR0");
  SafeMakeName(0xFF7A, "SCR0");
  SafeMakeName(0xFF7B, "TDR0");
  SafeMakeName(0xFF7C, "SSR0");
  SafeMakeName(0xFF7D, "RDR0");
  SafeMakeName(0xFF7E, "SCMR0");
  SafeMakeName(0xFF80, "SMR1");
  SafeMakeName(0xFF81, "BRR1");
  SafeMakeName(0xFF82, "SCR1");
  SafeMakeName(0xFF83, "TDR1");
  SafeMakeName(0xFF84, "SSR1");
  SafeMakeName(0xFF85, "RDR1");
  SafeMakeName(0xFF86, "SCMR1");
  SafeMakeName(0xFF88, "SMR2");
  SafeMakeName(0xFF89, "BRR2");
  SafeMakeName(0xFF8A, "SCR2");
  SafeMakeName(0xFF8B, "TDR2");
  SafeMakeName(0xFF8C, "SSR2");
  SafeMakeName(0xFF8D, "RDR2");
  SafeMakeName(0xFF3C, "MSTPCR");

}

static ByteRegister(ea, name, comment) {
  MakeByte(ea);
  if (!HasName(ea))
    MakeNameEx(ea, name, SN_NOLIST);
  if (comment != "")
    MakeComm(ea, comment);
  return ea;
}

static WordRegister(ea, name, comment) {
  MakeWord(ea);
  if (!HasName(ea))
    MakeNameEx(ea, name, SN_NOLIST);
  if (comment != "")
    MakeComm(ea, comment);
  return ea;
}

static LongRegister(ea, name, comment) {
  MakeDword(ea);
  if (!HasName(ea))
    MakeNameEx(ea, name, SN_NOLIST);
  if (comment != "")
    MakeComm(ea, comment);
  return ea;
}

static ReservedSpaceArray(start, end) {
  MakeByte(start);
  MakeArray(start, end - start + 1);
  SetArrayFormat(start, AP_ALLOWDUPS, 0, -1);
  MakeComm(start, "Reserved");
  return start;
}

static RegisterArray(ea, count) {
  MakeArray(ea, count);
  SetArrayFormat(ea, AP_ALLOWDUPS, count, -1);
}

static AddVTEntry(ea, name, funcname) {
  auto j;
  j = Dword(ea);
  SafeMakeNameEx(ea, "e" + name, SN_NOLIST);
  SafeMakeName(j, funcname);
  MakeFunction(j, BADADDR);
}

/* 
  
  H8S/2600 Exception Vector Table (Advanced Mode)

Exception Source	Vector  Address
Power-on reset	    0	    H'0000 to H'0003
Manual reset	    1	    H'0004 to H'0007
Reserved for system	2	    H'0008 to H'000B
    -:-	            3	    H'000C to H'000F
    -:-	            4   	H'0010 to H'0013
Trace	            5	    H'0014 to H'0017
Reserved for system	6	    H'0018 to H'001B
External intrpt NMI	7	    H'001C to H'001F
Trap instruction	8	    H'0020 to H'0023
    -:-	            9	    H'0024 to H'0027
    -:-	            10	    H'0028 to H'002B
    -:-	            11	    H'002C to H'002F
Reserved for system 12	    H'0030 to H'0033
    -:-	            13	    H'0034 to H'0037
    -:-	            14	    H'0038 to H'003B
    -:-	            15	    H'003C to H'003F
External interrupt		
IRQ0	            16	    H'0040 to H'0043
IRQ1	            17	    H'0044 to H'0047
IRQ2	            18	    H'0048 to H'004B
IRQ3	            19	    H'004C to H'004F
IRQ4	            20	    H'0050 to H'0053
IRQ5	            21	    H'0054 to H'0057
IRQ6	            22	    H'0058 to H'005B
IRQ7	            23	    H'005C to H'005F
Internal interrupt2	24	    H'0060 to H'0063
    -:-	            ↓	            ↓
    -:-	            91	    H'016C to H'016F
  */

static Fixup_VT(segoffset, romstart) {
  auto i, j, errcode;

  // fixup all vector table entries
  for (i = segoffset; i < (segoffset + romstart); i = i + 4) {
    MakeDword(i);
    OpOff(i, 0, 0);
    // These are stack pointers, not code
    if (i == 0x04 || i == 0x0C)
      continue;
    j = Dword(i);
    MakeCode(j);
    AutoMark(j, AU_PROC);
  }

  // Define known VT entries
  AddVTEntry(0x00000000, "v_power_on_reset", "init");
  AddVTEntry(0x00000004, "v_manual_reset", "init");

  AddVTEntry(0x00000010, "TRAP0", "trap");
  AddVTEntry(0x00000012, "TRAP1", "trap");
  AddVTEntry(0x00000014, "TRAP2", "trap");
  AddVTEntry(0x00000016, "TRAP3", "trap");
  AddVTEntry(0x00000040, "IRQ0", "IRQ");
  AddVTEntry(0x00000044, "IRQ0", "IRQ");
  AddVTEntry(0x00000048, "IRQ0", "IRQ");
  AddVTEntry(0x0000004C, "IRQ0", "IRQ");
  AddVTEntry(0x00000050, "IRQ0", "IRQ");
  AddVTEntry(0x00000054, "IRQ0", "IRQ");
  AddVTEntry(0x00000058, "IRQ0", "IRQ");
  AddVTEntry(0x0000005C, "IRQ0", "IRQ");

}



static FixupJumps(void) {
  auto ea, end, indexa, indexj, xref_from, xref_to;

  ea = 0;
  end = SegEnd(ea);
  Message("Fixing jmp from %x to %x... ", ea, end);

  for (ea; ea <= end; ea = NextAddr(ea)) {
    if (ea == BADADDR) {
      // Message("No more hits\n");
      break;
    }

    // Check for "mova"
    if (GetMnem(ea) == "mova") {
      // Message("mova @ %x\n", ea);
      if (Word(GetOperandValue(ea, 0)) == 0xFFFF)
        indexa = GetOperandValue(ea, 0);
      else
        indexa = NextHead(ea, end) + GetOperandValue(ea, 0);
      //Message("mova initial @ %x\n", indexa);

      while (Word(indexa) == 0xFFFF) {
        MakeWord(indexa);
        indexa = indexa + 2;
      }
      //Message("mova points to @ %x\n", indexa);
      do {
        ea = NextAddr(ea);
        if (GetMnem(ea) == "jmp") {
          xref_from = ea;
          //Message("jmp @ %x\n", xref_from);
          break;
        }

      } while (ea != BADADDR);

      indexj = indexa;
      while (isUnknown(GetFlags(indexj))) {
        MakeWord(indexj);
        xref_to = indexa + Word(indexj);
        MakeCode(xref_to);
        AddCodeXref(xref_from, xref_to, fl_JN);
        //Message("Adding jump from %x to %x\n", xref_from, xref_to);
        MakeComm(indexj, "jsr " + NameEx(indexj, xref_to));
        indexj = indexj + 2;
        ea = indexj;
      }
    }
  }
  Message("Done\n");
}

static Fix_Missing_Code(ea, end, is_byte_check) {
  if (ea == BADADDR || end == BADADDR) {
    Message("nothing selected\n");
    return;
  }
  Message("Fixing missing code from %x to %x... ", ea, end);

  for (ea; ea <= end; ea = NextAddr(ea)) {
    if (ea == BADADDR)
      break;

    if (isUnknown(GetFlags(ea)) && (is_byte_check || Byte(ea) == 0x2F || Byte(ea) == 0x4F)) {
      AddEntryPoint(ea, ea, "", 1);
      //MakeCode(ea);
    }
  }
  Message("Done\n");
}

  auto ea, end, i, mutname;

  ea = 0;
  end = SegEnd(ea);
  Message("Searching for MUT table %x to %x... ", ea, end);

  for (ea; ea <= end && ea != BADADDR; ea = NextAddr(ea)) {
    // Check for "mov.w"
    if (GetMnem(ea) == "mov.w") {
      //Message("Found mov.w at 0x%x\n", ea);
      if ((GetOperandValue(ea, 0) == 0xBF || Word(NextHead(NextHead(ea, end) + GetOperandValue(ea, 0), end)) == 0xBF) && GetMnem(ea + 6) == "shll2") {
        if (Word(NextHead(NextHead(ea, end) + GetOperandValue(ea, 0), end)) == 0xBF)
          ea = Dword(NextAddr(NextAddr(ea + 8) + GetOperandValue(ea + 8, 0)));
        else
          ea = GetOperandValue(ea + 8, 0);
        //Message("Found at 0x%x... ", ea);
        break;
      }
    }
  }

  if (ea == end || ea == BADADDR) {
    Warning("MUT table not found");
    return;
  }

  i = 0;
  for (ea; ea <= end; ea = ea + 4) {
    if (ea == BADADDR || end == BADADDR) {
      Message("No more matches...\n");
      return;
    }
    if (Dword(ea) == 0xFFFFFFFF)
      break;
    MakeDword(ea);
    mutname = form("808_%02X", i++);
    SafeMakeName(Dword(ea), mutname);
  }

  // Common MUT requests
  LabelMutVar("MUT_04", "TimingAdv", "Timing Advance Interpolated");
  LabelMutVar("MUT_06", "TimingAdv", "Timing Advance Scaled");
  LabelMutVar("MUT_06", "TimingAdv", "Timing Advance");
  LabelMutVar("MUT_07", "CoolantTemp", "Coolant Temp");
  LabelMutVar("MUT_0C", "LTFTLo", "Fuel Trim Low (LTFT)");
  LabelMutVar("MUT_0D", "LTFTMid", "Fuel Trim Mid (LTFT)");
  LabelMutVar("MUT_0E", "LTFTHigh", "Fuel Trim High (LTFT)");
  LabelMutVar("MUT_0F", "STFT", "Oxygen Feedback Trim (STFT)");
  LabelMutVar("MUT_10", "CoolantTempScaled", "Coolant Temp Scaled");
  LabelMutVar("MUT_11", "MAFAirTempScaled", "MAF Air Temp Scaled");
  LabelMutVar("MUT_12", "EGRTemp", "EGR Temperature");
  LabelMutVar("MUT_13", "O2Sensor", "Front Oxygen Sensor");
  LabelMutVar("MUT_14", "Battery", "Battery Level");
  LabelMutVar("MUT_15", "Baro", "Barometer");
  LabelMutVar("MUT_16", "ISCSteps", "ISC Steps");
  LabelMutVar("MUT_17", "TPS", "Throttle Position");
  LabelMutVar("MUT_18", "", "Open Loop Bit Array");
  LabelMutVar("MUT_19", "", "Startup Check Bits");
  LabelMutVar("MUT_1A", "AirFlow", "Air Flow - (TPS Idle Adder ?)");
  LabelMutVar("MUT_1A", "", "TPS Idle Adder");
  LabelMutVar("MUT_1C", "Load", "ECULoad");
  LabelMutVar("MUT_1D", "AccelEnrich", "Acceleration Enrichment - (Manifold_Absolute_Pressure_Mean ?)");
  LabelMutVar("MUT_1F", "PrevLoad", "ECU Load Previous");
  LabelMutVar("MUT_20", "RPM_Idle_Scaled", "Engine RPM Idle Scaled");
  LabelMutVar("MUT_21", "RPM", "Engine RPM");
  LabelMutVar("MUT_22", "", "Idle Related Value (unknown)");
  LabelMutVar("MUT_24", "TargetIdleRPM", "Target Idle RPM");
  LabelMutVar("MUT_25", "ISCV_Value", "Idle Stepper Value");
  LabelMutVar("MUT_26", "KnockSum", "Knock Sum");
  LabelMutVar("MUT_27", "OctaneFlag", "Octane Level");
  LabelMutVar("MUT_29", "InjPulseWidth", "Injector Pulse Width (LSB)");
  LabelMutVar("MUT_2A", "InjPulseWidth", "Injector Pulse Width (MSB)");
  LabelMutVar("MUT_2C", "AirVol", "Air Volume");
  LabelMutVar("MUT_2D", "", "Ignition Battery Trim");
  LabelMutVar("MUT_2E", "", "Vehicle speed Frequency");
  LabelMutVar("MUT_2F", "Speed", "Speed");
  LabelMutVar("MUT_30", "Knock", "Knock Voltage");
  LabelMutVar("MUT_31", "VE", "Volumetric Efficiency");
  LabelMutVar("MUT_32", "AFRMAP", "Air/Fuel Ratio (Map reference)");
  LabelMutVar("MUT_33", "Corr_TimingAdv", "Corrected Timing Advance");
  LabelMutVar("MUT_34", "", "MAP Index");
  LabelMutVar("MUT_35", "", "Limp Home Fuel TPS Based");
  LabelMutVar("MUT_36", "", "Active Fault Count");
  LabelMutVar("MUT_37", "Stored Fault Count", "Count");
  LabelMutVar("MUT_38", "MAP", "Boost (MDP)");
  LabelMutVar("MUT_39", "", "Fuel Tank Pressure");
  LabelMutVar("MUT_3A", "UnscaledAirTemp", "Unscaled Air Temperature");
  LabelMutVar("MUT_3B", "", "Masked Map Index");
  LabelMutVar("MUT_3C", "O2Sensor2", "Rear Oxygen Sensor #1");
  LabelMutVar("MUT_3D", "", "Front Oxygen Sensor #2");
  LabelMutVar("MUT_3E", "", "Rear Oxygen Sensor #2");
  LabelMutVar("MUT_3F", "", "Short Term Fuel Feedback Trim O2 Map Index");
  LabelMutVar("MUT_40", "", "Stored Faults Lo");
  LabelMutVar("MUT_41", "", "Stored Faults Hi");
  LabelMutVar("MUT_42", "", "Stored Faults Lo 1");
  LabelMutVar("MUT_43", "", "Stored Faults Hi 1");
  LabelMutVar("MUT_44", "", "Stored Faults Lo 2");
  LabelMutVar("MUT_45", "", "Stored Faults Hi 2");
  LabelMutVar("MUT_47", "", "Active Faults Lo");
  LabelMutVar("MUT_48", "", "Active Faults Hi");
  LabelMutVar("MUT_49", "ACRelaySw", "Air Conditioning Relay");
  LabelMutVar("MUT_4A", "PurgeDuty", "Purge Solenoid Duty Cycle");
  LabelMutVar("MUT_4C", "", "Fuel Trim Low Bank 2");
  LabelMutVar("MUT_4D", "", "Fuel Trim Mid Bank 2");
  LabelMutVar("MUT_4E", "", "Fuel Trim High Bank 2");
  LabelMutVar("MUT_4F", "", "Oxygen Feedback Trim Bank 2");
  LabelMutVar("MUT_50", "", "Long Fuel Trim Bank 1");
  LabelMutVar("MUT_51", "", "Long Fuel Trim Bank 2");
  LabelMutVar("MUT_52", "", "Rear Long Fuel Trim Bank 1");
  LabelMutVar("MUT_53", "", "Rear Long Fuel Trim Bank 2");
  LabelMutVar("MUT_54", "AccelEnrichTPS", "Acceleration Enrichment (increasing TPS)");
  LabelMutVar("MUT_55", "DecelLeanTPS", "Deceleration Enleanment (decreasing TPS)");
  LabelMutVar("MUT_56", "AccelLoadChg", "Acceleration Load Change");
  LabelMutVar("MUT_57", "DecelLoadChg", "Deceleration Load Change");
  LabelMutVar("MUT_58", "", "AFR Ct Adder");
  LabelMutVar("MUT_5B", "", "Rear O2 Voltage");
  LabelMutVar("MUT_5C", "", "ADC Rear O2 Voltage");
  LabelMutVar("MUT_60", "", "Rear O2 Trim - Low");
  LabelMutVar("MUT_61", "", "Rear O2 Trim - Mid");
  LabelMutVar("MUT_62", "", "Rear O2 Trim - High");
  LabelMutVar("MUT_63", "", "Rear O2 Feedback Trim");
  LabelMutVar("MUT_6A", "knock_adc", "knock adc processed");
  LabelMutVar("MUT_6B", "knock_base", "knock base");
  LabelMutVar("MUT_6C", "knock_var", "knock var (AKA Knock Sum Addition)");
  LabelMutVar("MUT_6D", "knock_change", "knock change");
  LabelMutVar("MUT_6E", "knock_dynamics", "knock dynamics");
  LabelMutVar("MUT_6F", "knock_flag", "knock flag (AKA Knock Acceleration)");
  LabelMutVar("MUT_70", "", "Array of Serial Receive Data Register 2 RDR 2 Values");
  LabelMutVar("MUT_71", "", "Sensor Error");
  LabelMutVar("MUT_72", "", "Knock Present");
  LabelMutVar("MUT_73", "", "Throttle Position Delta 1");
  LabelMutVar("MUT_74", "", "Throttle Position Delta 2");
  LabelMutVar("MUT_76", "ISCV % Demand", "ISCV % Demand (Columns)");
  LabelMutVar("MUT_79", "InjectorLatency", "Injector Latency");
  LabelMutVar("MUT_7A", "", "Continuous Monitor Completion Status 1");
  LabelMutVar("MUT_7B", "", "Continuous Monitor Completion Status 2");
  LabelMutVar("MUT_7C", "", "Continuous Monitor Completion Status 3");
  LabelMutVar("MUT_7D", "", "Non Continuous Monitor Completion Status OBD");
  LabelMutVar("MUT_7E", "", "Continuous Monitor Completion Status Low 4");
  LabelMutVar("MUT_7F", "", "Continuous Monitor Completion Status High 4");
  LabelMutVar("MUT_80", "", "ECU ID Type (LSB)");
  LabelMutVar("MUT_81", "", "ECU ID Type (MSB)");
  LabelMutVar("MUT_82", "", "ECU ID Version");
  LabelMutVar("MUT_83", "", "ADC Channel F");
  LabelMutVar("MUT_84", "ThermoFanDuty", "Thermo Fan Dutycycle");
  LabelMutVar("MUT_85", "EgrDuty", "EGR Dutycycle");
  LabelMutVar("MUT_86", "WGDC", "Wastegate Duty Cycle");
  LabelMutVar("MUT_87", "FuelTemperature", "Fuel Temperature");
  LabelMutVar("MUT_88", "FuelLevel", "Fuel Level");
  LabelMutVar("MUT_89", "", "ADC Channel 8 2");
  LabelMutVar("MUT_8A", "LoadError", "Load Error - (Throttle Position Corrected ?)");
  LabelMutVar("MUT_8B", "WGDCCorr", "WGDC Correction");
  LabelMutVar("MUT_8E", "", "Solenoid Duty");
  LabelMutVar("MUT_90", "", "Timer Status Register 9 TSR9");
  LabelMutVar("MUT_96", "MAF_ADC", "RAW MAF ADC value");
  LabelMutVar("MUT_9A", "ACClutch", "AC clutch");
  LabelMutVar("MUT_9B", "", "Output Pins");
  LabelMutVar("MUT_A2", "CrankPulse", "Crankshaft sensor pulse");
  LabelMutVar("MUT_A2", "MafPulse", "MAF sensor pulse");
  LabelMutVar("MUT_A2", "CamPulse", "Camshaft sensor pulse");
  LabelMutVar("MUT_A8", "ATInShaftPulse", "Input shaft speed pulse (A/T)");
  LabelMutVar("MUT_A8", "ATOutShaftPulse", "Output shaft speed pulse (A/T)");
  LabelMutVar("MUT_A8", "ATGearL", "Gear: Low (A/T)");
  LabelMutVar("MUT_A8", "ATGear2", "Gear: 2 (A/T)");
  LabelMutVar("MUT_A8", "ATGear3", "Gear: 3 (A/T)");
  LabelMutVar("MUT_A9", "O2HeaterFrontLeft", "Front O2 heater bank 1 (left)");
  LabelMutVar("MUT_A9", "O2HeaterRearLeft", "Rear O2 heater bank 1 (left)");
  LabelMutVar("MUT_A9", "O2HeaterFrontRight", "Front O2 heater bank 2 (right)");
  LabelMutVar("MUT_A9", "O2HeaterRearRight", "Rear O2 heater bank 2 (right)");
  LabelMutVar("MUT_AA", "Braking", "Brakes Pressed");
  LabelMutVar("MUT_B3", "ATGearNeutral", "Gear: Neutral (A/T)");
  LabelMutVar("MUT_B3", "ATGearDrive", "Gear: Drive (A/T)");
  LabelMutVar("MUT_B4", "ATGearPark", "Gear: Park (A/T)");
  LabelMutVar("MUT_B4", "ATGearRev", "Gear: Reverse (A/T)");
  LabelMutVar("MUT_B7", "O2HeaterBrokenFrRt", "front O2 heater circuit open (broken): bank 2 (right)");
  LabelMutVar("MUT_B8", "O2HeaterBrokenFrLt", "front O2 heater circuit open (broken): bank 1 (left)");
  LabelMutVar("MUT_B8", "NewACSwitch", "Air Conditioning Switch (Mattjin)");
  LabelMutVar("MUT_B8", "PowerSteering", "Power Steering");
  LabelMutVar("MUT_B9", "O2HeaterBrokenRearRt", "rear O2 heater circuit open (broken): bank 2 (right)");
  LabelMutVar("MUT_BA", "O2HeaterBrokenRearLt", "rear O2 heater circuit open (broken): bank 1 (left)");

  // Common MUT commands
  LabelMutVar("MUT_C3", "", "SAS (Speed Adjusting Screw)");
  LabelMutVar("MUT_C5", "", "Purge solenoid venting");
  LabelMutVar("MUT_CA", "", "Invalid command");
  LabelMutVar("MUT_CB", "", "Invalid command");
  LabelMutVar("MUT_CD", "", "A/C fan high");
  LabelMutVar("MUT_CE", "", "A/C fan low");
  LabelMutVar("MUT_CF", "", "Main fan high");
  LabelMutVar("MUT_D0", "", "Main fan low");
  LabelMutVar("MUT_D2", "", "Lower RPM");
  LabelMutVar("MUT_D3", "", "Boost control solenoid");
  LabelMutVar("MUT_D5", "", "EGR solenoid");
  LabelMutVar("MUT_D6", "", "Fuel pressure solenoid");
  LabelMutVar("MUT_D7", "", "Purge solenoid");
  LabelMutVar("MUT_D8", "", "Fuel pump");
  LabelMutVar("MUT_D9", "", "Fix timing at 5 degrees");
  LabelMutVar("MUT_DA", "", "Disable injector 1");
  LabelMutVar("MUT_DB", "", "Disable injector 2");
  LabelMutVar("MUT_DC", "", "Disable injector 3");
  LabelMutVar("MUT_DD", "", "Disable injector 4");
  LabelMutVar("MUT_DE", "", "Disable injector 5 (unused)");
  LabelMutVar("MUT_DF", "", "Disable injector 6 (unused)");
  LabelMutVar("MUT_EC", "", "Calibration F6A");
  LabelMutVar("MUT_ED", "", "Calibration");
  LabelMutVar("MUT_EE", "", "Calibration");
  LabelMutVar("MUT_EF", "", "Calibration");
  LabelMutVar("MUT_F3", "", "Cancel previously-active command (ie. SAS mode)");
  LabelMutVar("MUT_F9", "", "some keep alive function to keep the accuator engaged. response is 0xff");
  LabelMutVar("MUT_FA", "", "Clear active and stored faults");
  LabelMutVar("MUT_FB", "", "Force tests to run");
  LabelMutVar("MUT_FC", "", "Clear active faults");
  LabelMutVar("MUT_FE", "", "Immobilizer");
  LabelMutVar("MUT_FF", "", "Init code");

  Message("Done\n");
}

static FixDataOffsets(void) {
  auto ea, end, disass;

 /*  ea = 0;
  end = SegEnd(ea);
  if (ea == BADADDR || end == BADADDR) {
    Message("nothing selected\n");
    return;
  }
  Message("Fixing offsets from %x to %x... ", ea, end);

  for (ea; ea <= end; ea = NextAddr(ea)) {
    if (ea == BADADDR)
      break;

    // Check for loc_, off_xxx + y
    disass = GetDisasm(ea);

    if ((strstr(disass, ".data.l loc_") != -1 && strstr(disass, "+") != -1) ||
        (strstr(disass, ".data.l off_") != -1 && strstr(disass, "+") != -1)) {
      //Message("fixing %s  @0x%x\n", disass, ea);
      MakeWord(ea);
    }
  } */
  Message("Done\n");
}

static FixConstants(void) {
  auto ea, end, disass;

/*   ea = 0x1500;
  end = 0x3500;

  Message("Fixing constants from %x to %x... ", ea, end);
  for (ea; ea <= end && ea != BADADDR; ea = NextAddr(ea)) {
    if (Name(ea) == "" || strstr(Name(ea), "unk_") == 0)
      MakeWord(ea);
  } */
  Message("Done\n");
}


static WellKnownFunc(ea, name, comment) {
  if (ea == BADADDR)
    return;
  /* SafeMakeName(ea, name);
  MakeCode(ea);
  SetFunctionFlags(ea, 0);
  MakeFunction(ea, BADADDR);
  if (comment != "" && GetFunctionCmt(ea, 0) == "")
    SetFunctionCmt(ea, comment, 0); */
}

static LabelLibraryFuncs() {
  auto start, ea, i, end;

/*
  WellKnownFunc(0xDD2, "ZIP_DISK_DETECT", "Reads WORD at (R4 + (MAPindex * 4)) into R0");
  */

  {
    // Look for the main() function, it should be the only sub called from 'init'
    start = Dword(0);
    end = GetFunctionAttr(start, FUNCATTR_END);
    for (i = start; i != BADADDR; i = NextHead(i, end)) {
      if (GetMnem(i) == "jsr") {
        start = Rfirst0(i);
        // Message("Real init starts at %x\n", start);
        WellKnownFunc(start, "main", "ROM entry point");
        break;
      }
    }
  }
}


//-----------------------------------------------------------------------
// Get name of the current processor
static get_processor(void) {
  auto i, procname, chr;

  procname = "";
  for (i = 0; i < 8; i++) {
    chr = GetCharPrm(INF_PROCNAME + i);
    if (chr == 0) break;
    procname = procname + chr;
  }
  return procname;
}

static main() {
  auto processor, newaf;

  SetLongPrm(INF_MAXREF, 16);
  SetCharPrm(INF_INDENT, 22);
  SetCharPrm(INF_COMMENT, 70);
  SetCharPrm(INF_MARGIN, 120);
  SetCharPrm(INF_PREFFLAG, PREF_SEGADR | PREF_FNCOFF); // show segment and function prefixes

  SetCharPrm(INF_CMTFLAG, SW_ALLCMT);                  // show all comments
  SetCharPrm(INF_ASMTYPE, 0);                          // use GNU asm format
  {
    // Disable some analysis options that don't suit the SH2/SH4 code
    newaf = newaf & ~AF_MARKCODE; // Mark typical code sequences as code
    newaf = newaf & ~AF_PROCPTR;  // Create function if data xref->code32 exists
    newaf = newaf & ~AF_LVAR;     // Create stack variables
    newaf = newaf & ~AF_TRACE;    // Trace stack pointer
    newaf = newaf & ~AF_ASCII;    // Create ascii string if data xref exists
    newaf = newaf & ~AF_FINAL;    // Final pass of analysis
  //  SetShortPrm(INF_START_AF, newaf);

    newaf = GetShortPrm(INF_AF2);
    newaf = newaf & ~AF2_JUMPTBL; // Locate and create jump tables
    newaf = newaf & ~AF2_DODATA;  // Coagulate data segs in final pass
    newaf = newaf & ~AF2_CHKUNI;  // Check for unicode strings
    SetShortPrm(INF_AF2, newaf);
  }


 // MakeName	(0X10601354,	"show_dialog_box?");



/*
           ┌──────────────────────────────────┐
H'00000000 │                                  │
           │                                  │
           │                                  │
           │                                  │
           │          On-chip ROM             │
           │           64 kbytes              │
           │                                  │
           │                                  │
H'0000FFFF │                                  │
           ├──────────────────────────────────┤
H'00010000 │                                  │
           │                                  │
           │                                  │
           │                                  │
           │                                  │
           │  On-chip ROM / external address  │
           │        space/reserved area*      │
           │                                  │
           │                                  │
           │                                  │
H'0001FFFF │                                  │
           ├──────────────────────────────────┤
H'00020000 │                                  │
           ≡       External address space     ≡ 
           │                                  │
           ├──────────────────────────────────┤
H'00FFEC00 │                                  │
           │           On Chip RAM            │
H'00FFFBFF │            4 Kbytes              │
           ├──────────────────────────────────┤
H'00FFFC00 │      External address space      │
           ├──────────────────────────────────┤
H'00FFFE3F │     Internal I/O Registers       │
           ├──────────────────────────────────┤
H'00FFFF08 │      External address space      │
           ├──────────────────────────────────┤
H'00FFFF28 │      Internal I/O Registers      │
H'00FFFFFF └──────────────────────────────────┘
*/

  processor = get_processor_name();
  if {(processor == "h8") {
    Message("H8 create segment %x-%x\n", 0x10000, 0x1ffff);
    SegCreate(0x10000, 0x1ffff, 0x0, 0, 1, 2);
    SegRename(0x10000, "seg001");
    SegClass (0x10000, "CODE");
    SegDefReg(0x10000, "br", 0x0);
    SegDefReg(0x10000, "dp", 0x1);
    SetSegmentType(0x10000, 2);

    //Message("H8/500 create segment %x-%x\n", 0x14000, 0x1ffff);
    //SegCreate(0x14000, 0x20000, 0x0, 0, 1, 2);
    //SegRename(0x14000, "seg001");
    //SegClass (0x14000, "CODE");
    //SegDefReg(0x14000, "br", 0x0);
    //SegDefReg(0x14000, "dp", 0x1);
    //SetSegmentType(0x14000, 2);

    Message("H8/500 create segment %x-%x\n", 0x20000, 0x2ffff);
    SegCreate(0x20000, 0x2ffff, 0x0, 0, 1, 2);
    SegRename(0x20000, "seg002");
    SegClass (0x20000, "CODE");
    SegDefReg(0x20000, "br", 0x0);
    SegDefReg(0x20000, "dp", 0x2);
    SetSegmentType(0x20000, 2);

    Message("H8/500 Creating RAM\n");
    SegCreate(0xEE80, 0xFFFF, 0, 1, saRelWord, 0);
    SegRename(0XEE80, "RAM");

    MakeNameEx(0x0001021A, "rom_id", SN_NOLIST);
    MakeDword(0x0001021A);

    LowVoids(0);
    HighVoids(H8_CODE_OFFSET);
  } else {
    Message("Unknown processor type %s\n", processor);
  }
}
