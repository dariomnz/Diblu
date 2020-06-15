import pygame
from utils import  str2list2, load_image
from Game.Components.Sprite import Sprite
from Game.constants import TILE_SIZE_GENERAL, CHUNK_SIZE, TILE_TYPES


class TileMap():
    '''Clase que se encarga de guardar el tilemap'''
    def __init__(self,image):
        image+='.png'
#         file = os.path.join('..','data','images',image)
#         self.image=pygame.image.load(file).convert_alpha()
        self.image=load_image(image)
        self.original_image_size=[self.image.get_width(),self.image.get_height()]
        

class Chunk():
    
    def __init__(self,chunk_data):
        '''chunk_data is a list, in [0]:the string of position, in [1] a dict with tiles'''
        self.position=str2list2(chunk_data[0])
        self.position_map=[self.position[0]*CHUNK_SIZE[0]*TILE_SIZE_GENERAL[0],self.position[1]*CHUNK_SIZE[1]*TILE_SIZE_GENERAL[1]]
        self.tiles=chunk_data[1]
        self.tile_group=list(self.tiles.values())
    
        
    def draw(self):
        '''Dibuja todas las tiles del chunk por capas'''
        #Ordenacion por capas
        self.tile_group.sort(key=lambda tile:tile.layer)
        
        for tile in self.tile_group:
            tile.draw()
            
    def camera_update(self,camera):
        '''Actualiza la posicion de todas sus tile'''
        for tile in self.tiles.values():
            tile.camera_update(camera)
            
    def image_update(self,camera):
        '''Actualiza la imagen de todas sus tile'''
        for tile in self.tiles.values():
            tile.image_update(camera)    
    
        
class Tile(Sprite):
    '''Porcion de un chunk para mostrar objetos'''
    def __init__(self,position_chunk,layer,tile_type,tilemap):
        self.tile_type=tile_type
        self.layer=layer
        self.tilemap=tilemap
        self.position_chunk=position_chunk
        rect_in_tilemap=pygame.Rect(TILE_TYPES[self.tile_type])
        image=self.tilemap.image.subsurface(rect_in_tilemap)
        #Posicion calculada con su posicion dentro de la grid de chunks por su tamaño
        position_map=[position_chunk[0]*TILE_SIZE_GENERAL[0],position_chunk[1]*TILE_SIZE_GENERAL[1]]
        super().__init__(position_map, image)