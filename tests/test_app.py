import uuid
from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # basic sanity: known activity should exist
    assert "Chess Club" in data


def test_signup_and_unregister():
    email = f"test-{uuid.uuid4()}@example.com"

    # Sign up for Chess Club
    resp = client.post(f"/activities/Chess Club/signup?email={email}")
    assert resp.status_code == 200
    assert "Signed up" in resp.json().get("message", "")

    # Verify participant appears
    resp = client.get("/activities")
    participants = resp.json()["Chess Club"].get("participants", [])
    assert email in participants

    # Unregister and verify removal
    resp = client.post(f"/activities/Chess Club/unregister?email={email}")
    assert resp.status_code == 200
    resp = client.get("/activities")
    participants = resp.json()["Chess Club"].get("participants", [])
    assert email not in participants


def test_prevent_duplicate_signup():
    email = f"test-{uuid.uuid4()}@example.com"

    # First signup should succeed
    resp = client.post(f"/activities/Chess Club/signup?email={email}")
    assert resp.status_code == 200

    # Second signup should fail with 400
    resp = client.post(f"/activities/Chess Club/signup?email={email}")
    assert resp.status_code == 400

    # Cleanup: remove the test user
    resp = client.post(f"/activities/Chess Club/unregister?email={email}")
    assert resp.status_code == 200
