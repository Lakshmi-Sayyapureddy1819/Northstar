"""Export the FastAPI OpenAPI schema to the api-contracts package.

Backend owns the contract (ADR 0008). This script is the single source of the
OpenAPI document: it imports the real application, serializes `app.openapi()`,
and writes it to `packages/api-contracts/openapi.json`. The TypeScript types the
frontend consumes are generated from that file — never hand-written.

Run via: `uv run python scripts/export_openapi.py` (or the `export-openapi`
project script). Deterministic output (sorted keys) so a no-op run produces no
git diff and a real contract change produces a reviewable one.
"""

from __future__ import annotations

import json
from pathlib import Path

from northstar.main import app

# apps/api/scripts/export_openapi.py -> repo root is three parents up.
REPO_ROOT = Path(__file__).resolve().parents[3]
OUTPUT = REPO_ROOT / "packages" / "api-contracts" / "openapi.json"


def main() -> None:
    schema = app.openapi()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(schema, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    paths = ", ".join(sorted(schema.get("paths", {})))
    print(f"Wrote {OUTPUT.relative_to(REPO_ROOT)} (paths: {paths})")


if __name__ == "__main__":
    main()
