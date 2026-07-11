# @northstar/ui

The NorthStar shared design system — **reusable, business-agnostic primitives**
(Button, and future Input/Card/Dialog/…) plus the `cn()` class utility.

## Scope

- ✅ Generic, presentational primitives usable by any feature.
- ✅ Accessible by default (semantic HTML, visible focus states, aria passthrough) — see `apps/web/CLAUDE.md → Accessibility`.
- ❌ **No business-specific UI.** Anything that knows about companies, opportunities, engines, or Polaris belongs in that product's `apps/web/src/features/<capability>/`, never here.
- ❌ No data fetching, no API types (those come from `@northstar/api-contracts`).

## Theming

Components style with **semantic Tailwind tokens** (`bg-primary`, `text-foreground`, …),
never hardcoded colors, so light/dark/brand themes can be applied without touching
component code. Tokens are defined in `apps/web/src/app/globals.css`.
