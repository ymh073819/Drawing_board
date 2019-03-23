import pygame
from pygame.locals import *
import math


class Brush:
    def __init__(self, screen):
        self.screen = screen
        self.color = (0, 0, 0)#三元组表示颜色
        self.size = 1         #初始尺寸
        self.drawing = False #是否选中
        self.last_pos = None #最后的位置
        self.style = True    #刷子的样式
        self.brush = pygame.image.load("images/brush.png").convert_alpha()
        #转换成xx  不用纠结   此变量表示原始图片，放大、缩小、变色在此原始图片基础上
        self.brush_now = self.brush.subsurface((0, 0), (1, 1))   #子表面
        #此变量表示 当前的刷子图像(可以变大变小)
    def start_draw(self, pos):
        self.drawing = True
        self.last_pos = pos

    def end_draw(self):
        self.drawing = False

    def set_brush_style(self, style):
        print("* set brush style to", style)
        self.style = style

    def get_brush_style(self):
        return self.style

    def get_current_brush(self):
        return self.brush_now

    def set_size(self, size):
        #限制最小和最大的size
        if size < 1:
            size = 1
        elif size > 32:
            size = 32
        print("* set brush size to", size)
        self.size = size
        self.brush_now = self.brush.subsurface((0, 0), (size*2, size*2))

    def get_size(self):
        return self.size

    def set_color(self, color):#换颜色
        self.color = color
        for i in range(self.brush.get_width()):
            for j in range(self.brush.get_height()):
                self.brush.set_at((i, j),
                                  color + (self.brush.get_at((i, j)).a,))
                                #get_at获得某一像素位置的颜色   三元组可以相加  为什么是.a
       #set_at 获取某一像素位置的颜色 参数:像素坐标，颜色（三元组）
    def get_color(self):
        return self.color

    def draw(self, pos):
        if self.drawing:
            for p in self._get_points(pos):
                if self.style:
                    self.screen.blit(self.brush_now, p)#blit填充
                else:
                    pygame.draw.circle(self.screen, self.color, p, self.size)
            self.last_pos = pos

    def _get_points(self, pos):#获取画板坐标
        points = [(self.last_pos[0], self.last_pos[1])]
        len_x = pos[0] - self.last_pos[0]
        len_y = pos[1] - self.last_pos[1]
        length = math.sqrt(len_x**2 + len_y**2)
        step_x = len_x / length
        step_y = len_y / length
        for i in range(int(length)):
            points.append((points[-1][0] + step_x, points[-1][1] + step_y))
        points = map(lambda x: (int(0.5 + x[0]), int(0.5 + x[1])), points)
        return list(set(points))


class Menu:
    """
    Rect裁剪的用法:https://blog.csdn.net/qq_34404196/article/details/80718380
    """
    def __init__(self, screen):
        self.screen = screen
        self.brush = None
        self.colors = [
            (0xff, 0x00, 0xff), (0x80, 0x00, 0x80),
            (0x00, 0x00, 0xff), (0x00, 0x00, 0x80),
            (0x00, 0xff, 0xff), (0x00, 0x80, 0x80),
            (0x00, 0xff, 0x00), (0x00, 0x80, 0x00),
            (0xff, 0xff, 0x00), (0x80, 0x80, 0x00),
            (0xff, 0x00, 0x00), (0x80, 0x00, 0x00),
            (0xc0, 0xc0, 0xc0), (0xff, 0xff, 0xff),
            (0x00, 0x00, 0x00), (0x80, 0x80, 0x80),
        ]
        self.colors_rect = []
        for (i, rgb) in enumerate(self.colors):
            rect = pygame.Rect(10 + i % 2 * 32, 254 + i / 2 * 32, 32, 32)
            self.colors_rect.append(rect)
        self.pens = [
            pygame.image.load("images/pen1.png").convert_alpha(),
            pygame.image.load("images/pen2.png").convert_alpha(),
        ]
        self.pens_rect = []
        for (i, img) in enumerate(self.pens):
            rect = pygame.Rect(10, 10 + i * 64, 64, 64)
            self.pens_rect.append(rect)

        self.sizes = [
            pygame.image.load("images/big.png").convert_alpha(),
            pygame.image.load("images/small.png").convert_alpha()
        ]
        self.sizes_rect = []
        for (i, img) in enumerate(self.sizes):
            rect = pygame.Rect(10 + i * 32, 138, 32, 32)
            self.sizes_rect.append(rect)

    def set_brush(self, brush):
        self.brush = brush

    def draw(self):
        for (i, img) in enumerate(self.pens):
            self.screen.blit(img, self.pens_rect[i].topleft)
        for (i, img) in enumerate(self.sizes):
            self.screen.blit(img, self.sizes_rect[i].topleft)
        self.screen.fill((255, 255, 255), (10, 180, 64, 64))
        pygame.draw.rect(self.screen, (0, 0, 0), (10, 180, 64, 64), 1)
        size = self.brush.get_size()
        x = 10 + 32
        y = 180 + 32
        if self.brush.get_brush_style():
            x = x - size
            y = y - size
            self.screen.blit(self.brush.get_current_brush(), (x, y))
        else:
            pygame.draw.circle(self.screen,
                               self.brush.get_color(), (x, y), size)
        for (i, rgb) in enumerate(self.colors):
            pygame.draw.rect(self.screen, rgb, self.colors_rect[i])


    def click_button(self, pos):#颜色放进list中 分别对应 button
        for (i, rect) in enumerate(self.pens_rect):
            if rect.collidepoint(pos):
                self.brush.set_brush_style(bool(i))
                return True
        for (i, rect) in enumerate(self.sizes_rect):
            if rect.collidepoint(pos):
                if i:
                    self.brush.set_size(self.brush.get_size() - 1)
                else:
                    self.brush.set_size(self.brush.get_size() + 1)
                return True
        for (i, rect) in enumerate(self.colors_rect):
            if rect.collidepoint(pos):
                self.brush.set_color(self.colors[i])
                return True
        return False


class Painter:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))#设置屏幕尺寸
        pygame.display.set_caption("Painter")           #caption标题  设置标题
        self.clock = pygame.time.Clock()                 #帧速率  帮助我们确保程序以某一个最大的FPS运行
        self.brush = Brush(self.screen)                  #屏幕作为参数传给Brush类
        self.menu = Menu(self.screen)                    #
        self.menu.set_brush(self.brush)

    def run(self):
        self.screen.fill((255, 255, 255))
        while True:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.screen.fill((255, 255, 255))
                elif event.type == MOUSEBUTTONDOWN:
                    if event.pos[0] <= 74 and self.menu.click_button(event.pos):
                        pass
                    else:
                        self.brush.start_draw(event.pos)
                elif event.type == MOUSEMOTION:
                    self.brush.draw(event.pos)
                elif event.type == MOUSEBUTTONUP:
                    self.brush.end_draw()
            self.menu.draw()
            pygame.display.update()


def main():
    app = Painter()
    app.run()

if __name__ == '__main__':
    main()