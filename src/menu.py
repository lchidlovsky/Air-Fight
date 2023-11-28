import pygame
from constantes import *


class Bouton:
    """classe représentant le bouton d'un menu
    """
    
    def __init__(self, message, coord_visible, coord_cache):
        self.longueur = 290
        self.largeur = 70
        self.vitesse_deplacement = 9
        
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
    
    def transition(self):
        self.visible = not self.visible
        if not self.visible : self.selectionne = False
        
    def en_place(self):
        return self.topleft == (self.coord_visible if self.visible==True else self.coord_cache)
    
    def desti(self):
        if self.visible:
            return "coord_visible"
        return "coord_cache"
    
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
        message = font.render(self.message, True, "BLACK")
        surface.blit(message, (self.topleft[0] + self.longueur //2 - message.get_width() // 2, self.topleft[1] + self.largeur // 2 - message.get_height() // 2))
        
        #affichage du rectangle
        pygame.draw.rect(surface, 'BLACK', pygame.Rect(self.topleft, (self.longueur, self.largeur)), 4, 20)



class MenuAccueil(pygame.Surface):
    """classe représentant le menu principal du jeu
    """
    def __init__(self, size):
        pygame.Surface.__init__(self, size)
        self.fill("WHITE")
        
        self.longueur_max = size[0]
        self.hauteur_max = size[1]
        
        self.boutons = [
            Bouton("JOUER", (self.longueur_max //2, self.hauteur_max //2), (self.longueur_max //2, self.hauteur_max+40)),
            Bouton("OPTIONS", (self.longueur_max //2, self.hauteur_max //2 +100), (self.longueur_max //2, self.hauteur_max +190)),
            Bouton("QUITTER", (self.longueur_max //2, self.hauteur_max //2 +200), (self.longueur_max //2, self.hauteur_max +340)),
            Bouton("MUSIQUE : OUI", (self.longueur_max //2+280, self.hauteur_max//2-60), (self.longueur_max +150, self.hauteur_max//2-60)),
            Bouton("MENU", (self.longueur_max //2+280, self.hauteur_max//2+60), (self.longueur_max +150, self.hauteur_max//2+60))
        ]
        self.boutons_entrants = []
        self.boutons_sortants = []
        
        self.curseur = 0
        self.page = 0
        self.transition_en_cours = False
        self.continu = True
        
        self.transition_menu()
        
        
    def transition_menu(self):
        if not self.transition_en_cours:
            self.curseur = 0
            self.page = 0
            self.transition_en_cours = True
            
            #on fait transitionner tous les boutons déjà présents
            for b in self.boutons_entrants:
                self.boutons[b].transition()
                self.boutons_sortants.append(b)
            
            #on insère les trois boutons présents dans le menu principal
            for i in range(3):
                self.boutons[i].transition()
                self.boutons_entrants.append(i)
                
            self.boutons_entrants = self.boutons_entrants[-3:]

    def transition_jouer(self):
        if not self.transition_en_cours:
            self.curseur = 0
            self.page = 1
            self.transition_en_cours = True
            
            #on fait transitionner tous les boutons déjà présents
            for b in self.boutons_entrants:
                self.boutons[b].transition()
                self.boutons_sortants.append(b)
            self.boutons_entrants.clear()
        
    def transition_options(self):
        if not self.transition_en_cours:
            self.curseur = 3
            self.page = 2
            self.transition_en_cours = True
            
            #on fait transitionner tous les boutons déjà présents
            for b in self.boutons_entrants:
                self.boutons[b].transition()
                self.boutons_sortants.append(b)
            
            #on insère les trois boutons présents dans le menu principal
            for i in range(3, 5):
                self.boutons[i].transition()
                self.boutons_entrants.append(i)
                
            self.boutons_entrants = self.boutons_entrants[-2:]
    
    def transition_quitter(self):
        if not self.transition_en_cours:
            self.curseur = 0
            self.page = 3
            self.transition_en_cours = True
            
            #on fait transitionner tous les boutons déjà présents
            for b in self.boutons_entrants:
                self.boutons[b].transition()
                self.boutons_sortants.append(b)
            self.boutons_entrants.clear()
            
    def haut(self):
        if not self.transition_en_cours:
            limite = 0
            match self.page:
                case 0:
                    limite = 0
                
                case 2:
                    limite = 3
                    
            if self.curseur-1 >= limite:
                self.boutons[self.curseur].selectionne = False
                self.curseur -= 1
                self.boutons[self.curseur].selectionne = True
            print("\nUP\ncurseur =", self.curseur)
    
    def bas(self):
        if not self.transition_en_cours:
            limite = 0
            match self.page:
                case 0:
                    limite = 2
                case 2:
                    limite = 4
            if self.curseur+1 <= limite:
                self.boutons[self.curseur].selectionne = False
                self.curseur += 1
                self.boutons[self.curseur].selectionne = True
            print("\nDOWN\ncurseur =", self.curseur)
                        
    def selection(self):
        if not self.transition_en_cours:
            match self.curseur:
                case 0:
                    self.transition_jouer()
                case 1:
                    self.transition_options()
                case 2:
                    self.transition_quitter()
                case 3:
                    #activer/désactiver le son
                    pass
                case 4:
                    self.transition_menu()
                            
                    
    def update(self):
        for b in self.boutons_sortants + self.boutons_entrants:
            self.boutons[b].update()
        
        #on fait diparaitre tous les boutons venant de sortir de l'écran
        if self.transition_en_cours:
            disparition = True
            for b in self.boutons_sortants + self.boutons_entrants:
                if not self.boutons[b].en_place():
                    disparition = False
                    break
            if disparition:
                self.boutons_sortants.clear()
                self.transition_en_cours = False
                if self.boutons_entrants: self.boutons[self.boutons_entrants[0]].selectionne = True
                if self.page == 3: self.continu = False
    
    def draw(self, surface):
        surface.blit(self, (0, 0))
        
        for b in self.boutons_sortants + self.boutons_entrants:
            self.boutons[b].draw(surface)
        
        #affichage des données de debuggage
        font = pygame.font.Font(pygame.font.match_font(POLICE), 22)
        message = font.render("visible = "+("True" if self.boutons[0].visible else "False")+"  desti = "+self.boutons[0].desti(), True, "BLACK")
        surface.blit(message, (30, 30))
        message = font.render(
            str([self.boutons[b].message for b in self.boutons_sortants]) +
            str([self.boutons[b].message for b in self.boutons_entrants]), True, "BLACK")
        surface.blit(message, (30, 70))
        