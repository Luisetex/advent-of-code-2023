import os


def read_input(input_path: str):
    with open(input_path, "r", encoding="utf8") as f:
        return [line.strip() for line in f.readlines()]


INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")

# Part A

steps_map = read_input(INPUT_PATH)


def get_nodes(network_map: list[str]) -> dict[str, dict[str, str]]:
    nodes = {}
    for node in network_map:
        if node:
            origin, paths = node.split("=")
            origin = origin.strip()
            paths = [path.replace("(", "").replace(")", "").strip() for path in paths.split(",")]
            nodes[origin] = {"L": paths[0], "R": paths[1]}
    return nodes


def get_num_steps(path_steps: str, nodes_path: dict[str, dict[str, str]]) -> int:
    initial_node_label = "AAA"
    final_node_label = "ZZZ"
    current_node_label = initial_node_label
    num_steps: int = 0
    while current_node_label != final_node_label:
        for step in path_steps:
            current_node_label = nodes_path[current_node_label][step]
            num_steps += 1
            if current_node_label == final_node_label:
                return num_steps
    return num_steps


steps, network_map = steps_map[0], steps_map[1:]
print(get_num_steps(steps, get_nodes(network_map)))

# Part B

"""
We can check that in the steps in the network map are cyclic for each node traversing from A to Z:

AAA = (JXS, MFQ)
ZZZ = (MFQ, JXS)

RLA = (JSN, JVD)
JJZ = (JVD, JSN)

QLA = (TSH, RRN)
VHZ = (RRN, TSH)

QFA = (QQR, HDH)
PQZ = (HDH, QQR)

RXA = (NLJ, JPG)
QCZ = (JPG, NLJ)

JSA = (TNJ, JXC)
LRZ = (JXC, TNJ)
Given its cyclic nature, we can find the number of steps for each node ending with A and then
find the least common multiple of all of them.
"""


nodes_ending_with_a = [node for node in get_nodes(network_map) if node.endswith("A")]


def get_gcd(a: int, b: int) -> int:
    # Euclidean algorithm
    while b:
        a, b = b, a % b
    return a


def get_lcm(numbers: list[int]) -> int:
    lcm = numbers[0]
    for i in numbers[1:]:
        lcm = lcm * i // get_gcd(lcm, i)
    return lcm


def get_num_steps_to_z(path_steps: str, nodes_path: dict[str, dict[str, str]], node_label: str):
    current_node_label = node_label
    num_steps = 0
    while not current_node_label.endswith("Z"):
        for path_step in path_steps:
            current_node_label = nodes_path[current_node_label][path_step]
            num_steps += 1
            if current_node_label.endswith("Z"):
                return num_steps
    return num_steps


def get_num_steps_all_nodes(
    path_steps: str, nodes_path: dict[str, dict[str, str]], initial_node_labels: list[str]
):
    num_steps = [
        get_num_steps_to_z(path_steps, nodes_path, node_label) for node_label in initial_node_labels
    ]

    return num_steps


print(get_lcm(get_num_steps_all_nodes(steps, get_nodes(network_map), nodes_ending_with_a)))
