#!/usr/bin/env python3
# Problem description

import os, sys
import re
import numpy as np
import matplotlib.pyplot as plt

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from utils.decorators import *
import networkx as nx

class Element():
    def __init__(self, name, batch=1):
        self.name = name
        self.connections = {}
        self.available = 0
        self.depends = []
        self.batch = batch
        self.total_manufactured = 0

    def add_dependency(self, node, cost):
        self.connections[node.name] = {
            'node': node,
            'cost': cost,
        }
        self.depends.append(node.name)

    def manufacture(self, n):
        # print('[{}] manufacturing at least {}'.format(self.name, n))
        amt = 0
        while amt < n:
            for chem in self.depends:
                d = self.connections[chem]
                d['node'].consume(d['cost'])
            amt += self.batch
        # print('[{}] manufactured {}'.format(self.name, amt))
        self.available += amt
        self.total_manufactured += amt

    def consume(self, n):
        # print('[{}] {} requested, {} available'.format(self.name, n,self.available))
        if n > self.available:
            diff = n - self.available
            self.manufacture(diff)

        self.available -= n


def parse_to_d(x):
    d = {}
    chem_re = re.compile(r'(\d+) (\w+)')
    for line in x:
        left, right = line.split('=>')
        chems_in = left.split(',')
        chem_out = chem_re.match(right.strip())
        amt,key = int(chem_out.group(1)),chem_out.group(2)
        if key in d.keys():
            d[key].batch = amt
        else:
            d[key] = Element(key, amt)
        for c in chems_in:
            entry = chem_re.match(c.strip())
            camt,ckey = int(entry.group(1)),entry.group(2)
            if ckey in d.keys():
                pass
            else:
                d[ckey] = Element(ckey)
            d[key].add_dependency(d[ckey], camt)

    return d


@timeit('Part 1')
def part_one(x):
    '''Solves part one'''
    d = parse_to_d(x)
    d['FUEL'].manufacture(1)
    return d['ORE'].total_manufactured

@timeit('Part 2')
def part_two(x):
    '''Solves part two'''
    d = parse_to_d(x)
    d['ORE'].available = 1000000000000
    def exhausted(*args, **kwargs):
        print('I got no more!')
    d['ORE'].manufacture = exhausted
    # def consume(obj, n):
    #     if n > obj.available:
    #         print('Cannot consume anymore!')
    #     else:
    #         obj.available -= n
    # d['ORE'].consume = consume

    x = np.arange(0,100)
    data = []
    for i in range(100):
        d['FUEL'].manufacture(100)
        data.append(d['ORE'].available)

    from scipy.optimize import curve_fit

    def f(x, a, b):
        return a - b*x

    fitting_params, cov = curve_fit(
        f, x, data, 
        [1000000000000,220019]
    )

    a,b = fitting_params

    print(a,b)

    # plt.figure(1)
    # plt.plot(data)
    # plt.plot(a - b*x)
    plt.figure(2)
    plt.plot(data - (a - b*x))
    plt.show()


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
    d['FUEL'].manufacture(1)
    assert(d['ORE'].total_manufactured == 31)

    inp = [
        '9 ORE => 2 A',
        '8 ORE => 3 B',
        '7 ORE => 5 C',
        '3 A, 4 B => 1 AB',
        '5 B, 7 C => 1 BC',
        '4 C, 1 A => 1 CA',
        '2 AB, 3 BC, 4 CA => 1 FUEL',
    ]
    d = parse_to_d(inp)
    d['FUEL'].manufacture(1)
    assert(d['ORE'].total_manufactured == 165)


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