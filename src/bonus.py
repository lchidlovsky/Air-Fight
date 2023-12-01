import pygame
from constantes import *

class Bonus(pygame.sprite.Sprite):
    """classe représentant un bonus
    """
    def __init__(self, type, coord=[0, 0]):
        pygame.sprite.Sprite.__init__(self)
        
        self.type = type
        self.image = pygame.image.load("images/bonus/bonus.png").convert_alpha()
        match self.type:
            case 'coeur':
                self.image = pygame.image.load("images/bonus/bonus_coeur.png").convert_alpha()
            case 'munitions':
                self.image = pygame.image.load("images/bonus/bonus_munitions.png").convert_alpha()
            case 'explosif':
                self.image = pygame.image.load("images/bonus/bonus_explosif.png").convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.midbottom = coord
        
        self.vitesse = vitesse_bonus

    def update(self):
        self.rect.top += self.vitesse