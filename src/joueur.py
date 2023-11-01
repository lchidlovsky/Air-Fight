import pygame


class Joueur:
    
    def __init__(self, apparences, x, y, h_max, l_max):
        self.apparences = apparences
        self.x = x
        self.y = y
        self.largeur = apparences[0].get_size()[0]
        self.largeur = apparences[0].get_size()[1]
        self.hauteur_max = h_max
        self.largeur_max = l_max
        self.cooldown = 10
        
    def haut(self, vitesse):
        self.y -= vitesse
        
    def bas(self, vitesse):
        self.y += vitesse
        
    def gauche(self, vitesse):
        self.x -= vitesse
        
    def droite(self, vitesse):
        self.x += vitesse
        
    def visuel(self):
        return self.apparences[0]
    
    def coordonnees(self):
        return self.x, self.y