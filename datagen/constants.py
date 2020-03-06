# -*- coding: utf-8 -*-

from sympy import *

__all__ = [
    "Sub",
    "Div",
    "x",
    "y",
    "terminals",
    "binary_operations",
    "unary_operations",
    "max_internal_node_size",
    "symbol_to_unary_operation",
    "symbol_to_binary_operation",
    "unary_list",
    "binary_list",
]


def Sub(arg1, arg2):
    return Add(arg1, -arg2)


def Div(arg1, arg2):
    return Mul(arg1, 1 / arg2)


x, y = symbols("x y", positive=True, nonzero=True, real=True)

# for output data
terminals = set([x, S(-5), S(-4), S(-3), S(-2), S(-1), S(1), S(2), S(3), S(4), S(5)])
binary_operations = set([Add, Sub, Mul, Div])
unary_operations = set(
    [
        exp,
        log,
        sqrt,
        sin,
        cos,
        tan,
        asin,
        acos,
        atan,
        sinh,
        cosh,
        tanh,
        asinh,
        acosh,
        atanh,
    ]
)

max_internal_node_size = 15

# operation_name_to_symbol = {
#     "Add": "+",
#     "Sub": "-",
#     "Mul": "*",
#     "Div": "/",
# }

# for input data
symbol_to_unary_operation = {
    "Abs": Abs,
    "exp": exp,
    "log": log,
    "sqrt": sqrt,
    "sin": sin,
    "cos": cos,
    "tan": tan,
    "asin": asin,
    "acos": acos,
    "atan": atan,
    "sinh": sinh,
    "cosh": cosh,
    "tanh": tanh,
    "asinh": asinh,
    "acosh": acosh,
    "atanh": atanh,
}

symbol_to_binary_operation = {
    "+": Add,
    "-": Sub,
    "*": Mul,
    "/": Div,
    "**": Pow,
}


unary_list = list(reversed(sorted(symbol_to_unary_operation.keys())))
binary_list = list(reversed(sorted(symbol_to_binary_operation.keys())))
