

    // -------------------------
    // Active Document
    // -------------------------

    let activeDocumentId = null;


    // -------------------------
    // Elements
    // -------------------------

    const uploadForm =
        document.getElementById("upload-form");

    const fileInput =
        document.getElementById("pdf-file");

    const uploadStatus =
        document.getElementById("upload-status");

    const documentStatus =
        document.getElementById("document-status");

    const questionForm =
        document.getElementById("question-form");

    const questionInput =
        document.getElementById("question");

    const chatMessages =
        document.getElementById("chat-messages");

    const emptyChat =
        document.getElementById("empty-chat");


    // -------------------------
    // PDF Upload
    // -------------------------

    uploadForm.addEventListener(
        "submit",
        async (event) => {

            event.preventDefault();

            const file = fileInput.files[0];

            if (!file) {

                uploadStatus.textContent =
                    "Please select a PDF.";

                return;
            }

            uploadStatus.textContent =
                "Uploading and processing PDF...";

            documentStatus.style.display = "none";

            const formData = new FormData();

            formData.append("file", file);


            try {

                const response = await fetch(
                    "/upload",
                    {
                        method: "POST",
                        body: formData
                    }
                );

                const result =
                    await response.json();


                if (!response.ok) {

                    uploadStatus.textContent =
                        result.error ||
                        "Upload failed.";

                    return;
                }


                activeDocumentId =
                    result.document_id;


                uploadStatus.textContent =
                    "PDF uploaded successfully!";


                documentStatus.style.display =
                    "block";


                console.log(
                    "Active document ID:",
                    activeDocumentId
                );


            } catch (error) {

                uploadStatus.textContent =
                    "Something went wrong while uploading the PDF.";

                console.error(error);
            }

        }
    );


    // -------------------------
    // Ask Question
    // -------------------------

    questionForm.addEventListener(
        "submit",
        async (event) => {

            event.preventDefault();

            const question =
                questionInput.value.trim();


            if (!activeDocumentId) {

                addMessage(
                    "Please upload a PDF first.",
                    "ai-message"
                );

                return;
            }


            if (!question) {

                return;
            }


            addMessage(
                question,
                "user-message"
            );


            questionInput.value = "";


            const loadingMessage =
    addMessage(
        "Thinking...",
        "ai-message"
    );


            try {

                const response =
                    await fetch(
                        "/ask",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body: JSON.stringify({
                                question: question,
                                document_id:
                                    activeDocumentId
                            })
                        }
                    );


                const result =
                    await response.json();


                

                if (!response.ok) {

                    loadingMessage.textContent =
                        result.error ||
                        "Unable to answer the question.";

                    return;
                }


                loadingMessage.textContent =
                    result.answer;


            } catch (error) {

                const messages =
                    chatMessages.querySelectorAll(
                        ".ai-message"
                    );

                const loadingMessage =
                    messages[messages.length - 1];

                loadingMessage.textContent =
                    "Something went wrong while asking the question.";

                console.error(error);
            }

        }
    );


    // -------------------------
    // Add Chat Message
    // -------------------------

 function addMessage(text, className) {

    if (emptyChat) {
        emptyChat.remove();
    }

    const wrapper =
        document.createElement("div");

    const message =
        document.createElement("div");

    const label =
        document.createElement("div");


    wrapper.classList.add(
        "message-wrapper"
    );


    message.classList.add(
        "message",
        className
    );


    if (className === "user-message") {

        wrapper.classList.add("user");

        label.textContent = "You";

    } else {

        wrapper.classList.add("ai");

        label.textContent = "TalktoPdfGPT";
    }


    label.classList.add(
        "message-label"
    );


    message.textContent = text;


    wrapper.appendChild(label);
    wrapper.appendChild(message);

    chatMessages.appendChild(wrapper);


    chatMessages.scrollTop =
        chatMessages.scrollHeight;
}
return message;
