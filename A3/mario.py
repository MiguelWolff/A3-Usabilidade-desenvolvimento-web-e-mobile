import pygame as pg
from menu import Menu
from game import Game


class Main:
    
    def __init__(self, sizex, sizey, title):

        self.window = pg.display.set_mode([sizex, sizey])
        self.title = pg.display.set_caption(title)

        self.menu = Menu()
        self.game = Game()

        self.loop = True
        self.fps = pg.time.Clock()

    def draw(self):
        self.window.fill([0, 0, 0])
        if not self.menu.change_scene:
            self.menu.draw(self.window)
        elif not self.game.change_scene:
            self.game.draw(self.window)
            self.game.update()

    def events(self):
        for events in pg.event.get():
            if events.type == pg.QUIT:
                self.loop = False
            
            self.menu.events(events)

    def update(self):
        while self.loop:
            self.fps.tick(10)
            self.draw()
            self.events()
            pg.display.update()

game = Main(360, 640, "Mario Bros")
game.update()