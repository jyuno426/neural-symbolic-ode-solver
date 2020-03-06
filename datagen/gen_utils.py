# -*- coding: utf-8 -*-

from .constants import *
from .tree import *
from .node import *
from sympy import *
import numpy as np

__all__ = [
    "generate_random_tree",
    "traverse_in_preorder",
    "match_prefix",
    "separate_constant_term",
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

    return res


def match_prefix(sentence, candidates):
    prefix = None
    for candidate in candidates:
        if sentence.startswith(candidate):
            prefix = candidate
            break
    assert prefix is not None
    return prefix


def separate_constant_term(expr, var=None):
    if var is None:
        return expr
    else:
        return expr.as_independent(var, as_Add=True)
