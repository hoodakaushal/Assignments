__author__ = 'hooda'

import string
from collections import defaultdict
import nltk as nl


def dummy():
    return [0, 0]


def classify(infile, outfile, dictfile):
    dictfile = open(dictfile)

    bayes = defaultdict(dummy)
    for line in dictfile:
        [word, i, j] = line.split(' ')
        i = float(i)
        j = float(j)
        bayes[word] = [i, j]

    pos_counts = 1
    neg_counts = 1
    vocab = len(bayes.keys())
    for word in bayes.keys():
        neg_counts += bayes[word][0]
        pos_counts += bayes[word][1]
    for word in bayes.keys():
        bayes[word] = [((bayes[word][0] + 1) / (neg_counts + vocab)), ((bayes[word][1] + 1) / (pos_counts + vocab))]

    dictfile.close()
    print('Model loaded.')

    infile = open(infile)
    outfile = open(outfile, 'w')
    for line in infile:
        line = filter(lambda x: x in string.printable, line)
        line.replace('\n', '').replace('\r', '')
        tokens = nl.word_tokenize(line)
        pos = 1
        neg = 1
        for token in tokens:
            if token in bayes:
                neg = neg * bayes[token][0]
                pos = pos * bayes[token][1]
        if pos > neg:
            guess = 4
        else:
            guess = 0
        outfile.write(str(guess))
        outfile.write('\n')


classify('input.txt', 'output.txt', 'bayes')