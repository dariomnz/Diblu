import pygame


class Text():
    
    def __init__(self,position_screen,screen_container):
        self.position_screen=position_screen
        self.screen_container=screen_container
        self.screen=screen_container.screen
        self.font=pygame.font.SysFont("Cambria", 18)
        self.text='None'
        
    def draw(self):
        rendered=self.font.render(self.text, 1, pygame.Color(255,255,255))
        self.screen.blit(rendered,self.position_screen)
        
        
    def update(self,text):
        self.text=text
        
        