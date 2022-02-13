import pygame
from Game.constants import DEFAULT_SCALE
from utils import load_image
from Game.Components.Screen_container import getInstance as S_c
from Game.Components.Camera import getInstance as camera


class Image_item():
    '''Super clase de objetos con imagen'''
    def __init__(self,position_map,image,layer=None):
        if not hasattr(self, 'scale_image'):
            self.scale_image=DEFAULT_SCALE
        #Si es una imagen ya no la carga
        if isinstance(image, str):
            image+='.png'
            self.original_image=load_image(image)
        else:
            self.original_image=image
        
        self.image=self.original_image.copy()
        
        self.position_map=pygame.rect.Rect(position_map,[self.original_image.get_width(),self.original_image.get_height()])
#         self.position_map[0]*=self.scale_image
#         self.position_map[1]*=self.scale_image
#         self.position_map[0]-=self.position_map.centerx
#         self.position_map[1]-=self.position_map.centery
        self.position_camera=self.position_map.copy()
        
        if layer==None:
            self.layer=self.position_map.bottom
        else:
            self.layer=self.position_map.bottom-1000
        
#         S_c().add_to_self_layer(self)
        
    def draw(self):
        '''Pinta la imagen en su posicion respecto la camara'''
        
        S_c().screen.blit(self.image,self.position_camera)
        
        # Para ver colisiones        
#         for i in range(len(self.cB_rect_map)):
#             aux_rect=list(self.cB_rect_map.values())[i].copy()
#             aux_pos=[0,0]
#             aux_pos[0]=((aux_rect[0]-camera().position_map[0])*camera().zoom*S_c().w_factor_image)+camera().position_screen[0]
#             aux_pos[1]=((aux_rect[1]-camera().position_map[1])*camera().zoom*S_c().h_factor_image)+camera().position_screen[1]
#               
#             aux_surf=pygame.Surface(aux_rect.size,pygame.SRCALPHA)
#             aux_surf.fill((0,0,0,100))
#             S_c().screen.blit(aux_surf,aux_pos)
        
    def update(self):
        '''Actualiza'''
        pass
        
        
    
    def camera_update(self):
        '''Actualiza su posicion respecto a la camara'''

        self.position_camera[0]=((self.position_map[0]-camera().position_map[0])*camera().zoom*S_c().w_factor_image)+camera().position_screen[0]
        self.position_camera[1]=((self.position_map[1]-camera().position_map[1])*camera().zoom*S_c().h_factor_image)+camera().position_screen[1]

        
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

