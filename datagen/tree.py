# -*- coding: utf-8 -*-

from .constants import *
from .utils import *
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
        function_of_x=False,
    ):
        self.simplified_exp = None
        if random_generate:
            self.root = generate_random_tree()
            if function_of_x:
                self.replace_random_leaf(data=x)
            if always_valid:
                while not self.is_valid():
                    self.root = generate_random_tree()
                    if function_of_x:
                        self.replace_random_leaf(data=x)
        else:
            # Make sure that root is valid node
            assert type(root) is Node
            if function_of_x:
                assert root.has_symbols()
            self.root = root

    def is_valid(self):
        """
        Check validity of expression whether it contains invalid value (complex value or infinity or undefined)
        """

        return (
            self.root.is_real()
            and (not "oo" in str(self.get_sympy_exp()))
            and (not "nan" in str(self.get_sympy_exp()))
        )
        # res = True
        # for node in reversed(traverse_in_preorder(self.root)):
        #     if node.is_real() == False:  # it can be None when variable x is involved
        #         res = False
        #         break
        # return res

    def get_sympy_exp(self):
        return self.root.get_sympy_exp()

    def replace_random_leaf(self, data):
        assert data in terminals
        leaf_node_list = [
            node for node in traverse_in_preorder(self.root) if node.is_leaf()
        ]
        leaf_node = np.random.choice(leaf_node_list)
        leaf_node.set(data)

    def get_input(self):
        return str(
            Tree(transform(str(simplify(diff(self.get_sympy_exp()))).replace(" ", "")))
        )

    def get_output(self):
        return str(Tree(transform(str(self.get_sympy_exp()).replace(" ", ""))))

    def __str__(self):
        return ",".join([str(node) for node in traverse_in_preorder(self.root)])

