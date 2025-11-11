import os
def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

cls()

while True:
    print("Welcome to NekoLearn!")
    choice = input("Press 1 to view your known words, or 2 to add a new word: ")

    if choice == '1':
        print("Here are your known words: [Placeholder for word list]")
        input("Press any key to go back to the main menu.")
        cls()

    elif choice == '2':
        new_word = input("Enter the new word you want to add: ")
        new_definition = input("Enter the definition of the new word: ")
        new_example = input("Enter an example sentence using the new word: ")

        print(f"The word '{new_word}' has been added to your known words!")
        input("Press any key to go back to the main menu.")
        cls()   


    elif choice == '0':
        print("Goodbye!")
        cls()

        break  # exits the while loop, ending the program

    else:
        print("Invalid choice, try again.")
        input("Press any key to go back to the main menu.")
        cls()