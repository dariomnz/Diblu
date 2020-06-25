import pygame
from Game.constants import CURSOR_CROSS
from utils import nearValue

def getInstance():
    return _instance

def createInstance():
    Screen_container()
    
class Screen_container(pygame.Surface):
    
    def __init__(self):
        
        #Tamaño del monitor
        monitor_info=pygame.display.Info()
        monitor_w=monitor_info.current_w
        monitor_h=monitor_info.current_h
        #Escalado del tamano a la mitad
        monitor_scaled=2
        
        self.initial_size=[monitor_w//monitor_scaled,monitor_h//monitor_scaled]
        
        self.new_size=self.initial_size.copy()
        
        #Atributos de la pantalla
        self.screen_attri=pygame.RESIZABLE | pygame.DOUBLEBUF
        
        #Inicio de la pantalla
        self.screen=pygame.display.set_mode(self.initial_size,self.screen_attri)
        
        pygame.display.set_caption("Diblu")
        
        self.w_factor_position=1
        self.h_factor_position=1
        
        self.w_factor_image=1
        self.h_factor_image=1
        
        self.setUpCursor()
        
        # dict de layer key un int dentro una lista de image_item
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
        
        for item_layer in sorted(list(self.layers.items())):
            for i in range(len(item_layer[1])):
                item_layer[1][i].draw()
                
            item_layer[1].clear()

                
    def mean_factor_position(self):
        '''devuelve la media del factor de posicion'''
        return (self.w_factor_position+self.h_factor_position)/2
    
    def update_size(self,new_size):
        '''Actualiza el monitor al tamano especificado [new_size[0],new_size[1]]'''
        self.new_size=new_size
        self.update_factor_image()
        self.update_factor_position()
        
        self.screen=pygame.display.set_mode(new_size,self.screen_attri)
        
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
        
        
    def get_screen_size(self):
        '''Devuelve el tamao de la pantalla'''
        return [self.screen.get_width(),self.screen.get_height()]
     
    
    def add_to_layer(self,image_item,layer):
        '''Anade el objeto a la layer especificada'''

        if layer in self.layers:
            self.layers[layer].append(image_item)
            image_item.layer=layer
        else:
            self.layers[layer]=[]
            self.layers[layer].append(image_item)
            image_item.layer=layer
        
        
    def add_to_self_layer(self,image_item):
        '''Anade el objeto a la layer especificada'''

        if image_item.layer in self.layers:
            self.layers[image_item.layer].append(image_item)
        else:
            self.layers[image_item.layer]=[]
            self.layers[image_item.layer].append(image_item)
     
    

        
        