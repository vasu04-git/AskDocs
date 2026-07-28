const uploadBtn = document.getElementById("uploadBtn");
const sendBtn = document.getElementById("sendBtn");
const chatBox = document.getElementById("chatBox");
const uploadStatus = document.getElementById("uploadStatus");
const questionInput = document.getElementById("question");
const pdfFile = document.getElementById("pdfFile");

// ----------------------------
// Add Message to Chat
// ----------------------------
function addMessage(text, sender) {

    const message = document.createElement("div");
    message.className = `message ${sender}`;

    const bubble = document.createElement("div");
    bubble.className = "bubble";
    bubble.textContent = text;

    message.appendChild(bubble);

    chatBox.appendChild(message);

    chatBox.scrollTop = chatBox.scrollHeight;

    return bubble;
}


// ----------------------------
// Upload PDF
// ----------------------------
uploadBtn.addEventListener("click", async () => {

    if (pdfFile.files.length === 0) {
        alert("Please choose a PDF or TXT file.");
        return;
    }

    const formData = new FormData();
    formData.append("file", pdfFile.files[0]);

    uploadStatus.style.color = "#2563eb";
    uploadStatus.textContent = "Uploading document...";

    try {

        const response = await fetch("/upload", {
            method: "POST",
            body: formData
        });

        const result = await response.json();

        uploadStatus.style.color = "#16a34a";
        uploadStatus.textContent = result.message;

    } catch (error) {

        uploadStatus.style.color = "red";
        uploadStatus.textContent = "Upload failed.";

    }

});


// ----------------------------
// Ask Question
// ----------------------------
async function askQuestion() {

    const question = questionInput.value.trim();

    if (question === "")
        return;

    addMessage(question, "user");

    questionInput.value = "";

    // Temporary loading message
    const loadingBubble = addMessage("Thinking...", "bot");

    try {

        const response = await fetch("/ask", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                question: question
            })

        });

        const result = await response.json();

        loadingBubble.textContent = result.answer;

    } catch (error) {

        loadingBubble.textContent = "Something went wrong.";

    }

}


// ----------------------------
// Send Button
// ----------------------------
sendBtn.addEventListener("click", askQuestion);


// ----------------------------
// Press Enter
// ----------------------------
questionInput.addEventListener("keypress", function(e){

    if(e.key === "Enter"){
        askQuestion();
    }

});


// ----------------------------
// Welcome Message
// ----------------------------
window.onload = function(){

    addMessage(
        "👋 Welcome! Upload a PDF and ask me anything about it.",
        "bot"
    );

};