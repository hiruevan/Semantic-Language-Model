import numpy as np
from SLM import (load_json, save_json, validate_and_fix_vectors, tokenize, get_or_create_vector, testAgainstTrainingData,
TRAINING_DATA_FILE, VECTOR_SIZE, WORD_VECTOR_FILE, COMMAND_VECTOR_FILE)

if __name__ == "__main__":
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
            sentence_vector = np.mean([get_or_create_vector(word, word_vectors) for word in words], axis=0)

            # Adjust word vectors to align their sentence average with the expected command vector
            for word in words:
                current_vector = get_or_create_vector(word, word_vectors)
                adjusted_vector = current_vector + 0.01 * (expected_vector - sentence_vector)  # Small adjustment step
                word_vectors[word] = adjusted_vector.tolist()

        # Save the updated word vectors
        save_json(WORD_VECTOR_FILE, word_vectors)
        print("Training complete! Word vectors updated.")

        # Test the model
        if count % 30 == 0: 
            testAgainstTrainingData(training_data, word_vectors, command_vectors)

        count += 1

    if (count - 1) % 30 != 0:
        testAgainstTrainingData(training_data, word_vectors, command_vectors)

    print("\n\nTraining session complete!")