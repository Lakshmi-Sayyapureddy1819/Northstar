# Module Boundaries — Why the Two import-linter Contracts Exist

NorthStar is a **modular monolith** (ADR 0001): one deployable, many bounded
contexts, each with an internal boundary as strict as if it were a separate
service. That's a claim about intent. Without a mechanical check, intent
erodes the first time someone reaches for a "quick" cross-context import
under deadline pressure — and nothing in a monolith's process boundary stops
that. import-linter (config: `apps/api/pyproject.toml`, `[tool.importlinter]`)
turns the claim into a build gate. It defines exactly two contracts.

## Contract 1 — Bounded contexts are independent except through `contract.py`

```toml
type = "independence"
modules = ["northstar.contexts.ingestion", ... all 11 contexts ...]
ignore_imports = ["northstar.contexts.** -> northstar.contexts.*.contract"]
```

**Why this exists:** each context (`ingestion`, `companies`, `geo`,
`career_intelligence`, `identity`, `profile`, `resume`, `career_gps`,
`engagement`, `polaris`, `opportunities`) owns its own domain model,
persistence, and business rules. If context A can reach into context B's
`domain/` or `infrastructure/` directly, B can no longer change its internals
without a search across the whole codebase — the monolith degrades into a
tangle no safer than a poorly-factored single service, while losing the
simplicity a monolith is supposed to buy you (root CLAUDE.md rule 7).

The `independence` contract type forbids *any* import between the listed
modules. The one carve-out — `ignore_imports` — permits exactly one shape of
edge: `northstar.contexts.<any> -> northstar.contexts.<any>.contract`. That
carve-out **is** root CLAUDE.md rule 2 ("a bounded context may import another
context's `contract.py` — never its internals") expressed as config instead
of a convention someone has to remember. `contract.py` is deliberately the
*only* public surface (see any context's `contract.py` docstring, e.g.
`career_intelligence/contract.py`) — everything else in a context
(`domain/`, `application/`, `infrastructure/`) is private by construction.

`unmatched_ignore_imports_alerting = "none"` exists because Phase 0 shipped
contexts before any of them collaborate — the allow-rule matches nothing yet.
That's expected, not a bug; the rule engages the moment a context first
imports another's `contract.py`.

## Contract 2 — Clean Architecture layering within every context

```toml
type = "layers"
layers = ["infrastructure", "application", "domain"]
containers = [... all 11 contexts ...]
```

**Why this exists:** within a single context, `domain/` must stay ignorant of
frameworks, databases, and HTTP — it is where the business rule actually
lives, and business rules should not know they run inside FastAPI on
Postgres. `application/` orchestrates domain objects but still shouldn't know
*which* database or web framework is in use. `infrastructure/` is the only
layer allowed to know about SQLAlchemy, HTTP clients, or any concrete vendor
API. import-linter's `layers` contract lists layers **outer-to-inner**
(`infrastructure` → `application` → `domain`): each layer may import the ones
listed below it, never the reverse. Concretely: `domain/` cannot import
`application/` or `infrastructure/`; `application/` cannot import
`infrastructure/`. This is what root CLAUDE.md rule 5 ("cloud-agnostic...
no vendor SDK in domain/application layers") looks like enforced per-context
rather than asserted in prose.

This contract is applied identically across all 11 contexts via `containers`
— one rule, no per-context exceptions, so the same review question ("does
this import point outward?") has the same mechanical answer everywhere.

## Why we intentionally tested a violation

A guardrail nobody has watched fail is a guardrail nobody actually trusts —
it might be silently misconfigured, or scoped narrower than it looks. Before
relying on these two contracts to hold the line as Phase 1+ contexts start
collaborating, we deliberately introduced a cross-context import that skipped
`contract.py` and confirmed `lint-imports` caught it and failed the check —
proof the "independence except through `contract.py`" rule is load-bearing,
not decorative. The same discipline applies to any future contract change:
if you loosen or add a rule, first prove it still catches the violation it's
meant to catch, the same way you'd add a failing test before a fix.

## Running it locally

```bash
cd apps/api && uv run lint-imports --config pyproject.toml
```

This also runs automatically via the `PostToolUse` quality gate
(`.claude/hooks/quality-gate.sh`) on every `Edit`/`Write`, and in CI
(`docs/engineering/continuous-integration.md`) on every push — the same
check, run in three places, so a violation cannot slip through by skipping
any one of them.
