import pygame
from Game.constants import CURSOR_CROSS
from pygame import key
from copy import deepcopy
from utils import nearValue

def getInstance():
    return _instance

def createInstance():
    Screen_container()
    
class Screen_container(pygame.Surface):
    
    def __init__(self):
        
        #Tama�o del monitor
        monitor_info=pygame.display.Info()
        monitor_w=monitor_info.current_w
        monitor_h=monitor_info.current_h
        #Escalado del tamano a la mitad
        monitor_scaled=2
        
        self.initial_size=[monitor_w//monitor_scaled,monitor_h//monitor_scaled]
        
        self.new_size=self.initial_size.copy()
        #Inicio de la pantalla
        self.screen=pygame.display.set_mode(self.initial_size,pygame.RESIZABLE)
        
        pygame.display.set_caption("Diblu")
        
        self.w_factor_position=1
        self.h_factor_position=1
        
        self.w_factor_image=1
        self.h_factor_image=1
        
        self.setUpCursor()
        
        # dict de layer key un int dentro un dict con key identificador y el image_item
        self.layers={}
        
        global _instance
        _instance=self
        
    def setUpCursor(self):
        '''Carga un cursor'''
        hotspot = None
        for y in range(len(CURSOR_CROSS)):
            for x in range(len(CURSOR_CROSS[y])):
                if CURSOR_CROSS[y][x] in ['x', ',', 'O']:
                    hotspot = x,y
                    break
            if hotspot != None:
                break
        if hotspot == None:
            raise Exception("No hotspot specified for cursor!")
        s2 = []
        for line in CURSOR_CROSS:
            s2.append(line.replace(',', '.'))
        cursor, mask = pygame.cursors.compile(s2, 'X', '.', 'o')
        size = len(CURSOR_CROSS[0]), len(CURSOR_CROSS)
        pygame.mouse.set_cursor(size, hotspot, cursor, mask)
        
    
    def draw_layers(self):
        '''Pinta en pantalla todas las layers'''
        list_to_pop=[]
        for key_layer,item_layer in sorted(self.layers.items()):
            for key_obj in item_layer.keys():
                item_layer[key_obj].draw();
                list_to_pop.append([key_layer,key_obj])
                
        for aux in list_to_pop:
                del self.layers[aux[0]][aux[1]]
            
    
    def mean_factor_position(self):
        '''devuelve la media del factor de posicion'''
        return (self.w_factor_position+self.h_factor_position)/2
    
    def update_size(self,new_size):
        '''Actualiza el monitor al tamano especificado [new_size[0],new_size[1]]'''
        self.new_size=new_size
#         self.update_factors()
        self.update_factor_image()
        self.update_factor_position()
        
        self.screen=pygame.display.set_mode(new_size,pygame.RESIZABLE)
#     def update_factors(self):
#         self.w_factor_position=self.new_size[0]/self.screen.get_width()
#         self.h_factor_position=self.new_size[1]/self.screen.get_height()
#         
#         if nearValue(self.w_factor_position,0.5,0.2):
#             self.w_factor_position=0.5
#         if nearValue(self.h_factor_position,0.5,0.2):
#             self.h_factor_position=0.5
#         if nearValue(self.w_factor_position,2,0.2):
#             self.w_factor_position=2
#         if nearValue(self.h_factor_position,2,0.2):
#             self.h_factor_position=2
#         
#         self.w_factor_image=self.w_factor_position
#         self.h_factor_image=self.h_factor_position
        
    def update_factor_position(self):
        '''Actualiza el factor de la posicion de los objetos'''
        self.w_factor_position=self.new_size[0]/self.screen.get_width()
        self.h_factor_position=self.new_size[1]/self.screen.get_height()
        
        if nearValue(self.w_factor_position,0.5,0.2):
            self.w_factor_position=0.5
        if nearValue(self.h_factor_position,0.5,0.2):
            self.h_factor_position=0.5
        if nearValue(self.w_factor_position,2,0.2):
            self.w_factor_position=2
        if nearValue(self.h_factor_position,2,0.2):
            self.h_factor_position=2
            
        print(self.h_factor_position,' ',self.h_factor_position)
        
         
    def update_factor_image(self):
        '''Actualiza el factor del tamano de la imagen de los objetos'''
        self.w_factor_image=self.new_size[0]/self.initial_size[0]
        self.h_factor_image=self.new_size[1]/self.initial_size[1]
#         self.w_factor_image=self.new_size[0]/self.screen.get_width()
#         self.h_factor_image=self.new_size[1]/self.screen.get_height()
        
        if nearValue(self.w_factor_image,1,0.2):
            self.w_factor_image=1
        if nearValue(self.h_factor_image,1,0.2):
            self.h_factor_image=1
        if nearValue(self.w_factor_image,2,0.2):
            self.w_factor_image=2
        if nearValue(self.h_factor_image,2,0.2):
            self.h_factor_image=2
            
#         print(self.w_factor_image,' ',self.h_factor_image)
        
        
    def get_screen_size(self):
        '''Devuelve el tamao de la pantalla'''
        return [self.screen.get_width(),self.screen.get_height()]
    
    
    