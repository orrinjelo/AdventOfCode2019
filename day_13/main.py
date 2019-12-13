#!/usr/bin/env python3
# Problem description

import os, sys
import numpy as np
import matplotlib.pyplot as plt

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from utils.decorators import *
from vm.vm import ElfMachine

class Arcade():
    def __init__(self,screen_size=(40,20), input_cb=print):
        self.screen = np.zeros(screen_size)
        self.vm = ElfMachine(output_cb=self.disp, input_cb=input_cb, mem_size=4096)
        self.x, self.y = -2, -2
        self.score = 0
        self.ball = (0,0)
        self.paddle = (0,0)
        
    def run(self,x):
        self.vm.run_program(x)

    def disp(self,i):
        if self.x == -2:
            self.x = i
        elif self.y == -2:
            self.y = i
        else:
            x,y,c = self.x, self.y, i
            self.x, self.y = -2, -2

            if x == -1 and y == 0:
                self.score = c
            else:
                self.screen[x,y] = c
                if c == 4:
                    self.ball = (x,y)
                elif c == 3:
                    self.paddle = (x,y)


@timeit('Part 1')
def part_one(x):
    '''Solves part one'''
    a = Arcade()
    a.run(x)

    blocks = np.where(a.screen == 2)

    plt.figure(1)
    plt.imshow(np.transpose(a.screen))
    plt.show()

    return len(blocks[0])

@timeit('Part 2')
def part_two(x):
    '''Solves part two'''
    
    def dumb(x):
        ballx, bally = a.ball
        paddx, paddy = a.paddle
        if ballx > paddx:
            return 1
        elif ballx < paddx:
            return -1
        else:
            return 0

    a = Arcade(input_cb=dumb)

    x[0] = 2
    a.run(x)

    plt.figure(1)
    plt.imshow(np.transpose(a.screen))
    plt.show()

    return a.score

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
        print('Part 1 Result: {}'.format(part_one(x)))
        print('Part 2 Result: {}'.format(part_two(x)))

        part_two_visualized(x)

if __name__ == '__main__':
    test()
    main(sys.argv)