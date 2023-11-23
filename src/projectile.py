import pygame

class Projectile(pygame.sprite.Sprite):
    """classe représentant un projectile
    """
    def __init__(self, apparence, coord, vitesse, direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = apparence
        self.rect = apparence.get_rect()
        self.rect.center = coord
        
        self.vitesse = vitesse
        self.direction = direction
    
    def update(self):
        match self.direction:
            
            case 0:
                self.rect.top -= self.vitesse
            case 2:
                self.rect.top += self.vitesse