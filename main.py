import constants
import utils
import os
import random
import math
import pygame
from os.path import join

pygame.init()


pygame.display.set_caption("Platformer")



window = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))

class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    GRAVITY = 1
    ANIMATION_DELAY = 1
    SPRITES = utils.load_sprite_sheets("MainCharacters", "MaskDude", 32, 32, True)

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self, vel):
        self.x_vel = -vel

        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self, fps):
        #self.y_vel += min(1, (self.fall_count/fps)*self.GRAVITY)
        #self.y_vel += self.fall_count/fps*self.GRAVITY
        self.move(self.x_vel, self.y_vel)

        self.fall_count += 1
        self.update_sprite()
        #self.update()

    def update_sprite(self):
        sprite_sheet = "idle" #default spreadsheet (when no action is occurring)
        if self.x_vel != 0:
            sprite_sheet = "run"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win):
        #pygame.draw.rect(win, self.COLOR, self.rect)
        #self.sprite = self.SPRITES["idle_" + self.direction][0]
        win.blit(self.sprite, (self.rect.x, self.rect.y))

class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = utils.get_block(size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

def get_background(name):
    image = pygame.image.load(join("assets", "Background", name))
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(constants.WIDTH // width + 1):
        for j in range(constants.HEIGHT // height + 1):
            pos = (i * width, j*height)
            tiles.append(pos)

    return tiles, image


def draw(window, background, bg_image, player, objects):
    for tile in background:
        window.blit(bg_image, tile)
        
    for obj in objects:
        obj.draw(window)

    player.draw(window)
    
    pygame.display.update()

def handle_move(player):
    keys = pygame.key.get_pressed()

    player.x_vel = 0
    if keys[pygame.K_LEFT]:
        player.move_left(constants.PLAYER_VEL)

    if keys[pygame.K_RIGHT]:
        player.move_right(constants.PLAYER_VEL)



def main(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("Blue.png")
    block_size = 96

    player = Player(100, 100, 50, 50)
    #blocks = [Block(0, HEIGHT - block_size, block_size)]
    
    floor = [Block(i*block_size, constants.HEIGHT - block_size, block_size) 
             for i in range(-constants.WIDTH // block_size, (constants.WIDTH*2) // block_size)]
    
    run = True
    while run:
        clock.tick(constants.FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        player.loop(constants.FPS)
        handle_move(player)
        draw(window, background, bg_image, player, floor)

    pygame.quit()
    quit()


if __name__== "__main__":
    main(window)