# -*- coding: utf-8 -*-

from utility import *
from .constants import *
from .gen_utils import *
from .node import *
from .tree import *
from sympy import *
import warnings
import traceback

__all__ = [
    "parse_data",
    "parse_raw_data",
]

warnings.filterwarnings("error")


def parse_raw_data(internal_node_size, data_type):
    if data_type == "integration":
        timeout = 5
    else:
        timeout = 10

    while True:
        try:
            with time_limit(timeout):
                tree = Tree(
                    data_type=data_type,
                    random_generate=True,
                    internal_node_size=internal_node_size,
                )
                input_string = normalize(tree.input)
                output_string = normalize(tree.output)
            break
        except TimeoutException:
            # print("\rTimed out! Restart!\n")
            continue
        except:
            # print(traceback.format_exc())
            # raise Exception()
            # print("\rException occured:", e, "\n")
            continue

    return [input_string, output_string]


def parse_data(input_string, output_string):
    return [
        str(Tree(standard_to_tree(normalize(input_string)))),
        str(Tree(standard_to_tree(normalize(output_string)))),
    ]

