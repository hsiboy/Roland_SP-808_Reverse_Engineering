"""Render the read-only hardware/firmware evidence map into unique artifacts."""
import base64
import hashlib
import json
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / 'analysis/SP808_hardware_firmware_map_2026-10-06_evidence.json'


def hashes(path):
    content = path.read_bytes()
    return dict(path=path.relative_to(ROOT).as_posix(), size=len(content),
                md5=hashlib.md5(content).hexdigest(), sha256=hashlib.sha256(content).hexdigest())


def main():
    data = json.loads(EVIDENCE.read_text(encoding='utf-8'))
    sources = ['media/sp808-block_diagram.png', 'firmware/SP8EXall.bin', 'firmware/A6_all.bin',
               'SP-808EX_Evidence_Ledger_2026-10-05_v11.md',
               'SP-808EX_Observed_Architecture_Technical_Reference_2026-10-05_v9.md',
               'Roland_SP-808_Hardware_Architecture_Corrections_2026-10-05_v4.md',
               'analysis/CODEX_HANDOFF_2026-10-05.md', 'analysis/findings.md',
               'analysis/Link_Plan_v3_2026-10-05.md', 'IDA/H8.cfg',
               'protocols/Roland_SP-808_to_ZIP_Drive_sniff.md']
    inputs = [hashes(ROOT / p) for p in sources] + [hashes(EVIDENCE), hashes(Path(__file__).resolve())]
    assert inputs[1]['md5'] == 'd744a9cd4a2790ac68d165fd7849b5d8'
    data['inputs'] = inputs
    data['runtime_validation'] = 'UNRESOLVED; no hardware test, firmware/database edits or renames'
    assert len({n['id'] for n in data['nodes']}) == len(data['nodes'])
    for node in data['nodes']:
        for x, y, width, height in node['rects']:
            assert x >= 0 and y >= 0 and x + width <= 1069 and y + height <= 749
    base = ROOT / 'analysis' / ('SP808_hardware_firmware_map_2026-10-06_' + uuid.uuid4().hex[:8])
    md = ['# SP-808 hardware ↔ firmware map', '',
          '**OBSERVED:** Hardware blocks are read from [the block diagram](../media/sp808-block_diagram.png). '
          'Stock SP firmware MD5: ' + inputs[1]['md5'] + '. All addresses are hexadecimal runtime addresses; '
          'BIN offset = runtime − 100000. A6 and v3 references are named explicitly.', '',
          '**OBSERVED:** Examples were checked using read-only IDA on the matching SP database. '
          'The companion JSON includes returned disassembly excerpts and input hashes. Existing semantic names '
          'remain navigation aids. This is an interface map, not an exhaustive instruction/address-form census. '
          'Empty xrefs do not prove absence.', '',
          '**STRONGLY INFERRED:** The hardware maps to several firmware layers: H8 control code, executable '
          'ESP processing records, inherited DRAM services and device interfaces. Locating a high-level caller '
          'does not recover its low-level service implementation.', '',
          '| Diagram block | Firmware anchors | Interface | Mapping status |',
          '|---|---|---|---|']
    for n in data['nodes']:
        md.append('| ' + n['name'] + ' | ' + '<br>'.join(n['firmware']) + ' | ' +
                  '<br>'.join(n['registers'] or ['No established register mapping']) + ' | ' + n['confidence'] + ' |')
    md += ['', '## Evidence and boundaries by block', '']
    for n in data['nodes']:
        md += ['### ' + n['name'], '', '**OBSERVED:** ' + n['observed'], '',
               '**' + n['confidence'] + ' — mapping:** ' + '; '.join(n['firmware']) + '.', '',
               '**UNRESOLVED:** ' + n['unresolved'], '', 'Evidence: ' + '; '.join(n['sources']) + '.', '']
    md += ['## What the v3 experiment occupies', '',
           '**OBSERVED:** V3 adds A6 ATA routines at 17D000 onward and configures IRQ2 plus TPU1/TPU2 → '
           'DTC descriptors → 600000. SP 105476/10547A already write TGR1A/TGR2A; v3 changes the shell '
           'immediate from 0018 to 0050. These are CPU-internal transfer resources; the data endpoint '
           'belongs to the external storage interface. V3 does not reroute ordinary filesystem I/O.', '',
           '**UNRESOLVED:** A successful cold-init/read test would establish that bounded storage path; '
           'it would not establish panel, DSP, audio routing or normal SP functionality after transplant.', '',
           '## Mapping boundaries', '',
           '- **OBSERVED:** CPU DRAM and DSP DRAM are separate diagram blocks. ESP PRAM is not a general CPU sample-memory map.',
           '- **OBSERVED:** 400xxx denotes executable DRAM services, not MMIO registers or proven internal-ROM services.',
           '- **STRONGLY INFERRED:** SCI0 corresponds to MIDI; SCI1/CN7 is a separate proprietary interface not drawn as the MIDI board.',
           '- **OBSERVED:** Main-board internal Zip and option-board SCSI Zip are separate physical paths.',
           '- **UNRESOLVED:** TPU0 timing constants do not identify an IC19/sample-rate driver; H8 ADC names do not identify AK4520 control code.',
           '', '## Source navigation', '']
    for p in sources[3:]:
        md.append('- [' + p + '](../' + p + ')')
    md += ['', 'Sources include historical passages and later corrections. Use Technical Reference §13 for '
           'executable ESP records and the final programmed-vector clarification for 450/458. Earlier '
           'uncertainty on those points is superseded. Diagram wiring alone does not establish bus decode.']
    page = PAGE.replace('IMAGE_DATA', base64.b64encode((ROOT / sources[0]).read_bytes()).decode())
    page = page.replace('JSON_DATA', json.dumps(data, ensure_ascii=False).replace('</', '<\/'))
    outputs = []
    for suffix, content in [('.json', json.dumps(data, indent=2, ensure_ascii=False) + '\n'),
                            ('.md', '\n'.join(md) + '\n'), ('.html', page)]:
        path = base.with_suffix(suffix)
        with path.open('x', encoding='utf-8') as f:
            f.write(content)
        outputs.append(hashes(path))
    manifest = dict(schema_version=1, inputs=inputs, outputs=outputs,
                    verification=dict(firmware_md5='PASS', distinct_nodes='PASS', overlay_bounds='PASS',
                                      nodes=len(data['nodes']), runtime_validation='UNRESOLVED'))
    with Path(str(base) + '_hashes.json').open('x', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)
        f.write('\n')
    print(json.dumps(dict(outputs=outputs, nodes=len(data['nodes']), image_embedded=True), indent=2))


PAGE = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>SP-808 firmware / hardware map</title><style>
body{margin:0;background:#eef1f5;color:#17202d;font:16px system-ui,sans-serif}header{padding:20px 28px;background:#12233b;color:white}header p{max-width:1050px;line-height:1.5}.layout{display:grid;grid-template-columns:minmax(550px,1.5fr) minmax(330px,1fr);gap:20px;padding:20px}.picture,aside{background:white;border-radius:10px;padding:14px}.picture svg{width:100%;height:auto}.hit{cursor:pointer;fill:transparent;stroke-width:2;stroke-dasharray:5 3}.hit:hover,.hit:focus{fill:#3b82f633;stroke-width:4}.hit.selected{fill:#fbbf2444;stroke-width:4;stroke-dasharray:none}button{border:1px solid #a6b0bd;background:white;border-radius:6px;padding:7px 10px;margin:4px;cursor:pointer;text-align:left}button[aria-pressed=true]{background:#dbeafe;border-color:#2563eb}h2{margin-top:8px}p,li{line-height:1.5}.badge{font-weight:bold;font-size:13px;padding:5px;border-radius:4px;display:inline-block}.note{font-size:14px;color:#45566f}#picker{max-height:260px;overflow:auto;border-top:1px solid #ddd;margin-top:18px;padding-top:8px}@media(max-width:1000px){.layout{display:block}.picture{margin-bottom:18px}}.legend{font-size:13px;display:flex;flex-wrap:wrap;gap:10px}.legend span{border-bottom:3px solid;padding-bottom:3px}
</style><header><h1>SP-808 hardware ↔ firmware</h1><p>Click a hardware block for firmware anchors, interfaces, evidence and unresolved connections. The original block diagram is preserved. Mapping confidence is separate from observed wiring and instructions.</p><p style="color:#cbd5e1">Stock SP firmware · hexadecimal runtime addresses · read-only evidence · no hardware validation</p></header>
<main class="layout"><section class="picture"><div class="legend"><span style="border-color:#047857">OBSERVED</span><span style="border-color:#2563eb">STRONGLY INFERRED</span><span style="border-color:#b45309">HYPOTHESIZED</span><span style="border-color:#64748b">UNRESOLVED</span></div><svg viewBox="0 0 1069 749" aria-label="SP-808 hardware block diagram"><image width="1069" height="749" href="data:image/png;base64,IMAGE_DATA"></image><g id="overlays"></g></svg><p class="note">CPU DRAM, DSP DRAM and ESP PRAM are separate concepts. 400xxx contains executable inherited services; those entry addresses are not hardware registers.</p><div id="picker"></div></section><aside id="detail" aria-live="polite"></aside></main>
<script id="data" type="application/json">JSON_DATA</script><script>
const data=JSON.parse(document.getElementById('data').textContent);const colors={'OBSERVED':'#047857','STRONGLY INFERRED':'#2563eb','HYPOTHESIZED':'#b45309','UNRESOLVED':'#64748b'};const ns='http://www.w3.org/2000/svg';
function esc(s){return s.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;')}
function list(items){return '<ul>'+items.map(s=>'<li>'+esc(s)+'</li>').join('')+'</ul>'}
function select(id){const n=data.nodes.find(x=>x.id===id);document.querySelectorAll('.hit').forEach(x=>x.classList.toggle('selected',x.dataset.id===id));document.querySelectorAll('#picker button').forEach(x=>x.setAttribute('aria-pressed',x.dataset.id===id));document.getElementById('detail').innerHTML='<h2>'+esc(n.name)+'</h2><span class="badge" style="color:'+colors[n.confidence]+';background:#edf2f7">'+n.confidence+' — mapping confidence</span><h3>Firmware anchors</h3>'+list(n.firmware)+'<h3>Register / service interface</h3>'+list(n.registers.length?n.registers:['No established register mapping'])+'<h3>OBSERVED evidence</h3><p>'+esc(n.observed)+'</p><h3>UNRESOLVED</h3><p>'+esc(n.unresolved)+'</p><h3>Evidence references</h3>'+list(n.sources)+'<p class="note">Companion Markdown and JSON contain the scope, disassembly evidence and hashes. Mapping does not prove runtime success.</p>'}
for(const n of data.nodes){for(const box of n.rects){const r=document.createElementNS(ns,'rect');['x','y','width','height'].forEach((k,i)=>r.setAttribute(k,box[i]));r.setAttribute('rx',3);r.setAttribute('stroke',colors[n.confidence]);r.setAttribute('class','hit');r.setAttribute('tabindex',0);r.setAttribute('role','button');r.setAttribute('aria-label',n.name);r.dataset.id=n.id;r.addEventListener('click',()=>select(n.id));r.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();select(n.id)}});const t=document.createElementNS(ns,'title');t.textContent=n.name+' — '+n.confidence;r.appendChild(t);document.getElementById('overlays').appendChild(r)}const b=document.createElement('button');b.textContent=n.name;b.dataset.id=n.id;b.addEventListener('click',()=>select(n.id));document.getElementById('picker').appendChild(b)}select('gate');
</script></html>'''


if __name__ == '__main__':
    main()
