#!/usr/bin/env python3
# Problem description

import os, sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from utils.decorators import *

@timeit('Part 1')
def part_one(x):
    '''Solves part one'''
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