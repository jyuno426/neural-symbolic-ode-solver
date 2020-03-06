# -*- coding: utf-8 -*-

from datagen.utils import parse_simplified_string_exprssion_into_tree
from contextlib import contextmanager
from datetime import timedelta
from datagen import *
from sympy import *
import warnings
import signal
import slack
import time

warnings.filterwarnings("error")


class TimeoutException(Exception):
    pass


@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException

    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)


i = 0
n = int(2e4)
while i < n:
    tree = Tree(random_generate=True, always_valid=True)

    try:
        with time_limit(5):
            input_string = tree.get_simplified_derivative()
            output_string = tree.get_simplified_without_constant()
    except TimeoutException:
        # print("Timed out! Restart!", end="                                          ")
        continue

    # print("input_trans:\t", parse_simplified_string_exprssion_into_tree(input_string))
    # print("input_origin:\t", input_string)
    print(
        "output_trans:\t",
        Tree(parse_simplified_string_exprssion_into_tree(output_string)),
    )
    print("output_origin:\t", output_string)

    break
