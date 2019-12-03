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
    # print(d,x)
    if d == 'U':
        grid[pos[0],pos[1]-x:pos[1]] = 1
        newpos = pos[0],pos[1]-x
    elif d == 'D':
        grid[pos[0],pos[1]+1:pos[1]+x+1] = 1
        newpos = pos[0],pos[1]+x
    elif d == 'L':
        grid[pos[0]-x:pos[0],pos[1]] = 1
        newpos = pos[0]-x,pos[1]
    elif d == 'R':
        grid[pos[0]+1:pos[0]+x+1,pos[1]] = 1
        newpos = pos[0]+x,pos[1]

    return grid, newpos

def trace_grid_more(grid, pos, instruction, last):
    d,x = parse(instruction)
    # print(d,x)
    if d == 'U':
        grid[pos[0],pos[1]-x:pos[1]] = range(last+x,last,-1)
        newpos = pos[0],pos[1]-x
        last += x
    elif d == 'D':
        grid[pos[0],pos[1]+1:pos[1]+x+1] = range(last+1,last+x+1)
        newpos = pos[0],pos[1]+x
        last += x
    elif d == 'L':
        grid[pos[0]-x:pos[0],pos[1]] = range(last+x,last,-1)
        newpos = pos[0]-x,pos[1]
        last += x
    elif d == 'R':
        grid[pos[0]+1:pos[0]+x+1,pos[1]] = range(last+1,last+x+1)
        newpos = pos[0]+x,pos[1]
        last += x
    return grid, newpos, last

def dist(pt1, pt2):
    return np.abs(pt1[0]-pt2[0])+np.abs(pt1[1]-pt2[1])

@timeit('Part 1')
def part_one(x,SIZE=20001):
    '''Solves part one'''
    grid = np.zeros((SIZE,SIZE),dtype=np.uint16)
    
    for wire in x:
        newgrid = np.zeros((SIZE,SIZE),dtype=np.uint16)
        pos = (SIZE//2,SIZE//2)
        for entry in wire:
            newgrid,pos = trace_grid(newgrid, pos, entry)
        grid = grid + newgrid


    intersects = np.argwhere(grid > 1)

    dists = []

    for i in intersects:
        dists.append(dist(i, (SIZE//2,SIZE//2)))

    idx = np.argwhere(dists == min(dists))[0][0]

    return min(dists)

    # return None    

@timeit('Part 2')
def part_two(x,SIZE=20001):
    '''Solves part two'''

    grid = np.zeros((SIZE,SIZE),dtype=np.uint16)
    
    for wire in x:
        newgrid = np.zeros((SIZE,SIZE),dtype=np.uint16)
        pos = (SIZE//2,SIZE//2)
        for entry in wire:
            newgrid,pos = trace_grid(newgrid, pos, entry)
        grid = grid + newgrid


    intersects = np.argwhere(grid > 1)

    grid = np.zeros((SIZE,SIZE),dtype=np.uint32)
    
    for wire in x:
        last = 0
        newgrid = np.zeros((SIZE,SIZE),dtype=np.uint32)
        pos = (SIZE//2,SIZE//2)
        for entry in wire:
            newgrid,pos,last = trace_grid_more(newgrid, pos, entry, last)
        grid = grid + newgrid
        # grid[SIZE//2,SIZE//2] = 1

    dists = []

    for i in intersects:
        dists.append(grid[i[0],i[1]])

    idx = np.argwhere(dists == min(dists))[0][0]

    # pgrid = grid
    # pgrid[SIZE//2,SIZE//2] = 3
    # pgrid[intersects[idx][0],intersects[idx][1]] = 4
    # # pgrid = grey_dilation(pgrid, size=(SIZE//500, SIZE//500))
    # plt.figure()
    # plt.imshow(np.transpose(pgrid),cmap='gist_rainbow',aspect='auto')
    # plt.show()

    return min(dists)



def part_one_visualized(x,SIZE=20001):
    '''Visualization'''
    from scipy.ndimage.morphology import grey_dilation
    grid = np.zeros((SIZE,SIZE),dtype=np.uint8)
    
    for wire in x:
        newgrid = np.zeros((SIZE,SIZE),dtype=np.uint8)
        pos = (SIZE//2,SIZE//2)
        for entry in wire:
            newgrid,pos = trace_grid(newgrid, pos, entry)
        grid = grid + newgrid


    intersects = np.argwhere(grid > 1)

    dists = []

    for i in intersects:
        dists.append(dist(i, (SIZE//2,SIZE//2)))

    idx = np.argwhere(dists == min(dists))[0][0]

    pgrid = grid
    pgrid[SIZE//2,SIZE//2] = 3
    pgrid[intersects[idx][0],intersects[idx][1]] = 4
    pgrid = grey_dilation(pgrid, size=(SIZE//500, SIZE//500))
    plt.figure()
    plt.imshow(np.transpose(pgrid),cmap='gist_rainbow',aspect='auto')
    plt.show()
    return min(dists)

def part_two_visualized(x,SIZE=20001):
    '''Solves part two'''
    from scipy.ndimage.morphology import grey_dilation
    grid = np.zeros((SIZE,SIZE),dtype=np.uint16)
    
    for wire in x:
        newgrid = np.zeros((SIZE,SIZE),dtype=np.uint16)
        pos = (SIZE//2,SIZE//2)
        for entry in wire:
            newgrid,pos = trace_grid(newgrid, pos, entry)
        grid = grid + newgrid


    intersects = np.argwhere(grid > 1)

    grid = np.zeros((SIZE,SIZE),dtype=np.uint32)
    
    for wire in x:
        last = 10000
        newgrid = np.zeros((SIZE,SIZE),dtype=np.uint32)
        pos = (SIZE//2,SIZE//2)
        for entry in wire:
            newgrid,pos,last = trace_grid_more(newgrid, pos, entry, last)
        grid = np.max(grid,newgrid)
        # grid[SIZE//2,SIZE//2] = 1

    dists = []

    for i in intersects:
        dists.append(grid[i[0],i[1]])

    idx = np.argwhere(dists == min(dists))[0][0]

    pgrid = grid
    pgrid[SIZE//2,SIZE//2] = 3
    pgrid[intersects[idx][0],intersects[idx][1]] = 4
    pgrid = grey_dilation(pgrid, size=(SIZE//500, SIZE//500))
    plt.figure()
    plt.imshow(np.transpose(pgrid),cmap='plasma',aspect='auto')
    plt.show()

    return min(dists)

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

    grid1,pos = trace_grid(np.zeros((9,9)), (0,4), 'R8')
    grid2,pos = trace_grid(np.zeros((9,9)), (4,0), 'D8')
    grid = grid1+grid2

    assert(np.all(grid == check))
    assert(pos == (4,8))

    grid = np.zeros((9,9))
    check = np.zeros((9,9))
    check[4,:8] = 1
    check[:8,4] = 1
    check[4,4] = 2

    grid1,pos = trace_grid(np.zeros((9,9)), (8,4), 'L8')
    grid2,pos = trace_grid(np.zeros((9,9)), (4,8), 'U8')
    grid = grid1+grid2

    assert(np.all(grid == check))
    assert(pos == (4,0))

    test_input_0 = [
        'R8,U5,L5,D3'.split(','),
        'U7,R6,D4,L4'.split(',')
    ]
    test_solution_0 = 6
    ans = part_one(test_input_0,21)
    assert(ans == test_solution_0)

    test_input_1 = [
        'R75,D30,R83,U83,L12,D49,R71,U7,L72'.split(','),
        'U62,R66,U55,R34,D71,R55,D58,R83'.split(',')
    ]
    test_solution_1 = 159
    ans = part_one(test_input_1,501)
    assert(ans == test_solution_1)

    test_input_2 = [
        'R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51'.split(','),
        'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7'.split(','),
    ]
    test_solution_2 = 135
    ans = part_one(test_input_2,501)
    assert(ans == test_solution_2)

    test_solution_3 = 30
    ans = part_two(test_input_0,21)
    assert(ans == test_solution_3)

    test_solution_4 = 610
    ans = part_two(test_input_1,501)
    assert(ans == test_solution_4)

    test_solution_5 = 410
    ans = part_two(test_input_2,501)
    assert(ans == test_solution_5)


@timeit('Total')
def main(args):
    with open(args[1], 'r') as f:
        x = [line.strip().split(',') for line in f.readlines()]
        print('Part 1 Result: {}'.format(part_one(x)))
        print('Part 2 Result: {}'.format(part_two(x)))

        # part_one_visualized(x)
        part_two_visualized(x)

if __name__ == '__main__':
    test()
    main(sys.argv)