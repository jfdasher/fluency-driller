from collections import namedtuple
import math

Point = namedtuple('Point', ['x', 'y'])

def make_point(x, y):
    return Point(x, y)

def distance_from_origin(p):
    return math.sqrt(p.x ** 2 + p.y ** 2)
