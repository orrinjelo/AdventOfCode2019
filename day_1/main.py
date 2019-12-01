#!/usr/bin/env python3
# The Elves quickly load you into a spacecraft and prepare to launch.
#
# At the first Go / No Go poll, every Elf is Go until the Fuel Counter-Upper. They haven't determined the amount of fuel required yet.
#
# Fuel required to launch a given module is based on its mass. Specifically, to find the fuel required for a module, take its mass, divide by three, round down, and subtract 2.
#
# For example:
#
#     For a mass of 12, divide by 3 and round down to get 4, then subtract 2 to get 2.
#     For a mass of 14, dividing by 3 and rounding down still yields 4, so the fuel required is also 2.
#     For a mass of 1969, the fuel required is 654.
#     For a mass of 100756, the fuel required is 33583.
#
# The Fuel Counter-Upper needs to know the total fuel requirement. To find it, individually calculate the fuel needed for the mass of each module (your puzzle input), then add together all the fuel values.
#
# What is the sum of the fuel requirements for all of the modules on your spacecraft?
# ============================================================================================================
# Fuel itself requires fuel just like a module - take its mass, divide by three, round down, and subtract 2. However, that fuel also requires fuel, and that fuel requires fuel, and so on. Any mass that would require negative fuel should instead be treated as if it requires zero fuel; the remaining mass, if any, is instead handled by wishing really hard, which has no mass and is outside the scope of this calculation.
#
# So, for each module mass, calculate its fuel and add it to the total. Then, treat the fuel amount you just calculated as the input mass and repeat the process, continuing until a fuel requirement is zero or negative. For example:
#
#     A module of mass 14 requires 2 fuel. This fuel requires no further fuel (2 divided by 3 and rounded down is 0, which would call for a negative fuel), so the total fuel required is still just 2.
#     At first, a module of mass 1969 requires 654 fuel. Then, this fuel requires 216 more fuel (654 / 3 - 2). 216 then requires 70 more fuel, which requires 21 fuel, which requires 5 fuel, which requires no further fuel. So, the total fuel required for a module of mass 1969 is 654 + 216 + 70 + 21 + 5 = 966.
#     The fuel required by a module of mass 100756 and its fuel is: 33583 + 11192 + 3728 + 1240 + 411 + 135 + 43 + 12 + 2 = 50346.
#
# What is the sum of the fuel requirements for all of the modules on your spacecraft when also taking into account the mass of the added fuel? 

import os, sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from utils.decorators import *

@timeit('Part 1')
def part_one(mass_list):
    '''Given a list of integer values, computes the fuel requirements'''
    mass_to_fuel = lambda x: max(0, x // 3 - 2)
    return sum(map(mass_to_fuel, mass_list))

@timeit('Part 2')
def part_two(mass_list):
    '''Given a list of integer values, computes the fuel requirements considering the fuel itself.'''
    mass_to_fuel = lambda x: max(0, x // 3 - 2)
    fuel = []
    for mass in mass_list:
        temp_mass = mass
        while len(fuel) == 0 or temp_mass != 0:
            amount_fuel = mass_to_fuel(temp_mass)
            fuel.append(amount_fuel)
            temp_mass = amount_fuel
    return sum(fuel)

def test():
    '''Test functions'''
    test_input_list_one = [12, 14, 1969, 100756]
    test_output_one = [2, 2, 654, 33583]
    output_one = part_one(test_input_list_one)
    assert(sum(test_output_one) == output_one)

    test_input_list_two = [14, 1969, 100756]
    test_output_two = [2, 966, 50346]
    output_two = part_two(test_input_list_two)
    assert(sum(test_output_two) == output_two)

@timeit('Total')
def main(args):
    with open(args[1], 'r') as f:
        mass_list = [int(line.strip()) for line in f.readlines()]
        print('Part 1 Result: {}'.format(part_one(mass_list)))
        print('Part 2 Result: {}'.format(part_two(mass_list)))

if __name__ == '__main__':
    # test()
    main(sys.argv)