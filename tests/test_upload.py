import io
import os 
from unittest.mock import patch
from app import app


def test_upload_rejects_non_pdf():
    client = app.test_client()

    response = client.post(
        "/upload",
        data={
            "file": (
                io.BytesIO(b"This is not a PDF"),
                "test.txt"
            )
        },
        content_type="multipart/form-data"
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Only PDF files are allowed"

def test_upload_rejects_missing_file():
    client = app.test_client()

    response = client.post(
        "/upload",
        data={},
        content_type="multipart/form-data"
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "No file uploaded"

def test_upload_rejects_file_too_large():
    client = app.test_client()

    response = client.post(
        "/upload",
        data=b"0" * (10 * 1024 * 1024 + 1),
        content_type="application/pdf",
        content_length=10 * 1024 * 1024 + 1
    )

    assert response.status_code == 413

    data = response.get_json()

    assert data["error"] == (
        "PDF file is too large. Maximum allowed size is 10 MB."
    )

def test_upload_success():
    client = app.test_client()

    with patch(
        "app.ingest_pdf",
        return_value="test-document-id"
    ):
        response = client.post(
            "/upload",
            data={
                "file": (
                    io.BytesIO(b"%PDF-1.4 fake pdf content"),
                    "test.pdf"
                )
            },
            content_type="multipart/form-data"
        )

    assert response.status_code == 200

    data = response.get_json()

    assert data["message"] == (
        "PDF uploaded and ingested successfully"
    )

    assert data["document_id"] == "test-document-id"

def test_upload_ingestion_failure_deletes_file():
    client = app.test_client()

    upload_folder = "data/uploads"

    files_before = set(os.listdir(upload_folder))

    with patch(
        "app.ingest_pdf",
        side_effect=RuntimeError(
            "The AI embedding service is currently unavailable."
        )
    ):
        response = client.post(
            "/upload",
            data={
                "file": (
                    io.BytesIO(b"%PDF-1.4 fake pdf content"),
                    "test.pdf"
                )
            },
            content_type="multipart/form-data"
        )

    assert response.status_code == 503

    data = response.get_json()

    assert data["error"] == (
        "The AI embedding service is currently unavailable."
    )

    files_after = set(os.listdir(upload_folder))

    assert files_after == files_before