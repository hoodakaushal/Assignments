__author__ = 'hooda'
import os
from random import randint

import ner


f = 'features'
t = 'training'
m = 'crfmodel'


def splitter(infile):
    infile = open(infile)


def read_train(infile):
    infile = open(infile)
    data = []
    sentence = []
    for line in infile:
        if line == '\n':
            data += [sentence]
            sentence = []
        else:
            sentence += [line]

    infile.close()
    return data


def splitter(data, file1, file2, file3):
    file1 = open(file1, 'w')
    file2 = open(file2, 'w')
    file3 = open(file3, 'w')
    for sentence in data:
        x = randint(0, 9)
        if x == 9:
            for word in sentence:
                file2.write(word[:-3])
                file2.write('\n')
                file3.write(word)
            file2.write('\n')
            file3.write('\n')
        else:
            for word in sentence:
                file1.write(word)
            file1.write('\n')
    file1.close()
    file2.close()


def tester(train, test, model, output):
    ner.feature_gen(train, 'train_f')
    ner.feature_gen_test(test, 'test_f')
    train_f = 'train_f'

    test_f = 'test_f'
    # test_f = test
    mallet = 'java -cp "mallet/class:mallet/lib/mallet-deps.jar" cc.mallet.fst.SimpleTagger --threads 16 '

    train_command = mallet + '--iterations 3000 --train true --model-file ' + model + ' ' + train_f + ' >bhasad'
    test_command = mallet + '--model-file ' + model + ' ' + test_f + ' >' + output

    os.system(train_command)
    os.system(test_command)

    testfile = open(test)
    outfile = open(output)

    final = open('final', 'w')
    t = testfile.readlines()
    o = outfile.readlines()

    if len(t) != len(o):
        raise IOError
    else:
        for i in range(len(t)):
            final.write(t[i][:-1] + ' ' + o[i][:-2] + '\n')
        final.close()


def eval(final, gold):
    os.system('python F_Score_Assignment3.py ' + final + ' ' + gold + ' >result')


splitter(read_train('ner.txt'), 'train', 'test', 'gold')

tester('train', 'test', 'crfmodel', 'output')

eval('final', 'gold')

# def slice(ar):
# for i in range(0,len(ar)):
# print ar[max(0,i-2):i + 3]
#
# slice(range(0,15))



