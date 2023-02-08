from enum import Flag


def op_and(left: bool, right: bool) -> bool:
    return left and right


def op_or(left: bool, right: bool) -> bool:
    return left or right


def op_bitwise_or(left: Flag, right: Flag) -> Flag:
    return left | right
