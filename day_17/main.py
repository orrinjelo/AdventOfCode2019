#!/usr/bin/env python3
# Problem description

import os, sys
import numpy as np
import matplotlib.pyplot as plt

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from utils.decorators import *
from vm.vm import ElfMachine

def isjunction(x,coord):
    try:
        if x[coord[0],coord[1]] == 35 and \
           x[coord[0]+1,coord[1]] == 35 and \
           x[coord[0],coord[1]+1] == 35 and \
           x[coord[0]-1,coord[1]] == 35 and \
           x[coord[0],coord[1]-1] == 35:
            return True
    except:
        pass
    return False

def find_junctions(x):
    junctions = []
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            if isjunction(x,(i,j)):
                junctions.append((i,j))
    return junctions    

@timeit('Part 1')
def part_one(x):
    '''Solves part one'''
    global a,b
    a = []
    b = []
    def draw(x):
        global a,b
        if x == 10:
            a.append(b[:])
            b = []
        else:
            b.append(x)

    vm = ElfMachine(output_cb=draw, mem_size=4096)
    vm.run_program(x)

    m = np.array(a[:-1])
    # print(a)
    j = find_junctions(m)

    # plt.figure(1)
    # plt.imshow(m)
    # plt.show()

    ks = 0
    for i in j:
        ks += i[0]*i[1]

    return ks

@timeit('Part 2')
def part_two(x):
    '''Solves part two'''
    global a,b,c,d,dust
    a = []
    b = []
    dust = 0
    def draw(x):
        global a,b,dust
        print(chr(x),end='')
        if x == 10:
            a.append(b[:])
            b = []
        elif x > 255:
            dust = x
        else:
            b.append(x)

    c = 0
    d = 0
    def traverse(*args, **kwargs):
        global c,d
        p = 'A,B,A,B,C,A,B,C,A,C\n'
        A = 'R,6,L,6,L,10\n'
        B = 'L,8,L,6,L,10,L,6\n'
        C = 'R,6,L,8,L,10,R,6\n'
        disp = 'n\n'
        if c == 0:
            print(d,len(p))
            ret = p[d]
            d += 1
            if d == len(p):
                c = 1
                d = 0
            return ord(ret)
        elif c == 1:
            ret = A[d]
            d += 1
            if d == len(A):
                c = 2
                d = 0
            return ord(ret)
        elif c == 2:
            ret = B[d]
            d += 1
            if d == len(B):
                c = 3
                d = 0
            return ord(ret)
        elif c == 3:
            ret = C[d]
            d += 1
            if d == len(C):
                c = 4
                d = 0
            return ord(ret)
        elif c == 4:
            ret = disp[d]
            d += 1
            if d == len(disp):
                c = 5
                d = 0
            return ord(ret) 
        return ord(input('> '))
        

    vm = ElfMachine(output_cb=draw, input_cb=traverse, mem_size=4096)
    x[0] = 2
    vm.run_program(x)

    # print(c,d)

    # m = np.array(a[:-1])
    # j = find_junctions(m)

    return dust

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