import argparse
import urllib.request
import os
import random

def ask(prompt: str, valid: list[str] = None):
    inp_word = input(prompt)
    if valid is not None:
        while inp_word not in valid:
            if inp_word == ".": return inp_word
            inp_word = input(prompt)
    return inp_word

def inform(format_string: str, bulls: int, cows: int):
    print(format_string.format(bulls, cows))

def gameplay(ask: callable, inform: callable, words: list[str]):
    secret = random.choice(words)
    attempts = 0
    guess="."
    while guess != secret:
        guess = ask("Введите слово: ", words)
        if guess == ".":
            print("Вы проиграли. Загаданное слово: ",secret)
            return attempts
        attempts += 1
        #bulls, cows = bullscows(guess, secret)
        inform("Быки: {}, Коровы: {}", bulls, cows)
    print("Вы победили!")
    return attempts

parser = argparse.ArgumentParser()
parser.add_argument('dict', type=str)
parser.add_argument('len', nargs='?', default=5, type=int)
args = parser.parse_args()

if args.dict.startswith("http"):
    with urllib.request.urlopen(args.dict) as response:
        data = response.read().decode("utf-8")
        words = [w for w in filter(lambda w : len(w) == args.len, data.split("\n"))]
else:
    with open(args.dict, "r") as f:
        words = [w.strip() for w in filter(lambda w : len(w.strip()) == args.len, f)]

#print(len(words))
print("Конец игры. Количество попыток: ", gameplay(ask, inform, words))

