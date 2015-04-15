import random
from flask import Flask
from markovgen import Markov

app = Flask(__name__)

class Source(object):
    seeds = ['I']

    def __init__(self, dict_file):
        self.markov = Markov()

        with open(dict_file) as f:
            self.markov.feed_from_file(f, str)

    def gen(self):
        seed = random.choice(self.seeds)

        text = self.markov.generate_markov_text(seed=seed, max_size=20).strip()
        return text

SOURCE = Source('misha.txt')

@app.route('/')
def home():
    return SOURCE.gen()
