__author__ = 'hooda'


def intersection(line1, line2):
    [line1, line2] = sorted([line1, line2])
    if line1[0] == line2[0]:
        print("INVALID")
    m1, c1, m2, c2 = line1[0], line1[1], line2[0], line2[1]

    x = (c2 - c1) / (m1 - m2)
    y = (m2 * c1 - m1 * c2) / (m2 - m1)
    print('interstection', line1, line2, x, y)
    return [x, y]


def visible(lines):
    # print(lines)
    # print("visible check", lines)
    if len(lines) == 1:
        return [[float("-inf"), float("inf"), lines[0]]]

    if len(lines) == 2:
        line1 = lines[0]
        line2 = lines[1]
        point = intersection(line1, line2)
        return [[float("-inf"), point[0], line1], [point[0], float("inf"), line2]]

    mid = len(lines) / 2
    struct1 = visible(lines[0:mid])
    struct2 = visible(lines[mid:])

    struct = combine(struct1, struct2)
    # print("visibleD ", struct)
    return struct


def combine(struct1, struct2):
    # print("combining''''''''''''''''''''''''''''''''''''''")
    # print(struct1)
    # print(struct2)
    # IDEA : We assume that struct1 is from the lower slope half, struct2 from the higher slop half.
    # Now, we merge the intersection points in struct1 and struct2. We get something like:
    # p11, p12, p21, p13, p22 etc. some random order. The insight is the point of intersection we're looking for
    # Must lie between consec. p's. (Or straight up outside the range).
    # So we sort of pick each interleaving, find the corresponding lines
    # in that region, and check if their intersection is also in that region.

    # Another approach is to notice that as we approach form -infinity, struct2 must be lower,
    # and as we approach +infinity, struct2 must be higer.
    # The point of intersection is where this flip happens. This is also a reasonable approach,
    # but the corner casses etc. need to be considered.

    # Unsaid here is the assumption that there is one and only one point of intersection.
    # I can't come up with a definite proof, but it seems reasonable nonetheless.


    # The flippy approach.
    # Struct1 is required by intergalactic law to be low-slope struct.

    # if the infinity lines intersect at x < x10 and x20, we are done. Similarly for x > x1n and x2n.
    infx = intersection(struct1[0][2], struct2[0][2])[0]
    # print("infx", infx)
    inf2x = intersection(struct1[-1][2], struct2[-1][2])[0]
    # print("inf2x", inf2x)
    if infx <= min(struct1[0][1], struct2[0][1]):
        final = [[float("-inf"), infx, struct1[0][2]], [infx, struct2[0][1], struct2[0][2]]] + struct2[1:]

    elif inf2x >= max(struct1[-1][0], struct2[-1][0]):
        final = struct1[0:-1] + [[struct1[-1][0], inf2x, struct1[-1][2]], [inf2x, float("inf"), struct2[-1][2]]]

    # Otherwise we truncate the structs to finite lengths. Find the intersection using flipping.
    else:
        minx = min(struct1[0][1], struct2[0][1])
        maxx = max(struct1[-1][0], struct2[-1][0])
        struct1a = confine(struct1, minx, maxx)
        struct2a = confine(struct2, minx, maxx)

        intersectionx = struct_intersection(struct1a, struct2a)

        pos1 = getindex(intersectionx, struct1)
        pos2 = getindex(intersectionx, struct2)

        final1 = struct1[0:pos1] + [[struct1[pos1][0], intersectionx, struct1[pos1][2]]]
        final2 = [[intersectionx, struct2[pos2][1], struct2[pos2][2]]] + struct2[pos2 + 1:]
        final = final1 + final2
    flag = False
    if flag:
        print("=1=1=1=11=1=1=1=1=1=1=1=1=1=1=1=1=1=1=1")
        print(struct1, struct2)
        print("seem to have combined into")
        print(final)
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    return final


def confine(struct, x1, x2):
    # print("confinig", struct, x1, x2)
    newstruct = struct[0:]

    if newstruct[0][1] > x1:
        newstruct[0] = [x1, newstruct[0][1], newstruct[0][2]]
    elif newstruct[0][1] == x1:
        newstruct = newstruct[1:]

    if newstruct[-1][0] < x2:
        newstruct[-1] = [newstruct[-1][0], x2, newstruct[-1][2]]
    elif newstruct[-1][0] == x2:
        newstruct = newstruct[:-1]

    # print("CONNFFFIIIINNNNNEEEEEEDDDDDDD", newstruct)

    return newstruct


def struct_intersection(struct1, struct2):
    pos1 = binary_flip_search(struct1, struct2)
    pos2 = binary_flip_search(struct2, struct1)
    intersectionx = intersection(struct1[pos1][2], struct2[pos2][2])[0]
    return intersectionx


def binary_flip_search(struct, cand):
    # print("-----------------------------")
    # print("binary flip search", struct, cand)
    if len(struct) == 1:
        if higher(struct[0], cand) is 0:
            return 0
        else:
            print("ERROR. Flipping didn't happen in: ", struct, cand)

    mid = len(struct) / 2

    higher1 = higher(struct[0], cand)
    highern = higher(struct[-1], cand)
    higher_mid = higher(struct[mid], cand)

    if higher1 is 0:
        return 0
    if highern is 0:
        return len(struct) - 1
    if higher_mid is 0:
        return mid

    if higher1 == higher_mid:
        # print("in call case0|||||||||||||||||||||||")
        return mid + 1 + binary_flip_search(struct[mid + 1:-1], cand)
    else:
        # print("in call case1||||||||||||||||||||||||||")
        return 1 + binary_flip_search(struct[1:mid], cand)


def higher(region, cand):
    point1 = [region[0], gety(region[0], region[2])]
    point2 = [region[1], gety(region[1], region[2])]
    high1 = high(point1, cand)
    high2 = high(point2, cand)
    if high1 and high2:
        return 1

    elif not (high1 or high2):
        return -1

    else:
        return 0


def high(point, struct):
    # print("HIGHHIGHHIG", point, struct)
    line = struct[getindex(point[0], struct)][2]
    y = gety(point[0], line)

    # print("Results for :", point, struct, line, y)

    if point[1] >= y:
        return True
    else:
        return False


def getindex(x, struct):
    if len(struct) == 1:
        if struct[0][0] <= x <= struct[0][1]:
            return 0
        else:
            return "Out of range of struct."

    else:
        mid = len(struct) / 2
        if struct[mid][0] <= x <= struct[mid][1]:
            return mid
        elif x < struct[mid][0]:
            return getindex(x, struct[0:mid])
        elif x > struct[mid][1]:
            return mid + 1 + getindex(x, struct[mid + 1:])


def gety(x, line):
    return line[0] * x + line[1]


def reader(infile):
    linelist = []
    infile = open(infile)
    lines = infile.readlines()

    for i in range(1, int(lines[0]) + 1):
        line = lines[i].split(":")
        linelist += [[float(line[0]), float(line[1]), i]]
    return linelist


def writer(outfile, struct):
    outfile = open(outfile, "w")
    visibles = []
    for i in range(0, len(struct)):
        visibles += [struct[i][2][2]]
    visibles = sorted(list(set(visibles)))
    s = str(visibles)
    s = s[1:-1]
    s = s.replace("'", "").replace(' ', '')
    # print(s)
    outfile.write(s)
    outfile.close()
    return s


def clean(lines):
    if len(lines) < 2:
        return lines
    i = 1
    while i < len(lines):
        now = lines[i][0]
        prv = lines[i - 1][0]
        if now == prv:
            # print(len(lines))
            # print("hahaha. lele fuckru")
            lines = lines[0:i - 1] + lines[i:]
            # i += 1
            # print(len(lines))
        else:
            i += 1
    return lines


def runner(inf, outf):
    lines = reader(inf)
    lines.sort()
    lines = clean(lines)
    # sure = superbrute(lines)
    struct = visible(lines)
    s = writer(outf, struct)
    # surelines = []
    # for line in sure:
    # surelines += [line[2]]
    # s = str((sorted(surelines)))
    # s = s[1:-1].replace(' ', '')
    print(s)
    return s


infile = "input.txt"
outfile = "output.txt"


def superbrute(lines):
    visibles = []
    for line in lines:
        if brute(lines, line):
            visibles += [line]
    print(visibles)
    return visibles


def brute(lines, mine):
    # print(len(lines))
    intersections = []
    for line in lines:
        if not mine == line:
            intersections += [intersection(line, mine)[0]]
    # intersections.sort()
    ivisible = False
    print(intersections)
    for x in intersections:
        my = gety(x, mine)
        print('my',x,my)
        high = True
        for line in lines:
            if not mine == line:
                print('ot',x,gety(x, line))
                if gety(x, line) > my:
                    print('other was higher')
                    high = False

        if high:
            ivisible = True
            # print(mine)
            return ivisible
    return ivisible


import random


def generate(n):
    mylines = []
    for i in range(1, n + 1):
        m = float(random.uniform(-100000, 100000))
        c = float(random.uniform(-100000, 100000))
        mylines += [[m, c, i]]
    f = open('input.txt', 'w')
    f.write(str(n) + '\n')
    for line in mylines:
        f.write(str(line[0]) + ':' + str(line[1]) + '\n')
    return mylines


def supertest(n):
    # lines = generate(n)
    # lines.sort()
    # lines = clean(lines)
    # for line in lines:
    # print(line)
    # print("Doing Brute Forces")
    # sure = superbrute(lines)

    print("doing ninja speed mode")
    maybe = visible(lines)
    writer(outfile, maybe)
    surelines = []
    for line in sure:
        surelines += [line[2]]
    s = str((sorted(surelines)))
    s = s[1:-1].replace(' ', '')
    print(s)


def infitest():
    # print('lol')
    # return
    while True:
        i = int(raw_input('What now?'))
        lines = generate(i)
        print(sorted(lines))
        maybe = runner('input.txt', 'output.txt')
        sure = superbrute(lines)
        surelines = []
        for line in sure:
            surelines += [line[2]]
        s = str((sorted(surelines)))
        s = s[1:-1].replace(' ', '')
        print('sure',s)
        print('maybe',maybe)

# runner('input.txt','output.txt')
# infitest()

# TODO make etc. files for script based checking.
