import pygame
from Game.Components.Screen_container import getInstance as S_c

class Text():
    
    def __init__(self,position_screen,size=18):
        self.position_screen=position_screen
        self.size=size
        self.original_size=self.size
        self.font=pygame.font.SysFont("Comic Sans MS", self.size)
        self.text='None'
        
    def draw(self):
        '''Dibuja el texto en la pantalla'''
        rendered=self.font.render(self.text, 1, pygame.Color(255,255,255))
        S_c().screen.blit(rendered,self.position_screen)
        
    def draw_in(self,surface):
        '''Dibuja el texto en una surface'''
        rendered=self.font.render(self.text, 1, pygame.Color(255,255,255))
        surface.blit(rendered,self.position_screen) 
           
    def update_text(self,text):
        '''Actualiza el texto'''
        self.text=str(text)
        
    def update_size(self,size):
        '''Actualiza el tamano del texto'''
        self.size=size
        self.font=pygame.font.SysFont("Comic Sans MS", self.size)
        
        