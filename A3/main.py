import pygame as pg
from menu import Menu, FinalScreen
from game import Game

pg.mixer.pre_init(44100, -16, 2, 512)
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
        self.final_screen = None
        self.final_mode = False

    def draw(self):
        """Desenha o menu ou o jogo dependendo da cena atual."""
        self.window.fill((0, 0, 0))
        if not self.menu.change_scene:
            self.menu.draw(self.window)
        else:
            self.game.draw(self.window)
        if self.final_mode:
            self.final_screen.draw(self.window)

    def events(self):
        """Processa os eventos do pygame e os encaminha para menu ou jogo."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.loop = False

            elif self.final_mode:
                self.final_screen.events(event)
                if self.final_screen.finished:
                    self.loop = False

            elif not self.menu.change_scene:
                self.menu.events(event)
            else:
                self.game.events(event)

    def encerra_jogo(self):
        self.final_screen = FinalScreen()
        self.final_mode = True


    def run(self):
        jogo_iniciado = False
        """Loop principal do jogo."""
        while self.loop:
            self.fps.tick(60)  # limita a 60 FPS
            self.events()
            if self.final_mode:
                self.final_screen.draw(self.window)
            if self.menu.change_scene and not jogo_iniciado:
                self.game = Game(self.sizex, self.sizey)
                self.game.carregar_fase(self.menu.fase_selecionada)
                self.game.fase_atual = self.menu.fase_selecionada
                self.game.callback_encerrar = self.encerra_jogo
                jogo_iniciado = True

            if self.menu.change_scene:
                self.game.update()
            
            self.draw()

            pg.display.update()

        pg.quit()  # encerra o pygame ao sair do loop

if __name__ == "__main__":
    main = Main(400, 300, "Super Mario Bros")
    main.run()
