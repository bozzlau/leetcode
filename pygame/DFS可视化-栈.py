import pygame
import random
import time

# ---------- 配置 ----------
N = 10
WIDTH, HEIGHT = 600, 600
ROWS, COLS = N, N
CELL = WIDTH // COLS

# ---------- 颜色 ----------
WHITE = (240, 240, 240)
BLACK = (30, 30, 30)
BLUE = (120, 170, 255)
YELLOW = (255, 215, 0)
GREEN = (50, 205, 50)
RED = (220, 20, 60)
PURPLE = (160, 100, 255)

# ---------- 初始化 ----------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze DFS (Pause / Step / Order)")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 18)

# ---------- 迷宫 ----------
maze = [[0 if random.random() > 0.25 else 1 for _ in range(COLS)] for _ in range(ROWS)]
start = (0, 0)
end = (ROWS - 1, COLS - 1)
maze[start[0]][start[1]] = 0
maze[end[0]][end[1]] = 0

# ---------- DFS 生成器 ----------
def dfs(maze, start, end):
    stack = [start]
    visited = set([start])
    parent = {}
    step = 1
    visit_order = {start: step}

    while stack:
        x, y = stack.pop()
        yield ("visit", (x, y), visited, visit_order, parent)

        if (x, y) == end:
            path = []
            cur = end
            while cur != start:
                path.append(cur)
                cur = parent[cur]
            path.append(start)
            path.reverse()
            yield ("path", path, visited, visit_order, parent)
            return

        # 为了让 DFS 方向“看起来正常”，反向入栈
        for dx, dy in reversed([(-1,0),(1,0),(0,-1),(0,1)]):
            nx, ny = x + dx, y + dy
            if 0 <= nx < ROWS and 0 <= ny < COLS:
                if maze[nx][ny] == 0 and (nx, ny) not in visited:
                    step += 1
                    visit_order[(nx, ny)] = step
                    visited.add((nx, ny))
                    parent[(nx, ny)] = (x, y)
                    stack.append((nx, ny))

# ---------- 打印数字 ----------
def print_num(x, y):
    num = visit_order.get((x, y))
    if num:
        text = font.render(str(num), True, (0, 0, 0))
        screen.blit(
            text,
            text.get_rect(center=(y * CELL + CELL//2, x * CELL + CELL//2))
        )

# ---------- 绘制 ----------
def draw(maze, visited, visit_order, current=None, path=None):
    screen.fill((20, 20, 20))

    for i in range(ROWS):
        for j in range(COLS):
            rect = (j * CELL, i * CELL, CELL, CELL)
            if maze[i][j] == 1:
                pygame.draw.rect(screen, BLACK, rect)
            else:
                pygame.draw.rect(screen, WHITE, rect)

    for (x, y) in visited:
        pygame.draw.rect(screen, BLUE, (y * CELL, x * CELL, CELL, CELL))
        print_num(x, y)

    if current:
        x, y = current
        pygame.draw.rect(screen, YELLOW, (y * CELL, x * CELL, CELL, CELL))
        print_num(x, y)

    if path:
        for x, y in path:
            pygame.draw.rect(screen, PURPLE, (y * CELL, x * CELL, CELL, CELL))
            print_num(x, y)

    pygame.draw.rect(screen, GREEN, (start[1]*CELL, start[0]*CELL, CELL, CELL))
    print_num(start[0], start[1])
    pygame.draw.rect(screen, RED, (end[1]*CELL, end[0]*CELL, CELL, CELL))
    print_num(end[0], end[1])

    pygame.display.flip()

# ---------- 主循环 ----------
dfs_gen = dfs(maze, start, end)
visited = set()
visit_order = {}
current = None
path = None

paused = True
step_once = True

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            if event.key == pygame.K_RIGHT:
                step_once = True

    if not paused or step_once:
        try:
            action, data, visited, visit_order, parent = next(dfs_gen)
            if action == "visit":
                current = data
            elif action == "path":
                path = data
                current = None
        except StopIteration:
            pass
        step_once = False

    draw(maze, visited, visit_order, current, path)
    time.sleep(0.1)

pygame.quit()
