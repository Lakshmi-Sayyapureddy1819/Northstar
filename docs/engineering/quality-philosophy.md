# Quality Philosophy — Why Each Tool Is Here

Every tool in this list was chosen to enforce one of the nine non-negotiable
rules in root `CLAUDE.md`, not out of habit or ecosystem default. This is the
canonical reference for *why* the guardrail exists — read it before removing,
downgrading, or disabling any check in CI or the local quality gate
(`.claude/hooks/quality-gate.sh`).

## Backend (`apps/api`)

### Ruff — lint
- **Responsibility:** catches unused imports/variables, unsafe patterns,
  outdated syntax, and import ordering (`select = ["E", "F", "I", "UP", "B",
  "SIM"]` in `apps/api/pyproject.toml`).
- **Why we chose it:** one Rust-based tool replaces what used to be
  flake8 + isort + pyupgrade + a chunk of bugbear, at a fraction of the
  runtime — a hook that runs on every file edit has to be fast enough that
  nobody is tempted to skip it.
- **Architectural principle protected:** Simplicity (rule 7) — fewer tools,
  faster feedback, same coverage.

### Black — format
- **Responsibility:** deterministic code formatting; removes formatting from
  code review entirely.
- **Why we chose it:** zero-config, opinionated, matched to Ruff's
  `line-length = 88` so the two never fight over the same line.
- **Architectural principle protected:** Simplicity — formatting is a solved
  problem here, so no engineering time or review attention goes to it.

### mypy (strict)
- **Responsibility:** static type checking across `src/` (tests excluded —
  `exclude = ['(^|/)tests/']`), `strict = true`, with the `pydantic.mypy`
  plugin so Pydantic models are understood precisely.
- **Why we chose it:** `strict` mode, not permissive mode. A modular monolith
  depends on contracts between contexts being exact — `contract.py` is the
  one surface other contexts see, and if its types are loose, the contract is
  loose. Strict mypy makes every `contract.py` a real, checked interface
  rather than an informal convention.
- **Architectural principle protected:** Contract-only imports (rule 2) — a
  contract you can't trust the types of isn't a contract.

### pytest
- **Responsibility:** unit and integration tests; `testpaths = ["tests",
  "src/northstar/contexts"]` so tests live next to the context they verify.
- **Why we chose it:** standard, fixture-based, and the placement of
  `testpaths` inside each context reinforces that a context owns its own
  correctness — no central test suite has to know a context's internals.
- **Architectural principle protected:** Living Documentation (rule 8) — a
  feature isn't done without passing tests; tests are executable
  documentation of what a context actually guarantees.

### import-linter
- **Responsibility:** the two contracts described in
  `docs/engineering/module-boundaries.md` — context independence except via
  `contract.py`, and inward-only Clean Architecture layering within each
  context.
- **Why we chose it:** it is the only tool in this list that enforces an
  *architectural* rule rather than a code-quality one. Ruff/mypy/pytest can
  all pass on code that quietly violates the modular-monolith boundary;
  import-linter is what makes that boundary real instead of aspirational.
- **Architectural principle protected:** Contract-only imports (rule 2) and
  Automation enforces architecture (rule 9) directly — this tool exists
  *because* rule 9 says intent must be backed by a mechanical check.

## Frontend (`apps/web`)

### ESLint
- **Responsibility:** React/Next.js-specific correctness rules (hooks rules,
  accessibility, import hygiene) via the shared `@northstar/config-eslint`
  package.
- **Why we chose it:** a shared config package (rather than per-app config)
  means the same rules apply anywhere a new frontend surface is added,
  without re-deciding the rules each time.
- **Architectural principle protected:** Simplicity — one config, reused, not
  re-litigated per app.

### Prettier
- **Responsibility:** deterministic formatting for TS/TSX/CSS/JSON, same role
  as Black on the backend.
- **Why we chose it:** removes formatting bikeshedding from PR review;
  config lives once at the repo root (`.prettierrc.json`) rather than per app.
- **Architectural principle protected:** Simplicity.

### tsc (TypeScript, no ignored errors)
- **Responsibility:** type-checks the frontend against
  `packages/api-contracts`, the generated types from the backend's OpenAPI
  schema.
- **Why it matters here specifically:** this is the enforcement point for
  rule 4 ("API contracts are truth... frontend consumes generated types
  only"). If the frontend could silently ignore a type error against the
  generated client, a backend contract change could break the frontend
  without anyone noticing until runtime.
- **Architectural principle protected:** API contracts as truth (rule 4).

### Vitest
- **Responsibility:** fast unit/component tests for frontend logic and
  components.
- **Why we chose it:** native ESM and Vite-based tooling, fast enough for the
  same "runs on every edit" bar as the backend's pytest.
- **Architectural principle protected:** Living Documentation (rule 8).

### Playwright
- **Responsibility:** end-to-end browser tests exercising real user flows
  across the anonymous → personalized → Polaris tiers.
- **Why we chose it:** the only tool in this list that verifies the product
  from the outside — a real browser hitting real routes — rather than a
  single layer in isolation. Needed because rule 6 (Anonymous-first) is a
  cross-cutting UX guarantee that no unit test can verify by itself: it has
  to be checked by actually navigating the app without an identity.
- **Architectural principle protected:** Anonymous-first (rule 6) and Living
  Documentation (rule 8).

## Reading this table as a whole

Notice the shape: Ruff/Black/ESLint/Prettier protect *Simplicity* (cheap,
solved problems, kept off the review docket); mypy/tsc protect *contracts*
(rules 2 and 4); pytest/Vitest/Playwright protect *Living Documentation*
(rule 8, tests as proof a feature works); import-linter is the one tool that
protects *architecture itself* (rules 2 and 9). None of these are here by
ecosystem default — each maps to a specific rule in root `CLAUDE.md`. If a
future change needs to relax one of these tools, that's an architectural
decision, and per rule 9 it starts with an ADR, not a config edit.
