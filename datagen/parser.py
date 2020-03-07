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
    while True:
        try:
            with time_limit(5):
                tree = Tree(
                    data_type=data_type,
                    random_generate=True,
                    internal_node_size=internal_node_size,
                )
                input_string = normalize(tree.input)
                output_string = normalize(tree.output)
            break
        except TimeoutException:
            slack_message("Timeout: ", data_type)
            # print("\rTimed out! Restart!\n")
            continue
        except:
            slack_message(data_type + " error occured:")
            slack_message(traceback.format_exc())
            # raise Exception()
            # print("\rException occured:", e, "\n")
            continue

    return [input_string, output_string]


def parse_data(input_string, output_string):
    return [
        str(Tree(standard_to_tree(normalize(input_string)))),
        str(Tree(standard_to_tree(normalize(output_string)))),
    ]

