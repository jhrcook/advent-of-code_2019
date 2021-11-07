#!/usr/bin/env python3

from itertools import permutations
from pathlib import Path
from typing import Callable, Sequence

from intcode import Intcode, IntcodeComputer, IntcodeInput

AmplifierPhaseSequence = Sequence[int]

intcode_program: Intcode = Intcode([])
with open(Path("data", "07", "input.txt"), "r") as file:
    for line in file:
        intcode_program += [int(x) for x in line.strip().split(",")]


def run_amplifier_series(
    intcode: Intcode, phase_sequence: AmplifierPhaseSequence
) -> int:
    value = 0
    for phase in phase_sequence:
        inputs = IntcodeInput([phase, value])
        # res = run_intcode(code=intcode.copy(), inputs=inputs, verbose=False)
        res = IntcodeComputer(code=intcode.copy())(inputs=inputs)
        assert res.output is not None
        value = res.output
    return value


def find_fastest_phase_sequence(
    intcode: Intcode,
    amp_method: Callable[[Intcode, AmplifierPhaseSequence], int],
    amp_phases: list[int],
) -> tuple[AmplifierPhaseSequence, int]:
    best_phase_seq: AmplifierPhaseSequence = []
    max_thrust = -1
    for phase_sequence in permutations(amp_phases):
        amp_thrust = amp_method(intcode.copy(), phase_sequence)
        if amp_thrust > max_thrust:
            max_thrust = amp_thrust
            best_phase_seq = list(phase_sequence)
    assert len(best_phase_seq) == len(amp_phases)
    return best_phase_seq, max_thrust


# Test input.
test_intcode = Intcode([3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0])
test_input_seq = [4, 3, 2, 1, 0]
test_output = 43210
test_res = run_amplifier_series(test_intcode, test_input_seq)
assert test_res == test_output
res_phase_seq, res_max_thrust = find_fastest_phase_sequence(
    test_intcode, amp_method=run_amplifier_series, amp_phases=list(range(5))
)
assert all([a == b for a, b in zip(test_input_seq, res_phase_seq)])
assert res_max_thrust == test_output

# Puzzle input
best_phase_seq, max_thrust = find_fastest_phase_sequence(
    intcode_program.copy(), amp_method=run_amplifier_series, amp_phases=list(range(5))
)
print("(part 1) Series method results:")
print(f"  sequence {best_phase_seq}")
print(f"  max thrust of {max_thrust}")
assert max_thrust == 21860  # correct puzzle solution
print("")

# ---- Part 2 ----


def run_amplifier_feedback_loop(
    intcode: Intcode, phase_sequence: AmplifierPhaseSequence
) -> int:
    value = 0
    amp_codes: dict[int, IntcodeComputer] = {
        i: IntcodeComputer(code=intcode.copy()) for i in range(len(phase_sequence))
    }
    halt = False

    for amp_i, phase in enumerate(phase_sequence):
        inputs = IntcodeInput([phase, value])
        int_comp = amp_codes[amp_i]
        res = int_comp(inputs=inputs)

        if res.output is not None:
            value = res.output

        if res.opcode is not None:
            int_comp.set_instruction_pointer(
                res.instruction_pointer + res.opcode.n_params + 1
            )

    while not halt:
        for amp_i in range(len(phase_sequence)):
            inputs = IntcodeInput([value])
            int_comp = amp_codes[amp_i]
            res = int_comp(inputs=inputs)

            if res.output is not None:
                value = res.output

            if res.opcode is not None:
                int_comp.set_instruction_pointer(
                    res.instruction_pointer + res.opcode.n_params + 1
                )

            if res.instruction.opcode_value == 99:
                halt = True

    return value


# Test input.
test_intcode_str = """
3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5
"""
test_intcode = Intcode([int(x) for x in test_intcode_str.strip().split(",")])
test_input_seq = [9, 8, 7, 6, 5]
test_output = 139629729
test_res = run_amplifier_feedback_loop(test_intcode, test_input_seq)
assert test_res == test_output
res_phase_seq, res_max_thrust = find_fastest_phase_sequence(
    test_intcode, amp_method=run_amplifier_feedback_loop, amp_phases=list(range(5, 10))
)
assert all([a == b for a, b in zip(test_input_seq, res_phase_seq)])
assert res_max_thrust == test_output

# Puzzle input
best_phase_seq, max_thrust = find_fastest_phase_sequence(
    intcode_program.copy(),
    amp_method=run_amplifier_feedback_loop,
    amp_phases=list(range(5, 10)),
)
print("(part 2) Feedback Loop method results:")
print(f"  sequence {best_phase_seq}")
print(f"  max thrust of {max_thrust}")
assert max_thrust == 2645740  # correct puzzle solution
