import pygame
from utils import  str2list2, load_image
from Game.Components.Sprite import Sprite
from Game.constants import TILE_SIZE_GENERAL, CHUNK_SIZE, TILE_TYPES,\
    TILEMAP1_NAME, TILE_SIZE_GENERAL_PIXEL
from Game.Components import Screen_container as S_c
from Game.Components.Camera import getInstance as camera

class TileMap():
    '''Clase que se encarga de guardar el tilemap'''
    def __init__(self,image):
        image+='.png'
#         file = os.path.join('..','data','images',image)
#         self.image=pygame.image.load(file).convert_alpha()
        self.original_image=load_image(image)
        
        self.scale_image=TILE_SIZE_GENERAL_PIXEL[0]/TILE_SIZE_GENERAL[0]
        original_image_size=[int(self.original_image.get_width()*self.scale_image),int(self.original_image.get_height()*self.scale_image)]
        self.original_image=pygame.transform.scale(self.original_image, (original_image_size[0], original_image_size[1]))
        self.image=self.original_image.copy()
        self.original_image_size=[self.image.get_width(),self.image.get_height()]
        self.generate_tiles()
     
    def image_update(self):
        '''Actualiza la imagen escalada'''
        self.image=pygame.transform.scale(self.original_image, (int(self.original_image.get_width()*camera().zoom*S_c.getInstance().w_factor_image), int(self.original_image.get_height()*camera().zoom*S_c.getInstance().h_factor_image)))
        self.generate_tiles()
        
        
    def generate_tiles(self):
        self.image_tiles={}
        for tile_type in TILE_TYPES.keys():
            attr0=TILE_TYPES[tile_type][0]*camera().zoom*S_c.getInstance().w_factor_image*self.scale_image
            attr1=TILE_TYPES[tile_type][1]*camera().zoom*S_c.getInstance().h_factor_image*self.scale_image
            attr2=TILE_TYPES[tile_type][2]*camera().zoom*S_c.getInstance().w_factor_image*self.scale_image
            attr3=TILE_TYPES[tile_type][3]*camera().zoom*S_c.getInstance().h_factor_image*self.scale_image
            rect_in_tilemap=pygame.Rect(attr0,attr1,attr2,attr3)
            self.image_tiles[tile_type]=self.image.subsurface(rect_in_tilemap)
        
        
        
        
TILEMAP1=TileMap(TILEMAP1_NAME)

class Chunk():
    
    def __init__(self,chunk_data):
        '''chunk_data is a list, in [0]:the string of position, in [1] a dict with tiles'''
        self.position=str2list2(chunk_data[0])
        self.position_map=[self.position[0]*CHUNK_SIZE[0]*TILE_SIZE_GENERAL[0],self.position[1]*CHUNK_SIZE[1]*TILE_SIZE_GENERAL[1]]
        self.tiles=chunk_data[1]
        self.tile_group=list(self.tiles.values())
    
        
#     def draw(self):
#         '''Dibuja todas las tiles del chunk por capas'''
#         #Ordenacion por capas
#         self.tile_group.sort(key=lambda tile:tile.layer)
#          
#         for tile in self.tile_group:
#             tile.draw()
            
    def camera_update(self):
        '''Actualiza la posicion de todas sus tile'''
        for tile in self.tiles.values():
            tile.camera_update()
            
    def image_update(self):
        '''Actualiza la imagen de todas sus tile'''
        for tile in self.tiles.values():
            tile.image_update()    
    
    def add_self_layer(self):
        '''Se anaden a su layer'''
        for tile in self.tiles.values():
            S_c.getInstance().add_to_self_layer(tile) 
    
    def del_layer(self):
        '''Elimina de las layers el chunk'''
        for tile in self.tiles.values():
            tile.del_layer()    
        
class Tile(Sprite):
    '''Porcion de un chunk para mostrar objetos'''
    def __init__(self,position_chunk,layer,tile_type,tilemap):
        self.tile_type=tile_type
        self.tilemap=tilemap
        self.position_chunk=position_chunk
        image=self.tilemap.image_tiles[self.tile_type]
        #Posicion calculada con su posicion dentro de la grid de chunks por su tamaño
        position_map=[position_chunk[0]*TILE_SIZE_GENERAL[0],position_chunk[1]*TILE_SIZE_GENERAL[1]]
        super().__init__(position_map, image,layer)
        
    def image_update(self):
        '''Actualiza la imagen escalada, cogiendola del tilemap ya escalado'''
        self.image=self.tilemap.image_tiles[self.tile_type]
        
        
        
        
        
        
        
        