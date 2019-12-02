#!/usr/bin/env python3
# An Intcode program is a list of integers separated by commas (like 1,0,0,3,99). To run one, start by looking at the first integer (called position 0). Here, you will find an opcode - either 1, 2, or 99. The opcode indicates what to do; for example, 99 means that the program is finished and should immediately halt. Encountering an unknown opcode means something went wrong.
#
# Opcode 1 adds together numbers read from two positions and stores the result in a third position. The three integers immediately after the opcode tell you these three positions - the first two indicate the positions from which you should read the input values, and the third indicates the position at which the output should be stored.
#
# For example, if your Intcode computer encounters 1,10,20,30, it should read the values at positions 10 and 20, add those values, and then overwrite the value at position 30 with their sum.
#
# Opcode 2 works exactly like opcode 1, except it multiplies the two inputs instead of adding them. Again, the three integers after the opcode indicate where the inputs and outputs are, not their values.
#
# Once you're done processing an opcode, move to the next one by stepping forward 4 positions.
# ======================================
# "With terminology out of the way, we're ready to proceed. To complete the gravity assist, you need to determine what pair of inputs produces the output 19690720."

import os, sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from utils.decorators import *

def add(s, a, b, c):
    try:
        s[c] = s[a] + s[b] 
    except IndexError as e:
        print('Invalid index: {} {} {}'.format(a, b, c))
        print('Input list: {}'.format(s))
        raise e

def mul(s, a, b, c):
    try:
        s[c] = s[a] * s[b]
    except IndexError as e:
        print('Invalid index: {} {} {}'.format(a, b, c))
        print('Input list: {}'.format(s))
        raise e

def program_alarm(s, p1=None, p2=None):
    pc = 0
    if p1:
        s[1] = p1
    if p2:
        s[2] = p2
    while s[pc] != 99: # Program term
        # print('PC: {}'.format(pc))
        if s[pc] == 1:
            add(s, s[pc+1], s[pc+2], s[pc+3])
            pc += 4
        elif s[pc] == 2:
            mul(s, s[pc+1], s[pc+2], s[pc+3])
            pc += 4
        else:
            print('Erroneous op: {}'.format(s[pc]))
    return s[0]

@timeit('Part 1')
def part_one(s):
    '''Solves part one'''
    return program_alarm(s, 12, 2)


@timeit('Part 2')
def part_two(x):
    '''Solves part two'''
    for noun in range(99):
        for verb in range(noun):
            try:
                s = x[:]
                ret = program_alarm(s, noun, verb)
                if ret == 19690720:
                    return 100 * noun + verb
            except:
                pass
    return 'Not found'

def part_two_visualized(x):
    '''Visualization'''
    from PIL import Image, ImageDraw, ImageFont
    frames = []

    def write_text(pc=-1):
        # make a blank image for the text, initialized to transparent text color
        txt = Image.new('RGBA', (800, 600), (0,0,0,0))

        # get a font
        fnt = ImageFont.truetype('Pillow/Tests/fonts/FreeMonoBold.ttf', 16)
        # get a drawing context
        d = ImageDraw.Draw(txt)
        for i in range(len(x)):
            c = (255,255,255,255)
            if pc == i:
                c = (255,0,0,255)
            elif pc+1 == i and x[pc] != 99:
                c = (0,255,0,255)
            elif pc+2 == i and x[pc] != 99:
                c = (0,0,255,255)
            elif pc+3 == i and x[pc] != 99:
                c = (255,255,0,255)
            d.text((75*(i%10),30*(i//10)), str(x[i]), font=fnt, fill=c)
        return txt

    def program_alarm_vis(s, p1=None, p2=None):
        pc = 0
        if p1:
            s[1] = p1
        if p2:
            s[2] = p2
        while s[pc] != 99: # Program term
            frames.append(write_text(pc))
            if s[pc] == 1:
                add(s, s[pc+1], s[pc+2], s[pc+3])
                pc += 4
            elif s[pc] == 2:
                mul(s, s[pc+1], s[pc+2], s[pc+3])
                pc += 4
            else:
                print('Erroneous op: {}'.format(s[pc]))
        for _ in range(10):
            frames.append(write_text(pc))
        return s[0]

    program_alarm_vis(x, 12, 2)
    frames[0].save('day_02.gif', format='GIF', append_images=frames[1:], save_all=True, duration=500, delay=500, loop=0)

def test():
    '''Test functions'''
    inp = [1,9,10,3,2,3,11,0,99,30,40,50]
    oup = 3500

    tout = program_alarm(inp)
    assert(oup == tout)

    inp = [1,1,1,4,99,5,6,0,99]
    oup = 30

    tout = program_alarm(inp)
    assert(oup == tout)

    inp = [2,4,4,5,99,0]
    oup = 2

    tout = program_alarm(inp)
    assert(oup == tout)

    inp = [1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,99]
    oup = 1

    tout = program_alarm(inp)
    assert(oup == tout)

    print('Test 1 passes.')

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

        part_two_visualized(xv)

if __name__ == '__main__':
    test()
    main(sys.argv)
    # I get 1090665 but AoC isn't accepting...