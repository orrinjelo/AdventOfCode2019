#!/usr/bin/env python3
# Problem description

import os, sys
import numpy as np
import matplotlib.pyplot as plt

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from utils.decorators import *

def parse(x):
    return x[0],int(x[1:])

def trace_grid(grid, pos, instruction):
    d,x = parse(instruction)

    if d == 'U':
        grid[pos[0],pos[1]-x:pos[1]] += 1
        newpos = pos[0],pos[1]-x
    elif d == 'D':
        grid[pos[0],pos[1]+1:pos[1]+x+1] += 1
        newpos = pos[0],pos[1]+x
    elif d == 'L':
        grid[pos[0]-x:pos[0],pos[1]] += 1
        newpos = pos[0]-x,pos[1]
    elif d == 'R':
        grid[pos[0]+1:pos[0]+x+1,pos[1]] += 1
        newpos = pos[0]+x,pos[1]

    return grid, newpos


@timeit('Part 1')
def part_one(x):
    '''Solves part one'''
    SIZE = 20001
    grid = np.zeros((SIZE,SIZE),dtype=np.uint8)
    for wire in x:
        pos = (SIZE//2,SIZE//2)
        for entry in wire:
            grid,pos = trace_grid(grid, pos, entry)

    plt.figure()
    plt.imshow(grid)
    plt.show()
    return None    

@timeit('Part 2')
def part_two(x):
    '''Solves part two'''
    return None

def part_two_visualized(x):
    '''Visualization'''
    pass

def test():
    '''Test functions'''

    assert(parse('L234') == ('L',234))
    assert(parse('D493') == ('D',493))
    assert(parse('R55') == ('R',55))
    assert(parse('U3') == ('U',3))

    grid = np.zeros((9,9))
    check = np.zeros((9,9))
    check[4,1:] = 1
    check[1:,4] = 1
    check[4,4] = 2

    grid,pos = trace_grid(grid, (0,4), 'R8')
    grid,pos = trace_grid(grid, (4,0), 'D8')

    assert(np.all(grid == check))
    assert(pos == (4,8))

    grid = np.zeros((9,9))
    check = np.zeros((9,9))
    check[4,:8] = 1
    check[:8,4] = 1
    check[4,4] = 2

    grid,pos = trace_grid(grid, (8,4), 'L8')
    grid,pos = trace_grid(grid, (4,8), 'U8')

    assert(np.all(grid == check))
    assert(pos == (4,0))

@timeit('Total')
def main(args):
    with open(args[1], 'r') as f:
        x = [line.strip().split(',') for line in f.readlines()]
        print('Part 1 Result: {}'.format(part_one(x)))
        print('Part 2 Result: {}'.format(part_two(x)))

        part_two_visualized(x)

if __name__ == '__main__':
    test()
    main(sys.argv)