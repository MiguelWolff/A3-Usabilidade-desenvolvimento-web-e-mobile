import pygame as pg

class Menu:
    def __init__(self):
        self.fonte_titulo = pg.font.SysFont("Arial", 40)
        self.fonte_opcao = pg.font.SysFont("Arial", 25)
        self.opcoes = ["Começar Jogo", "Comandos do Jogo", "Seletor de Fases"]
        self.opcao_selecionada = 0
        self.change_scene = False
        self.comandos = False
        self.fases = False

        # Carrega a imagem de fundo
        self.fundo = pg.image.load("A2/Assets/Sprites/level_1.png").convert()
        largura_original = self.fundo.get_width()
        self.fundo = pg.transform.scale(self.fundo, (largura_original, 300))  #escala apenas no eixo Y
        #self.fundo = pg.transform.scale(self.fundo, (480, 244))  # ajuste para o tamanho da janela caso precise

    def desenhar_texto(self, window, texto, fonte, cor, centro):
        superficie = fonte.render(texto, True, cor)
        ret = superficie.get_rect(center=centro)
        window.blit(superficie, ret)
        return ret

    def tela_comandos(self, window):
        """Tela que mostra os comandos do jogo."""
        window.blit(self.fundo, (0, 0))  # desenha o fundo
        self.desenhar_texto(window, "Comandos do Jogo", self.fonte_titulo, (255, 255, 255), (window.get_width() // 2, 80))
        comandos = [
            "Setas - Mover",
            "Espaço - Pular",
            "ESC - Voltar ao menu",
            "B - Especial"
        ]
        for i, texto in enumerate(comandos):
            self.desenhar_texto(window, texto, self.fonte_opcao, (255, 255, 255), (window.get_width() // 2, 160 + i * 40))

    def tela_fases(self, window):
        """Tela que mostra as opções de fase."""
        window.blit(self.fundo, (0, 0))  # desenha o fundo
        self.desenhar_texto(window, "Seletor de Fases", self.fonte_titulo, (255, 255, 255), (window.get_width() // 2, 80))
        fases = [
            "1 - Floresta",
            "2 - Deserto",
            "3 - Castelo",
            "ESC - Voltar ao menu"
        ]
        for i, texto in enumerate(fases):
            self.desenhar_texto(window, texto, self.fonte_opcao, (255, 255, 255), (window.get_width() // 2, 160 + i * 40))

    def draw(self, window):
        """Desenha o menu ou uma tela de submenu."""
        if self.comandos:
            self.tela_comandos(window)
        elif self.fases:
            self.tela_fases(window)
        else:
            window.fill((0, 0, 0))
            self.desenhar_texto(window, "Mario Bros", self.fonte_titulo, (255, 255, 255), (window.get_width() // 2, 80))
            for i, texto in enumerate(self.opcoes):
                cor = (255, 255, 0) if i == self.opcao_selecionada else (255, 255, 255)
                self.desenhar_texto(window, texto, self.fonte_opcao, cor, (window.get_width() // 2, 160 + i * 40))

    def events(self, event):
        """Processa eventos do menu."""
        if event.type == pg.KEYDOWN:
            if self.comandos or self.fases:
                if event.key == pg.K_ESCAPE:
                    self.comandos = False
                    self.fases = False
            else:
                if event.key == pg.K_UP:
                    self.opcao_selecionada = (self.opcao_selecionada - 1) % len(self.opcoes)
                elif event.key == pg.K_DOWN:
                    self.opcao_selecionada = (self.opcao_selecionada + 1) % len(self.opcoes)
                elif event.key in (pg.K_RETURN, pg.K_KP_ENTER):
                    if self.opcao_selecionada == 0:
                        self.change_scene = True
                    elif self.opcao_selecionada == 1:
                        self.comandos = True
                    elif self.opcao_selecionada == 2:
                        self.fases = True
