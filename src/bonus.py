import pygame
from constantes import *

class Bonus(pygame.sprite.Sprite):
    """classe représentant un bonus
    """
    def __init__(self, coord, type):
        pygame.sprite.Sprite.__init__(self)
        
        self.type = type
        match self.type:
            case 'munitions':
                self.image = pygame.image.load("images/autres/munitions.png").convert_alpha()
            case 'explosif':
                self.image = pygame.image.load("images/autres/explosif.png").convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.midbottom = coord
        
        self.vitesse = vitesse_bonus

    def update(self):
        self.rect.top += self.vitesse