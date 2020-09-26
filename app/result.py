from collections import deque


def log_file(file_name):
    with open(file_name) as f:
        log_result = list(deque(f, 30))
    return log_result
