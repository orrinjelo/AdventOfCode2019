#!/usr/bin/env python3
# Problem description

import os, sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from utils.decorators import *
from vm.vm import ElfMachine

def execute_amps(program, amps):
    global res, idx, flip
    res = 0
    idx = -1
    flip = True
    def receive(*args, **kwargs):
        global res
        res = args[0]
    def send(*args, **kwargs):
        global idx, flip
        if flip:
            flip = False
            idx += 1
            # print('flip: {}'.format(amps[idx]))
            if idx > 4:
                idx = 0
            return amps[idx]
        else:
            # print('flop: {}'.format(res))
            flip = True
            return res

    vm = ElfMachine(send, receive)
    for _ in range(5):
        vm.run_program(program)
    return res

def execute_amps_feedback(program, amps):
    global queues
    from queue import Queue

    queues = [
        Queue(),
        Queue(),
        Queue(),
        Queue(),
        Queue(),
    ]

    queues[0].put(amps[0])
    queues[0].put(0)
    queues[1].put(amps[1])
    queues[2].put(amps[2])
    queues[3].put(amps[3])
    queues[4].put(amps[4])

    def rec_wrap(i):
        def receive(*args, **kwargs):
            global queues
            queues[i].put(args[0])
        return receive

    def send_wrap(i):
        def send(*args, **kwargs):
            global queues
            return queues[i].get(block=True)
        return send

    vms = [ElfMachine(input_cb=send_wrap(0), output_cb=rec_wrap(1)), 
           ElfMachine(input_cb=send_wrap(1), output_cb=rec_wrap(2)), 
           ElfMachine(input_cb=send_wrap(2), output_cb=rec_wrap(3)), 
           ElfMachine(input_cb=send_wrap(3), output_cb=rec_wrap(4)), 
           ElfMachine(input_cb=send_wrap(4), output_cb=rec_wrap(0))]

    import threading

    threads = []

    for i in range(5):
        threads.append( threading.Thread(
            target=vms[i].run_program, args=(program,)
        ))

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    res = queues[0].get()

    return res

@timeit('Part 1')
def part_one(x):
    '''Solves part one'''
    from itertools import permutations
    perm = permutations([0,1,2,3,4])
    max_thruster = (0, [1,2,3,4,5])
    for p in perm:
        res = execute_amps(x, list(p))
        if res > max_thruster[0]:
            max_thruster = (res, p)

    return max_thruster

@timeit('Part 2')
def part_two(x):
    '''Solves part two'''
    from itertools import permutations
    perm = permutations([5, 6, 7, 8, 9])
    max_thruster = (0, [5, 6, 7, 8, 9])
    for p in perm:
        res = execute_amps_feedback(x, list(p))
        if res > max_thruster[0]:
            max_thruster = (res, p)

    return max_thruster

def part_two_visualized(x):
    '''Visualization'''
    pass

def test():
    '''Test functions'''
    test_prog = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
    signal = 43210
    amps = [4,3,2,1,0]
    res = execute_amps(test_prog, amps)
    assert(res == signal)

    test_prog = [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]
    signal = 54321
    amps = [0, 1, 2, 3, 4]
    res = execute_amps(test_prog, amps)
    assert(res == signal)

    test_prog = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,
        1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]
    signal = 65210
    amps = [1,0,4,3,2]
    res = execute_amps(test_prog, amps)
    assert(res == signal)

    test_prog = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
        27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
    signal = 139629729
    amps = [9,8,7,6,5]
    res = execute_amps_feedback(test_prog, amps)

    print('Tests complete!')

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