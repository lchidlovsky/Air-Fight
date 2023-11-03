import pygame

class Joueur(pygame.sprite.Sprite):
    
    def __init__(self, apparences, coord, l_max, h_max):
        pygame.sprite.Sprite.__init__(self)
        self.apparences = apparences
        self.num_apparence = 0
        self.horloge_apparence = 0
        self.animation = 1
        self.image = apparences[0]
        self.rect = self.image.get_rect()
        self.rect.center = coord
        
        self.largeur_max = l_max
        self.hauteur_max = h_max
        
        self.puissance_de_feu = 1
        self.vitesse_tirs = 15
        self.cooldown = 0

    def coordonnees(self):
        return self.rect.left, self.rect.top

    def haut(self, vitesse):
        if self.rect.top - vitesse >= 0:
            self.rect.top -= vitesse
        
    def bas(self, vitesse):
        if self.rect.bottom <= self.hauteur_max:
            self.rect.top += vitesse
        
    def gauche(self, vitesse):
        if self.rect.left - vitesse >= 0:
            self.rect.left -= vitesse
        
    def droite(self, vitesse):
        if self.rect.right <= self.largeur_max:
            self.rect.left += vitesse
    
    def tirer(self):
        if self.cooldown > 0:
            return []
        
        self.cooldown += 1
        match self.puissance_de_feu:
            case 1:
                return[(self.rect.left +50, self.rect.top +5)]
            case 2:
                return[(self.rect.left +16, self.rect.top +44),
                       (self.rect.left +80, self.rect.top +44)]
            case 3:
                return[(self.rect.left +16, self.rect.top +44),
                       (self.rect.left +50, self.rect.top +5),
                       (self.rect.left +80, self.rect.top +44)]
    
    def tick(self):
        if self.cooldown > 0:
            self.cooldown += 1
            if self.cooldown > self.vitesse_tirs:
                self.cooldown = 0
            
        self.horloge_apparence += 1
        
        match self.animation:
            case 1:
                if self.horloge_apparence < 20:
                    self.num_apparence = 0
                    self.image = self.apparences[0]
                else:
                    self.num_apparence = 1
                    self.image = self.apparences[1]
                
                if self.horloge_apparence > 40:
                    self.horloge_apparence= 0
                
        
