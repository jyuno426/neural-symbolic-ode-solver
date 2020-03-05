# -*- coding: utf-8 -*-

# from .constants import *
from .tree import *
from .node import *
from .constants import *
from sympy import *
import numpy as np

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
    assert type(node) is Node

    res = [node]
    for child in node.children:
        res += traverse_in_preorder(child)

    return res


# def tree_to_simplified_tree(tree):
#     """
#     """
#     assert type(tree) is Tree

#     string_exp = str(simplify(tree.get_simpy_exp())).replace(" ", "")


def match_prefix(sentence, candidates):
    try:
        prefix = None
        for candidate in candidates:
            if sentence.startswith(candidate):
                prefix = candidate
                break
        assert prefix is not None
    except AssertionError:
        print("sentence:", sentence)
        print("candidates:", [str(candidate) for candidate in candidates])
        print("Holy")
        assert 0 == 1
    return prefix


# def find_par_pair(sentence, s):
#     n = len(sentence)
#     assert s < n

#     e = s
#     cnt = 0
#     while e < n:
#         c = sentence[i]
#         if c == "(":
#             cnt += 1
#         elif c == ")":
#             cnt -= 1
#             if cnt == 0:
#                 break
#         e += 1

#     assert e < n
#     return e


def transform(string_expression):
    # print(string_expression)
    root = Node()

    node = root
    # don't use root variable from here until return

    minus = False
    if string_expression[0] == "-":
        minus = True
        string_expression = string_expression[1:]

    n = len(string_expression)

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

    if len(pos) == 0:
        s = string_expression[0]
        if s == "(":
            # ()
            assert string_expression[-1] == ")"

            # print("par: ", string_expression)
            if minus:
                node.set(Mul)
                node.add_child(S(-1))
                node.add_child(transform(string_expression[1:-1]))
            else:
                return transform(string_expression[1:-1])
        elif s == "x":
            # x
            assert len(string_expression) == 1
            # print("variable: ", string_expression)

            if minus:
                node.set(Mul)
                node.add_child(S(-1))
                node.add_child(x)
            else:
                node.set(x)
        elif string_expression[:2] == "pi":
            # pi
            assert len(string_expression) == 2
            # print("const: ", string_expression)

            if minus:
                node.set(Mul)
                node.add_child(S(-1))
                node.add_child(pi)
            else:
                node.set(pi)
        elif s == "E":
            # E
            assert len(string_expression) == 1
            # print("const: ", string_expression)

            if minus:
                node.set(Mul)
                node.add_child(S(-1))
                node.add_child(E)
            else:
                node.set(E)
        elif s in "0123456789":
            # num
            assert len(string_expression) == len(
                [c for c in string_expression if c in "0123456789"]
            )

            # print("num:", string_expression)
            if minus:
                node.set(Mul)
                node.add_child(S(-1))
                node.add_child(S(int(string_expression)))
            else:
                node.set(S(int(string_expression)))
        else:
            # unary
            op = match_prefix(string_expression, unary_list)
            assert string_expression[len(op)] == "(" and string_expression[-1] == ")"
            # print("unary: ", op)

            if minus:
                node.set(Mul)
                node.add_child(S(-1))
                node = node.add_child(symbol_to_unary_operation[op])
                node.add_child(transform(string_expression[len(op) + 1 : -1]))
            else:
                node.set(symbol_to_unary_operation[op])
                node.add_child(transform(string_expression[len(op) + 1 : -1]))
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
                    node.add_child(transform("-" + string_expression[:p]))
                else:
                    node.add_child(transform(string_expression[:p]))

                # right child
                node.add_child(transform(string_expression[p + len(op) :]))

                break  # if success
            i += 1

        assert i < 3

    return root

