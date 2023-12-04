import os
from functools import reduce


def read_input(input_path: str):
    with open(input_path, "r", encoding="utf8") as f:
        return [line.strip() for line in f.readlines()]


INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")

# Read input

cards: list[str] = read_input(INPUT_PATH)
numbers = [card.split(":")[-1].split("|") for card in cards]

# Part A


def get_winning_and_player_numbers(numbers_game: list[str]) -> tuple[list[int], list[int], int]:
    winning_numbers, player_numbers = [
        [int(number) for number in number_list.split()] for number_list in numbers_game
    ]
    number_of_cards = 1
    return winning_numbers, player_numbers, number_of_cards


def get_winning_player_numbers(winning_and_player_numbers: tuple[list[int], list[int], int]):
    winning_numbers, player_numbers, _ = winning_and_player_numbers
    winning_player_numbers = [
        True if number in winning_numbers else False for number in player_numbers
    ]

    return winning_player_numbers


parsed_cards = [get_winning_and_player_numbers(numbers_game) for numbers_game in numbers]

wins_per_card = [
    get_winning_player_numbers(get_winning_and_player_numbers(numbers_game))
    for numbers_game in numbers
]


def get_points(matches: list[bool]):
    total_matches = sum(matches)
    return 2 ** (total_matches - 1) if total_matches > 0 else 0


points = [get_points(matches) for matches in wins_per_card]
print(sum(points))

# Part B


def process_card(
    parsed_card: tuple[list[int], list[int], int],
    card_index: int,
    parsed_cards: list[tuple[list[int], list[int], int]],
):
    winning_numbers, player_numbers, number_of_cards = parsed_card
    wins = sum([True if number in winning_numbers else False for number in player_numbers])
    if wins:
        card_indices_to_copy = [
            win + card_index for win in range(1, wins + 1) if win + card_index < len(parsed_cards)
        ]
        for card_index_to_copy in card_indices_to_copy:
            card_replacement = (
                parsed_cards[card_index_to_copy][0],
                parsed_cards[card_index_to_copy][1],
                parsed_cards[card_index_to_copy][2] + number_of_cards,
            )
            parsed_cards[card_index_to_copy] = card_replacement

    return number_of_cards


card_copies = [
    process_card(parsed_card, card_index, parsed_cards)
    for card_index, parsed_card in enumerate(parsed_cards)
]
print(sum(card_copies))
