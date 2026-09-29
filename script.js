// ------------------------------------------------------------
// Configuration
// ------------------------------------------------------------

const VECTOR_SIZE = 512;


// ------------------------------------------------------------
// Semion data
// ------------------------------------------------------------

let wordVectors = {};
let commandVectors = {};


// ------------------------------------------------------------
// Local Semion responses
// ------------------------------------------------------------

const responses = {
    greet:
        "Hi there! How can I help you?",

    hello:
        "Hello! It's nice to meet you.",

    goodbye:
        "Goodbye! Have a great day.",

    thanks:
        "You're welcome!",

    how_doing:
        "I don't really have feelings, but if I did I would be doing well. How about you?",

    user_doing_well:
        "That's great to hear!",

    user_doing_bad:
        "I'm sorry to hear that. I hope things get better.",

    name:
        "My name is Semion, a Semantic Language Model!",

    what_are_you:
        "I am Semion, a small semantic-search language model created as a proof of concept.",

    capabilities:
        "I can recognize the semantic meaning of certain phrases and respond to them.",

    how_work:
        "I compare the meaning of your words to semantic vectors that I have been given.",

    creator:
        "I was made by Evan Hill.",

    why_made:
        "I was created as a personal project. Although that project originated from a BYU math camp project.",

    purpose:
        "My purpose is to demonstrate how semantic language processing can work on a small scale.",

    compliment:
        "Thank you! That's nice of you to say.",

    joke:
        "The square root of negative four equals two... It's all fun and games until someone loses an i!",

    math:
        "Mathematics is very important to my existence. My semantic-search model relies on vectors and mathematical similarity.",

    woodchuck:
        "A woodchuck could chuck as much wood as a woodchuck could chuck if a woodchuck could chuck wood.",

    question:
        "That's an interesting question.",

    age:
        "I don't really have an age. I am a computer program. Though I was initially created durring the summer of 2023. My latest training was in the september of 2026.",

    human:
        "No, I am not human. I am a computer program.",

    ai:
        "I am a small semantic-search language model, but I am not designed to be a general-purpose artificial intelligence.",

    understand:
        "I don't understand language the same way a person does. I use mathematical representations of words and compare their similarity.",

    language:
        "Language is complicated, but mathematics gives me a way to represent some of its relationships.",

    vector:
        "A vector is a mathematical representation containing a collection of numerical values. I use vectors to represent words and their meanings.",

    similarity:
        "I use cosine similarity to compare semantic vectors and determine which meaning is closest to your input.",

    semantic:
        "Semantics is the study of meaning in language. My purpose is to use mathematical representations to recognize some of that meaning.",

    unknown:
        "I am unable to understand what you just said. Don't take it personally - it likely was not in my training."
};


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


async function processInput() {

    const inputField =
        document.getElementById("user-input");

    const inputText =
        inputField.value.trim();

    if (!inputText) {
        return;
    }


    displayMessage(
        inputText,
        "user"
    );


    inputField.value = "";


    await processSLM(inputText);
}


// ------------------------------------------------------------
// Semantic-search Language Model
// ------------------------------------------------------------

async function processSLM(input) {

    const result =
        determineCommand(input);


    if (
        result.command &&
        responses[result.command]
    ) {

        displayMessage(
            responses[result.command],
            "bot"
        );

    } else {

        displayMessage(
            responses.unknown,
            "bot"
        );
    }
}


// ------------------------------------------------------------
// Tokenization
// ------------------------------------------------------------

function tokenize(input) {

    const cleaned =
        input
            .replace(
                /[.,\/#!$%\^&\*;:{}=\-_`~()]/g,
                ""
            )
            .toLowerCase()
            .replace(
                /[^a-z0-9\s]/g,
                ""
            );


    return cleaned
        .split(/\s+/)
        .filter(Boolean);
}


// ------------------------------------------------------------
// Vector averaging
// ------------------------------------------------------------

function getVectorSum(tokens) {

    const vectorSum =
        new Array(
            VECTOR_SIZE
        ).fill(0);


    let tokenCount = 0;


    tokens.forEach(token => {

        if (wordVectors[token]) {

            wordVectors[token].forEach(
                (value, index) => {

                    vectorSum[index] +=
                        value;
                }
            );

            tokenCount++;
        }

    });


    if (tokenCount === 0) {
        return null;
    }


    return vectorSum.map(
        value =>
            value / tokenCount
    );
}


// ------------------------------------------------------------
// Cosine similarity
// ------------------------------------------------------------

function cosineSimilarity(
    vecA,
    vecB
) {

    let dot = 0;

    let magA = 0;

    let magB = 0;


    for (
        let i = 0;
        i < vecA.length;
        i++
    ) {

        dot +=
            vecA[i] *
            vecB[i];

        magA +=
            vecA[i] ** 2;

        magB +=
            vecB[i] ** 2;
    }


    magA =
        Math.sqrt(magA);

    magB =
        Math.sqrt(magB);


    return magA && magB
        ? dot / (magA * magB)
        : 0;
}


// ------------------------------------------------------------
// Determine semantic command
// ------------------------------------------------------------

function determineCommand(input) {

    const tokens =
        tokenize(input);


    const inputVector =
        getVectorSum(tokens);


    if (!inputVector) {

        console.error("Error finding vector sum of tokens.")
        return {
            command: "unknown",
            confidence: 0
        };
    }


    let bestMatch = null;

    let highestSimilarity = 0;


    for (
        const [
            command,
            commandVector
        ]
        of Object.entries(
            commandVectors
        )
    ) {

        const similarity =
            cosineSimilarity(
                inputVector,
                commandVector
            );


        if (
            similarity >
            highestSimilarity
        ) {

            highestSimilarity =
                similarity;

            bestMatch =
                command;
        }
    }

    console.log(`Command: ${bestMatch}\nConfidence: ${Math.round(highestSimilarity*100)}%`)

    return {

        command:
            bestMatch,

        confidence:
            highestSimilarity
    };
}


// ------------------------------------------------------------
// Load semantic-search model
// ------------------------------------------------------------

async function loadVectors() {

    try {

        wordVectors =
            await fetch(
                "word_token_vectors.json"
            ).then(
                response =>
                    response.json()
            );


        commandVectors =
            await fetch(
                "command_vectors.json"
            ).then(
                response =>
                    response.json()
            );


    } catch (error) {

        console.error(
            "Unable to load semantic model:",
            error
        );

        wordVectors = {};

        commandVectors = {};
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

    await loadVectors();


    displayMessage(
        "Hello! My name is Semion. How can I help you today?",
        "bot"
    );


    document
        .getElementById("user-input")
        .focus();
}


startSemion();