import sys
import math


# Point class to represent starting and ending positions
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, other):
        return (((self.x - other.x) ** 2) + ((self.y - other.y) ** 2)) ** 0.5


# Load class to represent each load
class Load:
    def __init__(self, id, x1, y1, x2, y2):
        self.id = id
        self.start = Point(x1, y1)
        self.end = Point(x2, y2)
        self.length = self.start.distance(self.end)

    def distance(self, other):
        return self.end.distance(other.start)

    def __str__(self):
        return f'Load {self.id}: {self.start.x},{self.start.y} -> {self.end.x},{self.end.y}'

    def __eq__(self, other):
        return self.id == other.id


def get_path_length(path):
    origin = Point(0, 0)
    length = path[0].start.distance(origin)
    for i, load in enumerate(path):
        if i != 0:
            length += path[i - 1].distance(load)
        length += load.length
    length += path[-1].end.distance(origin)
    return length


# Read input file
path = sys.argv[1]
raw = open(path, 'r').read().replace('\r', '')
lines = raw.split('\n')
lines.pop(0)
loads = []

for i, line in enumerate(lines):
    if line == '':
        continue
    space = 0
    for j, char in enumerate(line):
        if char == ' ':
            space = j
            break
    id = int(line[0:space])
    left, right = line[space + 1:-1].split(') (')
    x_start, y_start = left.replace('(', '').split(',')
    x_end, y_end = right.split(',')
    loads.append(Load(id, float(x_start), float(y_start), float(x_end), float(y_end)))

paths = []
max_length = 720
threshold = 100
while len(loads) > 0:
    path = [loads.pop(0)]

    driving = True
    # Add more loads to a driver's route if they are close enough
    while driving:
        shortest = math.inf
        chosen = None
        for load in loads:
            distance = path[-1].distance(load)
            if distance < shortest:
                shortest = distance
                chosen = load
        if shortest < threshold and get_path_length(path + [chosen]) < max_length:
            path.append(chosen)
            loads.remove(chosen)
        else:
            driving = False

    paths.append(path)
# Print paths
for path in paths:
    s = '['
    for i, load in enumerate(path):
        s += str(load.id)
        if i != len(path) - 1:
            s += ','
    s += ']'
    s.replace('\r','')
    print(s)

