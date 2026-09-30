// ------------------------------------------------------------
// Chat input
// ------------------------------------------------------------

document
    .getElementById("user-input")
    .addEventListener("keydown", function(event) {

        if (event.key === "Enter") {

            event.preventDefault();

            processInput();
        }
    });


// ------------------------------------------------------------
// Process user input
// ------------------------------------------------------------

async function processInput() {

    const inputField = document.getElementById("user-input");

    const inputText = inputField.value.trim();

    if (!inputText) {
        return;
    }

    // Display user's message
    displayMessage(
        inputText,
        "user"
    );

    // Clear input
    inputField.value = "";

    // Send message to Semion
    await processSLM(inputText);
}


// ------------------------------------------------------------
// Send message to server
// ------------------------------------------------------------

async function processSLM(input) {

    try {

        const response =
            await fetch("/api/chat", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    message: input
                })
            });


        if (!response.ok) {

            throw new Error(
                `Server returned ${response.status}`
            );
        }


        const result = await response.json();


        // Display Semion's response
        displayMessage(
            result.response,
            "bot"
        );


        // Log semantic information
        if (result.confidence > 0.7) {
            console.log(`Command: ${result.command}\nConfidence: ${Math.round(result.confidence*100)}%`);
        } else {
            console.warn(`Command: ${result.command}\nConfidence: ${Math.round(result.confidence*100)}%`);
        }

    } catch (error) {

        console.error(
            "Unable to communicate with Semion:",
            error
        );


        displayMessage(
            "I'm having trouble connecting to my semantic model.",
            "bot"
        );
    }
}


// ------------------------------------------------------------
// Display messages
// ------------------------------------------------------------

function displayMessage(
    message,
    sender = "bot"
) {

    const chatbox =
        document.getElementById("chatbox");


    const element =
        document.createElement("p");


    element.className =
        `${sender === "bot"
            ? "bot"
            : "user"}-message message`;


    element.textContent =
        message;


    chatbox.appendChild(
        element
    );


    chatbox.scrollTop =
        chatbox.scrollHeight;
}


// ------------------------------------------------------------
// Start Semion
// ------------------------------------------------------------

async function startSemion() {

    try {

        const response = await fetch("/api/status");


        if (!response.ok) {
            throw new Error("Server unavailable");
        }


        console.log("Semion server online.");

        res = await response.json()
        console.log(res);

        displayMessage(
            "Hello! My name is Semion. How can I help you today?",
            "bot"
        );


        document
            .getElementById("user-input")
            .focus();


    } catch (error) {

        console.error(
            "Unable to connect to Semion server:",
            error
        );


        displayMessage(
            "Unable to connect to Semion.",
            "bot"
        );
    }
}


startSemion();