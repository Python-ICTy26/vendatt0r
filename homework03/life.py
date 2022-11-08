import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        grid: Grid = []
        for i in range(self.rows):
            grid.append([])
            grid[i] = [random.randint(0, int(randomize)) for j in range(self.cols)]
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        row, col = cell
        rez = []

        positions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for i in positions:
            newrow, newcol = row + i[0], col + i[1]
            if newrow < 0 or newrow >= self.rows or newcol < 0 or newcol >= self.cols:
                continue
            rez.append(self.curr_generation[newrow][newcol])
        return rez

    def get_next_generation(self) -> Grid:
        newgrid: Grid = []

        for i in range(self.rows):
            newgrid.append([])
            for j in range(self.cols):
                neighbours = self.get_neighbours((i, j))
                count = 0
                for n in neighbours:
                    if n:
                        count += 1

                if count == 2 and self.curr_generation[i][j]:
                    newgrid[i].append(1)
                    continue

                if count == 3:
                    newgrid[i].append(1)
                    continue

                newgrid[i].append(0)

        return newgrid

    def step(self) -> None:
        self.prev_generation = self.curr_generation.copy()
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        return self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        if self.prev_generation == self.curr_generation:
            return False
        else:
            return True

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        file = open(filename)
        whole = file.readlines()
        grid = []
        for i in range(len(whole)):
            if whole[i] != "\n":
                whole[i] = whole[i][:-1]
                row = [int(n) for n in list(whole[i])]
                grid.append(row)
        game = GameOfLife((len(grid), len(grid[0])))
        game.curr_generation = grid
        file.close()
        return game

    def save(self, filename: pathlib.Path) -> None:
        file = open(filename, "w")
        for i in range(len(self.curr_generation)):
            for j in range(len(self.curr_generation[0])):
                file.write(str(self.curr_generation[i][j]))
            file.write("\n")
        file.close()
