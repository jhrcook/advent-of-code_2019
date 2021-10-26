#!/usr/bin/env python3

from dataclasses import dataclass
from enum import Enum, unique
from pathlib import Path


class TooManyWiresFoundInInputException(BaseException):
    pass


class UnknownDirectionException(BaseException):
    pass


WireInstructions = list[str]
Coordinate = tuple[int, int]
WireTrace = list[Coordinate]


@unique
class Direction(Enum):
    """Wire instruction directions."""

    L = "L"
    R = "R"
    U = "U"
    D = "D"


@dataclass(frozen=True)
class Wires:
    """Collection of wire instructions."""

    wire1: WireInstructions
    wire2: WireInstructions

    def __str__(self) -> str:
        s1 = ", ".join(self.wire1)
        s2 = ", ".join(self.wire2)
        return "Wires:" + "\n  (1) " + s1 + "\n  (2) " + s2


def parse_input_to_two_wires(text_input: str) -> Wires:
    wires: list[list[str]] = []
    for line in text_input.split("\n"):
        line = line.strip()
        if len(line) > 0:
            wires.append(line.split(","))
    if len(wires) != 2:
        raise TooManyWiresFoundInInputException(text_input)
    return Wires(wire1=wires[0], wire2=wires[1])


def get_trace_from_location(
    current_pos: Coordinate, direction: Direction, stride: int
) -> WireTrace:
    trace: WireTrace = []
    if direction == Direction.L:
        for i in reversed(range(current_pos[1] - stride, current_pos[1])):
            trace.append((current_pos[0], i))
    elif direction == Direction.R:
        for i in range(current_pos[1] + 1, current_pos[1] + stride + 1):
            trace.append((current_pos[0], i))
    elif direction == Direction.D:
        for i in reversed(range(current_pos[0] - stride, current_pos[0])):
            trace.append((i, current_pos[1]))
    elif direction == Direction.U:
        for i in range(current_pos[0] + 1, current_pos[0] + stride + 1):
            trace.append((i, current_pos[1]))
    else:
        raise UnknownDirectionException(direction)
    return trace


def trace_wire(wire: WireInstructions) -> WireTrace:
    wire_trace: WireTrace = [(0, 0)]
    for instruction in wire:
        current_pos = wire_trace[len(wire_trace) - 1]
        direction = Direction(instruction[0])
        stride = int(instruction[1:])
        wire_trace += get_trace_from_location(current_pos, direction, stride)
    return wire_trace


def get_wire_crosses(trace1: WireTrace, trace2: WireTrace) -> set[Coordinate]:
    return set(trace1).intersection(trace2)


def calculate_distance_to_closest_cross(
    trace1: WireTrace, trace2: WireTrace
) -> tuple[int, Coordinate]:
    crosses = list(get_wire_crosses(trace1, trace2))
    distances = [abs(a) + abs(b) for a, b in crosses if a != 0 and b != 0]
    idx = distances.index(min(distances))
    return distances[idx], crosses[idx]


def find_closest_point_of_overlap_for_two_wires(wires: Wires) -> tuple[int, Coordinate]:
    trace1 = trace_wire(wires.wire1)
    trace2 = trace_wire(wires.wire2)
    return calculate_distance_to_closest_cross(trace1, trace2)


# ---- Part 1 ----

# Test input
test_input1 = """
R75,D30,R83,U83,L12,D49,R71,U7,L72
U62,R66,U55,R34,D71,R55,D58,R83
"""
test_answer1 = 159

test_input2 = """
R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
U98,R91,D20,R16,D67,R40,U7,R15,U6,R7
"""
test_answer2 = 135

test_input3 = """
R8,U5,L5,D3
U7,R6,D4,L4
"""
test_answer3 = 6

for i, (test_in, test_ans) in enumerate(
    [
        (test_input1, test_answer1),
        (test_input2, test_answer2),
        (test_input3, test_answer3),
    ]
):
    test_wires = parse_input_to_two_wires(test_in)
    ans, coord = find_closest_point_of_overlap_for_two_wires(test_wires)
    print(f"test {i} -->  answer: {ans}  coord: {coord}")
    assert ans == test_ans

# Real input
with open(Path("data", "03", "input.txt"), "r") as file:
    wires_input = ""
    for line in file:
        wires_input += line


wires = parse_input_to_two_wires(wires_input)
ans, coord = find_closest_point_of_overlap_for_two_wires(wires)
print(f"(part 1) closest crossing of the wires was at {coord} at a distance of {ans}")
print("")

# ---- Part 2 ----


def calculate_distance_to_shortest_cross(
    trace1: WireTrace, trace2: WireTrace
) -> tuple[int, Coordinate]:
    crosses = list(get_wire_crosses(trace1, trace2))
    distances: list[int] = []
    for cross in crosses:
        if cross == (0, 0):
            continue
        d1 = trace1.index(cross)
        d2 = trace2.index(cross)
        distances.append(d1 + d2)
    idx = distances.index(min(distances))
    return distances[idx], crosses[idx]


def find_shortest_path_for_two_wires(wires: Wires) -> tuple[int, Coordinate]:
    trace1 = trace_wire(wires.wire1)
    trace2 = trace_wire(wires.wire2)
    return calculate_distance_to_shortest_cross(trace1, trace2)


test_answer1, test_answer2, test_answer3 = 610, 410, 30
for i, (test_in, test_ans) in enumerate(
    [
        (test_input1, test_answer1),
        (test_input2, test_answer2),
        (test_input3, test_answer3),
    ]
):
    test_wires = parse_input_to_two_wires(test_in)
    ans, coord = find_shortest_path_for_two_wires(test_wires)
    print(f"test {i} -->  answer: {ans}  coord: {coord}")
    assert ans == test_ans

ans, coord = find_shortest_path_for_two_wires(wires)
print(f"(part 2) shortest crossing of the wires was at {coord} at a distance of {ans}")
print("")
