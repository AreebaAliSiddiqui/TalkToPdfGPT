from flask import Flask, render_template, request, jsonify
from pipeline.ingest import ingest_pdf

import os
import uuid

from retrieval.retriever import retrieve
from generation.generator import generate_answer

app = Flask(__name__)

UPLOAD_FOLDER = "data/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_pdf():
    file = request.files.get("file")

    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if not file.filename.lower().endswith(".pdf"):
        return jsonify({"error": "Only PDF files are allowed"}), 400

    filename = f"{uuid.uuid4()}.pdf"
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    file.save(file_path)

    try:
        document_id = ingest_pdf(file_path)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify({
        "message": "PDF uploaded and ingested successfully",
        "document_id": document_id
    })

@app.route("/ask", methods=["POST"])
def ask_question():
    data = request.get_json()

    question = data.get("question")
    document_id = data.get("document_id")

    if not question:
        return jsonify({"error": "No question provided"}), 400

    if not document_id:
        return jsonify({"error": "No document selected"}), 400

    try:
        retrieved_chunks = retrieve(
            question,
            document_id  
        )
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500

    if not retrieved_chunks:
        return jsonify({
            "answer": "Your question doesn't seem to be answered by the active PDF."
        })
    # Here you would call your retrieval and answer generation logic
    try:
        answer = generate_answer(question, retrieved_chunks)
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({
    "answer": answer
})


if __name__ == "__main__":
    app.run(debug=True)