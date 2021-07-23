#!/usr/bin/env python3
import requests


class Question:
    def __init__(self, q_test, q_answer):
        self._text = q_test
        self._answer = q_answer

    @property
    def answer(self):
        return self._answer

    @property
    def q_text(self):
        return self._text

    def __repr__(self):
        return "<Node(_text= %s, _answer= %s)>" \
               % (self._text, self._answer)


class QuizBrain:
    def __init__(self, q_list):
        self.question_number = 0
        self.score = 0
        self.question_list = q_list

    def still_has_questions(self): #TODO
        return self.question_number - 1 < len(self.question_list)

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
        print('The correct answer was: %s' % question.answer)
        print('Your score is %d/%d' % (self.score, self.question_number))
        print("\n")

    def play(self):
        while self.still_has_questions:
            self.get_question()


class Player:
    def __init__(self, name):
        self._name = name

    def get_player_name(self):
        player_name = input('Please enter your name: ')
        return player_name


def get_json(x):
    return requests.get(x).json()

url = 'https://opentdb.com/api.php?amount=10&category=18&difficulty=easy&type=boolean'
answers = get_json(url)


def main():
    name = []
    player_name = Player(name)
    player_name.get_player_name()

    questions = []
    for elem in answers['results']:
        questions.append(Question(elem['question'], elem['correct_answer']))
    quiz = QuizBrain(questions)
    quiz.play()

    print("You've completed the quiz")
    print("Your final score %s: %s/%s" % (player_name, quiz.score, quiz.question_number))


if __name__ == '__main__':
    main()
