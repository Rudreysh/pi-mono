#!/usr/bin/env bash
set -euo pipefail

# Find repository root
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$DIR"

echo "Running ruff check..."
python3 -m ruff check python/src python/tests

echo "Running black check..."
python3 -m black --check python/src python/tests

echo "Running mypy check..."
python3 -m mypy python/src

echo "Running pytest..."
PYTHONPATH=python/src python3 -m pytest python/tests
