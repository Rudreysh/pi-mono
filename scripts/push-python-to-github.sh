#!/usr/bin/env bash
# Push local python/ to the standalone GitHub repo (Rudreysh/pi-mono-py).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PY_SRC="$ROOT/python"
PY_REPO="${PY_REPO:-$(cd "$ROOT/../pi-mono-py" && pwd)}"
BRANCH="${1:-develop}"
MESSAGE="${2:-}"

if [[ ! -d "$PY_SRC/src" ]]; then
  echo "python/ tree not found at: $PY_SRC" >&2
  exit 1
fi

if [[ ! -d "$PY_REPO/.git" ]]; then
  echo "Python repo not found at: $PY_REPO" >&2
  echo "Clone it: git clone https://github.com/Rudreysh/pi-mono-py.git $PY_REPO" >&2
  exit 1
fi

rsync -av \
  --exclude '__pycache__' \
  --exclude '.pytest_cache' \
  --exclude '.mypy_cache' \
  --exclude '.ruff_cache' \
  --exclude '*.html' \
  --exclude 'import.jsonl' \
  --exclude '.git' \
  --exclude 'pi_mono_python.egg-info' \
  "$PY_SRC/" \
  "$PY_REPO/"

cd "$PY_REPO"
git checkout "$BRANCH"
git add -A

if git diff --cached --quiet; then
  echo "No Python changes to push."
  exit 0
fi

if [[ -z "$MESSAGE" ]]; then
  echo "Enter commit message for pi-mono-py:"
  read -r MESSAGE
fi

git commit -m "$MESSAGE"
git push origin "$BRANCH"
echo "Pushed python/ to https://github.com/Rudreysh/pi-mono-py ($BRANCH)"
