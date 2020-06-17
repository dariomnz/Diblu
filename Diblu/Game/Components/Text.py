import pygame
from Game.Components.Screen_container import getInstance as S_c

class Text():
    
    def __init__(self,position_screen):
        self.position_screen=position_screen
        self.font=pygame.font.SysFont("Comic Sans MS", 18)
        self.text='None'
        
    def draw(self):
        '''Dibuja el texto en la pantalla'''
        rendered=self.font.render(self.text, 1, pygame.Color(255,255,255))
        S_c().screen.blit(rendered,self.position_screen)
        
        
    def update_text(self,text):
        '''Actualiza el texto'''
        self.text=text
        
        