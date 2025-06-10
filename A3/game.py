import pygame as pg
from obj import Mario, Bloco, Cogumelo, QuestionBlock, Estrela, FlorDeFogo, Fireball, Coin, Flag
from enemies import Goomba, Bowser, KoopaTroopa

# Constantes
AZUL = (135, 206, 235)
VERDE = (34, 139, 34)
AMARELO = (194, 178, 128)
CINZA = (192, 192, 192)
GRAVIDADE = 1
VELOCIDADE = 3
IMPULSO_PULO = -12
CHAO_Y = 270  # Altura do chão fixo (ALTURA - 30 do seu código)


class Game:
    def __init__(self, largura, altura):
        self.LARGURA = largura
        self.ALTURA = altura
        self.change_scene = False
        self.pulo = pg.mixer.Sound("Assets/Audio/jump.wav")
        self.som_estrela = pg.mixer.Sound("Assets/Audio/hurryup.wav")
        self.som_fireball = pg.mixer.Sound("Assets/Audio/fireball.wav")
        self.mario_world_x = 0
        self.mario_screen_x = 50
        self.mario_y = altura - 120
        self.vel_x = 0
        self.vel_y = 0
        self.no_chao = False
        self.vidas = 3
        self.mario = Mario("Assets/Sprites/Mario.png", self.mario_screen_x, self.mario_y, animated=True)
        self.cogumelo = None
        self.estrela = None
        self.flor = None
        self.coin = None
        self.crouching = False
        self.invencivel_timer = 0
        self.invencivel = False
        self.goombas = []
        self.blocos = []
        self.bowser = Bowser(600, altura - 62)
        self.koopas = []
        self.fireballs = []
        self.fireball_cooldown = 0
        self.inimigos = [self.bowser] + self.koopas + self.goombas
        self.inimigo = None
        self.flag = None
        self.moedas = []
        self.fase_atual = 1
        self.total_fases = 3
        self.carregar_fase(self.fase_atual)
        self.callback_encerrar = None

    def carregar_fase(self, fase):
        # Limpa os elementos anteriores
        self.blocos = []
        self.goombas = []
        self.koopas = []
        self.moedas = []
        self.bowser = None
        self.cogumelo = None
        self.estrela = None
        self.flor = None
        self.coin = None

        # Resetar posição do Mario
        self.mario_world_x = 0
        self.mario.sprite.rect.y = self.ALTURA - 120

        if fase == 1:
            self.blocos = [Bloco(-16, CHAO_Y - 32), 
                           Bloco(-16, CHAO_Y), 
                           Bloco(-16, CHAO_Y - 16), 
                           Bloco(-16, CHAO_Y - 48), 
                           Bloco(-16, CHAO_Y + 16), 
                           Bloco(-16, CHAO_Y - 64), 
                           Bloco(-16, CHAO_Y - 80),
                           Bloco(318, CHAO_Y -61),
                           Bloco(334, CHAO_Y -61),
                           Bloco(366, CHAO_Y -61),
                           QuestionBlock(350, CHAO_Y - 61, contem_cogumelo=True),
                           QuestionBlock(700, CHAO_Y - 61, contem_cogumelo_vida=True),
                           Bloco(400,CHAO_Y - 16)]
            self.goombas = [Goomba(300, CHAO_Y - 15),
                            Goomba(600, CHAO_Y - 15)]
            self.moedas = [Coin(400, CHAO_Y - 100)]
            self.flag = Flag(1800, CHAO_Y - 15)

        elif fase == 2:
            self.blocos = [Bloco(-16, CHAO_Y - 32), 
                           Bloco(-16, CHAO_Y), 
                           Bloco(-16, CHAO_Y - 16), 
                           Bloco(-16, CHAO_Y - 48), 
                           Bloco(-16, CHAO_Y + 16), 
                           Bloco(-16, CHAO_Y - 64), 
                           Bloco(-16, CHAO_Y - 80),
                           QuestionBlock(250, CHAO_Y - 48, contem_flor=True)]
            self.koopas = [KoopaTroopa(450, CHAO_Y - 25)]
            self.moedas = [Coin(300, CHAO_Y - 100)]
            self.flag = Flag(800, CHAO_Y - 15)

        elif fase == 3:
            self.blocos = [Bloco(-16, CHAO_Y - 32), 
                           Bloco(-16, CHAO_Y), 
                           Bloco(-16, CHAO_Y - 16), 
                           Bloco(-16, CHAO_Y - 48), 
                           Bloco(-16, CHAO_Y + 16), 
                           Bloco(-16, CHAO_Y - 64), 
                           Bloco(-16, CHAO_Y - 80),
                           QuestionBlock(150, CHAO_Y - 48, contem_estrela=True),
                           Bloco(600, CHAO_Y - 32)]
            self.bowser = Bowser(600, self.ALTURA - 62)
            self.moedas = [Coin(350, CHAO_Y - 100)]
            self.flag = Flag(1000, CHAO_Y - 15)

    def draw(self, window):
        window.fill(AZUL)
        camera_x = self.mario_world_x - self.mario_screen_x

        # Chão
        pg.draw.rect(window, VERDE, (0 - camera_x, self.ALTURA - 30, 2000, 30))
        if self.fase_atual == 2:
            pg.draw.rect(window, AMARELO, (0 - camera_x, self.ALTURA - 30, 2000, 30))
        if self.fase_atual == 3:
            pg.draw.rect(window, CINZA, (0 - camera_x, self.ALTURA - 30, 2000, 30))

        # Desenha blocos e atualiza animações
        for bloco in self.blocos:
            bloco.draw(window, camera_x)
            if isinstance(bloco, QuestionBlock):
                bloco.update()

        # Desenha inimigos e itens
        for goomba in self.goombas:
            goomba.draw(window, camera_x)

        if self.cogumelo:
            self.cogumelo.draw(window, camera_x)

        if self.flag:
            self.flag.draw(window, camera_x)

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

        for coin in self.moedas:
            coin.draw(window, camera_x)

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
        self.inimigos += [g for g in self.goombas]
        if self.bowser:
            self.inimigos.append(self.bowser)
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
            self.inimigos += [g for g in self.goombas]
            self.inimigos += [k for k in self.koopas if k.visible]

            # Colisão com inimigos
            for inimigo in self.inimigos:
                self.inimigo = inimigo
                inimigo.rect = self.inimigo.rect
                if fireball.rect.colliderect(inimigo.rect):
                    inimigo.morrer()
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
        for goomba in self.goombas:
            goomba.update(2000)
            for bloco in self.blocos:
                if goomba.rect.colliderect(bloco.get_rect()):
                    goomba.direction *= -1
            if goomba and not goomba.alive:
                goomba = None
        self.goombas = [g for g in self.goombas]

        # Atualiza cogumelo
        if self.cogumelo:
            self.cogumelo.update(2000)

            if not self.cogumelo.subindo:
                # Movimento horizontal
                for bloco in self.blocos:
                    if self.cogumelo.rect.colliderect(bloco.get_rect()):
                        if self.cogumelo.direction > 0:
                            self.cogumelo.rect.right = bloco.get_rect().left
                        elif self.cogumelo.direction < 0:
                            self.cogumelo.rect.left = bloco.get_rect().right
                        self.cogumelo.direction *= -1

                # Gravidade
                self.cogumelo.vel_y += self.cogumelo.gravidade
                self.cogumelo.rect.y += self.cogumelo.vel_y

                # Colisão vertical
                for bloco in self.blocos:
                    if self.cogumelo.rect.colliderect(bloco.get_rect()):
                        if self.cogumelo.vel_y > 0:
                            self.cogumelo.rect.bottom = bloco.get_rect().top
                            self.cogumelo.vel_y = 0
                        elif self.cogumelo.vel_y < 0:
                            self.cogumelo.rect.top = bloco.get_rect().bottom
                            self.cogumelo.vel_y = 0

            # Colisão com o chão
            if self.cogumelo.rect.bottom >= CHAO_Y:
                self.cogumelo.rect.bottom = CHAO_Y
                self.cogumelo.vel_y = 0

            # Colisão com o Mario
            if mario_real_rect.colliderect(self.cogumelo.rect):
                if self.cogumelo.tipo == "vida":
                    self.vidas += 1
                else:
                    self.mario.crescer(forcar=False)
                self.cogumelo = None

        # Atualiza estrela
        if self.estrela:
            self.estrela.update(2000)
            for bloco in self.blocos:
                if self.estrela.rect.colliderect(bloco.get_rect()):
                    self.estrela.direction *= -1
            if mario_real_rect.colliderect(self.estrela.rect):
                print("Estrela coletada! Mario invencível?")
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
            self.inimigos.append(self.bowser)
            if mario_real_rect.colliderect(self.bowser.get_rect()):
                print("Mario colidiu com o Bowser")

        # Atualiza KoopasTroopas
        for koopa in self.koopas:
            koopa.update(2000)
            for bloco in self.blocos:
                if koopa.rect.colliderect(bloco.get_rect()):
                    koopa.direction *= -1
        self.koopas = [k for k in self.koopas if k.visible]

        for coin in self.moedas[:]:
            coin.update()
            if mario_real_rect.colliderect(coin.rect):
                coin.collect()
                self.moedas.remove(coin)
        
        for inimigo in self.inimigos:
            if mario_real_rect.colliderect(inimigo.rect):
                if self.mario.estrela:
                    inimigo.morrer()
                    continue
                
                # Verifica se Mario está caindo e colidindo por cima
                if self.vel_y > 0 and self.mario.sprite.rect.bottom <= inimigo.rect.top + 10 and not inimigo == self.bowser:
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
                        self.carregar_fase(self.fase_atual)
                        if self.vidas <= 0:
                            print("MARIO MORREU")
                            self.carregar_fase(1)
                            self.vidas = 3
                            self.fase_atual = 1

        if self.flag and mario_real_rect.colliderect(self.flag.rect):
            if self.fase_atual >= self.total_fases:
                print("Jogo concluído!")
                if self.callback_encerrar:
                    self.callback_encerrar()
            else:
                self.fase_atual += 1
                self.carregar_fase(self.fase_atual)


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
                self.pulo.play()
            elif event.key == pg.K_DOWN:
                self.crouching = True
            elif event.key == pg.K_b:
                if not self.mario.estrela:
                    if self.mario.fogo and self.fireball_cooldown == 0:
                        direction = 1 if not self.mario.facing_left else -1
                        self.som_fireball.play()
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
