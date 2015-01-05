__author__ = 'hooda'

from collections import defaultdict

import string

import nltk as nl

import math


def split(infile, count):
    f = open(infile)
    pieces = []
    for i in range(0, count):
        pieces += [open(infile + str(i), "w")]

    i = 0
    for line in f:
        target = pieces[i % count]
        target.write(line)
        i += 1
    # print("done")
    return


def ar2str(tokens):
    s = ""
    for token in tokens:
        s += ' ' + token
    return s


def tokenise(infile):
    outfile = open(infile + "_tokens", "w")
    infile = open(infile)
    for line in infile:
        line = filter(lambda x: x in string.printable, line)
        sentiment = line[1]
        tweet = line[5:-1]
        tokens = nl.word_tokenize(tweet)[0:-1]
        newline = sentiment + ar2str(tokens) + '\n'
        outfile.write(newline)
    outfile.close()
    return


def dummy():
    return [0, 0]


def compute_counts(infile):
    f = open(infile)
    newcounts = defaultdict(dummy)
    i = 0
    sawnot = False
    for line in f:
        i = i + 1
        # print(i)
        words = line.split(' ')
        for word in words[1:]:
            word = word.replace('\n', '').replace('\r', '')
            # if word == 'not' or word == '.' or word == ',' or word == "isn't" or word == "wasn't":
            # sawnot = not sawnot
            # if sawnot:
            # word = 'NOT_' + word
            #     if words[0] == '4':
            #         newcounts[word][0] += 1
            #     else:
            #         newcounts[word][1] += 1
            #
            # else:
            #     if words[0] == '0':
            #         newcounts[word][0] += 1
            #     else:
            #         newcounts[word][1] += 1
            if words[0] == '0':
                newcounts[word][0] += 1
            else:
                newcounts[word][1] += 1
    return newcounts


def compute(infile):
    counts = compute_counts(infile)
    outfile = open(infile + '_counts', 'w')
    for word in counts.keys():
        line = word + ' ' + str(counts[word][0]) + ' ' + str(counts[word][1]) + '\n'
        outfile.write(line)
    outfile.close()


def combine(files):
    counts = defaultdict(dummy)
    outfile = open('training_tokens_counts_of8', 'w')
    for f in files:
        print(f)
        fstream = open(f)
        for line in fstream:
            # print(line)
            # time.sleep(5)
            [word, i, j] = line.split(' ')
            i, j = int(i), int(j)
            counts[word][0] += i
            counts[word][1] += j
    for word in counts.keys():
        line = word + ' ' + str(counts[word][0]) + ' ' + str(counts[word][1]) + '\n'
        outfile.write(line)
    outfile.close()


def evaluate(dict, input):
    right = 0
    wrong = 0
    dict = open(dict)
    bayes = defaultdict(dummy)
    for line in dict:
        [word, i, j] = line.split(' ')
        i = float(i)
        j = float(j)

        if i + j > 1:
            bayes[word] = [i, j]
    pos_counts = 1
    neg_counts = 1
    vocab = len(bayes.keys())
    for word in bayes.keys():
        neg_counts += bayes[word][0]
        pos_counts += bayes[word][1]
    for word in bayes.keys():
        bayes[word] = [((bayes[word][0] + 1) / (neg_counts + vocab)), ((bayes[word][1] + 1) / (pos_counts + vocab))]
    # print("model is ready! \n Proceeding with sentimentality.")

    input = open(input)
    for line in input:
        line = filter(lambda x: x in string.printable, line)
        sentiment = int(line[1])
        tweet = line[5:-2]
        tokens = nl.word_tokenize(tweet)
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
        if guess == sentiment:
            right = right + 1
        else:
            wrong = wrong + 1
    return [right, wrong]


def metavaluate(n):
    print("evaluating training", n)
    tocombine = []
    tovaluate = ''
    for i in range(0, 10):
        if not i == n:
            tocombine += ['training_tokens' + str(i) + '_counts']
        else:
            tovaluate = 'training' + str(i)
    combine(tocombine)
    return evaluate('training_tokens_counts_of8', tovaluate)


def metameta():
    right, wrong = 0, 0
    ans = []
    for i in range(0, 10):
        [right, wrong] = metavaluate(i)
        ans += [i, float(right) / (right + wrong)]
    av = ans[1:][::2]
    avr = sum(av) / 10.0
    for k in ans:
        print(k)
        print ('avr', avr)


def split2(infile, count):
    f = open(infile)
    piece1 = infile + '_research'
    target1 = open(piece1, 'w')
    target2 = open(infile + '_test', 'w')
    res = count / 2

    for i in range(0, 800000):
        if not (res == 0):
            target1.write(f.readline())
            res = res - 1
        target2.write(f.readline())

    res = count / 2
    for i in range(0, 800000):
        if not (res == 0):
            target1.write(f.readline())
            res = res - 1
        target2.write(f.readline())

    target1.close()
    target2.close()
    # print("done")


def research(tweets):
    split2('training', tweets)
    tokenised = 'training_research' + '_tokens'
    tokenise('training_research')
    compute(tokenised)
    counted = tokenised + '_counts'
    [right, wrong] = evaluate(counted, 'training_test')
    return float(right) / (right + wrong)


def counts2dict(infile):
    outfile = open('bayes2', 'w')
    dict = open(infile)
    for line in dict:
        [word, i, j] = line.split(' ')
        i = float(i)
        j = float(j)

        if i + j > 1:
            outfile.write(line)
    outfile.close()


def metaresearch():
    for i in range(0, 20):
        print(i)
        t = 2 ** i
        accuracy = research(t)
        print(i, 100 * accuracy)
