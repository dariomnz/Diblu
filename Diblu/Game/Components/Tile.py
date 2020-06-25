import pygame
from utils import  str2list2, load_image, JSONParser, getRect
from Game.Components.Sprite import Sprite
from Game.constants import TILE_SIZE_GENERAL, CHUNK_SIZE, TILE_TYPES,\
    TILEMAP1_NAME, TILE_SIZE_GENERAL_PIXEL
from Game.Components.Screen_container import getInstance as S_c
from Game.Components.Camera import getInstance as camera
# from Game.Components.Image_item import CollisionBox
# pygame.sprite.Group
class TileMap(Sprite):
    '''Clase que se encarga de guardar el tilemap'''
    def __init__(self,name):
#         image+='.png'
#         file = os.path.join('..','data','images',image)
#         self.image=pygame.image.load(file).convert_alpha()
        self.original_image=load_image(name+'.png')
        
        self.scale_image=TILE_SIZE_GENERAL_PIXEL[0]/TILE_SIZE_GENERAL[0]
#         original_image_size=[int(self.original_image.get_width()*self.scale_image),int(self.original_image.get_height()*self.scale_image)]
#         self.original_image=pygame.transform.scale(self.original_image, (original_image_size[0], original_image_size[1]))
        self.image=self.original_image.copy()
        self.original_image_size=[self.image.get_width(),self.image.get_height()]
        
        self.setUp_collisionBox(name)
#         self.collisionBox=CollisionBox(image,'TileMap')
        
        self.generate_tiles()
     
    def image_update(self):
        '''Actualiza la imagen escalada'''
        self.image=pygame.transform.scale(self.original_image, (int(self.original_image.get_width()*camera().zoom*S_c().w_factor_image), int(self.original_image.get_height()*camera().zoom*S_c().h_factor_image)))
        
        # para colisiones
#         self.collisionBox.image_tilemap_collision_box=\
#         pygame.transform.scale(self.collisionBox.original_image_tilemap_collision_box, 
#                                (int(self.collisionBox.original_image_tilemap_collision_box.get_width()*camera().zoom*S_c().w_factor_image),
#                                  int(self.collisionBox.original_image_tilemap_collision_box.get_height()*camera().zoom*S_c().h_factor_image))) 
       
        self.generate_tiles()
        
        
    def generate_tiles(self):
        self.image_tiles={}
        for tile_type in TILE_TYPES.keys():
            attr0=TILE_TYPES[tile_type][0]*camera().zoom*S_c().w_factor_image*self.scale_image
            attr1=TILE_TYPES[tile_type][1]*camera().zoom*S_c().h_factor_image*self.scale_image
            attr2=TILE_TYPES[tile_type][2]*camera().zoom*S_c().w_factor_image*self.scale_image
            attr3=TILE_TYPES[tile_type][3]*camera().zoom*S_c().h_factor_image*self.scale_image
            rect_in_tilemap=pygame.Rect(attr0,attr1,attr2,attr3)
            self.image_tiles[tile_type]=self.image.subsurface(rect_in_tilemap)
            
            # Para colisiones
#             self.collisionBox.image_collision_box[tile_type]=self.collisionBox.image_tilemap_collision_box.subsurface(rect_in_tilemap)
        
    def setUp_collisionBox(self,name):
        
        self.cB_data=JSONParser(name+'-collisionBox')
        
        #Diccionario con los tipos de colisiones, y su lista de imagenes
        self.original_image_tilemap_collision_box={}
         
        self.original_image_tilemap_collision_box['water']=[load_image(image_name) for image_name in self.cB_data['water']]
        
        self.image_tilemap_collision_box=self.original_image_tilemap_collision_box.copy()
          
        self.generate_cB_rects()
        
    def generate_cB_rects(self):             
        '''Formato de cB_rects key tile type con valor una lista de rect'''
        self.cB_rects={}
        for tile_type in TILE_TYPES.keys():
            attr0=TILE_TYPES[tile_type][0]*camera().zoom*S_c().w_factor_image*self.scale_image
            attr1=TILE_TYPES[tile_type][1]*camera().zoom*S_c().h_factor_image*self.scale_image
            attr2=TILE_TYPES[tile_type][2]*camera().zoom*S_c().w_factor_image*self.scale_image
            attr3=TILE_TYPES[tile_type][3]*camera().zoom*S_c().h_factor_image*self.scale_image
            rect_in_tilemap_image=pygame.Rect(attr0,attr1,attr2,attr3)
             
            for aux_image_tilemap_collisionBox in self.image_tilemap_collision_box['water']: 
                aux_cB_image=aux_image_tilemap_collisionBox.subsurface(rect_in_tilemap_image) 
                 
                aux_mask=pygame.mask.from_surface(aux_cB_image, 127)
                if tile_type not in self.cB_rects:
                    self.cB_rects[tile_type]=[]
                    
                aux_outline=aux_mask.outline()
                if len(aux_outline)>0:
                    self.cB_rects[tile_type].append(getRect(aux_outline))  
#                     print(self.cB_rects)  
        
        
TILEMAP1=TileMap(TILEMAP1_NAME)

class Chunk():
    
    def __init__(self,chunk_data):
        '''chunk_data is a list, in [0]:the string of position, in [1] a dict with tiles'''
        self.position=str2list2(chunk_data[0])
        self.position_map=[self.position[0]*CHUNK_SIZE[0]*TILE_SIZE_GENERAL[0],self.position[1]*CHUNK_SIZE[1]*TILE_SIZE_GENERAL[1]]
        self.tiles=chunk_data[1]
#         self.tile_group=list(self.tiles.values())
    
        
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
    
    def check_water_collisions(self,sprite):
        for tile in self.tiles.values():
            if sprite.check_collision(tile):
                return True
            
        return False
    
    def add_self_layer(self):
        '''Se anaden a su layer'''
        for tile in self.tiles.values():
            S_c().add_to_self_layer(tile) 
    
    def del_layer(self):
        '''Elimina de las layers el chunk'''
        for tile in self.tiles.values():
            tile.del_layer()    
        
class Tile(Sprite):
    '''Porcion de un chunk para mostrar objetos'''
    def __init__(self,position_chunk,layer,tile_type,tilemap):
        self.tile_type=tile_type
        self.tilemap=tilemap
        
#         self.collisionBox=CollisionBox(tile_type,'Tile')
        
        self.position_chunk=position_chunk
        image=self.tilemap.image_tiles[self.tile_type]
        #Posicion calculada con su posicion dentro de la grid de chunks por su tama�o
        position_map=[position_chunk[0]*TILE_SIZE_GENERAL[0],position_chunk[1]*TILE_SIZE_GENERAL[1]]
        super().__init__(position_map, image,layer)
        
        self.setUp_collisionBox()
        
    def image_update(self):
        '''Actualiza la imagen escalada, cogiendola del tilemap ya escalado'''
        self.image=self.tilemap.image_tiles[self.tile_type]
        #Para colisiones
#         self.collisionBox.image=self.tilemap.collisionBox.image_collision_box[self.tile_type]

    def setUp_collisionBox(self): 
        
        self.cB_rect=[]
        self.cB_rect_map=[]
        for rect in self.tilemap.cB_rects[self.tile_type]:
            self.cB_rect.append(rect.copy())
            self.cB_rect_map.append(rect.copy())
            
#         self.cB_rect=self.tilemap.cB_rects[self.tile_type].copy()
#         self.cB_rect_map=self.cB_rect.copy()
#         print(self.tilemap.cB_rects)
        self.update_collision()
#         print(self.tilemap.cB_rects)

        
        
        
        
        