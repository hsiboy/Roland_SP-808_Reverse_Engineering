// SP808_IDA_helper.idc
//
// IDA Pro IDC script for Roland SP-808 / Edirol A6 firmware analysis.
//
// Load SP8EXall.bin with:
//   Processor : H8/300H Advanced (H8S/2653)
//   Load base : 0x100000
//   ROM type  : binary
//
// Then run via File > Script file.
//
// All addresses are IDA runtime addresses.
// Conversion: file_offset = ida_address - 0x100000
//
// Register addresses from H8S/2655 Group Hardware Manual REJ09B0331-0500 Rev5.00.
// H8S/2653 and H8S/2655 share the same internal I/O register map.
//
// Authors: hsiboy, Professor_jonny
//

#include <idc.idc>

#define BASE_ADDRESS    0x100000
#define MASK_ROM_END    0x00E800
#define FLASH_END       0x1C0004

static SafeMakeName(ea, name) {
    auto existing_ea;
    existing_ea = LocByName(name);
    if (existing_ea != BADADDR && existing_ea != ea) return;
    MakeNameEx(ea, name, SN_NOWARN);
}

static NameLoc(ea, name, comment) {
    SafeMakeName(ea, name);
    if (comment != "")
        MakeRptCmt(ea, comment);
}

static MakeByteArray(ea, count, name, comment) {
    auto i;
    for (i = 0; i < count; i++)
        MakeByte(ea + i);
    MakeArray(ea, count);
    SafeMakeName(ea, name);
    if (comment != "")
        MakeRptCmt(ea, comment);
}

static NameFunc(ea, name, comment) {
    if (ea == BADADDR) return;
    MakeCode(ea);
    MakeFunction(ea, BADADDR);
    SafeMakeName(ea, name);
    if (comment != "")
        SetFunctionCmt(ea, comment, 0);
}

static H8RegisterNames() {
    NameLoc(0xFFFEC0, "ICRA",   "Interrupt control register A");
    NameLoc(0xFFFEC1, "ICRB",   "Interrupt control register B");
    NameLoc(0xFFFEC2, "ICRC",   "Interrupt control register C");
    NameLoc(0xFFFEC4, "IPRA",   "Interrupt priority register A");
    NameLoc(0xFFFEC5, "IPRB",   "Interrupt priority register B");
    NameLoc(0xFFFEC6, "IPRC",   "Interrupt priority register C");
    NameLoc(0xFFFEC7, "IPRD",   "Interrupt priority register D");
    NameLoc(0xFFFEC8, "IPRE",   "Interrupt priority register E");
    NameLoc(0xFFFEC9, "IPRF",   "Interrupt priority register F");
    NameLoc(0xFFFECA, "IPRG",   "Interrupt priority register G");
    NameLoc(0xFFFECB, "IPRH",   "Interrupt priority register H");
    NameLoc(0xFFFECC, "IPRI",   "Interrupt priority register I");
    NameLoc(0xFFFECD, "IPRJ",   "Interrupt priority register J");
    NameLoc(0xFFFECE, "IPRK",   "Interrupt priority register K");
    NameLoc(0xFFFED0, "ABWCR",  "Bus width control register");
    NameLoc(0xFFFED1, "ASTCR",  "Access state control register");
    NameLoc(0xFFFED2, "WCRH",   "Wait control register H");
    NameLoc(0xFFFED3, "WCRL",   "Wait control register L");
    NameLoc(0xFFFED4, "BCRH",   "Bus control register H (reset H'D0)");
    NameLoc(0xFFFED5, "BCRL",   "Bus control register L (reset H'3C): EAE/WAITE/WDBE");
    NameLoc(0xFFFED6, "MCR",    "Memory control register");
    NameLoc(0xFFFED7, "DRAMCR", "DRAM control register");
    NameLoc(0xFFFEB0, "P1DDR",  "Port 1 DDR (write-only)");
    NameLoc(0xFFFEB1, "P2DDR",  "Port 2 DDR (write-only): bits 0/5/6 drive HC138 A/B/C for DSP CS steering");
    NameLoc(0xFFFEB2, "P3DDR",  "Port 3 DDR (write-only)");
    NameLoc(0xFFFEB4, "P5DDR",  "Port 5 DDR (write-only)");
    NameLoc(0xFFFEB5, "P6DDR",  "Port 6 DDR (write-only)");
    NameLoc(0xFFFEB9, "PADDR",  "Port A DDR (write-only)");
    NameLoc(0xFFFEBA, "PBDDR",  "Port B DDR (write-only)");
    NameLoc(0xFFFEBB, "PCDDR",  "Port C DDR (write-only)");
    NameLoc(0xFFFEBC, "PDDDR",  "Port D DDR (write-only)");
    NameLoc(0xFFFEBD, "PEDDR",  "Port E DDR (write-only)");
    NameLoc(0xFFFEBE, "PFDDR",  "Port F DDR (write-only)");
    NameLoc(0xFFFEBF, "PGDDR",  "Port G DDR (write-only): CS0-CS3; CS3 enables HC138 for DSP decode");
    NameLoc(0xFFFF60, "P1DR",   "Port 1 data register");
    NameLoc(0xFFFF61, "P2DR",   "Port 2 data register: bits 0/5/6 steer HC138 A/B/C for DSP chip select");
    NameLoc(0xFFFF62, "P3DR",   "Port 3 data register");
    NameLoc(0xFFFF64, "P5DR",   "Port 5 data register");
    NameLoc(0xFFFF65, "P6DR",   "Port 6 data register");
    NameLoc(0xFFFF69, "PADR",   "Port A data register");
    NameLoc(0xFFFF6A, "PBDR",   "Port B data register");
    NameLoc(0xFFFF6B, "PCDR",   "Port C data register");
    NameLoc(0xFFFF6C, "PDDR",   "Port D data register");
    NameLoc(0xFFFF6D, "PEDR",   "Port E data register");
    NameLoc(0xFFFF6E, "PFDR",   "Port F data register");
    NameLoc(0xFFFF6F, "PGDR",   "Port G data register: CS0-CS3 outputs");
    NameLoc(0xFFFF50, "PORT1",  "Port 1 pin state (read-only)");
    NameLoc(0xFFFF51, "PORT2",  "Port 2 pin state (read-only)");
    NameLoc(0xFFFF52, "PORT3",  "Port 3 pin state (read-only)");
    NameLoc(0xFFFF53, "PORT4",  "Port 4 pin state (read-only)");
    NameLoc(0xFFFF54, "PORT5",  "Port 5 pin state (read-only)");
    NameLoc(0xFFFF55, "PORT6",  "Port 6 pin state (read-only)");
    NameLoc(0xFFFF59, "PORTA",  "Port A pin state (read-only)");
    NameLoc(0xFFFF5A, "PORTB",  "Port B pin state (read-only)");
    NameLoc(0xFFFF5B, "PORTC",  "Port C pin state (read-only)");
    NameLoc(0xFFFF5C, "PORTD",  "Port D pin state (read-only)");
    NameLoc(0xFFFF5D, "PORTE",  "Port E pin state (read-only)");
    NameLoc(0xFFFF5E, "PORTF",  "Port F pin state (read-only)");
    NameLoc(0xFFFF5F, "PORTG",  "Port G pin state (read-only)");
    NameLoc(0xFFFF2C, "ISCRH",  "IRQ sense control register H");
    NameLoc(0xFFFF2D, "ISCRL",  "IRQ sense control register L");
    NameLoc(0xFFFF2E, "IER",    "IRQ enable register");
    NameLoc(0xFFFF2F, "ISR",    "IRQ status register");
    NameLoc(0xFFFF38, "SBYCR",   "Standby control register");
    NameLoc(0xFFFF39, "SYSCR",   "System control register");
    NameLoc(0xFFFF3A, "SCKCR",   "System clock control register");
    NameLoc(0xFFFF3B, "MDCR",    "Mode control register (read-only)");
    NameLoc(0xFFFF3C, "MSTPCRH", "Module stop control register H");
    NameLoc(0xFFFF3D, "MSTPCRL", "Module stop control register L");
    NameLoc(0xFFFFC0, "TSTR",   "Timer start register");
    NameLoc(0xFFFFC1, "TSYR",   "Timer synchro register");
    NameLoc(0xFFFF78, "SMR0",   "SCI0 serial mode register (MIDI)");
    NameLoc(0xFFFF79, "BRR0",   "SCI0 bit rate register (MIDI)");
    NameLoc(0xFFFF7A, "SCR0",   "SCI0 serial control register (MIDI)");
    NameLoc(0xFFFF7B, "TDR0",   "SCI0 transmit data register (MIDI)");
    NameLoc(0xFFFF7C, "SSR0",   "SCI0 serial status register (MIDI)");
    NameLoc(0xFFFF7D, "RDR0",   "SCI0 receive data register (MIDI)");
    NameLoc(0xFFFF7E, "SCMR0",  "SCI0 smart card mode register");
    NameLoc(0xFFFF80, "SMR1",   "SCI1 serial mode register");
    NameLoc(0xFFFF81, "BRR1",   "SCI1 bit rate register");
    NameLoc(0xFFFF82, "SCR1",   "SCI1 serial control register");
    NameLoc(0xFFFF83, "TDR1",   "SCI1 transmit data register");
    NameLoc(0xFFFF84, "SSR1",   "SCI1 serial status register");
    NameLoc(0xFFFF85, "RDR1",   "SCI1 receive data register");
    NameLoc(0xFFFF86, "SCMR1",  "SCI1 smart card mode register");
    NameLoc(0xFFFF88, "SMR2",   "SCI2 serial mode register");
    NameLoc(0xFFFF89, "BRR2",   "SCI2 bit rate register");
    NameLoc(0xFFFF8A, "SCR2",   "SCI2 serial control register");
    NameLoc(0xFFFF8B, "TDR2",   "SCI2 transmit data register");
    NameLoc(0xFFFF8C, "SSR2",   "SCI2 serial status register");
    NameLoc(0xFFFF8D, "RDR2",   "SCI2 receive data register");
    NameLoc(0xFFFF8E, "SCMR2",  "SCI2 smart card mode register");
    NameLoc(0xFFFF90, "ADDRA",  "A/D data register A (16-bit, read-only)");
    NameLoc(0xFFFF92, "ADDRB",  "A/D data register B (16-bit, read-only)");
    NameLoc(0xFFFF94, "ADDRC",  "A/D data register C (16-bit, read-only)");
    NameLoc(0xFFFF96, "ADDRD",  "A/D data register D (16-bit, read-only)");
    NameLoc(0xFFFF98, "ADCSR",  "A/D control/status register");
    NameLoc(0xFFFF99, "ADCR",   "A/D control register");
    NameLoc(0xFFFFA8, "FLMCR1", "Flash memory control register 1");
    NameLoc(0xFFFFA9, "FLMCR2", "Flash memory control register 2");
    NameLoc(0xFFFFAA, "EBR1",   "Erase block register 1");
    NameLoc(0xFFFFAB, "EBR2",   "Erase block register 2");
    Message("H8S/2653 register names applied.\n");
}

static FixupVectorTable() {
    auto i, target;
    Message("Processing exception vector table...\n");
    for (i = 0x000000; i < 0x000170; i = i + 4) {
        MakeDword(i);
        OpOff(i, 0, 0);
        target = Dword(i) & 0x00FFFFFF;
        if (target >= BASE_ADDRESS && target < FLASH_END) {
            MakeCode(target);
            AutoMark(target, AU_PROC);
        }
    }
    SafeMakeName(0x000000, "vec_power_on_reset");
    SafeMakeName(0x000004, "vec_manual_reset");
    SafeMakeName(0x00001C, "vec_nmi");
    SafeMakeName(0x000020, "vec_trap0");
    SafeMakeName(0x000024, "vec_trap1");
    SafeMakeName(0x000028, "vec_trap2");
    SafeMakeName(0x00002C, "vec_trap3");
    SafeMakeName(0x000040, "vec_irq0");
    SafeMakeName(0x000044, "vec_irq1");
    SafeMakeName(0x000048, "vec_irq2");
    SafeMakeName(0x00004C, "vec_irq3");
    SafeMakeName(0x000050, "vec_irq4");
    SafeMakeName(0x000054, "vec_irq5");
    SafeMakeName(0x000058, "vec_irq6");
    SafeMakeName(0x00005C, "vec_irq7");
    Message("Vector table done.\n");
}

static LabelBootFunctions() {
    NameFunc(0x12CC54, "firmware_cold_start",
        "C runtime startup: zero RAM 0x403000-0x42BFFC, copy .data section, "
        "run ptr_installer, call boot_and_main_loop, tail-jmp main_loop_entry.");

    NameFunc(0x12CCC4, "ptr_installer",
        "Walks installer table at 0x12CCFA. Records: [ram_dest:32][flash_src:32]. "
        "OR's 0x5A000000 tag into flash address before storing. "
        "Terminated by 0xFFFFFFFF.");

    NameFunc(0x1258D8, "boot_and_main_loop",
        "Hardware bring-up via system_dispatcher opcodes 0x81/63/53/D0/D2/44/40/41. "
        "Infinite main loop: main_loop_svc_A/B/C then audio_tick via ptr.");

    NameFunc(0x1463C6, "top_level_init",
        "Calls subsystem_init_chain and audio_buf_dma_init.");

    NameFunc(0x151C66, "subsystem_init_chain",
        "Sequential init of 8 subsystems. Loads audio_config_byte (0x43B7B5). "
        "Order: sub_139206, sub_151BBA, sub_14A284, sub_136158, dsp_init, "
        "sub_138378, sub_13BC5E, audio_buf_dma_init.");

    NameFunc(0x13B812, "audio_buf_dma_init",
        "Calls RAM prims 0x4004D0 and 0x4004AC. "
        "Installs audio_tick (0x1464AA) into dword_4032EE. "
        "Calls RAM prim 0x400208 with arg 0x144. "
        "Stores 0x3E into word_427728.");

    NameFunc(0x1381BC, "system_dispatcher",
        "Hardware command dispatcher. Opcode in r0. "
        "Known opcodes: 0x81, 0x63, 0x53 (Zip detect/ready?), "
        "0xD0, 0xD2, 0x44, 0x40, 0x41. Returns 0 on success.");

    NameFunc(0x1464AA, "audio_tick",
        "Main audio processing callback. Installed into main_loop_callback_ptr (0x4104BC). "
        "Called every main loop iteration. TENTATIVE name.");

    NameFunc(0x12E614, "dsp_init",
        "DSP init. Loads dsp_config_byte (0x43B7C0), calls loc_100A8C, "
        "sub_12ECFA (part A), sub_12EAF0 (part B, tail call).");

    NameFunc(0x146502, "main_loop_svc_A",
        "Main loop service A. Called every iteration. Function TBD.");
    NameFunc(0x1274F4, "main_loop_svc_B",
        "Main loop service B. Called every iteration. Function TBD.");
    NameFunc(0x105E0A, "main_loop_svc_C",
        "Main loop service C. Called every iteration. Function TBD.");

    Message("Boot/init function names applied.\n");
}

static LabelDSPFunctions() {
    NameFunc(0x1241E4, "esp_memory_test",
        "Tests 6 TC170C140 DSP memory regions: PRAM0/1, IRAM0/1, GRAM, ERAM. "
        "Calls RAM_prim_dsp_write (0x40046C) and RAM_prim_dsp_read (0x400470). "
        "Command byte pairs: r0h=0x04/r1h=0x05 and r0h=0x1B/r1h=0x1C. "
        "Result bitmask 0x3F = all 6 regions OK. "
        "On pass: sets bit 0 of dsp_ram_test_result, calls sub_1255EC.");

    NameFunc(0x124224, "esp_memory_test_worker",
        "Per-region DSP test worker. Dispatches on r3l: "
        "0=fill 0xFF; 2/F=write via dsp_write loop; "
        "3=read/verify via sub_12E3D6.");

    Message("ESP/DSP test function names applied.\n");
}

static LabelIOFunctions() {
    NameFunc(0x131C84, "region_update",
        "Range/bounds manager. Commands in r3l: "
        "0=reset to max; 9=special mode (check system_state_word vs 0xB1); "
        "2/F=clamp region_start/end_pos to limits in region_param_table. "
        "Calls sub_147052 on change.");

    NameFunc(0x132038, "data_thunk_131C84_173368",
        "Data thunk: loads er1=0x173368 then tail-calls region_update.");

    NameFunc(0x1321A4, "data_thunk_131E66_13212C",
        "Data thunk: zeros r1, loads er0=0x13212C, calls sub_131E66.");

    NameFunc(0x1321B2, "data_thunk_131C84_1734B0",
        "Data thunk: loads er1=0x1734B0 then tail-calls region_update.");

    NameFunc(0x15204A, "thunk_audio_buf_dma_init",
        "Thunk: jmp audio_buf_dma_init. Out-of-range bsr workaround.");

    NameFunc(0x1528C8, "word_array_init",
        "Zeroes 0x98-entry word array at 0x43B7E2. "
        "Installs fn ptr at dword_43B7DE -> 0x1528FC.");

    Message("I/O registration function names applied.\n");
}

static LabelStorageFunctions() {
    NameFunc(0x12A808, "ide_init",
        "Zeros device state arrays, programs EPSON SLA919F ASIC registers.");
    NameFunc(0x12A956, "device_probe",
        "Top-level device probe. ZIP-only gate at 0x12AA14.");
    NameFunc(0x12AA72, "atapi_cmd_sequence_full",
        "Runs SZHC ATAPI command table from entry 0.");
    NameFunc(0x12AAF2, "atapi_cmd_sequence_partial",
        "Runs SZHC ATAPI command table from START/STOP UNIT onwards.");
    NameFunc(0x12ACB0, "device_validate",
        "Validates ATAPI response; dispatches on device geometry/type byte.");
    NameFunc(0x12AE88, "device_classifier",
        "Classifies drive; writes type 1/2/3 to device_type_by_slot.");
    NameFunc(0x12B150, "cache_device_params",
        "Issues READ CAPACITY (0x25); stores last LBA and block length.");
    NameFunc(0x12B712, "atapi_command_handler",
        "Core ATAPI command send/receive via EPSON SLA919F.");
    Message("Storage function names applied.\n");
}

static LabelPatchTarget() {
    SafeMakeName(0x12AA12, "dc_check_type1");
    MakeComm(0x12AA12, "cmp.b #1, r0l -- test for ZIP device type (type 1)");
    SafeMakeName(0x12AA14, "dc_branch_if_not_type1");
    MakeRptCmt(0x12AA14,
        "PATCH TARGET (file offset 0x2AA14): "
        "change 46 10 (bne, rejects non-ZIP) to 40 00 (bra, allows all types).");
    Message("Patch target labelled.\n");
}

static LabelRAMPrimitives() {
    NameLoc(0x400200, "main_loop_entry",
        "RAM-resident main loop entry. Installed by mask ROM. "
        "Flash tail-jumps here at end of firmware_cold_start.");
    NameLoc(0x400208, "RAM_prim_400208",
        "RAM primitive. Called from audio_buf_dma_init with arg 0x144.");
    NameLoc(0x40034C, "RAM_prim_40034C", "RAM primitive. Unknown function.");
    NameLoc(0x400350, "RAM_prim_400350", "RAM primitive. Unknown function.");
    NameLoc(0x40046C, "RAM_prim_dsp_write",
        "RAM primitive: DSP write. Called from esp_memory_test_worker. "
        "Args: r0h/r0l=command, r1h/r1l=register. "
        "HC138 A/B/C select (P2DR bits 0/5/6) must be set before calling.");
    NameLoc(0x400470, "RAM_prim_dsp_read",
        "RAM primitive: DSP read/verify. Called from esp_memory_test_worker.");
    NameLoc(0x4002C8, "RAM_prim_4002C8",
        "RAM primitive. Called with arg 0x1F4 during init.");
    NameLoc(0x4002E0, "RAM_prim_4002E0",
        "RAM primitive. Called during boot_and_main_loop bring-up.");
    NameLoc(0x4004AC, "RAM_prim_hardware_cfg_A",
        "RAM primitive: hardware config A. Called from audio_buf_dma_init.");
    NameLoc(0x4004D0, "RAM_prim_hardware_cfg_B",
        "RAM primitive: hardware config B. Called from audio_buf_dma_init.");
    Message("RAM primitive labels applied.\n");
}

static LabelRAM() {
    MakeByte(0x401001);
    NameLoc(0x401001, "boot_mode_flag",
        "Cleared during unconditional init in boot_and_main_loop.");

    MakeDword(0x4104BC);
    NameLoc(0x4104BC, "main_loop_callback_ptr",
        "Fn ptr called every main loop iteration. Set to audio_tick (0x1464AA).");

    MakeWord(0x427728);
    NameLoc(0x427728, "word_427728", "Set to 0x3E (62) by audio_buf_dma_init.");

    MakeDword(0x427758);
    NameLoc(0x427758, "dword_427758", "Return value of RAM_prim_400208.");

    MakeDword(0x4032EE);
    NameLoc(0x4032EE, "audio_tick_callback_ptr",
        "Set to audio_tick (0x1464AA) by audio_buf_dma_init.");

    MakeDword(0x426CCE);
    NameLoc(0x426CCE, "firmware_version_packed",
        "e0=0x0013, r0=0x03E9. Possible version encoding. Not confirmed.");

    MakeWord(0x427C38);
    NameLoc(0x427C38, "system_state_word",
        "Central 16-bit state. 66 xrefs, 2 writers (sub_125316, sub_146788). "
        "Bits 14/8 = mode flags, low byte = state value. "
        "Compared against 0xB1 in region_update. "
        "Changes trigger callback via state_change_callback_ptr.");

    MakeDword(0x422018);
    NameLoc(0x422018, "state_change_callback_ptr",
        "Fn ptr called after system_state_word is written in sub_125316.");

    MakeByte(0x42202A);
    NameLoc(0x42202A, "dsp_ram_test_result",
        "Bit 0 set when all 6 DSP memory regions pass esp_memory_test. "
        "0x3F = all of PRAM0/1, IRAM0/1, GRAM, ERAM OK.");

    MakeByte(0x43B7B5);
    NameLoc(0x43B7B5, "audio_config_byte",
        "Loaded before subsystem_init_chain. Likely encodes sample rate.");

    MakeByte(0x43B7C0);
    NameLoc(0x43B7C0, "dsp_config_byte",
        "Loaded at start of dsp_init (sub_12E614).");

    MakeDword(0x43B6D0);
    NameLoc(0x43B6D0, "region_param_table",
        "Limit descriptors for region_update. Field +4 is upper limit.");

    MakeDword(0x426F1C);
    NameLoc(0x426F1C, "region_start_pos", "Loop/region start position.");

    MakeDword(0x426F20);
    NameLoc(0x426F20, "region_end_pos", "Loop/region end position.");

    MakeDword(0x426F24);
    NameLoc(0x426F24, "region_current_pos", "Current playback position.");

    MakeDword(0x426F9C);
    NameLoc(0x426F9C, "dword_426F9C",
        "Set to er2 during region_update case 9 (special mode).");

    MakeWord(0x421F0A);
    NameLoc(0x421F0A, "word_421F0A", "Set to r6 during sub_12CD7E init.");

    MakeWord(0x426CD4);
    NameLoc(0x426CD4, "word_426CD4", "Zeroed at start of sub_12CD7E.");

    MakeDword(0x43B7DE);
    NameLoc(0x43B7DE, "dword_43B7DE",
        "Fn ptr installed by word_array_init -> 0x1528FC.");

    MakeByteArray(0x43B7E2, 0x130, "word_array_43B7E2",
        "0x98-entry (152) word array. Zeroed by word_array_init.");

    NameLoc(0x403000, "ram_clear_start",
        "Start of DRAM region zeroed by firmware_cold_start.");
    NameLoc(0x42BFFC, "ram_clear_end",
        "End of DRAM region zeroed by firmware_cold_start.");

    MakeByteArray(0x426C82, 8, "device_type_by_slot",
        "8-slot: 0=none, 1=ZIP, 2=HDD-small, 3=HDD-large");
    MakeByteArray(0x426C0A, 8, "slot_flag_A",   "8-slot (semantic unconfirmed)");
    MakeByteArray(0x426C12, 8, "slot_flag_B",   "8-slot (semantic unconfirmed)");
    MakeByteArray(0x426C1A, 8, "slot_flag_C",   "8-slot (semantic unconfirmed)");
    MakeByteArray(0x426C22, 8, "slot_flag_D",   "8-slot (semantic unconfirmed)");
    MakeByteArray(0x426C2A, 8, "slot_flag_E",   "8-slot (semantic unconfirmed)");
    MakeByteArray(0x426C32, 8, "slot_media_accepted",
        "8-slot: non-zero = device accepted");
    MakeByteArray(0x426C3A, 8, "slot_device_flags", "8-slot device flags");

    MakeByte(0x426C8A);
    NameLoc(0x426C8A, "active_slot", "Currently active device slot index");

    MakeWord(0x40101E);
    NameLoc(0x40101E, "device_status_reg",
        "ATAPI status: 0x8001=not init, 0x8003=no device, 0x8007=found, "
        "0x8008=ZIP OK, 0x8009=unknown, 0x800B=wrong device, 0x8015=rejected");

    MakeByte(0x426BF8); NameLoc(0x426BF8, "atapi_status_hi", "");
    MakeByte(0x426BF9); NameLoc(0x426BF9, "atapi_status_lo", "");
    MakeByte(0x426BFC); NameLoc(0x426BFC, "ide_init_done",   "Non-zero once IDE initialised");
    MakeByte(0x426BFD); NameLoc(0x426BFD, "atapi_result",    "");
    MakeByte(0x426BFE); NameLoc(0x426BFE, "classify_lock",   "Guards device_validate entry");

    Message("RAM labels applied.\n");
}

static LabelROMData() {
    SafeMakeName(0x12CCFA, "install_table_0");
    MakeRptCmt(0x12CCFA,
        "Installer table: 8-byte records [ram_dest:32][flash_src:32]. "
        "flash_src OR'd with 0x5A000000. Walked by ptr_installer. "
        "Terminated by 0xFFFFFFFF.");

    SafeMakeName(0x12CD35, "install_table_1");
    MakeRptCmt(0x12CD35, "Installer table: same format as install_table_0.");

    MakeComm(0x12CD22,
        "Debug section marker [[Section Address:...]] "
        "Output to SCI1 during development boot.");

    SafeMakeName(0x170CA8, "dsp_test_pattern_table");
    MakeRptCmt(0x170CA8,
        "DSP memory test patterns indexed by region (r6+0xF). "
        "6 regions: PRAM0, PRAM1, IRAM0, IRAM1, GRAM, ERAM.");

    SafeMakeName(0x173368, "io_descriptor_table_0");
    MakeRptCmt(0x173368,
        "I/O handler table. Records: [ram_addr:32][flash_handler:32]. "
        "Bound to region_update by data_thunk_131C84_173368.");

    SafeMakeName(0x1734B0, "io_descriptor_table_1");
    MakeRptCmt(0x1734B0,
        "I/O handler table. Same format. "
        "Bound to region_update by data_thunk_131C84_1734B0.");

    SafeMakeName(0x171D00, "esp_test_descriptor");
    MakeRptCmt(0x171D00,
        "ESP test display descriptor. NG/OK strings at +4/+7. "
        "7-byte display records: [str_ptr:24][type:8][subtype:8][idx:16].");

SafeMakeName(0x17C454, "init_data_src_start");
MakeRptCmt(0x17C454, "Start of .data section copied to DRAM at 0x403000 on boot. "
    "Size: 0x42D bytes (1069). Ends at init_data_src_end (0x17C881).");

SafeMakeName(0x17C881, "init_data_src_end");
MakeRptCmt(0x17C881, "End of .data section. Destination: ram_clear_start (0x403000).");

    MakeStr(0x171ABB, BADADDR); SafeMakeName(0x171ABB, "str_dev_self");
    MakeStr(0x171AC0, BADADDR); SafeMakeName(0x171AC0, "str_dev_zip");
    MakeStr(0x171AC5, BADADDR); SafeMakeName(0x171AC5, "str_dev_hd");
    MakeStr(0x171ACA, BADADDR); SafeMakeName(0x171ACA, "str_dev_cd");
    MakeStr(0x171ACF, BADADDR); SafeMakeName(0x171ACF, "str_szhc");

    SafeMakeName(0x171AD4, "szhc_cmd_table");
    MakeRptCmt(0x171AD4, "SZHC ATAPI command table: 4 entries x 7 bytes");
    MakeComm(0x171AD4, "entry 0: 06 00 00 00 00 00 00  (reset/null)");
    MakeComm(0x171ADB, "entry 1: 06 1B 00 00 00 00 00  (START/STOP UNIT)");
    MakeComm(0x171AE2, "entry 2: 06 1E 00 00 00 00 00  (PREVENT/ALLOW MEDIA REMOVAL)");
    MakeComm(0x171AE9, "entry 3: 06 03 00 00 00 00 00  (REQUEST SENSE)");

    MakeStr(0x171AF0, BADADDR); SafeMakeName(0x171AF0, "str_vendor_iomega_upper");
    MakeStr(0x171AF9, BADADDR); SafeMakeName(0x171AF9, "str_vendor_iomega_lower");
    MakeStr(0x171B02, BADADDR); SafeMakeName(0x171B02, "str_product_zip");
    MakeStr(0x171B90, BADADDR); SafeMakeName(0x171B90, "str_vendor_roland");

    MakeStr(0x171D3A, BADADDR); SafeMakeName(0x171D3A, "str_esp_device");
    MakeStr(0x171D46, BADADDR); SafeMakeName(0x171D46, "str_esp_menu");
    MakeStr(0x171D4F, BADADDR); SafeMakeName(0x171D4F, "str_esp_pram");
    MakeStr(0x171D62, BADADDR); SafeMakeName(0x171D62, "str_esp_iram");
    MakeStr(0x171D75, BADADDR); SafeMakeName(0x171D75, "str_esp_gram_eram");

    MakeStr(0x171DC0, BADADDR); SafeMakeName(0x171DC0, "str_data_invalid");
    MakeStr(0x171DD4, BADADDR); SafeMakeName(0x171DD4, "str_waiting_sysex");
    MakeStr(0x171DE6, BADADDR); SafeMakeName(0x171DE6, "str_receiving");
    MakeStr(0x171DF8, BADADDR); SafeMakeName(0x171DF8, "str_midi_update");
    MakeStr(0x171E04, BADADDR); SafeMakeName(0x171E04, "str_update_system");
    MakeStr(0x171E18, BADADDR); SafeMakeName(0x171E18, "str_version_display");
    MakeStr(0x171E2C, BADADDR); SafeMakeName(0x171E2C, "str_checksum");
    MakeStr(0x171E40, BADADDR); SafeMakeName(0x171E40, "str_build_date");

    MakeStr(0x174BDF, BADADDR); SafeMakeName(0x174BDF, "str_err_not_sp808");
    MakeStr(0x174CB7, BADADDR); SafeMakeName(0x174CB7, "str_err_wrong_disk");
    MakeStr(0x174CD6, BADADDR); SafeMakeName(0x174CD6, "str_err_wrong_size");
    MakeStr(0x175233, BADADDR); SafeMakeName(0x175233, "str_media_100mb");
    MakeStr(0x175245, BADADDR); SafeMakeName(0x175245, "str_media_250mb");

    Message("ROM data labels applied.\n");
}

static main() {
    Message("\n=== SP-808 IDA helper ===\n");
    Message("Base address  : 0x%X\n", BASE_ADDRESS);
    Message("Mask ROM end  : 0x%X  (not in dump)\n", MASK_ROM_END);
    Message("Flash end     : 0x%X\n\n", FLASH_END);

    H8RegisterNames();
    FixupVectorTable();
    LabelBootFunctions();
    LabelDSPFunctions();
    LabelIOFunctions();
    LabelStorageFunctions();
    LabelPatchTarget();
    LabelRAMPrimitives();
    LabelRAM();
    LabelROMData();

    Message("\n=== Done ===\n");
    Message("Patch target    : 0x12AA14  (file offset 0x2AA14)\n");
    Message("  Original      : 46 10  (bne, rejects non-ZIP)\n");
    Message("  Patched       : 40 00  (bra, allows all device types)\n");
    Message("\nKey investigation targets:\n");
    Message("  system_dispatcher   : 0x1381BC  (opcode table not yet mapped)\n");
    Message("  system_state_word   : 0x427C38  (66 xrefs, composite state)\n");
    Message("  audio_tick          : 0x1464AA  (main audio callback)\n");
    Message("  dsp_init chain      : 0x12E614 -> 0x12ECFA -> 0x12EAF0\n");
    Message("  main_loop_entry     : 0x400200  (RAM-resident, mask ROM installed)\n");
}
