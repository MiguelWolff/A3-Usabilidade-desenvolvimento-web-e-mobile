import pygame as pg

class Obj:
    def __init__(self, image_idle, x, y, animated=False):
        self.group = pg.sprite.Group()
        self.sprite = pg.sprite.Sprite(self.group)

        self.animated = animated
        self.big = False
        self.facing_left = False
        self.fogo = False

        self.image_idle = pg.image.load(image_idle).convert_alpha()
        self.image_jump = pg.image.load("Assets/Sprites/MarioJumping.png").convert_alpha()
        self.image_skid = pg.image.load("Assets/Sprites/MarioSkidding.png").convert_alpha()
        self.crouching = False # só será carregada ao crescer

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

    def crescer(self):
        if self.fogo == True:
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

    def virar_fogo(self):
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

    def draw(self, window):
        self.group.draw(window)

    def update_position(self, dx, dy):
        self.sprite.rect.x += dx
        self.sprite.rect.y += dy

    def animate(self, moving, jumping=False, skidding=False, crouching=False):
        if crouching and (self.big or self.fogo):
            if not self.crouching:
                if self.fogo:
                    image = pg.image.load("Assets/Sprites/FieryMarioCrouching.png").convert_alpha()
                else:
                    image = pg.image.load("Assets/Sprites/SuperMarioCrouching.png").convert_alpha()
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
            if self.fogo:
                image = pg.image.load("Assets/Sprites/FieryMarioJumping.png").convert_alpha()
            elif self.big:
                image = pg.image.load("Assets/Sprites/SuperMarioJumping.png").convert_alpha()
            else:
                image = pg.image.load("Assets/Sprites/MarioJumping.png").convert_alpha()
            if self.facing_left:
                image = pg.transform.flip(image, True, False)
            self.sprite.image = image
            return

        if skidding:
            if self.fogo:
                image = pg.image.load("Assets/Sprites/FieryMarioSkidding.png").convert_alpha()
            elif self.big:
                image = pg.image.load("Assets/Sprites/SuperMarioSkidding.png").convert_alpha()
            else:
                image = pg.image.load("Assets/Sprites/MarioSkidding.png").convert_alpha()
            if self.facing_left:
                image = pg.transform.flip(image, True, False)
            self.sprite.image = image
            return

        if not self.animated:
            return

        if moving:
            self.animation_timer += 1
            if self.animation_timer >= 8:
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.animation_timer = 0
            frame = self.frames[self.current_frame]
            if self.facing_left:
                frame = pg.transform.flip(frame, True, False)
            self.sprite.image = frame
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
        self.direction = 1
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
    def __init__(self, x, y, tema="brown", contem_cogumelo=False, contem_estrela=False, contem_flor=False, contem_cogumelo_vida=False):
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

    def load_frames(self, tema):
        prefix = "QuestionBlock"
        if tema == "castle":
            prefix = "QuestionBlockCastle"
        elif tema == "dark":
            prefix = "QuestionBlockDark"
        return [pg.image.load(f"Assets/Sprites/{prefix}{i}.png").convert_alpha() for i in range(6)]

    def update(self):
        if not self.hit:
            self.animation_timer += 1
            if self.animation_timer >= 8:
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.animation_timer = 0
            self.image = self.frames[self.current_frame]

    def ativar(self):
        if not self.ativo:
            return None
        self.ativo = False
        vazio = f"EmptyBlock{self.tema.capitalize() if self.tema != 'normal' else ''}.png"
        self.image = pg.image.load(f"Assets/Sprites/{vazio}").convert_alpha()

        if self.contem_cogumelo_vida:
            return Cogumelo(self.rect.x, self.rect.y, tipo="vida")

        if self.contem_cogumelo:
            return Cogumelo(self.rect.x, self.rect.y, tipo="normal")

        if self.contem_estrela:
            return Estrela(self.rect.x, self.rect.y)

        if self.contem_flor:
            return FlorDeFogo(self.rect.x, self.rect.y)

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
    
class FlorDeFogo():
    def __init__(self, x, y):
        self.frames = [
            pg.image.load(f"Assets/Sprites/Flor{i}.png").convert_alpha()
            for i in range(4)
        ]
        self.current_frame = 0
        self.animation_timer = 0
        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel_y = -4  # Efeito de "subir" do bloco ao aparecer

    def draw(self, window, camera_x):
        window.blit(self.image, (self.rect.x - camera_x, self.rect.y))

    def update(self, world_width=None):
        self.animation_timer += 1
        if self.animation_timer >= 10:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
            self.animation_timer = 0

        # Animação de surgimento (subir um pouco e parar)
        if self.vel_y < 0:
            self.rect.y += self.vel_y
            self.vel_y += 1  # Simula desaceleração
            if self.vel_y >= 0:
                self.vel_y = 0
