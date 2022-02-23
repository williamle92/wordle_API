import random

def load_dict(file_name):
    file = open(file_name)
    words = file.readlines()
    file.close()
    return [word[:5].upper() for word in words]

possible_wordle_words = load_dict("dict_wordle.txt")
english_5_letter_words = load_dict("english_5_words.txt")
answer = random.choice(possible_wordle_words)