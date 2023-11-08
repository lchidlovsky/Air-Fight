import pygame
from constantes import *
from bonus import Bonus
from ennemis import *
from projectile import Projectile
from random import randint, choice

class Vague:
    """classe représentant une vague d'entités volantes
    """
    def __init__(self, nom, coord_min, coord_max, joueur, nb_simultanes, nb_petits, nb_moyens, nb_gros, nb_munitions, nb_explosifs):
        self.nom = nom
        self.largeur_min = coord_min[0]
        self.hauteur_min = coord_min[1]
        self.largeur_max = coord_max[0]
        self.hauteur_max = coord_max[1]
        self.joueur = joueur
        
        self.nb_simultanes = nb_simultanes  #nm max d'ennemis en même temps à l'écran
        self.nb_visibles = 0
        self.coordonnee = []
        self.ennemis = pygame.sprite.Group()
        self.ennemis_visibles = pygame.sprite.Group()
        self.tirs_ennemis = pygame.sprite.Group()
        
        self.bonus = pygame.sprite.Group()
        self.bonus_visibles = pygame.sprite.Group()
        
        for p in range(nb_petits):
            self.ennemis.add(Petit((0, 0)))
            
        for m in range(nb_moyens):
            self.ennemis.add(Moyen((0, 0)))
        
        for g in range(nb_gros):
            self.ennemis.add(Gros((0, 0)))
            
        for b in range(nb_munitions):
            self.bonus.add(Bonus((0, 0), 'munitions'))
            
        for b in range(nb_explosifs):
            self.bonus.add(Bonus((0, 0), 'explosif'))
            
        for i in range(self.nb_simultanes):
            self.placement_ennemi()

    def placement_bonus(self):
        """méthode de placement aléatoire de bonus à l'écran
        """
        print("\tnew bonus !!")
        bonus_aleatoire = choice(self.bonus.sprites())
        self.bonus.remove(bonus_aleatoire)
        
        if self.coordonnee : self.coordonnee.pop()
        x = randint(20, self.largeur_max-80)
        while x // 20 * 20 in self.coordonnee:
            x = randint(20, self.largeur_max-80)
        self.coordonnee.append(x)
        
        bonus_aleatoire.rect.midbottom = (x, self.hauteur_min)
        self.bonus_visibles.add(bonus_aleatoire)


    def placement_ennemi(self):
        """méthode de placement aléatoire des nouveaux ennemis à l'écran
        """
        if not randint(0, 4) and self.bonus: self.placement_bonus()
        
        if self.nb_visibles < self.nb_simultanes and self.ennemis:
            self.nb_visibles += 1

            ennemi_aleatoire = choice(self.ennemis.sprites())
            self.ennemis.remove(ennemi_aleatoire)
            
            ennemi_aleatoire.est_touche = False
            if isinstance(ennemi_aleatoire, Gros):
                ennemi_aleatoire.preparation = False
                ennemi_aleatoire.tir = False
            
            if self.coordonnee : self.coordonnee.pop()
            x = randint(20, self.largeur_max-80)
            while x // 20 * 20 in self.coordonnee:
                x = randint(20, self.largeur_max-80)
            self.coordonnee.append(x)
                
            ennemi_aleatoire.rect.midbottom = (x, randint(self.hauteur_min-111, self.hauteur_min))
            if isinstance(ennemi_aleatoire, Gros):
                ennemi_aleatoire.dep_gauche = x > self.largeur_max // 2
            self.ennemis_visibles.add(ennemi_aleatoire)
    
           
    def update(self):
        self.tirs_ennemis.update()
        self.ennemis_visibles.update()
        self.bonus_visibles.update()
           
        for e in self.ennemis_visibles:
            
            #replacement des ennemis arrivés en bas
            if e.rect.top > self.hauteur_max or e.rect.left > self.largeur_max or e.rect.right < self.largeur_min:
                self.ennemis_visibles.remove(e)
                self.nb_visibles -= 1
                self.ennemis.add(e)
                self.placement_ennemi()
            
            #ajout des tirs ennemis
            if not isinstance(e, Petit):
                tir = e.tirer()
                if tir:
                    self.tirs_ennemis.add(tir)
            
            #suppression des ennemis en contact avec le joueur
            if e.vivant and not e.est_touche and self.joueur.animation == 1 and e.rect.colliderect(self.joueur):
                self.joueur.touche(e.vie)
                e.touche(vie_gros)
                
                  
            #suppression des ennemis touchés
            for p in self.joueur.projectiles:
                if e.vivant and p.rect.colliderect(e):
                    self.joueur.projectiles.remove(p)
                    e.touche(1)
            
            #suppression des nuages de fumée
            if not e.existant:
                self.ennemis_visibles.remove(e)
                self.nb_visibles -= 1
                self.placement_ennemi()
        
        for b in self.bonus_visibles:
            
            #replacement des ennemis arrivés en bas
            if b.rect.top > self.hauteur_max:
                self.bonus_visibles.remove(b)
                self.bonus.add(b)
                
            if b.rect.colliderect(self.joueur):
                self.bonus_visibles.remove(b)
                match b.type:
                    case 'munitions':
                        self.joueur.chargeur += 10
                        
                    case 'explosif':
                        self.joueur.explosifs += 1
        
    def draw(self, surface):
        self.bonus_visibles.draw(surface)
        self.tirs_ennemis.draw(surface)
        self.ennemis_visibles.draw(surface)
