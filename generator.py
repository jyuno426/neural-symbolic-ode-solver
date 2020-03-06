# -*- coding: utf-8 -*-

from utility import *
from datagen import *
from sympy import *
from datetime import date
import time
import sys

today = date.today().strftime("%b-%d-%Y")


def generate_integration_dataset(n=int(2e4)):
    start_time = time.time()
    slack_message("Start integration dataset generation: n=" + str(n))

    input_raw = (
        "./dataset/raw-integration-input-" + str(max_internal_node_size) + "-" + today
    )
    output_raw = (
        "./dataset/raw-integration-output-" + str(max_internal_node_size) + "-" + today
    )

    input_final = (
        "./dataset/final-integration-input-" + str(max_internal_node_size) + "-" + today
    )
    output_final = (
        "./dataset/final-integration-output-"
        + str(max_internal_node_size)
        + "-"
        + today
    )
    try:
        f = open(input_raw, "r")
        g = open(output_raw, "r")
        i = len(f.readlines())
        j = len(g.readlines())
        f.close()
        g.close()
    except:
        i = 0
        j = 0

    assert i == j

    if n < i:
        n = i
        print("current cnt:", n)

    # parse to sympy format
    while i < n:
        input_string, output_string = parse_raw_integration_data()

        f = open(input_raw, "a+")
        g = open(output_raw, "a+")
        f.write(input_string + "\n")
        g.write(output_string + "\n")
        f.close()
        g.close()

        i += 1

        message = print_progress_bar(
            iteration=i,
            total=n,
            prefix="raw data generation-" + str(i) + ":",
            start_time=start_time,
            current_time=time.time(),
            length=20,
        )

        if i % 1000 == 0:
            slack_message(message)

    # parse to our format
    f = open(input_raw, "r")
    g = open(output_raw, "r")
    input_list = list(f.readlines())
    output_list = list(g.readlines())
    f.close()
    g.close()

    assert len(input_list) == n
    assert len(output_list) == n

    f = open(input_final, "w")
    g = open(output_final, "w")

    for i in range(n):
        input_string, output_string = parse_integration_data(
            input_list[i], output_list[i]
        )

        f.write(input_string + "\n")
        g.write(output_string + "\n")

        i += 1

        message = print_progress_bar(
            iteration=i,
            total=n,
            prefix="final data generation-" + str(i) + ":",
            start_time=start_time,
            current_time=time.time(),
            length=20,
        )

        if i % 1000 == 0:
            slack_message(message)

    f.close()
    g.close()


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        generate_integration_dataset()
    else:
        data_cnt = int(sys.argv[1])
        assert data_cnt > 0
        generate_integration_dataset(n=data_cnt)

