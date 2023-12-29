import pygame
from constantes import *

class GameBar(pygame.Surface):
    """classe représentant la barre d'informations durant la partie
    """
    def __init__(self, size, joueur):
        pygame.Surface.__init__(self, size)
        self.fill("BLACK")
       
        self.joueur = joueur
        
        self.font_medium = pygame.font.Font(pygame.font.match_font(POLICE), 29)
        self.font_grand = pygame.font.Font(pygame.font.match_font(POLICE), 36)
        
        self.coeur = pygame.image.load("images/autres/coeur.png").convert_alpha()
        self.demi = pygame.image.load("images/autres/demi_coeur.png").convert_alpha()
        
        self.munition = pygame.image.load("images/autres/logo_munitions.png").convert_alpha()
        self.explosif = pygame.image.load("images/autres/logo_explosif.png").convert_alpha()
        self.duplication = pygame.image.load("images/autres/logo_duplication.png").convert_alpha()
        
    def draw(self, surface, txt=""):
        surface.blit(self, (0, 0))
        x_gauche, x_droite = 0, 0
        
        #affichage de la vie du joueur
        for i in range (self.joueur.vie // 2):
            x_gauche= i*self.coeur.get_width()
            surface.blit(self.coeur, (x_gauche, self.get_height() // 2-self.coeur.get_height()//2))
            x_gauche += self.coeur.get_width()
        
        #si le nombre de vies est impair
        if self.joueur.vie % 2:
            x_gauche = (self.joueur.vie // 2)*self.coeur.get_width()
            surface.blit(self.demi, (x_gauche, self.get_height() // 2-self.demi.get_height()//2))
            x_gauche += self.demi.get_width()
               
            
        #affichage des informations sur le chargeur
        nb_munitions = self.font_medium.render(str(self.joueur.chargeur), True, "WHITE")
        x_droite = self.get_width() - 20 - nb_munitions.get_width()
        surface.blit(nb_munitions, (x_droite, self.get_height() // 2 - nb_munitions.get_height() // 2))
        
        x_droite -= self.munition.get_width() + 20
        surface.blit(self.munition, (x_droite, self.get_height() // 2 - self.munition.get_height() // 2))
        
        #affichage des informations sur les explosifs
        if self.joueur.explosifs:
            nb_explosifs = self.font_medium.render(str(self.joueur.explosifs), True, "WHITE")
            x_droite -= nb_explosifs.get_width() + 80
            surface.blit(nb_explosifs, (x_droite, self.get_height() // 2 - nb_explosifs.get_height() // 2))
            
            x_droite -= self.explosif.get_width() + 20
            surface.blit(self.explosif, (x_droite, self.get_height() // 2 - self.explosif.get_height() // 2))
            
        #affichage des informations sur les duplications
        if self.joueur.duplications:
            nb_duplications = self.font_medium.render(str(self.joueur.duplications), True, "WHITE")
            x_droite -= nb_duplications.get_width() + 80
            surface.blit(nb_duplications, (x_droite, self.get_height() // 2 - nb_duplications.get_height() // 2))
            
            x_droite -= self.duplication.get_width() + 20
            surface.blit(self.duplication, (x_droite, self.get_height() // 2 - self.duplication.get_height() // 2))
            
        
        #affichage du texte
        x_gauche += 80
        x_droite -= 80
        
        texte = self.font_grand.render(txt, True, "WHITE")
        #surface.blit(texte, ((x_droite - x_gauche) // 2 + x_gauche -texte.get_height(), self.get_height() // 2 - texte.get_height() // 2))
        surface.blit(texte, (self.get_width()//2- texte.get_width() // 2, self.get_height() // 2 - texte.get_height() // 2))
