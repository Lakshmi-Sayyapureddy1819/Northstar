#!/usr/bin/env bash
# Repeatable verification of NorthStar local infrastructure.
# Checks the four requirements a new contributor needs green:
#   1. PostgreSQL connectivity
#   2. PostGIS extension available
#   3. pgvector extension available
#   4. Redis connectivity
#
# Usage:  infra/compose/verify.sh
# Exits non-zero if any check fails.

set -uo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPOSE="$DIR/docker-compose.yml"
DC=(docker compose -f "$COMPOSE")
PG_USER="${POSTGRES_USER:-northstar}"
PG_DB="${POSTGRES_DB:-northstar}"

fail=0
ok()   { echo "✓ $1"; }
bad()  { echo "✗ $1"; fail=1; }

# Preflight: is the stack running?
if ! "${DC[@]}" ps --status running --services 2>/dev/null | grep -qx postgres; then
  echo "Postgres container is not running. Start the stack first:"
  echo "  ${DC[*]} up -d"
  exit 1
fi

psql_q() {
  "${DC[@]}" exec -T postgres psql -U "$PG_USER" -d "$PG_DB" -tAc "$1" 2>/dev/null
}

# 1. PostgreSQL connectivity
if "${DC[@]}" exec -T postgres pg_isready -U "$PG_USER" -d "$PG_DB" >/dev/null 2>&1 \
   && [ "$(psql_q 'SELECT 1')" = "1" ]; then
  ok "PostgreSQL connectivity ($(psql_q 'SHOW server_version' | awk '{print $1}'))"
else
  bad "PostgreSQL connectivity"
fi

# 2. PostGIS extension available
if [ "$(psql_q "SELECT 1 FROM pg_extension WHERE extname='postgis'")" = "1" ]; then
  ok "PostGIS extension available ($(psql_q "SELECT extversion FROM pg_extension WHERE extname='postgis'"))"
else
  bad "PostGIS extension available"
fi

# 3. pgvector extension available (and operator works)
if [ "$(psql_q "SELECT 1 FROM pg_extension WHERE extname='vector'")" = "1" ] \
   && [ -n "$(psql_q "SELECT '[1,0]'::vector <=> '[0,1]'::vector")" ]; then
  ok "pgvector extension available ($(psql_q "SELECT extversion FROM pg_extension WHERE extname='vector'"))"
else
  bad "pgvector extension available"
fi

# 4. Redis connectivity
if [ "$("${DC[@]}" exec -T redis redis-cli ping 2>/dev/null | tr -d '\r')" = "PONG" ]; then
  ok "Redis connectivity"
else
  bad "Redis connectivity"
fi

echo
if [ "$fail" -eq 0 ]; then
  echo "All infrastructure checks passed."
else
  echo "Some infrastructure checks FAILED."
fi
exit "$fail"
