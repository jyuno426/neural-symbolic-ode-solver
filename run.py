# -*- coding: utf-8 -*-

from datagen import *
from sympy import *

f = open("./dataset/integration-input", "w")
g = open("./dataset/integration-output", "w")
f.close()
g.close()

f = open("./dataset/integration-input", "a+")
g = open("./dataset/integration-output", "a+")
n = 10e5

i = 0
while i < n:
    tree = Tree(random_generate=True, always_valid=True, function_of_x=True)
    try:
        input_string = tree.get_input()
        if len(input_string.split(",")) > 512:
            print("continue")
            continue
        output_string = tree.get_output()
        if len(output_string.split(",")) > 512:
            print("continue")
            continue
    except:
        continue
    f.write(input_string + "\n")
    g.write(output_string + "\n")
    # print("input:   ", input_string)
    # print("output:   ", output_string)
    i += 1

    print(i, "/", round(n))
