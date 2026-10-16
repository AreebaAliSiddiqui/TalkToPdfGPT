---
title: TalktoPdfGPT
emoji: 📚
colorFrom: blue
colorTo: purple
sdk: gradio
app_file: gradio_app.py
pinned: false
---

# TalktoPdfGPT

**A Retrieval-Augmented Generation (RAG) application that lets users upload a PDF and ask questions grounded in its content.**

🔗 **Live Demo:** [Try TalktoPdfGPT](https://talktopdfgpt-ddd53.containers.snapdeploy.app)

TalktoPdfGPT is an AI application built with Python, Google Gemini, and ChromaDB. It processes PDF documents, converts their content into searchable vector representations, retrieves relevant document chunks, and generates answers grounded in the retrieved context.

The application is designed to answer questions using the selected document rather than relying solely on the language model's general knowledge. When relevant information cannot be found, it can report that the information was not found in the provided PDF.

## Features

### 📄 PDF Upload
- Upload PDF documents through the web interface.
- Validate file types and reject missing or empty submissions.
- Enforce a 10 MB upload limit.

### 🔍 Document Processing
- Extract text from PDFs using `pypdf`.
- Split extracted text into manageable chunks.
- Generate embeddings using Google's Gemini embedding model.
- Store document embeddings in ChromaDB for similarity-based retrieval.

### 💬 RAG Question Answering
- Ask questions about the uploaded PDF.
- Retrieve relevant document chunks for each question.
- Generate context-grounded answers using Google Gemini.
- Display source page and chunk references alongside answers.
- Handle questions whose answers are not found in the document.

### 📚 Document Isolation
- Associate retrieval with the active document.
- Restrict retrieval to the selected document to prevent unintended cross-document results.

### 🛡️ Error Handling
- Validate invalid, empty, and oversized uploads.
- Handle ingestion, retrieval, and generation failures.
- Clean up uploaded files when ingestion fails.
- Return appropriate error responses in the Flask application.

### 🎨 User Interface
- Interactive PDF upload and status feedback.
- Chat-style question-and-answer interface.
- Loading indicators during answer generation.
- Clear chat functionality.
- Source references for retrieved document content.
- Responsive layout for smaller screens.

### 🧪 Automated Testing
The Flask application includes a pytest suite covering application setup, upload validation, successful uploads, ingestion failures, and question-answering endpoint validation and failure handling.

**Reported test status:** 11 tests passing.

## Live Demo

**[Open TalktoPdfGPT](https://talktopdfgpt-ddd53.containers.snapdeploy.app)**

The application has been deployed on SnapDeploy and tested with a live PDF upload and question-answering workflow. An unrelated question about Friedrich Nietzsche returned a message indicating that the information was not found in the provided PDF, demonstrating the intended document-grounding behavior for that test.

The free deployment may sleep after 15 minutes of inactivity, so the first request after idle time may take longer to respond.

## How It Works

TalktoPdfGPT follows a Retrieval-Augmented Generation pipeline.

### Document ingestion

1. **PDF upload:** The user uploads a document.
2. **PDF parsing:** `pypdf` extracts the document's text.
3. **Text chunking:** The extracted text is divided into manageable chunks.
4. **Embedding generation:** Gemini converts chunks into vector representations.
5. **Vector storage:** ChromaDB stores the vectors and associated document metadata.

### Question answering

1. **Question input:** The user asks a question about the PDF.
2. **Query embedding:** The question is converted into a vector representation.
3. **Similarity retrieval:** ChromaDB retrieves relevant chunks from the active document.
4. **Context construction:** The retrieved text is provided to the language model.
5. **Answer generation:** Gemini generates an answer based on the retrieved context.
6. **Source attribution:** The application returns page and chunk references where available.

```text
PDF Upload
    |
    v
PDF Parsing (pypdf)
    |
    v
Text Chunking
    |
    v
Gemini Embeddings
    |
    v
ChromaDB Vector Store


User Question
    |
    v
Query Embedding
    |
    v
Relevant Chunk Retrieval
    |
    v
Context-Grounded Gemini Answer
    |
    v
Answer + Source References
```

## Tech Stack

| Component | Technologies |
|---|---|
| Language | Python |
| Original web application | Flask |
| Alternative deployment interface | Gradio |
| AI model and embeddings | Google Gemini |
| GenAI integration | Google GenAI Python SDK |
| Vector database | ChromaDB |
| Text chunking | LangChain Text Splitters |
| PDF processing | pypdf |
| Frontend | HTML, CSS, JavaScript |
| Testing | pytest |
| Configuration | python-dotenv |
| Containerization | Docker |
| Hosting | SnapDeploy |

## Project Structure

```text
TalktoPdfGPT/
├── app.py
├── gradio_app.py
├── pipeline/
│   └── ingest.py
├── ingestion/
│   ├── chunker.py
│   └── pdf_loader.py
├── embeddings/
│   └── embedder.py
├── retrieval/
│   └── retriever.py
├── generation/
│   └── generator.py
├── vectorstore/
│   └── chroma_store.py
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── script.js
├── tests/
│   ├── test_ask.py
│   ├── test_smoke.py
│   └── test_upload.py
├── Dockerfile
├── .dockerignore
├── .gitignore
├── requirements.txt
└── README.md
```

*Note: Local data and generated vector-store files may be created at runtime and are excluded from the repository.*

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/AreebaAliSiddiqui/TalkToPdfGPT.git
cd TalkToPdfGPT
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Replace the placeholder with your own Gemini API key. Never commit the `.env` file or expose API credentials publicly.

### 5. Run the application

For the original Flask interface:

```bash
python app.py
```

For the Gradio interface used by the Docker deployment:

```bash
python gradio_app.py
```

The Flask application is typically available at `http://127.0.0.1:5000`. The Gradio application's port is configurable through the `PORT` environment variable and defaults to `7860` when no port is supplied.

## Running Tests

Run the test suite with:

```bash
pytest
```

The existing test suite covers cases including:

- Application setup
- Missing upload files and empty filenames
- Invalid file types
- Oversized PDF uploads
- Successful PDF uploads
- Cleanup after ingestion failures
- Missing questions and document IDs
- Retrieval and generation failures

**Expected result:** 11 passing tests, based on the current reported test status.

## Error Handling

The Flask application defines explicit responses for common failure conditions.

| Situation | HTTP status |
|---|---:|
| Missing uploaded file | 400 |
| Empty filename | 400 |
| Non-PDF file | 400 |
| Missing question | 400 |
| Missing document | 400 |
| File exceeds 10 MB | 413 |
| AI or embedding service unavailable | 503 |
| Retrieval failure | 503 |
| Generation failure | 503 |
| Unexpected server error | 500 |

Uploaded files are also removed when ingestion fails, helping prevent failed uploads from being left behind on disk.

## Source Attribution

When relevant document chunks are retrieved, the application can return source metadata including:

- Page number
- Chunk number

These references help users identify where the retrieved information originated in the uploaded PDF.

## Security and Configuration

Sensitive configuration is supplied through environment variables rather than committed to the repository.

The following should remain excluded from version control:

```text
.env
.venv/
__pycache__/
chroma_db/
data/
```

API credentials should never be committed to GitHub. Production deployments should configure secrets through the hosting provider's environment-variable settings.

## Current Status

### Application Development

- [x] PDF ingestion pipeline
- [x] Text extraction and chunking
- [x] Gemini embedding generation
- [x] ChromaDB vector storage
- [x] Document-specific retrieval
- [x] Gemini answer generation
- [x] Source references
- [x] Interactive question-answering interface
- [x] Upload validation and error handling
- [x] Automated test suite

### Deployment

- [x] Docker configuration
- [x] Public SnapDeploy deployment
- [x] Production environment variables configured
- [x] Live PDF upload tested
- [x] Live question answering tested
- [x] Out-of-document question tested

**Status: Deployed and live-tested.**

## Future Improvements

Potential improvements for future versions include:

- Persistent cloud storage for uploaded documents
- Managed vector database or durable vector-store persistence
- User authentication
- Multi-document management
- Conversation history
- Streaming model responses
- Improved source citation interface
- PDF page previews
- Rate limiting and usage controls
- Production monitoring and logging
- Continuous integration and deployment

## Why RAG?

A general-purpose language model can answer questions about text supplied directly in a prompt. Retrieval-Augmented Generation adds an explicit retrieval layer that selects relevant information from a document before the model generates its response.

TalktoPdfGPT uses this architecture to:

- Find relevant sections of an uploaded PDF.
- Restrict retrieval to the selected document.
- Provide retrieved passages as context to Gemini.
- Return source metadata with answers.
- Test how the application responds when information is not found.

This makes document-grounded question answering an explicit part of the application's design.

## Author

**Areeba Ali Siddiqui**

Computer Science student and AI/ML developer.

**Project focus:** Python · RAG · LLMs · Google Gemini · ChromaDB · PDF Processing · AI Engineering
