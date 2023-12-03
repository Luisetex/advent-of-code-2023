import os
from functools import reduce


def read_input(input_path: str):
    with open(input_path, "r", encoding="utf8") as f:
        return [line.strip() for line in f.readlines()]


INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")

# Read input

schematic: list[str] = read_input(INPUT_PATH)
schematic_matrix: list[list[str]] = [list(row) for row in schematic]

# Part 1

row_size = len(schematic_matrix)
column_size = len(schematic_matrix[0])

schematic_adyacency_matrix: list[list[tuple[str, bool]]] = [
    [(character, False) for character in row] for row in schematic_matrix
]

row_size = len(schematic_adyacency_matrix)
column_size = len(schematic_adyacency_matrix[0])


def check_neighborhood(row: int, column: int) -> bool:
    top_row = row - 1 if row > 0 else row
    bottom_row = row + 1 if row < row_size - 1 else row
    left_column = column - 1 if column > 0 else column
    right_column = column + 1 if column < column_size - 1 else column
    for row_index in range(top_row, bottom_row + 1):
        for column_index in range(left_column, right_column + 1):
            if row_index == row and column_index == column:
                continue
            if (
                not schematic_matrix[row_index][column_index].isdigit()
                and schematic_matrix[row_index][column_index] != "."
            ):
                return True
    return False


numbers_with_adyacency: list[tuple[str, bool]] = []


def add_number_with_adyacency(numbers_with_adyacency, number, adyacency_found):
    if number:
        numbers_with_adyacency.append((number, adyacency_found))


for row in range(row_size):
    number = ""
    adyacency_found = False
    for column in range(column_size):
        cell = schematic_adyacency_matrix[row][column]
        if cell[0].isdigit():
            adyacency_found = check_neighborhood(row, column) or adyacency_found
            number += cell[0]
            cell = (cell[0], adyacency_found)
        else:
            add_number_with_adyacency(numbers_with_adyacency, number, adyacency_found)
            number = ""
            adyacency_found = False
        schematic_adyacency_matrix[row][column] = cell
    add_number_with_adyacency(numbers_with_adyacency, number, adyacency_found)

print(sum(int(number) for number, adyacency_found in numbers_with_adyacency if adyacency_found))

# Part 2


def check_adyacent_star_position(row: int, column: int) -> tuple[str, str]:
    top_row = row - 1 if row > 0 else row
    bottom_row = row + 1 if row < row_size - 1 else row
    left_column = column - 1 if column > 0 else column
    right_column = column + 1 if column < column_size - 1 else column
    for row_index in range(top_row, bottom_row + 1):
        for column_index in range(left_column, right_column + 1):
            if row_index == row and column_index == column:
                continue
            if schematic_matrix[row_index][column_index] == "*":
                return str(row_index), str(column_index)
    return "_", "_"


possible_gears: dict[str, list[int]] = {}


def add_gear(possible_gears, star_position, number):
    if star_position[0] != "_":
        possible_gear_id = "_".join(star_position)
        possible_gears.setdefault(possible_gear_id, []).append(int(number))


for row in range(row_size):
    number = ""
    star_position: tuple[str, str] = "_", "_"  # encodes row and column of the * character
    for column in range(column_size):
        cell = schematic_matrix[row][column]
        if not cell.isdigit():
            add_gear(possible_gears, star_position, number)
            number = ""
            star_position = "_", "_"
        else:
            possible_star_position = check_adyacent_star_position(row, column)
            number += cell
            if possible_star_position[0] != "_":
                star_position = possible_star_position
    add_gear(possible_gears, star_position, number)

gears = [gear for gear in possible_gears.values() if len(gear) > 1]

print(sum([reduce(lambda x, y: x * y, gear_weights) for gear_weights in gears]))
