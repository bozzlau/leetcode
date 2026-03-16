import turtle
import random
import time

# ---------- 1. 初始化 ----------
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20

# 设置屏幕
screen = turtle.Screen()
screen.title("Snake Game")
screen.setup(width=WIDTH, height=HEIGHT)
screen.bgcolor("black")
screen.tracer(0)  # 关闭自动动画更新

# 颜色
screen.colormode(255)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLACK = (0, 0, 0)

# 蛇的绘图笔
snake_pen = turtle.Turtle()
snake_pen.hideturtle()
snake_pen.penup()
snake_pen.speed(0)
snake_pen.shape("square")
snake_pen.color(GREEN)

# 食物的绘图笔
food_pen = turtle.Turtle()
food_pen.hideturtle()
food_pen.penup()
food_pen.speed(0)
food_pen.shape("square")
food_pen.color(RED)

# 提示文字笔
text_pen = turtle.Turtle()
text_pen.hideturtle()
text_pen.penup()
text_pen.speed(0)
text_pen.color(WHITE)

# 坐标转换函数
def to_turtle_coords(x, y):
    tx = x - WIDTH // 2 + CELL_SIZE // 2
    ty = HEIGHT // 2 - y - CELL_SIZE // 2
    return tx, ty

# 全局变量
snake = []
snake_stamps = []  # 存储蛇每节身体的stamp ID
direction = (0, 0)
food = (0, 0)
game_over = False
paused = False  # 暂停状态

# ---------- 2. 重新开始游戏的函数 ----------
def reset_game():
    global snake, snake_stamps, direction, food, game_over, paused
    
    # 清理旧画面
    snake_pen.clear()
    food_pen.clear()
    text_pen.clear()
    
    # 重置变量
    snake = [(100, 100), (80, 100), (60, 100)]
    snake_stamps = []
    direction = (CELL_SIZE, 0)
    game_over = False
    paused = False
    
    # 绘制初始蛇身 (并记录ID)
    for x, y in snake:
        tx, ty = to_turtle_coords(x, y)
        snake_pen.goto(tx, ty)
        snake_stamps.append(snake_pen.stamp())
        
    # 生成食物
    spawn_food()

def spawn_food():
    global food
    food = (
        random.randrange(0, WIDTH, CELL_SIZE),
        random.randrange(0, HEIGHT, CELL_SIZE)
    )
    # 绘制食物
    food_pen.clear()
    fx, fy = to_turtle_coords(food[0], food[1])
    food_pen.goto(fx, fy)
    food_pen.stamp()

reset_game()

# ---------- 3. 事件处理 ----------
# 使用 next_direction 缓存，防止一帧内多次按键导致逻辑错误
# 但为了保持原项目最简逻辑，这里直接修改 direction，
# 只要使用 onkeypress 就能大幅降低延迟感。
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

def toggle_pause():
    global paused
    if not game_over:  # 只有在游戏未结束时才能暂停
        paused = not paused
        if paused:
            text_pen.goto(0, 0)
            text_pen.write("PAUSED", align="center", font=("Arial", 36, "normal"))
            text_pen.goto(0, -40)
            text_pen.write("Press SPACE to Continue", align="center", font=("Arial", 20, "normal"))
        else:
            text_pen.clear()

# 键盘监听 (改用 onkeypress 以获得按下即响应的效果)
screen.listen()
screen.onkeypress(go_up, "Up")
screen.onkeypress(go_down, "Down")
screen.onkeypress(go_left, "Left")
screen.onkeypress(go_right, "Right")
screen.onkeypress(restart_game, "r")
screen.onkeypress(restart_game, "R")
screen.onkeypress(toggle_pause, "space")  # 空格键暂停/继续

# ---------- 4. 主循环 (使用 ontimer) ----------
def game_loop():
    global game_over 
    
    try:
        if not game_over and not paused:
            head_x, head_y = snake[0]
            new_head = (head_x + direction[0], head_y + direction[1])
            
            # --- 碰撞检测逻辑 ---
            # 撞墙
            if (
                new_head[0] < 0 or new_head[0] >= WIDTH or
                new_head[1] < 0 or new_head[1] >= HEIGHT
            ):
                game_over = True

            # 撞自己
            if new_head in snake[1:]:  # 注意：这里如果头撞到尾巴末端(即将移走的)，逻辑上可能需要微调，但维持原逻辑
                game_over = True
            
            if not game_over:
                # 更新数据结构
                snake.insert(0, new_head)
                
                # 绘制新头部
                tx, ty = to_turtle_coords(new_head[0], new_head[1])
                snake_pen.goto(tx, ty)
                new_stamp_id = snake_pen.stamp()
                snake_stamps.insert(0, new_stamp_id)

                # 吃食物判断
                if new_head == food:
                    spawn_food()
                else:
                    # 没吃到：移除尾部数据
                    snake.pop()
                    # 移除尾部绘图
                    tail_stamp_id = snake_stamps.pop()
                    snake_pen.clearstamp(tail_stamp_id)

            else:
                # 游戏结束显示
                text_pen.goto(0, 0)
                text_pen.write("Game Over", align="center", font=("Arial", 36, "normal"))
                text_pen.goto(0, -40)
                text_pen.write("Press R to Restart", align="center", font=("Arial", 36, "normal"))

        screen.update()
        
        # 频率控制
        # 因为绘制开销变小了，200ms会比较稳定
        screen.ontimer(game_loop, 200)

    except turtle.Terminator:
        pass
    except Exception:
        pass

# 启动循环
game_loop()

# 进入Tkinter主循环
screen.mainloop()
