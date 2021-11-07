"""Test Intcode computer."""

import intcode


def test_opcode1() -> None:
    op1 = intcode.Opcode1(3, 8, 3)
    code = [-1, -1, -1, -1]
    inputs = intcode.IntcodeInput([-1, -2, -3])
    res = op1(code, inputs, 0)

    assert res.output is None
    assert res.instruction_pointer is None
    assert code == [-1, -1, -1, 11]
    assert inputs._values == [-1, -2, -3]
