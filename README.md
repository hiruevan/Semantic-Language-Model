# Semantic-Language-Model

**Semion** is a small **Semantic Language Model (SML)** created as a proof of concept for exploring how mathematical representations of language can be used to build a simple chatbot.

Rather than using a large neural network or a general-purpose AI model, Semion represents language using semantic vectors and uses mathematical similarity to determine what a user is saying. 

> **Semion is a learning project, not a general-purpose AI.**

## Features

* Semantic-vector-based language understanding
* Command-based response system
* Cosine similarity for comparing meanings
* Custom training data
* Lightweight and easy to understand
* No large language model API required
* Designed to demonstrate the fundamentals of semantic language processing

## How It Works

Semion follows a relatively simple pipeline:

```text
User Input
    ↓
Text Processing
    ↓
Word/Sentence Vector Representation
    ↓
Semantic Comparison
    ↓
Closest Command
    ↓
Response
```

When a user enters a sentence, Semion converts the input into a mathematical representation.

It then compares that representation against the semantic representations associated with its training data.

The command with the closest semantic match is selected, and Semion generates the corresponding response.

For example:

```text
User:
    "Who created you?"

Semantic matching:
    creator

Response:
    "I was made by Evan Hill."
```

## Commands

Semion currently uses commands to categorize different types of input.

Some examples include:

| Command           | Purpose                             |
| ----------------- | ----------------------------------- |
| `greet`           | Greetings                           |
| `hello`           | Hello-specific greetings            |
| `goodbye`         | Saying goodbye                      |
| `thanks`          | Thanking Semion                     |
| `how_doing`       | Asking how Semion is doing          |
| `user_doing_well` | Positive statements from the user   |
| `user_doing_bad`  | Negative statements from the user   |
| `name`            | Asking Semion's name                |
| `what_are_you`    | Asking what Semion is               |
| `capabilities`    | Asking what Semion can do           |
| `how_work`        | Asking how Semion works             |
| `creator`         | Asking who created Semion           |
| `why_made`        | Asking why Semion was created       |
| `purpose`         | Asking about Semion's purpose       |
| `compliment`      | Compliments toward Semion           |
| `joke`            | Requests for jokes                  |
| `math`            | Mathematics-related conversation    |
| `question`        | Generic questions                   |
| `age`             | Asking about Semion's age           |
| `human`           | Asking whether Semion is human      |
| `ai`              | Asking whether Semion is AI         |
| `understand`      | Asking about Semion's understanding |
| `language`        | Questions about language            |
| `vector`          | Questions about vectors             |
| `similarity`      | Questions about semantic similarity |
| `semantic`        | Questions about semantics           |

## Training Data

Semion's training data consists of sentences associated with commands.

For example:

```json
[
    {
        "sentence": "hi there!",
        "command": "greet"
    },
    {
        "sentence": "hello!",
        "command": "greet"
    },
    {
        "sentence": "who created you?",
        "command": "creator"
    },
    {
        "sentence": "what is a vector?",
        "command": "vector"
    }
]
```

The goal is not to memorize every possible sentence.

Instead, many different ways of expressing the same idea are included so that Semion can learn that sentences with similar meanings should produce similar results.

For example:

```text
"Who made you?"
"Who created you?"
"Who built you?"
"Who programmed you?"
"Who is your creator?"
```

can all correspond to:

```text
creator
```

## Responses

Each command has an associated response.

A simplified response dictionary looks like:

```javascript
const responses = {
    greet:
        "Hi there! How can I help you?",

    name:
        "My name is Semion, a Semantic Language Model!",

    creator:
        "I was made by Evan Hill.",

    vector:
        "A vector is a mathematical representation containing a collection of numerical values.",

    similarity:
        "I use cosine similarity to compare semantic vectors and determine which meaning is closest to your input."
};
```

This separates **understanding** from **responding**.

The semantic model determines:

```text
"What does the user mean?"
```

The response system determines:

```text
"What should Semion say?"
```

## Semantic Similarity

Semion uses **cosine similarity** to compare vectors.

For two vectors `A` and `B`, cosine similarity is:

```text
              A · B
similarity = -------
             ||A|| ||B||
```

The result indicates how similar the two vectors are in direction.

A value closer to `1` indicates greater similarity, while a value closer to `0` indicates less similarity.

This allows Semion to compare meanings mathematically rather than simply checking whether two sentences contain the same words.

## Example

Suppose the training data contains:

```text
"Who made you?" → creator
```

A user could instead ask:

```text
"Who built you?"
```

Even though the words are different, their semantic representations may be similar.

Semion can therefore identify:

```text
"Who built you?"
        ↓
semantic similarity
        ↓
creator
        ↓
"I was made by Evan Hill."
```

## Limitations

Semion is intentionally small, which means it has significant limitations.

### It does not truly understand language

Semion does not understand language in the same way a person does.

It works with mathematical representations and similarity measurements.

### It has limited knowledge

Semion only knows what has been represented in its training data and semantic model.

It cannot automatically learn everything about the world.

### Similar meanings can cause mistakes

Because Semion relies on mathematical similarity, unrelated sentences can sometimes have vectors that are closer than expected.

For example:

```text
"Tell me why"
```

could accidentally be associated with a training example about why Semion was created.

This happens because the model may place too much importance on words such as:

```text
why
tell
```

rather than understanding the complete context.

### Short inputs are difficult

Very short messages such as:

```text
"yo"
"yeah"
"k"
"tell"
```

contain very little semantic information.

Consequently, they can be difficult to classify correctly.

### It does not generate language freely

Semion does not generate completely new responses like a large language model.

Instead, it selects from predefined responses associated with commands.

## Why Semion Exists

Semion was created as a personal project to explore semantic language processing on a small scale.

The project originated from a BYU math camp project and evolved into an experiment involving:

* vectors
* mathematical similarity
* natural language
* semantic representations
* classification
* chatbot design

The goal is to demonstrate that some aspects of language processing can be explored using relatively simple mathematical concepts.

## Project Philosophy

Semion is intentionally different from modern large language models.

Instead of trying to build an enormous model capable of generating arbitrary text, the project focuses on understanding the underlying ideas behind semantic language processing.

The project asks a simple question:

> **How much language understanding can be achieved with a relatively small mathematical model?**

## Future Improvements

Possible future improvements include:

* Better sentence embeddings
* More training examples
* Improved handling of short messages
* Context-aware classification
* Conversation history
* Better handling of ambiguous phrases
* Confidence thresholds
* An explicit `unknown` command
* Improved tokenization
* Better semantic vector generation
* More sophisticated weighting of recent words
* Multiple possible commands instead of only the closest command
* Context-sensitive response selection

## Project Structure

A possible project structure is:

```text
Semion/
├── main.py
├── responses.js
├── training_data.json
├── vectors/
│   └── ...
├── static/
│   ├── index.html
│   ├── chat.js
│   └── style.css
└── README.md
```

The exact structure may vary depending on the implementation.

## Example Conversation

```text
Semion:
    Hello! My name is Semion. How can I help you today?

User:
    What is your name?

Semion:
    My name is Semion, a Semantic Language Model!

User:
    How do you work?

Semion:
    I compare the meaning of your words to semantic vectors that I have been given.

User:
    What is a vector?

Semion:
    A vector is a mathematical representation containing a collection of numerical values.

User:
    Are you human?

Semion:
    No, I am not human. I am a computer program.
```

## Credits

**Created by Evan Hill**

Semion was created as a personal programming and mathematics project, with the original concept developing from a BYU math camp project in 2023.
