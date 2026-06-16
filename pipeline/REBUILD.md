# FRC 2026 REBUILT dashboard — rebuild & publish playbook

The scheduled task **frc2026-dashboard-new-releases** does this automatically twice a
week. You can also trigger it manually by telling Claude (Cowork): **"refresh the FRC
2026 dashboard"**.

## What happens each run
1. **Find + add releases.** Follow `UPDATE_INSTRUCTIONS.md` (search Chief Delphi, verify
   CAD + 2026, pull Statbotics, append qualifying teams to `codex_data.json`, add deep
   profiles to `deepdive_extra.py`).
2. **Rebuild.** From `pipeline/`:
   ```
   python3 build_dashboard_v3.py      # also writes dashboard_state.json
   python3 build_deepdive_html.py
   python3 build_deepdive_pdf.py
   ```
3. **Changelog + banner.** `python3 apply_changelog.py`
   - diffs `codex_data` (via `dashboard_state.json`) against `snapshot.json`,
   - prepends a dated entry to `changelog.json` when teams were added / removed / newly
     picked / CAD-upgraded,
   - injects the **Updated …** banner + **What's changed** panel into the dashboard,
   - writes `../index.html` (for Pages) + refreshes the local dashboard HTML, and copies
     the deep-dive to `../deep-dive.html` / `../deep-dive.pdf`.
   - Optional one-line override: `python3 apply_changelog.py "custom summary"`.
4. **Publish.** If anything changed:
   ```
   bash publish.sh "Refresh FRC 2026 dashboard $(date +%F) — <one-line summary>"
   ```
   Pushes the three built files via a throwaway `/tmp` clone (lock-proof). Live within ~1 min.

   > **Do NOT** `git add/commit/push` directly inside this folder. The Cowork mount can
   > create files in `.git` but not delete them, so a leftover lock (`.git/index.lock`,
   > `refs/**/*.lock`) jams every later git command. `publish.sh` sidesteps this by
   > committing from a throwaway `/tmp` clone and never touching the mounted `.git`.
   >
   > If the mounted repo gets stuck on a stale lock, clear it from a Mac Terminal:
   > ```
   > cd "/Users/dmeglan/Documents/Claude/Projects/FRC 2026 Rebuilt Game"
   > find .git -name '*.lock' -delete && git fetch origin && git reset --hard origin/main
   > ```

## One-time setup for hands-off push (do this once, from a Mac Terminal)
```
cd "/Users/dmeglan/Documents/Claude/Projects/FRC 2026 Rebuilt Game"
git init
git add .gitignore README.md index.html deep-dive.html deep-dive.pdf
git commit -m "Initial FRC 2026 REBUILT dashboard"
git branch -M main
# fine-grained PAT limited to this repo, Contents: read/write (or a classic PAT w/ repo scope):
git remote add origin https://USERNAME:TOKEN@github.com/USERNAME/frc2026-rebuilt-dashboard.git
git push -u origin main
```
Then enable **Settings → Pages → Deploy from a branch → `main` / root**.
The token sits only in `.git/config` (never pushed). `publish.sh` reads this same URL,
so every later push is hands-off.

## Files
- `build_dashboard_v3.py`  codex_data.json -> dashboard + `dashboard_state.json`
- `build_deepdive_html.py` / `build_deepdive_pdf.py`  top-teams deep-dive
- `apply_changelog.py`     diff + changelog + banner injection -> `../index.html`
- `publish.sh`             pushes index.html + deep-dive.* via a /tmp clone (lock-proof)
- `changelog.json`         persisted changelog (newest first)
- `snapshot.json`          last published team -> {name,pick,cad} (for diffing)
- `dashboard_state.json`   authoritative counts + row set emitted by the builder
