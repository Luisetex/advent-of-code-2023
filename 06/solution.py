import os
from functools import reduce


def read_input(input_path: str):
    with open(input_path, "r", encoding="utf8") as f:
        return [line.strip() for line in f.readlines()]


INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")

race_data = read_input(INPUT_PATH)
parsed_lists = [line.split(":")[-1].strip().split() for line in race_data]
duration_distance_pairs = list(zip(*[map(int, pair) for pair in parsed_lists]))

# Part A, naive solution


def get_best_results(duration_distance_pairs: tuple[int, int]) -> int:
    race_duration, record_distance = duration_distance_pairs
    possible_distances = [
        race_duration * time_pressed - time_pressed**2
        for time_pressed in range(race_duration + 1)
    ]
    winning_distances = [distance for distance in possible_distances if distance > record_distance]
    return len(winning_distances)


print(
    reduce(
        lambda x, y: x * y,
        [get_best_results(distance_pairs) for distance_pairs in duration_distance_pairs],
        1,
    )
)

# Part B, optimized solution


new_parsed_list = [int("".join(line.split(":")[-1].strip().split())) for line in race_data]


def get_best_results_optimized(duration_distance_pairs: tuple[int, int]) -> int:
    race_duration, record_distance = duration_distance_pairs
    # deriving from race_duration * time_pressed - time_pressed**2 > record_distance
    # we have that -time_pressed**2 + race_duration*time_pressed - record_distance > 0
    # or time_pressed**2 - race_duration*time_pressed + record_distance < 0
    # which is a quadratic equation, so
    # time_pressed = race_duration +- sqrt(race_duration**2 - 4*record_distance) / 2
    # and we only need the negative solution according to the derivation
    sqrt = (race_duration**2 - 4 * record_distance) ** 0.5
    solutions = (race_duration + sqrt) / 2, (race_duration - sqrt) / 2
    # Given it's a negative parabola, the ranges for which the solution is positive, is between the two solutions
    range_start, range_end = int(min(solutions)), int(max(solutions))
    # Now that we have the ranges, we only need to get the range size
    return range_end - range_start


print(get_best_results_optimized((new_parsed_list[0], new_parsed_list[1])))
