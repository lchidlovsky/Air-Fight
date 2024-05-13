import pygame

class MixerAudio:
    
    def suivant():
        son_suivant = pygame.mixer.Sound("sons/suivant.mp3")
        son_suivant.play()
        
    def ok():
        son_ok = pygame.mixer.Sound("sons/ok.mp3")
        son_ok.play()
        
    def entree():
        son_entree = pygame.mixer.Sound("sons/entree.mp3")
        son_entree.play()
