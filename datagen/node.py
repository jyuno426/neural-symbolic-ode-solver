# -*- coding: utf-8 -*-

from .constants import *
from .gen_utils import *
from sympy import *
import numpy as np

__all__ = ["Node"]


class Node(object):
    def __init__(self, data=None):
        self.data = data
        self.symbols = set()
        self.parent = None
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
        new_child.parent = self
        return new_child

    def set(self, data):
        self.data = data

    def get_sympy_exp(self, re_calculate=False):
        """
        Get its expression as sympy object
        """
        if self.exp is None or re_calculate:
            # if self.data in terminals:
            #     self.exp = self.data
            if self.data in unary_operations:
                self.exp = self.data(self.children[0].get_sympy_exp(re_calculate))
            elif self.data in binary_operations:
                self.exp = self.data(
                    self.children[0].get_sympy_exp(re_calculate),
                    self.children[1].get_sympy_exp(re_calculate),
                )
            else:
                # terminals
                self.exp = self.data
                # raise Exception("get_sympy_exp error, invalid data: " + str(self.data))

        return self.exp

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
