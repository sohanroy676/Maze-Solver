import pygame
import random
from collections import deque

# Constants
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 20, 20
CELL_SIZE = WIDTH // COLS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Initialize Pygame
pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Solver")

class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.walls = [True, True, True, True]  # top, right, bottom, left
        self.visited = False

    def draw(self, win):
        x = self.col * CELL_SIZE
        y = self.row * CELL_SIZE

        if self.walls[0]:
            pygame.draw.line(win, WHITE, (x, y), (x + CELL_SIZE, y), 1)
        if self.walls[1]:
            pygame.draw.line(win, WHITE, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), 1)
        if self.walls[2]:
            pygame.draw.line(win, WHITE, (x, y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE), 1)
        if self.walls[3]:
            pygame.draw.line(win, WHITE, (x, y), (x, y + CELL_SIZE), 1)

def create_grid(rows, cols):
    return [[Cell(row, col) for col in range(cols)] for row in range(rows)]

def remove_walls(current, next):
    dx = current.col - next.col
    if dx == 1:
        current.walls[3] = False
        next.walls[1] = False
    elif dx == -1:
        current.walls[1] = False
        next.walls[3] = False

    dy = current.row - next.row
    if dy == 1:
        current.walls[0] = False
        next.walls[2] = False
    elif dy == -1:
        current.walls[2] = False
        next.walls[0] = False

def generate_maze(grid):
    stack = []
    current = grid[0][0]
    current.visited = True

    while True:
        next_cell = None
        neighbors = []
        if current.row > 0 and not grid[current.row - 1][current.col].visited:
            neighbors.append(grid[current.row - 1][current.col])
        if current.row < ROWS - 1 and not grid[current.row + 1][current.col].visited:
            neighbors.append(grid[current.row + 1][current.col])
        if current.col > 0 and not grid[current.row][current.col - 1].visited:
            neighbors.append(grid[current.row][current.col - 1])
        if current.col < COLS - 1 and not grid[current.row][current.col + 1].visited:
            neighbors.append(grid[current.row][current.col + 1])

        if neighbors:
            next_cell = random.choice(neighbors)
            stack.append(current)
            remove_walls(current, next_cell)
            current = next_cell
            current.visited = True
        elif stack:
            current = stack.pop()
        else:
            break

def draw_grid(win, grid):
    for row in grid:
        for cell in row:
            cell.draw(win)

def get_neighbors(cell, grid):
    neighbors = []
    if not cell.walls[0] and cell.row > 0:
        neighbors.append(grid[cell.row - 1][cell.col])
    if not cell.walls[1] and cell.col < COLS - 1:
        neighbors.append(grid[cell.row][cell.col + 1])
    if not cell.walls[2] and cell.row < ROWS - 1:
        neighbors.append(grid[cell.row + 1][cell.col])
    if not cell.walls[3] and cell.col > 0:
        neighbors.append(grid[cell.row][cell.col - 1])
    return neighbors

def bfs_solver(start, end, grid):
    queue = deque()
    queue.append(start)
    visited = set()
    visited.add(start)
    parent = {}
    parent[start] = None

    while queue:
        current = queue.popleft()
        if current == end:
            break
        for neighbor in get_neighbors(current, grid):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)

    path = []
    while end:
        path.append(end)
        end = parent[end]
    path.reverse()
    return path

def main():
    clock = pygame.time.Clock()
    grid = create_grid(ROWS, COLS)
    generate_maze(grid)
    
    draw_grid(win, grid)
    pygame.display.update()
    pygame.time.delay(5000)
    start = grid[0][0]
    end = grid[ROWS - 1][COLS - 1]
    path = bfs_solver(start, end, grid)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        win.fill(BLACK)
        draw_grid(win, grid)
        
        # Draw the path
        for cell in path:
            pygame.draw.rect(win, GREEN, (cell.col * CELL_SIZE, cell.row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        for i in range(len(path) - 1):
            cell, nextCell = path[i], path[i + 1]
            pygame.draw.line(win, RED, (cell.col * CELL_SIZE + CELL_SIZE//2, cell.row * CELL_SIZE + CELL_SIZE//2), (nextCell.col * CELL_SIZE + CELL_SIZE//2, nextCell.row * CELL_SIZE + CELL_SIZE//2))
        
        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
