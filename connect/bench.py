from board import Board
from negamax import Negamax
from alphabeta import Alphabeta
from insane import Insane
from stats import Stats
from evaluation import Eval
from heuristic import NopHeuristic, BadHeuristic


class Test:

    def __init__(self, width, height, N, evaluation, moves):
        self.HL = 0
        self.w = width
        self.h = height
        self.N = N
        self.evaluation = Eval(ML = self.w * self.h, HL = self.HL, n = evaluation)
        self.moves = moves


    def run(self, solver, depth, heuristic, timeout, index):
        board = Board.from_seq(self.w, self.h, self.N, self.moves)
        heuristic = heuristic(board.ML, board.N)

        result = solver.move(board, depth, heuristic, timeout)

        if isinstance(result, Stats):
            return None
        else:
            _, evaluation, stats = result
            if evaluation != self.evaluation:
                print("error at {}, we got {} ({}), should be {} ({})".format(
                    index, evaluation, evaluation.n, self.evaluation, self.evaluation.n))
            time = stats.end_time - stats.start_time
            return time, stats.nodecount


def load_tests(filename, maxcases):
    tests = []

    with open(filename) as f:
        for line in f.readlines()[:maxcases]:
            line = line.split()

            width = int(line[0])
            height = int(line[1])
            N = int(line[2])
            evaluation = int(line[3])
            moves = list(map(int, line[4:]))

            tests.append(Test(width, height, N, evaluation, moves))

    return tests


def run_tests(tests, solver, depth, heuristic, timeout):
    timeouts = 0
    nodecounts = []
    times = []

    for index, test in enumerate(tests):
        result = test.run(solver, depth, heuristic, timeout, index)
        if result is not None:
            time, nodecount = result
            times.append(time)
            nodecounts.append(nodecount)
        else:
            timeouts += 1

    nodecounts.sort()
    times.sort()

    total = len(tests)
    if total == timeouts: return total, timeouts, 0, 0, 0, 0, 0

    mean_time = round(times[len(times) // 2], 6)
    max_time = round(times[-1], 6)
    mean_visited = nodecounts[len(nodecounts) // 2]
    max_visited = nodecounts[-1]
    visited_per_second = round(sum(nodecounts) / sum(times))

    return total, timeouts, mean_time, max_time, mean_visited, max_visited, visited_per_second


def main():
    folder = "tests/sets/"
    testsets = [
        "30_07",
        "20_07",
        "30_14",
        "20_14"
    ]
    maxcases = 100

    solver = Insane() # Negamax() or Alphabeta() or Insane()
    depth = None
    heuristic = NopHeuristic
    timeout = 10

    builder = ""
    builder += "\\begin{tabular}{|c|c|c|c|c|c|c|c|}\\hline\n"

    bold = lambda s: "\\textbf{{{}}}".format(s)
    headers = ["test set", "total", "timeouts", "mean time", "max time", "mean count", "max count", "count per sec"]
    builder += " & ".join(map(bold, headers)) + " \\\\\\hline\n"

    for testset in testsets:
        print("running", testset)
        tests = load_tests(folder + testset + ".txt", maxcases)
        result = run_tests(tests, solver, depth, heuristic, timeout)

        builder += testset.replace("_", "-") + " & "
        builder += " & ".join(map(str, result)) + " \\\\\\hline\n"

    builder += "\\end{tabular}\n"

    print()
    print(builder)


if __name__ == "__main__":
    main()
