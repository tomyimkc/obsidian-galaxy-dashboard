#!/usr/bin/env python3
"""Scan an Obsidian vault and generate data.js for Knowledge Galaxy.

Adapted for sophia-agi.

Usage (from repo root):
    python galaxy/scripts/update_dashboard.py --vault . --name "sophia-agi" --min 3
    python galaxy/scripts/update_dashboard.py --vault . --root docs --name "sophia-agi"

Options:
    --vault   Path to vault (use "." when running from sophia-agi root).
    --root    Optional sub-folder (e.g. "docs" or "wiki").
    --name    Vault name shown in Obsidian for obsidian:// links.
    --min     Minimum .md count for a folder to become a planet (default 3).
    --out     Output data.js path (default: galaxy/data.js).
"""
import argparse
import json
from pathlib import Path
from datetime import datetime, date

RECENT_N = 8
SUB_RECENT_N = 5


def md_files(d: Path, root: Path):
    return [p for p in d.rglob("*.md")
            if not any(part.startswith(".") for part in p.relative_to(root).parts)]


def note_info(p: Path, vault: Path):
    return {"title": p.stem, "path": str(p.relative_to(vault)), "mtime": int(p.stat().st_mtime)}


def recent(files, n, vault):
    ordered = sorted(files, key=lambda p: p.stat().st_mtime, reverse=True)[:n]
    return [note_info(p, vault) for p in ordered]


def main():
    ap = argparse.ArgumentParser(description="Generate data.js from an Obsidian vault (sophia-agi edition).")
    ap.add_argument("--vault", required=True, help="Path to your vault ('.' for repo root).")
    ap.add_argument("--root", default="", help="Optional sub-folder inside the vault (e.g. docs, wiki).")
    ap.add_argument("--name", default="", help="Vault name for obsidian:// links.")
    ap.add_argument("--min", type=int, default=3, help="Min notes for a folder to show as planet.")
    ap.add_argument("--out", default="", help="Output path for data.js (default galaxy/data.js).")
    args = ap.parse_args()

    vault = Path(args.vault).expanduser().resolve()
    if not vault.is_dir():
        raise SystemExit(f"Vault not found: {vault}")
    root = (vault / args.root) if args.root else vault
    if not root.is_dir():
        raise SystemExit(f"Root folder not found: {root}")
    vault_name = args.name or vault.name
    out = Path(args.out) if args.out else Path(__file__).resolve().parents[1] / "data.js"

    folders, all_files = [], []
    for d in sorted(root.iterdir()):
        if not d.is_dir() or d.name.startswith("."):
            continue
        files = md_files(d, root)
        if len(files) < args.min:
            continue
        all_files += files
        subs = []
        for s in sorted(d.iterdir()):
            if s.is_dir() and not s.name.startswith("."):
                sf = md_files(s, root)
                subs.append({"name": s.name, "notes": len(sf),
                             "recent": recent(sf, SUB_RECENT_N, vault)})
        folders.append({"name": d.name, "notes": len(files), "subs": subs,
                        "recent": recent(files, RECENT_N, vault)})

    if not folders:
        raise SystemExit(f"No folders with >= {args.min} notes under {root}. "
                         "Try a lower --min or a different --root.")

    today = date.today()
    today_count = sum(1 for p in all_files if date.fromtimestamp(p.stat().st_mtime) == today)
    data = {
        "generated": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "vault": vault_name,
        "totalNotes": len(all_files),
        "todayUpdated": today_count,
        "recentAll": recent(all_files, 6, vault),
        "folders": folders,
    }
    out.write_text("window.GALAXY_DATA = " + json.dumps(data, ensure_ascii=False, indent=1) + ";\n",
                   encoding="utf-8")
    print(f"OK -> {out}  ({len(folders)} planets, {len(all_files)} notes, "
          f"{today_count} updated today)")


if __name__ == "__main__":
    main()
