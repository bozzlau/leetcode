import pygame
import random

# ---------- 初始化 ----------
pygame.init()
WIDTH, HEIGHT = 800, 450  # 减少高度给底部索引留空间
BAR_AREA_TOP = 40  # 柱子区域顶部（给数值留空间）
BAR_AREA_BOTTOM = 25  # 柱子区域底部（给索引留空间）
CONTROL_HEIGHT = 100  # 控制区域高度
screen = pygame.display.set_mode((WIDTH, HEIGHT + CONTROL_HEIGHT))
pygame.display.set_caption("Bubble Sort Visualization - 冒泡排序可视化")
clock = pygame.time.Clock()

# ---------- 字体 ----------
try:
    font = pygame.font.SysFont("pingfang", 18)
    small_font = pygame.font.SysFont("pingfang", 14)
    bar_font = pygame.font.SysFont("pingfang", 16, bold=True)  # 柱子标签字体（加粗加大）
except:
    font = pygame.font.Font(None, 24)
    small_font = pygame.font.Font(None, 18)
    bar_font = pygame.font.Font(None, 22)  # 柱子标签字体

# ---------- 颜色定义 ----------
BG_COLOR = (30, 30, 30)
BAR_COLOR = (100, 180, 255)
HIGHLIGHT_COLOR = (255, 80, 80)
SORTED_COLOR = (80, 255, 120)
BUTTON_COLOR = (70, 70, 90)
BUTTON_HOVER_COLOR = (90, 90, 120)
BUTTON_TEXT_COLOR = (255, 255, 255)
INPUT_BG_COLOR = (50, 50, 60)
INPUT_ACTIVE_COLOR = (70, 70, 100)

# ---------- 按钮类 ----------
class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.hovered = False
    
    def draw(self, surface):
        color = BUTTON_HOVER_COLOR if self.hovered else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, (100, 100, 120), self.rect, 2, border_radius=8)
        
        text_surface = font.render(self.text, True, BUTTON_TEXT_COLOR)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
    
    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)
        return self.hovered
    
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# ---------- 输入框类 ----------
class InputBox:
    def __init__(self, x, y, width, height, default_text="20"):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = default_text
        self.active = False
    
    def draw(self, surface):
        color = INPUT_ACTIVE_COLOR if self.active else INPUT_BG_COLOR
        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        pygame.draw.rect(surface, (100, 100, 120), self.rect, 2, border_radius=5)
        
        text_surface = font.render(self.text, True, BUTTON_TEXT_COLOR)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                self.active = False
            elif event.unicode.isdigit() and len(self.text) < 3:
                self.text += event.unicode
    
    def get_value(self):
        try:
            val = int(self.text)
            return max(5, min(100, val))  # 限制在5-100之间
        except:
            return 20

# ---------- 排序状态管理 ----------
class SortState:
    def __init__(self, n=20):
        self.n = n
        self.reset()
    
    def reset(self):
        """重置排序状态"""
        self.original_arr = [random.randint(30, HEIGHT - 50) for _ in range(self.n)]
        self.states = []  # 存储所有状态 (arr_copy, highlight, step_info)
        self.current_step = -1
        self.is_complete = False
        self._generate_all_states()
    
    def set_size(self, n):
        """设置数组大小并重置"""
        self.n = max(5, min(100, n))
        self.reset()
    
    def _generate_all_states(self):
        """预先生成所有排序状态（用于支持回退）"""
        arr = self.original_arr.copy()
        n = len(arr)
        
        # 初始状态
        self.states.append((arr.copy(), (), "初始状态"))
        
        for i in range(n):
            for j in range(n - i - 1):
                # 比较状态
                self.states.append((arr.copy(), (j, j + 1), f"比较 arr[{j}]={arr[j]} 和 arr[{j+1}]={arr[j+1]}"))
                
                if arr[j] > arr[j + 1]:
                    # 交换
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    self.states.append((arr.copy(), (j, j + 1), f"交换后: arr[{j}]={arr[j]}, arr[{j+1}]={arr[j+1]}"))
        
        # 完成状态
        self.states.append((arr.copy(), (), "排序完成！"))
    
    def next_step(self):
        """前进一步"""
        if self.current_step < len(self.states) - 1:
            self.current_step += 1
            if self.current_step == len(self.states) - 1:
                self.is_complete = True
        return self.get_current_state()
    
    def prev_step(self):
        """后退一步"""
        if self.current_step > 0:
            self.current_step -= 1
            self.is_complete = False
        return self.get_current_state()
    
    def get_current_state(self):
        """获取当前状态"""
        if 0 <= self.current_step < len(self.states):
            return self.states[self.current_step]
        return self.original_arr.copy(), (), "准备开始"
    
    def get_progress(self):
        """获取进度信息"""
        total = len(self.states) - 1
        current = max(0, self.current_step)
        return current, total

# ---------- 绘制函数 ----------
def draw_bars(arr, highlight=()):
    """绘制排序条形图"""
    bar_width = (WIDTH - 40) // len(arr)
    start_x = 20
    bar_area_height = HEIGHT - BAR_AREA_TOP - BAR_AREA_BOTTOM  # 可用于绘制柱子的高度
    
    # 计算最大值用于归一化
    max_val = max(arr) if arr else 1
    
    for i, val in enumerate(arr):
        if i in highlight:
            color = HIGHLIGHT_COLOR
        else:
            color = BAR_COLOR
        
        x = start_x + i * bar_width
        # 归一化高度
        normalized_height = int((val / max_val) * (bar_area_height - 10))
        normalized_height = max(10, normalized_height)  # 最小高度
        
        y = HEIGHT - BAR_AREA_BOTTOM - normalized_height
        w = bar_width - 2
        h = normalized_height
        
        # 绘制渐变效果的条形
        pygame.draw.rect(screen, color, (x, y, w, h), border_radius=3)
        
        # 顶部高亮
        lighter_color = tuple(min(255, c + 40) for c in color)
        pygame.draw.rect(screen, lighter_color, (x, y, w, 5), border_radius=3)
        
        # 绘制底部索引
        index_text = bar_font.render(str(i), True, (180, 180, 180))
        index_x = x + w // 2 - index_text.get_width() // 2
        index_y = HEIGHT - BAR_AREA_BOTTOM + 2
        screen.blit(index_text, (index_x, index_y))
        
        # 绘制顶部数值（只对高亮的柱子显示，避免拥挤）
        if i in highlight or len(arr) <= 15:
            val_text = bar_font.render(str(val), True, (255, 255, 100) if i in highlight else (150, 150, 150))
            val_x = x + w // 2 - val_text.get_width() // 2
            val_y = y - 20
            screen.blit(val_text, (val_x, val_y))

def draw_control_panel(buttons, input_box, sort_state):
    """绘制控制面板"""
    # 控制区域背景
    control_rect = pygame.Rect(0, HEIGHT, WIDTH, CONTROL_HEIGHT)
    pygame.draw.rect(screen, (40, 40, 50), control_rect)
    pygame.draw.line(screen, (80, 80, 100), (0, HEIGHT), (WIDTH, HEIGHT), 2)
    
    # 绘制按钮
    for btn in buttons:
        btn.draw(screen)
    
    # 绘制输入框标签（与按钮垂直对齐）
    label = font.render("数组长度:", True, (200, 200, 200))
    label_y = HEIGHT + 20 + (40 - label.get_height()) // 2  # 与按钮垂直居中对齐
    screen.blit(label, (450, label_y))
    input_box.draw(screen)
    
    # 绘制进度信息
    current, total = sort_state.get_progress()
    progress_text = f"步骤: {current} / {total}"
    progress_surface = small_font.render(progress_text, True, (200, 200, 200))
    screen.blit(progress_surface, (20, HEIGHT + 70))
    
    # 绘制当前步骤说明
    _, _, step_info = sort_state.get_current_state()
    info_surface = small_font.render(step_info, True, (255, 220, 100))
    screen.blit(info_surface, (150, HEIGHT + 70))

def draw_title():
    """绘制标题"""
    title = font.render("冒泡排序可视化 - Bubble Sort Visualization", True, (200, 200, 220))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 10))

# ---------- 主程序 ----------
def main():
    # 初始化排序状态
    sort_state = SortState(20)
    
    # 创建按钮
    btn_restart = Button(20, HEIGHT + 20, 100, 40, "重新开始")
    btn_prev = Button(140, HEIGHT + 20, 80, 40, "上一步")
    btn_next = Button(240, HEIGHT + 20, 80, 40, "下一步")
    btn_auto = Button(340, HEIGHT + 20, 80, 40, "自动播放")
    btn_apply = Button(700, HEIGHT + 20, 80, 40, "应用")
    
    buttons = [btn_restart, btn_prev, btn_next, btn_auto, btn_apply]
    
    # 创建输入框（与按钮垂直对齐）
    input_box = InputBox(550, HEIGHT + 20, 70, 40, "20")
    
    # 自动播放状态
    auto_play = False
    auto_timer = 0
    auto_delay = 450  # 毫秒
    
    running = True
    while running:
        dt = clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()
        
        # 更新按钮悬停状态
        for btn in buttons:
            btn.check_hover(mouse_pos)
        
        # 自动播放更新按钮文字
        btn_auto.text = "暂停" if auto_play else "自动播放"
        
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            input_box.handle_event(event)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_restart.is_clicked(event.pos):
                    sort_state.reset()
                    auto_play = False
                
                elif btn_prev.is_clicked(event.pos):
                    sort_state.prev_step()
                    auto_play = False
                
                elif btn_next.is_clicked(event.pos):
                    sort_state.next_step()
                
                elif btn_auto.is_clicked(event.pos):
                    auto_play = not auto_play
                    auto_timer = 0
                
                elif btn_apply.is_clicked(event.pos):
                    new_size = input_box.get_value()
                    sort_state.set_size(new_size)
                    input_box.text = str(new_size)
                    auto_play = False
            
            # 键盘快捷键
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    sort_state.prev_step()
                    auto_play = False
                elif event.key == pygame.K_RIGHT:
                    sort_state.next_step()
                elif event.key == pygame.K_SPACE:
                    auto_play = not auto_play
                    auto_timer = 0
                elif event.key == pygame.K_r:
                    sort_state.reset()
                    auto_play = False
        
        # 自动播放逻辑
        if auto_play and not sort_state.is_complete:
            auto_timer += dt
            if auto_timer >= auto_delay:
                sort_state.next_step()
                auto_timer = 0
        
        # 如果排序完成，停止自动播放
        if sort_state.is_complete:
            auto_play = False
        
        # 绘制
        screen.fill(BG_COLOR)
        draw_title()
        
        arr, highlight, _ = sort_state.get_current_state()
        draw_bars(arr, highlight)
        draw_control_panel(buttons, input_box, sort_state)
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()
