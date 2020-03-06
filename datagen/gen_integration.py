# -*- coding: utf-8 -*-

from utility import *
from .parser import *
import time

__all__ = ["generate_integration_dataset"]


def generate_integration_dataset(dataset_path, date, internal_node_size, n=int(2e4)):
    start_time = time.time()
    slack_message("Start integration dataset generation: n=" + str(n))

    input_raw = (
        dataset_path + "/raw-integration-input-" + str(internal_node_size) + "-" + date
    )
    output_raw = (
        dataset_path + "/raw-integration-output-" + str(internal_node_size) + "-" + date
    )

    input_final = (
        dataset_path
        + "/final-integration-input-"
        + str(internal_node_size)
        + "-"
        + date
    )
    output_final = (
        dataset_path
        + "/final-integration-output-"
        + str(internal_node_size)
        + "-"
        + date
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
        print("current_cnt:", n)

    # parse to sympy format
    while i < n:
        input_string, output_string = parse_raw_integration_data(internal_node_size)

        if any(s in (input_string + output_string) for s in ["oo", "I", "Dummy"]):
            # some weired result produced when simplifying...
            continue

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
            prefix="raw data generation-" + str(i) + "/" + str(n) + ":",
            start_time=start_time,
            current_time=time.time(),
            length=20,
        )

        if i % 1000 == 0:
            slack_message(message)

    # parse to our format
    f = open(input_raw, "r")
    g = open(output_raw, "r")
    input_list = [line.strip() for line in f.readlines()]
    output_list = [line.strip() for line in g.readlines()]
    f.close()
    g.close()

    assert len(input_list) == n
    assert len(output_list) == n

    f = open(input_final, "w")
    g = open(output_final, "w")

    i = 0
    total_cnt = 0
    while i < n:
        if any(s in (input_list[i] + output_list[i]) for s in ["oo", "I", "Dummy"]):
            # some weired result produced when simplifying...
            i += 1
            continue

        try:
            input_string, output_string = parse_integration_data(
                input_list[i], output_list[i]
            )
        except:
            i += 1
            print("Error occured!")
            print("input:\t", input_list[i])
            print("output:\t", output_list[i])
            continue

        f.write(input_string + "\n")
        g.write(output_string + "\n")

        i += 1
        total_cnt += 1

        message = print_progress_bar(
            iteration=i,
            total=n,
            prefix="final data generation-" + str(i) + ":",
            start_time=start_time,
            current_time=time.time(),
            length=20,
        )

        if i % 10000 == 0:
            slack_message(message)

    f.close()
    g.close()

    print("total_cnt:", total_cnt)
