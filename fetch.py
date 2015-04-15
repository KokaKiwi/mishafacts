#!/usr/bin/env python
import glob2
import re
from argparse import ArgumentParser

GLOB_PATTERN = '*.rpy'
MISHA_PATTERN = r'mi "(?P<sentence>[^"]+)"'
REMOVE_PATTERNS = [
    r'~',
    r'\{[^}]+\}',
]

def fetch_file(input_file):
    pattern = re.compile(MISHA_PATTERN)

    def extract(line):
        for remove_pattern in REMOVE_PATTERNS:
            line = re.sub(remove_pattern, '', line)
        m = pattern.match(line)
        if m:
            return m.group('sentence')

        return None

    is_something = lambda o: o is not None

    with open(input_file) as f:
        lines = filter(is_something, map(extract, f))
        sentences = list(lines)
        return sentences

def fetch(input_folder, output_file):
    def is_en(filename):
        m = re.match(r'(.*)_[A-Z]{2}\.rpy$', filename)
        return m is None

    input_pattern = '%s/%s' % (input_folder, GLOB_PATTERN)
    input_files = list(glob2.iglob(input_pattern))
    input_files = filter(is_en, input_files)

    sentences = []
    for file in input_files:
        sentences += fetch_file(file)

    with open(output_file, 'w+') as f:
        for sentence in sentences:
            f.write('%s\n' % (sentence))

# Main
parser = ArgumentParser()
parser.add_argument('input_folder')
parser.add_argument('output_file')

def main(args):
    fetch(args.input_folder, args.output_file)

if __name__ == '__main__':
    main(parser.parse_args())
