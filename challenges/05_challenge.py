#!/usr/bin/env python3

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Protocol, runtime_checkable


class UnknownOperationException(BaseException):
    pass


class UnknownParameterModeException(BaseException):
    pass


class FailedThermalEnvironmentSupervisionTerminalDiagnostic(BaseException):
    pass


Code = list[int]
ParameterModes = tuple[int, int, int]


@dataclass
class OperationResult:
    output: Optional[int]
    instruction_pointer: Optional[int]

    def __str__(self) -> str:
        return f"output: {self.output}  ptr: {self.instruction_pointer}"


@runtime_checkable
class Opcode(Protocol):
    def __call__(self, code: Code, input_val: int, inst_ptr: int) -> OperationResult:
        ...

    @property
    def n_params(self) -> int:
        ...


class Opcode1(Opcode):

    a: int
    b: int
    out_pos: int

    def __init__(self, a: int, b: int, out_pos: int) -> None:
        self.a = a
        self.b = b
        self.out_pos = out_pos
        return None

    def __call__(self, code: Code, input_val: int, inst_ptr: int) -> OperationResult:
        code[self.out_pos] = self.a + self.b
        return OperationResult(None, None)

    @property
    def n_params(self) -> int:
        return 3

    def __str__(self) -> str:
        return f"op1 - a: {self.a}, b: {self.b} -> out: {self.out_pos}"


class Opcode2(Opcode):

    a: int
    b: int
    out_pos: int

    def __init__(self, a: int, b: int, out_pos: int) -> None:
        self.a = a
        self.b = b
        self.out_pos = out_pos
        return None

    def __call__(self, code: Code, input_val: int, inst_ptr: int) -> OperationResult:
        code[self.out_pos] = self.a * self.b
        return OperationResult(None, None)

    @property
    def n_params(self) -> int:
        return 3

    def __str__(self) -> str:
        return f"op2 - a: {self.a}, b: {self.b} -> out: {self.out_pos}"


class Opcode3(Opcode):

    out_pos: int

    def __init__(self, out_pos: int) -> None:
        self.out_pos = out_pos
        return None

    def __call__(self, code: Code, input_val: int, inst_ptr: int) -> OperationResult:
        code[self.out_pos] = input_val
        return OperationResult(None, None)

    @property
    def n_params(self) -> int:
        return 1

    def __str__(self) -> str:
        return f"op3 -> out: {self.out_pos}"


class Opcode4(Opcode):

    a: int

    def __init__(self, a: int) -> None:
        self.a = a
        return None

    def __call__(self, code: Code, input_val: int, inst_ptr: int) -> OperationResult:
        return OperationResult(self.a, None)

    @property
    def n_params(self) -> int:
        return 1

    def __str__(self) -> str:
        return f"op4 - a: {self.a}"


class Opcode5(Opcode):

    a: int
    b: int

    def __init__(self, a: int, b: int) -> None:
        self.a = a
        self.b = b
        return None

    def __call__(self, code: Code, input_val: int, inst_ptr: int) -> OperationResult:
        return OperationResult(None, self.b if self.a != 0 else None)

    @property
    def n_params(self) -> int:
        return 2

    def __str__(self) -> str:
        return f"op5 - a: {self.a}, b{self.b}"


class Opcode6(Opcode):

    a: int
    b: int

    def __init__(self, a: int, b: int) -> None:
        self.a = a
        self.b = b
        return None

    def __call__(self, code: Code, input_val: int, inst_ptr: int) -> OperationResult:
        return OperationResult(None, self.b if self.a == 0 else None)

    @property
    def n_params(self) -> int:
        return 2

    def __str__(self) -> str:
        return f"op6 - a: {self.a}, b{self.b}"


class Opcode7(Opcode):

    a: int
    b: int
    out_pos: int

    def __init__(self, a: int, b: int, out_pos: int) -> None:
        self.a = a
        self.b = b
        self.out_pos = out_pos
        return None

    def __call__(self, code: Code, input_val: int, inst_ptr: int) -> OperationResult:
        code[self.out_pos] = 1 if self.a < self.b else 0
        return OperationResult(None, None)

    @property
    def n_params(self) -> int:
        return 3

    def __str__(self) -> str:
        return f"op7 - a: {self.a}, b{self.b}"


class Opcode8(Opcode):

    a: int
    b: int
    out_pos: int

    def __init__(self, a: int, b: int, out_pos: int) -> None:
        self.a = a
        self.b = b
        self.out_pos = out_pos
        return None

    def __call__(self, code: Code, input_val: int, inst_ptr: int) -> OperationResult:
        code[self.out_pos] = 1 if self.a == self.b else 0
        return OperationResult(None, None)

    @property
    def n_params(self) -> int:
        return 3

    def __str__(self) -> str:
        return f"op8 - a: {self.a}, b{self.b} -> out: {self.out_pos}"


class Opcode99(Opcode):
    def __call__(self, code: Code, input_val: int, inst_ptr: int) -> OperationResult:
        return OperationResult(None, inst_ptr)

    @property
    def n_params(self) -> int:
        return 0

    def __str__(self) -> str:
        return "op99"


def make_opcode(
    op: int, params: list[int], code: Code, modes: ParameterModes
) -> Opcode:

    opcode_values: list[int] = []
    for param, mode in zip(params[:-1], modes[:-1]):
        if mode == 0:
            opcode_values.append(code[param])
        elif mode == 1:
            opcode_values.append(param)
        else:
            UnknownParameterModeException(mode)
        if op in {3, 4, 99}:
            break

    if op == 1:
        return Opcode1(a=opcode_values[0], b=opcode_values[1], out_pos=params[2])
    elif op == 2:
        return Opcode2(a=opcode_values[0], b=opcode_values[1], out_pos=params[2])
    elif op == 3:
        return Opcode3(out_pos=params[0])
    elif op == 4:
        return Opcode4(a=opcode_values[0])
    elif op == 5:
        return Opcode5(a=opcode_values[0], b=opcode_values[1])
    elif op == 6:
        return Opcode6(a=opcode_values[0], b=opcode_values[1])
    elif op == 7:
        return Opcode7(a=opcode_values[0], b=opcode_values[1], out_pos=params[2])
    elif op == 8:
        return Opcode8(a=opcode_values[0], b=opcode_values[1], out_pos=params[2])
    elif op == 99:
        return Opcode99()
    else:
        raise UnknownOperationException(op)


class Instruction:

    instruction: str
    opcode_value: int
    modes: tuple[int, int, int]

    def __init__(self, instruction: int) -> None:
        self.instruction = str(instruction).rjust(5, "0")
        self.opcode_value = int(self.instruction[-2:])
        _modes = [int(m) for m in self.instruction[:3]]
        assert len(_modes) == 3
        assert all([m in {0, 1} for m in _modes])
        self.modes = _modes[2], _modes[1], _modes[0]
        return None

    def __str__(self) -> str:
        return f"[{self.instruction}] - op: {self.opcode_value}  modes: {self.modes}"


def run_opcode(code: Code, sys_input: int) -> Optional[int]:
    inst_ptr = 0
    output: Optional[int] = None
    nonzero_output: bool = False
    while True:
        instruction = Instruction(code[inst_ptr])
        if instruction.opcode_value == 99:
            print("found completion operation (op 99)")
            break

        if nonzero_output:
            raise FailedThermalEnvironmentSupervisionTerminalDiagnostic(output)

        params = code[inst_ptr + 1 : inst_ptr + 4]
        assert len(params) == len(instruction.modes) == 3
        operation = make_opcode(
            instruction.opcode_value, params=params, code=code, modes=instruction.modes
        )

        op_res = operation(code=code, input_val=sys_input, inst_ptr=inst_ptr)
        if op_res.output is not None:
            output = op_res.output
            if output == 0:
                print(f" successful diagnostic (instruction {inst_ptr})")
            else:
                nonzero_output = True

        if op_res.instruction_pointer is not None:
            inst_ptr = op_res.instruction_pointer
        else:
            inst_ptr += operation.n_params + 1

    return output


puzzle_input: Code = []
with open(Path("data", "05", "input.txt"), "r") as file:
    for line in file:
        puzzle_input += [int(x) for x in line.strip().split(",")]

opcode_out = run_opcode(puzzle_input.copy(), sys_input=1)
print(f"(part 1) output: {opcode_out}")

opcode_out = run_opcode(puzzle_input.copy(), sys_input=5)
print(f"(part 2) output: {opcode_out}")
