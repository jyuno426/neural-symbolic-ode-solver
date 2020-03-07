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

parse_raw_data_total_cnt = 0
parse_raw_data_timeout_cnt = 0
parse_raw_data_others_cnt = 0


def parse_raw_data(internal_node_size, data_type):
    global parse_raw_data_total_cnt, parse_raw_data_timeout_cnt, parse_raw_data_others_cnt

    if data_type == "integration":
        timeout = 5
    elif data_type == "ode1":
        timeout = 7
    else:
        timeout = 10

    while True:
        parse_raw_data_total_cnt += 1
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
            parse_raw_data_timeout_cnt += 1
            # slack_message(
            #     "Timeout: "
            #     + data_type
            #     + ", "
            #     + str(parse_raw_data_timeout_cnt)
            #     + "/"
            #     + str(parse_raw_data_total_cnt),
            #     data_type,
            # )
            # print("\rTimed out! Restart!\n")
            continue
        except Exception as e:
            parse_raw_data_others_cnt += 1
            slack_message(
                "------------------------------------\n"
                + data_type
                + " error occured, "
                + str(parse_raw_data_others_cnt)
                + "/"
                + str(parse_raw_data_total_cnt)
                + "\n"
                + str(e)
                + "\n"
                + str(traceback.format_exc())
                + "\n"
                + "------------------------------------",
                data_type,
            )
            # print("\rException occured:", e, "\n")
            # print(traceback.format_exc())
            # raise Exception()
            continue

    return [input_string, output_string]


def parse_data(input_string, output_string):
    return [
        str(Tree(standard_to_tree(normalize(input_string)))),
        str(Tree(standard_to_tree(normalize(output_string)))),
    ]

