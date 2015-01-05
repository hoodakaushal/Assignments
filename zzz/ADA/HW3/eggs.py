__author__ = 'hooda'

global solved
solved = {}

global matrix
# matrix[egg][floor]
matrix = []

global auxmat
auxmat = []


def eggsdrop(floors, eggs):
    global solved
    global auxmat

    case = (floors, eggs)
    if eggs == 0:
        print(case)
    # print(case)
    if case in solved:
        return solved[case]

    elif floors == 0:
        solved[case] = 0
        return 0

    elif floors == 1:

        solved[case] = 1
        return 1

    elif eggs == 1:
        solved[case] = floors
        return floors

    else:
        possibilities = []
        for i in range(1, floors + 1):
            cand = max(eggsdrop(i - 1, eggs - 1), eggsdrop(floors - i, eggs))
            possibilities += [cand]
        ans = 1 + min(possibilities)
        solved[case] = ans
        return ans


def dynadrop(floors, eggs):
    global matrix
    global auxmat

    # For 1 egg -> n trials
    for i in range(0, floors + 1):
        matrix[1][i] = i
    # For 0 or 1 floors -> 0 or 1 trials
    for i in range(1, eggs + 1):
        matrix[i][0] = 0
        matrix[i][1] = 1

    for e in range(2, eggs + 1):
        for f in range(2, floors + 1):
            mincount = float('inf')
            minfloor = float('inf')
            for i in range(1, f + 1):
                cand = max(matrix[e - 1][i - 1], matrix[e][f - i])
                if cand < mincount:
                    mincount = cand
                    minfloor = i

            matrix[e][f] = 1 + mincount
            auxmat[e][f] = minfloor

    return matrix[eggs][floors]


def matprint(A):
    print('\n'.join([''.join(['{:4}'.format(item) for item in row])
                     for row in A]))
    print('--------------------------')


# print(eggsdrop(100, 0))
# print(len(solved.keys()))

def runner(floors, eggs):
    if eggs == 1:
        s1 = str(floors - 1) + '\n'
        s2 = str(range(1, floors))[1:-1].replace(' ', '')
        return s1, s2
    global matrix
    matrix = []
    global auxmat
    auxmat = []
    for x in range(eggs + 1):
        matrix.append([-1] * (floors + 1))
        auxmat.append([0] * (floors + 1))
    trials = dynadrop(floors, eggs)

    s = ''
    i = eggs
    j = floors
    offset = 0
    cnt = 0
    while True:
        if j == 1:
            break
        if i == 1:
            s += str(1 + offset)
            cnt += 1
            if not (cnt == trials):
                s += ','
            j -= 1
            offset += 1
        else:
            s += str(auxmat[i][j])
            cnt += 1
            if not (cnt == trials):
                s += ','
            x = auxmat[i][j]
            t1 = matrix[i - 1][x - 1]
            t2 = matrix[i][j - x]

            if t1 > t2:
                i = i - 1
                j = x - 1
            else:
                j = j - x
                offset += x

    print(trials)
    print(s)

    s = s[:-1].split(',')
    s = list(map(int, s))
    s.sort()
    s.reverse()
    news = []
    sum = 0
    for i in s:
        sum += i
        news += [sum]
    news += [news[-1] - 1]
    s1 = str(trials) + '\n'
    s2 = str(news)[1:-1].replace(' ', '')
    return s1, s2


def runner2():
    f = open('input.txt')
    test = f.readline().replace('\n', '').replace('\r', '').split(',')
    floors = int(test[0])
    eggs = int(test[1])
    s1, s2 = runner(floors, eggs)

    f = open('output.txt', 'w')
    f.write(s1)
    f.write(s2)


runner2()

# matprint(matrix)