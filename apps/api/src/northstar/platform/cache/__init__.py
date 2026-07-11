"""Cache platform capability (Redis).

Owns the cache port and its adapter. Enables the anonymous-first, cacheable
Core tier (ADR 0004). Wiring arrives with the first cached read path.
"""
