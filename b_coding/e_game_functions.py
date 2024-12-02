import streamlit as st
from b_coding.b_player_data import player_dictionary
from b_coding.d_game_initialize import generate_player_list, start_game
from b_coding.c_filter_criteria import check_player_criteria

player_data = {
    "name": "Lionel Messi",
    "current_club": "Inter Miami",
    "league": "MLS",
    "nationality": "Argentina",
    "previous_club": "PSG",
    "position": "Forward",
    "titles": ["World Cup", "Champions League"],
    "age": 36,
    "shirt_number": 10,
    "height": 170
}

# List of predetermined questions
QUESTIONS = [
    "1. Am I currently playing for ... (club)?",
    "2. Do I play in the ... (league)?",
    "3. Am I from ... (nationality)?",
    "4. Did I use to play for ... (club)?",
    "5. Do I play as a ... (position)?",
    "6. Am I a ... winner (CL/WC/EC)?",
    "7. Am I older than ... (age)?",
    "8. Am I younger than ... (age)?",
    "9. Do I wear the shirt number ... at my current club (shirt number)?",
    "10. Am I taller than ... (height in cm)?",
    "11. Am I shorter than ... (height in cm)?"
]

def ask_user_for_question():
    """
    # Displays the list of questions and allows the user to select one.
    """
    while True:  # Korrekt eingerückter Block beginnt hier
        print("\n\nThese are the questions you can choose from:")
        for i, question in enumerate(QUESTIONS):
            print(f"{i + 1}. {question}")  # Zeigt die Fragen an
            
        # Testweise beenden, um die Schleife nicht endlos laufen zu lassen
        try:
            question_index = int(input("\nPlease choose your question from the ones above and put in the number of that question: ")) - 1   #this line asks the user to submit their question


            #checking if the number of the question is part of the list
            if 0 <= question_index < len(QUESTIONS):
                print (f"\nYou chose the following question: {QUESTIONS[question_index]}")

                #User submits additional input for the question such as height, age etc. 
                user_input = input("Please submit your additional value fitting your question (i.e height, age, position etc.): ").strip()
                print(f"\nYour input was: {user_input}")

                #returning of the chosen question and the submitted value
                return question_index, user_input
            
            else: 
                print("\nInvalid Choice. Please choose a valid number of a question from the list.\n")

        except ValueError:
            print("\nPlease submit a valid number.\n")

def process_question(player_data, question_index, user_input):
    # processes the question and returns an answer if the Information is right or wrong

    if question_index == 0:  # "Am I currently playing for ...?"
        is_correct = user_input.lower() == player_data["current_club"].lower()
    elif question_index == 1:  # "Do I play in ... (league)?"
        is_correct = user_input.lower() == player_data["league"].lower()
    elif question_index == 2:  # "Am I from ... (nationality)?"
        is_correct = user_input.lower() == player_data["nationality"].lower()
    elif question_index == 3:  # "Did I use to play for ... (club)?"
        is_correct = user_input.lower() == player_data["previous_club"].lower()
    elif question_index == 4:  # "Do I play as a ... (position)?"
        is_correct = user_input.lower() == player_data["position"].lower()
    elif question_index == 5:  # "Am I a ... winner (CL/WC/EC)?"
        is_correct = user_input in player_data["titles"]
    elif question_index == 6:  # "Am I older than ... (age)?"
        is_correct = player_data["age"] > int(user_input)
    elif question_index == 7:  # "Am I younger than ... (age)?"
        is_correct = player_data["age"] < int(user_input)
    elif question_index == 8:  # "Do I wear the shirt number ...?"
        is_correct = player_data["shirt_number"] == int(user_input)
    elif question_index == 9:  # "Am I taller than ... (height in cm)?"
        is_correct = player_data["height"] > int(user_input)
    elif question_index == 10:  # "Am I shorter than ... (height in cm)?"
        is_correct = player_data["height"] < int(user_input)
    else:
        return False, 0 
    
    return is_correct

def guess_player(player_data, lives):
    #here the user is asked if he/she wants to guess the player already oder not
    should_guess = input("\nDo you want to guess player? (yes/no) But keep in mind, that you will lose a live if you guess wrong!: ").strip().lower()

    #if the user wants to take a guess on the player this part will be activated after checking if the user wants to.
    if should_guess == "yes":
        player_guess = input("\nEnter your guess for the player's name: ").strip()
        if player_guess.lower() == player_data["name"].lower():
            print("\nCongratulations! You've guessed the player correctly!")
            return lives, True, False  #game_won = True, game_lost = False
        else:
            lives -= 1 
            print("\nWrong guess! You lost a life.")
            if lives <= 0:
                print("\nNo lives left! Game Over!")
                return lives, False, True # game_won = False, game_lost = True
    
    print("\nYou chose not to guess.")
    return lives, False, False #No guess taken and game goes on 