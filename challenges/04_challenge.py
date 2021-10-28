#!/usr/bin/env python3

import re

# Puzzle input.
puzzle_input = "156218-652527"
low, high = [int(x) for x in puzzle_input.split("-")]
print(f"range: {low} - {high}")


class BrokenInvariantException(BaseException):
    pass


def two_adjacent_values_p1(pswd: str) -> bool:
    for a, b in zip(pswd[1:], pswd[:-1]):
        if a == b:
            return True
    return False


def two_adjacent_values_p2(pswd: str) -> bool:
    for a in set(pswd):
        runs = re.findall(f"{a}+", pswd)
        if len(runs) != 1:
            raise BrokenInvariantException(pswd)
        run = runs[0]
        if len(run) == 2:
            return True
    return False


def all_digits_increase(pswd: str) -> bool:
    for i, j in zip(pswd[:-1], pswd[1:]):
        if i > j:
            return False
    return True


# Set variable to determine which part of the puzzle to solve.
PART = 2
if PART == 1:
    two_adjacent_values = two_adjacent_values_p1
elif PART == 2:
    two_adjacent_values = two_adjacent_values_p2
else:
    raise BaseException(f"Unknown puzzle part: {PART}")

# Find set of all passwords.
possible_passwords: set[int] = set()

for x in range(low, high):
    password = str(x)
    if not all_digits_increase(password):
        continue
    elif not two_adjacent_values(password):
        continue
    possible_passwords.add(x)


print(f"(part {PART}) number of possible passwords: {len(possible_passwords)}")
