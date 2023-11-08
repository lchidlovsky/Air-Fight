import pygame

class gameBar(pygame.Surface):
    
    def __init__(self, size):
        pygame.Surface.__init__(self, size)
        self.fill("BLACK")
       
        self.font = pygame.font.Font(pygame.font.match_font('comicsans'), 20)
        self.coeur = pygame.image.load("images/autres/coeur.png").convert_alpha()
        self.demi = pygame.image.load("images/autres/demi_coeur.png").convert_alpha()
        
    def draw(self, surface, vie):
        surface.blit(self, (0, 0))
        
        for i in range (vie // 2):
            surface.blit(self.coeur, (i*self.coeur.get_width(), 0))
        
        
        #si le nombre de vies est impair
        if vie % 2:
            surface.blit(self.demi, ((vie // 2)*self.coeur.get_width(), 0))
