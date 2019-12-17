#!/usr/bin/env python3
# Problem description

import os, sys
import re
import numpy as np

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from utils.decorators import *
import networkx as nx

def parse_to_d(x):
    d = {}
    chem_re = re.compile(r'(\d+) (\w+)')
    for line in x:
        left, right = line.split('=>')
        chems_in = left.split(',')
        chem_out = chem_re.match(right.strip())
        key = (chem_out.group(1),chem_out.group(2))
        d[key] = []
        for c in chems_in:
            entry = chem_re.match(c.strip())
            d[key].append((entry.group(1),entry.group(2)))
    return d

def d_to_m(d,x):
    chemicals = set(['ORE'])
    f = {}
    for k in d.keys():
        chemicals.add(k[1])

    chemicals = sorted(list(chemicals))
    chemicals.remove('FUEL')
    lookup = {}
    for c in range(len(chemicals)):
        lookup[chemicals[c]] = c

    x = np.zeros((len(x),len(chemicals)))
    y = np.zeros((len(x)))

    i = 0
    for entry in d.keys():
        if entry[1] == 'FUEL':
            y[i] = int(entry[0])
        else:
            x[i, lookup[entry[1]]] = -int(entry[0])
        for v in d[entry]:
            x[i, lookup[v[1]]] = int(v[0])
        i += 1

    # print(x,y)
    return x,y,lookup

def graph_reversal(x,y,lookup):
    fin = lookup['ORE']
    node = np.where(y == 1)[0][0]
    count = 1
        mats = np.where(x[node] > 1)
        resm = np.where(x[node] < 1)
        for i in range(len(resm)):
            count += 


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
    inp = [
        '10 ORE => 10 A',
        '1 ORE => 1 B',
        '7 A, 1 B => 1 C',
        '7 A, 1 C => 1 D',
        '7 A, 1 D => 1 E',
        '7 A, 1 E => 1 FUEL',
    ]
    d = parse_to_d(inp)
    x,y,l = d_to_m(d,inp)

    print(x,y,l)

    res = np.linalg.solve(x,y)

    print(l,res)

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