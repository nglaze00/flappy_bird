import pygame
import neat
import numpy as np

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_w,
    K_a,
    K_s,
    K_d,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    MOUSEBUTTONUP
)

COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255), (0, 0, 0)]
SCREEN_SIZE = 500
N_LIVES = 5
RELOAD_RATE = 30
BULLET_SPEED = 5

def make_tanks():
    # n_h_tanks = int(input("Enter # of human tanks (0 - 2):"))
    # n_bots = int(input("Enter # of bot tanks:"))
    num_h, num_b = 0, 5
    all, h, b = pygame.sprite.Group(), [], []
    i = 0
    while i < num_h:
        tank = Tank(COLORS[i], i)
        all.add(tank)
        h.append(tank)
        i += 1

    while i < num_h + num_b:
        tank = AI_Tank(COLORS[i], i)
        all.add(tank)
        b.append(tank)
        i += 1
    return h, b, all

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, vector, id):
        super(Bullet, self).__init__()

        self.surf = pygame.Surface((3, 3))
        self.surf.fill((0, 0, 0))
        self.rect = self.surf.get_rect()
        self.rect.x, self.rect.y = pos
        self.id = id

        mag = np.sqrt(vector[0] ** 2 + vector[1] ** 2)
        self.vector = np.divide(vector, mag / BULLET_SPEED)


    def move(self):
        self.rect.move_ip(*self.vector)
    def collides_with_wall(self):
        return self.rect.left < 0 or self.rect.right > 500 or self.rect.top < 0 or self.rect.bottom > 500


class Tank(pygame.sprite.Sprite):
    def __init__(self, color, index):
        super(Tank, self).__init__()

        self.surf = pygame.Surface((25, 25))
        self.surf.fill(color)
        self.rect = self.surf.get_rect()
        self.rect.x, self.rect.y = rand_pos()

        self.reloaded = 0
        self.lives = N_LIVES
        self.id = index

    def move(self, presses):
        if presses[K_w] and self.rect.top >= 0:
            self.rect.move_ip(0, -1)
        if presses[K_s] and self.rect.bottom < SCREEN_SIZE:
            self.rect.move_ip(0, 1)
        if presses[K_a] and self.rect.left >= 0:
            self.rect.move_ip(-1, 0)
        if presses[K_d] and self.rect.right < SCREEN_SIZE:
            self.rect.move_ip(1, 0)

    def reload(self):
        if self.reloaded > 0:
            self.reloaded -= 1
    def fire_bullet(self, mouse_pos):
        if self.reloaded > 0:
            return
        self.reloaded = RELOAD_RATE
        return Bullet(self.rect.center, np.subtract(mouse_pos, self.rect.center), self.id)

    def hurt(self):
        if self.lives == 1:
            self.kill()
        self.lives -= 1

class AI_Tank(Tank):
    def __init__(self, color, index):
        super(AI_Tank, self).__init__(color, index)

    def move(self, tank_vector, bullet_vector): # todo inputs from NEAT
        pass


def rand_pos():
    return np.random.randint(100, 400, size=2)



tanks_h, tanks_b, tanks_all = make_tanks()

bullets = pygame.sprite.Group()

pygame.init()

screen = pygame.display.set_mode([SCREEN_SIZE, SCREEN_SIZE])
screen.fill((255, 255, 255))

for tank in tanks_all:
    screen.blit(tank.surf, tank.rect)

pygame.display.flip()

clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        screen.fill((255, 255, 255))
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        elif event.type == QUIT:
            running = False

        # fire bullet from human tank 1
        elif event.type == MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()

            bullet = tanks_h[0].fire_bullet(mouse_pos)
            if bullet:
                bullets.add(bullet)


    screen.fill((255, 255, 255))

    # draw
    for tank in tanks_all:
        screen.blit(tank.surf, tank.rect)
    for bullet in bullets:
        screen.blit(bullet.surf, bullet.rect)
    pygame.display.flip()

    # move human tanks
    presses = pygame.key.get_pressed()
    for tank in tanks_h:
        tank.move(presses)
        tank.reload()

    # move bot tanks
    for tank in tanks_b:
        pass


    # check for bullet collisions
    for tank in tanks_all:
        for bullet in bullets:
            if pygame.sprite.collide_rect(tank, bullet) and tank.id != bullet.id:
                bullet.kill()
                tank.hurt()

    # move bullets
    for bullet in bullets:
        bullet.move()
        if bullet.collides_with_wall():
            bullet.kill()


    screen.fill((255,255,255))
    clock.tick(60)






