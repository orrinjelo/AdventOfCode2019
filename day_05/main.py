#!/usr/bin/env python3
# Problem description

import os, sys
import os, sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from utils.decorators import *

def scrape_op(x):
    # Position 0, immediate 1
    DE = x % 100
    C = x // 100 % 10
    B = x // 1000 % 10
    A = x // 10000 % 10
    return A, B, C, DE

def _set(s, pc, c, x, C):
    if C == 0:
        s[c]    = x
    else:
        s[pc+3] = x

def add(s, pc):
    a, b, c = s[pc + 1], s[pc + 2], s[pc + 3]
    C,B,A, DE = scrape_op(s[pc])

    try:
        if A == 0:
            if B == 0:
                x = s[a] + s[b]
            else:
                x = s[a] + b 
        else:
            if B == 0:
                x = a + s[b]
            else:
                x = a + b
        _set(s, pc, c, x, C)
        pc += 4
    except IndexError as e:
        print('Invalid index: {} {} {}'.format(a, b, c))
        print('Input list: {}'.format(s))
        raise e
    return pc

def mul(s, pc):
    a, b, c = s[pc + 1], s[pc + 2], s[pc + 3]
    C, B, A, DE = scrape_op(s[pc])

    try:
        if A == 0:
            if B == 0:
                x = s[a] * s[b]
            else:
                x = s[a] * b 
        else:
            if B == 0:
                x = a * s[b]
            else:
                x = a * b
        _set(s, pc, c, x, C)
        pc += 4
    except IndexError as e:
        print('Invalid index: {} {} {}'.format(a, b, c))
        print('Input list: {}'.format(s))
        raise e
    return pc

def inp(s, pc):
    c = s[pc + 1]
    _, _, C, DE = scrape_op(s[pc])

    try:
        x = int(input('> '))
        _set(s,pc, c, x, C)
        pc += 2
    except IndexError as e:
        print('Invalid index:  {}'.format(c))
        print('Input list: {}'.format(s))
        raise e
    return pc

def prt(s, pc):
    c = s[pc + 1]
    _, _, C, DE = scrape_op(s[pc])

    try:
        if C == 0:
            print('= ',s[c])
        else:
            print('= ',c)
        pc += 2
    except IndexError as e:
        print('Invalid index: {}'.format(c))
        print('Input list: {}'.format(s))
        raise e
    return pc

def jmp(s, pc):
    b, c = s[pc + 1], s[pc + 2]
    _, C, B, DE = scrape_op(s[pc])

    try:
        if C == 0:
            if B == 0:
                if s[b]:
                    pc = s[c]
                else:
                    pc += 3
            else:
                if b:
                    pc = s[c]
                else:
                    pc += 3
        else:
            if B == 0:
                if s[b]:
                    pc = c
                else:
                    pc += 3
            else:
                if b:
                    pc = c
                else:
                    pc += 3
    except IndexError as e:
        print('Invalid index: {} {}'.format(b, c))
        print('Input list: {}'.format(s))
        raise e
    return pc    

def jmf(s, pc):
    b, c = s[pc + 1], s[pc + 2]
    _, C, B, DE = scrape_op(s[pc])

    try:
        if C == 0:
            if B == 0:
                if not s[b]:
                    pc = s[c]
                else:
                    pc += 3
            else:
                if not b:
                    pc = s[c]
                else:
                    pc += 3
        else:
            if B == 0:
                if not s[b]:
                    pc = c
                else:
                    pc += 3
            else:
                if not b:
                    pc = c
                else:
                    pc += 3
    except IndexError as e:
        print('Invalid index: {} {}'.format(b, c))
        print('Input list: {}'.format(s))
        raise e
    return pc 

def ltn(s, pc):
    a, b, c = s[pc + 1], s[pc + 2], s[pc + 3]
    C, B, A, DE = scrape_op(s[pc])

    try:
        if A == 0:
            if B == 0:
                x = 1 if s[a] < s[b] else 0
            else:
                x = 1 if s[a] < b else 0
        else:
            if B == 0:
                x = 1 if a < s[b] else 0
            else:
                x = 1 if a < b else 0
        _set(s, pc, c, x, C)
        pc += 4
    except IndexError as e:
        print('Invalid index: {} {} {}'.format(a, b, c))
        print('Input list: {}'.format(s))
        raise e
    return pc

def eql(s, pc):
    a, b, c = s[pc + 1], s[pc + 2], s[pc + 3]
    C, B, A, DE = scrape_op(s[pc])

    try:
        if A == 0:
            if B == 0:
                x = 1 if s[a] == s[b] else 0
            else:
                x = 1 if s[a] == b else 0
        else:
            if B == 0:
                x = 1 if a == s[b] else 0
            else:
                x = 1 if a == b else 0
        _set(s, pc, c, x, C)
        pc += 4
    except IndexError as e:
        print('Invalid index: {} {} {}'.format(a, b, c))
        print('Input list: {}'.format(s))
        raise e
    return pc

op = {
    1: add,
    2: mul,
    3: inp,
    4: prt,
    5: jmp,
    6: jmf,
    7: ltn,
    8: eql
}

def program_alarm(s, p1=None, p2=None):
    pc = 0
    if p1:
        s[1] = p1
    if p2:
        s[2] = p2
    while s[pc] != 99: # Program term
        try:
            pc = op[s[pc]%100](s, pc)
        except Exception as e:
            print(e)
            print('Erroneous op: {}'.format(s[pc]))
    return pc, s

@timeit('Part 1')
def part_one(s):
    '''Solves part one'''
    program_alarm(s)


@timeit('Part 2')
def part_two(x):
    '''Solves part two'''
    return None

def part_two_visualized(x):
    '''Visualization'''
    return None

def test():
    '''Test functions'''
    inp = [1002,4,3,4,33]
    oup = [1002,4,3,4,99]

    program_alarm(inp)
    assert(oup == inp)

    inp = [1101,100,-1,4,0]
    oup = [1101,100,-1,4,99]

    program_alarm(inp)
    assert(oup == inp)

    print('Test 1 passes.')

def test_human():
    '''Human interactable tests'''
    inp = [3,9,8,9,10,9,4,9,99,-1,8]
    print('Equal to 8? ',end='')
    program_alarm(inp)

    inp = [3,9,7,9,10,9,4,9,99,-1,8]
    print('Less than 8? ',end='')
    program_alarm(inp)

    inp = [3,3,1108,-1,8,3,4,3,99]
    print('Equal to 8? ',end='')
    program_alarm(inp)

    inp = [3,3,1107,-1,8,3,4,3,99]
    print('Less than 8? ',end='')
    program_alarm(inp)

@timeit('Total')
def main(args):
    with open(args[1], 'r') as f:
        x = [line.strip() for line in f.readlines()]
        x = x[0].split(',')
        x = list(map(int, x))
        x2 = x[:]
        xv = x[:]
        print('Part 1 Result: {}'.format(part_one(x)))
        print('Part 2 Result: {}'.format(part_two(x2)))

        # part_two_visualized(xv)

if __name__ == '__main__':
    test()
    # test_human()
    main(sys.argv)