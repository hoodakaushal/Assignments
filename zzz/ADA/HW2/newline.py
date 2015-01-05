__author__ = 'hooda'


class Line:
    m = 0.0
    c = 0.0
    serial = 0

    def __init__(self, m, c, serial):
        self.m = m
        self.c = c
        self.serial = serial

    def gety(self, x):
        return self.m * x + self.c

    def intersect(self, l):
        if l.m == self.m:
            return "No Intersection! Parallel Lines!"
        else:
            x = (l.c - self.c) / (self.m - l.m)
            y = (l.m * self.c - self.m * l.c) / (l.m - self.m)
            return Point(x, y)


class Point:
    x = 0.0
    y = 0.0

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Region:
    start = 0.0
    end = 0.0
    line = None

    def __init(self, start, end, line):
        self.start = start
        self.end = end
        self.line = line

    def isin(self, x):
        if self.start <= x <= self.end:
            return True
        return False


class Struct:
    regions = []

    def __init__(self, regions):
        self.regions = regions

    def confine(self, minx, maxx):
        new_regions = self.regions[:]

        if new_regions[0].end > minx:
            new_regions[0] = Region(minx, new_regions[0].end, new_regions[0].line)
        elif new_regions[0].end == minx:
            new_regions = new_regions[1:]

        if new_regions[-1].start < maxx:
            new_regions[-1] = Region(new_regions[-1].start, maxx, new_regions[-1].line)
        elif new_regions[-1].start == maxx:
            new_regions = new_regions[:-1]
        return Struct(new_regions)

    def getindex(self, x):
        if len(self.regions) == 0:
            print("Could not find %s in Struct" % (x))
            return "Error!"
        else:
            mid = len(self.regions) / 2

            if self.regions[mid].isin(x):
                return mid
            elif x < self.regions[mid].start:
                return Struct(self.regions[0:mid]).getindex(x)
            else:
                return mid + 1 + Struct(self.regions[mid + 1:]).getindex(x)

    def height(self, x):
        return self.regions[self.getindex(x)].line.gety(x)

    def point_higher(self, point):
        return point.y >= self.height(point.x)

    def region_higher(self, region):
        start = Point(region.start, region.line.gety(region.start))
        end = Point(region.end, region.line.gety(region.end))

        higher_start = self.point_higher(start)
        higher_end = self.point_higher(end)

        if higher_start and higher_end:
            return 1
        elif not (higher_start or higher_end):
            return -1
        else:
            return 0

    def flip_search(self, other):
        if len(self.regions) == 0:
            print("There are no regions here!")
            return "Nope. Nope. Nope."

        mid = len(self.regions) / 2




