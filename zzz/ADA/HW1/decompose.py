__author__ = 'hooda'

global graph
global props
global counter
global edgestack
global components
global extracomponents

graph = {}
props = {}
counter = 0
edgestack = []
components = []
extracomponents = []


def reader(filename):
    mygraph = {}
    file = open(filename)
    for line in file.readlines()[1:]:
        line = line.replace('\n', '')
        line = line.split('->')
        # print(line)
        if line[-1] == '':
            line = line[0:-1]
        mygraph[line[0]] = line[1:]
    return mygraph


def edgelist_to_vertexlist(list_edgelist):
    list_vertexlist = []
    for edgelist in list_edgelist:
        vertexlist = []
        for edge in edgelist:
            if edge[0] not in vertexlist:
                vertexlist += [edge[0]]
            if edge[1] not in vertexlist:
                vertexlist += [edge[1]]
        list_vertexlist += [vertexlist]
    return list_vertexlist


def writer(list_stringlist):
    list_string = []
    list_stringlist = sorted(list_stringlist, key=len)
    list_stringlist = list(map(sorted, list_stringlist))
    for stringlist in list_stringlist:
        s = str(stringlist)
        s = s[1:-1]
        s = s.replace("'", "").replace(' ', '')
        list_string += [s]
    return list_string


def printer(filename, list_string):
    myfile = open(filename, 'w')
    myfile.write(str(len(list_string)))
    myfile.write('\n')
    for s in list_string:
        myfile.write(s)
        myfile.write('\n')
    myfile.close()


def prop_init(mygraph):
    myprops = {}
    for vertex in mygraph.keys():
        myprops[vertex] = [False, 0, 0]
    return myprops


def biconnected():
    global graph
    global props
    global counter
    global edgestack
    global components
    global extracomponents

    counter = 0
    edgestack = []
    for vertex in sorted(graph.keys()):
        if props[vertex][0] is False:
            prev = len(components)
            old_visited = []
            for v in graph.keys():
                if props[v][0]:
                    old_visited += [v]

            dfs(vertex, vertex)

            new = len(components)
            # We do this in case there IS no critical vertex, then the dfs will not add anything to components.
            # But, clearly if there is no critical vertex then graph is biconnected
            # (OR IS IT?? Well, I've decided to output it.)
            if new == prev:
                new_visited = []
                for v in graph.keys():
                    if props[v][0]:
                        new_visited += [v]
                visited_now = list(set(new_visited) - set(old_visited))
                extracomponents += [visited_now]


def dfs(v, u):
    global graph
    global props
    global counter
    global edgestack
    global components
    global extracomponents

    counter += 1
    props[v][0] = True
    props[v][1] = counter
    props[v][2] = counter

    for w in graph[v]:
        if props[w][0] is False:
            props[v][0] = True
            edgestack += [[v, w]]
            dfs(w, v)
            props[v][2] = min(props[v][2], props[w][2])
            if props[w][2] >= props[v][1]:
                newcomp = []
                flag = True
                while flag and len(edgestack) > 0:
                    edge = edgestack.pop()
                    if edge == [v, w]:
                        flag = False
                    newcomp += [edge]
                components += [newcomp]

        elif props[w][1] < props[v][1] and w is not u:
            edgestack += [[v, w]]
            props[v][2] = min(props[v][2], props[w][1])

    return


def runner(f_in, f_out):
    global graph
    global props
    global counter
    global edgestack
    global components
    global extracomponents

    graph = reader(f_in)
    props = prop_init(graph)
    biconnected()
    final_components = edgelist_to_vertexlist(components) + extracomponents
    to_print = writer(final_components)
    printer(f_out, to_print)


def printx(mygraph):
    for v in mygraph.keys():
        print(v, mygraph[v])


runner('t.txt', 'output.txt')