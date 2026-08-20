from app import app
from unittest.mock import patch
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
def test_ask_rejects_missing_document():
    client = app.test_client()

    response = client.post(
        "/ask",
        json={
            "question": "What is this document about?"
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "No document selected"

    


def test_ask_retrieval_failure_returns_503():
    client = app.test_client()

    with patch(
        "app.retrieve",
        side_effect=RuntimeError(
            "The retrieval service is currently unavailable."
        )
    ):
        response = client.post(
            "/ask",
            json={
                "question": "What is this document about?",
                "document_id": "test-document-id"
            }
        )

    assert response.status_code == 503

    data = response.get_json()

    assert data["error"] == (
        "The retrieval service is currently unavailable."
    )
def test_ask_returns_fallback_when_no_chunks_found():
    client = app.test_client()

    with patch(
        "app.retrieve",
        return_value=[]
    ):
        response = client.post(
            "/ask",
            json={
                "question": "What is this document about?",
                "document_id": "test-document-id"
            }
        )

    assert response.status_code == 200

    data = response.get_json()

    assert data["answer"] == (
        "Your question doesn't seem to be answered by the active PDF."
    )