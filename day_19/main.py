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
def part_two(p):
    '''Solves part two'''
    global x,y,grid,vm,query_g,xx,yy,fin
    fin = False
    grid = {}

    def draw(i):
        global x,y,grid,xx,yy
        grid[(xx,yy)] = i

    # def query_generator(*args, **kwargs):
    #     global x,y,grid,vm,xx,yy
    #     x,y = 0,0
    #     xx,yy = 0,0
    #     while True:
    #         yield x
    #         yield y

    #         if grid[(x,y)] == 0:
    #             y += 1
    #             yy = y
    #             continue
    #         elif grid[(x,y)] == 1:
    #             yield x
    #             yy = y + 99
    #             yield y + 99
    #             if x % 10 == 0:
    #                 print('At x =',x)
    #             if grid[(x,y+99)] == 0:
    #                 x += 1
    #                 xx = x
    #                 y = 0
    #                 yy = y
    #                 continue
    #             elif grid[(x,y+99)] == 1:
    #                 print('Almost at',x,y)
    #                 xx = x+99
    #                 yy = y
    #                 yield xx
    #                 yield yy
    #                 if grid[(xx,yy)] == 1:
    #                     print('Found at',x,y)
    #                     vm.finished = True
    #                     fin = True
    #                 else:
    #                     x += 1
    #                     xx = x 
    #                     y = 0
    #                     yy = y

    def query_generator(*args, **kwargs):
        global x,y,grid,vm,xx,yy,fin
        x,y = 0,10
        xx,yy = 0,10
        last_x = 0
        S = 99
        while True:
            yield x
            yield y

            if grid[(x,y)] == 0:
                x += 1
                xx = x
                continue
            elif grid[(x,y)] == 1:
                xx = x + S
                last_x = x
                yield xx
                yield y
                # if y % 10 == 0:
                    # print('At y =',y)
                if grid[(x+S,y)] == 0:
                    y += 1
                    yy = y
                    x = last_x
                    xx = x
                    continue
                elif grid[(x+S,y)] == 1:
                    # print('Almost at',x,y)
                    xx = x
                    yy = y+S
                    yield x
                    yield y+S
                    if grid[(x,y+S)] == 1:
                        print('Found at',x,y)
                        vm.finished = True
                        fin = True
                    else:
                        y += 1
                        yy = y 
                        x = last_x
                        xx = x

    query_g = query_generator() 

    def query(*args, **kwargs):
        global query_g
        return next(query_g)

    vm = ElfMachine(output_cb=draw, input_cb=query, mem_size=8196)

    while not fin:
        vm.run_program(p)

    # plt.figure(1)
    # plt.imshow(grid)
    # plt.show()

    return x*10000+y

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