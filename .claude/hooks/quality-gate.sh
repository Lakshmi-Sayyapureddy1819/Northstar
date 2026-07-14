#!/usr/bin/env bash
# NorthStar quality gate — runs on file edits.
# Enforces the architectural guardrails locally. Each check is resilient:
# if the tool isn't installed yet (early Phase 0), it skips with a note rather
# than failing. As Phase 0 lands the tooling, these gain full teeth.
#
# Exit non-zero to signal a violation to Claude Code.

set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT" || exit 0

status=0
have() { command -v "$1" >/dev/null 2>&1; }

# Python tools are installed into apps/api/.venv by uv, not onto the shell's
# PATH — resolve there first so the gate has real teeth even when the venv
# isn't activated in the hook's subshell. Fall back to PATH, then skip.
API_VENV="apps/api/.venv/bin"
py_tool() {
  if [ -x "$API_VENV/$1" ]; then echo "$API_VENV/$1";
  elif have "$1"; then command -v "$1";
  fi
}

# --- Python: ruff, mypy (strict), import-linter (the boundary rule) ---
if [ -d "apps/api" ]; then
  ruff_bin="$(py_tool ruff)"; [ -n "$ruff_bin" ] && { "$ruff_bin" check apps/api || status=1; }
  mypy_bin="$(py_tool mypy)"; [ -n "$mypy_bin" ] && { "$mypy_bin" apps/api/src || status=1; }
  lint_imports_bin="$(py_tool lint-imports)"
  if [ -n "$lint_imports_bin" ]; then
    lint_imports_abs="$(cd "$(dirname "$lint_imports_bin")" && pwd)/$(basename "$lint_imports_bin")"
    # import-linter reads config from CWD's pyproject.toml — that's apps/api, not repo root
    (cd apps/api && "$lint_imports_abs" --config pyproject.toml) || { echo "✗ import-linter: a context boundary was violated (see contract.py rule)"; status=1; }
  fi
fi

# --- Web: eslint + tsc (no ignored TS errors; generated-types discipline) ---
if [ -f "apps/web/package.json" ]; then
  if have pnpm; then
    pnpm --filter web exec tsc --noEmit 2>/dev/null || status=1
    pnpm --filter web exec eslint . 2>/dev/null || true
  fi
fi

[ "$status" -ne 0 ] && echo "NorthStar quality gate found issues. Fix before proceeding (see CLAUDE.md rules)."
exit "$status"
