# -*- coding: utf-8 -*-

from datagen import *
from sympy import *
import time
from datetime import timedelta


def print_progress_bar(
    iteration,
    total,
    prefix="",
    suffix="",
    decimals=1,
    length=100,
    fill="█",
    printEnd="\r",
):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + "-" * (length - filledLength)
    print("\r%s |%s| %s%% %s" % (prefix, bar, percent, suffix), end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


def slack_message(message, channel):
    token = (
        "xoxp-880429464020-868103546978-870635433953-b3c779132c2eeb887cb6971d7091836f"
    )

    client = slack.WebClient(token=token)

    response = client.chat_postMessage(channel=channel, text=message)

    assert response["ok"]
    assert response["message"]["text"] == message

    print('successfully post message "' + message + '" to ' + channel)


f = open("./dataset/integration-input", "w")
g = open("./dataset/integration-output", "w")
f.close()
g.close()

f = open("./dataset/integration-input", "a+")
g = open("./dataset/integration-output", "a+")
n = int(10e5)

start_time = time.time()

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

    if i % 1000 == 0:
        slack_message(str(i), "#laboratory")

    print_progress_bar(
        iteration=i + 1,
        total=n,
        prefix="data generation-" + str(i + 1) + ":",
        suffix=str(timedelta(seconds=int(time.time() - start_time))),
        length=20,
    )
