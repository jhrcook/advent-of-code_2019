#!/usr/bin/env python3

from pathlib import Path
from typing import Final


class UnknownOperationException(BaseException):
    pass


def run_operation(op: int, x1: int, x2: int) -> int:
    if op == 1:
        return x1 + x2
    elif op == 2:
        return x1 * x2
    else:
        raise UnknownOperationException(op)


def run_intcode(code: list[int]) -> None:
    for i in range(0, len(code), 4):
        data = code[i : (i + 4)]
        if data[0] == 99:
            return
        code[data[3]] = run_operation(op=data[0], x1=code[data[1]], x2=code[data[2]])
    return


# test input 1
code_input = "1,9,10,3,2,3,11,0,99,30,40,50"
test_code: list[int] = [int(x) for x in code_input.split(",")]
test_result = [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]
run_intcode(test_code)
assert all([a == b for a, b in zip(test_code, test_result)])

# test input 2
test_code2 = [1, 1, 1, 4, 99, 5, 6, 0, 99]
test_result2 = [30, 1, 1, 4, 2, 5, 6, 0, 99]
run_intcode(test_code2)
assert all([a == b for a, b in zip(test_code2, test_result2)])

# real input
initial_code: list[int] = []
with open(Path("data", "02", "input.txt"), "r") as file:
    for line in file:
        initial_code += [int(x) for x in line.split(",")]

# manual adjustments per puzzle
code = initial_code.copy()
code[1] = 12
code[2] = 2

run_intcode(code)
print(f"(part 1) value at position 0: {code[0]}")


# ---- Part 2 ----


class NoValidInputFound(BaseException):
    pass


def search_intcode(
    initial_code: list[int], target: int, min: int = 0, max: int = 99
) -> tuple[int, int]:
    for i in range(min, max + 1):
        for j in range(min, max + 1):
            code = initial_code.copy()
            code[1] = i
            code[2] = j
            run_intcode(code)
            if code[0] == target:
                print(f"Found answer -- noun: {i}  verb: {j}")
                return i, j
    raise NoValidInputFound()


TARGET_OUTPUT: Final[int] = 19690720
noun, verb = search_intcode(initial_code.copy(), target=TARGET_OUTPUT)
print(f"noun: {noun}  verb: {verb}")
print(f"(part 2) 100 * noun + verb: {100 * noun + verb}")
