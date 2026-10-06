Source: SP8EXall.bin; MD5 d744a9cd4a2790ac68d165fd7849b5d8.
BMPs: 1-bit black-on-white, native dimensions.
Raw images: width byte, height byte; ceil(width/7) bytes per row; bits 7..1 contain pixels, bit 0 unused.
179E52: width 69, height byte 8E. Observed RLE: 00nnnnnn repeats following byte, 01nnnnnn emits zeros, 11nnnnnn copies literals. No 10nnnnnn controls occur. Stream ends exactly at 179ED1, yields 140 bytes, arranged in seven-pixel column groups of fourteen rows.
Assembly uses final 14FB82 animation coordinates: Roland (3,0), SP- (3,15), 8 (61,15), 0 (86,15), 8 (111,15), EX (118,23). This is the logo bounding region, not a full LCD screenshot.
PNG preview is enlarged 6x without interpolation.

Startup calls it at `125904`. It draws several ROM graphics, then runs 17 animation steps, moving their vertical coordinate from `31` to `15`, with a delay after each step.

| ROM data | Behavior in `14FB82` |
|---|---|
| `179E52` | Drawn first through `400470`. |
| `179ED1` | Larger graphic, drawn through `400478` at horizontal coordinate `3`. |
| `179F5B` | Graphic drawn twice, at horizontal coordinates `61` and `111`. |
| `179FA1` | Graphic drawn between them, at horizontal coordinate `86`. |
| `179FE7` | Drawn through `400470` after the animation and another delay. |

The middle four draws assemble **“SP-808”**: the raw bitmap patterns at `179ED1` resemble the large **SP-** lettering; `179F5B` has the shape of **8**, and `179FA1` has the shape of **0**. Reusing the same graphic on either side gives **808**. Their placement and startup-only animation reinforce that interpretation.

The animation loop is **`14FBE2–14FC52`**, with drawing calls at `14FBF8`, `14FC0E`, `14FC28` and `14FC3E`.

