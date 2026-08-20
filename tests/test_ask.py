from app import app
def test_ask_rejects_missing_question():
    client = app.test_client()

    response = client.post(
        "/ask",
        json={
            "document_id": "test-document-id"
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "No question provided"