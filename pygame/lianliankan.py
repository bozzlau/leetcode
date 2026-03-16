"""
连连看游戏 - Python + Pygame 实现
作者: Antigravity AI
功能: 经典连连看游戏，支持提示、重排、计时等功能
"""

import pygame
import random
import sys
from collections import deque
from typing import List, Tuple, Optional
import time
import math

# 初始化 Pygame
pygame.init()
pygame.mixer.init()

# 颜色定义 - 现代配色方案
COLORS = {
    'background': (25, 25, 35),
    'board_bg': (35, 35, 50),
    'tile_bg': (60, 60, 80),
    'tile_hover': (80, 80, 110),
    'tile_selected': (100, 150, 255),
    'text': (255, 255, 255),
    'text_secondary': (180, 180, 200),
    'accent': (100, 200, 255),
    'success': (100, 255, 150),
    'warning': (255, 200, 100),
    'error': (255, 100, 100),
    'button': (70, 130, 200),
    'button_hover': (90, 150, 220),
    'line': (100, 200, 255),
}

# 图案类型和颜色 - 用于绘制不同的几何图形
PATTERNS = [
    {'type': 'star', 'color': (255, 215, 0)},       # 金星
    {'type': 'heart', 'color': (255, 100, 120)},    # 红心
    {'type': 'diamond', 'color': (100, 200, 255)},  # 钻石
    {'type': 'club', 'color': (100, 255, 150)},     # 梅花
    {'type': 'spade', 'color': (200, 180, 255)},    # 黑桃
    {'type': 'circle', 'color': (255, 150, 100)},   # 圆形
    {'type': 'square', 'color': (150, 255, 200)},   # 方块
    {'type': 'triangle', 'color': (255, 200, 150)}, # 三角
    {'type': 'hexagon', 'color': (200, 150, 255)},  # 六边形
    {'type': 'flower', 'color': (255, 180, 200)},   # 花朵
    {'type': 'sun', 'color': (255, 220, 100)},      # 太阳
    {'type': 'moon', 'color': (180, 200, 255)},     # 月亮
    {'type': 'bolt', 'color': (255, 255, 100)},     # 闪电
    {'type': 'snowflake', 'color': (200, 230, 255)},# 雪花
    {'type': 'cross', 'color': (255, 150, 200)},    # 十字
    {'type': 'ring', 'color': (200, 255, 200)},     # 圆环
]

# 游戏配置
class GameConfig:
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 700
    BOARD_ROWS = 8
    BOARD_COLS = 12
    TILE_SIZE = 55
    TILE_MARGIN = 3
    BOARD_OFFSET_X = 80
    BOARD_OFFSET_Y = 120
    FPS = 60
    PATTERN_COUNT = 16  # 使用的图案种类数


def get_chinese_font(size: int) -> pygame.font.Font:
    """获取支持中文的字体"""
    # macOS 系统中文字体文件路径
    font_paths = [
        '/System/Library/Fonts/PingFang.ttc',
        '/System/Library/Fonts/STHeiti Medium.ttc',
        '/System/Library/Fonts/STHeiti Light.ttc',
        '/System/Library/Fonts/Hiragino Sans GB.ttc',
        '/Library/Fonts/Arial Unicode.ttf',
        '/System/Library/Fonts/Supplemental/Arial Unicode.ttf',
    ]
    
    for font_path in font_paths:
        try:
            font = pygame.font.Font(font_path, size)
            # 测试是否能正确渲染中文
            test_surface = font.render("测试", True, (255, 255, 255))
            if test_surface.get_width() > 10:  # 如果渲染成功
                return font
        except Exception as e:
            continue
    
    # 尝试使用 SysFont
    chinese_fonts = ['PingFang SC', 'Heiti SC', 'STHeiti', 'Hiragino Sans GB']
    for font_name in chinese_fonts:
        try:
            font = pygame.font.SysFont(font_name, size)
            test_surface = font.render("测试", True, (255, 255, 255))
            if test_surface.get_width() > 10:
                return font
        except:
            continue
    
    # 如果都失败了，返回默认字体
    return pygame.font.Font(None, size)


class Tile:
    """方块类"""
    def __init__(self, row: int, col: int, pattern_id: int):
        self.row = row
        self.col = col
        self.pattern_id = pattern_id
        self.visible = True
        self.selected = False
        self.hover = False
        self.animation_scale = 1.0
        self.fade_alpha = 255
        
    def get_rect(self) -> pygame.Rect:
        """获取方块的矩形区域"""
        x = GameConfig.BOARD_OFFSET_X + self.col * (GameConfig.TILE_SIZE + GameConfig.TILE_MARGIN)
        y = GameConfig.BOARD_OFFSET_Y + self.row * (GameConfig.TILE_SIZE + GameConfig.TILE_MARGIN)
        return pygame.Rect(x, y, GameConfig.TILE_SIZE, GameConfig.TILE_SIZE)


class Button:
    """按钮类"""
    def __init__(self, x: int, y: int, width: int, height: int, text: str, color: Tuple[int, int, int]):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover = False
        self.enabled = True
        
    def draw(self, screen: pygame.Surface, font: pygame.font.Font):
        """绘制按钮"""
        color = self.color if not self.hover else tuple(min(c + 30, 255) for c in self.color)
        if not self.enabled:
            color = tuple(c // 2 for c in self.color)
        
        # 绘制按钮背景（带圆角效果）
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        pygame.draw.rect(screen, COLORS['accent'], self.rect, 2, border_radius=8)
        
        # 绘制文字
        text_surface = font.render(self.text, True, COLORS['text'])
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def is_clicked(self, pos: Tuple[int, int]) -> bool:
        """检查是否被点击"""
        return self.rect.collidepoint(pos) and self.enabled


class ShapeDrawer:
    """图形绘制器 - 用于绘制各种几何图形"""
    
    @staticmethod
    def draw_star(screen, center, size, color, points=5):
        """绘制五角星"""
        cx, cy = center
        outer_r = size
        inner_r = size * 0.4
        pts = []
        for i in range(points * 2):
            angle = math.pi / 2 + i * math.pi / points
            r = outer_r if i % 2 == 0 else inner_r
            x = cx + r * math.cos(angle)
            y = cy - r * math.sin(angle)
            pts.append((x, y))
        pygame.draw.polygon(screen, color, pts)
    
    @staticmethod
    def draw_heart(screen, center, size, color):
        """绘制心形"""
        cx, cy = center
        pts = []
        for i in range(360):
            t = math.radians(i)
            x = 16 * (math.sin(t) ** 3)
            y = 13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t)
            pts.append((cx + x * size / 18, cy - y * size / 18))
        pygame.draw.polygon(screen, color, pts)
    
    @staticmethod
    def draw_diamond(screen, center, size, color):
        """绘制菱形"""
        cx, cy = center
        pts = [
            (cx, cy - size),
            (cx + size * 0.6, cy),
            (cx, cy + size),
            (cx - size * 0.6, cy),
        ]
        pygame.draw.polygon(screen, color, pts)
    
    @staticmethod
    def draw_club(screen, center, size, color):
        """绘制梅花"""
        cx, cy = center
        r = size * 0.35
        # 三个圆
        pygame.draw.circle(screen, color, (int(cx), int(cy - size * 0.35)), int(r))
        pygame.draw.circle(screen, color, (int(cx - size * 0.35), int(cy + size * 0.15)), int(r))
        pygame.draw.circle(screen, color, (int(cx + size * 0.35), int(cy + size * 0.15)), int(r))
        # 茎
        pts = [
            (cx - size * 0.12, cy + size * 0.1),
            (cx + size * 0.12, cy + size * 0.1),
            (cx + size * 0.08, cy + size * 0.7),
            (cx - size * 0.08, cy + size * 0.7),
        ]
        pygame.draw.polygon(screen, color, pts)
    
    @staticmethod
    def draw_spade(screen, center, size, color):
        """绘制黑桃"""
        cx, cy = center
        # 上半部分 - 倒心形
        pts = []
        for i in range(360):
            t = math.radians(i)
            x = 16 * (math.sin(t) ** 3)
            y = 13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t)
            pts.append((cx + x * size / 22, cy + y * size / 22 - size * 0.1))
        pygame.draw.polygon(screen, color, pts)
        # 茎
        stem_pts = [
            (cx - size * 0.1, cy + size * 0.2),
            (cx + size * 0.1, cy + size * 0.2),
            (cx + size * 0.06, cy + size * 0.7),
            (cx - size * 0.06, cy + size * 0.7),
        ]
        pygame.draw.polygon(screen, color, stem_pts)
    
    @staticmethod
    def draw_circle(screen, center, size, color):
        """绘制实心圆"""
        pygame.draw.circle(screen, color, center, int(size))
    
    @staticmethod
    def draw_square(screen, center, size, color):
        """绘制正方形"""
        cx, cy = center
        half = size * 0.8
        pygame.draw.rect(screen, color, (cx - half, cy - half, half * 2, half * 2))
    
    @staticmethod
    def draw_triangle(screen, center, size, color):
        """绘制三角形"""
        cx, cy = center
        pts = [
            (cx, cy - size),
            (cx - size * 0.9, cy + size * 0.7),
            (cx + size * 0.9, cy + size * 0.7),
        ]
        pygame.draw.polygon(screen, color, pts)
    
    @staticmethod
    def draw_hexagon(screen, center, size, color):
        """绘制六边形"""
        cx, cy = center
        pts = []
        for i in range(6):
            angle = math.pi / 6 + i * math.pi / 3
            x = cx + size * math.cos(angle)
            y = cy + size * math.sin(angle)
            pts.append((x, y))
        pygame.draw.polygon(screen, color, pts)
    
    @staticmethod
    def draw_flower(screen, center, size, color):
        """绘制花朵"""
        cx, cy = center
        # 5个花瓣
        petal_r = size * 0.4
        for i in range(5):
            angle = i * 2 * math.pi / 5 - math.pi / 2
            px = cx + size * 0.5 * math.cos(angle)
            py = cy + size * 0.5 * math.sin(angle)
            pygame.draw.circle(screen, color, (int(px), int(py)), int(petal_r))
        # 中心
        pygame.draw.circle(screen, (255, 230, 150), (int(cx), int(cy)), int(size * 0.25))
    
    @staticmethod
    def draw_sun(screen, center, size, color):
        """绘制太阳"""
        cx, cy = center
        # 中心圆
        pygame.draw.circle(screen, color, center, int(size * 0.5))
        # 光芒
        for i in range(8):
            angle = i * math.pi / 4
            x1 = cx + size * 0.55 * math.cos(angle)
            y1 = cy + size * 0.55 * math.sin(angle)
            x2 = cx + size * math.cos(angle)
            y2 = cy + size * math.sin(angle)
            pygame.draw.line(screen, color, (x1, y1), (x2, y2), 3)
    
    @staticmethod
    def draw_moon(screen, center, size, color):
        """绘制月亮"""
        cx, cy = center
        # 主圆
        pygame.draw.circle(screen, color, center, int(size))
        # 遮挡圆（用背景色）
        pygame.draw.circle(screen, COLORS['tile_bg'], (int(cx + size * 0.4), int(cy - size * 0.1)), int(size * 0.8))
    
    @staticmethod
    def draw_bolt(screen, center, size, color):
        """绘制闪电"""
        cx, cy = center
        pts = [
            (cx + size * 0.2, cy - size),
            (cx - size * 0.3, cy - size * 0.1),
            (cx + size * 0.1, cy - size * 0.1),
            (cx - size * 0.3, cy + size),
            (cx + size * 0.1, cy + size * 0.1),
            (cx + size * 0.4, cy + size * 0.1),
        ]
        pygame.draw.polygon(screen, color, pts)
    
    @staticmethod
    def draw_snowflake(screen, center, size, color):
        """绘制雪花"""
        cx, cy = center
        for i in range(6):
            angle = i * math.pi / 3
            x1 = cx
            y1 = cy
            x2 = cx + size * math.cos(angle)
            y2 = cy + size * math.sin(angle)
            pygame.draw.line(screen, color, (x1, y1), (x2, y2), 2)
            # 分支
            for j in [-0.4, 0.4]:
                bx = cx + size * 0.6 * math.cos(angle)
                by = cy + size * 0.6 * math.sin(angle)
                bx2 = bx + size * 0.35 * math.cos(angle + j * math.pi)
                by2 = by + size * 0.35 * math.sin(angle + j * math.pi)
                pygame.draw.line(screen, color, (bx, by), (bx2, by2), 2)
    
    @staticmethod
    def draw_cross(screen, center, size, color):
        """绘制十字"""
        cx, cy = center
        w = size * 0.35
        pygame.draw.rect(screen, color, (cx - w, cy - size, w * 2, size * 2))
        pygame.draw.rect(screen, color, (cx - size, cy - w, size * 2, w * 2))
    
    @staticmethod
    def draw_ring(screen, center, size, color):
        """绘制圆环"""
        pygame.draw.circle(screen, color, center, int(size), 4)
        pygame.draw.circle(screen, color, center, int(size * 0.5), 4)
    
    @classmethod
    def draw_pattern(cls, screen, center, size, pattern_type, color):
        """根据类型绘制图案"""
        draw_methods = {
            'star': cls.draw_star,
            'heart': cls.draw_heart,
            'diamond': cls.draw_diamond,
            'club': cls.draw_club,
            'spade': cls.draw_spade,
            'circle': cls.draw_circle,
            'square': cls.draw_square,
            'triangle': cls.draw_triangle,
            'hexagon': cls.draw_hexagon,
            'flower': cls.draw_flower,
            'sun': cls.draw_sun,
            'moon': cls.draw_moon,
            'bolt': cls.draw_bolt,
            'snowflake': cls.draw_snowflake,
            'cross': cls.draw_cross,
            'ring': cls.draw_ring,
        }
        
        if pattern_type in draw_methods:
            draw_methods[pattern_type](screen, center, size, color)
        else:
            # 默认绘制圆形
            pygame.draw.circle(screen, color, center, int(size))


class LianLianKan:
    """连连看游戏主类"""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((GameConfig.SCREEN_WIDTH, GameConfig.SCREEN_HEIGHT))
        pygame.display.set_caption("连连看游戏 - Python版")
        
        # 加载中文字体
        self.font_large = get_chinese_font(42)
        self.font_medium = get_chinese_font(28)
        self.font_small = get_chinese_font(22)
        
        self.clock = pygame.time.Clock()
        
        # 游戏状态
        self.board: List[List[Optional[Tile]]] = []
        self.selected_tile: Optional[Tile] = None
        self.score = 0
        self.combo = 0
        self.max_combo = 0
        self.remaining_pairs = 0
        self.start_time = 0
        self.elapsed_time = 0
        self.game_over = False
        self.game_won = False
        self.hints_used = 0
        self.shuffles_used = 0
        
        # 动画相关
        self.connection_path: List[Tuple[int, int]] = []
        self.path_timer = 0
        self.removing_tiles: List[Tile] = []
        
        # 创建按钮
        btn_y = 50
        btn_width = 100
        btn_height = 35
        self.btn_restart = Button(GameConfig.SCREEN_WIDTH - 360, btn_y, btn_width, btn_height, "重新开始", COLORS['button'])
        self.btn_hint = Button(GameConfig.SCREEN_WIDTH - 240, btn_y, btn_width, btn_height, "提示", COLORS['button'])
        self.btn_shuffle = Button(GameConfig.SCREEN_WIDTH - 120, btn_y, btn_width, btn_height, "重排", COLORS['button'])
        
        # 游戏结束弹框内的重新开始按钮
        self.btn_restart_popup = None  # 将在draw_game_over中动态设置位置
        
        # 初始化游戏
        self.init_game()
        
    def init_game(self):
        """初始化游戏"""
        self.board = [[None for _ in range(GameConfig.BOARD_COLS)] 
                      for _ in range(GameConfig.BOARD_ROWS)]
        self.selected_tile = None
        self.score = 0
        self.combo = 0
        self.max_combo = 0
        self.start_time = time.time()
        self.elapsed_time = 0
        self.game_over = False
        self.game_won = False
        self.hints_used = 0
        self.shuffles_used = 0
        self.connection_path = []
        self.path_timer = 0
        self.removing_tiles = []
        
        # 生成配对的图案
        total_tiles = GameConfig.BOARD_ROWS * GameConfig.BOARD_COLS
        pairs_needed = total_tiles // 2
        
        # 创建配对的图案ID列表
        pattern_ids = []
        patterns_per_type = pairs_needed // GameConfig.PATTERN_COUNT
        extra_pairs = pairs_needed % GameConfig.PATTERN_COUNT
        
        for i in range(GameConfig.PATTERN_COUNT):
            count = patterns_per_type + (1 if i < extra_pairs else 0)
            pattern_ids.extend([i] * count * 2)  # 每种图案成对
        
        # 随机打乱
        random.shuffle(pattern_ids)
        
        # 填充棋盘
        idx = 0
        for row in range(GameConfig.BOARD_ROWS):
            for col in range(GameConfig.BOARD_COLS):
                if idx < len(pattern_ids):
                    self.board[row][col] = Tile(row, col, pattern_ids[idx])
                    idx += 1
        
        self.remaining_pairs = pairs_needed
        
    def get_tile_at_pos(self, pos: Tuple[int, int]) -> Optional[Tile]:
        """获取鼠标位置对应的方块"""
        for row in self.board:
            for tile in row:
                if tile and tile.visible and tile.get_rect().collidepoint(pos):
                    return tile
        return None
    
    def can_connect(self, tile1: Tile, tile2: Tile) -> List[Tuple[int, int]]:
        """检查两个方块是否可以连接，返回连接路径"""
        if tile1.pattern_id != tile2.pattern_id:
            return []
        if tile1 == tile2:
            return []
        
        # BFS 寻找路径（最多两次转弯）
        rows = GameConfig.BOARD_ROWS + 2  # 包含边界外的路径
        cols = GameConfig.BOARD_COLS + 2
        
        # 坐标转换（加1是因为有边界）
        start = (tile1.row + 1, tile1.col + 1)
        end = (tile2.row + 1, tile2.col + 1)
        
        # 创建可通行地图
        passable = [[True for _ in range(cols)] for _ in range(rows)]
        for row in range(GameConfig.BOARD_ROWS):
            for col in range(GameConfig.BOARD_COLS):
                if self.board[row][col] and self.board[row][col].visible:
                    passable[row + 1][col + 1] = False
        
        # 起点和终点设为可通行
        passable[start[0]][start[1]] = True
        passable[end[0]][end[1]] = True
        
        # BFS: (row, col, direction, turns, path)
        # direction: 0=none, 1=up, 2=down, 3=left, 4=right
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # 左右上下
        
        queue = deque()
        visited = {}  # (row, col, direction) -> min_turns
        
        # 从起点向四个方向开始
        for d, (dr, dc) in enumerate(directions):
            queue.append((start[0], start[1], d, 0, [start]))
            visited[(start[0], start[1], d)] = 0
        
        while queue:
            r, c, direction, turns, path = queue.popleft()
            
            if (r, c) == end:
                # 转换回原始坐标
                return [(p[0] - 1, p[1] - 1) for p in path]
            
            for d, (dr, dc) in enumerate(directions):
                nr, nc = r + dr, c + dc
                
                if 0 <= nr < rows and 0 <= nc < cols and passable[nr][nc]:
                    new_turns = turns + (1 if d != direction else 0)
                    
                    if new_turns <= 2:
                        state = (nr, nc, d)
                        if state not in visited or visited[state] > new_turns:
                            visited[state] = new_turns
                            queue.append((nr, nc, d, new_turns, path + [(nr, nc)]))
        
        return []
    
    def find_hint(self) -> Optional[Tuple[Tile, Tile]]:
        """找到一对可消除的方块"""
        visible_tiles = []
        for row in self.board:
            for tile in row:
                if tile and tile.visible:
                    visible_tiles.append(tile)
        
        for i, tile1 in enumerate(visible_tiles):
            for tile2 in visible_tiles[i + 1:]:
                if tile1.pattern_id == tile2.pattern_id:
                    path = self.can_connect(tile1, tile2)
                    if path:
                        return (tile1, tile2)
        return None
    
    def shuffle_board(self):
        """重新排列棋盘上的方块"""
        visible_tiles = []
        positions = []
        
        for row in range(GameConfig.BOARD_ROWS):
            for col in range(GameConfig.BOARD_COLS):
                tile = self.board[row][col]
                if tile and tile.visible:
                    visible_tiles.append(tile.pattern_id)
                    positions.append((row, col))
        
        # 随机打乱图案
        random.shuffle(visible_tiles)
        
        # 重新分配
        for i, (row, col) in enumerate(positions):
            self.board[row][col].pattern_id = visible_tiles[i]
        
        self.shuffles_used += 1
        
    def remove_tiles(self, tile1: Tile, tile2: Tile, path: List[Tuple[int, int]]):
        """移除一对方块"""
        tile1.visible = False
        tile2.visible = False
        self.remaining_pairs -= 1
        
        # 计算分数
        self.combo += 1
        if self.combo > self.max_combo:
            self.max_combo = self.combo
        
        base_score = 100
        combo_bonus = (self.combo - 1) * 20
        self.score += base_score + combo_bonus
        
        # 保存路径用于动画
        self.connection_path = path
        self.path_timer = 20  # 显示20帧
        
        # 检查游戏是否结束
        if self.remaining_pairs == 0:
            self.game_won = True
            self.game_over = True
            
    def handle_click(self, pos: Tuple[int, int]):
        """处理鼠标点击"""
        # 检查顶部重新开始按钮（始终可点击）
        if self.btn_restart.is_clicked(pos):
            self.init_game()
            return
        
        # 游戏结束时，检查弹框内的重新开始按钮
        if self.game_over:
            if self.btn_restart_popup and self.btn_restart_popup.is_clicked(pos):
                self.init_game()
            return
        
        # 检查按钮点击
        if self.btn_hint.is_clicked(pos):
            hint = self.find_hint()
            if hint:
                self.hints_used += 1
                tile1, tile2 = hint
                tile1.selected = True
                tile2.selected = True
                # 短暂显示后取消选中
                pygame.time.set_timer(pygame.USEREVENT, 500)
            return
        
        if self.btn_shuffle.is_clicked(pos):
            self.shuffle_board()
            self.selected_tile = None
            self.combo = 0
            return
        
        # 检查方块点击
        tile = self.get_tile_at_pos(pos)
        if tile:
            if self.selected_tile is None:
                self.selected_tile = tile
                tile.selected = True
            elif self.selected_tile == tile:
                tile.selected = False
                self.selected_tile = None
            else:
                # 尝试匹配
                path = self.can_connect(self.selected_tile, tile)
                if path:
                    self.remove_tiles(self.selected_tile, tile, path)
                    self.selected_tile.selected = False
                    self.selected_tile = None
                else:
                    # 不能连接，取消选中第一个，选中新的
                    self.selected_tile.selected = False
                    self.selected_tile = tile
                    tile.selected = True
                    self.combo = 0
                    
    def handle_mouse_motion(self, pos: Tuple[int, int]):
        """处理鼠标移动"""
        # 更新按钮悬停状态
        self.btn_restart.hover = self.btn_restart.rect.collidepoint(pos)
        self.btn_hint.hover = self.btn_hint.rect.collidepoint(pos)
        self.btn_shuffle.hover = self.btn_shuffle.rect.collidepoint(pos)
        
        # 更新弹框内按钮悬停状态
        if self.btn_restart_popup:
            self.btn_restart_popup.hover = self.btn_restart_popup.rect.collidepoint(pos)
        
        # 更新方块悬停状态
        for row in self.board:
            for tile in row:
                if tile and tile.visible:
                    tile.hover = tile.get_rect().collidepoint(pos)
                    
    def draw_tile(self, tile: Tile):
        """绘制单个方块"""
        if not tile.visible:
            return
            
        rect = tile.get_rect()
        
        # 确定颜色
        if tile.selected:
            bg_color = COLORS['tile_selected']
        elif tile.hover:
            bg_color = COLORS['tile_hover']
        else:
            bg_color = COLORS['tile_bg']
        
        # 绘制方块背景
        pygame.draw.rect(self.screen, bg_color, rect, border_radius=8)
        
        # 绘制边框
        border_color = COLORS['accent'] if tile.selected else COLORS['text_secondary']
        pygame.draw.rect(self.screen, border_color, rect, 2, border_radius=8)
        
        # 绘制图案
        pattern = PATTERNS[tile.pattern_id % len(PATTERNS)]
        ShapeDrawer.draw_pattern(
            self.screen, 
            rect.center, 
            18,  # 图案大小
            pattern['type'], 
            pattern['color']
        )
            
    def draw_connection_path(self):
        """绘制连接路径动画"""
        if self.path_timer <= 0 or len(self.connection_path) < 2:
            return
        
        points = []
        for row, col in self.connection_path:
            x = GameConfig.BOARD_OFFSET_X + col * (GameConfig.TILE_SIZE + GameConfig.TILE_MARGIN) + GameConfig.TILE_SIZE // 2
            y = GameConfig.BOARD_OFFSET_Y + row * (GameConfig.TILE_SIZE + GameConfig.TILE_MARGIN) + GameConfig.TILE_SIZE // 2
            points.append((x, y))
        
        # 绘制发光的连接线
        for i in range(len(points) - 1):
            pygame.draw.line(self.screen, COLORS['line'], points[i], points[i + 1], 4)
            
        self.path_timer -= 1
        
    def draw_ui(self):
        """绘制用户界面"""
        # 标题
        title = self.font_large.render("连连看", True, COLORS['accent'])
        self.screen.blit(title, (30, 35))
        
        # 分数
        score_text = self.font_medium.render(f"分数: {self.score}", True, COLORS['text'])
        self.screen.blit(score_text, (30, 85))
        
        # 连击
        if self.combo > 1:
            combo_text = self.font_small.render(f"连击: x{self.combo}", True, COLORS['success'])
            self.screen.blit(combo_text, (160, 90))
        
        # 剩余对数
        pairs_text = self.font_medium.render(f"剩余: {self.remaining_pairs}对", True, COLORS['text'])
        self.screen.blit(pairs_text, (280, 85))
        
        # 时间
        if not self.game_over:
            self.elapsed_time = int(time.time() - self.start_time)
        mins = self.elapsed_time // 60
        secs = self.elapsed_time % 60
        time_text = self.font_medium.render(f"时间: {mins:02d}:{secs:02d}", True, COLORS['text'])
        self.screen.blit(time_text, (450, 85))
        
        # 绘制按钮
        self.btn_restart.draw(self.screen, self.font_small)
        self.btn_hint.draw(self.screen, self.font_small)
        self.btn_shuffle.draw(self.screen, self.font_small)
        
        # 底部信息
        info_text = self.font_small.render(
            f"提示: {self.hints_used} | 重排: {self.shuffles_used} | 最高连击: {self.max_combo}", 
            True, COLORS['text_secondary']
        )
        self.screen.blit(info_text, (30, GameConfig.SCREEN_HEIGHT - 35))
        
    def draw_game_over(self):
        """绘制游戏结束画面"""
        if not self.game_over:
            return
        
        # 半透明遮罩
        overlay = pygame.Surface((GameConfig.SCREEN_WIDTH, GameConfig.SCREEN_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(180)
        self.screen.blit(overlay, (0, 0))
        
        # 结果框
        box_width = 400
        box_height = 320
        box_x = (GameConfig.SCREEN_WIDTH - box_width) // 2
        box_y = (GameConfig.SCREEN_HEIGHT - box_height) // 2
        
        pygame.draw.rect(self.screen, COLORS['board_bg'], 
                        (box_x, box_y, box_width, box_height), border_radius=15)
        pygame.draw.rect(self.screen, COLORS['accent'], 
                        (box_x, box_y, box_width, box_height), 3, border_radius=15)
        
        # 标题
        if self.game_won:
            title = self.font_large.render("恭喜通关!", True, COLORS['success'])
        else:
            title = self.font_large.render("游戏结束", True, COLORS['warning'])
        title_rect = title.get_rect(center=(GameConfig.SCREEN_WIDTH // 2, box_y + 50))
        self.screen.blit(title, title_rect)
        
        # 统计信息
        stats = [
            f"最终分数: {self.score}",
            f"用时: {self.elapsed_time // 60:02d}:{self.elapsed_time % 60:02d}",
            f"最高连击: {self.max_combo}",
            f"使用提示: {self.hints_used} 次",
            f"使用重排: {self.shuffles_used} 次",
        ]
        
        y_offset = box_y + 100
        for stat in stats:
            stat_text = self.font_medium.render(stat, True, COLORS['text'])
            stat_rect = stat_text.get_rect(center=(GameConfig.SCREEN_WIDTH // 2, y_offset))
            self.screen.blit(stat_text, stat_rect)
            y_offset += 35
        
        # 弹框内的重新开始按钮
        restart_btn_width = 150
        restart_btn_height = 40
        restart_btn_x = (GameConfig.SCREEN_WIDTH - restart_btn_width) // 2
        restart_btn_y = box_y + box_height - 60
        
        # 更新/创建弹框内重新开始按钮
        self.btn_restart_popup = Button(
            restart_btn_x, restart_btn_y, 
            restart_btn_width, restart_btn_height, 
            "重新开始", COLORS['success']
        )
        self.btn_restart_popup.draw(self.screen, self.font_medium)
        
    def draw(self):
        """绘制游戏画面"""
        # 背景
        self.screen.fill(COLORS['background'])
        
        # 棋盘背景
        board_width = GameConfig.BOARD_COLS * (GameConfig.TILE_SIZE + GameConfig.TILE_MARGIN) + 20
        board_height = GameConfig.BOARD_ROWS * (GameConfig.TILE_SIZE + GameConfig.TILE_MARGIN) + 20
        board_rect = pygame.Rect(
            GameConfig.BOARD_OFFSET_X - 10,
            GameConfig.BOARD_OFFSET_Y - 10,
            board_width,
            board_height
        )
        pygame.draw.rect(self.screen, COLORS['board_bg'], board_rect, border_radius=10)
        
        # 绘制所有方块
        for row in self.board:
            for tile in row:
                if tile:
                    self.draw_tile(tile)
        
        # 绘制连接路径
        self.draw_connection_path()
        
        # 绘制UI
        self.draw_ui()
        
        # 游戏结束画面
        self.draw_game_over()
        
        pygame.display.flip()
        
    def run(self):
        """运行游戏主循环"""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # 左键
                        self.handle_click(event.pos)
                elif event.type == pygame.MOUSEMOTION:
                    self.handle_mouse_motion(event.pos)
                elif event.type == pygame.USEREVENT:
                    # 提示动画结束
                    pygame.time.set_timer(pygame.USEREVENT, 0)
                    for row in self.board:
                        for tile in row:
                            if tile and tile.visible and tile != self.selected_tile:
                                tile.selected = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.init_game()
                    elif event.key == pygame.K_h:
                        hint = self.find_hint()
                        if hint:
                            self.hints_used += 1
                            hint[0].selected = True
                            hint[1].selected = True
                    elif event.key == pygame.K_s:
                        self.shuffle_board()
            
            self.draw()
            self.clock.tick(GameConfig.FPS)
        
        pygame.quit()
        sys.exit()


def main():
    """程序入口"""
    print("=" * 50)
    print("连连看游戏 - Python版")
    print("=" * 50)
    print("\n游戏说明:")
    print("  - 点击两个相同的图案进行消除")
    print("  - 两个图案之间的连线不能超过两次转弯")
    print("  - 消除所有图案即可获胜")
    print("\n快捷键:")
    print("  R - 重新开始")
    print("  H - 提示")
    print("  S - 重排")
    print("\n祝你游戏愉快!\n")
    
    game = LianLianKan()
    game.run()


if __name__ == "__main__":
    main()
