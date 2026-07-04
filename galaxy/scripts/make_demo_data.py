#!/usr/bin/env python3
"""Generate a privacy-safe demo data.js so the repo renders out of the box.

This invents fake folders/notes (PARA method) that match the shipped textures
and config.js. Real users overwrite data.js by running update_dashboard.py
against their own vault. Run: python scripts/make_demo_data.py
"""
import json, time
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "data.demo.js"
NOW = int(time.time())
H = 3600

def note(title, folder, hours_ago):
    return {"title": title, "path": f"{folder}/{title}.md", "mtime": NOW - hours_ago * H}

FOLDERS = [
    ("01_Projects", [("Website Redesign", 6), ("Q3 Launch Plan", 4)], [
        ("Launch checklist", 2), ("Landing page copy", 5), ("Roadmap", 20)]),
    ("02_Areas", [("Health", 8), ("Finances", 3)], [
        ("Weekly review", 12), ("Budget 2026", 30), ("Habits tracker", 48)]),
    ("03_Resources", [("Design", 5), ("Code Snippets", 9)], [
        ("Color theory notes", 15), ("Useful CSS tricks", 26), ("Typography", 60)]),
    ("04_Archive", [("2025", 40)], [
        ("Old project wrap-up", 200), ("Retired ideas", 240)]),
    ("05_Journal", [("Daily", 2)], [
        ("2026-06-12", 1), ("2026-06-11", 25), ("2026-06-10", 49)]),
    ("06_Ideas", [("Drafts", 7)], [
        ("App idea: focus timer", 3), ("Essay outline", 18), ("Random spark", 70)]),
    ("07_Reading", [("Books", 6), ("Articles", 4)], [
        ("Atomic Habits — notes", 9), ("Deep Work — highlights", 33)]),
    ("08_Inbox", [], [
        ("Untitled 1", 1), ("Voice memo transcript", 4), ("Link to read later", 7)]),
]

folders, all_notes = [], []
for name, subspec, recentspec in FOLDERS:
    subs = []
    for sname, scount in subspec:
        subnotes = [note(f"{sname} note {i+1}", f"{name}/{sname}", (i+1)*8)
                    for i in range(min(scount, 5))]
        subs.append({"name": sname, "notes": scount, "recent": subnotes})
    recent = [note(t, name, h) for t, h in recentspec]
    all_notes += recent
    total = sum(s["notes"] for s in subs) + len(recent) + 3
    folders.append({"name": name, "notes": total, "subs": subs, "recent": recent})

all_notes.sort(key=lambda n: n["mtime"], reverse=True)
data = {
    "generated": time.strftime("%Y-%m-%d %H:%M", time.localtime(NOW)),
    "vault": "DemoVault",
    "totalNotes": sum(f["notes"] for f in folders),
    "todayUpdated": sum(1 for n in all_notes if NOW - n["mtime"] < 86400),
    "recentAll": all_notes[:6],
    "folders": folders,
}
OUT.write_text("window.GALAXY_DATA = " + json.dumps(data, ensure_ascii=False, indent=1) + ";\n",
               encoding="utf-8")
print(f"OK -> {OUT} ({len(folders)} planets, demo data)")
