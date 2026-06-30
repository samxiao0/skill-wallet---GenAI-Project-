from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_home():

    response = client.get("/")

    assert response.status_code == 200


def test_generate():

    payload = {
        "description": "AI conference on Cloud Computing",
        "interests": ["AI", "Machine Learning"]
    }

    response = client.post(
        "/generate",
        json=payload
    )

    assert response.status_code == 200

    data = response.json()

    assert "topics" in data
    assert "suggestions" in data


def test_fact_check():

    response = client.post(
        "/fact-check",
        json={
            "query": "Artificial Intelligence"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "summary" in data