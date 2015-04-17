import random
from flask import Flask
from flask import render_template
from markovgen import Markov

DICT_FILE = 'misha.{lang}.txt'

# Source
class Source(object):
    seeds = {
        'en': ['I', 'It'],
        'fr': ['Je'],
        'es': [],
    }

    def __init__(self, lang):
        self.markov = Markov()
        self.lang = lang

        dict_file = DICT_FILE.format(lang=lang)
        with open(dict_file) as f:
            self.markov.feed_from_file(f, str)

    def gen(self, size=20):
        seed = None

        seeds = self.seeds.get(self.lang, [])
        if len(seeds) > 0:
            seed = random.choice(seeds)

        text = self.markov.generate_markov_text(seed=seed, max_size=size)
        text = text.strip()

        return text

LANGS = ['fr', 'en', 'es']
SOURCES = dict([(lang, Source(lang)) for lang in LANGS])

# App
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/<lang>')
def gen(lang):
    source = SOURCES.get(lang)

    if source is None:
        return 'Lang not found. :('

    return source.gen()

@app.route('/about')
def about():
    return 'https://github.com/KokaKiwi/mishafacts'

if __name__ == '__main__':
    app.run(debug=True)
