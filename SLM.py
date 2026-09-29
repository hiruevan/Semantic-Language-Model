import json
import numpy as np
import math
import re
import os

# This python script trains a SLM (Sematic Language Model) 
# (or as I jokingly call it, a Small Language Model)
# to recongnize speach to determine acceptable responses
# to user input. It uses vectors to represent words (or tokens)
# and runs a predicable calculation on all the words in a response.
# The result that is closest to the "command" defines how the AI
# interperets the result. The command vector that is scored
# the highest via cosine similarity will be returned.

# Number of dimensions for the word vectors
VECTOR_SIZE = 512
WORD_VECTOR_FILE = "word_token_vectors.json"
COMMAND_VECTOR_FILE = "command_vectors.json"
TRAINING_DATA_FILE = "training_data.json"

def load_json(file_path, default_value):
    """Loads a JSON file or returns default value if the file doesn't exist."""
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return default_value

def save_json(file_path, data):
    """Saves data as a JSON file."""
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

def validate_and_fix_vectors(word_vectors, command_vectors, vector_size):
    # Remove invalid word vectors
    words_to_remove = []
    for word, vec in word_vectors.items():
        if len(vec) != vector_size:
            print(f"Warning: Word vector '{word}' length {len(vec)} != {vector_size}, removing it.")
            words_to_remove.append(word)
    for word in words_to_remove:
        del word_vectors[word]

    # Regenerate invalid command vectors
    for command, vec in list(command_vectors.items()):
        if len(vec) != vector_size:
            print(f"Warning: Command vector '{command}' length {len(vec)} != {vector_size}, regenerating.")
            command_vectors[command] = np.random.uniform(-256, 256, vector_size).tolist()

    return word_vectors, command_vectors



# Load or initialize word vectors
word_vectors = load_json(WORD_VECTOR_FILE, {})

# Load command vectors
command_vectors = load_json(COMMAND_VECTOR_FILE, {})

# Validate vectors
word_vectors, command_vectors = validate_and_fix_vectors(word_vectors, command_vectors, VECTOR_SIZE)
save_json(COMMAND_VECTOR_FILE, command_vectors)
print("Vectors succesfully loaded and validated!")

# Load training data
training_data = load_json(TRAINING_DATA_FILE, [])

def get_or_create_vector(word):
    """Retrieves a word vector if it exists, otherwise creates a new one."""
    if word not in word_vectors:
        # Generate a new random vector for a new word
        word_vectors[word] = np.random.uniform(-1, 1, VECTOR_SIZE).tolist()
    return np.array(word_vectors[word])

def tokenize(input_text):
    # Regular expression to match words and punctuation
    pattern = r'\b\w+\b|[^\w\s,]'
    tokens = re.findall(pattern, input_text.lower())
    return tokens

def get_vector_sum(tokens, word_vectors):
    vector_sum = [0] * VECTOR_SIZE
    token_count = 0

    for token in tokens:
        if token in word_vectors:
            vector = word_vectors[token]
            for i in range(len(vector)):
                vector_sum[i] += vector[i]
            token_count += 1

    if token_count == 0:
        return None  # No valid words found

    return [val / token_count for val in vector_sum]  # Normalize sum

def cosine_similarity(vec_a, vec_b):
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    mag_a = math.sqrt(sum(a ** 2 for a in vec_a))
    mag_b = math.sqrt(sum(b ** 2 for b in vec_b))

    return dot / (mag_a * mag_b) if mag_a and mag_b else 0

def determine_command(input_text, word_vectors, command_vectors):
    tokens = tokenize(input_text)  # Assuming you have a tokenize function
    input_vector = get_vector_sum(tokens, word_vectors)

    if not input_vector:
        return {'command': 'gpt', 'confidence': 0}

    best_match = None
    highest_similarity = 0

    for command, cmd_vector in command_vectors.items():
        similarity = cosine_similarity(input_vector, cmd_vector)
        if similarity > highest_similarity:
            highest_similarity = similarity
            best_match = command

    return {'command': best_match if highest_similarity > 0.7 else 'gpt', 'confidence': highest_similarity}

def testAgainstTrainingData():
    totalTests = 0
    totalCorrect = 0
    for test in training_data:
        result = determine_command(test["sentence"], word_vectors, command_vectors)
        if result["command"] == test["command"]: 
            totalCorrect += 1
        totalTests += 1
    print(f"The SLM scored a success rate of {math.floor(totalCorrect / totalTests * 100)}% with {totalCorrect}/{totalTests} correct tests.")


times = int(input("Training times? "))

count = 0

for i in range(times):

    # Train the model
    for entry in training_data:
        sentence, command = entry["sentence"], entry["command"]
        words = tokenize(sentence)

        if command not in command_vectors:
            print(f"Warning: Command '{command}' is missing from command_vectors.json!")
            continue

        expected_vector = np.array(command_vectors[command])  # Target vector
        sentence_vector = np.mean([get_or_create_vector(word) for word in words], axis=0)

        # Adjust word vectors to align their sentence average with the expected command vector
        for word in words:
            current_vector = get_or_create_vector(word)
            adjusted_vector = current_vector + 0.01 * (expected_vector - sentence_vector)  # Small adjustment step
            word_vectors[word] = adjusted_vector.tolist()

    # Save the updated word vectors
    save_json(WORD_VECTOR_FILE, word_vectors)
    print("Training complete! Word vectors updated.")

    # Test the model
    if count % 30 == 0: 
        testAgainstTrainingData()

    count += 1

testAgainstTrainingData()

print("\n\nTraining session complete!")