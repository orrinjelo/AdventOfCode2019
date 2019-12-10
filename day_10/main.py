#!/usr/bin/env python3
# Problem description

import os, sys
import numpy as np
import matplotlib.pyplot as plt
from fractions import Fraction

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from utils.decorators import *

def parse_map(m):
    h = len(m)
    w = len(m[0])
    mp = np.zeros((w,h),dtype=int)

    for y in range(len(m)):
        for x in range(len(m[0])):
            mp[x,y] = 1 if m[y][x] == '#' else 0

    return mp

def calc_slope(a,b):
    return np.degrees(np.arctan2((b[0]-a[0]),-(b[1]-a[1])))

def generate_digest(x):
    asteroids = np.argwhere(x==1)
    digest = {}
    for a in asteroids:
        for b in asteroids:
            if tuple(a) == tuple(b):
                continue
            slope = calc_slope(a,b)
            if tuple(a) in digest.keys():
                if slope in digest[tuple(a)].keys():
                    digest[tuple(a)][slope].append(tuple(b))
                else:
                    digest[tuple(a)][slope] = [tuple(b)]
            else:
                digest[tuple(a)] = {
                    slope: [tuple(b)]
                }
    return digest

@timeit('Part 1')
def part_one(x):
    '''Solves part one'''
    digest = generate_digest(x)
    # from pprint import pprint 

    best = (0, (0,0))

    for k in digest.keys():
        if len(digest[k]) > best[0]:
            best = (len(digest[k]), k)

    return best

@timeit('Part 2')
def part_two(x, station):
    '''Solves part two'''
    digest = generate_digest(x)
    
    sweep = sorted(digest[station[1]].keys(),key=lambda x: (x-360.0)%360.0)
    # print(sweep)

    n = 0
    c = 0

    def dist(x,y):
        return ((x[0]-y[0])**2 + (x[1]-y[0])**2)**0.5

    beleted = []

    while n < 100:
        a_list = digest[station[1]][sweep[c]] 
        closest = (10000, (0,0))
        for entry in a_list:
            d = dist(entry, station[1])
            if d < closest[0]:
                closest = (d, entry)
        digest[station[1]][sweep[c]].remove(closest[1])
        beleted.append(closest[1])
        c += 1
        if c == len(sweep):
            c = 0
        n += 1
        if n == 100:
            print(beleted, len(beleted))
            return closest[1][0]*100 + closest[1][1]
        # not 1217

def part_two_visualized(x):
    '''Visualization'''
    pass

def test():
    '''Test functions'''
    map_1 = [
    '.#..#',
    '.....',
    '#####',
    '....#',
    '...##',
    ]
    m1 = parse_map(map_1)
    res = part_one(m1)
    assert(res[0] == 8)

    map_2 = [
        '......#.#.',
        '#..#.#....',
        '..#######.',
        '.#.#.###..',
        '.#..#.....',
        '..#....#.#',
        '#..#....#.',
        '.##.#..###',
        '##...#..#.',
        '.#....####',
    ]
    m2 = parse_map(map_2)
    res = part_one(m2)
    assert(res[0] == 33)

@timeit('Total')
def main(args):
    with open(args[1], 'r') as f:
        x = [line.strip() for line in f.readlines()]
        x = parse_map(x)
        station = part_one(x)
        print('Part 1 Result: {}'.format(station))
        print('Part 2 Result: {}'.format(part_two(x, station)))

        part_two_visualized(x)

if __name__ == '__main__':
    test()
    main(sys.argv)