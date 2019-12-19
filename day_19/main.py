#!/usr/bin/env python3
# Problem description

import os, sys
import numpy as np
import matplotlib.pyplot as plt

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from utils.decorators import *
from vm.vm import ElfMachine

@timeit('Part 1')
def part_one(p):
    global x,y,grid,vm,flip
    '''Solves part one'''
    x,y = -1,0
    flip = True

    grid = np.zeros((50,50),dtype=int)

    def draw(i):
        global x,y,grid
        grid[x][y] = i

    def query(*args, **kwargs):
        global x,y, vm, flip
        if flip:
            flip = False
            x += 1
            if x == 50:
                y += 1
                x = 0
                if y == 50:
                    vm.finished = True
            return x
        else:
            flip = True
            return y

    vm = ElfMachine(output_cb=draw, input_cb=query, mem_size=4096)

    for _ in range(50*50):
        vm.run_program(p)

    plt.figure(1)
    plt.imshow(grid)
    plt.show()

    count = len(np.where(grid.flatten() == 1)[0])

    return count

@timeit('Part 2')
def part_two(x):
    '''Solves part two'''
    return None

def part_two_visualized(x):
    '''Visualization'''
    pass

def test():
    '''Test functions'''
    assert(True)

@timeit('Total')
def main(args):
    with open(args[1], 'r') as f:
        x = [line.strip() for line in f.readlines()]
        x = x[0].split(',')
        x = list(map(int, x))
        print('Part 1 Result: {}'.format(part_one(x)))
        print('Part 2 Result: {}'.format(part_two(x)))

        part_two_visualized(x)

if __name__ == '__main__':
    test()
    main(sys.argv)