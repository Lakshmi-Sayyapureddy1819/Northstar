"""Database platform capability (Postgres + PostGIS + pgvector).

Owns connection/session management and the persistence port. Concrete
repositories live in each context's infrastructure layer. Adapter wiring
arrives with the first data-backed phase.
"""
