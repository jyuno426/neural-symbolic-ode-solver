# -*- coding: utf-8 -*-

from utility import *
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
        data_type="integration",
    ):
        self.root = None

        if random_generate:
            if data_type == "integration":
                while not self.is_valid():
                    self.root = generate_random_tree(internal_node_size)
                self.input = simplify(diff(self.get_sympy_exp()))
                self.output = simplify(self.drop_number())

            elif data_type == "ode1":
                simplified = None
                while True:
                    self.root = generate_random_tree(internal_node_size)
                    if not self.is_valid():
                        continue

                    leaf_node = self.get_random_leaf_except()
                    leaf_node.set(c1)

                    self.get_sympy_exp(re_calculate=True)
                    simplified = simplify(self.drop_number())
                    if "c1" in normalize(simplified):
                        break

                self.output = simplify_coefficient(simplified, c1, x)
                expr = solve_by_symb(Sub(self.output, f), c1)
                self.input = fraction(simplify(expr.diff(x)))[0]

            elif data_type == "ode2":
                pass

        else:
            # Make sure that root is valid node
            assert type(root) is Node
            self.root = root

    def is_valid(self):
        """
        Check validity of expression whether it contains invalid
        value (complex value or infinity or nan or undefined)
        """
        if self.root is None:
            return False
        else:
            return is_real(self.get_sympy_exp())

    # def has_symbol(self, symb):
    #     return self.root.has_symbol(symb)

    def get_sympy_exp(self, re_calculate=False):
        return self.root.get_sympy_exp(re_calculate)

    def get_random_leaf_except(self, exception=[]):
        leaf_node_list = [
            node
            for node in traverse_in_preorder(self.root)
            if node.is_leaf() and node.data not in exception
        ]
        return np.random.choice(leaf_node_list)

    def drop_number(self):
        return separate_constant_term(self.get_sympy_exp(), var=[x, c1, c2])[1]

    def __str__(self):
        # traverse = traverse_in_preorder(self.root)
        # return ",".join([str(node) for node in traverse]) + "----" + str(len(traverse))
        return ",".join([str(node) for node in traverse_in_preorder(self.root)])

