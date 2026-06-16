#!/usr/bin/env bash
# publish.sh — push the freshly built dashboard to GitHub Pages.
#
# Same lock-proof trick as the SRS watcher: the Cowork mount can CREATE files in
# .git but not DELETE them, so any leftover lock (.git/index.lock, refs/*.lock)
# jams later git commands. We therefore NEVER commit/push from the mounted repo.
# Instead we make a throwaway shallow clone in /tmp (always lock-free), drop the
# freshly built files in, and push from there.
#
# Publishes:  index.html  deep-dive.html  deep-dive.pdf   (all at repo root)
#
# Usage:   bash pipeline/publish.sh ["commit message"]
# Requires: the authenticated remote URL is stored once in the mounted repo's
#           .git/config (see REBUILD.md "One-time setup for hands-off push").

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(dirname "$SCRIPT_DIR")"
WORK="${FRC_PUBLISH_WORK:-/tmp/frc2026_publish}"
MSG="${1:-Refresh FRC 2026 REBUILT dashboard $(date +%F)}"
FILES=(index.html deep-dive.html deep-dive.pdf)

REMOTE="$(git -C "$REPO" config --get remote.origin.url || true)"
if [ -z "$REMOTE" ]; then
  echo "publish: ERROR — no remote.origin.url in $REPO/.git/config." >&2
  echo "publish: set it once (see pipeline/REBUILD.md):" >&2
  echo "  git remote add origin https://USERNAME:TOKEN@github.com/USERNAME/frc2026-rebuilt-dashboard.git" >&2
  exit 1
fi

rm -rf "$WORK"
git clone --depth 1 --branch main "$REMOTE" "$WORK" >/dev/null 2>&1

for f in "${FILES[@]}"; do
  [ -f "$REPO/$f" ] && cp "$REPO/$f" "$WORK/$f"
done

cd "$WORK"
# Commit identity (overridable via env). The sandbox git has none by default.
git config user.name  "${FRC_GIT_NAME:-FRC Dashboard Bot}"
git config user.email "${FRC_GIT_EMAIL:-frc-dashboard@users.noreply.github.com}"

if git diff --quiet -- "${FILES[@]}" 2>/dev/null; then
  echo "publish: files already match the live site — nothing to push."
  exit 0
fi

git add "${FILES[@]}"
git commit -m "$MSG" >/dev/null
git push origin main >/dev/null 2>&1
echo "publish: pushed $(git rev-parse --short HEAD) -> origin/main"
echo "publish: live within ~1 min"
