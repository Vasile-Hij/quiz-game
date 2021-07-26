import requests
import csv
import json
import sys
import os
import pandas as pd

class Question:
    def __init__(self, q_body, q_answer):
        self._body = q_body
        self._answer = q_answer

    @property
    def answer(self):
        return self._answer

    @property
    def q_text(self):
        return self._body

    def __repr__(self):
        return "<Node(body='%s', answer='%s')>" \
               % (self.body, self.answer)


class QuizBrain:
    def __init__(self, q_list):
        self.question_number = 0
        self.score = 0
        self.question_list = q_list

    def still_has_questions(self):
        return self.question_number < len(self.question_list)

    def get_question(self):
        current_question = self.question_list[self.question_number]
        self.question_number += 1
        user_answer = input("Q.%d: %s True or false? \n" % (self.question_number, str(current_question.q_text).replace('&quot;', '')))
        self.check_answer(user_answer, current_question)
        return user_answer, current_question

    def check_answer(self, user_answer, question):
        if user_answer.lower() == question.answer.lower():
            self.score += 1
            print('You got right!')
        else:
            print("That's wrong!")
        if user_answer.lower() in {'q', 'quit', 'e', 'exit'}:
            print('Goodbye!')
            quit()
        print('The correct answer was: %s' % question.answer)
        print('Your score is %d/%d' % (self.score, self.question_number))
        print("\n")

    def play(self):
        while self.still_has_questions():
           self.get_question()



class Player:
    def __init__(self, name):
        self._name = name
        self._score = 0


    @property
    def name(self):
        return self._name

    @property
    def score(self):
        return self._score

    @name.setter
    def name(self, name):
        self._name = name

    @score.setter
    def score(self, score):
        self._score = score


def get_json(x):
    return requests.get(x).json()


url = 'https://opentdb.com/api.php?amount=10&category=18&difficulty=easy&type=boolean'
answers = get_json(url)


def main():
    print('Welcome to Quiz game')
    print("Type 'exit' to quit game! Your progress will not be saved!")


    name = input('Enter player name: ')
    player = Player(name)

    questions = []
    for elem in answers['results']:
        questions.append(Question(elem['question'], elem['correct_answer']))
    while True:
        quiz = QuizBrain(questions)
        quiz.play()
        user_replay = str(input('Do you want to play again, (y/n)?'))
        if user_replay.lower() in {'yes', 'y'}:
            continue
        if user_replay.lower() in {'no', 'n'}:
            break
    print("You've completed the quiz!")
    print("Final score %s: %s/%s" % (player.name, quiz.score, quiz.question_number))

    save = player.name, quiz.score
    score = 'score.csv'
    with open(score, 'a', newline='') as saving:
        writer = csv.writer(saving)
        writer.writerow(save)

    df = pd.read_csv(score)
    p = df[df['score'] == df['score'].max()]

    print(p)


if __name__ == '__main__':
    main()
