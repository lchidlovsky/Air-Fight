import pygame

class Projectile(pygame.sprite.Sprite):
    """classe représentant un projectile
    """
    def __init__(self, apparence, coord):
        pygame.sprite.Sprite.__init__(self)
        self.image = apparence
        self.rect = apparence.get_rect()
        self.rect.center = coord
        
    def coordonnees(self):
        return self.rect.left, self.rect.top
    
    def haut(self, vitesse):
        self.rect.top -= vitesse
        
    def bas(self, vitesse):
        self.rect.top += vitesse