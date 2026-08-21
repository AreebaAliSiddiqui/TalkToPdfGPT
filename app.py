from flask import Flask, render_template, request, jsonify
from pipeline.ingest import ingest_pdf

import os
import uuid

from retrieval.retriever import retrieve
from generation.generator import generate_answer

app = Flask(__name__)

app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10 MB

UPLOAD_FOLDER = os.path.join(app.root_path, "data", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.errorhandler(413)
def file_too_large(error):
    return jsonify({
        "error": "PDF file is too large. Maximum allowed size is 10 MB."
    }), 413


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
        if os.path.exists(file_path):
            os.remove(file_path)

        return jsonify({"error": str(e)}), 400

    except RuntimeError as e:
        if os.path.exists(file_path):
            os.remove(file_path)

        return jsonify({
            "error": str(e)
        }), 503

    except Exception:
        if os.path.exists(file_path):
            os.remove(file_path)

        return jsonify({
            "error": "Something went wrong while processing the PDF."
        }), 500

    return jsonify({
        "message": "PDF uploaded and ingested successfully",
        "document_id": document_id
    })


@app.route("/ask", methods=["POST"])
def ask_question():
    data = request.get_json(silent=True) or {}


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
        return jsonify({"error": str(e)}), 503

    except Exception:
        return jsonify({
            "error": "Something went wrong while retrieving information."
        }), 500

    if not retrieved_chunks:
        return jsonify({
            "answer": "Your question doesn't seem to be answered by the active PDF."
        })

    try:
        answer = generate_answer(question, retrieved_chunks)

    except RuntimeError as e:
        return jsonify({"error": str(e)}), 503

    except Exception:
        return jsonify({
            "error": "Something went wrong while generating the answer."
        }), 500

    sources = []

    for chunk in retrieved_chunks:
        sources.append({
            "page_number": chunk["page_number"],
            "chunk_number": chunk["chunk_number"]
    })
    return jsonify({
    "answer": answer,
    "sources":sources
})


if __name__ == "__main__":
    app.run()

