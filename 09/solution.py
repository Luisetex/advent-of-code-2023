import os
from functools import reduce


def read_input(input_path: str):
    with open(input_path, "r", encoding="utf8") as f:
        return [line.strip() for line in f.readlines()]


INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")

# Part A

input_lines = read_input(INPUT_PATH)
sensor_histories = [[int(value) for value in line.split()] for line in input_lines]


def get_differences(sensor_history: list[int]) -> tuple[list[int], list[int]]:
    first_elements = [sensor_history[0]]
    last_elements = [sensor_history[-1]]
    diff = [sensor_history[i + 1] - sensor_history[i] for i in range(len(sensor_history) - 1)]
    while not all(d == 0 for d in diff):
        first_elements.append(diff[0])
        last_elements.append(diff[-1])
        diff = [diff[i + 1] - diff[i] for i in range(len(diff) - 1)]
    return last_elements[::-1], first_elements[::-1]  # Reversing for later traversal


differences = list(map(get_differences, sensor_histories))
print(sum(map(lambda difference: reduce(lambda acc, el: acc + el, difference[0]), differences)))

# Part B
print(sum(map(lambda difference: reduce(lambda acc, el: el - acc, difference[1]), differences)))
