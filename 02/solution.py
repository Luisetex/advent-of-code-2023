import os


def read_input(input_path: str):
    with open(input_path, "r", encoding="utf8") as f:
        return [line.strip() for line in f.readlines()]


INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")

# Read input

all_games = read_input(INPUT_PATH)

# Part 1

MAX_CUBES = {"red": 12, "green": 13, "blue": 14}


def is_parsed_set_possible(parsed_set: str):
    # Given a string like "3 blue", check if it is possible
    number, color = parsed_set.split(" ")
    return int(number) <= MAX_CUBES.get(color, 0)


def check_sets_in_game(game: str):
    parsed_game: str = game.split(":")[1].strip()
    parsed_turns: list[str] = parsed_game.split(";")
    parsed_set_per_turn = [
        parsed_set.strip() for turn in parsed_turns for parsed_set in turn.split(",")
    ]
    return all(is_parsed_set_possible(parsed_set) for parsed_set in parsed_set_per_turn)


possible_sets_per_game = [check_sets_in_game(game) for game in all_games]
print(sum([index + 1 if possible else 0 for index, possible in enumerate(possible_sets_per_game)]))

# Part 2


def get_cubes_power(game: str):
    parsed_game: str = game.split(":")[1].strip()
    parsed_turns: list[str] = parsed_game.split(";")
    parsed_set_per_turn = [
        parsed_set.strip() for turn in parsed_turns for parsed_set in turn.split(",")
    ]
    max_cubes = {"red": 0, "green": 0, "blue": 0}
    for parsed_set in parsed_set_per_turn:
        number, color = parsed_set.split(" ")
        max_cubes[color] = max(max_cubes[color], int(number))
    return max_cubes["red"] * max_cubes["blue"] * max_cubes["green"]


cubes_power_per_game = [get_cubes_power(game) for game in all_games]
print(sum(cubes_power_per_game))
