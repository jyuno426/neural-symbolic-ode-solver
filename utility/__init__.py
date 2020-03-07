# -*- coding: utf-8 -*-

from contextlib import contextmanager
from datetime import timedelta
import signal
import slack

__all__ = [
    "time_limit",
    "TimeoutException",
    "print_progress_bar",
    "slack_message",
    "normalize",
]


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


def print_progress_bar(
    iteration,
    total,
    prefix,
    start_time,
    current_time,
    decimals=1,
    length=20,
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
    suffix = str(timedelta(seconds=int(current_time - start_time)))
    message = prefix + " |" + bar + "| " + percent + "%% " + suffix
    print("\r" + message, end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()
    return message


def slack_message(message, channel="#laboratory"):
    token = (
        "xoxp-880429464020-868103546978-870635433953-b3c779132c2eeb887cb6971d7091836f"
    )

    client = slack.WebClient(token=token)
    response = client.chat_postMessage(channel=channel, text=message)

    assert response["ok"]
    assert response["message"]["text"] == message

    # print('successfully post message "' + message + '" to ' + channel)


def normalize(obj):
    return (
        str(obj)
        .strip()
        .replace(" ", "")
        .replace("Derivative(f(x),x)", "g")
        .replace("f(x)", "f")
    )
