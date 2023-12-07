import os


def read_input(input_path: str):
    with open(input_path, "r", encoding="utf8") as f:
        return [line.strip() for line in f.readlines()]


INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")

# Part A

HAND_TYPES = [
    "HIGH CARD",
    "ONE PAIR",
    "TWO PAIRS",
    "THREE OF A KIND",
    "FULL HOUSE",
    "FOUR OF A KIND",
    "FIVE OF A KIND",
]

CARD_LABELS = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]

games = read_input(INPUT_PATH)
parsed_games = [game.split() for game in games]


def count_cards(cards_bids: list[str]) -> tuple[str, int, dict[str, int]]:
    cards, bid = cards_bids
    count: dict[str, int] = {}
    for card in cards:
        count[card] = count.get(card, 0) + 1
    return (cards, int(bid), count)


def get_hand_type(
    cards_info: tuple[str, int, dict[str, int]], with_joker: bool = False
) -> tuple[str, int, str]:
    cards, bid, count = cards_info
    num_jokers = count.get("J", 0) if with_joker else 0

    if "J" in count and with_joker:
        del count["J"]

    if num_jokers == 5:
        return (cards, bid, "FIVE OF A KIND")

    count_values = sorted(count.values(), reverse=True)
    count_values[0] += num_jokers

    if count_values[0] == 5:
        return (cards, bid, "FIVE OF A KIND")
    if count_values[0] == 4:
        return (cards, bid, "FOUR OF A KIND")
    if count_values[0] == 3:
        if count_values[1] == 2:
            return (cards, bid, "FULL HOUSE")
        return (cards, bid, "THREE OF A KIND")
    if count_values[0] == 2:
        if count_values[1] == 2:
            return (cards, bid, "TWO PAIRS")
        return (cards, bid, "ONE PAIR")
    return (cards, bid, "HIGH CARD")


def card_sort_key(card_info: tuple[str, int, str]):
    card_string, _, _ = card_info
    return [CARD_LABELS.index(c) for c in card_string]


def sort_cards(cards_info: list[tuple[str, int, str]]):
    sorted_cards = []
    for hand_type in HAND_TYPES:
        hands = [cards_info for cards_info in cards_info if cards_info[2] == hand_type]
        sorted_hands = sorted(hands, key=card_sort_key)
        sorted_cards.extend(sorted_hands)
    return sorted_cards


counted_cards = [count_cards(parsed_game) for parsed_game in parsed_games]
type_cards = [get_hand_type(counted_card) for counted_card in counted_cards]
sorted_cards = sort_cards(type_cards)
print(sum([index * card[1] for index, card in enumerate(sorted_cards, start=1)]))

# Part B

CARD_LABELS = ["J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A"]

type_cards = [get_hand_type(counted_card, with_joker=True) for counted_card in counted_cards]
sorted_cards = sort_cards(type_cards)
print(sum([index * card[1] for index, card in enumerate(sorted_cards, start=1)]))
