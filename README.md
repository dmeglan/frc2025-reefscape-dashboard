# FRC 2025 REEFSCAPE — Robot Study Dashboard

An interactive, self-contained dashboard cataloging the FRC 2025 **REEFSCAPE** robots that
publicly released **downloadable CAD**, enriched with mechanism and vision detail mined from each
team's Chief Delphi reveal / CAD-release thread. Built with the `frc-robot-study-dashboard` pipeline,
mirroring the 2026 REBUILT dashboard.

- **`index.html`** — the interactive dashboard (desktop table + mobile card view), GitHub Pages entry point.
- **`deep-dive.html`** / **`deep-dive.pdf`** — printable subsystem teardown of the best-documented robots.
- **`pipeline/`** — the build pipeline (`config.py`, `codex_data.json`, `deepdive_extra.py`, build scripts).

## Status

- **64 teams** with downloadable CAD (Onshape / GrabCAD), discovered via the Spectrum 3847 CAD Collection.
- **13 ★ study picks**, each with a deep subsystem profile drawn from its Chief Delphi thread.
- **EPA / rank / record are pending**: Statbotics' data API was mid-outage at build time (HTTP 500 on
  all data endpoints). Those columns show "—" and will be backfilled when the API recovers — re-run the
  pipeline to enrich them.

## Rebuild

```
cd pipeline
python3 build_dashboard.py        # dashboard + dashboard_state.json
python3 build_deepdive_html.py
python3 build_deepdive_pdf.py     # needs: pip install reportlab --break-system-packages
python3 apply_changelog.py "summary"   # writes ../index.html + ../deep-dive.*
```

## One-time GitHub Pages setup

```
git init && git add . && git commit -m "Initial FRC 2025 REEFSCAPE dashboard"
git branch -M main
git remote add origin https://USERNAME:TOKEN@github.com/USERNAME/frc2025-reefscape-dashboard.git
git push -u origin main
```

Then enable **Settings → Pages → Deploy from a branch → `main` / root**. After that, `bash pipeline/publish.sh "msg"` pushes refreshes hands-off.
