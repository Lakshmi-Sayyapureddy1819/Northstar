# infra/compose — local infrastructure

Local-first data services for NorthStar development (ADR 0003).

## Start everything (one command)

```bash
docker compose -f infra/compose/docker-compose.yml up -d
```

Brings up:

| Service    | Image                                   | Port | Purpose |
|------------|-----------------------------------------|------|---------|
| `postgres` | `northstar/postgres:16-postgis-pgvector` (built from `infra/docker/postgres`) | 5432 | PostgreSQL 16 + PostGIS + pgvector |
| `redis`    | `redis:7-alpine`                        | 6379 | cache / queue |

Extensions (`postgis`, `vector`) are enabled automatically on first init by
`infra/docker/postgres/init/01-extensions.sql`.

## Defaults

Credentials default to `northstar` / `northstar`, database `northstar` — matching
the API's `NORTHSTAR_DATABASE_URL` / `NORTHSTAR_REDIS_URL` defaults. Override via
environment variables (`POSTGRES_USER`, `POSTGRES_PORT`, `REDIS_PORT`, …).

## Stop

```bash
docker compose -f infra/compose/docker-compose.yml down       # keep data
docker compose -f infra/compose/docker-compose.yml down -v    # wipe volumes
```
