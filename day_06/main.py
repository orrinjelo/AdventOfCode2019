#!/usr/bin/env python3
# Problem description

import os, sys
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.flow import shortest_augmenting_path

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from utils.decorators import *

def parse_line(x):
    a,b = x.split()

@timeit('Part 1')
def part_one(x):
    '''Solves part one'''
    G = nx.DiGraph()
    for orbit in x:
        G.add_edge(orbit[0],orbit[1])

    print(list(G.out_degree()))

    # plt.figure()
    # nx.draw(G, with_labels=True, font_weight='bold')
    # plt.show()


@timeit('Part 2')
def part_two(x):
    '''Solves part two'''
    return None

def part_two_visualized(x):
    '''Visualization'''
    pass

def test():
    '''Test functions'''
    orbits = [
    ('COM','B'),
    ('B','C'),
    ('C','D'),
    ('D','E'),
    ('E','F'),
    ('B','G'),
    ('G','H'),
    ('D','I'),
    ('E','J'),
    ('J','K'),
    ('K','L'),
    ]
    part_one(orbits)

@timeit('Total')
def main(args):
    with open(args[1], 'r') as f:
        x = [tuple(line.strip().split(')')) for line in f.readlines()]
        print('Part 1 Result: {}'.format(part_one(x)))
        print('Part 2 Result: {}'.format(part_two(x)))

        part_two_visualized(x)

if __name__ == '__main__':
    test()
    # main(sys.argv)