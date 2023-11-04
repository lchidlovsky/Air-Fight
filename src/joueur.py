import pygame
from constantes import *
from projectile import Projectile

class Joueur(pygame.sprite.Sprite):
    """classe représentant le vaisseau du joueur
    """
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
        
        self.image_projectile = pygame.image.load(f"images/autres/projectile_1.png").convert_alpha()
        self.projectiles = pygame.sprite.Group()
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
        if self.cooldown == 0:
            self.cooldown += 1
            
            match self.puissance_de_feu:
                case 1:
                    self.projectiles.add(Projectile(self.image_projectile, (self.rect.left +50, self.rect.top +5)))

                case 2:
                    self.projectiles.add(Projectile(self.image_projectile, (self.rect.left +16, self.rect.top +44)))
                    self.projectiles.add(Projectile(self.image_projectile, (self.rect.left +80, self.rect.top +44)))

                case 3:
                    self.projectiles.add(Projectile(self.image_projectile, (self.rect.left +16, self.rect.top +44)))
                    self.projectiles.add(Projectile(self.image_projectile, (self.rect.left +50, self.rect.top +5)))
                    self.projectiles.add(Projectile(self.image_projectile, (self.rect.left +80, self.rect.top +44)))

    
    def tick(self):
        for p in self.projectiles:      #animation des projectiles tirés
            p.haut(vitesse_projectile_joueur)
            if p.rect.bottom < 0:
                self.projectiles.remove(p)
        
        if self.cooldown > 0:       #gestion de la cadence de tir
            self.cooldown += 1
            if self.cooldown > self.vitesse_tirs:
                self.cooldown = 0
        
        
        match self.animation:
            case 1:
                self.horloge_apparence += 1
                
                if self.horloge_apparence < 20:
                    self.num_apparence = 0
                    self.image = self.apparences[0]
                else:
                    self.num_apparence = 1
                    self.image = self.apparences[1]
                
                if self.horloge_apparence > 40:
                    self.horloge_apparence= 0
                
        
