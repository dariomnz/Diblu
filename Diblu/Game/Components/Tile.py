import pygame,os
from Game.constants import *
from utils import str2list
from Game.Components.Sprite import Sprite

tile_types = {
            0:[0,0,16,16],
            1:[32,0,16,16],
            2:[32,32,16,16]
            }

def tile_size(tile_type):
    return tile_types[tile_type][2:] 

class TileMap():
    
    def __init__(self,image):

        file = os.path.join('..','data','images',image)
        self.image=pygame.image.load(file).convert_alpha()
        self.original_image_size=[self.image.get_width(),self.image.get_height()]
        


class Chunk():
    
    def __init__(self,chunk_data):
        '''chunk_data is a list, in [0]:the string of position, in [1] a dict with tiles'''
        self.position=str2list(chunk_data[0])
        self.position_map=[self.position[0]*CHUNK_SIZE[0]*TILE_SIZE_GENERAL[0],self.position[1]*CHUNK_SIZE[1]*TILE_SIZE_GENERAL[1]]
        self.tiles=chunk_data[1]
        
    def draw(self):
        for tile in self.tiles.values():
            tile.draw()
            
    def camera_update(self,camera):
        for tile in self.tiles.values():
            tile.camera_update(camera)
            
    def image_update(self,camera):
        for tile in self.tiles.values():
            tile.image_update(camera)    
    
        
class Tile(Sprite):
    
    def __init__(self,position_chunk,tile_type,tilemap,screen):
        self.tile_type=tile_type
        self.tilemap=tilemap
        self.position_chunk=position_chunk
        rect_in_tilemap=pygame.Rect(tile_types[self.tile_type])
        image=self.tilemap.image.subsurface(rect_in_tilemap)
        
        position_map=[position_chunk[0]*TILE_SIZE_GENERAL[0],position_chunk[1]*TILE_SIZE_GENERAL[1]]
        super().__init__(position_map, image, screen)