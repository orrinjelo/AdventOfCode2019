#!/usr/bin/env python3
# Problem description

import os, sys
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from utils.decorators import *
from vm.vm import ElfMachine

class RepairDroid():
    def __init__(self, grid=(100,100), pos=None):
        self.grid = np.full(grid, -1)
        if pos:
            self.pos = pos
        else:
            self.pos = grid[0]//2,grid[1]//2

        self.dist = 0

        self.start = self.pos
        self.dir_db = {
            1: [0,1], # North
            2: [0,-1],# South
            3: [-1,0],# West
            4: [1,0]  # East
        }
        self.dir = 1

        self.two_pass = 0

        self.G = nx.Graph()

        self.vm = ElfMachine(input_cb=self.move, output_cb=self.paint, mem_size=4096)

        # 0: The repair droid hit a wall. Its position has not changed.
        # 1: The repair droid has moved one step in the requested direction.
        # 2: The repair droid has moved one step in the requested direction; its new position is the location of the oxygen system.
        self.status = {}    

    def move(self, *args, **kwargs):
        loc = self.grid[self.pos[0]+self.dir_db[self.dir][0],self.pos[1]+self.dir_db[self.dir][1]]
        if loc == 0:
            if self.dir == 1:
                self.dir = 3
            elif self.dir == 3:
                self.dir = 2
            elif self.dir == 2:
                self.dir = 4
            elif self.dir == 4:
                self.dir = 1

            # plt.figure()
            # grid = self.grid.copy()
            # grid[self.pos] = 5
            # plt.imshow(grid)
            # plt.show()

        elif loc == 1:
            oldpos = self.pos
            self.pos = self.pos[0]+self.dir_db[self.dir][0],self.pos[1]+self.dir_db[self.dir][1]
            self.G.add_edge(oldpos, self.pos)
            # print('Added',[oldpos, self.pos])
            if self.dir == 1:
                self.dir = 4
            elif self.dir == 3:
                self.dir = 1
            elif self.dir == 2:
                self.dir = 3
            elif self.dir == 4:
                self.dir = 2




        elif loc == 2:
            oldpos = self.pos
            self.pos = self.pos[0]+self.dir_db[self.dir][0],self.pos[1]+self.dir_db[self.dir][1]
            self.G.add_edge(oldpos, self.pos)
            # print('Added',[oldpos, self.pos])

            print('Found at',self.pos)

            # plt.figure()
            # grid = self.grid.copy()
            # grid[self.pos] = 5
            # plt.imshow(grid)
            # plt.show()

            self.dist = len(nx.shortest_path(self.G, source=self.start, target=self.pos)) - 1
            print('Current dist: {}'.format(self.dist))
            
            self.two_pass += 1

            if self.two_pass == 2:
                self.vm.finished = True

                # try:
                # except nx.NetworkXNoPath:
                #     nx.draw(self.G)
                #     plt.show()
            
        return self.dir

        
    def paint(self, x):
        self.grid[self.pos[0]+self.dir_db[self.dir][0],self.pos[1]+self.dir_db[self.dir][1]] = x

    def run(self,x):
        self.vm.run_program(x)
        return self.dist, self.G, self.pos


@timeit('Part 1')
def part_one(x):
    '''Solves part one'''
    droid = RepairDroid()
    return droid.run(x)

@timeit('Part 2')
def part_two(G,loc):
    '''Solves part two'''
    longest = 0
    for n in G.nodes:
        longest = max(longest, len(nx.shortest_path(G,loc,n))-1)
    return longest

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
        res,g,loc = part_one(x)
        print('Part 1 Result: {}'.format(res))
        print('Part 2 Result: {}'.format(part_two(g,loc)))

        part_two_visualized(x)

if __name__ == '__main__':
    test()
    main(sys.argv)