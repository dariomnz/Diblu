import pygame
from Game.constants import TILE_SIZE_GENERAL_PIXEL, TILE_SIZE_GENERAL
from utils import load_image, list2str2
from Game.Components import Screen_container as S_c


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
        
        original_image_size=[int(self.original_image.get_width()*self.scale_image),int(self.original_image.get_height()*self.scale_image)]
        self.original_image=pygame.transform.scale(self.original_image, (original_image_size[0], original_image_size[1]))
        self.image=self.original_image.copy()
        
        self.position_map=position_map
        self.position_map[0]*=self.scale_image
        self.position_map[1]*=self.scale_image
        self.position_camera=position_map.copy()
        #rect para dibujar la imagen
        self.rect=[self.position_camera[0],self.position_camera[1],original_image_size[0],original_image_size[1]]
        
        self._add_layer(layer)
        
    def draw(self):
        '''Pinta la imagen en su posicion respecto la camara'''
        S_c.getInstance().screen.blit(self.image,self.position_camera)
        
    def update(self):
        '''Actualiza'''
        pass
    
    def camera_update(self,camera):
        '''Actualiza su posicion respecto a la camara'''
        self.rect=[self.position_camera[0],self.position_camera[1],self.original_image.get_width(),self.original_image.get_height()]
        self.position_camera[0]=((self.position_map[0]-camera.position_map[0])*camera.zoom*S_c.getInstance().w_factor_image)+camera.position_screen[0]
        self.position_camera[1]=((self.position_map[1]-camera.position_map[1])*camera.zoom*S_c.getInstance().h_factor_image)+camera.position_screen[1]
        
    def image_update(self,camera):
        '''Actualiza la imagen escalada'''
        self.image=pygame.transform.scale(self.original_image, (int(self.original_image.get_width()*camera.zoom*S_c.getInstance().w_factor_image), int(self.original_image.get_height()*camera.zoom*S_c.getInstance().h_factor_image)))
        
    def get_image_size(self):
        '''Devuelve el tamano de la imagen actual'''
        return [self.image.get_width(),self.image.get_height()]
    
    def change_layer(self,new_layer):
        '''Cambia el objeto a la nueva layer especificada'''
        for key_layer in S_c.getInstance().layers.keys():
            if self in S_c.getInstance().layers[key_layer].values():
                position_key=list2str2(self.position_map)
                S_c.getInstance().layers[key_layer].pop(position_key)
                self._add_layer(new_layer)
                return
    
        
    def _add_layer(self,layer):
        '''Anade el objeto a la layer especificada, si ya esta ocupada la posicion, lo anade a una layer mas'''
        notinsert=True
        while(notinsert):
            position_key=list2str2(self.position_map)
            if layer in S_c.getInstance().layers:
                if position_key not in  S_c.getInstance().layers[layer]:
                    S_c.getInstance().layers[layer][position_key]=self
                    self.layer=layer
                    notinsert=False
                else:
                    layer+=1
            else:
                S_c.getInstance().layers[layer]={}
                S_c.getInstance().layers[layer][position_key]=self
                self.layer=layer
                notinsert=False
            
    def del_layer(self):
        '''Elimina el objeto de la layer en la que este'''
        for key_layer in S_c.getInstance().layers.keys():
            if self in S_c.getInstance().layers[key_layer].values():
                position_key=list2str2(self.position_map)
                S_c.getInstance().layers[key_layer].pop(position_key)
                if len(S_c.getInstance().layers[key_layer].keys())==0:
                    S_c.getInstance().layers.pop(key_layer)
                    continue
                return       
            
            
            
            
            
            
            