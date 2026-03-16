"""
DFS 迷宫寻路可视化 - 增强版
功能：
  - 空格键：暂停/继续
  - 左/右箭头：单步后退/前进
  - 上/下箭头：加速/减速
  - R 键：重新生成迷宫
  - 鼠标左键：添加/移除墙壁
  - ESC：退出
"""

import pygame
import random
import math
from dataclasses import dataclass
from typing import Optional, Generator, Tuple, Set, Dict, List

# ============================================================
# 配置类
# ============================================================
@dataclass
class Config:
    # 迷宫尺寸
    N: int = 8
    WIDTH: int = 640
    HEIGHT: int = 740  # 额外高度用于信息面板
    INFO_HEIGHT: int = 100
    
    # 颜色主题 - 现代暗色系（调亮版本）
    BG_COLOR: Tuple[int, int, int] = (45, 50, 65)
    GRID_COLOR: Tuple[int, int, int] = (60, 65, 80)
    WALL_COLOR: Tuple[int, int, int] = (35, 40, 55)
    PATH_COLOR: Tuple[int, int, int] = (248, 248, 242)
    
    VISITED_COLOR: Tuple[int, int, int] = (98, 114, 164)
    CURRENT_COLOR: Tuple[int, int, int] = (241, 250, 140)
    START_COLOR: Tuple[int, int, int] = (80, 250, 123)
    END_COLOR: Tuple[int, int, int] = (255, 85, 85)
    
    # 路径渐变
    PATH_START: Tuple[int, int, int] = (139, 233, 253)
    PATH_END: Tuple[int, int, int] = (255, 121, 198)
    
    # 文字颜色
    TEXT_COLOR: Tuple[int, int, int] = (248, 248, 242)
    TEXT_DARK: Tuple[int, int, int] = (30, 30, 30)
    
    # 动画
    BORDER_RADIUS: int = 6
    WALL_PROBABILITY: float = 0.25

# ============================================================
# DFS 可视化器主类
# ============================================================
class MazeVisualizer:
    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.cell_size = self.config.WIDTH // self.config.N
        self.maze_height = self.cell_size * self.config.N
        
        # Pygame 初始化
        pygame.init()
        self.screen = pygame.display.set_mode((self.config.WIDTH, self.config.HEIGHT))
        pygame.display.set_caption("🔍 DFS 迷宫可视化 - 增强版")
        self.clock = pygame.time.Clock()
        
        # 字体 - 使用支持中文的字体
        # macOS: PingFang SC, Hiragino Sans GB
        # Windows: Microsoft YaHei
        # Linux: WenQuanYi Micro Hei
        chinese_fonts = ["PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "WenQuanYi Micro Hei", "SimHei"]
        self.font_small = pygame.font.SysFont(chinese_fonts, 14)
        self.font_medium = pygame.font.SysFont(chinese_fonts, 18)
        self.font_large = pygame.font.SysFont(chinese_fonts, 24, bold=True)
        
        # 状态标记字体 (用于绘制圆形标记)
        self.font_status_icon = pygame.font.SysFont(chinese_fonts, 28, bold=True)
        
        # 起点和终点
        self.start = (0, 0)
        self.end = (self.config.N - 1, self.config.N - 1)
        
        # 状态
        self.speed = 10  # FPS
        self.paused = True
        self.step_once = False
        self.finished = False
        
        # 历史记录（用于回退）
        self.history: List[Tuple] = []
        self.history_index = -1
        
        # 初始化迷宫
        self.reset_maze()
    
    def generate_maze(self) -> List[List[int]]:
        """生成随机迷宫"""
        maze = [
            [0 if random.random() > self.config.WALL_PROBABILITY else 1 
             for _ in range(self.config.N)] 
            for _ in range(self.config.N)
        ]
        # 确保起点和终点是通路
        maze[self.start[0]][self.start[1]] = 0
        maze[self.end[0]][self.end[1]] = 0
        return maze
    
    def reset_maze(self):
        """重置迷宫和搜索状态"""
        self.maze = self.generate_maze()
        self.reset_search()
    
    def reset_search(self):
        """仅重置搜索状态（保留迷宫）"""
        self.visited: Set[Tuple[int, int]] = set()
        self.visit_order: Dict[Tuple[int, int], int] = {}
        self.parent: Dict[Tuple[int, int], Tuple[int, int]] = {}
        self.current: Optional[Tuple[int, int]] = None
        self.path: Optional[List[Tuple[int, int]]] = None
        self.finished = False
        self.dfs_gen = self.dfs()
        
        # 历史记录
        self.history = []
        self.history_index = -1
    
    def dfs(self) -> Generator:
        """DFS 生成器"""
        visited = set()
        parent = {}
        visit_order = {}
        step = 0
        found = False
        
        def dfs_visit(x: int, y: int):
            nonlocal step, found
            if found:
                return
            
            visited.add((x, y))
            step += 1
            visit_order[(x, y)] = step
            
            # 返回当前状态
            state = ("visit", (x, y), set(visited), dict(visit_order), dict(parent))
            yield state
            
            if (x, y) == self.end:
                # 构建路径
                path = []
                cur = self.end
                while cur != self.start:
                    path.append(cur)
                    cur = parent[cur]
                path.append(self.start)
                path.reverse()
                
                yield ("path", path, set(visited), dict(visit_order), dict(parent))
                found = True
                return
            
            # 四个方向：上、下、左、右
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.config.N and 0 <= ny < self.config.N:
                    if self.maze[nx][ny] == 0 and (nx, ny) not in visited:
                        parent[(nx, ny)] = (x, y)
                        yield from dfs_visit(nx, ny)
                        if found:
                            return
        
        yield from dfs_visit(self.start[0], self.start[1])
    
    def step_forward(self):
        """前进一步"""
        if self.finished:
            return
        
        # 如果可以从历史中前进
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self._apply_state(self.history[self.history_index])
            return
        
        # 否则从生成器获取新状态
        try:
            state = next(self.dfs_gen)
            self.history.append(state)
            self.history_index = len(self.history) - 1
            self._apply_state(state)
        except StopIteration:
            self.finished = True
    
    def step_backward(self):
        """后退一步"""
        if self.history_index > 0:
            self.history_index -= 1
            self._apply_state(self.history[self.history_index])
        elif self.history_index == 0:
            # 回到初始状态
            self.history_index = -1
            self.visited = set()
            self.visit_order = {}
            self.parent = {}
            self.current = None
            self.path = None
    
    def _apply_state(self, state: Tuple):
        """应用状态"""
        action, data, visited, visit_order, parent = state
        self.visited = visited
        self.visit_order = visit_order
        self.parent = parent
        
        if action == "visit":
            self.current = data
            self.path = None
            self.finished = False
        elif action == "path":
            self.path = data
            self.current = None
            self.finished = True
    
    def toggle_wall(self, pos: Tuple[int, int]):
        """切换墙壁状态"""
        x, y = pos
        if (x, y) == self.start or (x, y) == self.end:
            return  # 不能修改起点和终点
        
        self.maze[x][y] = 1 - self.maze[x][y]
        self.reset_search()
    
    def draw(self):
        """绘制所有内容"""
        self.screen.fill(self.config.BG_COLOR)
        
        self.draw_maze()
        self.draw_visited()
        self.draw_current()
        self.draw_path()
        self.draw_start_end()
        self.draw_grid()
        self.draw_info_panel()
        
        pygame.display.flip()
    
    def draw_maze(self):
        """绘制迷宫基础"""
        for i in range(self.config.N):
            for j in range(self.config.N):
                rect = pygame.Rect(
                    j * self.cell_size + 2, 
                    i * self.cell_size + 2,
                    self.cell_size - 4, 
                    self.cell_size - 4
                )
                if self.maze[i][j] == 1:
                    pygame.draw.rect(self.screen, self.config.WALL_COLOR, rect, 
                                   border_radius=self.config.BORDER_RADIUS)
                else:
                    pygame.draw.rect(self.screen, self.config.PATH_COLOR, rect, 
                                   border_radius=self.config.BORDER_RADIUS)
    
    def draw_visited(self):
        """绘制已访问节点"""
        for (x, y) in self.visited:
            if (x, y) == self.start or (x, y) == self.end:
                continue
            if self.path and (x, y) in self.path:
                continue
            
            rect = pygame.Rect(
                y * self.cell_size + 2, 
                x * self.cell_size + 2,
                self.cell_size - 4, 
                self.cell_size - 4
            )
            pygame.draw.rect(self.screen, self.config.VISITED_COLOR, rect, 
                           border_radius=self.config.BORDER_RADIUS)
            self._draw_order_number(x, y)
    
    def draw_current(self):
        """绘制当前节点（带脉冲动画）"""
        if not self.current:
            return
        
        x, y = self.current
        
        # 脉冲效果
        pulse = (math.sin(pygame.time.get_ticks() * 0.008) + 1) / 2
        size_offset = int(pulse * 6)
        
        rect = pygame.Rect(
            y * self.cell_size + 2 + size_offset,
            x * self.cell_size + 2 + size_offset,
            self.cell_size - 4 - size_offset * 2,
            self.cell_size - 4 - size_offset * 2
        )
        
        # 发光效果
        glow_color = (
            min(255, self.config.CURRENT_COLOR[0] + 30),
            min(255, self.config.CURRENT_COLOR[1] + 30),
            min(255, self.config.CURRENT_COLOR[2])
        )
        pygame.draw.rect(self.screen, glow_color, rect, 
                        border_radius=self.config.BORDER_RADIUS + 2)
        
        self._draw_order_number(x, y)
    
    def draw_path(self):
        """绘制最终路径（渐变色）"""
        if not self.path:
            return
        
        L = len(self.path)
        for i, (x, y) in enumerate(self.path):
            if (x, y) == self.start or (x, y) == self.end:
                continue
            
            t = i / (L - 1) if L > 1 else 0
            color = (
                int(self.config.PATH_START[0] + (self.config.PATH_END[0] - self.config.PATH_START[0]) * t),
                int(self.config.PATH_START[1] + (self.config.PATH_END[1] - self.config.PATH_START[1]) * t),
                int(self.config.PATH_START[2] + (self.config.PATH_END[2] - self.config.PATH_START[2]) * t),
            )
            
            rect = pygame.Rect(
                y * self.cell_size + 2,
                x * self.cell_size + 2,
                self.cell_size - 4,
                self.cell_size - 4
            )
            pygame.draw.rect(self.screen, color, rect, 
                           border_radius=self.config.BORDER_RADIUS)
            self._draw_order_number(x, y)
    
    def draw_start_end(self):
        """绘制起点和终点"""
        # 起点
        rect = pygame.Rect(
            self.start[1] * self.cell_size + 2,
            self.start[0] * self.cell_size + 2,
            self.cell_size - 4,
            self.cell_size - 4
        )
        pygame.draw.rect(self.screen, self.config.START_COLOR, rect, 
                        border_radius=self.config.BORDER_RADIUS)
        self._draw_label(self.start[0], self.start[1], "S")
        
        # 终点
        rect = pygame.Rect(
            self.end[1] * self.cell_size + 2,
            self.end[0] * self.cell_size + 2,
            self.cell_size - 4,
            self.cell_size - 4
        )
        pygame.draw.rect(self.screen, self.config.END_COLOR, rect, 
                        border_radius=self.config.BORDER_RADIUS)
        self._draw_label(self.end[0], self.end[1], "E")
    
    def draw_grid(self):
        """绘制网格线"""
        for i in range(self.config.N + 1):
            # 水平线
            pygame.draw.line(
                self.screen, self.config.GRID_COLOR,
                (0, i * self.cell_size),
                (self.config.WIDTH, i * self.cell_size),
                1
            )
            # 垂直线
            pygame.draw.line(
                self.screen, self.config.GRID_COLOR,
                (i * self.cell_size, 0),
                (i * self.cell_size, self.maze_height),
                1
            )
    
    def draw_info_panel(self):
        """绘制信息面板"""
        panel_y = self.maze_height + 5
        
        # 面板背景
        panel_rect = pygame.Rect(0, panel_y, self.config.WIDTH, self.config.INFO_HEIGHT)
        pygame.draw.rect(self.screen, (30, 32, 44), panel_rect)
        
        # 状态标记颜色和文字
        icon_center = (25, panel_y + 22)
        icon_radius = 15
        dark_color = (30, 30, 30)
        
        if self.finished:
            if self.path:
                icon_color = (80, 250, 123)  # 绿色
                status = f"找到路径! 长度: {len(self.path)}"
                icon_type = "check"
            else:
                icon_color = (255, 85, 85)  # 红色
                status = "无法到达终点"
                icon_type = "cross"
        else:
            if self.paused:
                icon_color = (241, 250, 140)  # 黄色
                status = "暂停中"
                icon_type = "pause"
            else:
                icon_color = (139, 233, 253)  # 青色
                status = "运行中"
                icon_type = "play"
        
        # 绘制圆形背景
        pygame.draw.circle(self.screen, icon_color, icon_center, icon_radius)
        
        # 根据状态绘制不同图标
        cx, cy = icon_center
        if icon_type == "play":
            # 播放三角形 ▶
            points = [
                (cx - 5, cy - 8),
                (cx - 5, cy + 8),
                (cx + 8, cy)
            ]
            pygame.draw.polygon(self.screen, dark_color, points)
        elif icon_type == "pause":
            # 暂停双竖线 ‖
            pygame.draw.rect(self.screen, dark_color, (cx - 6, cy - 7, 4, 14))
            pygame.draw.rect(self.screen, dark_color, (cx + 2, cy - 7, 4, 14))
        elif icon_type == "check":
            # 对勾 √
            pygame.draw.lines(self.screen, dark_color, False, [
                (cx - 7, cy),
                (cx - 2, cy + 6),
                (cx + 8, cy - 6)
            ], 3)
        elif icon_type == "cross":
            # 叉号 X
            pygame.draw.line(self.screen, dark_color, (cx - 6, cy - 6), (cx + 6, cy + 6), 3)
            pygame.draw.line(self.screen, dark_color, (cx + 6, cy - 6), (cx - 6, cy + 6), 3)
        
        # 绘制状态文字
        status_text = self.font_large.render(status, True, self.config.TEXT_COLOR)
        self.screen.blit(status_text, (50, panel_y + 10))
        
        # 统计信息
        stats = f"已访问: {len(self.visited)}  |  速度: {self.speed} FPS  |  步骤: {self.history_index + 1}/{len(self.history)}"
        stats_text = self.font_medium.render(stats, True, (180, 180, 180))
        self.screen.blit(stats_text, (15, panel_y + 45))
        
        # 快捷键提示
        hints = "Space:暂停  Left/Right:单步  Up/Down:速度  R:重置  Click:编辑墙壁"
        hints_text = self.font_small.render(hints, True, (150, 150, 170))
        self.screen.blit(hints_text, (15, panel_y + 72))
    
    def _draw_order_number(self, x: int, y: int):
        """绘制访问顺序数字"""
        num = self.visit_order.get((x, y))
        if num:
            text = self.font_small.render(str(num), True, self.config.TEXT_DARK)
            rect = text.get_rect(center=(
                y * self.cell_size + self.cell_size // 2,
                x * self.cell_size + self.cell_size // 2
            ))
            self.screen.blit(text, rect)
    
    def _draw_label(self, x: int, y: int, label: str):
        """绘制标签（S/E）"""
        text = self.font_large.render(label, True, self.config.TEXT_DARK)
        rect = text.get_rect(center=(
            y * self.cell_size + self.cell_size // 2,
            x * self.cell_size + self.cell_size // 2
        ))
        self.screen.blit(text, rect)
    
    def handle_events(self) -> bool:
        """处理事件，返回是否继续运行"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pygame.K_RIGHT:
                    self.step_once = True
                elif event.key == pygame.K_LEFT:
                    self.step_backward()
                elif event.key == pygame.K_UP:
                    self.speed = min(60, self.speed + 5)
                elif event.key == pygame.K_DOWN:
                    self.speed = max(1, self.speed - 5)
                elif event.key == pygame.K_r:
                    self.reset_maze()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 左键
                    mx, my = event.pos
                    if my < self.maze_height:  # 在迷宫区域内
                        grid_x = my // self.cell_size
                        grid_y = mx // self.cell_size
                        if 0 <= grid_x < self.config.N and 0 <= grid_y < self.config.N:
                            self.toggle_wall((grid_x, grid_y))
        
        return True
    
    def run(self):
        """主循环"""
        running = True
        
        while running:
            self.clock.tick(60)  # UI 刷新保持 60 FPS
            
            running = self.handle_events()
            
            # 控制搜索速度
            if not self.paused or self.step_once:
                if pygame.time.get_ticks() % max(1, 60 // self.speed) == 0 or self.step_once:
                    self.step_forward()
                    self.step_once = False
            
            self.draw()
        
        pygame.quit()


# ============================================================
# 入口
# ============================================================
if __name__ == "__main__":
    config = Config(
        N=6,           # 8x8 迷宫
        WIDTH=640,
        HEIGHT=740,    # 包含信息面板的总高度
    )
    
    visualizer = MazeVisualizer(config)
    visualizer.run()
