# Autor original: https://github.com/kidscancode/pygame_tutorials
# KidsCanCode - Game Development with Pygame video series
# Jumpy! (a platform game)
# Video link: https://youtu.be/G8pYfkIajE8
# Modificado por: rmnicola

import os
import pygame as pg
from pygame.locals import *

os.environ['SDL_VIDEO_CENTERED'] = '1' #Garante que a janela seja centralizada

#CORES
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GRAY = (125, 125, 125)
BLUE = (0,0,255)
RED = (255,0,0)

#TAMANHO DA TELA
HEIGHT = 600
WIDTH = 1200

#Inicializar
pg.init()
size = WIDTH, HEIGHT
screen = pg.display.set_mode(size)
pg.display.set_caption("Beer Pong")
clock = pg.time.Clock()

# Player properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.8
JUMP = -20

vec = pg.math.Vector2

#CLASSE DO JOGADOR
class Power(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface ( (40, 10) ) #Cria superfície retangular
        self.image.fill(WHITE)
        self.rect = self.image.get_rect() #Ajusta um retângulo à imagem definida acima
        self.pos = vec(WIDTH-20, HEIGHT-40)
        self.rect.center = self.pos
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.flag = 0

    
    def jump(self):
        if self.flag == 0:        
            if self.vel.y == 0:
                self.vel.y = JUMP
        if self.flag == 1:
            self.acc.y = 0
            self.vel.y = 0
        
    def update(self):
        self.acc = vec(0, PLAYER_GRAV)
        if self.flag == 1:
            self.jump()

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # wrap around the sides of the screen
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos

class Angle(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface ( (40, 10) ) #Cria superfície retangular
        self.image.fill(RED)
        self.rect = self.image.get_rect() #Ajusta um retângulo à imagem definida acima
        self.pos = vec(WIDTH-100, HEIGHT-140)
        self.rect.center = self.pos
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.flag = 0

    def update(self):
        if self.flag == 0:
            if self.vel.y == 0:
                self.acc = vec(0, PLAYER_GRAV)
                self.vel.y = JUMP
                self.flag = 1
                
        if self.flag == 1:
            if self.pos.y < (HEIGHT - 140):
                self.acc = vec(0, PLAYER_GRAV)
                if self.pos.y == (HEIGHT - 240):
                    self                    
                    self.vel.y = 0
                    self.vel.y = (-1)*JUMP
            if self.pos.y > (HEIGHT - 140):
                self.acc = vec(0, ((-1)*(PLAYER_GRAV)))
                self.vel.y = 0
                self.vel.y = JUMP
                
        if self.flag == 2:
            self.acc.y=0
            self.vel.y=0

        # equations of motion                
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.rect.midbottom = self.pos
        
class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.midbottom = x, y

i=0

bar = Power()
ang = Angle()
plat = Platform( WIDTH / 2, HEIGHT, WIDTH, 40)


all_sprites = pg.sprite.Group()
all_sprites.add(bar)
all_sprites.add(ang)
all_sprites.add(plat)

power_bar = pg.sprite.Group()
power_bar.add(bar)

plat_sprites = pg.sprite.Group()
plat_sprites.add(plat)

#barra=[]
#all_sprites.add(barra)
#power_bar.add(barra)

rodando = True
#Game loop
while rodando:
    clock.tick(60)
    #Eventos
    for evt in pg.event.get():
        if evt.type == pg.QUIT:
            rodando = False
        if evt.type == pg.KEYDOWN:
            if evt.key == K_ESCAPE:
                rodando = False
            if evt.key == K_SPACE:
                bar.jump()
            if evt.key == K_RETURN:
                bar.flag = 1
            if evt.key == K_a:
                ang.flag = 2
                
    #Atualizar
    all_sprites.update()
    if bar.vel.y > 0:
        i=i
#        bar.size += 1
#        b1 = Power()
#        barra[0]
#        i += 1
#    if bar.vel.y < 0:
#
        hits = pg.sprite.spritecollide(bar, plat_sprites, False)
        
        if hits:
            bar.vel.y = 0
            bar.pos.y = hits[0].rect.top

        
    if ang.vel.y < 0:
        hits2 = pg.sprite.spritecollide(ang, plat_sprites, False)
        if hits2:
            ang.vel.y = 0
            ang.pos.y = hits2[0].rect.top
    #Desenhar
    screen.fill(BLACK)
    all_sprites.draw(screen)
    pg.display.flip()
    
    