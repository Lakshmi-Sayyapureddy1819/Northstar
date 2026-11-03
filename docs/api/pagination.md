# API Pagination Convention

> Introduced in Phase 1, Slice 1 (`GET /companies`) — the first endpoint that
> needed it. Applies to every future list endpoint (opportunities, etc.).
> Slice 3's `GET /companies/nearby` reuses this convention unchanged, plus
> its own `lat`/`lng`/`radius_km` query params — proof the convention
> generalizes to a second list endpoint without modification.

## Convention: `limit` / `offset` query parameters

```
GET /companies?limit=50&offset=0
```

- `limit` — page size. Default `50`, bounded `[1, 200]` at the router
  (`Query(ge=1, le=200)`); FastAPI returns `422` if violated.
- `offset` — rows to skip. Default `0`, bounded `>= 0`.
- Response wraps the page in an envelope carrying the request-echoing
  `limit`/`offset` alongside `items`, e.g.:

```json
{
  "items": [ { "id": "...", "slug": "...", "name": "...", "...": "..." } ],
  "limit": 50,
  "offset": 0
}
```

## Why offset-based (not cursor-based) for MVP

Simplicity: MVP list sizes (companies/opportunities in one city, one
vertical) are small enough that offset pagination's O(offset) cost is not a
real concern, and it's trivially easy for the frontend to reason about ("page
3 of role search results"). Move to cursor-based pagination only when a
concrete list genuinely outgrows this — via an ADR if it changes the public
contract shape, per `docs/api/evolution.md`.

## Validation errors

Out-of-range `limit`/`offset` are caught at two layers:

1. **Router** (`Query(ge=..., le=...)`) — FastAPI/Pydantic returns `422` before
   the request reaches application code.
2. **Application** (`ListCompanies.execute`) — defends the same invariant for
   any caller that isn't the HTTP router (e.g. a future seed script or another
   context calling the use case directly), returning `Err(DomainError(code="invalid_pagination"))`
   rather than raising.
