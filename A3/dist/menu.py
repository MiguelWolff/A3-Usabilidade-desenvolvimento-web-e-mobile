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
        self.fase_selecionada = 1

        # Carrega a imagem de fundo
        self.fundo = pg.image.load("Assets/Sprites/level_1.png").convert()
        largura_original = self.fundo.get_width()
        self.fundo = pg.transform.scale(self.fundo, (largura_original, 300))  #escala apenas no eixo Y
        #self.fundo = pg.transform.scale(self.fundo, (480, 244))  # ajuste para o tamanho da janela caso precise

    def desenhar_texto(self, window, texto, fonte, cor, centro, bg=None, padding=10):
        """Renderiza e desenha o texto centralizado, com fundo e margem."""
        superficie = fonte.render(texto, True, cor)
        texto_rect = superficie.get_rect(center=centro)

        if bg:
            fundo_rect = pg.Rect(
                texto_rect.left - padding,
                texto_rect.top - padding,
                texto_rect.width + padding * 2,
                texto_rect.height + padding * 2
            )
            pg.draw.rect(window, bg, fundo_rect, border_radius=6)

        window.blit(superficie, texto_rect)
        return texto_rect

    def tela_comandos(self, window):
        """Tela que mostra os comandos do jogo."""
        window.blit(self.fundo, (0, 0))  # desenha o fundo
        self.desenhar_texto(window, "Comandos do Jogo", self.fonte_titulo, "White", (window.get_width() // 2, 50), bg=("Dark Blue"), padding=6)
        comandos = [
            "Setas - Mover",
            "Espaço - Pular",
            "B - Especial",
            "ESC - Voltar ao menu"
        ]
        for i, texto in enumerate(comandos):
            self.desenhar_texto(window, texto, self.fonte_opcao, "White", (window.get_width() // 2, 110 + i * 40))

    def tela_fases(self, window):
        """Tela que mostra as opções de fase."""
        window.blit(self.fundo, (0, 0))  # desenha o fundo
        self.desenhar_texto(window, "Seletor de Fases", self.fonte_titulo, (255, 255, 255), (window.get_width() // 2, 50), bg=("Dark Blue"), padding=6)
        fases = [
            "1 - Floresta",
            "2 - Deserto",
            "3 - Castelo",
            "ESC - Voltar ao menu"
        ]
        for i, texto in enumerate(fases):
            self.desenhar_texto(window, texto, self.fonte_opcao, (255, 255, 255), (window.get_width() // 2, 110 + i * 40))

    def draw(self, window):
        """Desenha o menu ou uma tela de submenu."""
        if self.comandos:
            self.tela_comandos(window)
        elif self.fases:
            self.tela_fases(window)
        else:
            window.blit(self.fundo, (0, 0))  # desenha o fundo
            self.desenhar_texto(window, "Mario Bros", self.fonte_titulo, "White", (window.get_width() // 2, 50), bg=("Dark Blue"), padding=6)
            for i, texto in enumerate(self.opcoes):
                cor = (255, 255, 0) if i == self.opcao_selecionada else "White"
                self.desenhar_texto(window, texto, self.fonte_opcao, cor, (window.get_width() // 2, 110 + i * 40))

    def events(self, event):
        """Processa eventos do menu."""
        if event.type == pg.KEYDOWN:
            if self.comandos or self.fases:
                if event.key == pg.K_ESCAPE:
                    # Voltar ao menu principal
                    self.comandos = False
                    self.fases = False
                elif self.fases:
                    # Seletor de fases ativo, escolher fase com as teclas 1, 2, 3
                    if event.key == pg.K_1:
                        self.fase_selecionada = 1
                        self.change_scene = True
                        self.fases = False
                    elif event.key == pg.K_2:
                        self.fase_selecionada = 2
                        self.change_scene = True
                        self.fases = False
                    elif event.key == pg.K_3:
                        self.fase_selecionada = 3
                        self.change_scene = True
                        self.fases = False
            else:
                # Menu principal: navegação com setas
                if event.key == pg.K_UP:
                    self.opcao_selecionada = (self.opcao_selecionada - 1) % len(self.opcoes)
                elif event.key == pg.K_DOWN:
                    self.opcao_selecionada = (self.opcao_selecionada + 1) % len(self.opcoes)
                elif event.key in (pg.K_RETURN, pg.K_KP_ENTER):
                    if self.opcao_selecionada == 0:
                        self.change_scene = True
                        self.fase_selecionada = 1  # padrão, fase 1
                    elif self.opcao_selecionada == 1:
                        self.comandos = True
                    elif self.opcao_selecionada == 2:
                        self.fases = True

class FinalScreen:
    def __init__(self):
        self.finished = False
        self.font = pg.font.SysFont("Arial", 20, True)
        self.big_font = pg.font.SysFont("Arial", 30, True)
        self.fundo = pg.image.load("Assets/Sprites/level_1.png").convert()
        largura_original = self.fundo.get_width()
        self.fundo = pg.transform.scale(self.fundo, (largura_original, 300))  #escala apenas no eixo Y

    def draw(self, window):
        window.blit(self.fundo, (0, 0))  # desenha o fundo
        texto1 = self.big_font.render("Parabéns!", True, (255, 255, 0), "Dark Blue")
        texto2 = self.font.render("Você concluiu todas as fases.", True, (255, 255, 255))
        texto3 = self.font.render("Pressione qualquer tecla para sair.", True, (200, 200, 200))
        window_width, window_height = window.get_size()
        window.blit(texto1, (window_width//2 - texto1.get_width()//2, 60))
        window.blit(texto2, (window_width//2 - texto2.get_width()//2, 120))
        window.blit(texto3, (window_width//2 - texto3.get_width()//2, 180))


    def events(self, event):
        if event.type == pg.KEYDOWN or event.type == pg.QUIT:
            self.finished = True