# -*- coding: utf-8 -*-

from .constants import *
from .gen_utils import *
from sympy import *
import numpy as np

__all__ = ["Node"]


class Node(object):
    def __init__(self, data=None):
        self.data = data
        self.children = []
        self.exp = None

    def is_leaf(self):
        return len(self.children) == 0

    def is_internal(self):
        return not self.is_leaf()

    def add_child(self, data=None, node=None):
        if type(node) is Node:
            new_child = node
        else:
            new_child = Node(data)
        self.children.append(new_child)
        return new_child

    def set(self, data):
        self.data = data

    def get_sympy_exp(self):
        """
        Get its expression as sympy object
        """
        if self.exp is None:
            if self.data in terminals:
                self.exp = self.data
            elif self.data in unary_operations:
                self.exp = self.data(self.children[0].get_sympy_exp())
            elif self.data in binary_operations:
                self.exp = self.data(
                    self.children[0].get_sympy_exp(), self.children[1].get_sympy_exp()
                )
            else:
                raise Exception("get_sympy_exp error, invalid data: " + str(self.data))

        return self.exp

    def has_symbols(self):
        return len(self.get_sympy_exp().free_symbols) > 0

    def is_real(self):
        try:
            f = lambdify(x, self.get_sympy_exp(), "numpy")
        except:
            return False

        numeric = 0.12345
        while numeric < 1000:
            try:
                value = f(numeric)
                if np.isfinite(value) and np.isreal(value):
                    return True
            except:
                pass
            numeric = numeric * 10

        return False

    def __str__(self):
        try:
            res = self.data.__name__
        except:
            res = str(self.data)

        if res == "".join([c for c in res if c in "0123456789"]):
            return ",".join("p" + res)
        elif res == "-" + "".join([c for c in res if c in "0123456789"]):
            return ",".join("m" + res[1:])
        else:
            return res
