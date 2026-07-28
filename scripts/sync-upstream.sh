#!/usr/bin/env bash
# Merge latest upstream TypeScript into the current branch.
# Keeps your python/ folder; everything else should match upstream.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

UPSTREAM_REMOTE="${UPSTREAM_REMOTE:-upstream}"
UPSTREAM_BRANCH="${UPSTREAM_BRANCH:-main}"

echo "Fetching $UPSTREAM_REMOTE..."
git fetch "$UPSTREAM_REMOTE"
git fetch earendil 2>/dev/null || true

CURRENT="$(git branch --show-current)"
echo "Merging $UPSTREAM_REMOTE/$UPSTREAM_BRANCH into $CURRENT..."

if ! git merge "$UPSTREAM_REMOTE/$UPSTREAM_BRANCH" -m "Merge $UPSTREAM_REMOTE/$UPSTREAM_BRANCH into $CURRENT"; then
  echo ""
  echo "Merge conflict. Resolve manually:"
  echo "  - Outside python/: prefer upstream (theirs) unless you know you need a local change"
  echo "  - Inside python/: keep your Python port (ours)"
  echo ""
  echo "After resolving: git add <files> && git commit"
  exit 1
fi

echo "Upstream sync complete on branch: $CURRENT"
echo "Push fork: git push my_fork $CURRENT"
echo "Push Python separately: ./scripts/push-python-to-github.sh"
