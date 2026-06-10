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
// Authors: hsiboy, Professor_jonny
//

#include <idc.idc>

#define BASE_ADDRESS    0x100000
#define MASK_ROM_END    0x00E800
#define FLASH_END       0x1C0004

// Apply a name only if the location does not already have a meaningful name.
static SafeMakeName(ea, name) {
    auto existing;
    if (ea == BADADDR) return;
    existing = Name(ea);
    if (existing == "" ||
        strstr(existing, "sub_")  == 0 ||
        strstr(existing, "unk_")  == 0 ||
        strstr(existing, "off_")  == 0 ||
        strstr(existing, "byte_") == 0 ||
        strstr(existing, "word_") == 0 ||
        strstr(existing, "dword_")== 0) {
        MakeNameEx(ea, name, SN_NOWARN);
    }
}

// Define a byte array of 'count' bytes and name it.
static MakeByteArray(ea, count, name) {
    auto i;
    for (i = 0; i < count; i++)
        MakeByte(ea + i);
    MakeArray(ea, count);
    SafeMakeName(ea, name);
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
// ---------------------------------------------------------------------------
static H8RegisterNames() {
    // Interrupt controller
    SafeMakeName(0xFFEC00, "INTC_ICRA");
    SafeMakeName(0xFFEC01, "INTC_ICRB");
    SafeMakeName(0xFFEC02, "INTC_ICRC");
    SafeMakeName(0xFFEC04, "INTC_IPRA");
    SafeMakeName(0xFFEC05, "INTC_IPRB");
    SafeMakeName(0xFFEC06, "INTC_IPRC");
    SafeMakeName(0xFFEC07, "INTC_IPRD");
    SafeMakeName(0xFFEC08, "INTC_IPRE");
    SafeMakeName(0xFFEC09, "INTC_IPRF");
    SafeMakeName(0xFFEC0A, "INTC_IPRG");
    SafeMakeName(0xFFEC0B, "INTC_IPRH");
    SafeMakeName(0xFFEC0C, "INTC_IPRI");
    SafeMakeName(0xFFEC0D, "INTC_IPRJ");
    SafeMakeName(0xFFEC0E, "INTC_IPRK");

    // Bus controller
    SafeMakeName(0xFFED00, "ABWCR");
    SafeMakeName(0xFFED01, "ASTCR");
    SafeMakeName(0xFFED02, "WCRH");
    SafeMakeName(0xFFED03, "WCRL");
    SafeMakeName(0xFFED04, "BCRH");
    SafeMakeName(0xFFED05, "BCRL");
    SafeMakeName(0xFFED06, "MCR");
    SafeMakeName(0xFFED07, "DRAMCR");
    SafeMakeName(0xFFED08, "RTCNT");
    SafeMakeName(0xFFED09, "RTCOR");

    // System control
    SafeMakeName(0xFFFF38, "SBYCR");
    SafeMakeName(0xFFFF39, "SYSCR");
    SafeMakeName(0xFFFF3A, "SCKCR");
    SafeMakeName(0xFFFF3B, "MDCR");
    SafeMakeName(0xFFFF3C, "MSTPCRH");
    SafeMakeName(0xFFFF3D, "MSTPCRL");

    // SCI channel 0 (MIDI)
    SafeMakeName(0xFFFF78, "SMR0");
    SafeMakeName(0xFFFF79, "BRR0");
    SafeMakeName(0xFFFF7A, "SCR0");
    SafeMakeName(0xFFFF7B, "TDR0");
    SafeMakeName(0xFFFF7C, "SSR0");
    SafeMakeName(0xFFFF7D, "RDR0");
    SafeMakeName(0xFFFF7E, "SCMR0");

    // SCI channel 1 (debug / CN7)
    SafeMakeName(0xFFFF80, "SMR1");
    SafeMakeName(0xFFFF81, "BRR1");
    SafeMakeName(0xFFFF82, "SCR1");
    SafeMakeName(0xFFFF83, "TDR1");
    SafeMakeName(0xFFFF84, "SSR1");
    SafeMakeName(0xFFFF85, "RDR1");
    SafeMakeName(0xFFFF86, "SCMR1");

    // SCI channel 2
    SafeMakeName(0xFFFF88, "SMR2");
    SafeMakeName(0xFFFF89, "BRR2");
    SafeMakeName(0xFFFF8A, "SCR2");
    SafeMakeName(0xFFFF8B, "TDR2");
    SafeMakeName(0xFFFF8C, "SSR2");
    SafeMakeName(0xFFFF8D, "RDR2");

    // Port data direction
    SafeMakeName(0xFFFEB0, "P1DDR");
    SafeMakeName(0xFFFEB1, "P2DDR");

    // Timer
    SafeMakeName(0xFFFFB0, "TCR0");
    SafeMakeName(0xFFFFB2, "TCSR0");
    SafeMakeName(0xFFFFB4, "TCORA0");

    Message("H8S/2653 register names applied.\n");
}

// ---------------------------------------------------------------------------
// Exception vector table
// H8S/2600 Advanced Mode: vectors at 0x000000, 4 bytes each
// ---------------------------------------------------------------------------
static FixupVectorTable() {
    auto i, target;

    Message("Processing exception vector table...\n");

    // Vectors 0x00 to 0x16F (92 vectors x 4 bytes)
    for (i = 0x000000; i < 0x000170; i = i + 4) {
        MakeDword(i);
        OpOff(i, 0, 0);
        target = Dword(i) & 0x00FFFFFF;  // H8S: upper byte ignored
        if (target >= BASE_ADDRESS && target < FLASH_END) {
            MakeCode(target);
            AutoMark(target, AU_PROC);
        }
    }

    // Named vectors
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
        "Top-level device probe. Contains ZIP-only gate at 0x12AA14 (patch target)");
    NameFunc(0x12AA72, "atapi_cmd_sequence_full",
        "Runs SZHC ATAPI command table from entry 0 (06 00 00 00 00 00 00)");
    NameFunc(0x12AAF2, "atapi_cmd_sequence_partial",
        "Runs SZHC ATAPI command table from START/STOP UNIT onwards");
    NameFunc(0x12ACB0, "device_validate",
        "Validates ATAPI response; dispatches on device geometry/type byte");
    NameFunc(0x12AE88, "device_classifier",
        "Classifies drive from IDENTIFY data; writes type 1/2/3 to device_type_by_slot");
    NameFunc(0x12B150, "zip_device_init",
        "Post-classification device init (originally ZIP-specific; review for HDD compat)");
    NameFunc(0x12B712, "atapi_command_handler",
        "Core ATAPI command send/receive via EPSON SLA919F");

    Message("Function names applied.\n");
}

// ---------------------------------------------------------------------------
// Patch target labels
// ---------------------------------------------------------------------------
static LabelPatchTarget() {
    SafeMakeName(0x12AA12, "dc_check_type1");
    MakeComm(0x12AA12, "cmp.b #1, r0l  -- test for ZIP device type (type 1)");

    SafeMakeName(0x12AA14, "dc_branch_if_not_type1");
    MakeComm(0x12AA14,
        "PATCH TARGET (file offset 0x2AA14): "
        "change 46 10 (bne, rejects non-ZIP) to 40 00 (bra, allows all types). "
        "Allows HDD types 2 and 3 through the ZIP-only gate.");

    Message("Patch target labelled at 0x12AA14.\n");
}

// ---------------------------------------------------------------------------
// RAM: per-slot arrays and scalar device state
// ---------------------------------------------------------------------------
static LabelRAM() {
    // Per-slot arrays (8 bytes each, indexed by slot number 0-7)
    MakeByteArray(0x426C82, 8, "device_type_by_slot");
    MakeComm(0x426C82, "type codes: 0=none, 1=ZIP, 2=HDD-small, 3=HDD-large");

    MakeByteArray(0x426C0A, 8, "slot_flag_A");
    MakeByteArray(0x426C12, 8, "slot_flag_B");
    MakeByteArray(0x426C1A, 8, "slot_flag_C");
    MakeByteArray(0x426C22, 8, "slot_flag_D");
    MakeByteArray(0x426C2A, 8, "slot_flag_E");
    MakeByteArray(0x426C32, 8, "slot_media_accepted");
    MakeComm(0x426C32, "non-zero = device accepted for this slot");
    MakeByteArray(0x426C3A, 8, "slot_device_flags");

    // Scalars
    MakeByte(0x426C8A);  SafeMakeName(0x426C8A, "active_slot");
    MakeWord(0x40101E);  SafeMakeName(0x40101E, "device_status_reg");
    MakeComm(0x40101E,
        "ATAPI status codes: "
        "0x8001=not init, 0x8003=no device, 0x8007=device found, "
        "0x8008=success/ZIP accepted, 0x8009=unknown type, "
        "0x800B=wrong device, 0x8015=rejected");
    MakeByte(0x426BF8);  SafeMakeName(0x426BF8, "atapi_status_hi");
    MakeByte(0x426BF9);  SafeMakeName(0x426BF9, "atapi_status_lo");
    MakeByte(0x426BFC);  SafeMakeName(0x426BFC, "ide_init_done");
    MakeByte(0x426BFD);  SafeMakeName(0x426BFD, "atapi_result");
    MakeByte(0x426BFE);  SafeMakeName(0x426BFE, "classify_lock");

    Message("RAM labels applied.\n");
}

// ---------------------------------------------------------------------------
// ROM: device type strings, vendor strings, SZHC table, error strings
// ---------------------------------------------------------------------------
static LabelROMData() {
    // Device type string table (0x171ABB)
    MakeStr(0x171ABB, BADADDR); SafeMakeName(0x171ABB, "str_dev_self");
    MakeStr(0x171AC0, BADADDR); SafeMakeName(0x171AC0, "str_dev_zip");
    MakeStr(0x171AC5, BADADDR); SafeMakeName(0x171AC5, "str_dev_hd");
    MakeStr(0x171ACA, BADADDR); SafeMakeName(0x171ACA, "str_dev_cd");
    MakeStr(0x171ACF, BADADDR); SafeMakeName(0x171ACF, "str_szhc");

    // SZHC ATAPI command table (4 x 7-byte entries, base 0x171AD4)
    SafeMakeName(0x171AD4, "szhc_cmd_table");
    MakeComm(0x171AD4, "SZHC ATAPI command table: 4 entries x 7 bytes");
    MakeComm(0x171AD4, "entry 0: 06 00 00 00 00 00 00  (reset/null)");
    MakeComm(0x171ADB, "entry 1: 06 1B 00 00 00 00 00  (START/STOP UNIT)");
    MakeComm(0x171AE2, "entry 2: 06 1E 00 00 00 00 00  (PREVENT/ALLOW MEDIA REMOVAL)");
    MakeComm(0x171AE9, "entry 3: 06 03 00 00 00 00 00  (REQUEST SENSE)");

    // Vendor/product strings
    MakeStr(0x171AF0, BADADDR); SafeMakeName(0x171AF0, "str_vendor_iomega_upper");
    MakeStr(0x171AF9, BADADDR); SafeMakeName(0x171AF9, "str_vendor_iomega_lower");
    MakeStr(0x171B02, BADADDR); SafeMakeName(0x171B02, "str_product_zip");
    MakeStr(0x171B90, BADADDR); SafeMakeName(0x171B90, "str_vendor_roland");

    // Filesystem/disk strings
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
    Message("Mask ROM end : 0x%X (code below here is not patchable)\n", MASK_ROM_END);
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
}
