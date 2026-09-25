"""Render SVG marks into a test contact sheet PNG: sizes 16/32/64/256 px, one-colour and reversed.

Usage: python contact_sheet.py OUT.png a.svg b.svg ...
Needs a Chromium binary (CHROME env var, or /opt/pw-browsers/chromium-*/chrome-linux/chrome).
SVGs should draw ink in #15181b/currentColor so the reversed row can recolour them.
"""
import sys, os, glob, subprocess, tempfile, pathlib, re
out, svgs = sys.argv[1], sys.argv[2:]
chrome = os.environ.get("CHROME") or (glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome") + [""])[0]
def inline(p, ink):
    s = pathlib.Path(p).read_text()
    s = re.sub(r'#15181b|currentColor', ink, s, flags=re.I)
    return re.sub(r' width="[\d.]+" height="[\d.]+"', ' ', s, count=1)
rows = []
for p in svgs:
    name = pathlib.Path(p).stem
    cells = "".join(f'<div class="c"><div style="height:{s}px">{inline(p,"#15181b")}</div><small>{s}</small></div>' for s in (16, 32, 64, 256))
    mono = f'<div class="c"><div style="height:64px;filter:grayscale(1) contrast(9)">{inline(p,"#000")}</div><small>1-colour</small></div>'
    inv = f'<div class="c inv"><div style="height:64px">{inline(p,"#f2f0ec")}</div><small>reversed</small></div>'
    rows.append(f'<h3>{name}</h3><div class="r">{cells}{mono}{inv}</div>')
html = """<style>body{font:13px sans-serif;margin:20px;background:#fff}.r{display:flex;gap:24px;align-items:flex-end;margin-bottom:18px}
.c{display:flex;flex-direction:column;gap:4px;align-items:flex-start}.c svg{height:100%;width:auto}.inv{background:#15181b;padding:10px;color:#ccc}
h3{margin:14px 0 6px}</style>""" + "".join(rows)
tmp = pathlib.Path(tempfile.mkdtemp()) / "sheet.html"; tmp.write_text(html)
h = 60 + 380 * len(svgs)
subprocess.run([chrome, "--headless", "--no-sandbox", "--disable-gpu", f"--window-size=1400,{h}",
                f"--screenshot={os.path.abspath(out)}", f"file://{tmp}"], check=True, capture_output=True)
print("wrote", out)
