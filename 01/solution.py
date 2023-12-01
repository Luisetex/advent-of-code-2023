import os


def read_input(input_path: str):
    with open(input_path, "r", encoding="utf8") as f:
        return [line.strip() for line in f.readlines()]


INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")

# Read input

text_input = read_input(INPUT_PATH)

# Part 1

digits = ["".join(char for char in line if char.isdigit()) for line in text_input]
filter_digits = [digit for digit in digits if len(digit) > 0]
calibration_values = [int(digit[0] + digit[-1]) for digit in filter_digits]
print(sum(calibration_values))

# Part 2
numbers = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


def replace_numbers_in_string(string: str):
    if len(string) == 0:
        return ""
    for number in numbers:
        if string.startswith(number):
            replaced_string = string.replace(number, str(numbers.index(number) + 1), 1)
            return replaced_string[0] + replace_numbers_in_string(
                string[len(number) - 1 :]
            )  # handles the special case of blablatwoneblabla converted to blabla21blabla
    return string[0] + replace_numbers_in_string(string[1:])


replaced_digits = [replace_numbers_in_string(line) for line in text_input]
only_digits = ["".join(char for char in line if char.isdigit()) for line in replaced_digits]
calibration_values = [int(digit[0] + digit[-1]) for digit in only_digits]
print(sum(calibration_values))
