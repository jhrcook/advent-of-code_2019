"""Test Intcode computer."""

import intcode
from intcode import Intcode, IntcodeInput


def test_opcode1() -> None:
    op1 = intcode.Opcode1(3, 8, 3)
    code = [-1, -1, -1, -1]
    inputs = IntcodeInput([-1, -2, -3])
    res = op1(Intcode(code), inputs, 0)

    assert res.output is None
    assert res.instruction_pointer is None
    assert code == [-1, -1, -1, 11]
    assert inputs._values == [-1, -2, -3]


def test_opcode9() -> None:
    op = intcode.Opcode9(10)
    res = op(code=Intcode(), inputs=IntcodeInput([]), inst_ptr=0)
    assert res.instruction_pointer is None
    assert res.output is None
    assert res.relative_base == 10
