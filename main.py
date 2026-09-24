"""
Pathfinding Algorithm Visualizer
---------------------------------
An interactive grid where you place a start point, an end point, and
walls, then watch BFS, DFS, or Dijkstra search for a path in real time.

Controls:
    Left click            -> place start (1st click), end (2nd click),
                              walls (every click after that)
    Right click           -> erase a cell back to empty
    B                     -> run BFS
    D                     -> run DFS
    J                     -> run Dijkstra   (J for "Dijkstra", D is taken)
    C                     -> clear the grid and start over
    ESC / close window    -> quit

Run with:
    pip install pygame
    python main.py
"""

from tkinter import font

import pygame
import time
from algorithms import ALGORITHMS

# ---- Grid / window configuration -----------------------------------
ROWS, COLS = 25, 40
CELL_SIZE = 24
GRID_WIDTH = COLS * CELL_SIZE
GRID_HEIGHT = ROWS * CELL_SIZE
INFO_HEIGHT = 60  # strip at the bottom for text
WINDOW_WIDTH = GRID_WIDTH
WINDOW_HEIGHT = GRID_HEIGHT + INFO_HEIGHT

# ---- Colors ----------------------------------------------------------
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GREY = (200, 200, 200)
WALL_COLOR = (40, 40, 40)
START_COLOR = (46, 204, 113)     # green
END_COLOR = (231, 76, 60)        # red
VISITED_COLOR = (174, 214, 241)  # light blue
PATH_COLOR = (241, 196, 15)      # yellow
BG_COLOR = (30, 30, 30)


class Grid:
    """Thin wrapper around the 2D grid + cell states for drawing."""

    EMPTY, WALL, START, END = 0, 1, 2, 3

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.cells = [[self.EMPTY for _ in range(cols)] for _ in range(rows)]
        self.start = None
        self.end = None

    def as_walls_grid(self):
        """Convert to the plain 0/1 grid the algorithms module expects."""
        return [[1 if cell == self.WALL else 0 for cell in row]
                for row in self.cells]

    def reset(self):
        self.cells = [[self.EMPTY for _ in range(self.cols)]
                      for _ in range(self.rows)]
        self.start = None
        self.end = None

    def set_cell(self, row, col, left_click):
        if left_click:
            if self.start is None and (row, col) != self.end:
                self.cells[row][col] = self.START
                self.start = (row, col)
            elif self.end is None and (row, col) != self.start:
                self.cells[row][col] = self.END
                self.end = (row, col)
            elif (row, col) not in (self.start, self.end):
                self.cells[row][col] = self.WALL
        else:  # right click erases
            if (row, col) == self.start:
                self.start = None
            if (row, col) == self.end:
                self.end = None
            self.cells[row][col] = self.EMPTY


def draw_grid(screen, grid, visited=None, path=None, font=None, status=""):
    screen.fill(BG_COLOR)

    visited = visited or []
    path = path or []
    path_set = set(path)
    visited_set = set(visited)

    for r in range(grid.rows):
        for c in range(grid.cols):
            rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE,
                                CELL_SIZE, CELL_SIZE)
            cell = grid.cells[r][c]

            if cell == Grid.WALL:
                color = WALL_COLOR
            elif cell == Grid.START:
                color = START_COLOR
            elif cell == Grid.END:
                color = END_COLOR
            elif (r, c) in path_set:
                color = PATH_COLOR
            elif (r, c) in visited_set:
                color = VISITED_COLOR
            else:
                color = WHITE

            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, GREY, rect, 1)  # grid lines

    # Info strip at the bottom
    info_rect = pygame.Rect(0, GRID_HEIGHT, WINDOW_WIDTH, INFO_HEIGHT)
    pygame.draw.rect(screen, BLACK, info_rect)
    if font:
        text = font.render(status, True, WHITE)
        screen.blit(text, (10, GRID_HEIGHT + 18))

    pygame.display.update()


def get_row_col_from_pos(pos):
    x, y = pos
    if y >= GRID_HEIGHT:
        return None
    return y // CELL_SIZE, x // CELL_SIZE


def run_algorithm(name, grid, screen, font):
    """Run the chosen algorithm and animate its exploration + final path."""
    if grid.start is None or grid.end is None:
        draw_grid(screen, grid, font=font,
                   status="Set both a start (green) and end (red) cell first.")
        pygame.time.wait(1200)
        return

    algo_fn = ALGORITHMS[name]
    walls_grid = grid.as_walls_grid()

    start_time = time.perf_counter()
    visited_order, path = algo_fn(walls_grid, grid.start, grid.end)
    elapsed_ms = (time.perf_counter() - start_time) * 1000

    # Animate exploration
    animated = []
    for node in visited_order:
        if node in (grid.start, grid.end):
            continue
        animated.append(node)
        draw_grid(screen, grid, visited=animated, font=font,
                   status=f"Running {name.upper()}...")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
        pygame.time.wait(8)  # small delay so the animation is visible

    if path:
        status = (f"{name.upper()} done in {elapsed_ms:.2f} ms | "
                  f"visited {len(visited_order)} cells | "
                  f"path length {len(path)}")
    else:
        status = (f"{name.upper()} done in {elapsed_ms:.2f} ms | "
                  f"NO PATH FOUND (visited {len(visited_order)} cells)")

    draw_grid(screen, grid, visited=animated, path=path, font=font,
           status=status)

    return animated, path, status


def main():     
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Pathfinding Visualizer - BFS / DFS / Dijkstra")
    font = pygame.font.SysFont("consolas", 16)

    grid = Grid(ROWS, COLS)
    visited = []
    path = []
    status = "Left click: start -> end -> walls | B=BFS D=DFS J=Dijkstra C=Clear"

    running = True
    while running:
        draw_grid(screen, grid, visited=visited, path=path,
          font=font, status=status)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = get_row_col_from_pos(pygame.mouse.get_pos())
                if pos:
                    row, col = pos
                    left_click = event.button == 1
                    grid.set_cell(row, col, left_click)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_c:
                    grid.reset()
                    visited = []
                    path = []
                    status = "Grid cleared."
                elif event.key == pygame.K_b:
                    visited, path, status = run_algorithm("bfs", grid, screen, font)

                elif event.key == pygame.K_d:
                    visited, path, status = run_algorithm("dfs", grid, screen, font)

                elif event.key == pygame.K_j:
                    visited, path, status = run_algorithm("dijkstra", grid, screen, font)

    pygame.quit()


if __name__ == "__main__":
    main()