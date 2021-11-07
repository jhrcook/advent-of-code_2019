#!/usr/bin/env python3

from pathlib import Path
from typing import Optional

from intcode import (
    FailedThermalEnvironmentSupervisionTerminalDiagnostic,
    Intcode,
    IntcodeComputer,
    IntcodeInput,
)


def run_intcode_diagnostics(code: Intcode, inputs: IntcodeInput) -> Optional[int]:
    inst_ptr = 0
    output: Optional[int] = None
    nonzero_output: bool = False
    while True:
        comp = IntcodeComputer(code=code, verbose=True)
        comp.set_instruction_pointer(inst_ptr)
        res = comp(inputs=inputs)

        if res.instruction.opcode_value == 99:
            print("finished running intcode with diagnostics")
            break

        if nonzero_output:
            raise FailedThermalEnvironmentSupervisionTerminalDiagnostic(output)

        if res.output is not None:
            output = res.output
            if output == 0:
                print(f" successful diagnostic (instruction {inst_ptr})")
            else:
                nonzero_output = True

        assert res.opcode is not None
        inst_ptr = res.instruction_pointer + res.opcode.n_params + 1
    return output


if __name__ == "__main__":
    puzzle_input: Intcode = []
    with open(Path("data", "05", "input.txt"), "r") as file:
        for line in file:
            puzzle_input += [int(x) for x in line.strip().split(",")]

    opcode_out = run_intcode_diagnostics(puzzle_input.copy(), inputs=IntcodeInput([1]))
    print(f"(part 1) output: {opcode_out}")
    assert opcode_out == 6069343

    opcode_out = run_intcode_diagnostics(puzzle_input.copy(), inputs=IntcodeInput([5]))
    print(f"(part 2) output: {opcode_out}")
    assert opcode_out == 3188550
