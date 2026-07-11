#!/usr/bin/env bash
# NorthStar doc-drift check — Living Documentation enforcement.
# Flags structural additions that lack their required companion artifact:
#   - a CIE engine folder without its docs/engines/<name>.md spec
#   - a bounded context without a contract.py
# Advisory (exit 0) so it never blocks mid-edit, but prints clear warnings.

set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT" || exit 0

ENGINES_DIR="apps/api/src/northstar/contexts/career_intelligence/engines"
CONTEXTS_DIR="apps/api/src/northstar/contexts"
warned=0

if [ -d "$ENGINES_DIR" ]; then
  for d in "$ENGINES_DIR"/*/; do
    [ -d "$d" ] || continue
    name="$(basename "$d")"
    [ "$name" = "__pycache__" ] && continue
    if [ ! -f "docs/engines/${name}.md" ]; then
      echo "⚠ Living-Doc: engine '${name}' has no docs/engines/${name}.md spec (use the update-documentation Skill)."
      warned=1
    fi
  done
fi

if [ -d "$CONTEXTS_DIR" ]; then
  for d in "$CONTEXTS_DIR"/*/; do
    [ -d "$d" ] || continue
    name="$(basename "$d")"
    [ "$name" = "__pycache__" ] && continue
    if [ ! -f "${d}contract.py" ]; then
      echo "⚠ Boundary: context '${name}' has no contract.py (its only permitted public surface)."
      warned=1
    fi
  done
fi

[ "$warned" -eq 0 ] && exit 0
echo "— Living Documentation reminder: a feature is complete only with updated docs + ADRs (see root CLAUDE.md)."
exit 0
