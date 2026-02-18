import pygame
import sys
import time
from collections import deque
import heapq

# ===============================
# CONFIGURATION
# ===============================
ROWS = 20
COLS = 20
CELL_SIZE = 30
WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)      # Start
BLUE = (0, 0, 200)       # Target
RED = (200, 0, 0)        # Walls
YELLOW = (255, 255, 0)   # Frontier
GRAY = (150, 150, 150)   # Explored
PURPLE = (160, 32, 240)  # Final Path

DELAY = 0.03

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Uninformed Search Visualizer")

# ===============================
# MOVEMENT ORDER (STRICT)
# ===============================
# 1. Up
# 2. Right
# 3. Bottom
# 4. Bottom-Right (Diagonal)
# 5. Left
# 6. Top-Left (Diagonal)

MOVES = [
    (-1, 0),  # Up
    (0, 1),   # Right
    (1, 0),   # Bottom
    (1, 1),   # Bottom-Right
    (0, -1),  # Left
    (-1, -1)  # Top-Left
]

# ===============================
# GRID INITIALIZATION
# ===============================
grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

start = (2, 2)
target = (17, 17)

# Example wall
for i in range(5, 15):
    grid[i][10] = -1

# ===============================
# DRAW FUNCTION
# ===============================
def draw(frontier=set(), explored=set(), path=[]):
    screen.fill(WHITE)

    for r in range(ROWS):
        for c in range(COLS):
            rect = pygame.Rect(c*CELL_SIZE, r*CELL_SIZE, CELL_SIZE, CELL_SIZE)

            if grid[r][c] == -1:
                pygame.draw.rect(screen, RED, rect)
            elif (r, c) == start:
                pygame.draw.rect(screen, GREEN, rect)
            elif (r, c) == target:
                pygame.draw.rect(screen, BLUE, rect)
            elif (r, c) in path:
                pygame.draw.rect(screen, PURPLE, rect)
            elif (r, c) in frontier:
                pygame.draw.rect(screen, YELLOW, rect)
            elif (r, c) in explored:
                pygame.draw.rect(screen, GRAY, rect)

            pygame.draw.rect(screen, BLACK, rect, 1)

    pygame.display.update()

# ===============================
# PATH RECONSTRUCTION
# ===============================
def reconstruct_path(parent):
    path = []
    node = target
    while node in parent:
        path.append(node)
        node = parent[node]
    path.reverse()
    return path

# ===============================
# BFS
# ===============================
def bfs():
    queue = deque([start])
    parent = {}
    explored = set()
    frontier = {start}

    while queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current = queue.popleft()
        frontier.remove(current)
        explored.add(current)

        if current == target:
            return reconstruct_path(parent)

        for dr, dc in MOVES:
            nr, nc = current[0] + dr, current[1] + dc
            if 0 <= nr < ROWS and 0 <= nc < COLS:
                if grid[nr][nc] != -1 and (nr, nc) not in explored and (nr, nc) not in frontier:
                    parent[(nr, nc)] = current
                    queue.append((nr, nc))
                    frontier.add((nr, nc))

        draw(frontier, explored)
        time.sleep(DELAY)

    return []

# ===============================
# DFS
# ===============================
def dfs():
    stack = [start]
    parent = {}
    explored = set()
    frontier = {start}

    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current = stack.pop()
        frontier.remove(current)
        explored.add(current)

        if current == target:
            return reconstruct_path(parent)

        for dr, dc in reversed(MOVES):
            nr, nc = current[0] + dr, current[1] + dc
            if 0 <= nr < ROWS and 0 <= nc < COLS:
                if grid[nr][nc] != -1 and (nr, nc) not in explored and (nr, nc) not in frontier:
                    parent[(nr, nc)] = current
                    stack.append((nr, nc))
                    frontier.add((nr, nc))

        draw(frontier, explored)
        time.sleep(DELAY)

    return []

# ===============================
# UCS
# ===============================
def ucs():
    pq = [(0, start)]
    parent = {}
    cost = {start: 0}
    explored = set()
    frontier = {start}

    while pq:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current_cost, current = heapq.heappop(pq)
        frontier.remove(current)
        explored.add(current)

        if current == target:
            return reconstruct_path(parent)

        for dr, dc in MOVES:
            nr, nc = current[0] + dr, current[1] + dc
            if 0 <= nr < ROWS and 0 <= nc < COLS and grid[nr][nc] != -1:
                new_cost = current_cost + 1
                if (nr, nc) not in cost or new_cost < cost[(nr, nc)]:
                    cost[(nr, nc)] = new_cost
                    parent[(nr, nc)] = current
                    heapq.heappush(pq, (new_cost, (nr, nc)))
                    frontier.add((nr, nc))

        draw(frontier, explored)
        time.sleep(DELAY)

    return []

# ===============================
# DLS
# ===============================
def dls(limit):
    stack = [(start, 0)]
    parent = {}
    explored = set()
    frontier = {start}

    while stack:
        current, depth = stack.pop()
        frontier.discard(current)
        explored.add(current)

        if current == target:
            return reconstruct_path(parent)

        if depth < limit:
            for dr, dc in reversed(MOVES):
                nr, nc = current[0] + dr, current[1] + dc
                if 0 <= nr < ROWS and 0 <= nc < COLS:
                    if grid[nr][nc] != -1 and (nr, nc) not in explored:
                        parent[(nr, nc)] = current
                        stack.append(((nr, nc), depth+1))
                        frontier.add((nr, nc))

        draw(frontier, explored)
        time.sleep(DELAY)

    return []

# ===============================
# IDDFS
# ===============================
def iddfs():
    for depth in range(ROWS * COLS):
        path = dls(depth)
        if path:
            return path
    return []

# ===============================
# BIDIRECTIONAL SEARCH
# ===============================
def bidirectional():
    q1 = deque([start])
    q2 = deque([target])

    parent1 = {}
    parent2 = {}

    visited1 = {start}
    visited2 = {target}

    while q1 and q2:
        current1 = q1.popleft()
        for dr, dc in MOVES:
            nr, nc = current1[0] + dr, current1[1] + dc
            if 0 <= nr < ROWS and 0 <= nc < COLS and grid[nr][nc] != -1:
                if (nr, nc) not in visited1:
                    parent1[(nr, nc)] = current1
                    visited1.add((nr, nc))
                    q1.append((nr, nc))
                if (nr, nc) in visited2:
                    meet = (nr, nc)
                    path1 = reconstruct_path(parent1)
                    path2 = []
                    node = meet
                    while node in parent2:
                        path2.append(node)
                        node = parent2[node]
                    return path1 + path2[::-1]

        draw(visited1 | visited2, set())
        time.sleep(DELAY)

    return []

# ===============================
# MAIN LOOP
# ===============================
def main():
    draw()
    print("Press:")
    print("1 = BFS")
    print("2 = DFS")
    print("3 = UCS")
    print("4 = DLS (limit=15)")
    print("5 = IDDFS")
    print("6 = Bidirectional")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    path = bfs()
                elif event.key == pygame.K_2:
                    path = dfs()
                elif event.key == pygame.K_3:
                    path = ucs()
                elif event.key == pygame.K_4:
                    path = dls(15)
                elif event.key == pygame.K_5:
                    path = iddfs()
                elif event.key == pygame.K_6:
                    path = bidirectional()
                else:
                    continue

                draw(path=path)

main()

