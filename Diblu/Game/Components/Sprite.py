import pygame
from Game.Components.Image_item import Image_item


class Sprite(pygame.sprite.Sprite,Image_item):
    
    def __init__(self,position_map,image,screen_container):
        pygame.sprite.Sprite.__init__(self)
        Image_item.__init__(self,position_map,image,screen_container)