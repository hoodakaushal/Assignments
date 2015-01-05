# Get the list of tweets from input.txt
import sys


din = 'input.txt'
dout = 'output.txt'

if len(sys.argv) > 1:
    din = sys.argv[1]

punctuations = ["'", '"', '[', ']', '{', '}', '(', ')', ':', ',', '!', '.', '?', ';']
clitics = {"they're": ['they', 'are'], "we'll": ['we', 'will'], "you're": ['you', 'are'], "we've": ['we', 'have'],
           "he's": ['he', 'is'], "they've": ['they', 'have'], "can't": ['can', 'not'], "won't": ['will', 'not'],
           "we're": ['we', 'are'], "couldn't": ['could', 'not'], "she's": ['she', 'is'], "i'm": ['I', 'am'],
           "I'm": ['I', 'am'], "haven't": ['have', 'not'], "shouldn't": ['should', 'not'], "didn't": ['did', 'not'],
           "don't": ['do', 'not']}


def reader(filename):
    f = open(filename)
    tweets = []
    for line in f:
        tweets += [line[:-1]]
    return tweets


def writer(strings, output):
    output = open(output, 'w')
    for s in strings[:-1]:
        output.write(s)
        output.write('\n')
    output.write(strings[-1])
    output.close()


def tokenise(tweet):
    tokens = tweet.split(' ')
    tokens = depunctuate(tokens)
    tokens = clitic(tokens)
    tokens = dehyphenate(tokens)
    i = tokens.count('')
    for j in range(0, i):
        tokens.remove('')
    # print(tokens)
    return tokens


def clitic(tokens):
    tokens2 = []
    for i in range(0, len(tokens)):
        s = tokens[i]
        # print(clitics.keys())
        # print(s)
        if s in clitics.keys():
            tokens2 += clitics[s]
        else:
            tokens2 += [s]
    return tokens2


def dehyphenate(tokens):
    tokens2 = []
    for i in range(0, len(tokens)):
        if '-' in tokens[i]:
            pieces = tokens[i].split('-')
            pieces[1] = '-' + pieces[1]
            tokens2 += pieces
        else:
            tokens2 += [tokens[i]]
    return tokens2


def depunctuate(tokens):
    tokens2 = []
    for j in range(0, len(tokens)):
        tokens2 += rempunc(tokens[j])
    return tokens2


def rempunc(s):
    a = ''
    b = ''
    c = ''
    ret = []
    i = 0
    while i < len(s) and s[i] in punctuations:
        a += s[i]
        i += 1
    s = s[i:]

    i = 1
    while i < len(s) + 1 and s[-i] in punctuations:
        i += 1
    c = s[-i + 1:]
    s = s[0:-i + 1]

    if (a is not ''):
        ret += [a]
    if (s is not ''):
        ret += [s]
    if (c is not ''):
        ret += [c]
    return ret


def runner(filename, outname):
    tweets = reader(filename)
    tokens = []
    for tweet in tweets:
        tokens += [tweet]
        # print(tweet)
        t = tokenise(tweet)
        tokens += [str(len(t))]
        tokens += t
    print(len(tokens))
    writer(tokens, outname)


def x():
    runner(din, dout)


x()
# print(tokenise("i didn't do it!"))
# print(rempunc('@anitapuspasari....'))

# Step 1 : Basic setup of program. Mostly created functions to read the input file, print the tokens
# according to the specified format. Also created a very basic tokeniser that split using just spaces.
# Got an F Score of 0.62
#
# Next, I started to add to and improve the tokeniser function.
# There were several things to be done - splitting hyphenated words, taking care of clitics,
# URLs etc. I have decided to work only with single words - that is, first split the tweets by spaces, and
# then worry about the individual pieces. While it has the disadvantage of missing out things like words with spaces
# between them (R E T W E E T, for instance), as well as not breaking up tokens where spaces are missing (like around a period),
# it has the advantage that I no longer have to worry about incorrectly splitting URLs, hashtags etc.I
#
# For punctuations, I created a list of punctuation marks and stripped any occurences of them from the beginning and the end.
# As specified on piazza, multiple marks (like !!!) are to be considered a single token.
# This done, I manually expanded all the clitics by creating a dictionary. Majority of the cases are covered in it, though not every single
# one.

