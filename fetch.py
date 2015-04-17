#!/usr/bin/env python
import re
from argparse import ArgumentParser
from collections import defaultdict
from pathlib import Path

GLOB_PATTERN = '**/script-*.rpy'

SCRIPT_PATTERN = r'(.+)_(?P<lang>[A-Z]{2})\.rpy$'
SCRIPT_PATTERN = re.compile(SCRIPT_PATTERN)

MISHA_PATTERN = r'mi "(?P<sentence>[^"]+)"'
MISHA_PATTERN = re.compile(MISHA_PATTERN)

REMOVE_PATTERNS = [
    r'~',
    r'\{[^}]+\}',
]
REMOVE_PATTERNS = [re.compile(pattern) for pattern in REMOVE_PATTERNS]

def fetch_file(input_file):
    def extract(line):
        sentence = None

        m = MISHA_PATTERN.match(line)
        if m:
            sentence = m.group('sentence')
            for pattern in REMOVE_PATTERNS:
                sentence = pattern.sub('', sentence)

        return sentence

    with input_file.open() as f:
        sentences = map(extract, f)
        sentences = filter(bool, sentences)
        sentences = list(sentences)

        return sentences

def fetch(input_dir, output_dir):
    langs = defaultdict(list)

    for path in input_dir.glob(GLOB_PATTERN):
        lang = 'en'

        m = SCRIPT_PATTERN.match(path.name)
        if m:
            lang = m.group('lang').lower()

        langs[lang].append(path)

    if not output_dir.exists():
        output_dir.mkdir(parents=True)

    for (lang, paths) in langs.items():
        output_file = output_dir / ('misha.%s.txt' % (lang))

        with output_file.open('w+') as f:
            for path in paths:
                for sentence in fetch_file(path):
                    f.write('%s\n' % (sentence))

# Main
parser = ArgumentParser()
parser.add_argument('input_dir', type=Path, help='Pass the Katawa Shoujo folder with decompiled sources containing sentences')
parser.add_argument('output_dir', type=Path, help='Output directory.')

def main(args):
    fetch(args.input_dir, args.output_dir)

if __name__ == '__main__':
    main(parser.parse_args())
