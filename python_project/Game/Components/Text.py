import pygame,os
from Game.Components.Screen_container import getInstance as S_c

class Text():
    
    def __init__(self,position_screen,size=25,color=(0,0,0),color_fill=(255,255,255)):
        self.position_screen=position_screen
        self.size=size
        self.original_size=self.size
        # Para el relleno
        self.color_fill=pygame.Color(color_fill[0],color_fill[1],color_fill[2])
        self.font_type_fill=os.path.join('..','data','font','CCOverbyteOn W00 Regular.ttf')
#         self.font_type_fill=os.path.join('..','data','font','Sabo-Filled.otf')
        self.font_fill=pygame.font.Font(self.font_type_fill, self.size)
        
        # Para el borde
        self.color=pygame.Color(color[0],color[1],color[2])
        self.font_type=os.path.join('..','data','font','CCOverbyteOff W00 Regular.ttf')
#         self.font_type=os.path.join('..','data','font','Sabo-Regular.otf')
        self.font=pygame.font.Font(self.font_type, self.size)
        
        
        self.text='None'
        
    def draw(self):
        '''Dibuja el texto en la pantalla'''
        S_c().screen.blit(self.rendered_fill,[self.position_screen[0]+2,self.position_screen[1]+2])
        S_c().screen.blit(self.rendered,self.position_screen)
        
    def draw_in(self,surface):
        '''Dibuja el texto en una surface'''
        surface.blit(self.rendered_fill,[self.position_screen[0]+2,self.position_screen[1]+2]) 
        surface.blit(self.rendered,self.position_screen) 
           
    def update_text(self,text):
        '''Actualiza el texto'''
        self.text=str(text)
        self.rendered_fill=self.font_fill.render(self.text, 1, self.color_fill)
        self.rendered=self.font.render(self.text, 1, self.color)
        
    def update_size(self,size):
        '''Actualiza el tamano del texto'''
        self.size=size
        self.font_fill=pygame.font.Font(self.font_type_fill, self.size)
        self.font=pygame.font.Font(self.font_type, self.size)
        self.rendered_fill=self.font_fill.render(self.text, 1, self.color_fill)
        self.rendered=self.font.render(self.text, 1, self.color)
        
        