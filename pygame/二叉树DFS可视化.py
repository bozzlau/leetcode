"""
二叉树 DFS 遍历可视化
功能：
  - 随机生成二叉树
  - 三种遍历方式：前序、中序、后序
  - 动画展示遍历过程
  - 空格键：暂停/继续
  - 左/右箭头：单步后退/前进
  - 上/下箭头：加速/减速
  - 1/2/3 键：切换前序/中序/后序
  - R 键：重新生成树
  - ESC：退出
"""

import pygame
import random
import math
from dataclasses import dataclass
from typing import Optional, Generator, Tuple, List, Dict

# ============================================================
# 配置类
# ============================================================
@dataclass
class Config:
    WIDTH: int = 1000
    HEIGHT: int = 750
    INFO_HEIGHT: int = 100
    
    # 树的参数
    MAX_DEPTH: int = 4          # 最大深度
    NODE_RADIUS: int = 28       # 节点半径
    LEVEL_GAP: int = 80         # 层间距
    
    # 颜色主题 - 现代暗色系
    BG_COLOR: Tuple[int, int, int] = (30, 32, 44)
    EDGE_COLOR: Tuple[int, int, int] = (100, 110, 140)
    
    NODE_DEFAULT: Tuple[int, int, int] = (80, 90, 120)
    NODE_VISITED: Tuple[int, int, int] = (98, 114, 164)
    NODE_CURRENT: Tuple[int, int, int] = (241, 250, 140)
    NODE_PROCESSED: Tuple[int, int, int] = (80, 250, 123)
    NODE_IN_STACK: Tuple[int, int, int] = (255, 184, 108)
    
    # 路径渐变
    PATH_START: Tuple[int, int, int] = (139, 233, 253)
    PATH_END: Tuple[int, int, int] = (255, 121, 198)
    
    # 文字颜色
    TEXT_COLOR: Tuple[int, int, int] = (248, 248, 242)
    TEXT_DARK: Tuple[int, int, int] = (30, 30, 30)
    
    # 遍历模式颜色
    PREORDER_COLOR: Tuple[int, int, int] = (255, 85, 85)
    INORDER_COLOR: Tuple[int, int, int] = (80, 250, 123)
    POSTORDER_COLOR: Tuple[int, int, int] = (139, 233, 253)


# ============================================================
# 二叉树节点
# ============================================================
class TreeNode:
    def __init__(self, val: int):
        self.val = val
        self.left: Optional['TreeNode'] = None
        self.right: Optional['TreeNode'] = None
        # 可视化位置
        self.x: float = 0
        self.y: float = 0


# ============================================================
# 二叉树DFS可视化器
# ============================================================
class BinaryTreeDFSVisualizer:
    def __init__(self, config: Config = None):
        self.config = config or Config()
        
        # Pygame 初始化
        pygame.init()
        self.screen = pygame.display.set_mode((self.config.WIDTH, self.config.HEIGHT))
        pygame.display.set_caption("🌳 二叉树 DFS 遍历可视化")
        self.clock = pygame.time.Clock()
        
        # 字体
        chinese_fonts = ["PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", 
                        "WenQuanYi Micro Hei", "SimHei"]
        self.font_small = pygame.font.SysFont(chinese_fonts, 14)
        self.font_medium = pygame.font.SysFont(chinese_fonts, 18)
        self.font_large = pygame.font.SysFont(chinese_fonts, 24, bold=True)
        self.font_node = pygame.font.SysFont(chinese_fonts, 16, bold=True)
        
        # 状态
        self.speed = 8
        self.paused = True
        self.step_once = False
        self.finished = False
        
        # 遍历模式: 'preorder', 'inorder', 'postorder'
        self.traversal_mode = 'preorder'
        self.mode_names = {
            'preorder': '前序遍历 (根-左-右)',
            'inorder': '中序遍历 (左-根-右)',
            'postorder': '后序遍历 (左-右-根)'
        }
        
        # 历史记录
        self.history: List[Dict] = []
        self.history_index = -1
        
        # 初始化树
        self.reset_tree()
    
    def generate_tree(self, depth: int = 0, max_val: int = 99) -> Optional[TreeNode]:
        """递归生成随机二叉树"""
        if depth >= self.config.MAX_DEPTH:
            return None
        
        # 随机决定是否创建节点（深度越深，概率越低）
        prob = 0.9 - depth * 0.15
        if depth > 0 and random.random() > prob:
            return None
        
        node = TreeNode(random.randint(1, max_val))
        node.left = self.generate_tree(depth + 1, max_val)
        node.right = self.generate_tree(depth + 1, max_val)
        
        return node
    
    def calculate_positions(self, node: Optional[TreeNode], x: float, y: float, 
                           h_gap: float, depth: int = 0):
        """计算节点位置"""
        if not node:
            return
        
        node.x = x
        node.y = y
        
        next_gap = h_gap * 0.55
        child_y = y + self.config.LEVEL_GAP
        
        if node.left:
            self.calculate_positions(node.left, x - h_gap, child_y, next_gap, depth + 1)
        if node.right:
            self.calculate_positions(node.right, x + h_gap, child_y, next_gap, depth + 1)
    
    def reset_tree(self):
        """重置树和搜索状态"""
        self.root = self.generate_tree()
        
        # 确保树不为空
        while not self.root:
            self.root = self.generate_tree()
        
        # 计算节点位置
        tree_top = 80
        h_gap = self.config.WIDTH * 0.22
        self.calculate_positions(self.root, self.config.WIDTH // 2, tree_top, h_gap)
        
        self.reset_search()
    
    def reset_search(self):
        """重置搜索状态"""
        self.visited: set = set()           # 已访问过的节点
        self.processed: set = set()         # 已处理完成的节点（输出）
        self.in_stack: set = set()          # 当前在栈中的节点
        self.current: Optional[TreeNode] = None
        self.result: List[int] = []         # 遍历结果序列
        self.finished = False
        
        self.dfs_gen = self.dfs_traversal()
        
        self.history = []
        self.history_index = -1
    
    def dfs_traversal(self) -> Generator:
        """DFS遍历生成器"""
        
        def preorder(node: TreeNode):
            """前序遍历：根 -> 左 -> 右"""
            if not node:
                return
            
            self.in_stack.add(id(node))
            self.visited.add(id(node))
            
            # 访问当前节点（处理）
            self.processed.add(id(node))
            self.result.append(node.val)
            yield self._create_state(node, "process")
            
            # 递归左子树
            yield from preorder(node.left)
            
            # 递归右子树
            yield from preorder(node.right)
            
            self.in_stack.discard(id(node))
            yield self._create_state(node, "backtrack")
        
        def inorder(node: TreeNode):
            """中序遍历：左 -> 根 -> 右"""
            if not node:
                return
            
            self.in_stack.add(id(node))
            self.visited.add(id(node))
            yield self._create_state(node, "visit")
            
            # 递归左子树
            yield from inorder(node.left)
            
            # 访问当前节点（处理）
            self.processed.add(id(node))
            self.result.append(node.val)
            yield self._create_state(node, "process")
            
            # 递归右子树
            yield from inorder(node.right)
            
            self.in_stack.discard(id(node))
            yield self._create_state(node, "backtrack")
        
        def postorder(node: TreeNode):
            """后序遍历：左 -> 右 -> 根"""
            if not node:
                return
            
            self.in_stack.add(id(node))
            self.visited.add(id(node))
            yield self._create_state(node, "visit")
            
            # 递归左子树
            yield from postorder(node.left)
            
            # 递归右子树
            yield from postorder(node.right)
            
            # 访问当前节点（处理）
            self.processed.add(id(node))
            self.result.append(node.val)
            yield self._create_state(node, "process")
            
            self.in_stack.discard(id(node))
            yield self._create_state(node, "backtrack")
        
        if self.traversal_mode == 'preorder':
            yield from preorder(self.root)
        elif self.traversal_mode == 'inorder':
            yield from inorder(self.root)
        else:
            yield from postorder(self.root)
    
    def _create_state(self, node: TreeNode, action: str) -> Dict:
        """创建当前状态快照"""
        return {
            'node': node,
            'action': action,
            'visited': set(self.visited),
            'processed': set(self.processed),
            'in_stack': set(self.in_stack),
            'result': list(self.result)
        }
    
    def step_forward(self):
        """前进一步"""
        if self.finished:
            return
        
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self._apply_state(self.history[self.history_index])
            return
        
        try:
            state = next(self.dfs_gen)
            self.history.append(state)
            self.history_index = len(self.history) - 1
            self._apply_state(state)
        except StopIteration:
            self.finished = True
            self.current = None
    
    def step_backward(self):
        """后退一步"""
        if self.history_index > 0:
            self.history_index -= 1
            self._apply_state(self.history[self.history_index])
        elif self.history_index == 0:
            self.history_index = -1
            self.visited = set()
            self.processed = set()
            self.in_stack = set()
            self.current = None
            self.result = []
    
    def _apply_state(self, state: Dict):
        """应用状态"""
        self.current = state['node']
        self.visited = state['visited']
        self.processed = state['processed']
        self.in_stack = state['in_stack']
        self.result = state['result']
        self.finished = False
    
    def draw(self):
        """绘制所有内容"""
        self.screen.fill(self.config.BG_COLOR)
        
        self.draw_edges(self.root)
        self.draw_nodes(self.root)
        self.draw_info_panel()
        self.draw_result_sequence()
        
        pygame.display.flip()
    
    def draw_edges(self, node: Optional[TreeNode]):
        """绘制边"""
        if not node:
            return
        
        if node.left:
            self._draw_edge(node, node.left)
            self.draw_edges(node.left)
        
        if node.right:
            self._draw_edge(node, node.right)
            self.draw_edges(node.right)
    
    def _draw_edge(self, parent: TreeNode, child: TreeNode):
        """绘制单条边"""
        # 计算边的起点和终点（从节点边缘开始）
        dx = child.x - parent.x
        dy = child.y - parent.y
        dist = math.sqrt(dx * dx + dy * dy)
        
        if dist == 0:
            return
        
        # 单位向量
        ux = dx / dist
        uy = dy / dist
        
        start_x = parent.x + ux * self.config.NODE_RADIUS
        start_y = parent.y + uy * self.config.NODE_RADIUS
        end_x = child.x - ux * self.config.NODE_RADIUS
        end_y = child.y - uy * self.config.NODE_RADIUS
        
        # 根据状态选择颜色
        if id(child) in self.processed and id(parent) in self.processed:
            # 两个节点都已处理，渐变色
            color = self.config.PATH_START
            width = 3
        elif id(child) in self.in_stack or id(parent) in self.in_stack:
            color = self.config.NODE_IN_STACK
            width = 3
        elif id(child) in self.visited:
            color = self.config.NODE_VISITED
            width = 2
        else:
            color = self.config.EDGE_COLOR
            width = 2
        
        pygame.draw.line(self.screen, color, 
                        (int(start_x), int(start_y)), 
                        (int(end_x), int(end_y)), width)
    
    def draw_nodes(self, node: Optional[TreeNode]):
        """绘制节点"""
        if not node:
            return
        
        # 先绘制子节点
        self.draw_nodes(node.left)
        self.draw_nodes(node.right)
        
        # 绘制当前节点
        self._draw_node(node)
    
    def _draw_node(self, node: TreeNode):
        """绘制单个节点"""
        x, y = int(node.x), int(node.y)
        radius = self.config.NODE_RADIUS
        
        # 确定节点颜色
        if node == self.current:
            # 当前节点 - 脉冲动画
            pulse = (math.sin(pygame.time.get_ticks() * 0.01) + 1) / 2
            radius_offset = int(pulse * 5)
            color = self.config.NODE_CURRENT
            
            # 发光效果
            glow_radius = radius + 8 + radius_offset
            glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
            for i in range(8, 0, -1):
                alpha = 30 - i * 3
                glow_color = (*color, alpha)
                pygame.draw.circle(glow_surface, glow_color, 
                                  (glow_radius, glow_radius), radius + i)
            self.screen.blit(glow_surface, (x - glow_radius, y - glow_radius))
            
        elif id(node) in self.processed:
            color = self.config.NODE_PROCESSED
        elif id(node) in self.in_stack:
            color = self.config.NODE_IN_STACK
        elif id(node) in self.visited:
            color = self.config.NODE_VISITED
        else:
            color = self.config.NODE_DEFAULT
        
        # 绘制节点圆
        pygame.draw.circle(self.screen, color, (x, y), radius)
        pygame.draw.circle(self.screen, (255, 255, 255), (x, y), radius, 2)
        
        # 绘制节点值
        text_color = self.config.TEXT_DARK if color in [
            self.config.NODE_CURRENT, 
            self.config.NODE_PROCESSED,
            self.config.NODE_IN_STACK
        ] else self.config.TEXT_COLOR
        
        text = self.font_node.render(str(node.val), True, text_color)
        text_rect = text.get_rect(center=(x, y))
        self.screen.blit(text, text_rect)
    
    def draw_info_panel(self):
        """绘制信息面板"""
        panel_y = self.config.HEIGHT - self.config.INFO_HEIGHT
        
        # 面板背景
        panel_rect = pygame.Rect(0, panel_y, self.config.WIDTH, self.config.INFO_HEIGHT)
        pygame.draw.rect(self.screen, (25, 27, 38), panel_rect)
        pygame.draw.line(self.screen, (60, 65, 80), 
                        (0, panel_y), (self.config.WIDTH, panel_y), 2)
        
        # 遍历模式
        mode_colors = {
            'preorder': self.config.PREORDER_COLOR,
            'inorder': self.config.INORDER_COLOR,
            'postorder': self.config.POSTORDER_COLOR
        }
        mode_color = mode_colors[self.traversal_mode]
        mode_text = self.font_large.render(self.mode_names[self.traversal_mode], 
                                           True, mode_color)
        self.screen.blit(mode_text, (20, panel_y + 10))
        
        # 状态
        if self.finished:
            status = "✓ 遍历完成"
            status_color = self.config.NODE_PROCESSED
        elif self.paused:
            status = "⏸ 暂停中"
            status_color = self.config.NODE_CURRENT
        else:
            status = "▶ 运行中"
            status_color = self.config.PATH_START
        
        status_text = self.font_medium.render(status, True, status_color)
        self.screen.blit(status_text, (self.config.WIDTH - 150, panel_y + 15))
        
        # 统计信息
        stats = f"已访问: {len(self.visited)}  |  已处理: {len(self.processed)}  |  速度: {self.speed} FPS  |  步骤: {self.history_index + 1}/{len(self.history)}"
        stats_text = self.font_medium.render(stats, True, (180, 180, 180))
        self.screen.blit(stats_text, (20, panel_y + 45))
        
        # 快捷键提示
        hints = "Space:暂停  ←/→:单步  ↑/↓:速度  1/2/3:前序/中序/后序  R:重置"
        hints_text = self.font_small.render(hints, True, (120, 120, 140))
        self.screen.blit(hints_text, (20, panel_y + 75))
    
    def draw_result_sequence(self):
        """绘制遍历结果序列"""
        if not self.result:
            return
        
        # 序列面板
        panel_x = 20
        panel_y = self.config.HEIGHT - self.config.INFO_HEIGHT - 50
        
        # 标题
        title = self.font_medium.render("遍历序列:", True, self.config.TEXT_COLOR)
        self.screen.blit(title, (panel_x, panel_y))
        
        # 结果序列（显示最后15个）
        display_result = self.result[-15:] if len(self.result) > 15 else self.result
        prefix = "... " if len(self.result) > 15 else ""
        
        result_str = prefix + " → ".join(map(str, display_result))
        result_text = self.font_medium.render(result_str, True, self.config.NODE_PROCESSED)
        self.screen.blit(result_text, (panel_x + 90, panel_y))
    
    def switch_mode(self, mode: str):
        """切换遍历模式"""
        if mode != self.traversal_mode:
            self.traversal_mode = mode
            self.reset_search()
    
    def handle_events(self) -> bool:
        """处理事件"""
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
                    self.speed = min(60, self.speed + 2)
                elif event.key == pygame.K_DOWN:
                    self.speed = max(1, self.speed - 2)
                elif event.key == pygame.K_r:
                    self.reset_tree()
                elif event.key == pygame.K_1:
                    self.switch_mode('preorder')
                elif event.key == pygame.K_2:
                    self.switch_mode('inorder')
                elif event.key == pygame.K_3:
                    self.switch_mode('postorder')
        
        return True
    
    def run(self):
        """主循环"""
        running = True
        last_step_time = 0
        
        while running:
            self.clock.tick(60)
            current_time = pygame.time.get_ticks()
            
            running = self.handle_events()
            
            # 控制搜索速度
            step_interval = 1000 // self.speed
            if not self.paused or self.step_once:
                if current_time - last_step_time >= step_interval or self.step_once:
                    self.step_forward()
                    self.step_once = False
                    last_step_time = current_time
            
            self.draw()
        
        pygame.quit()


# ============================================================
# 入口
# ============================================================
if __name__ == "__main__":
    config = Config(
        WIDTH=1000,
        HEIGHT=750,
        MAX_DEPTH=4,
        NODE_RADIUS=28,
        LEVEL_GAP=90
    )
    
    visualizer = BinaryTreeDFSVisualizer(config)
    visualizer.run()
