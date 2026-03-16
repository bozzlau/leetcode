import turtle
import random
import time

# ---------- 1. 初始化 ----------
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20

# 设置屏幕
screen = turtle.Screen()
screen.title("Snake Game V1 (Basic)")
screen.setup(width=WIDTH, height=HEIGHT)
screen.bgcolor("black")
screen.tracer(0)  # 关闭自动动画更新

# 颜色
screen.colormode(255)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLACK = (0, 0, 0)

# 绘图笔
pen = turtle.Turtle()
pen.hideturtle()
pen.penup()
pen.speed(0)
pen.shape("square")

# 坐标转换函数
def to_turtle_coords(x, y):
    tx = x - WIDTH // 2 + CELL_SIZE // 2
    ty = HEIGHT // 2 - y - CELL_SIZE // 2
    return tx, ty

# ---------- 2. 重新开始游戏的函数 ----------
def reset_game():
    global snake, direction, food, game_over
    snake = [(100, 100), (80, 100), (60, 100)]
    direction = (CELL_SIZE, 0)
    food = (
        random.randrange(0, WIDTH, CELL_SIZE),
        random.randrange(0, HEIGHT, CELL_SIZE)
    )
    game_over = False

# 初始化全局变量
snake = []
direction = (0, 0)
food = (0, 0)
game_over = False

reset_game()

# ---------- 3. 事件处理 ----------
def go_up():
    global direction
    if direction != (0, CELL_SIZE):
        direction = (0, -CELL_SIZE)

def go_down():
    global direction
    if direction != (0, -CELL_SIZE):
        direction = (0, CELL_SIZE)

def go_left():
    global direction
    if direction != (CELL_SIZE, 0):
        direction = (-CELL_SIZE, 0)

def go_right():
    global direction
    if direction != (-CELL_SIZE, 0):
        direction = (CELL_SIZE, 0)

def restart_game():
    if game_over:
        reset_game()

# 键盘监听
screen.listen()
screen.onkey(go_up, "Up")
screen.onkey(go_down, "Down")
screen.onkey(go_left, "Left")
screen.onkey(go_right, "Right")
screen.onkey(restart_game, "r")
screen.onkey(restart_game, "R")

# ---------- 4. 主循环 ----------
while True:
    try:
        # ---------- 4.1 游戏逻辑 ----------
        if not game_over:
            head_x, head_y = snake[0]
            new_head = (head_x + direction[0], head_y + direction[1])
            
            snake.insert(0, new_head)

            # 吃食物
            if new_head == food:
                food = (
                    random.randrange(0, WIDTH, CELL_SIZE),
                    random.randrange(0, HEIGHT, CELL_SIZE)
                )
            else:
                snake.pop()

            # 撞墙
            if (
                new_head[0] < 0 or new_head[0] >= WIDTH or
                new_head[1] < 0 or new_head[1] >= HEIGHT
            ):
                game_over = True

            # 撞自己
            if new_head in snake[1:]:
                game_over = True

        # ---------- 4.2 绘制 ----------
        pen.clear()

        # 画蛇
        pen.color(GREEN)
        for x, y in snake:
            tx, ty = to_turtle_coords(x, y)
            pen.goto(tx, ty)
            pen.stamp()

        # 画食物
        pen.color(RED)
        fx, fy = to_turtle_coords(food[0], food[1])
        pen.goto(fx, fy)
        pen.stamp()

        # 游戏结束提示
        if game_over:
            pen.color(WHITE)
            pen.goto(0, 0)
            pen.write("Game Over", align="center", font=("Arial", 36, "normal"))
            pen.goto(0, -40)
            pen.write("Press R to Restart", align="center", font=("Arial", 36, "normal"))

        screen.update()
        
        time.sleep(0.2)
        
    except turtle.Terminator:
        break
