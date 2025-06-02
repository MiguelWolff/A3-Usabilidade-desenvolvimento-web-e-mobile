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
        """Desenha o menu ou o jogo dependendo da cena atual."""
        self.window.fill((0, 0, 0))
        if not self.menu.change_scene:
            self.menu.draw(self.window)
        else:
            self.game.draw(self.window)

    def events(self):
        """Processa os eventos do pygame e os encaminha para menu ou jogo."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.loop = False

            if not self.menu.change_scene:
                self.menu.events(event)
            else:
                self.game.events(event)

    def run(self):
        """Loop principal do jogo."""
        while self.loop:
            self.fps.tick(60)  # limita a 60 FPS

            self.events()

            if self.menu.change_scene:
                self.game.update()

            self.draw()

            pg.display.update()

        pg.quit()  # encerra o pygame ao sair do loop

if __name__ == "__main__":
    main = Main(400, 300, "Mario Bros")
    main.run()
