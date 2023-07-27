import pygame

# We need to call pygame.init() before importing modules that use pygame features
pygame.init()

import constants
import player as player_module
import utils
import object

import os
import random
import math

from os.path import join

print(pygame.init())


pygame.display.set_caption("Platformer")



window = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))

class Block(object.Object):
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

    player = player_module.Player(100, 100, 50, 50)
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