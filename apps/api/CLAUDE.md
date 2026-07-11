# apps/api — Backend Conventions

FastAPI modular monolith. Read the root `CLAUDE.md` first for the non-negotiable rules.

## Clean Architecture layering (inside every context)

```
API/Router → Application (use cases) → Domain (entities, logic)
                    ↓                        ↑
               Ports (interfaces) ← Infrastructure (adapters)
```

- Dependencies point **inward**. Domain/Application **never** import infrastructure.
- Infrastructure implements ports defined by inner layers.
- No vendor SDK (SQLAlchemy models aside) leaks into Domain/Application.

## Anatomy of a bounded context

```
contexts/<name>/
├── domain/            # entities, value objects, pure business logic
├── application/       # use cases orchestrating domain + ports
├── infrastructure/    # repositories, adapters
├── (providers/ | engines/ …)   # context-specific extension points
└── contract.py        # THE ONLY public surface. Others import this and nothing else.
```

## Hard rules

- **Cross-context access is via `contract.py` only.** import-linter enforces this in CI. If you need something from another context, expose it through that context's contract.
- **`platform/`** = technical foundation (`db`, `cache`, `geo`, `config`, `observability`, `llm`). Not business logic.
- **`shared_kernel/`** = domain primitives shared across contexts (IDs, Result/error types, common value objects). Keep it tiny — it is not a junk drawer.
- **AI is a platform capability.** The `LLMPort` + Claude adapter + prompt infra live in `platform/llm/`. Business decisions never live there.

## Conventions

- Typing: `mypy --strict`. Lint/format: Ruff + Black. No ignored type errors.
- Errors: prefer explicit `Result`/typed errors over exceptions for domain flows (see `shared_kernel/`).
- Config: Pydantic Settings, env-only.
- Tests: pytest. Every engine and use case is independently testable without a live DB where possible.
- Contracts: the API emits OpenAPI; TS types are generated into `packages/api-contracts`. Never hand-edit those.

## Deterministic engines

See `contexts/career_intelligence/CLAUDE.md`. Providers: `contexts/ingestion/CLAUDE.md`. AI boundary: `contexts/polaris/CLAUDE.md`.
