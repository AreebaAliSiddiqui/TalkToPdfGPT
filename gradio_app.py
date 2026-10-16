
import os

import gradio as gr

from pipeline.ingest import ingest_pdf
from retrieval.retriever import retrieve
from generation.generator import generate_answer


MAX_PDF_SIZE = 10 * 1024 * 1024


def process_pdf(file_path):
    if not file_path:
        return "Please upload a PDF first.", None

    if not file_path.lower().endswith(".pdf"):
        return "Only PDF files are supported.", None

    if os.path.getsize(file_path) > MAX_PDF_SIZE:
        return "PDF exceeds the 10 MB size limit.", None

    try:
        document_id = ingest_pdf(file_path)
        return (
            "PDF processed successfully! You can now ask questions.",
            document_id,
        )
    except ValueError as exc:
        return str(exc), None
    except RuntimeError as exc:
        return str(exc), None
    except Exception:
        return (
            "Something went wrong while processing the PDF. "
            "Check the Space logs for details.",
            None,
        )


def answer_question(question, document_id):
    if not document_id:
        return "Please upload and process a PDF first.", ""

    if not question or not question.strip():
        return "Please enter a question.", ""

    try:
        chunks = retrieve(question.strip(), document_id)

        if not chunks:
            return (
                "Your question doesn't seem to be answered by the active PDF.",
                "",
            )

        answer = generate_answer(question.strip(), chunks)

        source_lines = [
            f"- Page {chunk['page_number']}, "
            f"chunk {chunk['chunk_number']}"
            for chunk in chunks
        ]

        sources = "\n".join(source_lines)
        return answer, sources

    except RuntimeError as exc:
        return f"Unable to process your question: {exc}", ""
    except Exception:
        return (
            "Something went wrong while answering. "
            "Check the Space logs for details.",
            "",
        )


with gr.Blocks(title="TalktoPdfGPT") as demo:
    gr.Markdown(
        """
        # TalktoPdfGPT
        Upload a PDF and ask questions about its contents.
        Answers are generated using retrieved PDF passages.
        """
    )

    document_state = gr.State(value=None)

    pdf_file = gr.File(
        label="Upload your PDF",
        file_types=[".pdf"],
        type="filepath",
    )

    process_button = gr.Button("Process PDF", variant="primary")
    upload_status = gr.Textbox(label="Document status", interactive=False)

    process_button.click(
        fn=process_pdf,
        inputs=[pdf_file],
        outputs=[upload_status, document_state],
    )

    question = gr.Textbox(
        label="Your question",
        placeholder="Ask something about your PDF...",
    )

    ask_button = gr.Button("Ask", variant="primary")
    answer = gr.Markdown(label="Answer")
    sources = gr.Markdown(label="Retrieved sources")

    ask_button.click(
        fn=answer_question,
        inputs=[question, document_state],
        outputs=[answer, sources],
    )

    question.submit(
        fn=answer_question,
        inputs=[question, document_state],
        outputs=[answer, sources],
    )


if __name__ == "__main__":
    demo.launch()
