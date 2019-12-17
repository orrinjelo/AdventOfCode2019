#!/usr/bin/env python3
# Problem description

import os, sys
import numpy as np
import matplotlib.pyplot as plt

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from utils.decorators import *

def generate_phase(i,l):
    r = [0]*i + [1]*i + [0]*i + [-1]*i
    r = r*(l//4+1)
    return r[1:l+1]

# @timeit('ApplyPhase1')
def apply_phase(x):
    l = []
    for i in range(len(x)):
        l.append(
            np.sum(
                np.multiply(
                    generate_phase(i+1,len(x)),
                    x
                )
            )
        )
    return [abs(x)%10 for x in l]

def apply_phase_2(x,offset):
    '''puzzle input repeated 10000 times'''
    l = []
    x_size = len(x)*10000 
    r_size = x_size - offset
    n = (r_size // len(x)) + 1
    y = x * n 
    y = y[-r_size:]

    for _ in range(100):
        s = 0
        for j in range(len(y)-1, -1, -1):
            s += y[j]
            y[j] = s % 10

    return y


def ltos(x):
    return ''.join(map(str, x))

def stol(x):
    return list(map(int,x))

@timeit('Part 1')
def part_one(x):
    '''Solves part one'''
    y = stol(x)
    for _ in range(100):
        y = apply_phase(y)

    z = ltos(y)

    return z[:8]

def part_one_visualized(x):
    '''Visualization'''
    y = stol(x)
    l = [y[:]]
    for _ in range(100):
        y = apply_phase(y)
        l.append(y[:])

    plt.figure(1)
    plt.imshow(l)
    plt.show()


@timeit('Part 2')
def part_two(x):
    '''Solves part two'''
    offset = int(x[:7])
    y = stol(x)
    y = apply_phase_2(y,offset)

    z = ltos(y)

    return z[:8]

def part_two_visualized(x):
    '''Visualization'''
    pass

def test():
    '''Test functions'''
    assert(generate_phase(2,7) == [0,1,1,0,0,-1,-1])

    inps = '12345678'
    inp = [int(x) for x in inps]
    res = apply_phase(inp)
    res = ltos(res)

    assert(res == '48226158')

    inps = '80871224585914546619083218645595'
    outs = '24176176'
    res = part_one(inps)

    assert(res == outs)

    inps = '03036732577212944063491565474664'
    outs = '84462026'
    res = part_two(inps)

    print(res)

    assert(res == outs)
    print('tests pass')


@timeit('Total')
def main(args):
    with open(args[1], 'r') as f:
        x = [line.strip() for line in f.readlines()]
        # print('Part 1 Result: {}'.format(part_one(x[0])))
        print('Part 2 Result: {}'.format(part_two(x[0])))

        # part_one_visualized(x[0])
        # part_two_visualized(x[0])

if __name__ == '__main__':
    test()
    main(sys.argv)