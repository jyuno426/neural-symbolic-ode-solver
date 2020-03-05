# -*- coding: utf-8 -*-

from .constants import *
from .utils import *
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

    def add_child(self, data=None):
        new_child = data if type(data) is Node else Node(data)
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
            # try:
            #     self.exp = simplify(self.exp)
            # except:
            #     print(self.exp)

        return self.exp

    def has_symbols(self):
        return len(self.get_sympy_exp().free_symbols) > 0

    # def evaluate(self, x_val=None):
    #     assert x_val is None
    #     # evaluate for x is not allowed yet
    #     return self.get_sympy_exp().evalf()

    def is_real(self):
        # assert not self.has_symbols()
        self.exp = simplify(self.get_sympy_exp())
        return self.exp.is_real

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
