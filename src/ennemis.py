from typing import Any
import pygame
from constantes import *
from projectile import Projectile
from random import randint, choice

class Ennemi(pygame.sprite.Sprite):
    """classe représentant un ennemi quelconque
    """
    def __init__(self, apparences, coord, vitesse):
        pygame.sprite.Sprite.__init__(self)
        self.apparences = apparences
        self.num_apparence = 0
        self.horloge_apparence = 0
        
        self.image = apparences[0]
        self.rect = self.image.get_rect()
        self.rect.midbottom = coord
        
        self.vitesse = vitesse
        
        self.vivant = True
        self.existant = True
    
    def bas(self, vitesse):
        self.rect.top += vitesse

    def update(self):
        self.bas(self.vitesse)
        
        if not self.vivant:             #animation de destruction du vaisseau
            if self.horloge_apparence % 8 == 0:
                if self.num_apparence < len(self.apparences)-1:
                    self.num_apparence += 1
                    self.image = self.apparences[self.num_apparence]
                else:
                    self.existant = False

            self.horloge_apparence += 1


class Petit(Ennemi):
    """classe représentant un petit ennemi
    """
    def __init__(self, coord):
        
        apparences = []
        for i in range(1,4):
            apparences.append(pygame.image.load(f"images/ennemis/petit_{i}.png").convert_alpha())
        
        super().__init__(apparences, coord, vitesse_petit)


class Moyen(Ennemi):
    """classe représentant un ennemi de taille moyenne
    """
    def __init__(self, coord):
        
        apparences = []
        for i in range(1,6):
            apparences.append(pygame.image.load(f"images/ennemis/moyen_{i}.png").convert_alpha())
        
        super().__init__(apparences, coord, vitesse_moyen)
        self.projectiles = pygame.sprite.Group()
        self.cadence_tirs = 100
        self.cooldown = 1
        
    def tirer(self):
        if self.vivant and self.cooldown == 0 and not randint(0, self.cadence_tirs):
            self.cooldown += 1
            return [Projectile(
                pygame.image.load(f"images/autres/projectile_2.png").convert_alpha(),
                (self.rect.left +35, self.rect.top +66), vitesse_projectile_moyen, 2)
                    ]

    def update(self):
        super().update()

        if self.cooldown > 0:       #gestion de la cadence de tir
            self.cooldown += 1
            if self.cooldown > self.cadence_tirs:
                self.cooldown = 0


















 

class Gros(Ennemi):
    """classe représentant un gros ennemi
    """
    def __init__(self, coord):
        
        apparences = []
        for i in range(1,10):
            apparences.append(pygame.image.load(f"images/ennemis/gros_{i}.png").convert_alpha())

        super().__init__(apparences, coord, vitesse_gros)
        self.dep_gauche = False
        self.vitesse_laterale = vitesse_laterale_gros
        
        self.horloge_attaque = 0
        self.preparation = False
        self.tir = False
        self.projectiles = pygame.sprite.Group()
        self.cadence_tirs = 2
        self.cooldown = 0
        
    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)
        
        if name == 'dep_gauche':
            self.num_apparence = 0
            self.image = self.apparences[0]
            self.tir = False
            self.preparation = False
            self.horloge_apparence = 0
            self.horloge_attaque = 0
        
    def tirer(self):
        if self.vivant and self.tir and self.cooldown == 0:
            self.cooldown += 1
            return [
                Projectile(
                    pygame.image.load("images/autres/laser_1.png").convert_alpha(),
                    (self.rect.left +74, self.rect.top +175), vitesse_laser_gros, 2),
                Projectile(
                    pygame.image.load("images/autres/laser_2.png").convert_alpha(),
                    (self.rect.left +90, self.rect.top +170), vitesse_laser_gros, 2)
                ]
            
    def update(self):
        self.bas(self.vitesse)
        #gestion du déplacement latéral
        if self.dep_gauche:
            self.rect.left -= self.vitesse_laterale
        else:
            self.rect.left += self.vitesse_laterale
        
        #gestion de la cadence de tir
        if self.cooldown > 0:
            self.cooldown += 1
            if self.cooldown > self.cadence_tirs:
                self.cooldown = 0
                
        
        #animation de destruction du vaisseau
        if not self.vivant:
            if self.num_apparence < 3:
                self.num_apparence = 2
                self.image = self.apparences[2]
            if self.horloge_apparence % 8 == 0:
                if self.num_apparence < len(self.apparences)-1:
                    self.num_apparence += 1
                    self.image = self.apparences[self.num_apparence]
                else:
                    self.existant = False

            self.horloge_apparence += 1
            
        else:
            
            if not self.preparation and not self.tir and not randint(0, 400):
                self.preparation = True
                
            #gestion de l'apparence durant la préparation
            if self.preparation:
                self.horloge_attaque += 1
                if self.horloge_attaque % 10 < 5:
                    self.num_apparence = 1
                    self.image = self.apparences[1]
                else:
                    self.num_apparence = 2
                    self.image = self.apparences[2]
                if self.horloge_attaque > len(self.apparences)*20:
                    self.preparation = False
                    self.tir = True
                    self.horloge_attaque = 0

            elif self.tir:
                self.num_apparence = 0
                self.image = self.apparences[0]
                self.horloge_attaque += 1
                if self.horloge_attaque > len(self.apparences)*30:
                    self.tir = False
                    self.horloge_attaque = 0
            else:
                self.num_apparence = 0
                self.image = self.apparences[0]
















class Vague:
    """classe représentant une vague d'entités volantes
    """
    def __init__(self, nom, l_max, h_max, joueur, nb_simultanes, nb_petits, nb_moyens, nb_gros):
        self.nom = nom
        self.largeur_max = l_max
        self.hauteur_max = h_max
        self.joueur = joueur
        
        self.nb_simultanes = nb_simultanes  #nm max d'ennemis en même temps à l'écran
        self.nb_visibles = 0
        self.coordonnee = []
        self.ennemis = pygame.sprite.Group()
        self.ennemis_visibles = pygame.sprite.Group()
        self.tirs_ennemis = pygame.sprite.Group()
        self.bonus = pygame.sprite.Group()
        
        for p in range(nb_petits):
            self.ennemis.add(Petit((0, 0)))
            
        for m in range(nb_moyens):
            self.ennemis.add(Moyen((0, 0)))
        
        for g in range(nb_gros):
            self.ennemis.add(Gros((0, 0)))
            
        for i in range(self.nb_simultanes):
            self.placement()


    def placement(self):
        """méthode de deplacement aléatoire des nouveaux ennemis à l'écran
        """
        if self.nb_visibles < self.nb_simultanes and self.ennemis:
            self.nb_visibles += 1

            ennemi_aleatoire = choice(self.ennemis.sprites())
            self.ennemis.remove(ennemi_aleatoire)
            if isinstance(ennemi_aleatoire, Gros):
                ennemi_aleatoire.preparation = False
                ennemi_aleatoire.tir = False
            
            if self.coordonnee : self.coordonnee.pop()
            x = randint(20, self.largeur_max-80)
            while x // 20 * 20 in self.coordonnee:
                x = randint(20, self.largeur_max-80)
            self.coordonnee.append(x)
                
            ennemi_aleatoire.rect.midbottom = (x, randint(-100, 0))
            if isinstance(ennemi_aleatoire, Gros):
                ennemi_aleatoire.dep_gauche = x > self.largeur_max // 2
            self.ennemis_visibles.add(ennemi_aleatoire)
    
           
    def update(self):
        self.tirs_ennemis.update()
        self.ennemis_visibles.update()
        self.bonus.update()
           
        for e in self.ennemis_visibles:
            
            #replacement des ennemis arrivés en bas
            if e.rect.top > self.hauteur_max or e.rect.left > self.largeur_max or e.rect.right < 0:
                self.ennemis_visibles.remove(e)
                self.nb_visibles -= 1
                self.ennemis.add(e)
                self.placement()
            
            #ajout des tirs ennemis
            if not isinstance(e, Petit):
                tir = e.tirer()
                if tir:
                    self.tirs_ennemis.add(tir)
            
            #suppression des ennemis en contact avec le joueur
            if e.vivant and e.rect.colliderect(self.joueur):
                e.vivant = False
                  
            #suppression des ennemis touchés
            for p in self.joueur.projectiles:
                if e.vivant and p.rect.colliderect(e):
                    self.joueur.projectiles.remove(p)
                    e.vivant = False
                   
            if not e.existant:
                self.ennemis_visibles.remove(e)
                self.nb_visibles -= 1
                self.placement()
                        
        
    def draw(self, surface):
        self.tirs_ennemis.draw(surface)
        self.ennemis_visibles.draw(surface)
        self.bonus.draw(surface)
