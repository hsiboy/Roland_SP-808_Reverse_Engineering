# 🖥️ The SP‑808EX boot splash — recovered from ROM

The startup logo the SP‑808EX paints on its LCD, reconstructed directly from the firmware's own graphic
data. Every piece below was carved out of `SP8EXall.bin`
(MD5 `d744a9cd4a2790ac68d165fd7849b5d8`) — no external artwork.

<div align="center">
<img src="logo_full.png" alt="Roland SP-808EX boot logo" width="620">
</div>

---

## Recovered elements

The splash is assembled from **five** ROM graphics. The `8` sprite is drawn *twice*, so “808” is really
`8 0 8` built from just two distinct digit bitmaps:

<table>
<tr>
<td align="center" valign="bottom"><img src="element_roland.png" width="210"><br><code>0x179E52</code><br><b>Roland</b><br><sub>69×14 px</sub></td>
<td align="center" valign="bottom"><img src="element_sp-dash.png" width="180"><br><code>0x179ED1</code><br><b>SP‑</b><br><sub>56×17 px</sub></td>
<td align="center" valign="bottom"><img src="element_8.png" width="74"><br><code>0x179F5B</code><br><b>8</b> <sub>(drawn ×2)</sub><br><sub>22×17 px</sub></td>
<td align="center" valign="bottom"><img src="element_0.png" width="74"><br><code>0x179FA1</code><br><b>0</b><br><sub>22×17 px</sub></td>
<td align="center" valign="bottom"><img src="element_ex.png" width="60"><br><code>0x179FE7</code><br><b>EX</b><br><sub>18×9 px</sub></td>
</tr>
</table>

*(Each image is the 1‑bit ROM bitmap upscaled 8× with no smoothing — exact pixels — shown in the
SP‑808's characteristic **yellow‑green backlit LCD** colours.)*

---

## How it's drawn

The boot routine at `0x125904` calls the logo painter at `0x14FB82`, which draws the graphics and then
animates them into place.

| ROM data | Role |
|---|---|
| `0x179E52` | **Roland** wordmark — drawn first (via `0x400470`). |
| `0x179ED1` | **SP‑** large lettering — drawn at x = 3 (via `0x400478`). |
| `0x179F5B` | the **8** — drawn twice, at x = 61 and x = 111. |
| `0x179FA1` | the **0** — drawn between them at x = 86 → **808**. |
| `0x179FE7` | **EX** badge — drawn after the animation (via `0x400470`). |

Final assembly coordinates (from `0x14FB82`): Roland `(3,0)`, SP‑ `(3,15)`, 8 `(61,15)`, 0 `(86,15)`,
8 `(111,15)`, EX `(118,23)`. This is the logo's bounding region, not a full LCD screenshot.

### The animation

The logo doesn't just appear — the four middle graphics slide up. The animation loop is
`0x14FBE2–0x14FC52` (draw calls at `14FBF8 / 14FC0E / 14FC28 / 14FC3E`): **17 steps** moving the
vertical coordinate from `31` up to `15`, with a short delay after each step.

---

## Bitmap format

- **Source:** `firmware/SP8EXall.bin`, MD5 `d744a9cd4a2790ac68d165fd7849b5d8`.
- Raw ROM images: a width byte, a height byte, then `ceil(width / 7)` bytes per row; bits 7..1 hold
  pixels and bit 0 is unused (seven pixels per byte).
- Light compression (seen in the `0x179E52` stream, which ends exactly at `0x179ED1`):
  `00nnnnnn` repeats the following byte, `01nnnnnn` emits zero bytes, `11nnnnnn` copies literals; no
  `10nnnnnn` controls occur. That stream yields 140 bytes, arranged in seven‑pixel column groups of
  fourteen rows.

---

## Files

| File | What |
|---|---|
| `logo_full.png` | the assembled logo (8× preview) |
| `element_*.png` | the individual recovered sprites (8×) |
| `sp808ex_preview.png` | earlier 6× whole‑logo preview |
| `sp808ex_assembled.bmp` · `*_<offset>.bmp` | the raw 1‑bit sprites at native resolution (ROM offset in each name) |
