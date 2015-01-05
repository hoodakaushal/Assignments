import os

__author__ = 'hooda'

# Step 1 : Generate features from training data.
# Step 2 : Train CRF using mallet.
# Step 3 : Evaluate the CRF.
# Step 4 : Do it again for the test set.
# So, effectively - python need only generate features.
# Features - prev WORD next, POS tag.

import nltk as nl
import string
from collections import defaultdict
import sys


def dummy():
    return 0


def compute_counts(infile):
    stop_words = ['a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', "aren't",
                  'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by',
                  "can't", 'cannot', 'could', "couldn't", 'did', "didn't", 'do', 'does', "doesn't", 'doing', "don't",
                  'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', "hadn't", 'has', "hasn't", 'have',
                  "haven't", 'having', 'he', "he'd", "he'll", "he's", 'her', 'here', "here's", 'hers', 'herself', 'him',
                  'himself', 'his', 'how', "how's", 'i', "i'd", "i'll", "i'm", "i've", 'if', 'in', 'into', 'is',
                  "isn't", 'it', "it's", 'its', 'itself', "let's", 'me', 'more', 'most', "mustn't", 'my', 'myself',
                  'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our',
                  'ours\tourselves', 'out', 'over', 'own', 'same', "shan't", 'she', "she'd", "she'll", "she's",
                  'should', "shouldn't", 'so', 'some', 'such', 'than', 'that', "that's", 'the', 'their', 'theirs',
                  'them', 'themselves', 'then', 'there', "there's", 'these', 'they', "they'd", "they'll", "they're",
                  "they've", 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', "wasn't",
                  'we', "we'd", "we'll", "we're", "we've", 'were', "weren't", 'what', "what's", 'when', "when's",
                  'where', "where's", 'which', 'while', 'who', "who's", 'whom', 'why', "why's", 'with', "won't",
                  'would', "wouldn't", 'you', "you'd", "you'll", "you're", "you've", 'your', 'yours', 'yourself',
                  'yourselves']

    f = open(infile)
    newcounts = defaultdict(dummy)
    i = 0
    for line in f:
        i = i + 1
        # print(i)
        words = line.split(' ')[0:1]
        for word in words:
            word = word.replace('\n', '').replace('\r', '').replace(',', '').replace('(', '').replace(')', '').lower()
            newcounts[word] += 1
    output = open(infile + '_count3', 'w')
    sorted_n = sorted(newcounts.items(), key=lambda x: x[1])
    for word in sorted_n:
        if word[0] not in stop_words:
            output.write(word[0] + ' ' + str(word[1]) + '\n')
    output.close()


# compute_counts('diseases2')

def read_train(infile):
    infile = open(infile)
    data = []
    sentence = []
    for line in infile:
        line = filter(lambda x: x in string.printable, line)
        line = line.replace("\n", '').replace('\r', '')
        if line == '':
            data += [sentence]
            sentence = []
        else:
            sentence += [(line[:-2], line[-1])]

    infile.close()
    return data


def read_test(infile):
    infile = open(infile)
    data = []
    sentence = []
    for line in infile:
        line = filter(lambda x: x in string.printable, line)
        line = line.replace("\n", '').replace('\r', '')
        if line == '':
            data += [sentence]
            sentence = []
        else:
            sentence += [line]

    infile.close()
    return data


# read = read_train('ner.txt')
# for line in read:
# print line

def feature_gen(infile, outfile):
    # diseases = open('diseases_count3')
    # d_list = set()
    # for line in diseases:
    # d_list.add(line.split(' ')[0].lower())#replace('\n',''))

    data = read_train(infile)
    features = []
    for sentence in data:
        text = []
        for word in sentence:
            text += [word[0]]
        # print text
        tagged = nl.pos_tag(text)
        featured = []
        for i in range(0, len(tagged)):
            temp = []
            temp += text[max(0, i - 0):i + 1]

            temp += ['#F_PREV_' + x for x in text[i - 1:i]]
            temp += ['#F_PREV2_' + x for x in text[i - 2:i - 1]]
            # temp += ['#F_PREV3_' + x for x in text[i-3:i-2]]

            temp += ['#F_NEXT_' + x for x in text[i + 1:i + 2]]
            # temp += ['#F_NEXT2_' + x for x in text[i+2:i+3]]
            # temp += ['#F_NEXT3_' + x for x in text[i+3:i+4]]

            # if 'chronic' in text[i-1:i+1]:
            #     temp += ['#F_CHRONIC']
            #
            # if text[i] in d_list:
            #     temp += ['#F_D_LIST']
            # else:
            #     temp += ['#F_D_UNLIST']

            # if text[i][0] in 'QWERTYUIOPASDFGHJKLZXCVBNM':
            #     temp += ['CASE_CAPITAL']
            # else:
            #     temp += ['#F_CASE_UNCAPITAL']
            #
            temp += ['#F_POS_' + tagged[i][1]]
            temp += [sentence[i][1]]
            featured += [temp]
        features += [featured]
        # print(features)
    outfile = open(outfile, 'w')
    for sentence in features:
        # print(sentence)
        for word in sentence:
            s = ''
            for letter in word:
                s = s + letter + ' '
            s = s[:-1] + '\n'
            outfile.write(s)
        outfile.write('\n')
    outfile.close


def feature_gen_test(infile, outfile):
    # diseases = open('diseases_count3')
    # d_list = set()
    # for line in diseases:
    # d_list.add(line.split(' ')[0].lower())#replace('\n',''))

    data = read_test(infile)
    features = []
    for sentence in data:
        # print sentence
        text = []
        for word in sentence:
            text += [word]
        # print text
        tagged = nl.pos_tag(text)
        featured = []
        for i in range(0, len(tagged)):
            temp = []
            temp += text[max(0, i - 0):i + 1]

            temp += ['#F_PREV_' + x for x in text[i - 1:i]]
            temp += ['#F_PREV2_' + x for x in text[i - 2:i - 1]]
            # temp += ['#F_PREV3_' + x for x in text[i-3:i-2]]

            temp += ['#F_NEXT_' + x for x in text[i + 1:i + 2]]
            # temp += ['#F_NEXT2_' + x for x in text[i+2:i+3]]
            # temp += ['#F_NEXT3_' + x for x in text[i+3:i+4]]

            # if 'chronic' in text[i-1:i+1]:
            #     temp += ['#F_CHRONIC']

            # if text[i] in d_list:
            #     temp += ['#F_D_LIST']
            # else:
            #     temp += ['#F_D_UNLIST']

            # if text[i][0] in 'QWERTYUIOPASDFGHJKLZXCVBNM':
            #     temp += ['CASE_CAPITAL']
            # else:
            #     temp += ['#F_CASE_UNCAPITAL']
            #
            temp += ['#F_POS_' + tagged[i][1]]
            # temp += [sentence[i][1]]
            featured += [temp]
        features += [featured]
        # print(features)
    outfile = open(outfile, 'w')
    for sentence in features:
        # print(sentence)
        for word in sentence:
            s = ''
            for letter in word:
                s = s + letter + ' '
            s = s[:-1] + '\n'
            outfile.write(s)
        outfile.write('\n')
    outfile.close


# feature_gen_test('test', 'test_f')
# print feature_gen('ner.txt', 'ner_f')

def runner(model, test, outfile):
    feature_gen_test(test, 'test_f')
    output = 'output'

    test_f = 'test_f'
    # test_f = test
    mallet = 'java -cp "mallet/class:mallet/lib/mallet-deps.jar" cc.mallet.fst.SimpleTagger --threads 16 '
    # mallet = 'java -cp $MALLET_INC cc.mallet.fst.SimpleTagger --threads 4 '

    test_command = mallet + '--model-file ' + model + ' ' + test_f + ' >' + output

    os.system(test_command)

    testfile = open(test)
    beta = open(output)

    final = open(outfile, 'w')
    t = testfile.readlines()
    o = beta.readlines()

    if len(t) != len(o):
        raise IOError
    else:
        for i in range(len(t)):
            final.write(t[i][:-1] + ' ' + o[i][:-2] + '\n')
        final.close()

# def merge(file1, file2, res):
#     file1 = open(file1)
#     file2 = open(file2)
#     res = open(res, 'w')
#

arg = sys.argv

# if not len(arg) > 2:
# raise IOError
#
# runner('crfmodel', arg[1], arg[2])
runner('crfmodel', 'test_input.txt', 'test_output.txt')
# runner('crfmodel', 'test_my_input','test_my_output')

# Data : baseline
# microF_Score is tpT0.307692,
# microPrecision is 0.796380
# microRecall is 0.190683
# macroF_Score is 0.300615,
# macroPrecision is 0.814495
# macroRecall is 0.184323

# Data : With prev
# microF_Score is tpT0.490295,
# microPrecision is 0.751101
# microRecall is 0.363927
# macroF_Score is 0.468933,
# macroPrecision is 0.731513
# macroRecall is 0.345069

# Data : with prev and next
# microF_Score is tpT0.463546,
# microPrecision is 0.786458
# microRecall is 0.328618
# macroF_Score is 0.453509,
# macroPrecision is 0.790152
# macroRecall is 0.318018

# Data : with prev and chronic
# microF_Score is tpT0.444109,
# microPrecision is 0.717073
# microRecall is 0.321663
# macroF_Score is 0.430317,
# macroPrecision is 0.699302
# macroRecall is 0.310778

# Data : with prev and Dlist
# microF_Score is tpT0.355879,
# microPrecision is 0.777273
# microRecall is 0.230769
# macroF_Score is 0.319528,
# macroPrecision is 0.741227
# macroRecall is 0.203661

# Data : with prev and capital
# microF_Score is tpT0.379585,
# microPrecision is 0.746082
# microRecall is 0.254545
# macroF_Score is 0.380724,
# macroPrecision is 0.757422
# macroRecall is 0.254266

# Data : with prev and POSTag
# microF_Score is tpT0.546125,
# microPrecision is 0.654867
# microRecall is 0.468354
# macroF_Score is 0.545290,
# macroPrecision is 0.680770
# macroRecall is 0.454784

# Data : with prev123 and POSTag
# microF_Score is tpT0.576311,
# microPrecision is 0.736446
# microRecall is 0.473379
# macroF_Score is 0.559310,
# macroPrecision is 0.718161
# macroRecall is 0.458004

# Data : with prev123 next123 POSTag
# microF_Score is tpT0.595588,
# microPrecision is 0.733696
# microRecall is 0.501238
# macroF_Score is 0.588570,
# macroPrecision is 0.734737
# macroRecall is 0.490909

# Data : with prev123 next1 POSTag
# microF_Score is tpT0.601671,
# microPrecision is 0.781193
# microRecall is 0.489241
# macroF_Score is 0.602026,
# macroPrecision is 0.782396
# macroRecall is 0.489239

# Data : with prev123 next1 POSTag DLIST (v2.3)l
# microF_Score is tpT0.624490,
# microPrecision is 0.787307
# microRecall is 0.517475
# macroF_Score is 0.615719,
# macroPrecision is 0.781757
# macroRecall is 0.507855

# Data : with prev12 next1 POSTag DLIST(v2.3)l
# microF_Score is tpT0.631850,
# microPrecision is 0.804598
# microRecall is 0.520170
# macroF_Score is 0.625133,
# macroPrecision is 0.808194
# macroRecall is 0.509686
