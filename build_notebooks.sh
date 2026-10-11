#!/usr/bin/env bash
# Convert the percent-format sources in <question>/notebooks/_src into .ipynb and execute them in order.
# Usage: ./build_notebooks.sh q0_boom_catalogue        (all)   |   ./build_notebooks.sh q0_boom_catalogue 03   (one)
set -euo pipefail
cd "$(dirname "$0")/$1/notebooks"
PY=${PYTHON:-python}
for src in _src/${2:-}*.py; do
  nb="$(basename "${src%.py}").ipynb"
  echo "== $nb"
  $PY -m jupytext --to ipynb --output "$nb" "$src" >/dev/null
  $PY -m jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=1800 "$nb"
done
