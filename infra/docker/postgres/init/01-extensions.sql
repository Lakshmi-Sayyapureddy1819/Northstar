-- Enable required PostgreSQL extensions in the application database.
-- Runs once on first cluster initialization (docker-entrypoint-initdb.d).
-- Idempotent so it is safe to re-run.
--
--   postgis  — geospatial types/queries for hyperlocal navigation.
--   vector   — embedding storage/search (reserved for future AI features).
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS vector;
