import os


def read_input(input_path: str):
    with open(input_path, "r", encoding="utf8") as f:
        return f.read().split("\n\n")


INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")

# Read input

# Parse the input
categories = read_input(INPUT_PATH)
seeds, category_maps = categories[0], categories[1:]

# Convert seeds to integers
parsed_seeds = [int(seed) for seed in seeds.split(": ")[1].split()]


def create_coordinate_map(map_coordinates: list[str]) -> list[tuple[int, int, int, int]]:
    """
    Create a coordinate map from a list of map coordinates.
    """
    coordinate_map = []
    for coordinates in map_coordinates:
        destination_start, source_start, length = [
            int(coordinate) for coordinate in coordinates.split()
        ]
        source_end = source_start + length - 1
        destination_end = destination_start + length - 1
        coordinate_map.append((source_start, source_end, destination_start, destination_end))
    return coordinate_map


def apply_coordinate_maps(maps: list[list[tuple[int, int, int, int]]], original_seed: int) -> int:
    """
    Apply each coordinate map to the original seed.
    """
    seed = original_seed
    for coordinate_map in maps:
        for source_start, source_end, destination_start, destination_end in coordinate_map:
            if source_start <= seed <= source_end:
                seed = destination_start + (seed - source_start)
                break
    return seed


coordinate_maps = [
    create_coordinate_map([coordinate for coordinate in coordinates if coordinate])
    for coordinates in [category.split("\n")[1:] for category in category_maps]
]

print(min([apply_coordinate_maps(coordinate_maps, seed) for seed in parsed_seeds]))

# Part 2

# Take elements of list in pairs and create a list of tuples
seed_pairs = list(zip(parsed_seeds[::2], parsed_seeds[1::2]))


def get_mapped_ranges(seed_pair, maps):
    untouched_ranges = [(seed_pair[0], seed_pair[0] + seed_pair[1] - 1)]
    all_ranges = []
    for coordinate_map in maps:
        transformed_ranges = []
        for map_range in coordinate_map:
            transformed, untouched = map_untouched_ranges(map_range, untouched_ranges)
            transformed_ranges.extend(transformed)
            untouched_ranges = untouched
        all_ranges = untouched_ranges + transformed_ranges
        untouched_ranges = all_ranges
    return all_ranges


def map_untouched_ranges(map_range, untouched_ranges):
    transformed_ranges = []
    new_untouched_ranges = []
    for seed_range in untouched_ranges:
        transformed, untouched = map_coordinate_ranges(map_range, seed_range)
        transformed_ranges.extend(transformed)
        new_untouched_ranges.extend(untouched)
    return transformed_ranges, new_untouched_ranges


def map_coordinate_ranges(map_range, seed_range):
    transformed_ranges = []
    untouched_ranges = []
    source_start, source_end, dest_start, dest_end = map_range
    seed_start, seed_end = seed_range

    if seed_end < source_start or source_end < seed_start:
        # Seed range is completely outside the map range
        untouched_ranges.append(seed_range)
        return transformed_ranges, untouched_ranges
    if seed_start < source_start <= seed_end <= source_end:
        # Map range overlaps the end of the seed range
        transformed_ranges.append((dest_start, dest_start + (seed_end - source_start)))
        untouched_ranges.append((seed_start, source_start - 1))
        return transformed_ranges, untouched_ranges
    if source_start <= seed_start <= source_end < seed_end:
        # Map range overlaps the start of the seed range
        transformed_ranges.append((dest_start + (seed_start - source_start), dest_end))
        untouched_ranges.append((source_end + 1, seed_end))
        return transformed_ranges, untouched_ranges
    if source_start <= seed_start and seed_end <= source_end:
        # Seed range is completely inside the map range
        transformed_ranges.append(
            (dest_start + (seed_start - source_start), dest_start + (seed_end - source_start))
        )
        return transformed_ranges, untouched_ranges
    if seed_start < source_start and source_end < seed_end:
        # Map range is completely inside the seed range
        transformed_ranges.append((dest_start, dest_end))
        untouched_ranges.append((seed_start, source_start - 1))
        untouched_ranges.append((source_end + 1, seed_end))
    return transformed_ranges, untouched_ranges


min_per_range = []
for seed_pair in seed_pairs:
    mapped_ranges = get_mapped_ranges(seed_pair, coordinate_maps)
    min_per_range.append(min([range_[0] for range_ in mapped_ranges]))
print(min(min_per_range))
