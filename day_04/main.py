#!/usr/bin/env python3
# However, they do remember a few key facts about the password:
#
#     It is a six-digit number.
#     The value is within the range given in your puzzle input.
#     Two adjacent digits are the same (like 22 in 122345).
#     Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).
#
# Other than the range rule, the following are true:
#
#     111111 meets these criteria (double 11, never decreases).
#     223450 does not meet these criteria (decreasing pair of digits 50).
#     123789 does not meet these criteria (no double).


import os, sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from utils.decorators import *

def is_sequential(x):
    y = str(x)
    n = 0
    for i in y:
        if n > int(i):
            return False
        n = int(i)
    return True

def has_double_digit(x):
    if len(str(x)) > len(set(str(x))):
        return True
    else:
        return False

def is_special(x):
    for i in range(len(str(x))):
        count = 1
        for j in range(len(str(x))):
            if i != j:
                if str(x)[i] == str(x)[j]:
                    count += 1
        if count == 2:
            return True
    return False


@timeit('Part 1')
def part_one(x):
    '''Solves part one'''
    a,b = int(x[0]),int(x[1])
    r = range(a,b+1)
    filtered = filter(is_sequential,r)
    filtered2 = filter(has_double_digit,filtered)
    return len(list(filtered2))

@timeit('Part 2')
def part_two(x):
    '''Solves part two'''
    a,b = int(x[0]),int(x[1])
    r = range(a,b+1)
    filtered = filter(is_sequential,r)
    filtered2 = filter(is_special,filtered)
    return len(list(filtered2))

def part_one_visualized(x):
    '''Visualization'''
    pass

def part_two_visualized(x):
    '''Visualization'''
    pass

def test():
    '''Test functions'''
    assert(is_sequential(12345))
    assert(not is_sequential(43523))
    assert(is_sequential(11111))
    assert(not is_sequential(2222221))
    assert(is_sequential(2999999))
    assert(has_double_digit(112345))
    assert(not has_double_digit(134567))
    assert(is_special(112233))
    assert(not is_special(123444))
    assert(is_special(111122))

@timeit('Total')
def main(args):
    with open(args[1], 'r') as f:
        line = f.readlines()[0]
        x = line.strip().split('-')
        print('Part 1 Result: {}'.format(part_one(x)))
        print('Part 2 Result: {}'.format(part_two(x)))

        part_one_visualized(x)
        part_two_visualized(x)

if __name__ == '__main__':
    test()
    main(sys.argv)