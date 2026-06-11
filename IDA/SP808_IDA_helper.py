"""
SP808_IDA_helper.py — IDA Pro analysis script for Roland SP-808 firmware

Load SP8EXall.bin with:
  Processor : H8/300H Advanced (H8S/2653)
  Load base : 0x100000
  ROM type  : binary

Then run this script via File > Script file.

All IDA addresses are runtime addresses (file offset + 0x100000).
Conversion: file_offset = ida_address - 0x100000

Register addresses are taken directly from the H8S/2655 Group Hardware Manual
(Renesas REJ09B0331-0500, Rev 5.00, Sep 2006). The H8S/2653 and H8S/2655 share
the same internal I/O register map. All three-source conflicts in prior versions
of this script have been resolved against that datasheet.

Authors: hsiboy, Professor_jonny
"""

from idc import *
from idaapi import *
from idautils import *
import idc
import idaapi
import idautils

BASE      = 0x100000   # IDA load base = external flash runtime address
FLASH_END = 0x1C0004
MASK_ROM_END = 0x00E800  # Code below here is not patchable from flash image


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def set_name_safe(ea, name, comment=""):
    """Rename address only if the name is not already taken at a different address."""
    existing = idc.get_name_ea_simple(name)
    if existing != idc.BADADDR and existing != ea:
        print(f"  SKIP rename {name!r}: already used at 0x{existing:X}")
        return
    idc.set_name(ea, name, idc.SN_NOWARN | idc.SN_NOCHECK)
    if comment:
        idc.set_cmt(ea, comment, 0)


def make_array_bytes(ea, count, name, comment=""):
    for i in range(count):
        idc.create_byte(ea + i)
    set_name_safe(ea, name, comment)


# ---------------------------------------------------------------------------
# H8S/2653 internal I/O register names
# All addresses from H8S/2655 Group Hardware Manual REJ09B0331-0500 Rev5.00
# The H8S/2653 and H8S/2655 share the same internal I/O register map.
#
# Address format in the datasheet is H'xxxx (lower 16 bits).
# Full 24-bit runtime address = 0xFF0000 | lower16 for the I/O space.
# ---------------------------------------------------------------------------

H8S_REGISTERS = [

    # --- Interrupt controller (H'FEC0 base) ---
    (0xFFFEC0, "ICRA",   "Interrupt control register A"),
    (0xFFFEC1, "ICRB",   "Interrupt control register B"),
    (0xFFFEC2, "ICRC",   "Interrupt control register C"),
    (0xFFFEC4, "IPRA",   "Interrupt priority register A"),
    (0xFFFEC5, "IPRB",   "Interrupt priority register B"),
    (0xFFFEC6, "IPRC",   "Interrupt priority register C"),
    (0xFFFEC7, "IPRD",   "Interrupt priority register D"),
    (0xFFFEC8, "IPRE",   "Interrupt priority register E"),
    (0xFFFEC9, "IPRF",   "Interrupt priority register F"),
    (0xFFFECA, "IPRG",   "Interrupt priority register G"),
    (0xFFFECB, "IPRH",   "Interrupt priority register H"),
    (0xFFFECC, "IPRI",   "Interrupt priority register I"),
    (0xFFFECD, "IPRJ",   "Interrupt priority register J"),
    (0xFFFECE, "IPRK",   "Interrupt priority register K"),

    # --- Bus controller (H'FED0 base) ---
    (0xFFFED0, "ABWCR",  "Bus width control register — sets 8/16-bit access per area"),
    (0xFFFED1, "ASTCR",  "Access state control register — idle cycle insertion per area"),
    (0xFFFED2, "WCRH",   "Wait control register H — wait states for areas 4-7"),
    (0xFFFED3, "WCRL",   "Wait control register L — wait states for areas 0-3"),
    (0xFFFED4, "BCRH",   "Bus control register H — DRAM/burst/ICIS config. Reset=H'D0"),
    (0xFFFED5, "BCRL",   "Bus control register L — EAE/WAITE/WDBE flags. Reset=H'3C"),
    (0xFFFED6, "MCR",    "Memory control register"),
    (0xFFFED7, "DRAMCR", "DRAM control register"),

    # --- GPIO data direction registers (write-only, H'FEB0 base) ---
    # Writing 1 to a bit configures the corresponding pin as output.
    (0xFFFEB0, "P1DDR",  "Port 1 DDR (write-only) — A0-A7 alternate"),
    (0xFFFEB1, "P2DDR",  "Port 2 DDR (write-only) — A8-A15 alternate. "
                          "Bits 0/5/6 drive HC138 A/B/C for DSP chip select steering."),
    (0xFFFEB2, "P3DDR",  "Port 3 DDR (write-only) — SCI TxD/RxD/SCK alternate"),
    (0xFFFEB4, "P5DDR",  "Port 5 DDR (write-only) — A16-A19/SCI2 alternate"),
    (0xFFFEB5, "P6DDR",  "Port 6 DDR (write-only)"),
    (0xFFFEB9, "PADDR",  "Port A DDR (write-only) — A20-A23/PPG alternate"),
    (0xFFFEBA, "PBDDR",  "Port B DDR (write-only) — D0-D7 alternate"),
    (0xFFFEBB, "PCDDR",  "Port C DDR (write-only) — D8-D15 alternate"),
    (0xFFFEBC, "PDDDR",  "Port D DDR (write-only) — DMAC/PPG alternate"),
    (0xFFFEBD, "PEDDR",  "Port E DDR (write-only) — PWM/GPIO"),
    (0xFFFEBE, "PFDDR",  "Port F DDR (write-only) — AS/RD/HWR/LWR/CLK/WAIT system bus"),
    (0xFFFEBF, "PGDDR",  "Port G DDR (write-only) — CS0-CS3 chip selects. "
                          "PG2=CS2 (EPSON ASIC), PG4=CS0 (flash). "
                          "CS3 enables HC138 G2A/G2B for DSP chip select decode."),

    # --- GPIO data registers (read/write output latch, H'FF60 base) ---
    (0xFFFF60, "P1DR",   "Port 1 data register"),
    (0xFFFF61, "P2DR",   "Port 2 data register — bits 0/5/6 steer HC138 A/B/C "
                          "to select DSP chip select line (CS1-CS7 on IC10). "
                          "Write before accessing DSP address window."),
    (0xFFFF62, "P3DR",   "Port 3 data register — SCI TxD/RxD/SCK"),
    (0xFFFF64, "P5DR",   "Port 5 data register — A16-A19"),
    (0xFFFF65, "P6DR",   "Port 6 data register"),
    (0xFFFF69, "PADR",   "Port A data register — A20-A23"),
    (0xFFFF6A, "PBDR",   "Port B data register — D0-D7"),
    (0xFFFF6B, "PCDR",   "Port C data register — D8-D15"),
    (0xFFFF6C, "PDDR",   "Port D data register"),
    (0xFFFF6D, "PEDR",   "Port E data register"),
    (0xFFFF6E, "PFDR",   "Port F data register — system bus control outputs"),
    (0xFFFF6F, "PGDR",   "Port G data register — CS0-CS3. "
                          "CS3 bit drives HC138 enable for DSP chip select decode."),

    # --- GPIO pin state registers (read-only, H'FF50 base) ---
    (0xFFFF50, "PORT1",  "Port 1 pin state (read-only)"),
    (0xFFFF51, "PORT2",  "Port 2 pin state (read-only)"),
    (0xFFFF52, "PORT3",  "Port 3 pin state (read-only)"),
    (0xFFFF53, "PORT4",  "Port 4 pin state (read-only)"),
    (0xFFFF54, "PORT5",  "Port 5 pin state (read-only)"),
    (0xFFFF55, "PORT6",  "Port 6 pin state (read-only)"),
    (0xFFFF59, "PORTA",  "Port A pin state (read-only)"),
    (0xFFFF5A, "PORTB",  "Port B pin state (read-only)"),
    (0xFFFF5B, "PORTC",  "Port C pin state (read-only)"),
    (0xFFFF5C, "PORTD",  "Port D pin state (read-only)"),
    (0xFFFF5D, "PORTE",  "Port E pin state (read-only)"),
    (0xFFFF5E, "PORTF",  "Port F pin state (read-only)"),
    (0xFFFF5F, "PORTG",  "Port G pin state (read-only)"),

    # --- IRQ control (H'FF2C base) ---
    (0xFFFF2C, "ISCRH",  "IRQ sense control register H"),
    (0xFFFF2D, "ISCRL",  "IRQ sense control register L"),
    (0xFFFF2E, "IER",    "IRQ enable register"),
    (0xFFFF2F, "ISR",    "IRQ status register"),

    # --- System control (H'FF38 base) ---
    (0xFFFF38, "SBYCR",   "Standby control register"),
    (0xFFFF39, "SYSCR",   "System control register"),
    (0xFFFF3A, "SCKCR",   "System clock control register"),
    (0xFFFF3B, "MDCR",    "Mode control register (read-only)"),
    (0xFFFF3C, "MSTPCRH", "Module stop control register H"),
    (0xFFFF3D, "MSTPCRL", "Module stop control register L"),

    # --- Timer pulse unit: start/sync (H'FFC0) ---
    (0xFFFFC0, "TSTR",   "Timer start register — enables TPU channel counters"),
    (0xFFFFC1, "TSYR",   "Timer synchro register"),

    # --- SCI channel 0 — MIDI IN/OUT (H'FF78) ---
    (0xFFFF78, "SMR0",   "SCI0 serial mode register — MIDI"),
    (0xFFFF79, "BRR0",   "SCI0 bit rate register — MIDI"),
    (0xFFFF7A, "SCR0",   "SCI0 serial control register — MIDI"),
    (0xFFFF7B, "TDR0",   "SCI0 transmit data register — MIDI"),
    (0xFFFF7C, "SSR0",   "SCI0 serial status register — MIDI"),
    (0xFFFF7D, "RDR0",   "SCI0 receive data register — MIDI"),
    (0xFFFF7E, "SCMR0",  "SCI0 smart card mode register"),

    # --- SCI channel 1 (H'FF80) ---
    (0xFFFF80, "SMR1",   "SCI1 serial mode register"),
    (0xFFFF81, "BRR1",   "SCI1 bit rate register"),
    (0xFFFF82, "SCR1",   "SCI1 serial control register"),
    (0xFFFF83, "TDR1",   "SCI1 transmit data register"),
    (0xFFFF84, "SSR1",   "SCI1 serial status register"),
    (0xFFFF85, "RDR1",   "SCI1 receive data register"),
    (0xFFFF86, "SCMR1",  "SCI1 smart card mode register"),

    # --- SCI channel 2 (H'FF88) ---
    (0xFFFF88, "SMR2",   "SCI2 serial mode register"),
    (0xFFFF89, "BRR2",   "SCI2 bit rate register"),
    (0xFFFF8A, "SCR2",   "SCI2 serial control register"),
    (0xFFFF8B, "TDR2",   "SCI2 transmit data register"),
    (0xFFFF8C, "SSR2",   "SCI2 serial status register"),
    (0xFFFF8D, "RDR2",   "SCI2 receive data register"),
    (0xFFFF8E, "SCMR2",  "SCI2 smart card mode register"),

    # --- A/D converter (H'FF90 base) ---
    (0xFFFF90, "ADDRA",  "A/D data register A (16-bit, read-only)"),
    (0xFFFF92, "ADDRB",  "A/D data register B (16-bit, read-only)"),
    (0xFFFF94, "ADDRC",  "A/D data register C (16-bit, read-only)"),
    (0xFFFF96, "ADDRD",  "A/D data register D (16-bit, read-only)"),
    (0xFFFF98, "ADCSR",  "A/D control/status register"),
    (0xFFFF99, "ADCR",   "A/D control register"),

    # --- Flash memory control (H'FFA8) ---
    (0xFFFFA8, "FLMCR1", "Flash memory control register 1"),
    (0xFFFFA9, "FLMCR2", "Flash memory control register 2"),
    (0xFFFFAA, "EBR1",   "Erase block register 1"),
    (0xFFFFAB, "EBR2",   "Erase block register 2"),
]


# ---------------------------------------------------------------------------
# Known functions
# ---------------------------------------------------------------------------

FUNCTIONS = [
    (0x12A808, "ide_init",
        "Zeros device state arrays, programs EPSON SLA919F ASIC registers"),
    (0x12A956, "device_probe",
        "Top-level device probe. Contains ZIP-only gate at 0x12AA14 (patch target)."),
    (0x12AA72, "atapi_cmd_sequence_full",
        "Runs SZHC ATAPI command table from entry 0"),
    (0x12AAF2, "atapi_cmd_sequence_partial",
        "Runs SZHC ATAPI command table from START/STOP UNIT onwards"),
    (0x12ACB0, "device_validate",
        "Validates ATAPI response; dispatches on device geometry/type byte"),
    (0x12AE88, "device_classifier",
        "Classifies drive from IDENTIFY data; writes type 1/2/3 to device_type_by_slot"),
    (0x12B150, "cache_device_params",
        "Issues READ CAPACITY (0x25); stores last LBA and block length into "
        "slot arrays 0x426C42/0x426C62. Standard ATAPI only — no Iomega-specific commands."),
    (0x12B712, "atapi_command_handler",
        "Core ATAPI command send/receive via EPSON SLA919F"),
]


# ---------------------------------------------------------------------------
# Named locations
# ---------------------------------------------------------------------------

NAMES = [
    # --- Patch target ---
    (0x12AA12, "dc_check_type1",
        "cmp.b #1, r0l — test for ZIP device type (type 1)"),
    (0x12AA14, "dc_branch_if_not_type1",
        "PATCH TARGET (file offset 0x2AA14): "
        "change 46 10 (bne, rejects non-ZIP) to 40 00 (bra, allows all types). "
        "Allows HDD types 2 and 3 through the ZIP-only gate."),

    # --- RAM: scalars ---
    (0x426C8A, "active_slot",
        "Currently active device slot index"),
    (0x40101E, "device_status_reg",
        "ATAPI status codes: 0x8001=not init, 0x8003=no device, 0x8007=device found, "
        "0x8008=success/ZIP accepted, 0x8009=unknown type, 0x800B=wrong device, "
        "0x8015=rejected"),
    (0x426BF8, "atapi_status_hi",   ""),
    (0x426BF9, "atapi_status_lo",   ""),
    (0x426BFC, "ide_init_done",     "Non-zero once IDE hardware initialised"),
    (0x426BFD, "atapi_result",      ""),
    (0x426BFE, "classify_lock",     "Guards single-entry into device_validate"),

    # --- ROM: device/vendor/product strings ---
    (0x171ABB, "str_dev_self",             "SELF"),
    (0x171AC0, "str_dev_zip",              "ZIP "),
    (0x171AC5, "str_dev_hd",               "HD  "),
    (0x171ACA, "str_dev_cd",               "CD  "),
    (0x171ACF, "str_szhc",                 "-SZHC"),
    (0x171AF0, "str_vendor_iomega_upper",  "IOMEGA  "),
    (0x171AF9, "str_vendor_iomega_lower",  "iomega  "),
    (0x171B02, "str_product_zip",          "ZIP"),
    (0x171B90, "str_vendor_roland",        "Roland  "),

    # --- ROM: filesystem/disk error strings ---
    (0x174BDF, "str_err_not_sp808",   "Not SP-808 Disk."),
    (0x174CB7, "str_err_wrong_disk",  "Wrong Disk."),
    (0x174CD6, "str_err_wrong_size",  "Wrong Media Size."),
    (0x175233, "str_media_100mb",     "SP808 100MB Disk."),
    (0x175245, "str_media_250mb",     "SP808EX 250MB Disk."),
]


# ---------------------------------------------------------------------------
# Per-slot RAM arrays (8 bytes each, indexed by slot 0-7)
# ---------------------------------------------------------------------------

SLOT_ARRAYS = [
    (0x426C82, "device_type_by_slot",
        "8-slot array: 0=none, 1=ZIP, 2=HDD-small (<0x951229), 3=HDD-large (>=0x951229)"),
    (0x426C0A, "slot_flag_A",   "8-slot flag array (semantic meaning unconfirmed)"),
    (0x426C12, "slot_flag_B",   "8-slot flag array (semantic meaning unconfirmed)"),
    (0x426C1A, "slot_flag_C",   "8-slot flag array (semantic meaning unconfirmed)"),
    (0x426C22, "slot_flag_D",   "8-slot flag array (semantic meaning unconfirmed)"),
    (0x426C2A, "slot_flag_E",   "8-slot flag array (semantic meaning unconfirmed)"),
    (0x426C32, "slot_media_accepted",
        "8-slot array: non-zero = device accepted for this slot"),
    (0x426C3A, "slot_device_flags", "8-slot device flags array"),
]


# ---------------------------------------------------------------------------
# ATAPI command table (SZHC): 4 entries x 7 bytes, base 0x171AD4
# ---------------------------------------------------------------------------

ATAPI_CMDS = [
    (0x171AD4, 0x00, "reset/null"),
    (0x171ADB, 0x1B, "START/STOP UNIT"),
    (0x171AE2, 0x1E, "PREVENT/ALLOW MEDIA REMOVAL"),
    (0x171AE9, 0x03, "REQUEST SENSE"),
]


# ---------------------------------------------------------------------------
# Known ASCII string literals in ROM
# ---------------------------------------------------------------------------

STRING_LOCS = [
    (0x171ABB, 4,  "SELF"),
    (0x171AC0, 4,  "ZIP "),
    (0x171AC5, 4,  "HD  "),
    (0x171ACA, 4,  "CD  "),
    (0x171ACF, 5,  "-SZHC"),
    (0x171AF0, 8,  "IOMEGA  "),
    (0x171AF9, 8,  "iomega  "),
    (0x171B02, 3,  "ZIP"),
    (0x171B90, 8,  "Roland  "),
    (0x174BDF, 16, "Not SP-808 Disk."),
    (0x174CB7, 11, "Wrong Disk."),
    (0x174CD6, 17, "Wrong Media Size."),
    (0x175233, 17, "SP808 100MB Disk."),
    (0x175245, 19, "SP808EX 250MB Disk."),
]


# ---------------------------------------------------------------------------
# Exception vector table
# H8S/2600 Advanced Mode: 4-byte vectors starting at 0x000000
# ---------------------------------------------------------------------------

VECTORS = [
    (0x000000, "vec_power_on_reset"),
    (0x000004, "vec_manual_reset"),
    (0x00001C, "vec_nmi"),
    (0x000020, "vec_trap0"),
    (0x000024, "vec_trap1"),
    (0x000028, "vec_trap2"),
    (0x00002C, "vec_trap3"),
    (0x000040, "vec_irq0"),
    (0x000044, "vec_irq1"),
    (0x000048, "vec_irq2"),
    (0x00004C, "vec_irq3"),
    (0x000050, "vec_irq4"),
    (0x000054, "vec_irq5"),
    (0x000058, "vec_irq6"),
    (0x00005C, "vec_irq7"),
]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("\n=== SP-808 IDA helper ===")
    print(f"Base address  : 0x{BASE:X}")
    print(f"Mask ROM end  : 0x{MASK_ROM_END:X}  (code below here is not patchable)")
    print(f"Flash end     : 0x{FLASH_END:X}\n")

    # 1. H8S/2653 internal I/O registers
    # Addresses from H8S/2655 Group HW Manual REJ09B0331-0500 Rev5.00
    print("Applying H8S/2653 register names (authoritative from datasheet)...")
    for ea, name, comment in H8S_REGISTERS:
        idc.create_byte(ea)
        set_name_safe(ea, name, comment)

    # 2. Exception vector table
    print("Processing exception vector table...")
    for i in range(0, 0x170, 4):
        idc.create_dword(i)
        idc.op_plain_offset(i, 0, 0)
        target = idc.get_wide_dword(i) & 0x00FFFFFF
        if BASE <= target < FLASH_END:
            idc.create_insn(target)
            idc.auto_mark_range(target, target + 2, idc.AU_PROC)
    for ea, name in VECTORS:
        set_name_safe(ea, name)

    # 3. Known functions
    print("Applying function names...")
    for ea, name, comment in FUNCTIONS:
        idc.create_insn(ea)
        idc.add_func(ea, idc.BADADDR)
        set_name_safe(ea, name, comment)

    # 4. Named locations and scalars
    print("Applying named locations...")
    for ea, name, comment in NAMES:
        set_name_safe(ea, name, comment)

    # 5. Per-slot RAM arrays
    print("Defining slot arrays...")
    for ea, name, comment in SLOT_ARRAYS:
        make_array_bytes(ea, 8, name, comment)

    # 6. ATAPI command table entries
    print("Marking ATAPI command table entries...")
    set_name_safe(0x171AD4, "szhc_cmd_table",
        "SZHC ATAPI command table: 4 entries x 7 bytes at 0x171AD4")
    for ea, cmd, desc in ATAPI_CMDS:
        for i in range(7):
            idc.create_byte(ea + i)
        idc.set_cmt(ea,     "marker (0x06)", 0)
        idc.set_cmt(ea + 1, f"command 0x{cmd:02X}: {desc}", 0)
        for i in range(2, 7):
            idc.set_cmt(ea + i, "param", 0)

    # 7. ROM string literals
    print("Marking ROM string literals...")
    for ea, length, content in STRING_LOCS:
        idc.create_strlit(ea, ea + length + 1, idc.STRTYPE_C)

    # 8. Patch target prominent comment
    idc.set_cmt(0x12AA14,
        "PATCH TARGET: change 46 10 (bne) to 40 00 (bra) to allow HDD types 2/3 "
        "through the ZIP-only gate. File offset 0x2AA14.", 1)

    print("\n=== Done ===")
    print("Patch target : 0x12AA14  (file offset 0x2AA14)")
    print("  Original   : 46 10  (bne +0x10, rejects non-ZIP)")
    print("  Patched    : 40 00  (bra +0x00, allows all classified devices)")
    print()
    print("DSP interface notes:")
    print("  TC170C140AF (IC11) is selected via HC138 (IC10) chip select decode.")
    print("  HC138 is enabled when CS3 (PG bit) is asserted.")
    print("  HC138 A/B/C inputs driven by P2DR bits 0/5/6 (P20, P25, P26).")
    print("  Search for writes to P2DR (0xFFFF61) to find DSP communication code.")
    print("  CS3 address window: read BCRL (0xFFFED5) EAE/area bits from firmware init.")


if __name__ == "__main__":
    main()
