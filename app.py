import random
from flask import Flask
from flask import render_template, request, Response
from functools import wraps
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

    @property
    def seed(self):
        seeds = self.seeds.get(self.lang, [])
        return random.choice(seeds) if len(seeds) > 0 else None

    def gen(self, seed=None, size=20):
        text = self.markov.generate_markov_text(seed=seed, max_size=size)
        text = text.strip()

        return text

LANGS = ['fr', 'en', 'es']
SOURCES = dict([(lang, Source(lang)) for lang in LANGS])

# Utils
def content_type(mimetype, charset=None):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            res = f(*args, **kwargs)

            if not isinstance(res, Response):
                res = Response(res)

            res.content_type = mimetype
            if charset is not None:
                res.content_type += '; charset=%s' % (charset)
            return res
        return wrapped
    return wrapper

# App
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/<lang>')
@content_type('text/plain', charset='utf-8')
def gen(lang):
    '''
        ?seed=<seed>    - Choose a start word. (default: choose from a list)
        ?size=<size>    - Set the max sentence size. (default: 20)
        ?noseed         - Do not choose automatically a seed.
    '''
    if 'help' in request.args:
        return Response(gen.__doc__)

    source = SOURCES.get(lang)

    if source is None:
        return 'Lang not found. :('

    seed = request.args.get('seed', source.seed)
    size = request.args.get('size', 20)

    if 'noseed' in request.args:
        seed = None

    return Response(source.gen(seed=seed, size=int(size)))

if __name__ == '__main__':
    app.run(debug=True)
