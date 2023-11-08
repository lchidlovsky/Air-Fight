import pygame

class Bonus(pygame.sprite.Sprite):
    """classe représentant un projectile
    """
    def __init__(self, coord, vitesse, type):
        pygame.sprite.Sprite.__init__(self)
        
        match type:
            case 1:
                self.image = pygame.image.load("images/autres/munitions.png").convert_alpha()
            case 2:
                self.image = pygame.image.load("images/autres/explosif.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.midbottom = coord
        
        self.vitesse = vitesse

    def update(self):
        self.rect.top += self.vitesse