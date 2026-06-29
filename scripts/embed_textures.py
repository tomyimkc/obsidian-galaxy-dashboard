#!/usr/bin/env python3
"""Pack textures/*.jpg and assets/bg.jpg into textures.js (base64-embedded).

Usage:
    python scripts/embed_textures.py

Why embed as base64: Chrome blocks WebGL from reading local image files under
the file:// protocol (canvas tainting / CORS). Embedding the images as base64
data URIs is the only way to texture the 3D planets while keeping the app a
double-click-to-open static page with no local server. The trade-off is a
larger textures.js (parsed once on load).

Naming convention: name each planet texture after its folder, e.g.
    textures/01_Projects.jpg  ->  applied to the "01_Projects" planet
Textures use a 2:1 equirectangular projection (a sphere "unwrapped" flat).
Folders without a matching texture fall back to a procedural texture.
"""
import base64
import mimetypes
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEX_DIR = ROOT / "textures"
BG = ROOT / "assets" / "bg.jpg"
OUT = ROOT / "textures.js"

# Try sips (macOS) to downscale the background; fall back to embedding as-is.
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
