from pathlib import Path


def make_graph(problem: str) -> list[list]:
    graph = []
    for line in problem.split("\n"):
        vertex = list(map(int, line.split(" ")))
        graph.append(vertex)
    return graph


# read input file
def parse_input(path: Path) -> list[dict]:
    with open(path, "r") as input:
        i = input.read()
    problem_solution = i.split("\n\n")
    res = []
    for i in range(len(problem_solution)):
        if i % 2 == 0:
            res.append(
                make_problem(
                    [make_graph(problem_solution[i]), int(problem_solution[i + 1])]
                )
            )
        else:
            continue

    return res


def make_problem(problem) -> dict:
    return {"input": problem[0], "solution": problem[1]}


def get_nodes(problem) -> set:
    res = set()
    for p in problem:
        for el in p:
            res.add(el)
    return res


def solve_problem(problem: list[list]):
    from itertools import combinations

    nodes = get_nodes(problem)
    edges = set((p[0], p[1]) for p in problem) | set((p[1], p[0]) for p in problem)

    def is_independent(subset):
        for a, b in combinations(subset, 2):
            if (a, b) in edges:
                return False
        return True

    for size in range(len(nodes), 0, -1):
        for subset in combinations(nodes, size):
            if is_independent(subset):
                return size
    return 1 if nodes else 0


def main():
    from argparse import ArgumentParser

    parser = ArgumentParser(description="Paths to problem files")
    parser.add_argument("paths", nargs="+", type=Path, help="Directory to search")
    args = parser.parse_args()
    inputs = list(map(parse_input, args.paths))
    for problems in inputs:
        for problem in problems:
            res = solve_problem(problem["input"])
            print(f"res: {problem['solution']} solution {res}")


if __name__ == "__main__":
    main()
