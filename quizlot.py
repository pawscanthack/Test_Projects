#! /usr/bin/python3

# Quizlot - program runs quiz from .csv
# sdavis_10272023  -- Initial Version

import csv
import time
import os

DEFAULT_DATA = [
    {
        'question': 'What is the capital of France?',
        'options': ['Berlin', 'Paris', 'London', 'Madrid'],
        'correct_option': 'B'
    },
    {
        'question': 'How many legs does a spider have?',
        'options': ['Four', 'Six', 'Eight'],
        'correct_option': 'C'
    },
    {
        'question': 'Which of these is not a fruit?',
        'options': ['Apple', 'Carrot', 'Banana', 'Orange'],
        'correct_option': 'B'
    }
]

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_csv_files_in_directory():
    all_files = os.listdir('.')
    csv_files = [file for file in all_files if file.endswith('.csv')]
    return csv_files

def choose_csv_file():
    csv_files = get_csv_files_in_directory()
    if not csv_files:
        print("No csv files found")
        return DEFAULT_DATA
    print("\nChoose a csv file or press enter for default quiz data.\n")
    
    for index, file in enumerate(csv_files, 1):
        print(f'{index}:{file}')
    while True:
        choice = input("\nEnter the number of your choice:")
        if not choice:
            return DEFAULT_DATA
        else:
            try:
                choice_num  = int(choice)
                if 1 <= choice_num <= len(csv_files):
                    return load_questions_from_csv(csv_files[choice_num-1])
                else:
                    print("\nInvalid choice. Please choose a number from the list")
                
            except ValueError:
                print('\nPlease anter a valid number or press enter')


def load_questions_from_csv(filename='questions_test.csv'):
    questions = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) < 2:
                print(f"Skipping row due to insufficient data: {row}")
                continue
            question_data = {
                'question' : row[0],
                'options' : row[1:-1],
                'correct_option' : row[-1]
            }
            questions.append(question_data)
    return questions

def quiz(compiled_questions):
    correct_answers = 0
    incorrect_data = []
    print()
    for question_data in compiled_questions:
            clear_screen()
            print(question_data['question'])
            for index, option in enumerate(question_data['options'], 1):
                print(f"{chr(64 + index)}) {option}")
            choice = input("\nWhat is your choice? \nFinal Answer: ")
            if choice.lower() == question_data['correct_option'].lower():
                correct_answers += 1
                print("\nYOU SMART!!!\n")
            else:
                print("\nWRONG!!\n")
                print(f"{question_data['correct_option']} is the correct answer.")
                incorrect_data.append(question_data)
                
            time.sleep(1)
    return correct_answers, incorrect_data

def grade(correct, total):
    clear_screen()
    print(f'You got {correct} out of {total}:')
    if correct == total:
        print("Genius level!")
    elif correct >= total * .75:
        print("You did well.")
    elif correct >= total * .50:
        print("Keep studying, you can do better!")
    else:
        print("Don't quit your day job.")
    time.sleep(3)


def display_incorrect(result):
    print('\nThese are the questions you should study:')
    total, incorrect_questions_list = result
    for question in incorrect_questions_list:
        print()
        print(question['question'])
        for index, option in enumerate(question['options'],1):
            print(f'{chr(64 + index)}) {option}')
        print(f"Correct answer: {question['correct_option']}")
        time.sleep(.5) 

def main():
    play_again = 'y'
    while play_again.lower() == 'y':
        questions = choose_csv_file()
        #questions = load_questions_from_csv(quiz_file)
        quiz_result = quiz(questions)
        grade(quiz_result[0], len(questions))
        if quiz_result[0] != len(questions):
            display_incorrect(quiz_result)
            
        play_again = input('\nPlay again (y/n)? ')
    print('\nGoodbye!')

if __name__ == "__main__":
    main()
