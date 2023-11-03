#! /usr/bin/python3

# Quizlot - program runs quiz from .csv or uses default data
# sdavis_10272023  -- Initial Version

import csv
import time
import os

DEFAULT_DATA = [
    {
        'question': 'Which programming language is known for its iconic "Zen"?',
        'options': ['Java', 'Python', 'Ruby', 'C#'],
        'correct_option': 'B'
    },
    {
        'question': 'Who is considered the "father" of the free software movement?',
        'options': ['Bill Gates', 'Linus Torvalds', 'Richard Stallman', 'Steve Jobs'],
        'correct_option': 'C'
    },
    {
        'question': 'What is the main protocol used on the web?',
        'options': ['FTP', 'SSH', 'HTTP', 'SMTP'],
        'correct_option': 'C'
    },
    {
        'question': 'In "The Matrix", what pill does Neo take to discover the truth?',
        'options': ['Red Pill', 'Blue Pill', 'Green Pill', 'Yellow Pill'],
        'correct_option': 'A'
    },
    {
        'question': 'Which OS is known for the mascot Tux, a penguin?',
        'options': ['Windows', 'OS X', 'Linux', 'Solaris'],
        'correct_option': 'C'
    },
    {
        'question': 'Who wrote the book "Neuromancer", which predicted virtual reality?',
        'options': ['Orson Scott Card', 'Philip K. Dick', 'Isaac Asimov', 'William Gibson'],
        'correct_option': 'D'
    }
]

def banner():
    logo = """
  ___        _     _       _   
 / _ \ _   _(_)___| | ___ | |_ 
| | | | | | | |_  / |/ _ \| __|
| |_| | |_| | |/ /| | (_) | |_ 
 \__\_\\__,_|_/___|_|\___/ \__|                
                by Red Ninja
         """
    print(logo)
    
def clear_screen():
    """Function to clear screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_csv_files_in_directory():
    """Function return list of csv files in current directory"""
    all_files = os.listdir('.')
    csv_files = [file for file in all_files if file.endswith('.csv')]
    return csv_files

def choose_csv_file():
    """Function allows the user to choose csv file or default data set as source for quiz material. returns question data"""
    csv_files = get_csv_files_in_directory()
    if not csv_files:
        print("No csv files found")
        return DEFAULT_DATA
    print("\nChoose a csv file as source or press enter for default quiz material.\n")
    
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
                    print("\nInvalid choice. Please choose a number from the list or press enter")
                
            except ValueError:
                print('\nPlease anter a valid number or press enter')


def load_questions_from_csv(filename='questions_test.csv'):
    """Function loads questions from csv file"""
    questions = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) < 2:
                print(f"Skipping row due to insufficient data: {row}")
                continue
            question_data = {
                'question' : row[0].strip('"'),
                'options' : [opt.strip().strip('"') for opt in row[1:-1]],
                'correct_option' : row[-1].strip()
            }
            questions.append(question_data)
    return questions

def quiz(compiled_questions):
    """Function conducts quiz"""
    correct_answers = 0
    incorrect_data = []
    print()
    for question_data in compiled_questions:
            clear_screen()
            print(question_data['question'])
            for index, option in enumerate(question_data['options'], 1):
                print(f"{chr(64 + index)}) {option}")
            choice = input("\nWhat is your choice? \nFinal Answer: ")
            if choice.lower() == question_data['correct_option'].lower().strip('"'):
                correct_answers += 1
                print("\nYOU SMART!!!\n")
            else:
                print("\nWRONG!!\n")
                print(f"{question_data['correct_option']} is the correct answer.")
                incorrect_data.append(question_data)
            time.sleep(1.5)
    return correct_answers, incorrect_data

def grade(correct, total):
    """Function displays feedback"""
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
    """Function displays incorrect answers"""
    print('\nThese are the questions you should study:')
    total, incorrect_questions_list = result
    for question in incorrect_questions_list:
        print()
        print(question['question'])
        for index, option in enumerate(question['options'],1):
            print(f'{chr(64 + index)}) {option}')
        print(f"Correct answer: {question['correct_option']}")
        time.sleep(.75) 

def main():
    banner()
    play_again = 'y'
    while play_again.lower() == 'y':
        questions = choose_csv_file()
        quiz_result = quiz(questions)
        grade(quiz_result[0], len(questions))
        if quiz_result[0] != len(questions):
            display_incorrect(quiz_result)
            
        play_again = input('\nPlay again (y/n)? ')
    print('\nGoodbye!')

if __name__ == "__main__":
    main()
