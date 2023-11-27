import pygame
from constantes import *

class gameBar(pygame.Surface):
    """classe représentant la barre d'informations durant la partie
    """
    def __init__(self, size, joueur):
        pygame.Surface.__init__(self, size)
        self.fill("BLACK")
       
        self.joueur = joueur
        
        self.font = pygame.font.Font(pygame.font.match_font(POLICE), 29)
        
        self.coeur = pygame.image.load("images/autres/coeur.png").convert_alpha()
        self.demi = pygame.image.load("images/autres/demi_coeur.png").convert_alpha()
        
        self.munition = pygame.image.load("images/autres/logo_munitions.png").convert_alpha()
        self.explosif = pygame.image.load("images/autres/logo_explosif.png").convert_alpha()
        self.duplication = pygame.image.load("images/autres/logo_duplication.png").convert_alpha()
        
    def draw(self, surface):
        surface.blit(self, (0, 0))

        #affichage de la vie du joueur
        for i in range (self.joueur.vie // 2):
            surface.blit(self.coeur, (i*self.coeur.get_width(), 0))
        
        #si le nombre de vies est impair
        if self.joueur.vie % 2:
            surface.blit(self.demi, ((self.joueur.vie // 2)*self.coeur.get_width(), 0))
            
            
        #affichage des informations sur le chargeur
        nb_munitions = self.font.render(str(self.joueur.chargeur), True, "WHITE")
        pos = self.get_width() - 20 - nb_munitions.get_width()
        surface.blit(nb_munitions, (pos, self.get_height() // 2 - nb_munitions.get_height() // 2))
        
        pos -= self.munition.get_width() + 20
        surface.blit(self.munition, (pos, self.get_height() // 2 - self.munition.get_height() // 2))
        
        #affichage des informations sur les explosifs
        if self.joueur.explosifs:
            nb_explosifs = self.font.render(str(self.joueur.explosifs), True, "WHITE")
            pos -= nb_explosifs.get_width() + 80
            surface.blit(nb_explosifs, (pos, self.get_height() // 2 - nb_explosifs.get_height() // 2))
            
            pos -= self.explosif.get_width() + 20
            surface.blit(self.explosif, (pos, self.get_height() // 2 - self.explosif.get_height() // 2))
            
        #affichage des informations sur les duplications
        if self.joueur.duplications:
            nb_duplications = self.font.render(str(self.joueur.duplications), True, "WHITE")
            pos -= nb_duplications.get_width() + 80
            surface.blit(nb_duplications, (pos, self.get_height() // 2 - nb_duplications.get_height() // 2))
            
            pos -= self.duplication.get_width() + 20
            surface.blit(self.duplication, (pos, self.get_height() // 2 - self.duplication.get_height() // 2))
        
