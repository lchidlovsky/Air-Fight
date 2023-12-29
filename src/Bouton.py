import pygame
from constantes import POLICE

class Bouton:
    """classe représentant un bouton d'un menu
    """

    def __init__(self, message, coord_visible, coord_cache, couleur="BLACK"):
        self.longueur = 290
        self.largeur = 70
        self.vitesse_deplacement = 11
        
        self.coord_cache = [
            coord_cache[0] - coord_cache[0] % self.vitesse_deplacement - self.longueur //2,
            coord_cache[1] - coord_cache[1] % self.vitesse_deplacement - self.largeur //2]
        self.coord_visible = [
            coord_visible[0] - coord_visible[0] % self.vitesse_deplacement - self.longueur //2,
            coord_visible[1] - coord_visible[1] % self.vitesse_deplacement - self.largeur //2]
        self.topleft = [self.coord_cache[0], self.coord_cache[1]]
        
        self.message = message
        self.horloge_message = 0
        self.grossir_message = True
        self.taille_message = 25
        
        self.selectionne = False
        self.visible = False
        self.couleur = couleur
    
    def transition(self):
        self.visible = not self.visible
        if not self.visible : self.selectionne = False
        
    def en_place(self):
        return self.topleft == (self.coord_visible if self.visible==True else self.coord_cache)
    
    def update(self):
        #gestion de la taille du message
        if self.selectionne:
            #agrandissement du message
            self.horloge_message += 1
            if self.horloge_message % 5 == 0:
                self.taille_message += (1 if self.grossir_message else -1)
            
            if self.taille_message == 17 or self.taille_message == 33:
                self.grossir_message = not self.grossir_message
        else:
            self.horloge_message = 0
            self.grossir_message = True
            self.taille_message = 25

        #gestion du déplacement du bouton
        destination = (self.coord_visible if self.visible==True else self.coord_cache)
        if self.topleft != destination:
            #cas du déplacement vers haut
            if self.topleft[1] > destination[1]:
                self.topleft[1] -= self.vitesse_deplacement
            #cas du déplacement vers le bas
            if self.topleft[1] < destination[1]:
                self.topleft[1] += self.vitesse_deplacement
            #cas du déplacement vers la gauche
            if self.topleft[0] > destination[0]:
                self.topleft[0] -= self.vitesse_deplacement
            #cas du déplacement vers la droite
            if self.topleft[0] < destination[0]:
                self.topleft[0] += self.vitesse_deplacement
    
    def draw(self, surface):
        #affichage du message
        font = pygame.font.Font(pygame.font.match_font(POLICE), self.taille_message)
        message = font.render(self.message, True, self.couleur)
        surface.blit(message, (self.topleft[0] + self.longueur //2 - message.get_width() // 2, self.topleft[1] + self.largeur // 2 - message.get_height() // 2))
        
        if self.selectionne:
            #affichage du rectangle aux angles rentrés
            coin = self.largeur//4
            
            pygame.draw.circle(
                surface, self.couleur, (self.topleft[0], self.topleft[1]),
                coin, width=5, draw_bottom_right=True)
            pygame.draw.circle(
                surface, self.couleur, (self.topleft[0]+self.longueur, self.topleft[1]),
                coin, width=5, draw_bottom_left=True)
            pygame.draw.circle(
                surface, self.couleur, (self.topleft[0]+self.longueur, self.topleft[1]+self.largeur),
                coin, width=5, draw_top_left=True)
            pygame.draw.circle(
                surface, self.couleur, (self.topleft[0], self.topleft[1]+self.largeur),
                coin, width=5, draw_top_right=True)
            
            pygame.draw.line(surface, self.couleur,
                (self.topleft[0]+coin, self.topleft[1]+2), (self.topleft[0]+self.longueur-coin, self.topleft[1]+2), 5)
            pygame.draw.line(surface, self.couleur,
                (self.topleft[0]+self.longueur-2, self.topleft[1]+coin), (self.topleft[0]+self.longueur-2, self.topleft[1]+self.largeur-coin), 5)
            pygame.draw.line(surface, self.couleur,
                (self.topleft[0]+self.longueur-coin, self.topleft[1]+self.largeur-2), (self.topleft[0]+coin, self.topleft[1]+self.largeur-2), 5)
            pygame.draw.line(surface, self.couleur,
                (self.topleft[0]+2, self.topleft[1]+self.largeur-coin), (self.topleft[0]+2, self.topleft[1]+coin), 5)

            #affichage des quatre petits cercles
            pygame.draw.circle(
                surface, self.couleur, (self.topleft[0]-self.taille_message//2 +9, self.topleft[1]-self.taille_message//2 +9),
                coin//3, width=0)
            pygame.draw.circle(
                surface, self.couleur, (self.topleft[0]+self.longueur+self.taille_message//2 -9, self.topleft[1]-self.taille_message//2 +9),
                coin//3, width=0)
            pygame.draw.circle(
                surface, self.couleur, (self.topleft[0]+self.longueur+self.taille_message//2 -9, self.topleft[1]+self.largeur+self.taille_message//2 -9),
                coin//3, width=0)
            pygame.draw.circle(
                surface, self.couleur, (self.topleft[0]-self.taille_message//2 +9, self.topleft[1]+self.largeur+self.taille_message//2 -9),
                coin//3, width=0)
            
        else:
            #affichage du rectangle
            pygame.draw.rect(surface, self.couleur, pygame.Rect(self.topleft, (self.longueur, self.largeur)), 5, 20)
