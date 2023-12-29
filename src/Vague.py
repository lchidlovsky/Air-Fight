import pygame
from constantes import *
from Bonus import Bonus
from ennemis import *
from Projectile import Projectile
from random import randint, choice

class Vague:
    """classe représentant une vague d'entités volantes
    """
    def __init__(self, nom, coord_min, coord_max, joueur, nb_simultanes,
                 nb_petits, nb_moyens, nb_gros,
                 nb_coeurs, nb_munitions, nb_explosifs, nb_vitesses, nb_feux):
        self.nom = nom
        self.finie = False
        self.largeur_min = coord_min[0]
        self.hauteur_min = coord_min[1]
        self.largeur_max = coord_max[0]
        self.hauteur_max = coord_max[1]
        self.joueur = joueur
        
        self.nb_simultanes = nb_simultanes  #nm max d'ennemis en même temps à l'écran
        self.nb_visibles = 0
        self.coordonnees = []
        self.ennemis = pygame.sprite.Group()
        self.ennemis_visibles = pygame.sprite.Group()
        self.tirs_ennemis = pygame.sprite.Group()
        
        self.bonus = pygame.sprite.Group()
        self.bonus_visibles = pygame.sprite.Group()
        
        for p in range(nb_petits):
            self.ennemis.add(Petit())
            
        for m in range(nb_moyens):
            self.ennemis.add(Moyen())
        
        for g in range(nb_gros):
            self.ennemis.add(Gros())
            
        for c in range(nb_coeurs):
            self.bonus.add(Bonus(type='coeur'))
        
        for m in range(nb_munitions):
            self.bonus.add(Bonus(type='munitions'))
            
        for e in range(nb_explosifs):
            self.bonus.add(Bonus(type='explosif'))
            
        for v in range(nb_vitesses):
            self.bonus.add(Bonus(type='vitesse'))
            
        for f in range(nb_feux):
            self.bonus.add(Bonus(type='feu'))
            
        for i in range(self.nb_simultanes):
            self.placement_ennemi()
            
    def coordonnees_pop(self):
        if self.coordonnees :
            self.coordonnees.pop(0)

    def placement_bonus(self):
        """méthode de placement aléatoire de bonus à l'écran
        """
        bonus_aleatoire = choice(self.bonus.sprites())
        self.bonus.remove(bonus_aleatoire)
        
        if len(self.coordonnees) >= self.nb_simultanes : self.coordonnees_pop()
        for _ in range(100):
            x = randint(50, self.largeur_max-50)
            if x // 60 * 60 not in self.coordonnees:
                break
        self.coordonnees.append(x // 60 * 60)
        
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
            
            if len(self.coordonnees) >= self.nb_simultanes : self.coordonnees_pop()
            for _ in range(100):
                x = randint(50, self.largeur_max-50)
                while x // 60 * 60 in self.coordonnees:
                    break
            self.coordonnees.append(x // 60 * 60)
                
            ennemi_aleatoire.rect.midbottom = (x, randint(self.hauteur_min-333, self.hauteur_min))
            if isinstance(ennemi_aleatoire, Gros):
                ennemi_aleatoire.dep_gauche = x > self.largeur_max // 2
            self.ennemis_visibles.add(ennemi_aleatoire)
    
           
    def update(self):
        self.tirs_ennemis.update()
        self.ennemis_visibles.update()
        self.bonus_visibles.update()
        
        if self.joueur.explosion:
            for e in self.ennemis_visibles:
                e.touche(e.vie)
        self.joueur.explosion = False
        
        if not self.ennemis and not self.ennemis_visibles and not self.bonus_visibles:
            self.finie = True
        
        for b in self.bonus_visibles:
            
            #replacement des bonus arrivés en bas
            if b.rect.top > self.hauteur_max:
                self.bonus_visibles.remove(b)
                self.bonus.add(b)
            
            #récupération du bonus par le joueur
            if b.rect.colliderect(self.joueur) and self.joueur.animation != 3:
                self.bonus_visibles.remove(b)
                self.coordonnees_pop()
                match b.type:
                    case 'coeur':
                        self.joueur.vie +=2
                        self.joueur.animation = 1
                    case 'munitions':
                        self.joueur.chargeur += 10
                    case 'explosif':
                        self.joueur.explosifs += 1
                    case 'vitesse':
                        self.joueur.amelioration_vitesse()
                    case 'feu':
                        self.joueur.amelioration_puissance_feu()
                    case 'duplication':
                        self.joueur.duplications += 1
        
        
        for e in self.ennemis_visibles:

            #replacement des ennemis arrivés en bas
            if e.rect.top > self.hauteur_max or e.rect.left > self.largeur_max or e.rect.right < self.largeur_min:
                self.ennemis_visibles.remove(e)
                self.nb_visibles -= 1
                self.ennemis.add(e)
                self.placement_ennemi()
                self.coordonnees_pop()
            
            #ajout des tirs ennemis
            if not isinstance(e, Petit):
                tir = e.tirer()
                if tir:
                    self.tirs_ennemis.add(tir)
            
            #suppression des ennemis en contact avec le joueur
            if e.vivant and not e.est_touche and self.joueur.animation == 1 and e.rect.colliderect(self.joueur):
                self.joueur.touche(e.vie)
                e.touche(e.vie)
                self.coordonnees_pop()
                
            #impact des ennemis touchés
            for p in self.joueur.projectiles:
                if e.vivant and p.rect.colliderect(e):
                    self.joueur.projectiles.remove(p)
                    e.touche(1)
            
            #suppression des nuages de fumée
            if not e.existant:
                self.ennemis_visibles.remove(e)
                self.nb_visibles -= 1
                self.placement_ennemi()
                self.coordonnees_pop()
        
        for p in self.tirs_ennemis:
            if p.rect.colliderect(self.joueur) and self.joueur.animation ==1:
                self.joueur.touche(1)
                self.tirs_ennemis.remove(p)
        
        
    def draw(self, surface):
        self.bonus_visibles.draw(surface)
        self.tirs_ennemis.draw(surface)
        self.ennemis_visibles.draw(surface)
