"""Intcode computer."""
from __future__ import annotations

from dataclasses import dataclass
from typing import (
    Any,
    Iterable,
    Optional,
    Protocol,
    SupportsIndex,
    Union,
    overload,
    runtime_checkable,
)


class UnknownOperationException(BaseException):
    pass


class UnknownParameterModeException(BaseException):
    pass


class FailedThermalEnvironmentSupervisionTerminalDiagnostic(BaseException):
    pass


ParameterModes = tuple[int, int, int]


class Intcode(list[int]):
    @overload
    def __getitem__(self, i: SupportsIndex) -> int:
        ...

    @overload
    def __getitem__(self, i: slice) -> list[int]:
        ...

    def __getitem__(self, i: Union[SupportsIndex, slice]) -> Union[int, list[int]]:
        self._extend_based_on_index(i)
        return super().__getitem__(i)

    def _ensure_length_atleast(self, x: int) -> None:
        if x >= len(self):
            self.extend([0] * (x + 1 - len(self)))

    def _extend_based_on_index(self, i: Union[SupportsIndex, slice]) -> None:
        if isinstance(i, SupportsIndex):
            self._ensure_length_atleast(x=int(i))
        elif isinstance(i, slice):
            x = max([a for a in (i.start, i.stop, i.stop) if a is not None])
            self._ensure_length_atleast(x=x)

    @overload
    def __setitem__(self, i: SupportsIndex, o: int) -> None:
        ...

    @overload
    def __setitem__(self, s: slice, o: Iterable[int]) -> None:
        ...

    def __setitem__(self, *args: Any) -> None:
        assert len(args) == 2
        idx = args[0]
        if isinstance(idx, (SupportsIndex, slice)):
            self._extend_based_on_index(idx)

        super().__setitem__(*args)
        return None

    def __copy__(self) -> Intcode:
        return Intcode(super().copy())

    def copy(self) -> Intcode:
        return self.__copy__()


class IntcodeInput:

    _values: list[int]

    def __init__(self, values: list[int]) -> None:
        self._values = values

    def get(self) -> int:
        return self._values.pop(0)

    def put(self, value: int) -> None:
        self._values.append(value)
        return None


@dataclass
class OperationResult:

    output: Optional[int] = None
    instruction_pointer: Optional[int] = None
    relative_base: Optional[int] = None

    def __str__(self) -> str:
        return f"output: {self.output}  ptr: {self.instruction_pointer}"


@runtime_checkable
class Opcode(Protocol):
    def __call__(
        self, code: Intcode, inputs: IntcodeInput, inst_ptr: int
    ) -> OperationResult:
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

    def __call__(
        self, code: Intcode, inputs: IntcodeInput, inst_ptr: int
    ) -> OperationResult:
        code[self.out_pos] = self.a + self.b
        return OperationResult()

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

    def __call__(
        self, code: Intcode, inputs: IntcodeInput, inst_ptr: int
    ) -> OperationResult:
        code[self.out_pos] = self.a * self.b
        return OperationResult()

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

    def __call__(
        self, code: Intcode, inputs: IntcodeInput, inst_ptr: int
    ) -> OperationResult:
        code[self.out_pos] = inputs.get()
        return OperationResult()

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

    def __call__(
        self, code: Intcode, inputs: IntcodeInput, inst_ptr: int
    ) -> OperationResult:
        return OperationResult(output=self.a)

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

    def __call__(
        self, code: Intcode, inputs: IntcodeInput, inst_ptr: int
    ) -> OperationResult:
        return OperationResult(instruction_pointer=self.b if self.a != 0 else None)

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

    def __call__(
        self, code: Intcode, inputs: IntcodeInput, inst_ptr: int
    ) -> OperationResult:
        return OperationResult(instruction_pointer=self.b if self.a == 0 else None)

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

    def __call__(
        self, code: Intcode, inputs: IntcodeInput, inst_ptr: int
    ) -> OperationResult:
        code[self.out_pos] = 1 if self.a < self.b else 0
        return OperationResult()

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

    def __call__(
        self, code: Intcode, inputs: IntcodeInput, inst_ptr: int
    ) -> OperationResult:
        code[self.out_pos] = 1 if self.a == self.b else 0
        return OperationResult()

    @property
    def n_params(self) -> int:
        return 3

    def __str__(self) -> str:
        return f"op8 - a: {self.a}, b{self.b} -> out: {self.out_pos}"


class Opcode9(Opcode):

    a: int

    def __init__(self, a: int) -> None:
        self.a = a
        return None

    def __call__(
        self, code: Intcode, inputs: IntcodeInput, inst_ptr: int
    ) -> OperationResult:
        return OperationResult(relative_base=self.a)

    @property
    def n_params(self) -> int:
        return 1

    def __str__(self) -> str:
        return f"op9 - a: {self.a}"


class Opcode99(Opcode):
    def __call__(
        self, code: Intcode, inputs: IntcodeInput, inst_ptr: int
    ) -> OperationResult:
        return OperationResult(None, inst_ptr)

    @property
    def n_params(self) -> int:
        return 0

    def __str__(self) -> str:
        return "op99"


def make_opcode(
    op: int, params: list[int], code: Intcode, modes: ParameterModes, rel_base: int
) -> Opcode:

    if op not in set(list(range(1, 10)) + [99]):
        raise UnknownOperationException(op)

    opcode_values: list[int] = []
    for param, mode in zip(params[:-1], modes[:-1]):
        if mode == 0:
            opcode_values.append(code[param])
        elif mode == 1:
            opcode_values.append(param)
        elif mode == 2:
            opcode_values.append(code[param + rel_base])
        else:
            UnknownParameterModeException(mode)
        if op in {3, 4, 9, 99}:
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
    elif op == 9:
        return Opcode9(a=opcode_values[0])
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
        assert all([m in {0, 1, 2} for m in _modes])
        self.modes = _modes[2], _modes[1], _modes[0]
        return None

    def __str__(self) -> str:
        return f"[{self.instruction}] - op: {self.opcode_value}  modes: {self.modes}"


@dataclass
class IntcodeResult:
    instruction_pointer: int
    output: Optional[int]
    instruction: Instruction
    opcode: Optional[Opcode]

    def __str__(self) -> str:
        s = "Intruction Result:\n"
        s += f" instruction pointer: {self.instruction_pointer}\n"
        s += f" instruction: {self.instruction}\n"

        if self.output is None:
            s += " output: [None]\n"
        else:
            s += f" output: {self.output}\n"

        if self.opcode is None:
            s += " opcode: [None]\n"
        else:
            s += f" opcode: {self.opcode}\n"
        return s


class IntcodeComputer:

    code: Intcode
    _verbose: bool
    _instr_ptr: int
    _relative_base: int

    def __init__(self, code: Intcode, verbose: bool = False) -> None:
        self.code = code
        self._verbose = verbose
        self._instr_ptr = 0
        self._relative_base = 0

    def _update_instruction_pointer(self, op: Opcode, op_res: OperationResult) -> None:
        if op_res.instruction_pointer is not None:
            self._instr_ptr = op_res.instruction_pointer
        else:
            self._instr_ptr += op.n_params + 1

    def __call__(self, inputs: Optional[IntcodeInput] = None) -> IntcodeResult:
        if inputs is None:
            inputs = IntcodeInput([])
        output: Optional[int] = None
        operation: Optional[Opcode] = None
        while True:
            instruction = Instruction(self.code[self._instr_ptr])
            if self._verbose:
                print(f"instruction: {instruction}")

            if instruction.opcode_value == 99:
                if self._verbose:
                    print("found completion operation (op 99)")
                break

            params = self.code[(self._instr_ptr + 1) : (self._instr_ptr + 4)]
            operation = make_opcode(
                instruction.opcode_value,
                params=params,
                code=self.code,
                modes=instruction.modes,
                rel_base=self._relative_base,
            )
            op_res = operation(code=self.code, inputs=inputs, inst_ptr=self._instr_ptr)
            if op_res.output is not None:
                output = op_res.output
                break

            self._update_instruction_pointer(op=operation, op_res=op_res)

        return IntcodeResult(
            instruction_pointer=self._instr_ptr,
            output=output,
            instruction=instruction,
            opcode=operation,
        )

    def set_instruction_pointer(self, new_ptr: int) -> None:
        assert new_ptr >= 0
        self._instr_ptr = new_ptr
        return None
