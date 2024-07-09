import pygame
import math
from queue import PriorityQueue

SCREEN_SIZE = 800
WINDOW = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("A* Path Finding Algorithm")

COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 255, 0)
COLOR_YELLOW = (255, 255, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_PURPLE = (128, 0, 128)
COLOR_ORANGE = (255, 165 ,0)
COLOR_GREY = (128, 128, 128)
COLOR_TURQUOISE = (64, 224, 208)


class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = COLOR_WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col


    def is_closed(self):
        return self.color == COLOR_RED


    def is_open(self):
        return self.color == COLOR_GREEN

    def is_barrier(self):
        return self.color == COLOR_BLACK

    def is_start(self):
        return self.color == COLOR_ORANGE

    def is_end(self):
        return self.color == COLOR_TURQUOISE

    def reset(self):
        self.color = COLOR_WHITE

    def make_start(self):
        self.color = COLOR_ORANGE

    def make_closed(self):
        self.color = COLOR_RED

    def make_open(self):
        self.color = COLOR_GREEN

    def make_barrier(self):
        self.color = COLOR_BLACK

    def make_end(self):
        self.color = COLOR_TURQUOISE

    def make_path(self):
        self.color = COLOR_PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): #up
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
             self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)

    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, COLOR_GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, COLOR_GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    win.fill(COLOR_WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


def main(win, width):
    NUM_ROWS = 50
    grid = make_grid(NUM_ROWS, width)

    start_spot = None
    end_spot = None

    run = True
    while run:
        draw(win, grid, NUM_ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]: # LEFT
                mouse_pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(mouse_pos, NUM_ROWS, width)
                spot = grid[row][col]
                if not start_spot and spot != end_spot:
                    start_spot = spot
                    start_spot.make_start()

                elif not end_spot and spot != start_spot:
                    end_spot = spot
                    end_spot.make_end()

                elif spot != end_spot and spot != start_spot:
                    spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]: # RIGHT
                mouse_pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(mouse_pos, NUM_ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start_spot:
                    start_spot = None
                elif spot == end_spot:
                    end_spot = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start_spot and end_spot:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    algorithm(lambda: draw(win, grid, NUM_ROWS, width), grid, start_spot, end_spot)

                if event.key == pygame.K_c:
                    start_spot = None
                    end_spot = None
                    grid = make_grid(NUM_ROWS, width)

    pygame.quit()

main(WINDOW, SCREEN_SIZE)
