#!/usr/bin/env python3
# Problem description

import os, sys
import numpy as np

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from utils.decorators import *

def format_image(w,h,i):
    num_layers = len(i)//(w*h)
    im = np.zeros((num_layers*w*h),dtype=np.uint8)
    for c in range(num_layers*w*h):
        im[c] = np.uint8(i[c])

    im.resize(num_layers,h,w)
    # print(len(i),num_layers, im.shape)
    return im

def image_decoder(i):
    x,h,w = i.shape
    im = np.zeros((h,w),dtype=np.uint8)
    for c in range(x):
        for y in range(h):
            for x in range(w):
                if im[y,x] == 0:
                    if i[c,y,x] == 0:
                        im[y,x] = 1
                    elif i[c,y,x] == 1:
                        im[y,x] = 2
    return im


@timeit('Part 1')
def part_one(x):
    '''Solves part one'''
    im = format_image(25, 6, x)

    min_zeros = (10000, -1) # N, layer
    print(im.shape)
    for i in range(im.shape[0]):
        n = sum(im[i,:,:].flatten() == 0)
        # print(n)
        if n < min_zeros[0]:
            min_zeros = (n, i)

    n_ones = sum(im[min_zeros[1],:,:].flatten() == 1)
    n_twos = sum(im[min_zeros[1],:,:].flatten() == 2)

    return n_ones*n_twos
    # import matplotlib.pyplot as plt
    # plt.figure(1)
    # plt.imshow(im[0,:,:])
    # plt.show()

@timeit('Part 2')
def part_two(x):
    '''Solves part two'''
    import matplotlib.pyplot as plt
    im = format_image(25, 6, x)
    im = image_decoder(im)

    plt.figure(1)
    plt.imshow(im)
    plt.show()

def part_two_visualized(x):
    '''Visualization'''
    pass

def test():
    '''Test functions'''
    import matplotlib.pyplot as plt
    x = '0222112222120000'
    im = format_image(2,2, x)
    im = image_decoder(im)
    plt.figure(1)
    plt.imshow(im)
    plt.show()

    assert(True)

@timeit('Total')
def main(args):
    with open(args[1], 'r') as f:
        x = [line.strip() for line in f.readlines()]
        print('Part 1 Result: {}'.format(part_one(x[0])))
        print('Part 2 Result: {}'.format(part_two(x[0])))

        part_two_visualized(x)

if __name__ == '__main__':
    test()
    main(sys.argv)