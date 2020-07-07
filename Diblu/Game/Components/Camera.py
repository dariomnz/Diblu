from utils import pos2center, list2str2
from Game.constants import CHUNK_SIZE,TILE_SIZE_GENERAL_PIXEL
from Game.Components.Screen_container import getInstance as S_c
import logging
import pygame

def getInstance():
    return _instance

def createInstance():
    Camera()

class Camera():
    
    def __init__(self):
        self.float_position_map=[0,0]
        self.position_map=pygame.rect.Rect([0,0,0,0])
        
        self.position_screen=pos2center([0,0],S_c().get_screen_size())
        self.zoom=1
        
        self.posible_zoom={0:0.125,1:0.25,2:0.5,3:0.75,4:1,5:2,6:3}
        self.actual_zoom=4
        

        #Encargado de identificar los controles con lo que hacen
        self.controls={
            2:self.zoom_reset,
            4:self.zoom_out,
            5:self.zoom_in
            }
        
        global _instance
        _instance=self
        
    def update_position(self,position_to_folow):
        '''Actualiza la posicion'''
#         Partido de n para crear el movimiento suave
        self.float_position_map[0]+=((position_to_folow[0]-self.float_position_map[0])/60)
        self.float_position_map[1]+=((position_to_folow[1]-self.float_position_map[1])/60)
        
        self.position_map[0]=int(self.float_position_map[0])
        self.position_map[1]=int(self.float_position_map[1])

       
    def screen_update(self):
        '''Actualizar cuando se actualiza el tamano de la pantalla'''
        self.position_screen=pos2center([0,0],S_c().get_screen_size())
        
    def list_of_str_in_screen_chunks(self):
        '''Devuelve una lista de identificadores chunks que hay en pantalla. Ej: '0;0' '''
        screen_size = S_c().get_screen_size()
        #Actualizaciones para cuando se cambie la resolucion
        screen_size[0]//=S_c().w_factor_position*self.zoom
        screen_size[1]//=S_c().h_factor_position*self.zoom
        
#         Posiciones por pixeles en pantalla
#                   y1
#                    |
#         x1------------------x2
#                    |
#                   y2
        x1=self.position_map[0]-(screen_size[0]//2)
        x2=self.position_map[0]+(screen_size[0]//2)
        y1=self.position_map[1]-(screen_size[1]//2)
        y2=self.position_map[1]+(screen_size[1]//2)
        
#         Posiciones por posicion de chunk
        x1_chunk=int(x1//TILE_SIZE_GENERAL_PIXEL[0]//CHUNK_SIZE[0])
        x2_chunk=int(x2//TILE_SIZE_GENERAL_PIXEL[0]//CHUNK_SIZE[0])
        y1_chunk=int(y1//TILE_SIZE_GENERAL_PIXEL[1]//CHUNK_SIZE[1])
        y2_chunk=int(y2//TILE_SIZE_GENERAL_PIXEL[1]//CHUNK_SIZE[1])
                
        chunks_target=[]
        for x in range(x1_chunk,x2_chunk+1):
            for y in range(y1_chunk,y2_chunk+1):
                chunks_target.append(list2str2([x,y]))
        
        return chunks_target

    
    def zoom_reset(self):
        '''Resetea el zoom a 1'''
        self.zoom=1
        self.actual_zoom=4
        logging.info('Zoom: '+str(self.zoom))
        
    def zoom_in(self):
        '''Disminuye el zoom, lo que hace las cosas en pantalla mas grandes'''
        if self.actual_zoom-1 in self.posible_zoom:
            self.actual_zoom-=1
            self.zoom=self.posible_zoom[self.actual_zoom]
        logging.info('Zoom: '+str(self.zoom))
#         print('Zoom: '+str(self.zoom))
        
    def zoom_out(self):
        '''Aumenta el zoom, lo que hace las cosas en pantalla mas pequenas'''
        if self.actual_zoom+1 in self.posible_zoom:
            self.actual_zoom+=1
            self.zoom=self.posible_zoom[self.actual_zoom]
        logging.info('Zoom: '+str(self.zoom))
#         print('Zoom: '+str(self.zoom))