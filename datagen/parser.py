# -*- coding: utf-8 -*-

from utility import *
from .constants import *
from .gen_utils import *
from .node import *
from .tree import *
from sympy import *
import warnings

__all__ = ["parse_raw_integration_data", "parse_integration_data"]

warnings.filterwarnings("error")


def parse_raw_integration_data():
    while True:
        try:
            with time_limit(5):
                tree = Tree(random_generate=True, always_valid=True)
                input_string = tree.get_simplified_derivative()
                output_string = tree.get_simplified_without_constant()
            break
        except TimeoutException:
            # print("\rTimed out! Restart!\n")
            continue
        except Exception as e:
            # print("\rException occured:", e, "\n")
            continue

    return [input_string, output_string]


def parse_integration_data(input_string, output_string):
    return [
        str(Tree(parse_simplified_string_expression_into_tree(input_string))),
        str(Tree(parse_simplified_string_expression_into_tree(output_string))),
    ]


def parse_simplified_string_expression_into_tree(string_expression):
    # print(string_expression)
    root = Node()

    node = root
    # don't use root variable from here until return

    # If there's minus sign in simplified string_expression,
    # it always appear at the front
    minus = False
    if string_expression[0] == "-":
        minus = True
        string_expression = string_expression[1:]

    n = len(string_expression)

    # Find candidate binary operations------------------------------
    i = 0
    cnt = 0
    pos = []
    orders = []
    operations = []

    while i < n:
        s = string_expression[i]
        if s == "(":
            cnt += 1
        elif s == ")":
            cnt -= 1
        elif cnt == 0:
            if i + 1 < n and string_expression[i : i + 2] == "**":
                pos.append(i)
                orders.append(2)
                operations.append("**")
                i += 1
            elif s == "*" or s == "/":
                pos.append(i)
                orders.append(1)
                operations.append(s)
            elif s == "+" or s == "-":
                pos.append(i)
                orders.append(0)
                operations.append(s)
        i += 1
    # --------------------------------------------------------------

    if len(pos) == 0:
        # binary doesn't exist

        s = string_expression[0]
        if s == "(":
            # ()
            # print("par: ", string_expression)
            assert string_expression[-1] == ")"
            if minus:
                node.set(Mul)
                node.add_child(data=S(-1))
                node.add_child(
                    node=parse_simplified_string_expression_into_tree(
                        string_expression[1:-1]
                    )
                )
            else:
                return parse_simplified_string_expression_into_tree(
                    string_expression[1:-1]
                )
        elif s == "x":
            # x
            # print("variable: ", string_expression)
            assert len(string_expression) == 1

            if minus:
                node.set(Mul)
                node.add_child(data=S(-1))
                node.add_child(data=x)
            else:
                node.set(x)
        elif string_expression[:2] == "pi":
            # pi
            # print("const: ", string_expression)
            assert len(string_expression) == 2

            if minus:
                node.set(Mul)
                node.add_child(data=S(-1))
                node.add_child(data=pi)
            else:
                node.set(pi)
        elif s == "E":
            # E
            # print("const: ", string_expression)
            assert len(string_expression) == 1

            if minus:
                node.set(Mul)
                node.add_child(data=S(-1))
                node.add_child(data=E)
            else:
                node.set(E)
        elif s in "0123456789":
            # num
            # print("num:", string_expression, len(string_expression))
            assert len(string_expression) == len(
                [c for c in string_expression if c in "0123456789"]
            )

            if minus:
                node.set(S(-int(string_expression)))
            else:
                node.set(S(int(string_expression)))
        else:
            # unary
            op = match_prefix(string_expression, unary_list)
            # print("unary: ", op)
            assert string_expression[len(op)] == "(" and string_expression[-1] == ")"

            if minus:
                node.set(Mul)
                node.add_child(data=S(-1))
                node = node.add_child(data=symbol_to_unary_operation[op])
                node.add_child(
                    node=parse_simplified_string_expression_into_tree(
                        string_expression[len(op) + 1 : -1]
                    )
                )
            else:
                node.set(symbol_to_unary_operation[op])
                node.add_child(
                    node=parse_simplified_string_expression_into_tree(
                        string_expression[len(op) + 1 : -1]
                    )
                )
    else:
        # binary exists

        i = 0
        while i < 3:
            try:
                idx = orders.index(i)
            except:
                idx = None

            if idx is not None:
                op = operations[idx]
                p = pos[idx]

                # print("binary: ", op)

                node.set(symbol_to_binary_operation[op])

                # left child
                if minus:
                    node.add_child(
                        node=parse_simplified_string_expression_into_tree(
                            "-" + string_expression[:p]
                        )
                    )
                else:
                    node.add_child(
                        node=parse_simplified_string_expression_into_tree(
                            string_expression[:p]
                        )
                    )

                # right child
                node.add_child(
                    node=parse_simplified_string_expression_into_tree(
                        string_expression[p + len(op) :]
                    )
                )

                break  # if success
            i += 1

        assert i < 3

    # print("root:", root, ", children:", [str(child) for child in root.children])
    return root
