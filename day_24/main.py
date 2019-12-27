#!/usr/bin/env python3
# Problem description

import os, sys
import numpy as np

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from utils.decorators import *

def get_col(x):
    l2 = np.log2(x)
    return l2 % 5

def get_row(x):
    l2 = np.log2(x)
    return l2 // 5

def get_grid(g, x, y):
    n = 2**(5*y + x)
    return 1 if g & n else 0

def set_grid(g, x, y, v=1):
    n = 2**(5*y + x)
    if v == 1:
        g = g | n 
    else:
        g = g & (~n)
    return g

def parse_grid(x):
    i = 1
    g = 0
    for line in x:
        for c in line:
            if c == '#':
                g += i
            i *= 2

    return g

def num_neighbors(g,x,y):
    count = 0
    if x > 0:
        count += get_grid(g,x-1,y)
    if y > 0:
        count += get_grid(g,x,y-1)
    if x < 4:
        count += get_grid(g,x+1,y)
    if y < 4:
        count += get_grid(g,x,y+1)

    return count

def step(g):
    gg = g
    for x in range(5):
        for y in range(5):
            nn = num_neighbors(g,x,y)
            if get_grid(g,x,y):
                if nn != 1:
                    # print('flip 0 at',x,y)
                    gg = set_grid(gg,x,y,0)
            else:
                if nn == 1 or nn == 2:
                    # print('flip 1 at',x,y)
                    gg = set_grid(gg,x,y,1)
    return gg

@timeit('Part 1')
def part_one(x):
    '''Solves part one'''
    g = parse_grid(x)
    states = set()
    for i in range(1000):
        if g in states:
            return g
        else:
            states.add(g)
        g = step(g)

@timeit('Part 2')
def part_two(x):
    '''Solves part two'''
    return None

def part_two_visualized(x):
    '''Visualization'''
    pass

def test():
    '''Test functions'''
    assert(get_col(1) == 0)
    assert(get_col(2) == 1)
    assert(get_col(4) == 2)
    assert(get_col(8) == 3)
    assert(get_col(16) == 4)
    assert(get_col(32) == 0)
    assert(get_col(128) == 2)

    assert(get_row(1) == 0)
    assert(get_row(2) == 0)
    assert(get_row(4) == 0)
    assert(get_row(16) == 0)
    assert(get_row(32) == 1)
    assert(get_row(128) == 1)
    assert(get_row(32768) == 3)

    assert(get_grid(32768, 0, 3) == 1)

    assert(set_grid(0, 3, 0, 1) == 8)
    assert(set_grid(1, 0, 3, 1) == 32769)
    assert(set_grid(32769, 0, 0, 0) == 32768)

    lines = [
        '.....',
        '.....',
        '.....',
        '#....',
        '.#...',
    ]
    g = parse_grid(lines)
    assert(g == 2129920)

    n = num_neighbors(g,0,4)
    assert(n == 2)

    g = step(g)
    assert(get_grid(g,0,4) == 1)

    lines = [
        '....#',
        '#..#.',
        '#..##',
        '..#..',
        '#....',
    ]
    next_step = [
        '#..#.',
        '####.',
        '###.#',
        '##.##',
        '.##..',
    ]

    g = parse_grid(lines)
    k = parse_grid(next_step)
    g = step(g)
    assert(g == k)

    res = part_one(lines)
    assert(res == 2129920)


@timeit('Total')
def main(args):
    with open(args[1], 'r') as f:
        x = [line.strip() for line in f.readlines()]
        print('Part 1 Result: {}'.format(part_one(x)))
        print('Part 2 Result: {}'.format(part_two(x)))

        part_two_visualized(x)

if __name__ == '__main__':
    test()
    main(sys.argv)