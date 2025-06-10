import pygame as pg

class Mario:
    def __init__(self, image_idle, x, y, animated=False):
        self.group = pg.sprite.Group()
        self.sprite = pg.sprite.Sprite(self.group)

        self.animated = animated
        self.big = False
        self.facing_left = False
        self.fogo = False
        self.estrela = False
        self.estrela_timer = 0
        self.estado_pre_estrela = None
        self.fireballs = []
        self.fireball_cooldown = 0 
        self.som_estrela = pg.mixer.Sound("Assets/Audio/hurryup.wav")
        self.image_idle = pg.image.load(image_idle).convert_alpha()
        self.image_jump = pg.image.load("Assets/Sprites/MarioJumping.png").convert_alpha()
        self.image_skid = pg.image.load("Assets/Sprites/MarioSkidding.png").convert_alpha()
        self.crouching = False

        if animated:
            self.frames = [
                pg.image.load(f"Assets/Sprites/MarioRun{i}.png").convert_alpha()
                for i in range(3)
            ]
            self.current_frame = 0
            self.animation_timer = 0
            self.sprite.image = self.image_idle
        else:
            self.sprite.image = self.image_idle

        self.sprite.rect = self.sprite.image.get_rect()
        self.sprite.rect.topleft = (x, y)

    def crescer(self, forcar=False):
        if self.fogo and not forcar:
            return
        if self.estrela and not forcar:
            return
        self.big = True
        self.image_idle = pg.image.load("Assets/Sprites/SuperMario.png").convert_alpha()
        self.frames = [
            pg.image.load(f"Assets/Sprites/SuperMarioRun{i}.png").convert_alpha()
            for i in range(3)
        ]
        self.image_jump = pg.image.load("Assets/Sprites/SuperMarioJumping.png").convert_alpha()
        self.image_skid = pg.image.load("Assets/Sprites/SuperMarioSkidding.png").convert_alpha()
        self.image_crouch = pg.image.load("Assets/Sprites/SuperMarioCrouching.png").convert_alpha()
        self.sprite.image = self.image_idle

        rect = self.sprite.rect
        self.sprite.rect = self.image_idle.get_rect(topleft=(rect.x, rect.y - 32))

    def virar_fogo(self, forcar = False):
        if self.estrela and not forcar:
            return
        self.fogo = True
        self.image_idle = pg.image.load("Assets/Sprites/FieryMario.png").convert_alpha()
        self.frames = [
            pg.image.load(f"Assets/Sprites/FieryMarioRun{i}.png").convert_alpha()
            for i in range(3)
        ]
        self.image_jump = pg.image.load("Assets/Sprites/FieryMarioJumping.png").convert_alpha()
        self.image_skid = pg.image.load("Assets/Sprites/FieryMarioSkidding.png").convert_alpha()
        self.image_crouch = pg.image.load("Assets/Sprites/FieryMarioCrouching.png").convert_alpha()
        self.sprite.image = self.image_idle

        rect = self.sprite.rect
        self.sprite.rect = self.image_idle.get_rect(topleft=(rect.x, rect.y - 32))

    def marioestrela(self):
        if self.fogo:
            self.estado_pre_estrela = "fogo"
        else:
            self.estado_pre_estrela = "super"

        if not self.big and not self.fogo:
            self.crescer()
        self.som_estrela.play(loops=-1)
        self.estrela = True
        self.estrela_timer = 600  # Duração da invencibilidade (~10 segundos a 60 FPS)

        self.frames_idle = [
            pg.image.load("Assets/Sprites/SuperMario.png").convert_alpha(),
            pg.image.load("Assets/Sprites/FieryMario.png").convert_alpha(),
            pg.image.load("Assets/Sprites/SuperLuigi.png").convert_alpha()
        ]

        self.frames = [
            [
                pg.image.load(f"Assets/Sprites/SuperMarioRun{i}.png").convert_alpha(),
                pg.image.load(f"Assets/Sprites/FieryMarioRun{i}.png").convert_alpha(),
                pg.image.load(f"Assets/Sprites/SuperLuigiRun{i}.png").convert_alpha()
            ]
            for i in range(3)
        ]

        self.frames_jump = [
            pg.image.load("Assets/Sprites/SuperMarioJumping.png").convert_alpha(),
            pg.image.load("Assets/Sprites/FieryMarioJumping.png").convert_alpha(),
            pg.image.load("Assets/Sprites/SuperLuigiJumping.png").convert_alpha()
        ]

        self.frames_skid = [
            pg.image.load("Assets/Sprites/SuperMarioSkidding.png").convert_alpha(),
            pg.image.load("Assets/Sprites/FieryMarioSkidding.png").convert_alpha(),
            pg.image.load("Assets/Sprites/SuperLuigiSkidding.png").convert_alpha()
        ]

        self.frames_crouch = [
            pg.image.load("Assets/Sprites/SuperMarioCrouching.png").convert_alpha(),
            pg.image.load("Assets/Sprites/FieryMarioCrouching.png").convert_alpha(),
            pg.image.load("Assets/Sprites/SuperLuigiCrouching.png").convert_alpha()
        ]

    def update(self, tile_list=None, world_width=None):
        if self.estrela:
            self.estrela_timer -= 1
            if self.estrela_timer <= 0:
                self.estrela = False
                self.som_estrela.stop()
                print("Acabou estrela")
                if self.estado_pre_estrela == "fogo":
                    self.virar_fogo(forcar=True)
                else:
                    self.crescer(forcar=True)

        # Atualizar cooldown da bola de fogo
        if self.fireball_cooldown > 0:
            self.fireball_cooldown -= 1

        # Atualizar bolas de fogo
        if tile_list is not None and world_width is not None:
            for fireball in self.fireballs[:]:
                fireball.update(tile_list)
                if fireball.rect.right < 0 or fireball.rect.left > world_width:
                    self.fireballs.remove(fireball)

    def draw(self, window):
        self.group.draw(window)
        for fireball in self.fireballs:
            fireball.draw(window, 0)  # Assumindo câmera em 0 ou ajustar conforme seu código

    def update_position(self, dx, dy):
        self.sprite.rect.x += dx
        self.sprite.rect.y += dy

    def animate(self, moving, jumping=False, skidding=False, crouching=False):
        if self.estrela:
            index = (pg.time.get_ticks() // 100) % 3

            # Piscar nos últimos 3 segundos (180 frames)
            if self.estrela_timer < 180:
                if (self.estrela_timer // 6) % 2 == 0:
                    self.sprite.image = pg.Surface((0, 0), pg.SRCALPHA)  # Invisível temporariamente
                    return
            old_bottom = self.sprite.rect.bottom  # Salvar posição do chão antes de trocar imagem

            if crouching and (self.big or self.fogo):
                image = self.frames_crouch[index]
            elif jumping:
                image = self.frames_jump[index]
            elif skidding:
                image = self.frames_skid[index]
            elif moving:
                self.animation_timer += 1
                if self.animation_timer >= 8:
                    self.current_frame = (self.current_frame + 1) % len(self.frames)
                    self.animation_timer = 0
                image = self.frames[self.current_frame][index]
            else:
                image = self.frames_idle[index]

            if self.facing_left:
                image = pg.transform.flip(image, True, False)

            self.sprite.image = image
            self.sprite.rect = image.get_rect()
            self.sprite.rect.bottom = old_bottom  # Reposiciona corretamente
            return

        # Fora do modo estrela: segue comportamento normal
        if crouching and (self.big or self.fogo):
            if not self.crouching:
                image = self.image_crouch
                if self.facing_left:
                    image = pg.transform.flip(image, True, False)
                old_bottom = self.sprite.rect.bottom
                self.sprite.image = image
                self.sprite.rect = image.get_rect()
                self.sprite.rect.bottom = old_bottom
                self.crouching = True
            return
        elif self.crouching:
            self.crouching = False
            old_bottom = self.sprite.rect.bottom
            self.sprite.image = self.image_idle
            self.sprite.rect = self.image_idle.get_rect()
            self.sprite.rect.bottom = old_bottom

        if jumping:
            image = self.image_jump
        elif skidding:
            image = self.image_skid
        elif not self.animated:
            return
        elif moving:
            self.animation_timer += 1
            if self.animation_timer >= 8:
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.animation_timer = 0
            image = self.frames[self.current_frame]
        else:
            image = self.image_idle

        if self.facing_left:
            image = pg.transform.flip(image, True, False)
        self.sprite.image = image

    def set_y(self, y):
        self.sprite.rect.y = y

    def get_rect(self):
        return self.sprite.rect

class Bloco:
    def __init__(self, x, y, tipo="brown", tema="brown"):
        self.tema = tema
        self.tipo = tipo  # Pode ser usado para lógica futura

        # Define a imagem do bloco conforme o tipo
        if tipo == "brown":
            imagem = "BrickBlockBrown.png"
        elif tipo == "castle":
            imagem = "BrickBlockCastle.png"
        elif tipo == "dark":
            imagem = "BrickBlockDark.png"
        elif tipo == "question":
            imagem = "QuestionBlock0.png"  # Placeholder para bloco de questão
        else:
            raise ValueError(f"Tipo de bloco desconhecido: {tipo}")

        self.image = pg.image.load(f"Assets/Sprites/{imagem}").convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, window, camera_x):
        window.blit(self.image, (self.rect.x - camera_x, self.rect.y))

    def get_rect(self):
        return self.rect

class Cogumelo:
    def __init__(self, x, y, tipo="normal", dark=False):
        self.tipo = tipo
        self.dark = dark

        # Define imagem do cogumelo conforme o tipo e tema
        if tipo == "vida":
            nome_arquivo = "1upMushroomDark.png" if dark else "1upMushroom.png"
        else:
            nome_arquivo = "Mushroom.png"

        self.image = pg.image.load(f"Assets/Sprites/{nome_arquivo}").convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 2
        self.direction = -1
        self.subindo = True  # Indica se está saindo do bloco
        self.alvo_y = y - 32  # Altura alvo ao subir
        self.vel_y = 0
        self.gravidade = 1

    def update(self, world_width):
        if self.subindo:
            self.rect.y -= 2
            if self.rect.y <= self.alvo_y:
                self.subindo = False
        else:
            self.vel_y += self.gravidade
            self.rect.y += self.vel_y
            self.rect.x += self.speed * self.direction

            # Inverte a direção ao atingir os limites do mundo
            if self.rect.left <= 0 or self.rect.right >= world_width:
                self.direction *= -1

    def draw(self, window, camera_x):
        window.blit(self.image, (self.rect.x - camera_x, self.rect.y))

    def get_rect(self):
        return self.rect

class QuestionBlock(Bloco):
    def __init__(self, x, y, tema="brown", contem_cogumelo=False, contem_estrela=False, contem_flor=False, contem_cogumelo_vida=False, contem_moeda=False):
        self.ativo = True
        super().__init__(x, y, tipo="question", tema=tema)
        self.frames = self.load_frames(tema)
        self.current_frame = 0
        self.animation_timer = 0
        self.hit = False
        self.contem_cogumelo = contem_cogumelo
        self.contem_estrela = contem_estrela
        self.contem_flor = contem_flor
        self.contem_cogumelo_vida = contem_cogumelo_vida
        self.contem_moeda = contem_moeda

    def load_frames(self, tema):
        prefix = "QuestionBlock"
        if tema == "castle":
            prefix = "QuestionBlockCastle"
        elif tema == "dark":
            prefix = "QuestionBlockDark"
        return [pg.image.load(f"Assets/Sprites/{prefix}{i}.png").convert_alpha() for i in range(6)]

    def update(self):
        if not self.ativo or self.hit:
            if self.tema in ["brown", "castle", "dark"]:
                vazio = f"EmptyBlock{self.tema.capitalize()}.png"
            else:
                vazio = "EmptyBlockBrown.png"
            self.image = pg.image.load(f"Assets/Sprites/{vazio}").convert_alpha()
            return  # <- não anima mais

        self.animation_timer += 1
        if self.animation_timer >= 8:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.animation_timer = 0
        self.image = self.frames[self.current_frame]

    def ativar(self):
        if not self.ativo:
            return None
        self.ativo = False
        self.hit = True
        if self.contem_cogumelo_vida:
            return Cogumelo(self.rect.x, self.rect.y, tipo="vida")

        if self.contem_cogumelo:
            return Cogumelo(self.rect.x, self.rect.y, tipo="normal")

        if self.contem_estrela:
            return Estrela(self.rect.x, self.rect.y)

        if self.contem_flor:
            return FlorDeFogo(self.rect.x, self.rect.y)
        
        if self.contem_moeda:
            return Coin(self.rect.x, self.rect.y)
        return None

class Estrela:
    def __init__(self, x, y):
        self.frames = [
            pg.image.load(f"Assets/Sprites/Estrela{i}.png").convert_alpha()
            for i in range(4)
        ]
        self.current_frame = 0
        self.animation_timer = 0
        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.direction = 1
        self.vel_y = -10  # impulso inicial para pulo
        self.gravity = 1
        self.bounce_strength = -10
        self.speed = 3

    def update(self, world_width):
        # Animação da estrela
        self.animation_timer += 1
        if self.animation_timer >= 8:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
            self.animation_timer = 0

        # Movimento horizontal e troca de direção nos limites
        self.rect.x += self.speed * self.direction
        if self.rect.left <= 0 or self.rect.right >= world_width:
            self.direction *= -1

        # Gravidade e quique no chão fixo (240)
        self.vel_y += self.gravity
        self.rect.y += self.vel_y
        if self.rect.bottom >= 270:
            self.rect.bottom = 270
            self.vel_y = self.bounce_strength

    def draw(self, window, camera_x):
        window.blit(self.image, (self.rect.x - camera_x, self.rect.y))

    def get_rect(self):
        return self.rect
    
class FlorDeFogo:
    def __init__(self, x, y):
        self.frames = [
            pg.image.load(f"Assets/Sprites/Flor{i}.png").convert_alpha()
            for i in range(4)
        ]
        self.current_frame = 0
        self.animation_timer = 0
        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=(x, y))
        
        self.vel_y = -2  # Suaviza o movimento de subida
        self.max_rise = 16  # Sobe 16 pixels (1 bloco)
        self.spawn_y = y  # Altura inicial (dentro do bloco)
        self.target_y = y - self.max_rise  # Altura final (acima do bloco)

        self.finished_spawning = False

    def draw(self, window, camera_x):
        window.blit(self.image, (self.rect.x - camera_x, self.rect.y))

    def update(self, world_width=None):
        self.animation_timer += 1
        if self.animation_timer >= 10:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
            self.animation_timer = 0

        # Subir até a posição final
        if not self.finished_spawning:
            self.rect.y += self.vel_y
            if self.rect.y <= self.target_y:
                self.rect.y = self.target_y
                self.finished_spawning = True

class Fireball:
    def __init__(self, x, y, direction):
        self.frames = [
            pg.image.load(f"Assets/Sprites/Fireball{i}.png").convert_alpha()
            for i in range(4)
        ]
        self.hit_frames = [
            pg.image.load(f"Assets/Sprites/FireballHit{i}.png").convert_alpha()
            for i in range(4)
        ]
        self.current_frame = 0
        self.animation_timer = 0
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=(x, y))
        self.vel_x = 5 * direction
        self.vel_y = 0
        self.gravity = 1
        self.bounce = -6
        self.bouncing = False
        self.visible = True
        self.exploding = False  # Está em modo explosão
        self.explosion_done = False

    def explode(self):
        self.exploding = True
        self.current_frame = 0
        self.animation_timer = 0
        self.vel_x = 0
        self.vel_y = 0
        self.bouncing = False

    def update(self):
        if not self.visible:
            return

        if self.exploding:
            self.animation_timer += 1
            if self.animation_timer >= 10:
                self.current_frame += 1
                self.animation_timer = 0
                if self.current_frame >= len(self.hit_frames):
                    self.explosion_done = True
                    self.visible = False
                    return
            self.image = self.hit_frames[self.current_frame]
            return

        # Movimento normal da fireball
        self.rect.x += self.vel_x

        # Animação normal
        self.animation_timer += 1
        if self.animation_timer >= 10:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
            self.animation_timer = 0

        # Gravidade e quique vertical (se quiser manter)
        if not self.bouncing:
            self.vel_y += self.gravity
            self.rect.y += self.vel_y

        CHAO_Y = 270
        if self.rect.bottom >= CHAO_Y:
            self.rect.bottom = CHAO_Y
            self.vel_y = self.bounce
            self.bouncing = True

    def draw(self, window, camera_x):
        if self.visible:
            window.blit(self.image, (self.rect.x - camera_x, self.rect.y))

class Coin:
    def __init__(self, x, y):
        self.frames = [
            pg.image.load(f"Assets/Sprites/Coin{i}.png").convert_alpha()
            for i in range(6)  # supondo 6 frames para animação da moeda
        ]
        self.som_moeda = pg.mixer.Sound("Assets/Audio/coin.wav")
        self.current_frame = 0
        self.animation_timer = 0
        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=(x, y))
        
        self.vel_y = -2  # movimento suave de subida
        self.max_rise = 16  # sobe 16 pixels (1 bloco)
        self.spawn_y = y
        self.target_y = y - self.max_rise
        
        self.finished_spawning = False
        self.collected = False  # flag para indicar se a moeda foi coletada

    def draw(self, window, camera_x):
        if not self.collected:
            window.blit(self.image, (self.rect.x - camera_x, self.rect.y))

    def update(self):
        # animação dos frames da moeda
        self.animation_timer += 1
        if self.animation_timer >= 8:  # controle da velocidade da animação
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
            self.animation_timer = 0

        # movimento de subida até a posição final
        if not self.finished_spawning:
            self.rect.y += self.vel_y
            if self.rect.y <= self.target_y:
                self.rect.y = self.target_y
                self.finished_spawning = True

    def collect(self):
        # método para chamar quando o jogador pegar a moeda
        self.som_moeda.play()
        self.collected = True

class Flag:
    def __init__(self, x, y):
        self.image = pg.image.load("Assets/Sprites/Flag.png")
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, window, camera_x):
        window.blit(self.image, (self.rect.x - camera_x, self.rect.y))

    def get_rect(self):
        return self.rect
