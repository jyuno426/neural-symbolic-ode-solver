# -*- coding: utf-8 -*-

from datetime import date
from datagen import *
from utility import *
import time
import sys


def generator(data_type, dataset_path, date, internal_node_size, n=int(2e4)):

    start_time = time.time()
    slack_message("Start " + data_type + " dataset generation: n=" + str(n))

    input_raw = (
        dataset_path
        + "/raw-"
        + data_type
        + "-input-"
        + str(internal_node_size)
        + "-"
        + date
    )
    output_raw = (
        dataset_path
        + "/raw-"
        + data_type
        + "-output-"
        + str(internal_node_size)
        + "-"
        + date
    )

    input_final = (
        dataset_path
        + "/final-"
        + data_type
        + "-input-"
        + str(internal_node_size)
        + "-"
        + date
    )
    output_final = (
        dataset_path
        + "/final-"
        + data_type
        + "-output-"
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
        input_string, output_string = parse_raw_data(internal_node_size, data_type)

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
    duplicate_check = set()
    while i < n:
        if any(s in (input_list[i] + output_list[i]) for s in ["oo", "I", "Dummy"]):
            # some weired result produced when simplifying...
            i += 1
            continue

        try:
            input_string, output_string = parse_data(input_list[i], output_list[i])
        except:
            i += 1
            print("Error occured!")
            print("input:\t", input_list[i])
            print("output:\t", output_list[i])
            continue

        if input_string.count(",") >= 511 or output_string.count(",") >= 511:
            i += 1
            continue

        if input_string + "$" + output_string in duplicate_check:
            i += 1
            continue

        duplicate_check.add(input_string + "$" + output_string)
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


if __name__ == "__main__":
    today = date.today().strftime("%b-%d-%Y")
    internal_node_size = max_internal_node_size
    dataset_path = "./dataset"
    data_type = "integration"
    data_cnt = int(2e4)

    l = len(sys.argv)

    assert 1 <= l <= 4

    try:
        data_type = sys.argv[1]
    except:
        pass
    assert data_type in ["integration", "ode1", "ode2"]

    try:
        data_cnt = int(sys.argv[2])
    except:
        pass
    assert data_cnt >= 0

    try:
        internal_node_size = int(sys.argv[3])
    except:
        pass
    assert 0 <= internal_node_size <= max_internal_node_size

    generator(
        n=data_cnt,
        date=today,
        data_type=data_type,
        dataset_path=dataset_path,
        internal_node_size=internal_node_size,
    )
