# Getting Started

From a fresh clone to a fully working, guardrailed NorthStar in a few commands.
Everything here is exercised end-to-end by `scripts/verify-phase0.sh` (Milestone
8), so it stays honest.

## Prerequisites

Install these once (versions are pinned by the repo):

| Tool | Version | Notes |
|------|---------|-------|
| Node | 20 (`.nvmrc`) | JS runtime |
| pnpm | 9.15.0 (`packageManager`) | `corepack enable` or install directly |
| uv | latest | Python package/venv manager (`apps/api`) |
| Docker + Compose | recent | local infrastructure |

Python 3.12 is provisioned by uv automatically (`apps/api/.python-version`).

## One-command verification (recommended)

```bash
scripts/verify-phase0.sh
```

This runs the full production-readiness gauntlet — install, infrastructure,
contract generation, every quality gate (the same checks CI runs), and boots the
backend and frontend to confirm they serve. It exits non-zero if anything fails.
Add `--down` to tear infrastructure down afterward, or `--no-infra` to skip
Docker.

## Manual steps (what the script automates)

### 1. Install dependencies

```bash
pnpm install --frozen-lockfile          # JS workspaces
(cd apps/api && uv sync)                # Python backend
```

### 2. Start infrastructure

```bash
docker compose -f infra/compose/docker-compose.yml up -d --wait
bash infra/compose/verify.sh            # postgres · postgis · pgvector · redis
```

### 3. Configure the backend (optional for /health)

```bash
cp apps/api/.env.example apps/api/.env  # all keys prefixed NORTHSTAR_
```

The health endpoint runs on defaults; `.env` matters once features use the DB/cache.

### 4. Start the backend

```bash
cd apps/api && uv run uvicorn northstar.main:app --reload
# → http://localhost:8000/health  →  {"status":"ok", ...}
```

### 5. Start the frontend

```bash
pnpm --filter web dev
# → http://localhost:3000  (health page at /health)
```

### 6. Generate API contracts

Backend owns the contract (ADR 0008); the frontend consumes generated types.
After any backend contract change:

```bash
pnpm contracts:generate                 # export OpenAPI → regenerate TS types
```

See `docs/api/contract-generation.md`.

### 7. Run the quality gates (mirrors CI)

```bash
# Python
cd apps/api && uv run ruff check . && uv run black --check . \
  && uv run mypy src && uv run lint-imports && uv run pytest -q
# JS / monorepo
pnpm format:check
pnpm exec turbo run lint typecheck test build
```

These are exactly the checks enforced in `.github/workflows/ci.yml`
(see `docs/engineering/continuous-integration.md`). Running
`scripts/verify-phase0.sh` runs all of them plus the boot checks in one shot.

## Where to go next

- Architecture: `docs/architecture/blueprint.md` (frozen v1.0).
- Roadmap & milestones: `docs/roadmap/phase-0.md`.
- CI: `docs/engineering/continuous-integration.md`.
- API contracts: `docs/api/`.
