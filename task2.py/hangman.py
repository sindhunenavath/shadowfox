import random


WORDS = [
    "python",
    "program",
    "developer",
    "computer",
    "keyboard",
    "function",
]

HANGMAN_PICS = [
    """
       +---+
       |   |
           |
           |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
           |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
       |   |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
      /|   |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
      /|\\  |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
      /|\\  |
      /    |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
      /|\\  |
      / \\  |
           |
    =========
    """,
]


def display_word(secret_word, guessed_letters):
    return " ".join(
        letter if letter in guessed_letters else "_"
        for letter in secret_word
    )


def play_game():
    secret_word = random.choice(WORDS)
    guessed_letters = set()
    wrong_guesses = 0
    max_wrong_guesses = len(HANGMAN_PICS) - 1

    print("Welcome to Hangman!")
    print("Guess the hidden word one letter at a time.")

    while wrong_guesses < max_wrong_guesses:
        print(HANGMAN_PICS[wrong_guesses])
        print(f"Word: {display_word(secret_word, guessed_letters)}")
        print(f"Wrong guesses left: {max_wrong_guesses - wrong_guesses}")

        try:
            guess = input("Enter a letter: ").lower().strip()
        except EOFError:
            print("\nNo input provided. Please run the game again and enter letters.")
            return

        if len(guess) != 1 or not guess.isalpha():
            print("Please enter one alphabet letter.\n")
            continue

        if guess in guessed_letters:
            print("You already guessed that letter.\n")
            continue

        guessed_letters.add(guess)

        if guess in secret_word:
            print("Good guess!\n")
        else:
            wrong_guesses += 1
            print("Wrong guess!\n")

        if all(letter in guessed_letters for letter in secret_word):
            print(f"Congratulations! You guessed the word: {secret_word}")
            return

    print(HANGMAN_PICS[wrong_guesses])
    print(f"Game over! The word was: {secret_word}")


if __name__ == "__main__":
    play_game()
