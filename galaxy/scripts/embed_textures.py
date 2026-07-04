#!/usr/bin/env python3
"""Pack textures/*.jpg and assets/bg.jpg into textures.js (base64-embedded).

See upstream for full docs. Run from inside galaxy/ or repo root.

Usage:
    python galaxy/scripts/embed_textures.py
"""
import base64
import mimetypes
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEX_DIR = ROOT / "textures"
BG = ROOT / "assets" / "bg.jpg"
OUT = ROOT / "textures.js"


def shrink_bg(src: Path) -> bytes:
    try:
        tmp = Path(tempfile.mkstemp(suffix=".jpg")[1])
        subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "80",
                        "--resampleWidth", "2048", str(src), "--out", str(tmp)],
                       capture_output=True, check=True)
        data = tmp.read_bytes()
        tmp.unlink()
        return data
    except Exception:
        return src.read_bytes()


entries = []

if BG.exists():
    b64 = base64.b64encode(shrink_bg(BG)).decode()
    entries.append(f' "__bg": "data:image/jpeg;base64,{b64}"')
    print(f"packed assets/bg.jpg -> __bg")

for p in sorted(TEX_DIR.glob("*")):
    if p.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
        continue
    mime = mimetypes.guess_type(p.name)[0]
    b64 = base64.b64encode(p.read_bytes()).decode()
    entries.append(f' "{p.stem}": "data:{mime};base64,{b64}"')
    print(f"packed textures/{p.name} ({p.stat().st_size // 1024} KB)")

OUT.write_text("window.GALAXY_TEXTURES = {\n" + ",\n".join(entries) + "\n};\n",
               encoding="utf-8")
print(f"OK -> {OUT} ({OUT.stat().st_size // 1024} KB, {len(entries)} images)")
