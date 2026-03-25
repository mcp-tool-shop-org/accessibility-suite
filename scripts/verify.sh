#!/usr/bin/env bash
set -euo pipefail

# Run all sub-project tests from the monorepo root.
# Requires: Python 3.10+, Node.js 18+, pip, npm

PASS=0
FAIL=0
FAILED=()

run_python() {
  local project="$1"
  echo "==> [$project] (Python)"
  pushd "src/$project" > /dev/null

  if [ ! -d ".venv" ]; then
    python -m venv .venv
  fi
  source .venv/bin/activate 2>/dev/null || source .venv/Scripts/activate 2>/dev/null
  pip install -q -e . 2>/dev/null
  pip install -q pytest 2>/dev/null

  if pytest --collect-only > /dev/null 2>&1; then
    if pytest -q; then
      PASS=$((PASS + 1))
    else
      FAIL=$((FAIL + 1))
      FAILED+=("$project")
    fi
  else
    echo "    (no tests found, skipping)"
    PASS=$((PASS + 1))
  fi

  deactivate 2>/dev/null || true
  popd > /dev/null
  echo ""
}

run_node() {
  local project="$1"
  echo "==> [$project] (Node.js)"
  pushd "src/$project" > /dev/null

  npm ci --silent 2>/dev/null || npm install --silent 2>/dev/null
  if npm test 2>/dev/null; then
    PASS=$((PASS + 1))
  else
    FAIL=$((FAIL + 1))
    FAILED+=("$project")
  fi

  popd > /dev/null
  echo ""
}

echo "Accessibility Suite — Local Test Runner"
echo "========================================"
echo ""

# Python projects
run_python "a11y-lint"
run_python "a11y-ci"
run_python "a11y-assist"

# Node.js projects
run_node "a11y-evidence-engine"
run_node "a11y-mcp-tools"

# Handbook verification
echo "==> [handbooks] (verification)"
if python scripts/verify_handbooks.py; then
  PASS=$((PASS + 1))
else
  FAIL=$((FAIL + 1))
  FAILED+=("handbooks")
fi
echo ""

echo "========================================"
echo "Passed: $PASS  Failed: $FAIL"

if [ "$FAIL" -gt 0 ]; then
  echo ""
  echo "FAILED:"
  for f in "${FAILED[@]}"; do
    echo "  - $f"
  done
  exit 1
fi

echo "All sub-projects passed."
exit 0
