import io

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