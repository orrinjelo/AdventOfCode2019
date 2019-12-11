#!/usr/bin/env python3
# The Intcode program will serve as the brain of the robot. The program uses input instructions to access the robot's camera: provide 0 if the robot is over a black panel or 1 if the robot is over a white panel. Then, the program will output two values:

#     First, it will output a value indicating the color to paint the panel the robot is over: 0 means to paint the panel black, and 1 means to paint the panel white.
#     Second, it will output a value indicating the direction the robot should turn: 0 means it should turn left 90 degrees, and 1 means it should turn right 90 degrees.

# After the robot turns, it should always move forward exactly one panel. The robot starts facing up.

import os, sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from utils.decorators import *
from vm.vm import ElfMachine

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

BLACK = 0
WHITE = 1

class HullPaintingRobot():
    def __init__(self, canvas_size=100,start=None):
        self.canvas_size = canvas_size
        self.direction = UP
        self.sym = 'r^'
        self.canvas = np.full((canvas_size,canvas_size),-1,dtype=int)
        if start is None:
            self.position = (canvas_size//2,canvas_size//2)
        else:
            self.position = start
        self.tick = True

    def instruct(self, x):
        self.interpret_instruction(x)
        self.tick = not self.tick

    def observe(self, *args, **kwargs):
        return max(0,self.canvas[self.position[0],self.position[1]])

    def interpret_instruction(self, x):

        if self.tick:
            # Paint panel
            if x == 0:
                self.canvas[self.position[0],self.position[1]] = BLACK
            elif x == 1:
                self.canvas[self.position[0],self.position[1]] = WHITE
        else:
            # Rotate
            if x == 1:
                self.direction = (self.direction + 1) % 4
            elif x == 0:
                self.direction = (self.direction - 1) % 4

            # Move forward
            if self.direction == UP:
                self.position = (self.position[0],self.position[1]-1)
                self.sym = 'r^'
            elif self.direction == DOWN:
                self.position = (self.position[0],self.position[1]+1)
                self.sym = 'rv'
            elif self.direction == LEFT:
                self.position = (self.position[0]-1,self.position[1])
                self.sym = 'r<'
            elif self.direction == RIGHT:
                self.position = (self.position[0]+1,self.position[1])
                self.sym = 'r>'


@timeit('Part 1')
def part_one(x):
    '''Solves part one'''
    rob = HullPaintingRobot()
    vm = ElfMachine(input_cb=rob.observe, output_cb=rob.instruct, mem_size=2048)
    vm.run_program(x)

    plt.figure(1)
    plt.imshow(rob.canvas)
    plt.show()

    rob.canvas[rob.canvas==0]=1
    rob.canvas[rob.canvas==-1]=0

    return np.sum(rob.canvas.flatten())

@timeit('Part 2')
def part_two(x):
    '''Solves part two'''
    rob = HullPaintingRobot()
    rob.canvas[rob.position[0],rob.position[1]] = 1
    vm = ElfMachine(input_cb=rob.observe, output_cb=rob.instruct, mem_size=2048)
    vm.run_program(x)

    plt.figure(1)
    plt.imshow(np.transpose(rob.canvas))
    plt.show()

def part_two_visualized(x):
    '''Visualization'''
    rob = HullPaintingRobot(canvas_size=50,start=(0,0))
    rob.canvas[rob.position[0],rob.position[1]] = 1

    fig,ax = plt.subplots()

    p = plt.imshow(np.transpose(rob.canvas))
    t, = plt.plot([rob.position[0]],[rob.position[1]],rob.sym)
    frames = [[p,t]]

    def observe(*args, **kwargs):
        res = rob.observe(*args, **kwargs)
        p = plt.imshow(np.transpose(rob.canvas))
        t, = plt.plot([rob.position[0]],[rob.position[1]],rob.sym)
        frames.append([p,t])
        return res

    vm = ElfMachine(input_cb=observe, output_cb=rob.instruct, mem_size=2048)
    vm.run_program(x)

    ani = animation.ArtistAnimation(fig, frames, interval=50, blit=False)
    ani.save('day_11.gif', writer='imagemagick')
    plt.show()

def test():
    '''Test functions'''
    rob = HullPaintingRobot()

    inst = [1,0,0,0,1,0,1,0,0,1,1,0,1,0]
    for i in inst:
        rob.instruct(i)

    # plt.figure()
    # plt.imshow(rob.canvas)
    # plt.show()


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