#!/usr/bin/env python3
# Problem description

import os, sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from vm.vm import ElfMachine
from utils.decorators import *

@timeit('Part 1')
def part_one(x):
    '''Solves part one'''
    global res

    res = 0
    def output_cb(*args, **kwargs):
        global res
        print(args, kwargs)
        res = args[0]

    def input_cb(*args, **kwargs):
        return 1

    vm = ElfMachine(output_cb=output_cb, input_cb=input_cb, mem_size=2048)
    vm.run_program(x)

    return res

@timeit('Part 2')
def part_two(x):
    '''Solves part two'''
    global res

    res = 0
    def output_cb(*args, **kwargs):
        global res
        print(args, kwargs)
        res = args[0]

    def input_cb(*args, **kwargs):
        return 2

    vm = ElfMachine(output_cb=output_cb, input_cb=input_cb, mem_size=2048)
    vm.run_program(x)

    return res

def part_two_visualized(x):
    '''Visualization'''
    pass

def test():
    '''Test functions'''
    global res
    prog = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]

    res = []
    def output_cb_1(*args, **kwargs):
        res.append(args[0])

    vm = ElfMachine(output_cb=output_cb_1)
    vm.run_program(prog)

    assert(prog == res)

    prog = [1102,34915192,34915192,7,4,7,99,0]
    res = 0

    def output_cb_2(*args, **kwargs):
        global res
        res = args[0]

    vm = ElfMachine(output_cb=output_cb_2)
    vm.run_program(prog)

    assert(len(str(res)) == 16)

    prog = [104,1125899906842624,99]
    vm = ElfMachine(output_cb=output_cb_2)
    vm.run_program(prog)

    assert(res == 1125899906842624)    


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