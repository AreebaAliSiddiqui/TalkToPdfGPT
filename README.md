# TalktoPdfGPT

> A Retrieval-Augmented Generation (RAG) chatbot that lets users upload a PDF and ask questions about its content.

TalktoPdfGPT is a full-stack AI application built with Flask, Google Gemini, and ChromaDB. It processes uploaded PDF documents, converts their content into searchable vector representations, retrieves the most relevant document chunks for a user's question, and generates an answer grounded in the retrieved context.

The application is designed to keep answers tied to the uploaded document rather than relying solely on the language model's general knowledge.

## Features

* 📄 **PDF Upload**

  * Upload PDF documents directly through the web interface.
  * Rejects non-PDF files.
  * Rejects missing or empty file submissions.
  * Enforces a 10 MB upload limit.

* 🔍 **Document Processing**

  * Extracts text from PDFs using `pypdf`.
  * Splits extracted text into manageable chunks.
  * Generates embeddings for document chunks using Google's Gemini embedding model.
  * Stores embeddings in ChromaDB.

* 💬 **RAG Question Answering**

  * Ask questions about the currently selected PDF.
  * Retrieves relevant chunks from the active document.
  * Generates answers using Google Gemini.
  * Returns source page and chunk references alongside answers.

* 📚 **Document Isolation**

  * Tracks the active document using a unique document ID.
  * Retrieval is restricted to the selected document.
  * Prevents accidental cross-document retrieval.

* 🛡️ **Error Handling**

  * Handles invalid uploads.
  * Handles oversized files.
  * Handles ingestion failures.
  * Cleans up uploaded files when ingestion fails.
  * Handles retrieval and generation failures.
  * Returns appropriate HTTP error responses.

* 🎨 **Chat Interface**

  * Separate HTML, CSS, and JavaScript files.
  * Interactive upload status.
  * Chat-style question and answer interface.
  * Loading state while generating answers.
  * Clear chat functionality.
  * Source display for retrieved document content.
  * Responsive layout for smaller screens.

* 🧪 **Automated Testing**

  * Pytest test suite covering application setup, upload validation, successful uploads, ingestion failures, and `/ask` endpoint validation and failure handling.
  * Current test suite: **11 tests passing**.

## How It Works

TalktoPdfGPT follows a standard Retrieval-Augmented Generation pipeline:

```text
                    ┌─────────────────┐
                    │    PDF Upload   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   PDF Parsing   │
                    │     pypdf       │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Text Chunking   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    Gemini       │
                    │   Embeddings    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    ChromaDB     │
                    │  Vector Store   │
                    └─────────────────┘


User Question
      │
      ▼
┌─────────────────┐
│  Query Embedding│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Chroma Retrieval│
│ Active Document │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Retrieved Chunks│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Gemini Generator│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Answer + Sources│
└─────────────────┘
```

## Tech Stack

### Backend

* Python
* Flask
* Gunicorn

### AI / RAG

* Google Gemini
* Google GenAI Python SDK
* Gemini embeddings
* ChromaDB
* LangChain text splitters

### Document Processing

* pypdf

### Frontend

* HTML
* CSS
* JavaScript

### Testing

* pytest

### Configuration

* python-dotenv
* Environment variables for API credentials

## Project Structure

```text
TalktoPdfGPT/
│
├── app.py
│
├── embeddings/
│   └── embedder.py
│
├── generation/
│   └── generator.py
│
├── ingestion/
│   ├── chunker.py
│   └── pdf_loader.py
│
├── pipeline/
│   └── ingest.py
│
├── retrieval/
│   └── retriever.py
│
├── vectorstore/
│   └── chroma_store.py
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   └── script.js
│
├── tests/
│   ├── test_ask.py
│   ├── test_smoke.py
│   └── test_upload.py
│
├── data/
│   └── uploads/
│
├── chroma_db/
│
├── .env
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone <repository-url>
cd TalktoPdfGPT
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

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

The `.env` file is intentionally excluded from version control.

### 5. Run the application

For local development:

```bash
python app.py
```

The application will be available at:

```text
http://127.0.0.1:5000
```

## Running Tests

Run the complete test suite with:

```bash
pytest
```

The project currently contains **11 automated tests** covering:

* Application test configuration
* Missing upload files
* Empty filenames
* Non-PDF uploads
* Oversized PDF uploads
* Successful PDF uploads
* Ingestion failure cleanup
* Missing questions
* Missing document IDs
* Retrieval failures
* Generation failure handling

Expected result:

```text
11 passed
```

## Error Handling

TalktoPdfGPT uses explicit HTTP responses for common failure cases.

| Situation                          | HTTP Status |
| ---------------------------------- | ----------: |
| Missing uploaded file              |       `400` |
| Empty filename                     |       `400` |
| Non-PDF file                       |       `400` |
| Missing question                   |       `400` |
| Missing document                   |       `400` |
| File exceeds 10 MB                 |       `413` |
| AI / embedding service unavailable |       `503` |
| Retrieval failure                  |       `503` |
| Generation failure                 |       `503` |
| Unexpected server error            |       `500` |

Uploaded files are also removed when document ingestion fails, preventing failed uploads from being left behind on disk.

## Source Attribution

When relevant chunks are retrieved successfully, the application returns source metadata including:

* Page number
* Chunk number

This allows the interface to show where the generated answer was derived from within the uploaded document.

## Security and Configuration

The application keeps sensitive configuration outside the repository using environment variables.

The following are excluded from version control:

```text
.env
data/
chroma_db/
.venv/
__pycache__/
```

API credentials should never be committed to the repository.

For a public GitHub repository, GitHub recommends enabling available security features such as secret scanning, push protection, Dependabot alerts, and code scanning where appropriate.

## Current Status

### Application Development

**Complete — v1.0**

* Core Flask application ✅
* PDF ingestion pipeline ✅
* Text chunking ✅
* Gemini embeddings ✅
* ChromaDB vector storage ✅
* Document-specific retrieval ✅
* Gemini answer generation ✅
* Source references ✅
* Chat interface ✅
* Upload validation ✅
* Error handling ✅
* Automated test suite ✅
* Production debug mode disabled ✅
* Dependency cleanup ✅

### Deployment

**Pending**

The application is production-configured at the code level, but a live deployment has not yet been completed.

The remaining work is infrastructure-specific:

* Hosting provider
* Persistent storage
* Production environment variables
* Production deployment
* Live end-to-end verification

The local application and automated test suite are complete independently of the deployment environment.

## Future Improvements

Potential improvements for future versions include:

* Persistent cloud object storage for uploaded documents
* Managed vector database or persistent Chroma deployment
* User authentication
* Multiple document management
* Conversation persistence
* Streaming model responses
* Improved source citation UI
* PDF page previews
* Rate limiting
* Production monitoring and logging
* CI/CD pipeline
* Automated deployment

## Why RAG?

A general-purpose LLM can answer many questions about text supplied directly in a prompt, but a dedicated RAG pipeline provides an application-level retrieval layer between the user's question and the language model.

TalktoPdfGPT uses this layer to:

1. Identify relevant sections of the uploaded document.
2. Restrict retrieval to the active document.
3. Provide those sections as context to the generator.
4. Return source metadata with the response.

This makes the document-grounding behavior explicit and testable within the application architecture.


## Author

**Areeba Ali Siddiqui**

Computer Science student and AI/ML developer.

---

### Project Focus

`Python` · `Flask` · `RAG` · `LLMs` · `Gemini` · `ChromaDB` · `PDF Processing` · `AI Engineering`
