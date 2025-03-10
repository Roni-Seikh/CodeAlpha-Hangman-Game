import random
import requests
import tkinter as tk
from tkinter import messagebox

# Hangman Stages (Graphical)
HANGMAN_PICS = [
    """
      +---+
      |   |
          |
          |
          |
          |
    =========""",
    """
      +---+
      |   |
      O   |
          |
          |
          |
    =========""",
    """
      +---+
      |   |
      O   |
      |   |
          |
          |
    =========""",
    """
      +---+
      |   |
      O   |
     /|   |
          |
          |
    =========""",
    """
      +---+
      |   |
      O   |
     /|\\  |
          |
          |
    =========""",
    """
      +---+
      |   |
      O   |
     /|\\  |
     /    |
          |
    =========""",
    """
      +---+
      |   |
      O   |
     /|\\  |
     / \\  |
          |
    =========
    GAME OVER!"""
]

# Fetch random word from an API
def get_random_word():
    try:
        response = requests.get("https://random-word-api.vercel.app/api?words=1", timeout=5)
        response.raise_for_status()
        word = response.json()[0]
        return word.lower()
    except requests.exceptions.RequestException:
        return random.choice(["python", "developer", "hangman", "programming"])

# Multiplayer mode 
def multiplayer_game():
    start_game(multiplayer=True)

# Start Game
def start_game(multiplayer=False):
    global word, guessed_word, attempts, guessed_letters, player_turn, players  
    word = get_random_word()
    guessed_word = ["_"] * len(word)
    attempts = len(HANGMAN_PICS) - 1
    guessed_letters = []
    
    # Initialize players and turn handling properly
    if multiplayer:
        players = ["Player 1", "Player 2"]
        player_turn = 0  # Ensure player_turn is initialized in multiplayer mode
    else:
        players = ["Single Player"]
        player_turn = 0  # Even in single-player, initialize player_turn

    play_hangman(multiplayer)

# Main Game Loop
def play_hangman(multiplayer=False):
    global word, guessed_word, attempts, guessed_letters, player_turn
    while attempts > 0 and "_" in guessed_word:
        print(HANGMAN_PICS[len(HANGMAN_PICS) - 1 - attempts])
        print("\nWord: ", " ".join(guessed_word))
        print(f"Incorrect Attempts Left: {attempts}")
        if multiplayer:
            print(f"{players[player_turn]}'s turn")
        guess = input("Guess a letter: ").lower()
        if len(guess) != 1 or not guess.isalpha() or guess in guessed_letters:
            print("Invalid input or already guessed!")
            continue
        guessed_letters.append(guess)
        if guess in word:
            for i, letter in enumerate(word):
                if letter == guess:
                    guessed_word[i] = guess
        else:
            attempts -= 1
        if multiplayer:
            player_turn = 1 - player_turn  # Switch turns
    if "_" in guessed_word:
        print(HANGMAN_PICS[-1])
        print(f"Game Over! The correct word was: {word}")
    else:
        print(f"\nCongratulations! {players[player_turn]} guessed the word: {word}")

# GUI Version
def gui_hangman():
    global word, guessed_word, attempts, guessed_letters
    word = get_random_word()
    guessed_word = ["_"] * len(word)
    attempts = len(HANGMAN_PICS) - 1
    guessed_letters = []
    
    root = tk.Tk()
    root.title("Hangman Game")
    root.geometry("900x900")
    root.configure(bg="#87CEEB")

    def guess_letter(letter):
        global attempts
        if letter in guessed_letters:
            return
        guessed_letters.append(letter)
        if letter in word:
            for i, l in enumerate(word):
                if l == letter:
                    guessed_word[i] = letter
        else:
            attempts -= 1
        update_display()

    def update_display():
        word_label.config(text=" ".join(guessed_word))
        hangman_label.config(text=HANGMAN_PICS[len(HANGMAN_PICS) - 1 - attempts])
        if "_" not in guessed_word:
            messagebox.showinfo("Hangman", "Congratulations! You guessed the word: " + word)
            root.destroy()
        elif attempts == 0:
            messagebox.showinfo("Hangman", "Game Over! The word was: " + word)
            root.destroy()

    hangman_label = tk.Label(root, text=HANGMAN_PICS[0], font=("Courier", 14), bg="#87CEEB")
    hangman_label.pack()
    word_label = tk.Label(root, text=" ".join(guessed_word), font=("Helvetica", 24), bg="#87CEEB")
    word_label.pack()
    button_frame = tk.Frame(root, bg="#87CEEB")
    button_frame.pack()
    
    for i, letter in enumerate("abcdefghijklmnopqrstuvwxyz"):
        btn = tk.Button(button_frame, text=letter.upper(), width=6, height=3, font=("Helvetica", 16), command=lambda l=letter: guess_letter(l))
        btn.grid(row=i // 6, column=i % 6, padx=5, pady=5)
    
    root.mainloop()

# Main Menu
def main():
    print("---------------------------------")
    print("------ WELCOME TO HANGMAN! ------")
    print("---------------------------------")
    print("1. Single Player")
    print("2. Multiplayer")
    print("3. Play GUI Version")
    print("---------------------------------")
    choice = input("Enter your choice: ")
    if choice == "1":
        start_game(multiplayer=False)
    elif choice == "2":
        multiplayer_game()
    elif choice == "3":
        gui_hangman()
    else:
        print("Invalid choice. Exiting.")

# Run the Game
if __name__ == "__main__":
    main()
