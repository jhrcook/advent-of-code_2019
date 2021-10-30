#!/usr/bin/env python3

from itertools import permutations
from pathlib import Path
from typing import Sequence

from challenge_05 import Code, run_opcode

AmplifierPhaseSequence = Sequence[int]

intcode_program: Code = []
with open(Path("data", "07", "input.txt"), "r") as file:
    for line in file:
        intcode_program += [int(x) for x in line.strip().split(",")]


def run_amplifier_series(intcode: Code, phase_sequence: AmplifierPhaseSequence) -> int:
    value = 0
    for phase in phase_sequence:
        inputs = [phase, value]
        output = run_opcode(code=intcode.copy(), inputs=inputs, verbose=False)
        assert len(inputs) == 0
        assert output is not None
        value = output
    return value


def find_fastest_phase_sequence(
    intcode: Code, n_amps: int = 5
) -> tuple[AmplifierPhaseSequence, int]:
    best_phase_seq: AmplifierPhaseSequence = []
    max_thrust = -1
    for phase_sequence in permutations(list(range(n_amps))):
        amp_thrust = run_amplifier_series(intcode.copy(), phase_sequence=phase_sequence)
        if amp_thrust > max_thrust:
            max_thrust = amp_thrust
            best_phase_seq = list(phase_sequence)
    assert len(best_phase_seq) == n_amps
    return best_phase_seq, max_thrust


test_intcode = [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0]
test_input_seq = [4, 3, 2, 1, 0]
test_output = 43210
test_res = run_amplifier_series(test_intcode, test_input_seq)
assert test_res == test_output
res_phase_seq, res_max_thrust = find_fastest_phase_sequence(test_intcode, n_amps=5)
assert all([a == b for a, b in zip(test_input_seq, res_phase_seq)])
assert res_max_thrust == test_output


phase_seq, max_thrust = find_fastest_phase_sequence(intcode_program, n_amps=5)
print(f"(part 1) with sequence {phase_seq}, max thrust of {max_thrust}")
