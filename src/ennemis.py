import pygame

class Ennemi(pygame.sprite.Sprite):
    
    def __init__(self, apparences, coord):
        pygame.sprite.Sprite.__init__(self)
        self.apparences = apparences
        self.num_apparence = 0
        self.horloge_apparence = 0
        
        self.image = apparences[0]
        self.rect = self.image.get_rect()
        self.rect.midbottom = coord
        
        self.vivant = True
        self.existant = True
        
    def tick(self):
        if not self.vivant:             #animation de destruction du vaisseau
            if self.horloge_apparence % (6*3) == 0:
                if self.num_apparence < len(self.apparences)-1:
                    self.num_apparence += 1
                    self.image = self.apparences[self.num_apparence]
                else:
                    self.existant = False

            self.horloge_apparence += 1
            
    def bas(self, vitesse):
        self.rect.top += vitesse