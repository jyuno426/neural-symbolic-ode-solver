# -*- coding: utf-8 -*-

from datetime import date
from datagen import *
import sys

today = date.today().strftime("%b-%d-%Y")
internal_node_size = max_internal_node_size
dataset_path = "./dataset"
data_cnt = int(2e4)

if __name__ == "__main__":
    l = len(sys.argv)

    assert 2 <= l <= 4

    generator = None
    if sys.argv[1] == "integration":
        generator = generate_integration_dataset

    try:
        data_cnt = int(sys.argv[2])
    except:
        pass

    try:
        internal_node_size = int(sys.argv[3])
    except:
        pass

    if generator is not None:
        generator(
            n=data_cnt,
            date=today,
            dataset_path=dataset_path,
            internal_node_size=internal_node_size,
        )
