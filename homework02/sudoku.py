import pathlib
import random
import typing as tp

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    group_n = []
    for i in range(0, len(values), n):
        group_n.append(values[i : i + n])
    return group_n


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    return grid[pos[0]]


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    return [row[pos[1]] for row in grid]


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    pos_block = (pos[0] // 3, pos[1] // 3)
    block = []
    for row in grid[pos_block[0] * 3 : pos_block[0] * 3 + 3]:
        for elem in row[pos_block[1] * 3 : pos_block[1] * 3 + 3]:
            block.append(elem)
    return block


def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]]:
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == ".":
                return row, col
    return None


def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    row = get_row(grid, pos)
    col = get_col(grid, pos)
    block = get_block(grid, pos)
    return set("123456789") - set(block) - set(row) - set(col)


def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    empty = find_empty_positions(grid)
    if not empty:
        return grid
    values = find_possible_values(grid, empty)
    new = [list(arr) for arr in grid]
    for value in values:
        new[empty[0]][empty[1]] = value
        rez = solve(new)
        if rez:
            return rez
    return None


def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    nabor = set("123456789")
    for i in range(len(solution)):
        for j in range(len(solution)):
            if (
                set(get_block(solution, (i, j))) != nabor
                or set(get_row(solution, (i, j))) != nabor
                or set(get_col(solution, (i, j))) != nabor
            ):
                return False
    return True


def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    init = solve([["."] * 9 for _ in range(9)])
    count = 0
    while count < 81 - N:
        row, col = random.randint(0, 8), random.randint(0, 8)
        if init and init[row][col] != ".":
            init[row][col] = "."
            count += 1
    return init


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)
