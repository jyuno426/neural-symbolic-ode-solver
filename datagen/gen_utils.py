# -*- coding: utf-8 -*-

from utility import *
from .constants import *
from .node import *
from sympy import *
import numpy as np

__all__ = [
    "generate_random_tree",
    "traverse_in_preorder",
    "match_prefix",
    "separate_constant_term",
    "is_real",
    "solve_by_symb",
    "simplify_coefficient",
    "standard_to_tree",
]

# dp table for tree_count
tree_count_table = [
    [-1 for j in range(max_internal_node_size + 2)]
    for i in range(max_internal_node_size + 2)
]


def tree_count(empty_node_count, internal_node_count):
    """
    Calculate the number of tree representations in terms of
    combinations of terminals, unary and binary operations defiend in constants.py.
    @params{
        empty_node_count:       # of empty nodes wating to be allocated.
        internal_node_count:    # of internal_nodes not determined yet.
    }
    """

    enc = empty_node_count
    inc = internal_node_count
    l_t = len(terminals)
    l_u = len(unary_operations)
    l_b = len(binary_operations)

    assert enc >= 0 and inc >= 0

    if tree_count_table[enc][inc] == -1:
        # if dp value is not set yet
        if inc == 0:
            tree_count_table[enc][inc] = l_t ** enc

        elif enc == 0:
            tree_count_table[enc][inc] = 0

        else:
            c_t = l_t * tree_count(enc - 1, inc)
            c_u = l_u * tree_count(enc, inc - 1)
            c_b = l_b * tree_count(enc + 1, inc - 1)

            tree_count_table[enc][inc] = c_t + c_u + c_b

    return tree_count_table[enc][inc]


def sample_intenral_node_size():
    """
    Sample internal_node_size uniformly in [1, max_internal_node_size].
    "uniformly" means combinatorial uniformness according to tree_count
    """
    node_size_list = range(1, max_internal_node_size)
    probs = [tree_count(1, node_size) for node_size in node_size_list]
    probs_sum = sum(probs)
    probs = [p / probs_sum for p in probs]
    return np.random.choice(node_size_list, p=probs)


def generate_random_tree(internal_node_size=None):
    """
    Generate random tree (math-expression) uniformly which consists of
    terminals, unary and binary operations defiend in constants.py.
    Returns its root node of type Node.
    "uniformly" means combinatorial uniformness
    @params{
        internal_node_size:     # of operations in expression
    }
    """

    root = Node()
    empty_node_list = [root]

    if internal_node_size is None:
        internal_node_count = sample_intenral_node_size()
    else:
        internal_node_count = internal_node_size

    while len(empty_node_list) + internal_node_count > 0:
        assert internal_node_count >= 0

        total_count = tree_count(len(empty_node_list), internal_node_count)

        # sampling
        nodes, probs = [], []

        for v in terminals:
            count = tree_count(len(empty_node_list) - 1, internal_node_count)
            probs.append(count / total_count)
            nodes.append({"data": v, "child_count": 0})

        if internal_node_count > 0:
            for v in unary_operations:
                count = tree_count(len(empty_node_list), internal_node_count - 1)
                probs.append(count / total_count)
                nodes.append({"data": v, "child_count": 1})

            for v in binary_operations:
                count = tree_count(len(empty_node_list) + 1, internal_node_count - 1)
                probs.append(count / total_count)
                nodes.append({"data": v, "child_count": 2})

        sampled_node = np.random.choice(nodes, p=probs)

        selected_empty_node = empty_node_list.pop(
            np.random.choice(range(len(empty_node_list)))
        )

        selected_empty_node.set(sampled_node["data"])
        for _ in range(sampled_node["child_count"]):
            empty_node_list.append(selected_empty_node.add_child())

        if sampled_node["child_count"] > 0:
            internal_node_count -= 1

    return root


def traverse_in_preorder(node):
    """
    Traverse the tree in preorder, which has the given "node" as its root.
    """
    # print("traverse:", node)
    assert type(node) is Node

    res = [node]
    for child in node.children:
        res += traverse_in_preorder(child)
        node.symbols.update(child.symbols)

    if node.is_leaf() and node.data in [x, c1, c2]:
        node.symbols.add(node.data)

    return res


def match_prefix(sentence, candidates):
    prefix = None
    for candidate in candidates:
        if sentence.startswith(candidate):
            prefix = candidate
            break
    if prefix is None:
        # print("It contains", sentence, "\n")
        raise Exception("match_prefix error")
    else:
        return prefix


def separate_constant_term(expr, var=None):
    if var is None:
        return expr
    else:
        return expr.as_independent(*var, as_Add=True)


def is_real(expr):
    try:
        ftn = lambdify(x, expr, "numpy")
    except:
        return False

    numeric = 0.12345
    while numeric < 1000:
        try:
            value = ftn(numeric)
            if np.isfinite(value) and np.isreal(value):
                return True
        except:
            pass
        numeric = numeric * 10

    return False


def simplify_coefficient(expr, const, var):
    c_str = str(const)

    if c_str in normalize(expr):
        res = S(0)
        for term, coeff in expr.as_coefficients_dict().items():
            if c_str in normalize(coeff):
                res = Add(res, Mul(c1, term))
            elif c_str in normalize(term):
                coeff2, term2 = term.as_independent(var, as_Mul=True)
                if c_str in normalize(coeff2):
                    res = Add(res, Mul(c1, term2))
                else:
                    res = Add(res, Mul(coeff, term))
            else:
                res = Add(res, Mul(coeff, term))
        return res
    else:
        return expr


def solve_by_symb(expr, symb):
    root = standard_to_tree(normalize(expr))
    # for kk in traverse_in_preorder(root):
    #     print(kk)
    traverse_in_preorder(root)

    assert symb in root.symbols

    node = root

    exp = S(0)
    while node.data != symb:
        assert symb in node.symbols

        if str(node) in inverse_mapping:
            exp = inverse_mapping[str(node)](exp)
            node = node.children[0]

        elif node.data == Add:
            left = node.children[0]
            right = node.children[1]
            if symb in left.symbols:
                exp = Sub(exp, right.get_sympy_exp())
                node = left
            else:
                exp = Sub(exp, left.get_sympy_exp())
                node = right

        elif node.data == Sub:
            left = node.children[0]
            right = node.children[1]
            if symb in left.symbols:
                exp = Add(exp, right.get_sympy_exp())
                node = left
            else:
                exp = Sub(left.get_sympy_exp(), exp)
                node = right

        elif node.data == Mul:
            left = node.children[0]
            right = node.children[1]
            if symb in left.symbols:
                exp = Div(exp, right.get_sympy_exp())
                node = left
            else:
                exp = Div(exp, left.get_sympy_exp())
                node = right

        elif node.data == Div:
            left = node.children[0]
            right = node.children[1]
            if symb in left.symbols:
                exp = Mul(exp, right.get_sympy_exp())
                node = left
            else:
                exp = Div(left.get_sympy_exp(), exp)
                node = right

        else:
            raise Exception("solve error")

    return exp


def standard_to_tree(string_expression):
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
                operations.append("**")
                i += 1
            elif s in "+-*/":
                pos.append(i)
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
                node.add_child(node=standard_to_tree(string_expression[1:-1]))
            else:
                return standard_to_tree(string_expression[1:-1])
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
        elif s == "f":
            # f
            # print("function: ", string_expression)
            assert len(string_expression) == 1

            if minus:
                node.set(Mul)
                node.add_child(data=S(-1))
                node.add_child(data=f)
            else:
                node.set(f)
        elif s == "g":
            # g
            # print("function: ", string_expression)
            assert len(string_expression) == 1

            if minus:
                node.set(Mul)
                node.add_child(data=S(-1))
                node.add_child(data=g)
            else:
                node.set(g)
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
        elif string_expression[:2] == "c1":
            # pi
            # print("const: ", string_expression)
            assert len(string_expression) == 2

            if minus:
                node.set(Mul)
                node.add_child(data=S(-1))
                node.add_child(data=c1)
            else:
                node.set(c1)
        elif string_expression[:2] == "c2":
            # pi
            # print("const: ", string_expression)
            assert len(string_expression) == 2

            if minus:
                node.set(Mul)
                node.add_child(data=S(-1))
                node.add_child(data=c2)
            else:
                node.set(c2)
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
                    node=standard_to_tree(string_expression[len(op) + 1 : -1])
                )
            else:
                node.set(symbol_to_unary_operation[op])
                node.add_child(
                    node=standard_to_tree(string_expression[len(op) + 1 : -1])
                )
    else:
        # binary exists

        # calculate in reverse order
        pos.reverse()
        operations.reverse()

        check = False
        for op in ["+", "-", "*", "/", "**"]:
            try:
                # right most index
                p = pos[operations.index(op)]

                # set operation
                node.set(symbol_to_binary_operation[op])

                left = string_expression[:p]
                right = string_expression[p + len(op) :]

                # left child
                if minus:
                    node.add_child(node=standard_to_tree("-" + left))
                else:
                    node.add_child(node=standard_to_tree(left))

                # right child
                node.add_child(node=standard_to_tree(right))

                check = True
                break

            except:
                pass

        assert check

    # print("root:", root, ", children:", [str(child) for child in root.children])
    return root
