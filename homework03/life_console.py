import curses
import time

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        screen.border("|", "|", "-", "-", "+", "+", "+", "+")

    def draw_grid(self, screen) -> None:
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                if self.life.curr_generation[i][j]:
                    screen.addstr(1 + i, 1 + j, "*")
                else:
                    screen.addstr(1 + i, 1 + j, " ")

    def run(self) -> None:
        screen = curses.initscr()
        curses.noecho()
        self.draw_borders(screen)
        self.draw_grid(screen)
        screen.refresh()

        while not self.life.is_max_generations_exceeded and self.life.is_changing:
            self.life.step()
            self.draw_grid(screen)
            screen.refresh()
            time.sleep(0.2)

        curses.endwin()
