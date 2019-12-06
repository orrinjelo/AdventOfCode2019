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
    node_set = set()
    for orbit in x:
        G.add_edge(orbit[0],orbit[1])
        node_set.add(orbit[0])
        node_set.add(orbit[1])


    paths = {}

    def get_successors(x):
        return [node for node in nx.dfs_preorder_nodes(G, x)]

    count = 0
    for node in G.nodes():
        count += len(get_successors(node))-1
    
    # This works, but it takes too long
    # count = 0
    # for node_a in node_set:
    #     if len(G.out_edges(node_a)) == 0:
    #         continue
    #     for node_b in node_set:
    #         if node_a != node_b:
    #             count += len(list(nx.all_simple_paths(G, node_a, node_b)))

    return count

    # plt.figure()
    # nx.draw(G, with_labels=True, font_weight='bold')
    # plt.show()


@timeit('Part 2')
def part_two(x):
    '''Solves part two'''
    G = nx.Graph()
    node_set = set()
    for orbit in x:
        G.add_edge(orbit[0],orbit[1])
        node_set.add(orbit[0])
        node_set.add(orbit[1])

    return nx.shortest_path_length(G,'YOU','SAN')-2

def part_one_visualized(x):
    G = nx.DiGraph()
    node_set = set()
    for orbit in x:
        G.add_edge(orbit[0],orbit[1])
        node_set.add(orbit[0])
        node_set.add(orbit[1])

    # plt.figure(1)
    # nx.draw_spectral(G, with_labels=True, font_weight='normal', 
    #     font_size=2, node_size=20, cmap='viridis')
    plt.figure(2)
    nx.draw(G, with_labels=True, font_weight='normal', 
        font_size=2, node_size=20, cmap='viridis')    
    # plt.figure(3)
    # nx.draw_kamada_kawai(G, with_labels=True, font_weight='normal', 
    #     font_size=2, node_size=20, cmap='viridis')
    plt.show()    

def part_two_visualized(x):
    '''Visualization'''
    pass

def test_visualized(x):
    import numpy as np
    import matplotlib.animation as animation

    plt.rcParams['animation.ffmpeg_path'] = '/usr/bin/ffmpeg'
    plt.switch_backend('QT5Agg')

    G = nx.DiGraph()
    for orbit in x:
        G.add_edge(orbit[0],orbit[1]) 

    class Orbit():
        def __init__(self, *args, **kwargs):
            self.baloney = 1.0
            self.dt = 0.01
            if np.random.randint(7) == 3:
                self.dt = -self.dt
            self.orbiting = kwargs.get('orbiting', None)
            self.center = kwargs.get('center', None)
            if self.center == None:
                self.center = (self.orbiting.x,self.orbiting.y)
            if self.orbiting:
                self.radius = np.random.randint(self.orbiting.radius) + 10
            else:
                self.radius = 60
            self.angle = np.random.rand() * 2 * np.pi
            self.period = 2*np.pi*self.baloney*self.radius**1.5
            self.calc_pos()

        def step(self, i=None):
            self.angle += self.period * 2 * np.pi * self.dt
            if self.angle > 2*np.pi:
                self.angle -= 2*np.pi
            elif self.angle < 0.0:
                self.angle += 2*np.pi
            self.calc_pos()

        def calc_pos(self):
            if self.orbiting:
                self.center = self.orbiting.x, self.orbiting.y
            self.x = self.center[0] + self.radius * np.cos(self.angle)
            self.y = self.center[1] + self.radius * np.sin(self.angle)
            try:
                self.body.set_data(self.x, self.y)
                self.path.set_data(self.center, self.radius)
            except:
                pass

        def plot(self, ax):
            if not self.orbiting:
                ax.add_artist(
                    plt.Circle(self.center, self.radius/10+1, color='b', fill=True, linestyle='-')
                )
            self.path = plt.Circle(self.center, self.radius, color='k', linestyle='--', fill=False, alpha=0.15)
            self.orbit_path = ax.add_artist(self.path)
            self.body = ax.plot(self.x, self.y, 'o', color=np.random.rand(3,))

    fig, ax = plt.subplots()
    a = Orbit(center=(0,0))
    prev = a
    orbits = [a]
    for _ in range(10):
        b = Orbit(orbiting=prev)
        prev = b
        orbits.append(b)
    for o in orbits:
        o.plot(ax)
    plt.xlim(-100,100)
    plt.ylim(-100,100)
    plt.axis('off')

    def update(i):
        # plt.clf()
        for o in orbits:
            o.step()
            # o.plot(ax)

    ani = animation.FuncAnimation(fig, update, interval=50, blit=False, repeat_delay=500)
    ani.save('output.gif', writer='imagemagick')

    plt.show()


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
    res = part_one(orbits)
    assert(res == 42)

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
    ('K','YOU'),
    ('I','SAN'),
    ]
    res = part_two(orbits)

    assert(res == 4)

    test_visualized(orbits)

@timeit('Total')
def main(args):
    with open(args[1], 'r') as f:
        x = [tuple(line.strip().split(')')) for line in f.readlines()]
        print('Part 1 Result: {}'.format(part_one(x)))
        print('Part 2 Result: {}'.format(part_two(x)))

        # part_one_visualized(x)
        # part_two_visualized(x)

if __name__ == '__main__':
    test()
    main(sys.argv)