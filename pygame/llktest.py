import pygame
import random
import time

# ---------- 配置 ----------
N = 5
WIDTH, HEIGHT = 600, 600
STACK_WIDTH = 200  # 右侧调用栈宽度
ROWS, COLS = N, N
CELL = WIDTH // COLS

# ---------- 颜色 ----------
WHITE = (240, 240, 240)
BLACK = (30, 30, 30)
BLUE = (120, 170, 255)
YELLOW = (255, 215, 0)
GREEN = (50, 205, 50)
RED = (220, 20, 60)

# ---------- 初始化 ----------
pygame.init()
screen = pygame.display.set_mode((WIDTH + STACK_WIDTH, HEIGHT))
pygame.display.set_caption("Maze DFS Recursive Visualization")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 18)
small_font = pygame.font.SysFont(None, 14)

# ---------- 迷宫 ----------
maze = [[0 if random.random() > 0.25 else 1 for _ in range(COLS)] for _ in range(ROWS)]
start = (0, 0)
end = (ROWS - 1, COLS - 1)
maze[start[0]][start[1]] = 0
maze[end[0]][end[1]] = 0

# ---------- DFS（递归 + 回溯动画 + stack可视化） ----------
dfs_stack = []

def dfs(maze, start, end):
    visited = set()
    parent = {}
    visit_order = {}
    step = 0
    found = False

    def dfs_visit(x, y, depth):
        nonlocal step, found
        if found:
            return

        dfs_stack.append(((x, y), depth))  # 入栈
        visited.add((x, y))
        step += 1
        visit_order[(x, y)] = step

        yield ("visit", (x, y), visited, visit_order, parent, depth)

        if (x, y) == end:
            path = []
            cur = end
            while cur != start:
                path.append(cur)
                cur = parent[cur]
            path.append(start)
            path.reverse()
            yield ("path", path, visited, visit_order, parent, depth)
            found = True
            dfs_stack.pop()  # 终点回溯
            return

        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < ROWS and 0 <= ny < COLS:
                if maze[nx][ny] == 0 and (nx, ny) not in visited:
                    parent[(nx, ny)] = (x, y)
                    yield from dfs_visit(nx, ny, depth + 1)
                    if found:
                        dfs_stack.pop()
                        return

        # 回溯
        yield ("backtrack", (x, y), visited, visit_order, parent, depth)
        dfs_stack.pop()

    yield from dfs_visit(start[0], start[1], 0)

# ---------- 打印访问序号 ----------
def print_num(x, y, visit_order):
    num = visit_order.get((x, y))
    if num:
        text = font.render(str(num), True, (0, 0, 0))
        screen.blit(
            text,
            text.get_rect(center=(y * CELL + CELL//2, x * CELL + CELL//2))
        )

# ---------- 打印 depth ----------
def print_depth(x, y, depth):
    text = small_font.render(str(depth), True, (80, 80, 80))
    screen.blit(text, (y * CELL + 2, x * CELL + 2))

# ---------- 绘制 ----------
def draw(maze, visited, visit_order, current, current_depth,
         backtracking, backtrack_depth, path):

    screen.fill((20, 20, 20))

    # 迷宫格子
    for i in range(ROWS):
        for j in range(COLS):
            rect = (j * CELL, i * CELL, CELL, CELL)
            pygame.draw.rect(
                screen,
                BLACK if maze[i][j] == 1 else WHITE,
                rect
            )

    # 已访问节点
    for (x, y) in visited:
        pygame.draw.rect(screen, BLUE, (y * CELL, x * CELL, CELL, CELL))
        print_num(x, y, visit_order)

    # 当前递归节点
    if current:
        x, y = current
        pygame.draw.rect(screen, YELLOW, (y * CELL, x * CELL, CELL, CELL))
        print_num(x, y, visit_order)
        print_depth(x, y, current_depth)

    # 回溯动画
    if backtracking:
        x, y = backtracking
        t = min(backtrack_depth / 10, 1.0)
        color = (
            int(200 + 55 * t),
            int(200 - 120 * t),
            int(255 - 180 * t),
        )
        pygame.draw.rect(screen, color, (y * CELL, x * CELL, CELL, CELL))
        print_depth(x, y, backtrack_depth)

    # 最终路径（渐变色）
    if path:
        L = len(path)
        start_color = (100, 100, 255)
        end_color = (255, 80, 80)
        for i, (x, y) in enumerate(path):
            t = i / (L - 1) if L > 1 else 0
            color = (
                int(start_color[0] + (end_color[0] - start_color[0]) * t),
                int(start_color[1] + (end_color[1] - start_color[1]) * t),
                int(start_color[2] + (end_color[2] - start_color[2]) * t),
            )
            pygame.draw.rect(screen, color, (y * CELL, x * CELL, CELL, CELL))
            print_num(x, y, visit_order)

    # 起点 / 终点
    pygame.draw.rect(screen, GREEN, (start[1]*CELL, start[0]*CELL, CELL, CELL))
    pygame.draw.rect(screen, RED, (end[1]*CELL, end[0]*CELL, CELL, CELL))

    # ---------- 右侧 DFS 调用栈 ----------
    panel_x = WIDTH
    pygame.draw.rect(screen, (220,220,220), (panel_x, 0, STACK_WIDTH, HEIGHT))
    title = font.render("DFS Call Stack", True, (0,0,0))
    screen.blit(title, (panel_x + 10, 10))

    # 显示栈顶 25 个
    for i, ((x, y), depth) in enumerate(dfs_stack[-25:]):
        color = (255,0,0) if i == len(dfs_stack[-25:])-1 else (0,0,0)  # 栈顶红色
        text = font.render(f"{x},{y} : {depth}", True, color)
        screen.blit(text, (panel_x + 10, 40 + i*20))

    pygame.display.flip()

# ---------- 主循环 ----------
dfs_gen = dfs(maze, start, end)

visited = set()
visit_order = {}
current = None
current_depth = None
backtracking = None
backtrack_depth = None
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
            action, data, visited, visit_order, parent, depth = next(dfs_gen)

            if action == "visit":
                current = data
                current_depth = depth
                backtracking = None

            elif action == "backtrack":
                backtracking = data
                backtrack_depth = depth
                current = None

            elif action == "path":
                path = data
                current = None

        except StopIteration:
            pass

        step_once = False

    draw(
        maze, visited, visit_order,
        current, current_depth,
        backtracking, backtrack_depth,
        path
    )

    time.sleep(0.1)

pygame.quit()
