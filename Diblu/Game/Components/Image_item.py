import pygame
from Game.constants import TILE_SIZE_GENERAL_PIXEL, TILE_SIZE_GENERAL
from utils import load_image
from Game.Components.Screen_container import getInstance as S_c
from Game.Components.Camera import getInstance as camera


class Image_item():
    '''Super clase de objetos con imagen'''
    def __init__(self,position_map,image,layer):
        self.scale_image=TILE_SIZE_GENERAL_PIXEL[0]/TILE_SIZE_GENERAL[0]
        #Si es una imagen ya no la carga
        if isinstance(image, str):
            image+='.png'
            self.original_image=load_image(image)
        else:
            self.original_image=image
        
        self.image=self.original_image.copy()
        
        self.position_map=pygame.rect.Rect(position_map,[self.original_image.get_width(),self.original_image.get_height()])
        self.position_map[0]*=self.scale_image
        self.position_map[1]*=self.scale_image
#         self.position_map[0]-=self.position_map.centerx
#         self.position_map[1]-=self.position_map.centery
        self.position_camera=self.position_map.copy()
#         print(self.position_camera)
        #rect para dibujar la imagen
#         self.rect=[self.position_camera[0],self.position_camera[1],self.original_image.get_width(),self.original_image.get_height()]
        
        self.layer=layer
        
        S_c().add_to_self_layer(self)
        
    def draw(self):
        '''Pinta la imagen en su posicion respecto la camara'''
        
        S_c().screen.blit(self.image,self.position_camera)
        
        # Para ver colisiones
#         if len(self.cB_rect_map)>0:
#             pygame.draw.rect(S_c().screen, (0,0,0), self.cB_rect_map[0])
        
    def update(self):
        '''Actualiza'''
        pass
    
    def camera_update(self):
        '''Actualiza su posicion respecto a la camara'''
#         self.rect=pygame.rect.Rect([self.position_camera[0],self.position_camera[1],self.original_image.get_width(),self.original_image.get_height()])
#         self.collisionBox.rect=self.rect.copy()
#         print(self.collisionBox.rect)
        self.position_camera[0]=((self.position_map[0]-camera().position_map[0])*camera().zoom*S_c().w_factor_image)+camera().position_screen[0]
        self.position_camera[1]=((self.position_map[1]-camera().position_map[1])*camera().zoom*S_c().h_factor_image)+camera().position_screen[1]
#         aux_position_camera=center2pos(self.position_camera,self.position_camera.size)
#         self.position_camera[0]=aux_position_camera[0]
#         self.position_camera[1]=aux_position_camera[1]
        
    def image_update(self):
        '''Actualiza la imagen escalada'''
        self.image=pygame.transform.scale(self.original_image, (int(self.original_image.get_width()*camera().zoom*S_c().w_factor_image), int(self.original_image.get_height()*camera().zoom*S_c().h_factor_image)))
        
    def get_image_size(self):
        '''Devuelve el tamano de la imagen actual'''
        return [self.image.get_width(),self.image.get_height()]
    
    def add_layer_below(self,image_item):
        '''Cambia la layer a una debajo de image_item'''
        self.layer=image_item.layer-0.1

    def add_layer_above(self,image_item):
        '''Cambia la layer a una encima de image_item'''
        self.layer=image_item.layer+0.1





    
#     def show_collisionBox(self):
#         pygame.draw.rect(self.image, (0,0,0), self.collisionBox.image.get_rect(), 1) 
             
# class CollisionBox(pygame.sprite.Sprite):
#     
#     def __init__(self,name,name_instance):
#         self.rect=[0,0,0,0]
#         
#         
#         if  name_instance=='AnimateSprite':
#             self.setUp_AnimateSprite(name)
#         elif name_instance=='Tile':       
#             self.setUp_Tile(name)
#         elif name_instance=='TileMap': 
#             self.setUp_TileMap(name)     
#         elif name_instance=='Sprite': 
#             self.setUp_Sprite(name)       
#                
#     def setUp_AnimateSprite(self,name): 
#         
#         self.original_image_sprite_sheet_collision_box=load_image(name+'-collisionBox.png')
#         
#         
#         self.scale_image=TILE_SIZE_GENERAL_PIXEL[0]/TILE_SIZE_GENERAL[0]
#         self.original_image_sprite_sheet_collision_box=pygame.transform.scale(self.original_image_sprite_sheet_collision_box, (int(self.original_image_sprite_sheet_collision_box.get_width()*self.scale_image), int(self.original_image_sprite_sheet_collision_box.get_height()*self.scale_image)))
#         
#         self.image_sprite_sheet_collision_box=self.original_image_sprite_sheet_collision_box.copy()
#         
#         self.image_collision_box={}
#         
#         self.image=self.image_sprite_sheet_collision_box
#         
#     def update_AnimateSprite(self):
#         pass
#     
#     def setUp_TileMap(self,name):
#         
#         self.original_image_tilemap_collision_box=load_image(name+'-collisionBox.png')
#         
#         self.scale_image=TILE_SIZE_GENERAL_PIXEL[0]/TILE_SIZE_GENERAL[0]
#         self.original_image_tilemap_collision_box=pygame.transform.scale(self.original_image_tilemap_collision_box, (int(self.original_image_tilemap_collision_box.get_width()*self.scale_image), int(self.original_image_tilemap_collision_box.get_height()*self.scale_image)))
#         self.image_tilemap_collision_box=self.original_image_tilemap_collision_box.copy()
#         
#         self.image_collision_box={}
#         
#         self.image=self.image_tilemap_collision_box
#         
#     def setUp_Sprite(self,name):
#         pass
#         
#     
#     def setUp_Tile(self,name):         
#         self.image=0
# #             
# #     def update_rect(self):
# #         self.rect=pygame.ge       
            