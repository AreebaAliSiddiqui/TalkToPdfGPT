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

    document_id = ingest_pdf(file_path)

    return jsonify({
        "message": "PDF uploaded and ingested successfully",
        "document_id": document_id
    })

@app.route("/ask", methods=["POST"])
def ask_question():
    data = request.get_json()
    question = data.get("question")

    if not question:
        return jsonify({"error": "No question provided"}), 400

    retrieved_chunks = retrieve(question)
   
    # Here you would call your retrieval and answer generation logic
    retrieved_chunks = retrieve(question)

    answer = generate_answer(question, retrieved_chunks)

    return jsonify({
    "answer": answer
})


if __name__ == "__main__":
    app.run(debug=True)