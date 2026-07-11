"""Geospatial platform capability (Mapbox and PostGIS-backed geo queries).

Owns the geo port; keeps map/provider SDKs out of the domain (ADR 0003).
Wiring arrives with the Data phase (map + nearby companies).
"""
