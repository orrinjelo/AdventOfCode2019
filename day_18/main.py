#!/usr/bin/env python3
# Problem description

import os, sys
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx 

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from utils.decorators import *

def convert_to_map(x):
    m = np.zeros((len(x),len(x[0])),dtype=int)
    for l in range(len(x)):
        for i in range(len(x[0])):
            m[l,i] = ord(x[l][i]) 

    # plt.figure(1)
    # plt.imshow(m)
    # plt.show()

    return m

def construct_network()

@timeit('Part 1')
def part_one(x):
    '''Solves part one'''
    m = convert_to_map(x)
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
    inp = [
        '#########',
        '#b.A.@.a#',
        '#########',
    ]

    m = convert_to_map(inp)

    assert(True)

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