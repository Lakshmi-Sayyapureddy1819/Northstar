# Continuous Integration

CI is the mechanical enforcement of the Engineering Blueprint. Every
architectural guardrail runs here and **fails the build** if violated. Pipeline:
`.github/workflows/ci.yml`.

## Triggers & posture

- Runs on push to `main` and on every pull request.
- `concurrency` cancels superseded runs on the same ref.
- Least-privilege `permissions: contents: read`.

## Jobs (parallel)

| Job | Enforces | Steps |
|-----|----------|-------|
| **backend** | Python quality, typing, module boundaries, tests | ruff · black --check · mypy (strict) · **import-linter** (ADR 0001) · pytest |
| **frontend** | JS quality, typing, tests, build | prettier · turbo `lint` · `typecheck` · `test` (vitest) · `build` (`next build`) |
| **contracts** | API-contract integrity (ADR 0008) | regenerate contracts → `git diff --exit-code` on `openapi.json` + `schema.ts`; stale ⇒ fail |

### Guardrails that fail CI

- **Module boundaries** — import-linter (context independence + Clean-Architecture layers).
- **Contract drift** — committed contracts must match the backend.
- **Types** — mypy (strict) and `tsc --noEmit`.
- **Lint & format** — ruff, eslint, black, prettier.
- **Tests** — pytest, vitest.

## Caching

- **Python** — `astral-sh/setup-uv` dependency cache keyed on `apps/api/uv.lock`.
- **pnpm** — `actions/setup-node` store cache (`cache: pnpm`).
- **Turbo** — `actions/cache` on `.turbo`, SHA-keyed with restore-keys.

## Dependency updates

`.github/dependabot.yml` opens weekly, grouped update PRs for three ecosystems —
GitHub Actions, npm/pnpm, and uv (Python). Every Dependabot PR must pass the full
CI suite above before merge.

## Deferred: end-to-end (Playwright) job

The Playwright e2e scaffold (`apps/web/e2e/`, `apps/web/playwright.config.ts`)
exists and is validated by typecheck/lint, but **e2e is intentionally not run in
CI during Phase 0**.

**Why deferred**

- Running it requires downloading browser binaries (`playwright install`) and
  building + booting the app (`webServer`), adding minutes and flakiness surface
  to every run.
- Phase 0 has no real user flow to protect — the only e2e is a health-page smoke
  test. The cost/benefit doesn't justify it yet (simplicity principle).

**What will trigger adding it**

Add the e2e job when the **first real user journey** ships — concretely, at
**Phase 1 (Data / product identity)**, when the map + company cards + search flow
becomes something a regression could break. Also add it sooner if a bug ever
ships that a cheap e2e would have caught.

**Where it fits in the pipeline**

A new parallel job `e2e` in `.github/workflows/ci.yml`, gated to run after
`frontend` (it needs a build). It will: set up pnpm/Node (reusing the store
cache) → `pnpm install --frozen-lockfile` → `pnpm --filter web exec playwright
install --with-deps chromium` → `pnpm --filter web test:e2e`. Consider running it
only on PRs to `main` (not every push) if runtime becomes a concern.

## Local verification

Milestone 8 provides a single fresh-clone script that runs the same gates
locally so a developer can reproduce CI before pushing. See
`docs/roadmap/phase-0.md` (Milestone 8).
