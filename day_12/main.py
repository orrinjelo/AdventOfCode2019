#!/usr/bin/env python3
# Problem description

import os, sys
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import re

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from utils.decorators import *

class Body():
    def __init__(self, position, velocity=[0,0,0]):
        self.position = position[:]
        self.velocity = velocity[:]

    def calc_velocity(self, bodies):
        for body in bodies:
            if body == self:
                continue
            for axis in range(3):
                if body.position[axis] < self.position[axis]:
                    self.velocity[axis] -= 1
                elif body.position[axis] > self.position[axis]:
                    self.velocity[axis] += 1

    def calc_position(self):
        for axis in range(3):
            self.position[axis] += self.velocity[axis]

    def calc_potential(self):
        return sum(map(np.abs, self.position))

    def calc_kinetic(self):
        return sum(map(np.abs, self.velocity))

    def calc_total_energy(self):
        return self.calc_kinetic() * self.calc_potential()

    def __str__(self):
        return 'pos=<x={:>4}, y={:>4}, z={:>4}>, vel=<x={:>4}, y={:>4}, z={:>4}>'.format(
            self.position[0],self.position[1],self.position[2],
            self.velocity[0],self.velocity[1],self.velocity[2]
            )


def parse_moons(x):
    coord = re.compile(r'<x=(-?\d+), y=(-?\d+), z=(-?\d+)>')
    moons = []
    for line in x:
        r = coord.match(line)
        pos = [int(r.group(1)),int(r.group(2)),int(r.group(3))]
        moons.append(Body(pos))
    return moons

def step_moons(moons):
    for moon in moons:
        moon.calc_velocity(moons)
    for moon in moons:
        moon.calc_position()

def print_moons(moons):
    for moon in moons:
        print(moon)
    print()
    for moon in moons:
        print('E: {}'.format(moon.calc_total_energy()))

def calc_system_energy(moons):
    return sum(map(Body.calc_total_energy, moons))

def n_step_moons(moons, n):
    for i in range(n):
        step_moons(moons)

@timeit('Part 1')
def part_one(x):
    '''Solves part one'''
    moons = parse_moons(x)
    n_step_moons(moons,1000)

    return calc_system_energy(moons)

def part_one_visualized(x):
    '''Visualization'''
    moons = parse_moons(x)
    system_energy = []
    io_x = []
    callisto_x = []
    callisto_v = []
    for i in range(500000):
        step_moons(moons)
        system_energy.append(calc_system_energy(moons))
        io_x.append(moons[0].position[0])
        callisto_x.append(moons[3].position[0])
        callisto_v.append(moons[3].velocity[0])

    # plt.figure(1)
    # plt.plot(system_energy)
    # plt.xlabel('Steps')
    # plt.ylabel('System Energy (Elf-Energy Units)')

    plt.figure(2)
    plt.plot(io_x)
    plt.xlabel('Steps')
    plt.ylabel('X-position of IO (Elf-Metres)')

    plt.figure(3)
    plt.plot(callisto_x)
    plt.xlabel('Steps')
    plt.ylabel('X-position of Callisto (Elf-Metres)')
    plt.show()

    plt.figure(3)
    plt.plot(callisto_v)
    plt.xlabel('Steps')
    plt.ylabel('X-position of Callisto (Elf-Metres)')
    plt.show()

@timeit('Part 2')
def part_two(x):
    '''Solves part two'''
    moons = parse_moons(x)
    def extract(moons):
        x = [moon.position[0] for moon in moons]
        y = [moon.position[1] for moon in moons]
        z = [moon.position[2] for moon in moons]
        vx = [moon.velocity[0] for moon in moons]
        vy = [moon.velocity[1] for moon in moons]
        vz = [moon.velocity[2] for moon in moons]
        return (x,y,z,vx,vy,vz)
    stop = False
    init = extract(moons)
    i = 0
    m = [0,0,0]
    while not stop:
        i += 1
        step_moons(moons)
        e = extract(moons)
        for j in range(3):
            if e[j] == init[j] and m[j] == 0:
                m[j] = i+1
        if m[0] != 0 and m[1] != 0 and m[2] != 0:
            stop = True

    return np.lcm.reduce(m)

def part_two_visualized(x):
    '''Visualization'''
    pass

def test():
    '''Test functions'''
    lines = [
        '<x=-1, y=0, z=2>',
        '<x=2, y=-10, z=-7>',
        '<x=4, y=-8, z=8>',
        '<x=3, y=5, z=-1>',
    ]

    moons = parse_moons(lines)
    n_step_moons(moons,10)

    assert(calc_system_energy(moons) == 179)

    lines = [
        '<x=-8, y=-10, z=0>',
        '<x=5, y=5, z=10>',
        '<x=2, y=-7, z=3>',
        '<x=9, y=-8, z=-3>',
    ]
    moons = parse_moons(lines)
    n_step_moons(moons,100)

    assert(calc_system_energy(moons) == 1940)

    res = part_two(lines)

    assert(res == 4686774924)


@timeit('Total')
def main(args):
    with open(args[1], 'r') as f:
        x = [line.strip() for line in f.readlines()]
        print('Part 1 Result: {}'.format(part_one(x)))
        print('Part 2 Result: {}'.format(part_two(x)))

        # part_one_visualized(x)
        # part_two_visualized(x)

if __name__ == '__main__':
    test()
    main(sys.argv)