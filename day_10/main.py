#!/usr/bin/env python3
# Problem description

import os, sys
import numpy as np
import matplotlib.pyplot as plt

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from utils.decorators import *

@timeit('Parsing map.')
def parse_map(m):
    h = len(m)
    w = len(m[0])
    mp = np.zeros((w,h),dtype=int)

    for y in range(len(m)):
        for x in range(len(m[0])):
            mp[x,y] = 1 if m[y][x] == '#' else 0

    return mp

def calc_slope(a,b):
    return np.degrees(np.arctan2((b[0]-a[0]),-(b[1]-a[1])))

def generate_digest(x):
    asteroids = np.argwhere(x==1)
    digest = {}
    for a in asteroids:
        for b in asteroids:
            if tuple(a) == tuple(b):
                continue
            slope = calc_slope(a,b)
            if tuple(a) in digest.keys():
                if slope in digest[tuple(a)].keys():
                    digest[tuple(a)][slope].append(tuple(b))
                else:
                    digest[tuple(a)][slope] = [tuple(b)]
            else:
                digest[tuple(a)] = {
                    slope: [tuple(b)]
                }
    return digest

@timeit('Part 1')
def part_one(x):
    '''Solves part one'''
    digest = generate_digest(x)

    best = (0, (0,0))

    for k in digest.keys():
        if len(digest[k]) > best[0]:
            best = (len(digest[k]), k)

    return best

@timeit('Part 2')
def part_two(x, station):
    '''Solves part two'''
    digest = generate_digest(x)
    
    sweep = sorted(digest[station[1]].keys(),key=lambda x: (x-360.0)%360.0)
    # print(sweep)

    n = 0
    c = 0

    def dist(x,y):
        return ((x[0]-y[0])**2 + (x[1]-y[1])**2)**0.5

    beleted = []

    while n < 200:
        a_list = digest[station[1]][sweep[c]] 
        closest = (10000, (0,0))
        if not a_list:
            continue
        for entry in a_list:
            d = dist(entry, station[1])

            # if entry == (11,12):
            #     print(d, closest, station)

            if d < closest[0]:
                closest = (d, entry)
        digest[station[1]][sweep[c]].remove(closest[1])
        beleted.append(closest[1])
        c += 1
        if c == len(sweep):
            c = 0
        n += 1
        # print(beleted, len(beleted))
        if n == 200:
            # print(beleted, len(beleted))
            return (closest[1][0]*100 + closest[1][1], beleted)
        # not 1217

    return (0, beleted)

def part_two_visualized(x, station, history):
    '''Visualization'''
    import matplotlib.animation as animation

    bg = np.zeros_like(x)

    fig, ax = plt.subplots(1)
    plt.gca().invert_yaxis()
    ax.axis('off') #xlim=(0,x.shape[0]-1),ylim=(0,x.shape[1]-1))
    fig.set_facecolor('xkcd:black')
    fig.patch.set_alpha(0.)
    # im = plt.imshow(np.transpose(x))
    asteroids = np.where(x==1)
    plt.imshow(bg,cmap='gray')
    plt.plot(asteroids[0], asteroids[1], 'yh')
    plt.plot([station[1][0]],[station[1][1]],'gs')
    hist_x, hist_y = [x[0] for x in history],[x[1] for x in history]
    p, = plt.plot([hist_x[0]], [hist_y[0]] ,'r8')
    pk, = plt.plot([], [] ,'k8')
    l, = plt.plot([station[1][0],hist_x[0]],[station[1][1],hist_y[0]],'r-')

    def update(i):
        p.set_data([hist_x[:i],hist_y[:i]])
        pk.set_data([hist_x[:i-1],hist_y[:i-1]])
        l.set_data([station[1][0],hist_x[i]],[station[1][1],hist_y[i]])
        return p

    ani = animation.FuncAnimation(fig, update, 200, interval=100)
    ani.save('d10.gif',writer='imagemagick')
    plt.show()
    

def test():
    '''Test functions'''
    map_1 = [
    '.#..#',
    '.....',
    '#####',
    '....#',
    '...##',
    ]
    m1 = parse_map(map_1)
    res = part_one(m1)
    assert(res[0] == 8)

    map_2 = [
        '......#.#.',
        '#..#.#....',
        '..#######.',
        '.#.#.###..',
        '.#..#.....',
        '..#....#.#',
        '#..#....#.',
        '.##.#..###',
        '##...#..#.',
        '.#....####',
    ]
    m2 = parse_map(map_2)
    res = part_one(m2)
    assert(res[0] == 33)
    # res = part_two(m2, res)

    # map_3 = [
    #     '.#....#####...#..',
    #     '##...##.#####..##',
    #     '##...#...#.#####.',
    #     '..#.....#...###..',
    #     '..#.#.....#....##',
    # ]
    # m3 = parse_map(map_3)
    # station = part_one(m3)
    # res = part_two(m3, station)

    map_4 = [
        '.#..##.###...#######',
        '##.############..##.',
        '.#.######.########.#',
        '.###.#######.####.#.',
        '#####.##.#.##.###.##',
        '..#####..#.#########',
        '####################',
        '#.####....###.#.#.##',
        '##.#################',
        '#####.##.###..####..',
        '..######..##.#######',
        '####.##.####...##..#',
        '.#####..#.######.###',
        '##...#.##########...',
        '#.##########.#######',
        '.####.#.###.###.#.##',
        '....##.##.###..#####',
        '.#.#.###########.###',
        '#.#.#.#####.####.###',
        '###.##.####.##.#..##',
    ]
    m4 = parse_map(map_4)
    station = part_one(m4)

    assert(station[1] == (11,13))
    res = part_two(m4, station)

    # The 1st asteroid to be vaporized is at 11,12.
    # The 2nd asteroid to be vaporized is at 12,1.
    # The 3rd asteroid to be vaporized is at 12,2.
    # The 10th asteroid to be vaporized is at 12,8.
    # The 20th asteroid to be vaporized is at 16,0.
    # The 50th asteroid to be vaporized is at 16,9.
    # The 100th asteroid to be vaporized is at 10,16.
    # The 199th asteroid to be vaporized is at 9,6.
    # The 200th asteroid to be vaporized is at 8,2.
    # The 201st asteroid to be vaporized is at 10,9.
    # The 299th and final asteroid to be vaporized is at 11,1.
    # print(res[1][0])
    assert(res[1][0] == (11,12))
    assert(res[1][1] == (12,1))
    assert(res[1][2] == (12,2))
    assert(res[1][9] == (12,8))
    assert(res[1][19] == (16,0))
    assert(res[1][49] == (16,9))
    assert(res[1][99] == (10,16))
    assert(res[1][198] == (9,6))
    assert(res[1][199] == (8,2))
    # assert(res[200] == (10,9))
    # assert(res[298] == (11,1))

@timeit('Total')
def main(args):
    with open(args[1], 'r') as f:
        x = [line.strip() for line in f.readlines()]
        x = parse_map(x)
        station = part_one(x)
        print('Part 1 Result: {}'.format(station))
        res, history = part_two(x, station)
        print('Part 2 Result: {}'.format(res))

        part_two_visualized(x, station, history)

if __name__ == '__main__':
    test()
    main(sys.argv)