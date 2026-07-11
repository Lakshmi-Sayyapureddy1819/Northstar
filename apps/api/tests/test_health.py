"""API smoke test — the /health endpoint boots and responds."""

from fastapi.testclient import TestClient

from northstar.main import app

client = TestClient(app)


def test_health_returns_ok():
    resp = client.get("/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert body["app_name"]
    assert body["environment"]
