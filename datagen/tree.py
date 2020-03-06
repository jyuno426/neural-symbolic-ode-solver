# -*- coding: utf-8 -*-

from .constants import *
from .gen_utils import *
from .node import *
from sympy import *
import numpy as np

__all__ = ["Tree"]


class Tree(object):
    def __init__(
        self,
        root=None,
        random_generate=False,
        internal_node_size=None,
        always_valid=False,
    ):
        self.simplified_exp = None
        if random_generate:
            # self.root = Node(x)
            self.root = generate_random_tree()
            if always_valid:
                while not self.is_valid():
                    self.root = generate_random_tree()
        else:
            # Make sure that root is valid node
            assert type(root) is Node
            self.root = root

    def is_valid(self):
        """
        Check validity of expression whether it contains invalid value (complex value or infinity or nan or undefined)
        """
        return self.root.is_real()

    def get_sympy_exp(self):
        return self.root.get_sympy_exp()

    def replace_random_leaf(self, data):
        assert data in terminals
        leaf_node_list = [
            node for node in traverse_in_preorder(self.root) if node.is_leaf()
        ]
        leaf_node = np.random.choice(leaf_node_list)
        leaf_node.set(data)

    def get_simplified_derivative(self):
        derivative = diff(self.get_sympy_exp())
        return str(simplify(derivative)).replace(" ", "").strip()

    def get_simplified_without_constant(self):
        expr_without_constant = separate_constant_term(self.get_sympy_exp(), var=x)[1]
        return str(simplify(expr_without_constant)).replace(" ", "").strip()

    def __str__(self):
        # traverse = traverse_in_preorder(self.root)
        # return ",".join([str(node) for node in traverse]) + "----" + str(len(traverse))
        return ",".join([str(node) for node in traverse_in_preorder(self.root)])

