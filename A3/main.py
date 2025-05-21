import pygame as pg
from menu import Menu
from game import Game

pg.init()

class Main:

    def __init__(self, sizex, sizey, title):
        self.sizex = sizex
        self.sizey = sizey
        self.window = pg.display.set_mode([sizex, sizey])
        pg.display.set_caption(title)

        self.menu = Menu()
        self.game = Game(sizex, sizey)

        self.loop = True
        self.fps = pg.time.Clock()

    def draw(self):
        self.window.fill((0, 0, 0))
        if not self.menu.change_scene:
            self.menu.draw(self.window)
        else:
            self.game.draw(self.window)
            self.game.update()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.loop = False

            if not self.menu.change_scene:
                self.menu.events(event)
            else:
                self.game.events(event)

    def update(self):
        while self.loop:
            self.fps.tick(60)
            self.draw()
            self.events()
            pg.display.update()

game = Main(400, 300, "Mario Bros")
game.update()
