import pygame

# We need to call pygame.init() before importing modules that use pygame features
pygame.init()

import constants
import player as player_module
import utils
import object
import block

import os
import random
import math

from os.path import join

print(pygame.init())


pygame.display.set_caption("Platformer")



window = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))

def main(window):
    clock = pygame.time.Clock()
    background, bg_image = utils.get_background("Blue.png")
    block_size = 96

    player = player_module.Player(100, 100, 50, 50)
    #blocks = [Block(0, HEIGHT - block_size, block_size)]
    
    floor = [block.Block(i*block_size, constants.HEIGHT - block_size, block_size) 
             for i in range(-constants.WIDTH // block_size, (constants.WIDTH*2) // block_size)]
    
    run = True
    while run:
        clock.tick(constants.FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()

        player.loop(constants.FPS)
        utils.handle_move(player, objects=floor)
        utils.draw(window, background, bg_image, player, floor)

    pygame.quit()
    quit()


if __name__== "__main__":
    main(window)