"""Test Intcode computer."""

import intcode
from intcode import Intcode, IntcodeInput


def test_opcode1() -> None:
    op1 = intcode.Opcode1(3, 8, 3)
    code = Intcode([-1, -1, -1, -1])
    inputs = IntcodeInput([-1, -2, -3])
    res = op1(code, inputs, 0)

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


# ---- Intcode ----


def test_get_item_intcode() -> None:
    code = Intcode([9, 5, 1, 8, 11, 29])
    assert code[0] == 9
    assert code[3] == 8


def test_get_item_slice_intcode() -> None:
    code = Intcode([9, 5, 1, 8, 11, 29])
    assert code[0:1] == [9]
    assert code[3:] == [8, 11, 29]


def test_get_item_beyond_intcode() -> None:
    code = Intcode([9, 5, 1, 8, 11, 29])
    res = code[100]
    assert res == 0
    assert len(code) == 101


def test_set_item_intcode() -> None:
    code = Intcode([9, 5, 1, 8, 11, 29])
    code[1] = -3
    assert code[1] == -3


def test_set_item_beyond_intcode() -> None:
    code = Intcode([9, 5, 1, 8, 11, 29])
    code[100] = -3
    assert code[100] == -3
    assert len(code) == 101
