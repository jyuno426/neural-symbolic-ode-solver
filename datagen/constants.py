# -*- coding: utf-8 -*-

from sympy import *

__all__ = [
    "Sub",
    "Div",
    "square",
    "x",
    "f",
    "g",
    "h",
    "c1",
    "c2",
    "terminals",
    "binary_operations",
    "unary_operations",
    "inverse_mapping",
    "max_internal_node_size",
    "symbol_to_unary_operation",
    "symbol_to_binary_operation",
    "unary_list",
    "binary_list",
    "invalid_characters",
]


def Sub(arg1, arg2):
    return Add(arg1, -arg2)


def Div(arg1, arg2):
    return Mul(arg1, 1 / arg2)


def square(arg1):
    return Mul(arg1, arg1)


x = Symbol("x", positive=True, nonzero=True, real=True)
c1, c2 = symbols("c1 c2", real=True)
f = Function("f")(x)
g = Function("g")(x)
h = Function("h")(x)

# for output data
terminals = set([x, S(-5), S(-4), S(-3), S(-2), S(-1), S(1), S(2), S(3), S(4), S(5)])
binary_operations = set([Add, Sub, Mul, Div])
unary_operations = set(
    [
        exp,
        log,
        sqrt,
        # square,
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

inverse_mapping = {
    "exp": log,
    "log": exp,
    "sqrt": square,
    # "square": sqrt,
    "sin": asin,
    "cos": acos,
    "tan": atan,
    "asin": sin,
    "acos": cos,
    "atan": tan,
    "sinh": asinh,
    "cosh": acosh,
    "tanh": atanh,
    "asinh": sinh,
    "acosh": cosh,
    "atanh": tanh,
}

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

invalid_characters = ["oo", "I", "Dummy", "nan", "zoo"]
