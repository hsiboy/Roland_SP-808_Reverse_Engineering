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
// Register addresses are taken directly from the H8S/2655 Group Hardware Manual
// (Renesas REJ09B0331-0500, Rev 5.00, Sep 2006). The H8S/2653 and H8S/2655 share
// the same internal I/O register map. All prior address conflicts have been
// resolved against that datasheet.
//
// Authors: hsiboy, Professor_jonny
//

#include <idc.idc>

#define BASE_ADDRESS    0x100000
#define MASK_ROM_END    0x00E800
#define FLASH_END       0x1C0004

// Apply a name only if the location does not already have a meaningful name.
static SafeMakeName(ea, name) {
    auto existing_ea;
    existing_ea = LocByName(name);
    if (existing_ea != BADADDR && existing_ea != ea) return;
    MakeNameEx(ea, name, SN_NOWARN);
}

// Apply a name and a repeatable comment.
static NameLoc(ea, name, comment) {
    SafeMakeName(ea, name);
    if (comment != "")
        MakeRptCmt(ea, comment);
}

// Define a byte array of 'count' bytes and name it.
static MakeByteArray(ea, count, name, comment) {
    auto i;
    for (i = 0; i < count; i++)
        MakeByte(ea + i);
    MakeArray(ea, count);
    SafeMakeName(ea, name);
    if (comment != "")
        MakeRptCmt(ea, comment);
}

// Name a function and set a comment.
static NameFunc(ea, name, comment) {
    if (ea == BADADDR) return;
    MakeCode(ea);
    MakeFunction(ea, BADADDR);
    SafeMakeName(ea, name);
    if (comment != "")
        SetFunctionCmt(ea, comment, 0);
}

// ---------------------------------------------------------------------------
// H8S/2653 internal I/O register names
// Source: H8S/2655 Group Hardware Manual REJ09B0331-0500 Rev5.00
// H8S/2653 and H8S/2655 share the same internal I/O register map.
// All addresses are lower 16 bits; full 24-bit address = 0xFF0000 | lower16.
// ---------------------------------------------------------------------------
static H8RegisterNames() {

    // --- Interrupt controller (base H'FEC0) ---
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

    // --- Bus controller (base H'FED0) ---
    NameLoc(0xFFFED0, "ABWCR",  "Bus width control register");
    NameLoc(0xFFFED1, "ASTCR",  "Access state control register");
    NameLoc(0xFFFED2, "WCRH",   "Wait control register H");
    NameLoc(0xFFFED3, "WCRL",   "Wait control register L");
    NameLoc(0xFFFED4, "BCRH",   "Bus control register H (reset=H'D0): DRAM/burst/ICIS config");
    NameLoc(0xFFFED5, "BCRL",   "Bus control register L (reset=H'3C): EAE/WAITE/WDBE flags");
    NameLoc(0xFFFED6, "MCR",    "Memory control register");
    NameLoc(0xFFFED7, "DRAMCR", "DRAM control register");

    // --- GPIO data direction registers (write-only, base H'FEB0) ---
    // Writing 1 to a bit configures the corresponding pin as output.
    NameLoc(0xFFFEB0, "P1DDR",  "Port 1 DDR (write-only): A0-A7 alternate");
    NameLoc(0xFFFEB1, "P2DDR",  "Port 2 DDR (write-only): A8-A15 alternate. Bits 0/5/6 drive HC138 A/B/C for DSP chip select steering");
    NameLoc(0xFFFEB2, "P3DDR",  "Port 3 DDR (write-only): SCI TxD/RxD/SCK alternate");
    NameLoc(0xFFFEB4, "P5DDR",  "Port 5 DDR (write-only): A16-A19/SCI2 alternate");
    NameLoc(0xFFFEB5, "P6DDR",  "Port 6 DDR (write-only)");
    NameLoc(0xFFFEB9, "PADDR",  "Port A DDR (write-only): A20-A23/PPG alternate");
    NameLoc(0xFFFEBA, "PBDDR",  "Port B DDR (write-only): D0-D7 alternate");
    NameLoc(0xFFFEBB, "PCDDR",  "Port C DDR (write-only): D8-D15 alternate");
    NameLoc(0xFFFEBC, "PDDDR",  "Port D DDR (write-only): DMAC/PPG alternate");
    NameLoc(0xFFFEBD, "PEDDR",  "Port E DDR (write-only): PWM/GPIO");
    NameLoc(0xFFFEBE, "PFDDR",  "Port F DDR (write-only): AS/RD/HWR/LWR/CLK/WAIT system bus");
    NameLoc(0xFFFEBF, "PGDDR",  "Port G DDR (write-only): CS0-CS3 chip selects. PG2=CS2 (EPSON ASIC), PG4=CS0 (flash). CS3 enables HC138 G2A/G2B for DSP chip select decode");

    // --- GPIO data registers (read/write output latch, base H'FF60) ---
    NameLoc(0xFFFF60, "P1DR",   "Port 1 data register");
    NameLoc(0xFFFF61, "P2DR",   "Port 2 data register: bits 0/5/6 steer HC138 A/B/C to select DSP chip select line (CS1-CS7 on IC10). Write before accessing DSP address window");
    NameLoc(0xFFFF62, "P3DR",   "Port 3 data register: SCI TxD/RxD/SCK");
    NameLoc(0xFFFF64, "P5DR",   "Port 5 data register: A16-A19");
    NameLoc(0xFFFF65, "P6DR",   "Port 6 data register");
    NameLoc(0xFFFF69, "PADR",   "Port A data register: A20-A23");
    NameLoc(0xFFFF6A, "PBDR",   "Port B data register: D0-D7");
    NameLoc(0xFFFF6B, "PCDR",   "Port C data register: D8-D15");
    NameLoc(0xFFFF6C, "PDDR",   "Port D data register");
    NameLoc(0xFFFF6D, "PEDR",   "Port E data register");
    NameLoc(0xFFFF6E, "PFDR",   "Port F data register: system bus control outputs");
    NameLoc(0xFFFF6F, "PGDR",   "Port G data register: CS0-CS3. CS3 bit drives HC138 enable for DSP chip select decode");

    // --- GPIO pin state registers (read-only, base H'FF50) ---
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

    // --- IRQ sense/enable (base H'FF2C) ---
    NameLoc(0xFFFF2C, "ISCRH",  "IRQ sense control register H");
    NameLoc(0xFFFF2D, "ISCRL",  "IRQ sense control register L");
    NameLoc(0xFFFF2E, "IER",    "IRQ enable register");
    NameLoc(0xFFFF2F, "ISR",    "IRQ status register");

    // --- System control (base H'FF38) ---
    NameLoc(0xFFFF38, "SBYCR",   "Standby control register");
    NameLoc(0xFFFF39, "SYSCR",   "System control register");
    NameLoc(0xFFFF3A, "SCKCR",   "System clock control register");
    NameLoc(0xFFFF3B, "MDCR",    "Mode control register (read-only)");
    NameLoc(0xFFFF3C, "MSTPCRH", "Module stop control register H");
    NameLoc(0xFFFF3D, "MSTPCRL", "Module stop control register L");

    // --- Timer pulse unit: start/sync ---
    NameLoc(0xFFFFC0, "TSTR",   "Timer start register");
    NameLoc(0xFFFFC1, "TSYR",   "Timer synchro register");

    // --- SCI channel 0: MIDI IN/OUT (base H'FF78) ---
    NameLoc(0xFFFF78, "SMR0",   "SCI0 serial mode register (MIDI)");
    NameLoc(0xFFFF79, "BRR0",   "SCI0 bit rate register (MIDI)");
    NameLoc(0xFFFF7A, "SCR0",   "SCI0 serial control register (MIDI)");
    NameLoc(0xFFFF7B, "TDR0",   "SCI0 transmit data register (MIDI)");
    NameLoc(0xFFFF7C, "SSR0",   "SCI0 serial status register (MIDI)");
    NameLoc(0xFFFF7D, "RDR0",   "SCI0 receive data register (MIDI)");
    NameLoc(0xFFFF7E, "SCMR0",  "SCI0 smart card mode register");

    // --- SCI channel 1 (base H'FF80) ---
    NameLoc(0xFFFF80, "SMR1",   "SCI1 serial mode register");
    NameLoc(0xFFFF81, "BRR1",   "SCI1 bit rate register");
    NameLoc(0xFFFF82, "SCR1",   "SCI1 serial control register");
    NameLoc(0xFFFF83, "TDR1",   "SCI1 transmit data register");
    NameLoc(0xFFFF84, "SSR1",   "SCI1 serial status register");
    NameLoc(0xFFFF85, "RDR1",   "SCI1 receive data register");
    NameLoc(0xFFFF86, "SCMR1",  "SCI1 smart card mode register");

    // --- SCI channel 2 (base H'FF88) ---
    NameLoc(0xFFFF88, "SMR2",   "SCI2 serial mode register");
    NameLoc(0xFFFF89, "BRR2",   "SCI2 bit rate register");
    NameLoc(0xFFFF8A, "SCR2",   "SCI2 serial control register");
    NameLoc(0xFFFF8B, "TDR2",   "SCI2 transmit data register");
    NameLoc(0xFFFF8C, "SSR2",   "SCI2 serial status register");
    NameLoc(0xFFFF8D, "RDR2",   "SCI2 receive data register");
    NameLoc(0xFFFF8E, "SCMR2",  "SCI2 smart card mode register");

    // --- A/D converter (base H'FF90) ---
    NameLoc(0xFFFF90, "ADDRA",  "A/D data register A (16-bit, read-only)");
    NameLoc(0xFFFF92, "ADDRB",  "A/D data register B (16-bit, read-only)");
    NameLoc(0xFFFF94, "ADDRC",  "A/D data register C (16-bit, read-only)");
    NameLoc(0xFFFF96, "ADDRD",  "A/D data register D (16-bit, read-only)");
    NameLoc(0xFFFF98, "ADCSR",  "A/D control/status register");
    NameLoc(0xFFFF99, "ADCR",   "A/D control register");

    // --- Flash memory control (base H'FFA8) ---
    NameLoc(0xFFFFA8, "FLMCR1", "Flash memory control register 1");
    NameLoc(0xFFFFA9, "FLMCR2", "Flash memory control register 2");
    NameLoc(0xFFFFAA, "EBR1",   "Erase block register 1");
    NameLoc(0xFFFFAB, "EBR2",   "Erase block register 2");

    Message("H8S/2653 register names applied (source: REJ09B0331-0500 Rev5.00).\n");
}

// ---------------------------------------------------------------------------
// Exception vector table
// H8S/2600 Advanced Mode: 4-byte vectors at physical 0x000000
// ---------------------------------------------------------------------------
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

// ---------------------------------------------------------------------------
// Known functions
// ---------------------------------------------------------------------------
static LabelFunctions() {
    NameFunc(0x12A808, "ide_init",
        "Zeros device state arrays, programs EPSON SLA919F ASIC registers");
    NameFunc(0x12A956, "device_probe",
        "Top-level device probe. Contains ZIP-only gate at 0x12AA14 (patch target).");
    NameFunc(0x12AA72, "atapi_cmd_sequence_full",
        "Runs SZHC ATAPI command table from entry 0");
    NameFunc(0x12AAF2, "atapi_cmd_sequence_partial",
        "Runs SZHC ATAPI command table from START/STOP UNIT onwards");
    NameFunc(0x12ACB0, "device_validate",
        "Validates ATAPI response; dispatches on device geometry/type byte");
    NameFunc(0x12AE88, "device_classifier",
        "Classifies drive from IDENTIFY data; writes type 1/2/3 to device_type_by_slot");
    NameFunc(0x12B150, "cache_device_params",
        "Issues READ CAPACITY (0x25); stores last LBA and block length into slot arrays 0x426C42/0x426C62. Standard ATAPI only.");
    NameFunc(0x12B712, "atapi_command_handler",
        "Core ATAPI command send/receive via EPSON SLA919F");

    Message("Function names applied.\n");
}

// ---------------------------------------------------------------------------
// Patch target
// ---------------------------------------------------------------------------
static LabelPatchTarget() {
    SafeMakeName(0x12AA12, "dc_check_type1");
    MakeComm(0x12AA12, "cmp.b #1, r0l  -- test for ZIP device type (type 1)");

    SafeMakeName(0x12AA14, "dc_branch_if_not_type1");
    MakeRptCmt(0x12AA14,
        "PATCH TARGET (file offset 0x2AA14): "
        "change 46 10 (bne, rejects non-ZIP) to 40 00 (bra, allows all types). "
        "Allows HDD types 2 and 3 through the ZIP-only gate.");

    Message("Patch target labelled at 0x12AA14.\n");
}

// ---------------------------------------------------------------------------
// RAM: per-slot arrays and scalar device state
// ---------------------------------------------------------------------------
static LabelRAM() {
    MakeByteArray(0x426C82, 8, "device_type_by_slot",
        "8-slot array: 0=none, 1=ZIP, 2=HDD-small (<0x951229), 3=HDD-large (>=0x951229)");
    MakeByteArray(0x426C0A, 8, "slot_flag_A",   "8-slot flag array (semantic unconfirmed)");
    MakeByteArray(0x426C12, 8, "slot_flag_B",   "8-slot flag array (semantic unconfirmed)");
    MakeByteArray(0x426C1A, 8, "slot_flag_C",   "8-slot flag array (semantic unconfirmed)");
    MakeByteArray(0x426C22, 8, "slot_flag_D",   "8-slot flag array (semantic unconfirmed)");
    MakeByteArray(0x426C2A, 8, "slot_flag_E",   "8-slot flag array (semantic unconfirmed)");
    MakeByteArray(0x426C32, 8, "slot_media_accepted",
        "8-slot array: non-zero = device accepted for this slot");
    MakeByteArray(0x426C3A, 8, "slot_device_flags", "8-slot device flags array");

    MakeByte(0x426C8A);
    NameLoc(0x426C8A, "active_slot", "Currently active device slot index");

    MakeWord(0x40101E);
    NameLoc(0x40101E, "device_status_reg",
        "ATAPI status codes: 0x8001=not init, 0x8003=no device, 0x8007=device found, "
        "0x8008=ZIP accepted, 0x8009=unknown type, 0x800B=wrong device, 0x8015=rejected");

    MakeByte(0x426BF8); NameLoc(0x426BF8, "atapi_status_hi", "");
    MakeByte(0x426BF9); NameLoc(0x426BF9, "atapi_status_lo", "");
    MakeByte(0x426BFC); NameLoc(0x426BFC, "ide_init_done",   "Non-zero once IDE hardware initialised");
    MakeByte(0x426BFD); NameLoc(0x426BFD, "atapi_result",    "");
    MakeByte(0x426BFE); NameLoc(0x426BFE, "classify_lock",   "Guards single-entry into device_validate");

    Message("RAM labels applied.\n");
}

// ---------------------------------------------------------------------------
// ROM: strings, SZHC command table, vendor strings, error strings
// ---------------------------------------------------------------------------
static LabelROMData() {
    // Device type string table
    MakeStr(0x171ABB, BADADDR); SafeMakeName(0x171ABB, "str_dev_self");
    MakeStr(0x171AC0, BADADDR); SafeMakeName(0x171AC0, "str_dev_zip");
    MakeStr(0x171AC5, BADADDR); SafeMakeName(0x171AC5, "str_dev_hd");
    MakeStr(0x171ACA, BADADDR); SafeMakeName(0x171ACA, "str_dev_cd");
    MakeStr(0x171ACF, BADADDR); SafeMakeName(0x171ACF, "str_szhc");

    // SZHC ATAPI command table: 4 entries x 7 bytes
    SafeMakeName(0x171AD4, "szhc_cmd_table");
    MakeRptCmt(0x171AD4, "SZHC ATAPI command table: 4 entries x 7 bytes");
    MakeComm(0x171AD4, "entry 0: 06 00 00 00 00 00 00  (reset/null)");
    MakeComm(0x171ADB, "entry 1: 06 1B 00 00 00 00 00  (START/STOP UNIT)");
    MakeComm(0x171AE2, "entry 2: 06 1E 00 00 00 00 00  (PREVENT/ALLOW MEDIA REMOVAL)");
    MakeComm(0x171AE9, "entry 3: 06 03 00 00 00 00 00  (REQUEST SENSE)");

    // Vendor/product strings
    MakeStr(0x171AF0, BADADDR); SafeMakeName(0x171AF0, "str_vendor_iomega_upper");
    MakeStr(0x171AF9, BADADDR); SafeMakeName(0x171AF9, "str_vendor_iomega_lower");
    MakeStr(0x171B02, BADADDR); SafeMakeName(0x171B02, "str_product_zip");
    MakeStr(0x171B90, BADADDR); SafeMakeName(0x171B90, "str_vendor_roland");

    // Error/disk strings
    MakeStr(0x174BDF, BADADDR); SafeMakeName(0x174BDF, "str_err_not_sp808");
    MakeStr(0x174CB7, BADADDR); SafeMakeName(0x174CB7, "str_err_wrong_disk");
    MakeStr(0x174CD6, BADADDR); SafeMakeName(0x174CD6, "str_err_wrong_size");
    MakeStr(0x175233, BADADDR); SafeMakeName(0x175233, "str_media_100mb");
    MakeStr(0x175245, BADADDR); SafeMakeName(0x175245, "str_media_250mb");

    Message("ROM data labels applied.\n");
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------
static main() {
    Message("\n=== SP-808 IDA helper ===\n");
    Message("Base address : 0x%X\n", BASE_ADDRESS);
    Message("Mask ROM end : 0x%X  (code below here is not patchable from flash)\n", MASK_ROM_END);
    Message("Flash end    : 0x%X\n\n", FLASH_END);

    H8RegisterNames();
    FixupVectorTable();
    LabelFunctions();
    LabelPatchTarget();
    LabelRAM();
    LabelROMData();

    Message("\n=== Done ===\n");
    Message("Patch target : 0x12AA14  (file offset 0x2AA14)\n");
    Message("  Original   : 46 10  (bne +0x10, rejects non-ZIP devices)\n");
    Message("  Patched    : 40 00  (bra +0x00, allows all classified devices)\n");
    Message("\nDSP interface notes:\n");
    Message("  TC170C140AF (IC11) selected via HC138 (IC10) chip select decode.\n");
    Message("  HC138 enabled when CS3 (PGDR bit) is asserted.\n");
    Message("  HC138 A/B/C inputs driven by P2DR (0xFFFF61) bits 0/5/6.\n");
    Message("  Search for writes to P2DR to find DSP communication code.\n");
    Message("  CS3 address window: read BCRL (0xFFFED5) from firmware init.\n");
}
