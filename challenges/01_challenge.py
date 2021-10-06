#!/usr/bin/env python3

import math
from pathlib import Path

# ---- Part I ----


def fuel_required(mass: float) -> float:
    """Calculate the fuel required for a mass."""
    return math.floor(mass / 3.0) - 2.0


# Read in puzzle input.
module_masses: list[float] = []
with open(Path("data", "01", "input.txt"), "r") as file:
    for line in file:
        module_masses.append(float(line.strip()))

# Tests from examples provided.
assert fuel_required(12) == 2
assert fuel_required(14) == 2
assert fuel_required(1969) == 654
assert fuel_required(100756) == 33583

fuel_requirements = [fuel_required(m) for m in module_masses]
print(f"(part 1) Total fuel required: {sum(fuel_requirements)}")

# ---- Part II ----


def total_fuel_for_module(mass: float) -> float:
    """Calculate the total fuel required for a module including the fuel's mass."""
    fuel_mass = fuel_required(mass)
    new_mass = fuel_required(fuel_mass)
    while new_mass > 0:
        fuel_mass += new_mass
        new_mass = fuel_required(new_mass)
    return fuel_mass


# Tests from examples provided.
assert total_fuel_for_module(14) == 2
assert total_fuel_for_module(1969) == 966
assert total_fuel_for_module(100756) == 50346

fuel_requirements = [total_fuel_for_module(m) for m in module_masses]
print(f"(part 2) Total fuel required: {sum(fuel_requirements)}")
