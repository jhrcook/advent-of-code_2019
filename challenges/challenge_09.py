#!/usr/bin/env python3

from pathlib import Path

from intcode import Intcode, IntcodeComputer, IntcodeInput

# ---- Part 1 ----

test_code = Intcode(
    [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
)
test_comp = IntcodeComputer(test_code.copy())
res = test_comp()
assert test_code == test_comp.code

test_code = Intcode([1102, 34915192, 34915192, 7, 4, 7, 99, 0])
test_comp = IntcodeComputer(test_code.copy())
res = test_comp()
assert len(str(res.output)) == 16

test_code = Intcode([104, 1125899906842624, 99])
test_comp = IntcodeComputer(test_code.copy())
res = test_comp()
assert res.output == test_code[1]

boost_code = Intcode()
with open(Path("data", "09", "input.txt"), "r") as file:
    for line in file:
        boost_code += Intcode([int(a) for a in line.strip().split(",")])
# print(boost_code)
intcode_computer = IntcodeComputer(boost_code, verbose=True)
res = intcode_computer(inputs=IntcodeInput([1]))
print(res)

# 203 too low
# TODO: go back through challenges that built up the Intcode comp and tidy it up.
