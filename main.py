import os
import json

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

cls()
vocab_list = []

while True:
    print("Welcome to NekoLearn!")
    choice = input("Press 1 to view your known words, or 2 to add a new word: ")

    if choice == '1':
        print("Here are your known words: ")
        for entry in vocab_list:
            print(f"Term: {entry['term']} | Translation: {entry['translation']} | Example: {entry['example']}\n") 


        input("Press any key to go back to the main menu.")
        cls()

    elif choice == '2':
        new_word = input("Enter the new word you want to add: ")
        new_translation = input("Enter the definition of the new word: ")
        new_example = input("Enter an example sentence using the new word: ")

        word_entry = {
            "term": new_word,
            "translation": new_translation,
            "example": new_example
        }

        vocab_list.append(word_entry)

        print(f"The word '{new_word}' has been added to your known words!")
        input("Press any key to go back to the main menu.")
        cls()   


    elif choice == '0':
        print("Goodbye!")
        cls()

        break

    else:
        print("Invalid choice, try again.")
        input("Press any key to go back to the main menu.")
        cls()