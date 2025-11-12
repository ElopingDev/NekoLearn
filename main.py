import os
import json

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def save_vocab():
    with open('vocab.json', 'w') as file:
        json.dump(vocab_list, file, ensure_ascii=False, indent=2)

def load_vocab():
    if os.path.exists('vocab.json'):
        with open('vocab.json', 'r') as file:
            return json.load(file)
    return []

def list_vocab():
    if not vocab_list:
        print("You have no known words yet.")
        return
    for i, entry in enumerate(vocab_list, start=1):
        print(f"{i}. Term: {entry['term']} | Translation: {entry['translation']} | Example: {entry['example']}")

def delete_word(vocab_list, index):
    if 0 <= index < len(vocab_list):
        del vocab_list[index]
        save_vocab()
        print("Word deleted successfully.")
    else:
        print("Invalid index.")

cls()
vocab_list = load_vocab()

while True:
    print("Welcome to NekoLearn!")
    choice = input("Press 1 to view your known words, or 2 to add a new word, or 3 to delete a word: ")

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
        save_vocab()

        print(f"The word '{new_word}' has been added to your known words!")
        input("Press any key to go back to the main menu.")
        cls()   

    elif choice == '3':
        list_vocab()
        index_to_delete = int(input("Enter the index of the word you want to delete (starting from 1): ")) - 1
        delete_word(vocab_list, index_to_delete)
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