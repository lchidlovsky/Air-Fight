import pygame
from constantes import vie_joueur, vitesse_joueur, vitesse_projectile_joueur, chargeur_joueur
from Projectile import Projectile

class Joueur(pygame.sprite.Sprite):
    """classe représentant le vaisseau du joueur
    """
    def __init__(self, coord, coord_min, coord_max):
        pygame.sprite.Sprite.__init__(self)
        self.apparences = []
        for i in range(1,8):
            self.apparences.append(pygame.image.load(f"images/joueur/joueur_{i}.png").convert_alpha())
        
        self.vie = vie_joueur
        self.num_apparence = 0
        self.horloge_apparence = 0
        self.animation = 1
        self.image = self.apparences[0]
        self.rect = self.image.get_rect()
        self.rect.center = coord
        
        self.largeur_min = coord_min[0]
        self.hauteur_min = coord_min[1]
        self.largeur_max = coord_max[0]
        self.hauteur_max = coord_max[1]
        
        self.image_projectile = pygame.image.load("images/autres/projectile_1.png").convert_alpha()
        self.projectiles = pygame.sprite.Group()
        self.chargeur = chargeur_joueur
        self.puissance_de_feu = 1
        self.cadence_tirs = 15
        self.cooldown = 0
        
        self.vitesse = vitesse_joueur
        self.explosifs = 0
        self.boucliers = 0
        self.duplications = 0
    
    def est_mort(self):
        return self.vie < 1
    
    def disparu(self):
        return self.num_apparence == 6 and self.horloge_apparence % 16 == 0

    def haut(self):
        if self.animation != 4 and self.rect.top - self.vitesse >= self.hauteur_min:
            self.rect.top -= self.vitesse
        
    def bas(self):
        if self.animation != 4 and self.rect.bottom <= self.hauteur_max:
            self.rect.top += self.vitesse
        
    def gauche(self):
        if self.animation != 4 and self.rect.left - self.vitesse >= self.largeur_min:
            self.rect.left -= self.vitesse
        
    def droite(self):
        if self.animation != 4 and self.rect.right <= self.largeur_max:
            self.rect.left += self.vitesse
            
    def amelioration_puissance_feu(self):
        if self.puissance_de_feu < 4:
            self.puissance_de_feu += 1
            
    def amelioration_vitesse(self):
        self.vitesse += 1
    
    def explosion(self):
        if self.explosifs and self.animation == 1 and self.vie > 0:
            self.explosifs -= 1
            return True
        return False
    
    def bouclier(self):
        if self.boucliers and self.animation == 1 and self.vie > 0:
            self.boucliers -= 1
            self.animation = 3
            self.horloge_apparence = 0

    def touche(self, degat):
        if self.animation == 1:
            self.vie -= degat
            self.horloge_apparence = 0
            
            if self.vie < 1 and self.animation != 4:
                self.vie = 0
                self.animation = 4
                self.num_apparence = 3
                self.image = self.apparences[3]
            else:
                self.animation = 2

    def tirer(self):
        if self.cooldown == 0 and self.animation == 1 and self.chargeur > 0:
            self.cooldown += 1
            self.chargeur -= 1
            
            match self.puissance_de_feu:
                case 1:
                    self.projectiles.add(Projectile(self.image_projectile, (self.rect.left +50, self.rect.top +5), vitesse_projectile_joueur, 0))

                case 2:
                    self.projectiles.add(Projectile(self.image_projectile, (self.rect.left +35, self.rect.top +20), vitesse_projectile_joueur, 0))
                    self.projectiles.add(Projectile(self.image_projectile, (self.rect.left +65, self.rect.top +20), vitesse_projectile_joueur, 0))

                case 3:
                    self.projectiles.add(Projectile(self.image_projectile, (self.rect.left +16, self.rect.top +44), vitesse_projectile_joueur, 0))
                    self.projectiles.add(Projectile(self.image_projectile, (self.rect.left +50, self.rect.top +5), vitesse_projectile_joueur, 0))
                    self.projectiles.add(Projectile(self.image_projectile, (self.rect.left +80, self.rect.top +44), vitesse_projectile_joueur, 0))
                    
                case 4:
                    self.projectiles.add(Projectile(self.image_projectile, (self.rect.left +16, self.rect.top +44), vitesse_projectile_joueur, 0))
                    self.projectiles.add(Projectile(self.image_projectile, (self.rect.left +40, self.rect.top +20), vitesse_projectile_joueur, 0))
                    self.projectiles.add(Projectile(self.image_projectile, (self.rect.left +60, self.rect.top +20), vitesse_projectile_joueur, 0))
                    self.projectiles.add(Projectile(self.image_projectile, (self.rect.left +80, self.rect.top +44), vitesse_projectile_joueur, 0))

    def update(self):
        #animation des projectiles tirés
        self.projectiles.update()
        for p in self.projectiles:
            if p.rect.bottom < self.hauteur_min:
                self.projectiles.remove(p)
        
        if self.cooldown > 0:       #gestion de la cadence de tir
            self.cooldown += 1
            if self.cooldown > self.cadence_tirs:
                self.cooldown = 0

        match self.animation:
            case 1:     #passif
                self.horloge_apparence += 1
                
                if self.horloge_apparence % 40 < 20:
                    self.num_apparence = 0
                    self.image = self.apparences[0]
                else:
                    self.num_apparence = 2
                    self.image = self.apparences[2]
            
            case 2:     #touché
                self.horloge_apparence += 1
                
                if self.horloge_apparence % 10 < 5:
                    self.num_apparence = 0
                    self.image = self.apparences[0]
                else:
                    self.num_apparence = 1
                    self.image = self.apparences[1]
                if self.horloge_apparence > 100:
                    self.animation = 1
                    self.horloge_apparence = 0

            case 3:     #bouclier
                self.horloge_apparence += 1
                
                if self.horloge_apparence % 7 < 3:
                    self.num_apparence = 0
                    self.image = self.apparences[0]
                else:
                    self.num_apparence = 1
                    self.image = self.apparences[1]
                if self.horloge_apparence > 360:
                    self.animation = 1
                    self.horloge_apparence = 0
            
            case 4:     #destruction
                self.horloge_apparence += 1
                
                if self.horloge_apparence % 16 == 0 and self.num_apparence < len(self.apparences)-1:
                    self.num_apparence += 1
                    self.image = self.apparences[self.num_apparence]
                    self.horloge_apparence = 1
    
    def draw(self, surface):
        surface.blit(self.apparences[self.num_apparence], self.rect.topleft)

        self.projectiles.draw(surface)
        
        if self.animation == 3:     #cercle du bouclier
            cote = max(self.rect.width, self.rect.height) * 1.1
            carre = pygame.Rect(self.rect.centerx - cote//2, self.rect.centery - cote//2, cote, cote)
            pi_sur_deux = 1.57079632
            degree_a_radian = 0.01745329
            deux_pi = 6.28318531
            pygame.draw.arc(surface, 'BLACK', carre, pi_sur_deux + self.horloge_apparence * degree_a_radian % deux_pi, pi_sur_deux)
