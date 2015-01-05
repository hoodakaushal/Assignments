__author__ = 'hooda'

# Implementing the ford fulkerson algorithm for max-flow.

from collections import defaultdict


def dummy():
    return []


def dummy2():
    return 0


# Graph and capacity have to be defaultdicts with default value as returned by dummy and dummy2 respectively.
def fulkerson(source, sink, graph, capacity):
    [aug_graph, flow] = initialise(graph)
    path = find_path(source, sink, aug_graph, flow, capacity, [])

    while not (path is None):
        increment = min([capacity[edge] - flow[edge] for edge in path])
        for edge in path:
            flow[edge] += increment
            flow[(edge[1], edge[0])] -= increment
        path = find_path(source, sink, aug_graph, flow, capacity, [])

    return flow


def initialise(graph):
    flow = {}
    aug_graph = defaultdict(dummy)
    for a in graph.keys():
        aug_graph[a] = []

    for a in graph.keys():
        for b in graph[a]:
            aug_graph[a] += [b]
            aug_graph[b] += [a]
            flow[(a, b)] = 0
            flow[(b, a)] = 0
    return [aug_graph, flow]


def find_path(source, sink, aug_graph, aug_cap, capacity, path):
    if source == sink:
        return path

    for vertex in aug_graph[source]:
        edge = (source, vertex)
        if capacity[edge] - aug_cap[edge] > 0 and edge not in path:
            result = find_path(vertex, sink, aug_graph, aug_cap, capacity, path + [edge])
            if result is not None:
                return result


def make_capacity(graph):
    capacity = {}
    for a in graph.keys():
        for b in graph[a]:
            capacity[(a, b)] = 1
    return capacity


def test():
    # Expected Max flow is 5.
    graph = defaultdict(dummy)
    graph['s'] = ['o', 'p']
    graph['o'] = ['p', 'q']
    graph['p'] = ['r']
    graph['q'] = ['r', 't']
    graph['r'] = ['t']

    capacity = defaultdict(dummy2)
    capacity[('s', 'o')] = 3
    capacity[('s', 'p')] = 3
    capacity[('o', 'p')] = 2
    capacity[('o', 'q')] = 3
    capacity[('p', 'r')] = 2
    capacity[('r', 't')] = 3
    capacity[('q', 'r')] = 4
    capacity[('q', 't')] = 2

    flow = fulkerson('s', 't', graph, capacity)

    for v in graph.keys():
        for e in graph[v]:
            print(v, e, flow[(v, e)])


# Solving the given problem.

def reader(infile):
    infile = open(infile)

    n = infile.readline()
    n = list(map(int, n.strip().replace('\n', '').replace('\r', '').split(' ')))[0]
    data = []
    for i in range(0, n):
        line = infile.readline()
        line = list(map(int, line.strip().replace('\n', '').replace('\r', '').replace(' ', '\t').split('\t')))
        data += [line]

    infile.close()
    return data


def writer(outfile, strs):
    outfile = open(outfile, 'w')
    for s in strs[:-1]:
        outfile.write(s + '\n')
    outfile.write(strs[-1])
    outfile.close()


def white(i, j):
    if i % 2 == j % 2:
        return True
    else:
        return False


def make_graph(data):
    graph = defaultdict(dummy)
    capacity = defaultdict(dummy2)
    whites = []
    blacks = []
    for i in range(0, len(data)):
        for j in range(0, len(data)):
            if data[i][j] == 1:
                if white(i, j):
                    whites += [(i, j)]
                else:
                    blacks += [(i, j)]

    # To the right
    for i in range(0, len(data)):
        for j in range(0, len(data) - 1):
            if data[i][j + 1] == 1 and data[i][j] == 1:
                if white(i, j):
                    graph[(i, j)] += [(i, j + 1)]
                else:
                    graph[(i, j + 1)] += [(i, j)]

    # Below
    for i in range(0, len(data) - 1):
        for j in range(0, len(data)):
            if data[i + 1][j] == 1 and data[i][j] == 1:
                if white(i, j):
                    graph[(i, j)] += [(i + 1, j)]
                else:
                    graph[(i + 1, j)] += [(i, j)]

    # To the left
    for i in range(0, len(data)):
        for j in range(1, len(data)):
            if data[i][j - 1] == 1 and data[i][j] == 1:
                if white(i, j):
                    graph[(i, j)] += [(i, j - 1)]
                else:
                    graph[(i, j - 1)] += [(i, j)]

    # Above
    for i in range(1, len(data)):
        for j in range(0, len(data)):
            if data[i - 1][j] == 1 and data[i][j] == 1:
                if white(i, j):
                    graph[(i, j)] += [(i - 1, j)]
                else:
                    graph[(i - 1, j)] += [(i, j)]

    graph["s"] = whites

    for i in blacks:
        graph[i] += ["t"]

    for a in graph.keys():
        for b in graph[a]:
            capacity[a, b] = 1

    return [len(whites) + len(blacks), graph, capacity]


def tiler(graph, capacity):
    print("ford")
    flow = fulkerson("s", "t", graph, capacity)
    print("fulkerson")
    locations = []

    for edge in capacity:
        if flow[edge] == 1 and edge[0] != "s" and edge[1] != "t":
            locations += [edge]

    return locations


def runner(infile, outfile):
    data = reader(infile)

    print("data read")

    places, graph, capacity = make_graph(data)

    print("Graph constructed")

    locations = tiler(graph, capacity)

    if 2 * len(locations) == places:
        print("Doable")
        strs = ['1']
        for loc in locations:
            strs += [(str(loc)[1:-1].replace(" ", ''))]
    else:
        print("Not possible.")
        strs = ['0']

    writer(outfile, strs)
    return


(runner("input.txt", "output.txt"))
