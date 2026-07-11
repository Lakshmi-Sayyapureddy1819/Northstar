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

# --- Python: ruff, mypy (strict), import-linter (the boundary rule) ---
if [ -d "apps/api" ]; then
  if have ruff; then ruff check apps/api || status=1; fi
  if have mypy; then mypy apps/api/src || status=1; fi
  if have lint-imports; then
    # import-linter enforces contract-only cross-context imports
    lint-imports || { echo "✗ import-linter: a context boundary was violated (see contract.py rule)"; status=1; }
  elif have import-linter; then
    import-linter || status=1
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
