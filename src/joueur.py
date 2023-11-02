import pygame

class Joueur:
    
    def __init__(self, apparences, x, y, l_max, h_max):
        self.apparences = apparences
        self.num_apparence = 0
        self.x = x
        self.y = y
        self.largeur = apparences[0].get_size()[0]
        self.hauteur = apparences[0].get_size()[1]
        self.largeur_max = l_max
        self.hauteur_max = h_max
        self.horloge_apparence = 0
        
    def haut(self, vitesse):
        if self.y - vitesse >= 0:
            self.y -= vitesse
        
    def bas(self, vitesse):
        if self.y + self.hauteur <= self.hauteur_max:
            self.y += vitesse
        
    def gauche(self, vitesse):
        if self.x - vitesse >= 0:
            self.x -= vitesse
        
    def droite(self, vitesse):
        if self.x + self.largeur <= self.largeur_max:
            self.x += vitesse
        
    def visuel(self):
        return self.apparences[self.num_apparence]
    
    def coordonnees(self):
        return self.x, self.y
    
    def tick(self):
        self.horloge_apparence += 1
        
        if self.horloge_apparence < 20:
            self.num_apparence = 0
        else:
            self.num_apparence = 1
        
        if self.horloge_apparence > 40:
            self.horloge_apparence= 0