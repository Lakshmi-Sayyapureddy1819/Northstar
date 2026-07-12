#!/usr/bin/env bash
#
# NorthStar — Phase 0 production-readiness verification (Milestone 8).
#
# Proves a fresh clone reaches a fully working, guardrailed state with ZERO
# manual intervention. Runs the entire developer gauntlet end to end:
#
#   1. Preconditions (required tools present)
#   2. Install dependencies (pnpm + uv)
#   3. Start infrastructure (docker compose: PostGIS + pgvector + Redis)
#   4. Generate API contracts + drift check (ADR 0008)
#   5. Quality gates == CI, locally (ruff·black·mypy·import-linter·pytest;
#      prettier·turbo lint/typecheck/test/build)
#   6. Start the backend, assert /health responds
#   7. Start the frontend, assert it serves
#
# Exits non-zero if ANY step fails. Safe to re-run (idempotent).
#
# Usage:
#   scripts/verify-phase0.sh            # full run; leaves infra up
#   scripts/verify-phase0.sh --down     # bring infra down at the end
#   scripts/verify-phase0.sh --no-infra # skip docker steps (quality gates only)

set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

COMPOSE_FILE="infra/compose/docker-compose.yml"
API_PORT="${NORTHSTAR_API_PORT:-8000}"
WEB_PORT="${NORTHSTAR_WEB_PORT:-3100}"
DOWN=0
USE_INFRA=1
for arg in "$@"; do
  case "$arg" in
    --down) DOWN=1 ;;
    --no-infra) USE_INFRA=0 ;;
    *) echo "unknown arg: $arg"; exit 2 ;;
  esac
done

FAILED=0
API_PID=""
WEB_PID=""

c_green="$(printf '\033[32m')"; c_red="$(printf '\033[31m')"
c_dim="$(printf '\033[2m')"; c_bold="$(printf '\033[1m')"; c_off="$(printf '\033[0m')"
ok()   { printf "  ${c_green}✓${c_off} %s\n" "$1"; }
bad()  { printf "  ${c_red}✗ %s${c_off}\n" "$1"; FAILED=1; }
group(){ printf "\n${c_bold}%s${c_off}\n" "$1"; }
# step "label" cmd...  → run a command quietly, report pass/fail, keep going.
step() {
  local label="$1"; shift
  if "$@" >/tmp/ns_verify.log 2>&1; then ok "$label"; else
    bad "$label"; printf "${c_dim}%s${c_off}\n" "$(tail -8 /tmp/ns_verify.log | sed 's/^/      /')"
  fi
}

cleanup() {
  # Kill and reap background servers quietly (wait suppresses the async
  # "Terminated" job-control notice).
  for pid in "$WEB_PID" "$API_PID"; do
    [ -n "$pid" ] || continue
    kill "$pid" 2>/dev/null
    wait "$pid" 2>/dev/null
  done
  if [ "$USE_INFRA" = 1 ] && [ "$DOWN" = 1 ]; then
    docker compose -f "$COMPOSE_FILE" down >/dev/null 2>&1 && echo "infra: brought down"
  fi
}
trap cleanup EXIT

wait_for_http() { # url attempts
  local url="$1" tries="${2:-30}"
  for _ in $(seq 1 "$tries"); do
    if curl -fsS -o /dev/null "$url" 2>/dev/null; then return 0; fi
    sleep 1
  done
  return 1
}

printf "${c_bold}NorthStar — Phase 0 verification${c_off}  ${c_dim}(%s)${c_off}\n" "$ROOT"

# 1. Preconditions ------------------------------------------------------------
group "1. Preconditions"
for tool in node pnpm uv curl; do
  if command -v "$tool" >/dev/null 2>&1; then ok "$tool present ($("$tool" --version 2>&1 | head -1))"; else bad "$tool present"; fi
done
if [ "$USE_INFRA" = 1 ]; then
  if command -v docker >/dev/null 2>&1 && docker info >/dev/null 2>&1; then ok "docker daemon up"; else bad "docker daemon up (use --no-infra to skip)"; fi
fi

# 2. Install ------------------------------------------------------------------
group "2. Install dependencies"
step "pnpm install (frozen lockfile)" pnpm install --frozen-lockfile
step "uv sync (backend)" bash -c "cd apps/api && uv sync"

# 3. Infrastructure -----------------------------------------------------------
if [ "$USE_INFRA" = 1 ]; then
  group "3. Infrastructure (docker compose)"
  step "compose up (--wait for healthy)" docker compose -f "$COMPOSE_FILE" up -d --wait
  step "infra checks (postgres · postgis · pgvector · redis)" bash infra/compose/verify.sh
else
  group "3. Infrastructure (skipped: --no-infra)"
fi

# 4. API contracts ------------------------------------------------------------
group "4. API contracts (ADR 0008)"
step "regenerate contracts" pnpm contracts:generate
step "no contract drift" git diff --exit-code -- packages/api-contracts/openapi.json packages/api-contracts/src/schema.ts

# 5. Quality gates (== CI, locally) ------------------------------------------
group "5. Quality gates (mirrors CI)"
step "ruff" bash -c "cd apps/api && uv run ruff check ."
step "black --check" bash -c "cd apps/api && uv run black --check ."
step "mypy (strict)" bash -c "cd apps/api && uv run mypy src"
step "import-linter (module boundaries)" bash -c "cd apps/api && uv run lint-imports"
step "pytest" bash -c "cd apps/api && uv run pytest -q"
step "prettier (format check)" pnpm format:check
step "turbo lint/typecheck/test/build" pnpm exec turbo run lint typecheck test build

# 6. Backend boots ------------------------------------------------------------
group "6. Backend serves /health"
( cd apps/api && uv run uvicorn northstar.main:app --port "$API_PORT" --log-level warning ) >/tmp/ns_api.log 2>&1 &
API_PID=$!
if wait_for_http "http://localhost:${API_PORT}/health" 30 \
   && curl -fsS "http://localhost:${API_PORT}/health" 2>/dev/null | grep -q '"status":"ok"'; then
  ok "backend /health → 200 ok (port ${API_PORT})"
else
  bad "backend /health"; printf "${c_dim}%s${c_off}\n" "$(tail -8 /tmp/ns_api.log | sed 's/^/      /')"
fi

# 7. Frontend boots -----------------------------------------------------------
group "7. Frontend serves"
( cd apps/web && pnpm exec next start -p "$WEB_PORT" ) >/tmp/ns_web.log 2>&1 &
WEB_PID=$!
if wait_for_http "http://localhost:${WEB_PORT}/health" 40; then
  ok "frontend serves /health (port ${WEB_PORT})"
else
  bad "frontend serves"; printf "${c_dim}%s${c_off}\n" "$(tail -8 /tmp/ns_web.log | sed 's/^/      /')"
fi

# Summary ---------------------------------------------------------------------
group "Result"
if [ "$FAILED" -eq 0 ]; then
  printf "  ${c_green}${c_bold}ALL PHASE 0 VERIFICATION STEPS PASSED${c_off}\n"
  [ "$USE_INFRA" = 1 ] && [ "$DOWN" = 0 ] && printf "  ${c_dim}infra left running — stop with: docker compose -f %s down${c_off}\n" "$COMPOSE_FILE"
else
  printf "  ${c_red}${c_bold}VERIFICATION FAILED — see ✗ items above${c_off}\n"
fi
exit "$FAILED"
