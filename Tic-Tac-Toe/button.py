import pygame as pg
import time as t


class Button:
    def __init__(self, x0, y0):
        self.image = pg.image.load("play_again.png")
        self.rect = self.image.get_rect()
        self.w = self.image.get_width()
        self.h = self.image.get_height()
        self.scale = 0.35
        self.image = pg.transform.scale(self.image, (self.w*self.scale, self.h*self.scale))
        self.rect.x = x0
        self.rect.y = y0
        self.cl = False

    def clicked(self, ev, pos):
        if ev.type == pg.MOUSEBUTTONDOWN:
            if self.rect.x < pos[0] < self.rect.x + self.w and self.rect.y < pos[1] < self.rect.y + self.h:
                self.cl = True
        return self.cl

    def draw(self, screen):
        screen.blit(self.image, self.rect)