"""
SP808_IDA_helper.py — IDA Pro analysis script for Roland SP-808 firmware

Load SP8EXall.bin with:
  Processor : H8/300H Advanced (H8S/2653)
  Load base : 0x100000
  ROM type  : binary

Then run this script via File > Script file.

All IDA addresses are runtime addresses (file offset + 0x100000).
Conversion: file_offset = ida_address - 0x100000
"""

from idc import *
from idaapi import *
from idautils import *
import idc
import idaapi
import idautils

BASE = 0x100000   # IDA load base = external flash runtime address


# ---------------------------------------------------------------------------
# Named locations — (ida_address, name, comment)
# ---------------------------------------------------------------------------

NAMES = [
    # --- Functions ---
    (0x12A808, "ide_init",                    "Zeros device state arrays, programs ASIC registers"),
    (0x12A956, "device_probe",                "Top-level device probe; contains ZIP-only gate at 0x12AA14"),
    (0x12AA72, "atapi_cmd_sequence_full",     "Runs SZHC command table from entry 0 (06 00...)"),
    (0x12AAF2, "atapi_cmd_sequence_partial",  "Runs SZHC command table from START/STOP UNIT onwards"),
    (0x12ACB0, "device_validate",             "Validates ATAPI response, dispatches on device geometry/type"),
    (0x12AE88, "device_classifier",           "Classifies drive; writes type 1/2/3 to device_type_by_slot"),
    (0x12B150, "zip_device_init",             "Post-classification init (originally ZIP-specific; review for HDD)"),
    (0x12B712, "atapi_command_handler",       "Core ATAPI command send/receive"),

    # --- Patch target ---
    (0x12AA12, "dc_check_type1",              "cmp.b #1, r0l — test for ZIP device type"),
    (0x12AA14, "dc_branch_if_not_type1",      "bne — rejects non-ZIP; PATCH TARGET (46 10 -> 40 00)"),

    # --- RAM: per-slot arrays (8 bytes each, indexed by slot number) ---
    (0x426C82, "device_type_by_slot",         "8-slot array: 0=none 1=ZIP 2=HDD-small 3=HDD-large"),
    (0x426C0A, "slot_flag_A",                 "8-slot flag array"),
    (0x426C12, "slot_flag_B",                 "8-slot flag array"),
    (0x426C1A, "slot_flag_C",                 "8-slot flag array"),
    (0x426C22, "slot_flag_D",                 "8-slot flag array"),
    (0x426C2A, "slot_flag_E",                 "8-slot flag array"),
    (0x426C32, "slot_media_accepted",         "8-slot array: non-zero = device accepted for this slot"),
    (0x426C3A, "slot_device_flags",           "8-slot device flags array"),

    # --- RAM: scalars ---
    (0x426C8A, "active_slot",                 "Currently active device slot index"),
    (0x40101E, "device_status_reg",           "ATAPI command status codes (0x8001/8003/8007/8008/800B/8015)"),
    (0x426BF8, "atapi_status_hi",             ""),
    (0x426BF9, "atapi_status_lo",             ""),
    (0x426BFC, "ide_init_done",               "Non-zero once IDE hardware initialised"),
    (0x426BFD, "atapi_result",                ""),
    (0x426BFE, "classify_lock",               "Guards single-entry into device_validate"),

    # --- ROM: device/vendor strings ---
    (0x171ABB, "str_dev_self",                "SELF"),
    (0x171AC0, "str_dev_zip",                 "ZIP "),
    (0x171AC5, "str_dev_hd",                  "HD  "),
    (0x171ACA, "str_dev_cd",                  "CD  "),
    (0x171ACF, "str_szhc",                    "-SZHC"),
    (0x171AF0, "str_vendor_iomega_upper",     "IOMEGA  "),
    (0x171AF9, "str_vendor_iomega_lower",     "iomega  "),
    (0x171B02, "str_product_zip",             "ZIP"),

    # --- ROM: filesystem/disk strings ---
    (0x171B90, "str_vendor_roland",           "Roland  "),
    (0x174BDF, "str_err_not_sp808",           "Not SP-808 Disk."),
    (0x174CB7, "str_err_wrong_disk",          "Wrong Disk."),
    (0x174CD6, "str_err_wrong_size",          "Wrong Media Size."),
    (0x175233, "str_media_100mb",             "SP808 100MB Disk."),
    (0x175245, "str_media_250mb",             "SP808EX 250MB Disk."),
]


# ---------------------------------------------------------------------------
# ATAPI command table entries — (ida_address, command_byte, description)
# SZHC signature at 0x171ACF; command entries begin at 0x171AD4
# ---------------------------------------------------------------------------

ATAPI_CMDS = [
    (0x171AD4, 0x00, "reset/null"),
    (0x171ADB, 0x1B, "START/STOP UNIT"),
    (0x171AE2, 0x1E, "PREVENT/ALLOW MEDIA REMOVAL"),
    (0x171AE9, 0x03, "REQUEST SENSE"),
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def set_name_safe(ea, name, comment=""):
    """Rename address, skipping if already taken by a different address."""
    existing = idc.get_name_ea_simple(name)
    if existing != idc.BADADDR and existing != ea:
        print(f"  SKIP rename {name!r}: already used at 0x{existing:X}")
        return
    idc.set_name(ea, name, idc.SN_NOWARN | idc.SN_NOCHECK)
    if comment:
        idc.set_cmt(ea, comment, 0)


def make_array_bytes(ea, count, name, comment=""):
    """Define a byte array and name it."""
    for i in range(count):
        idc.create_byte(ea + i)
    set_name_safe(ea, name, comment)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("\n=== SP-808 IDA helper ===")
    print(f"Base address: 0x{BASE:X}\n")

    # 1. Apply names and comments
    print("Applying names...")
    for ea, name, comment in NAMES:
        set_name_safe(ea, name, comment)

    # 2. Mark per-slot arrays as byte arrays (8 bytes each)
    SLOT_ARRAYS = [
        (0x426C82, "device_type_by_slot"),
        (0x426C0A, "slot_flag_A"),
        (0x426C12, "slot_flag_B"),
        (0x426C1A, "slot_flag_C"),
        (0x426C22, "slot_flag_D"),
        (0x426C2A, "slot_flag_E"),
        (0x426C32, "slot_media_accepted"),
        (0x426C3A, "slot_device_flags"),
    ]
    print("Defining slot arrays...")
    for ea, name in SLOT_ARRAYS:
        make_array_bytes(ea, 8, name)

    # 3. Mark ATAPI command entries and add comments
    print("Marking ATAPI command table entries...")
    for ea, cmd, desc in ATAPI_CMDS:
        for i in range(7):
            idc.create_byte(ea + i)
        idc.set_cmt(ea,     f"marker (0x06)", 0)
        idc.set_cmt(ea + 1, f"command 0x{cmd:02X}: {desc}", 0)
        for i in range(2, 7):
            idc.set_cmt(ea + i, "param", 0)

    # 4. Mark known ASCII strings
    print("Marking known strings...")
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
    for ea, length, content in STRING_LOCS:
        idc.create_strlit(ea, ea + length + 1, idc.STRTYPE_C)

    # 5. Mark patch location prominently
    patch_ea = 0x12AA14
    idc.set_cmt(patch_ea,
        "PATCH TARGET: change 46 10 (bne) to 40 00 (bra) to allow HDD types 2/3 "
        "through the ZIP-only gate. File offset 0x2AA14.", 1)

    print("\nDone.")
    print("Patch target : 0x12AA14 (file offset 0x2AA14)")
    print("  Original   : 46 10  (bne +0x10, rejects non-ZIP)")
    print("  Patched    : 40 00  (bra +0x00, allows all classified devices)")


if __name__ == "__main__":
    main()
