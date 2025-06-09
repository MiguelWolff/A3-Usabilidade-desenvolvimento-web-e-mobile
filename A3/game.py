import pygame as pg
from obj import Obj, Bloco, Cogumelo, QuestionBlock, Estrela, FlorDeFogo, Fireball, Coin
from enemies import Goomba, Bowser, KoopaTroopa

# Constantes
AZUL = (135, 206, 235)
VERDE = (34, 139, 34)
GRAVIDADE = 1
VELOCIDADE = 4
IMPULSO_PULO = -12
CHAO_Y = 270  # Altura do chão fixo (ALTURA - 30 do seu código)


class Game:
    def __init__(self, largura, altura):
        self.LARGURA = largura
        self.ALTURA = altura

        self.change_scene = False

        self.mario_world_x = 0
        self.mario_screen_x = 50
        self.mario_y = altura - 120

        self.vel_x = 0
        self.vel_y = 0
        self.no_chao = False
        self.vidas = 3

        self.mario = Obj("Assets/Sprites/Mario.png", self.mario_screen_x, self.mario_y, animated=True)

        self.goomba = Goomba(300, altura - 45)
        self.cogumelo = None
        self.estrela = None
        self.flor = None
        self.coin = None
        self.crouching = False
        self.invencivel_timer = 0
        self.invencivel = False

        self.blocos = [
            Bloco(200, altura - 80, tipo="brown"),
            Bloco(250, altura - 80, tipo="castle"),
            Bloco(300, altura - 80, tipo="dark"),
            QuestionBlock(350, altura - 80, tema="normal", contem_flor=True),
            QuestionBlock(400, altura - 80, tema="castle", contem_estrela=True),
            QuestionBlock(450, altura - 80, tema="dark", contem_cogumelo=True),
            QuestionBlock(500, altura - 80, tema="normal", contem_cogumelo_vida=True),
            QuestionBlock(550, altura - 80, tema="castle", contem_flor=True),
            QuestionBlock(600, altura - 80, tema="dark", contem_moeda=True)
        ]
        self.bowser = Bowser(600, altura - 62)
        self.koopas = [
            KoopaTroopa(500, altura - 55, tipo="verde"),
            KoopaTroopa(600, altura - 55, tipo="verde_casco_azul"),
            KoopaTroopa(700, altura - 55, tipo="vermelho")
        ]
        self.fireballs = []
        self.fireball_cooldown = 0
        self.inimigos = [self.goomba] + self.koopas
        self.inimigo = None


    def draw(self, window):
        window.fill(AZUL)
        camera_x = self.mario_world_x - self.mario_screen_x

        # Chão
        pg.draw.rect(window, VERDE, (0 - camera_x, self.ALTURA - 30, 2000, 30))

        # Desenha blocos e atualiza animações
        for bloco in self.blocos:
            bloco.draw(window, camera_x)
            if isinstance(bloco, QuestionBlock):
                bloco.update()

        # Desenha inimigos e itens
        if self.goomba:
            self.goomba.draw(window, camera_x)

        if self.cogumelo:
            self.cogumelo.draw(window, camera_x)

        if self.estrela:
            self.estrela.draw(window, camera_x)
        
        if self.flor:
            self.flor.draw(window, camera_x)
        
        if self.bowser:
            self.bowser.draw(window, camera_x)

        if self.coin:
            self.coin.draw(window, camera_x)

        for koopa in self.koopas:
            koopa.draw(window, camera_x)

        for fireball in self.fireballs:
            fireball.draw(window, camera_x)

        # Desenha Mario (sprite fixo na tela)
        self.mario.sprite.rect.x = self.mario_screen_x
        self.mario.draw(window)

        # HUD vidas
        font = pg.font.SysFont("Arial", 20)
        vidas_texto = font.render(f"Vidas: {self.vidas}", True, (255, 255, 255))
        window.blit(vidas_texto, (10, 10))


    def update(self):
        if self.invencivel:
            self.invencivel_timer -= 1
            if self.invencivel_timer <= 0:
                self.invencivel = False
        self.inimigos = []
        if self.goomba:
            self.inimigos.append(self.goomba)
        self.inimigos += [k for k in self.koopas if k.visible]

        # Atualiza posição horizontal do Mario no mundo
        self.mario_world_x += self.vel_x

        # Atualiza posição vertical com gravidade
        self.vel_y += GRAVIDADE
        # Atualiza a posição vertical (Y) do Mario, sem alterar X ainda
        self.mario.sprite.rect.y += self.vel_y
        # Atualiza a posição horizontal do Mario (no mundo)
        self.mario_world_x += self.vel_x
        # ATualiza o rect real com a posição atual do Mario no mundo
        mario_real_rect = self.mario.sprite.rect.copy()
        mario_real_rect.x = self.mario_world_x
        self.no_chao = False
        # Colisão com o chão
        if mario_real_rect.bottom >= CHAO_Y:
            mario_real_rect.bottom = CHAO_Y
            self.vel_y = 0
            self.no_chao = True
            self.mario.sprite.rect.bottom = CHAO_Y
        else:
            self.mario.sprite.rect.y = mario_real_rect.y

        # Colisões com blocos
        for bloco in self.blocos:
            bloco_rect = bloco.get_rect()
            if mario_real_rect.colliderect(bloco_rect):
                if self.vel_y > 0 and mario_real_rect.bottom - self.vel_y <= bloco_rect.top:
                    # Mario caiu sobre bloco
                    mario_real_rect.bottom = bloco_rect.top
                    self.vel_y = 0
                    self.no_chao = True
                elif self.vel_y < 0 and mario_real_rect.top - self.vel_y >= bloco_rect.bottom:
                    # Mario bateu na parte inferior do bloco
                    mario_real_rect.top = bloco_rect.bottom
                    self.vel_y = 0
                    if isinstance(bloco, QuestionBlock):
                        novo_item = bloco.ativar()
                        if isinstance(novo_item, Cogumelo):
                            self.cogumelo = novo_item
                        elif isinstance(novo_item, Estrela):
                            self.estrela = novo_item
                        elif isinstance(novo_item, FlorDeFogo):
                            self.flor = novo_item
                        elif isinstance(novo_item, Coin):
                            self.coin = novo_item
                else:
                    # Colisão lateral
                    if self.vel_x > 0:
                        mario_real_rect.right = bloco_rect.left
                    else:
                        mario_real_rect.left = bloco_rect.right
                    self.vel_x = 0

        for fireball in self.fireballs[:]:
            if fireball.exploding:
                # Atualiza animação da explosão
                fireball.update()
                if fireball.explosion_done:
                    self.fireballs.remove(fireball)
                continue
            
            # Atualiza movimento da fireball
            fireball.update()
    
            # Colisão lateral com blocos
            for bloco in self.blocos:
                if fireball.rect.colliderect(bloco.get_rect()):
                    # Verificar colisão lateral (exemplo simples)
                    if (fireball.rect.right >= bloco.get_rect().left and
                        fireball.rect.left < bloco.get_rect().left) or \
                       (fireball.rect.left <= bloco.get_rect().right and
                        fireball.rect.right > bloco.get_rect().right):
                        fireball.explode()
                        break
            
            self.inimigos = []
            if self.goomba:
                self.inimigos.append(self.goomba)
            self.inimigos += [k for k in self.koopas if k.visible]

            # Colisão com inimigos
            for inimigo in self.inimigos:
                self.inimigo = inimigo
                inimigo.rect = self.inimigo.rect
                if fireball.rect.colliderect(inimigo.rect):
                    inimigo.morrer()  # Ajuste de acordo com seu código
                    fireball.explode()
                    break
            # Remover fireball se sair da tela ou invisível
            if not fireball.visible:
                self.fireballs.remove(fireball)

        if self.fireball_cooldown > 0:
            self.fireball_cooldown -= 1

        # Atualiza posição real no mundo
        self.mario_world_x = mario_real_rect.x
        self.mario.sprite.rect.y = mario_real_rect.y

        # Atualiza inimigos
        if self.goomba:
            self.goomba.update(2000)

        # Colisão com Goomba
        """if self.goomba and mario_real_rect.colliderect(self.goomba.rect):
            if self.vel_y > 0 and mario_real_rect.bottom <= self.goomba.rect.top + 10:
                print("Goomba derrotado!")
                self.vel_y = -8
                self.goomba.morrer()
            else:
                print("Mario colidiu com o Goomba (lado ou baixo)")
                # Aqui poderia tratar perda de vida etc."""

        if self.goomba and not self.goomba.alive:
            self.goomba = None

        # Atualiza cogumelo
        if self.cogumelo:
            self.cogumelo.update(2000)
            if self.cogumelo.rect.bottom >= CHAO_Y:
                self.cogumelo.rect.bottom = CHAO_Y
            if mario_real_rect.colliderect(self.cogumelo.rect):
                if self.cogumelo.tipo == "vida":
                    self.vidas += 1
                else:
                    self.mario.crescer(forcar=False)
                self.cogumelo = None

        # Atualiza estrela
        if self.estrela:
            self.estrela.update(2000)
            if mario_real_rect.colliderect(self.estrela.rect):
                print("Estrela coletada! Mario invencível?")
                # Implementar efeitos da estrela
                self.mario.marioestrela()
                self.estrela = None

        # Atualiza flor
        if self.flor:
            self.flor.update(2000)
            if mario_real_rect.colliderect(self.flor.rect):
                print("Mario pegou a flor de fogo!")
                self.mario.virar_fogo(forcar=False)
                self.flor = None
        
        # Atualiza Moeda
        if self.coin:
            self.coin.update()
            if mario_real_rect.colliderect(self.coin.rect):
                self.coin.collect()
                print("Mario pegou a moeda")
                self.coin = None
        
        # Atualiza Mario
        if self.mario:
            self.mario.update()

        # Anima Mario (correndo ou parado)
        skidding = False
        if self.vel_x < 0 and not self.mario.facing_left:
            skidding = True
        elif self.vel_x > 0 and self.mario.facing_left:
            skidding = True
        
        self.mario.animate(
            moving=self.vel_x != 0,
            jumping=not self.no_chao,
            skidding=skidding,
            crouching=self.crouching
        )

        if self.bowser:
            self.bowser.update(2000)
            if mario_real_rect.colliderect(self.bowser.get_rect()):
                print("Mario colidiu com o Bowser")

        # Atualiza KoopasTroopas
        for koopa in self.koopas:
            koopa.update(2000)
        self.koopas = [k for k in self.koopas if k.visible]
            # Verifica colisão koopastroopas
        """for koopa in self.koopas:
            if mario_real_rect.colliderect(koopa.get_rect()):
                if self.vel_y > 0 and mario_real_rect.bottom <= koopa.get_rect().top + 10:
                    self.vel_y = -8
                    koopa.morrer()
                else:
                    print("Mario colidiu com o Koopa!")"""
        
        current_time = pg.time.get_ticks()
        for inimigo in self.inimigos:
            if mario_real_rect.colliderect(inimigo.rect):
                if self.mario.estrela:
                    inimigo.morrer()
                    continue
                
                # Verifica se Mario está caindo e colidindo por cima
                if self.vel_y > 0 and self.mario.sprite.rect.bottom <= inimigo.rect.top + 10:
                    self.vel_y = -10  # Rebote do pulo
                    inimigo.morrer()
                    continue
                
                # Caso contrário, é dano (lateral ou por baixo)
                if not self.invencivel:
                    self.invencivel = True
                    self.invencivel_timer = 60  # 1 segundo

                    if self.mario.fogo:
                        print("Mario perdeu o poder de fogo!")
                        self.mario.fogo = False
                        self.mario.crescer(forcar=True)
                    elif self.mario.big:
                        print("Mario voltou a ser pequeno!")
                        self.mario.big = False
                        self.mario.image_idle = pg.image.load("Assets/Sprites/Mario.png").convert_alpha()
                        self.mario.frames = [
                            pg.image.load(f"Assets/Sprites/MarioRun{i}.png").convert_alpha()
                            for i in range(3)
                        ]
                        self.mario.image_jump = pg.image.load("Assets/Sprites/MarioJumping.png").convert_alpha()
                        self.mario.image_skid = pg.image.load("Assets/Sprites/MarioSkidding.png").convert_alpha()
                        self.mario.sprite.image = self.mario.image_idle
                        rect = self.mario.sprite.rect
                        self.mario.sprite.rect = self.mario.image_idle.get_rect(topleft=(rect.x, rect.y + 32))
                    else:
                        self.vidas -= 1
                        print(f"Mario perdeu uma vida! Vidas restantes: {self.vidas}")
                        if self.vidas <= 0:
                            print("MARIO MORREU")
                            self.__init__(self.LARGURA, self.ALTURA)
                            return
                        """if self.vidas <= 0:
                            print("MARIO MORREU")
                            self.__init__(self.LARGURA, self.ALTURA)
                            return"""


    def events(self, event):
        # Evento de teclado mais responsivo e correto
        self.crouching = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                self.vel_x = -VELOCIDADE
                self.mario.facing_left = True
            elif event.key == pg.K_RIGHT:
                self.vel_x = VELOCIDADE
                self.mario.facing_left = False
            elif event.key == pg.K_SPACE and self.no_chao:
                self.vel_y = IMPULSO_PULO
                self.no_chao = False
            elif event.key == pg.K_DOWN:
                self.crouching = True
            elif event.key == pg.K_b:
                if not self.mario.estrela:
                    if self.mario.fogo and self.fireball_cooldown == 0:
                        direction = 1 if not self.mario.facing_left else -1

                        # Posição X real de Mario no mundo (não a da tela)
                        mario_x = self.mario_world_x
                        mario_y = self.mario.sprite.rect.centery

                        # Ajuste para sair à frente do Mario
                        offset = 10
                        fireball_x = mario_x + offset if direction == 1 else mario_x - offset

                        fireball = Fireball(fireball_x, mario_y, direction)
                        self.fireballs.append(fireball)
                        self.fireball_cooldown = 20

                    
        elif event.type == pg.KEYUP:
            if event.key in [pg.K_LEFT, pg.K_RIGHT]:
                self.vel_x = 0
