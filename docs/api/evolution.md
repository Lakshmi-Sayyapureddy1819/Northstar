# API Evolution Strategy

> Companion to `versioning.md`. Versioning defines *how the contract is
> tracked*; this defines *how it should change over time*. Guiding rule:
> **prefer additive, backward-compatible changes; treat breaking changes as a
> deliberate, documented event.**

## Default: additive changes

Whenever a goal can be met without breaking existing consumers, do it
additively:

- **Add** a new optional field rather than repurposing an existing one.
- **Add** a new endpoint rather than changing the shape of an existing one.
- **Add** a new enum value only when clients can safely ignore unknown values.
- **Widen** types (e.g. make a field optional) rather than narrowing them.

Additive changes regenerate the contract, the frontend keeps compiling, and new
capability is adopted when the frontend chooses to consume it. This is the
overwhelming majority of expected change during NorthStar's growth.

## When a breaking change is unavoidable

Some changes genuinely cannot be additive (removing a deprecated field,
correcting a wrong type, restructuring a response). Handle them as a process,
not a surprise:

1. **Record the decision.** A breaking API change is an architectural decision —
   capture it in an ADR (via the `update-adr` skill) before implementing.
2. **Prefer expand → migrate → contract** (the same pattern used for databases):
   - **Expand:** add the new field/endpoint alongside the old one (additive).
   - **Migrate:** move the frontend to the new shape; regenerate contracts.
   - **Contract:** remove the old field/endpoint once nothing consumes it.
   This turns one breaking change into a sequence of safe additive steps.
3. **Let the compiler find the call sites.** When the old shape is finally
   removed and contracts are regenerated, `tsc` fails at every affected
   frontend usage. That is the intended mechanism — fix each site, don't
   suppress it.
4. **Document the migration.** For anything beyond a trivial rename, add notes
   (affected endpoints, old→new mapping, removal timeline) to the relevant
   feature docs and reference them from the ADR.

## What NOT to do

- Do not make a silent breaking change and hand-edit the generated types to
  hide it — generated files are never edited (see `versioning.md`), and CI
  drift validation will fail.
- Do not version by forking types manually in the frontend. There is one
  generated contract; evolve the backend and regenerate.
- Do not introduce a `/v2` surface speculatively. Add explicit API versioning
  only when a real, documented need arises — consistent with the simplicity
  principle.

## Summary

Additive by default. Breaking only when necessary, and then only via
ADR + expand/migrate/contract, with the regenerated contract and the resulting
compile errors as the safety net.
