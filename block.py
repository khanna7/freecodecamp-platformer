import pygame
import utils
import object

class Block(object.Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = utils.get_block(size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)