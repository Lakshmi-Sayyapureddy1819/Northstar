# NorthStar local PostgreSQL — PostGIS + pgvector on PostgreSQL 16.
#
# ADR 0003 (Cloud-Agnostic Infrastructure): local-first image for development.
# No single official image bundles both PostGIS and pgvector, so we extend the
# PostGIS image and add pgvector from the PGDG apt repo (already configured in
# the base image). In production this is swapped for a managed equivalent
# (e.g. a Postgres service with both extensions enabled) — config, not code.
FROM postgis/postgis:16-3.4

RUN apt-get update \
    && apt-get install -y --no-install-recommends postgresql-16-pgvector \
    && rm -rf /var/lib/apt/lists/*
