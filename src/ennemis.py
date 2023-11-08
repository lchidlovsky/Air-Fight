import pygame
from constantes import *
from projectile import Projectile
from random import randint, choice

class Ennemi(pygame.sprite.Sprite):
    """classe représentant un ennemi quelconque
    """
    def __init__(self, apparences, coord, nb_vie, vitesse):
        pygame.sprite.Sprite.__init__(self)
        self.apparences = apparences
        self.num_apparence = 0
        self.horloge_apparence = 0
        
        self.vie = nb_vie
        self.image = apparences[0]
        self.rect = self.image.get_rect()
        self.rect.midbottom = coord
        
        self.vitesse = vitesse
        self.est_touche = False
        self.vivant = True
        self.existant = True
    
    def bas(self, vitesse):
        self.rect.top += vitesse
        
    def touche(self, degat):
        if not self.est_touche:
            self.est_touche = True
            self.vie -= degat
            self.horloge_apparence = 0
            if self.vie < 1:
                self.vie = 0
                self.vivant = False
                self.num_apparence = 1
                self.image = self.apparences[1]
            
    
    def update(self):
        if self.vivant:
            self.bas(self.vitesse)
            
            if self.est_touche:
                if self.horloge_apparence % 10 < 5:
                    self.num_apparence = 0
                    self.image = self.apparences[0]
                else:
                    self.num_apparence = 1
                    self.image = self.apparences[1]
                if self.horloge_apparence > 100:
                    self.animation = 1
                    self.horloge_apparence = 0
                    self.est_touche = False
                    
                self.horloge_apparence += 1
                        
        else:
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
        for i in range(1,6):
            apparences.append(pygame.image.load(f"images/ennemis/petit_{i}.png").convert_alpha())
        
        super().__init__(apparences, coord, vie_petit, vitesse_petit)


class Moyen(Ennemi):
    """classe représentant un ennemi de taille moyenne
    """
    def __init__(self, coord):
        
        apparences = []
        for i in range(1,7):
            apparences.append(pygame.image.load(f"images/ennemis/moyen_{i}.png").convert_alpha())
        
        super().__init__(apparences, coord, vie_moyen, vitesse_moyen)
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
        for i in range(1,11):
            apparences.append(pygame.image.load(f"images/ennemis/gros_{i}.png").convert_alpha())

        super().__init__(apparences, coord, vie_gros, vitesse_gros)
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
        
        #gestion de la cadence de tir
        if self.cooldown > 0:
            self.cooldown += 1
            if self.cooldown > self.cadence_tirs:
                self.cooldown = 0

        #animation de destruction du vaisseau
        if not self.vivant:
            if self.num_apparence < 4:
                self.num_apparence = 3
                self.image = self.apparences[3]
            if self.horloge_apparence % 8 == 0:
                if self.num_apparence < len(self.apparences)-1:
                    self.num_apparence += 1
                    self.image = self.apparences[self.num_apparence]
                else:
                    self.existant = False

            self.horloge_apparence += 1
            
        else:
            self.bas(self.vitesse)
            #gestion du déplacement latéral
            if self.dep_gauche:
                self.rect.left -= self.vitesse_laterale
            else:
                self.rect.left += self.vitesse_laterale
            
            if not self.preparation and not self.tir and not randint(0, 400):
                self.preparation = True
                
                
            if self.est_touche:
                self.preparation = False
                if self.horloge_apparence % 10 < 5:
                    self.num_apparence = 0
                    self.image = self.apparences[0]
                else:
                    self.num_apparence = 1
                    self.image = self.apparences[1]
                if self.horloge_apparence > 100:
                    self.animation = 1
                    self.horloge_apparence = 0
                    self.est_touche = False
                    
                self.horloge_apparence += 1
                
            #gestion de l'apparence durant la préparation
            elif self.preparation:
                self.horloge_attaque += 1
                if self.horloge_attaque % 10 < 5:
                    self.num_apparence = 3
                    self.image = self.apparences[3]
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
    def __init__(self, nom, coord_min, coord_max, joueur, nb_simultanes, nb_petits, nb_moyens, nb_gros):
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
                
            ennemi_aleatoire.rect.midbottom = (x, randint(self.hauteur_min-111, self.hauteur_min))
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
                self.placement()
                        
        
    def draw(self, surface):
        self.tirs_ennemis.draw(surface)
        self.ennemis_visibles.draw(surface)
        self.bonus.draw(surface)
