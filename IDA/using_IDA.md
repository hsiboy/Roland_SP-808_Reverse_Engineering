# IDA Pro Setup — Roland SP-808 Firmware

## Loading the firmware

1. Start IDA Pro and choose **New**.
2. Select `SP8EXall.bin`.
3. In the load dialog:
   - Processor: **H8/300H Advanced** (covers H8S/2653)
   - Loading offset / RAM: leave at default — the script sets the base address
   - When asked to load as a binary file, confirm **Yes**
4. When IDA asks about the processor sub-type, select **H8S/2600 Advanced**.
5. Let the initial auto-analysis run to completion before running any script.

## Loading offset

The SP-808 external flash is mapped at **0x100000** at runtime. Set this in
IDA via **Edit > Segments > Rebase program** if it was not set at load time.

All IDA addresses in this project use the runtime address. Conversion:

```
file_offset = IDA_address - 0x100000
```

## Running the helper scripts

Two scripts are provided. Run them via **File > Script file**:

### SP808_IDA_helper.idc (IDC)

The primary setup script. Run this first after loading.

- Names all known functions, RAM locations, and ROM strings
- Marks the patch target at 0x12AA14 with a repeatable comment
- Defines per-slot byte arrays at 0x426C82 etc.
- Names H8S/2653 internal I/O registers
- Processes the exception vector table

```
File > Script file > SP808_IDA_helper.idc
```

## Navigating key locations after running the script

| What                        | Address    | Shortcut              |
|-----------------------------|------------|-----------------------|
| Device type string table    | 0x171AC0   | G → type address      |
| SZHC ATAPI command table    | 0x171AD4   | G → type address      |
| IOMEGA vendor string        | 0x171AF0   | G → type address      |
| device_classifier function  | 0x12AE88   | G → type address      |
| device_probe function       | 0x12A956   | G → type address      |
| Patch target                | 0x12AA14   | G → type address      |
| device_type_by_slot array   | 0x426C82   | G → type address      |

Press **X** on any named location to see all cross-references to it.

Use **Shift+F4** (Names window) to browse all labels created by the script.

## Patch location

| File offset | IDA address | Original   | Patched    | Effect                        |
|-------------|-------------|------------|------------|-------------------------------|
| `0x2AA14`   | `0x12AA14`  | `46 10`    | `40 00`    | `bne +0x10` → `bra +0x00`    |

Apply via `patch_sp808.py`. See `README.md` in /firmware for the full flash workflow.
