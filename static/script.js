

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

    const clearChatButton =
    document.getElementById("clear-chat");

    const askButton =
    questionForm.querySelector("button");

    const activeDocumentName =
    document.getElementById("active-document-name");

    const replaceDocumentButton =
    document.getElementById("replace-document-button");

    function setUploadStatus(message, statusType) {

    uploadStatus.textContent = message;

    uploadStatus.classList.remove(
        "status-processing",
        "status-success",
        "status-error"
    );

    if (statusType) {
        uploadStatus.classList.add(statusType);
    }
}
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

            setUploadStatus(
    "Uploading and processing PDF...",
    "status-processing"
);

            documentStatus.style.display = "none";

            const formData = new FormData();

            formData.append("file", file);

            const uploadButton =
    uploadForm.querySelector("button");


            try {

                uploadButton.disabled = true;
uploadButton.textContent = "Processing...";
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

                   setUploadStatus(
    result.error || "Upload failed.",
    "status-error"
); 

                    return;
                }


                activeDocumentId =
                    result.document_id;

                activeDocumentName.textContent =
    file.name;


                setUploadStatus(
    "PDF uploaded successfully!",
    "status-success"
);


                documentStatus.style.display =
                    "block";


                console.log(
                    "Active document ID:",
                    activeDocumentId
                );


            } catch (error) {

                setUploadStatus(
    "Something went wrong while uploading the PDF.",
    "status-error"
);

                console.error(error);
            }
            finally{
                uploadButton.disabled = false;
uploadButton.textContent = "Upload PDF";
            }
        }
    );

    replaceDocumentButton.addEventListener(
    "click",
    () => {

        activeDocumentId = null;

        activeDocumentName.textContent = "";

        documentStatus.style.display = "none";

        fileInput.value = "";

        chatMessages.innerHTML = `
            <div
                id="empty-chat"
                class="empty-chat"
            >
                <p>
                    Upload a PDF to start chatting with it.
                </p>
            </div>
        `;

        uploadStatus.textContent = "";

        questionInput.value = "";

        console.log("Active document cleared.");
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
        "ai-message loading-message"
    );

            try {
                const askButton =
    questionForm.querySelector("button");

askButton.disabled = true;
askButton.textContent = "Thinking...";
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

                   setMessageError(
    loadingMessage,
    result.error ||
    "Unable to answer the question."
);

                    return;
                }


                loadingMessage.textContent =
    result.answer;

if (result.sources && result.sources.length > 0) {
    addSources(
        loadingMessage.parentElement,
        result.sources
    );
}


            } catch (error) {

                const messages =
                    chatMessages.querySelectorAll(
                        ".ai-message"
                    );

                const loadingMessage =
                    messages[messages.length - 1];

                setMessageError(
    loadingMessage,
    "Something went wrong while asking the question."
);

                console.error(error);
            } finally{
                askButton.disabled = false;
askButton.textContent = "Ask";
            }

        }
    );


    // -------------------------
    // Add Chat Message
    // -------------------------

 function addMessage(text, className) {

    const currentEmptyChat =
    document.getElementById("empty-chat");

if (currentEmptyChat) {
    currentEmptyChat.remove();
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
    ...className.split(" ")
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

    return message;
    }

function addSources(wrapper, sources) {

    const uniquePages = [
        ...new Set(
            sources.map(
                source => source.page_number
            )
        )
    ];

    const sourcesContainer =
        document.createElement("div");

    sourcesContainer.classList.add(
        "sources-container"
    );

    const sourcesTitle =
        document.createElement("div");

    sourcesTitle.classList.add(
        "sources-title"
    );

    sourcesTitle.textContent =
        "Sources";

    sourcesContainer.appendChild(
        sourcesTitle
    );


    const sourcesList =
        document.createElement("div");

    sourcesList.classList.add(
        "sources-list"
    );


    uniquePages.forEach(pageNumber => {

        const sourceCard =
            document.createElement("div");

        sourceCard.classList.add(
            "source-card"
        );

        sourceCard.textContent =
            `Page ${pageNumber}`;

        sourcesList.appendChild(
            sourceCard
        );
    });


    sourcesContainer.appendChild(
        sourcesList
    );

    wrapper.appendChild(
        sourcesContainer
    );
}



     clearChatButton.addEventListener(
    "click",
    () => {

        chatMessages.innerHTML = `
            <div
                id="empty-chat"
                class="empty-chat"
            >
                <p>
                    Upload a PDF to start chatting with it.
                </p>
            </div>
        `;

        questionInput.value = "";
    }
);

function setMessageError(messageElement, text) {

    messageElement.textContent = text;

    messageElement.classList.remove("ai-message");
    messageElement.classList.add("error-message");
}