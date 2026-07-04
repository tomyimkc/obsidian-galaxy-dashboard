# 🌌 Sophia Galaxy

Turn the sophia-agi knowledge base into an explorable 3D galaxy.

Each major folder becomes a glowing planet. Subfolders orbit as moons. Click a planet to fly in, browse recent notes, and jump straight into Obsidian.

Built from the beautiful [obsidian-galaxy-dashboard](https://github.com/Aprillllllw/obsidian-galaxy-dashboard) — zero build, single-file Three.js + bloom + custom shaders.

## Quick start

1. Generate fresh data from the repo (recommended after any big doc/wiki changes):

```bash
python galaxy/scripts/update_dashboard.py --vault . --name "sophia-agi" --min 3
```

2. Open the dashboard:

```bash
# macOS
open galaxy/index.html

# or any OS
# double-click galaxy/index.html in your file browser
```

The page works from `file://` (all assets are embedded or procedural).

## Recommended scans

- Full repo knowledge view (recommended):
  ```bash
  python galaxy/scripts/update_dashboard.py --vault . --name "sophia-agi" --min 3
  ```

- Focus only on the structured docs:
  ```bash
  python galaxy/scripts/update_dashboard.py --vault . --root docs --name "sophia-agi"
  ```

- Just the living wiki corpus:
  ```bash
  python galaxy/scripts/update_dashboard.py --vault . --root wiki --name "sophia-agi" --min 1
  ```

> **Vault name**: `--name "sophia-agi"` must match exactly the name you gave this folder when you added it to Obsidian.  
> If `obsidian://` links do nothing, re-run with the correct vault name.

## Controls

- Drag background → orbit the galaxy
- Scroll → zoom
- Drag a planet → spin that planet
- Click a planet → fly in (planet view + side panel)
- In planet view: click moons to highlight, click notes to open in Obsidian
- `Esc` or the Back button → return to galaxy
- Bottom nav: Galaxy / Grid / Timeline / Stats / Search (Search hands off to Obsidian full-text)

## Customize appearance

Edit `galaxy/config.js`:

- Change titles, quote
- Map specific folders to colors, subtitles, descriptions, and Saturn rings
- Add your own planet textures (2:1 equirectangular `.jpg`) under `galaxy/textures/`, then run:

  ```bash
  python galaxy/scripts/embed_textures.py
  ```

## How data works

- `data.js` — generated from your current files (committed snapshot for the public repo)
- `data.demo.js` — fallback demo data
- `index.html` loads `data.demo.js` then `data.js` (your data wins)

Re-run the updater script whenever you want the galaxy to reflect the latest notes.

## Privacy & offline

- Purely local. No network calls except loading Three.js from a CDN for the 3D engine.
- `obsidian://` deep links are the only external action (they stay on your machine).

## Serving over http (optional)

```bash
node galaxy/serve.js
# or PORT=9000 node galaxy/serve.js
```

## Maintaining & Updating (via your fork + subtree)

This dashboard is managed as a **git subtree** from your fork:

- Your fork (where you can push sophia-specific improvements):  
  https://github.com/tomyimkc/obsidian-galaxy-dashboard

- Upstream (original project, for pulling general improvements):  
  https://github.com/Aprillllllw/obsidian-galaxy-dashboard

### To pull the latest improvements from upstream into sophia-agi

```bash
git fetch galaxy-upstream
git subtree pull --prefix=galaxy galaxy-upstream main --squash
```

Then re-apply any sophia customizations that might have conflicted (usually just `config.js`, the scanner script, and `README.md`), and regenerate data:

```bash
python galaxy/scripts/update_dashboard.py --vault . --name "sophia-agi" --min 3
```

### To push your sophia changes to your own fork

If you improve the dashboard code itself (e.g. new features, better config handling), push from this subtree:

```bash
git subtree push --prefix=galaxy galaxy-fork main
```

Or work directly in your fork repo and then pull the changes here with `git subtree pull`.

### Adding the remotes (one-time)

These were already added for you:

```bash
git remote add galaxy-upstream https://github.com/Aprillllllw/obsidian-galaxy-dashboard.git
git remote add galaxy-fork https://github.com/tomyimkc/obsidian-galaxy-dashboard.git
```

## Credits

- Original beautiful implementation: https://github.com/Aprillllllw/obsidian-galaxy-dashboard
- Your fork for sophia customizations: https://github.com/tomyimkc/obsidian-galaxy-dashboard
- Adapted + themed for the sophia-agi epistemic corpus.

> _Per aspera ad astra_ — through hardship to the stars.
