
from generateword import answer, possible_wordle_words
import random
class wordle:
    id = 1

    def __init__(self):
        self.id = self.id + 1
        self.word = random.choice(possible_wordle_words)

    def __repr__(self):
        return f"id : {self.id} "


w = wordle()


t = wordle()
g = wordle()
print(f"{w.id}: {w.word}, {t.id}: {t.word}, {g.id}:{g.word} ")

print(w)
print(t)
print(g)