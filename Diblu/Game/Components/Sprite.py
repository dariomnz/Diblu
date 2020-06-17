import pygame
from Game.Components.Image_item import Image_item
from utils import JSONParser, load_image
from Game.constants import TPS, TILE_SIZE_GENERAL_PIXEL, TILE_SIZE_GENERAL
from Game.Components import Screen_container as S_c
from Game import Particle_manager


class Sprite(pygame.sprite.Sprite,Image_item):
    '''Super clase de los sprites, hereda de pygame Sprite y de Image_item'''
    def __init__(self,position_map,image,layer):
        pygame.sprite.Sprite.__init__(self)
        Image_item.__init__(self,position_map,image,layer)
        
        
class AnimateSprite(pygame.sprite.Sprite,Image_item):
    '''Super clase de los sprites animados, hereda de pygame Sprite y de Image_item'''
    def __init__(self,position_map,image,layer):
        self.setup(image)
        
        image=self.images[0] 
        
        pygame.sprite.Sprite.__init__(self)
        Image_item.__init__(self,position_map,image,layer)
        
        # Escalamos todas las imagenes para que sean iguales
#         for keys,value in self.images.items():
#             image_size=[int(value.get_width()*self.scale_image),int(value.get_height()*self.scale_image)]
#             self.images[keys]=pygame.transform.scale(value, (image_size[0], image_size[1]))
        
        
        
    def setup(self,image):
        '''Carga la configuracion del archivo .json de igual nombre'''
        config_data=JSONParser(image)

        aux_tags=config_data['meta']['frameTags']
        
        # Creacion del animation_manager
        # Es un dict que tiene el estado como key y {las aciones(key) con los estados(value) a los que lleva} como value
        self.animation_manager=JSONParser(image+'_animation_manager')
        
        # Almacena las animaciones con el nombre como key y una lista con numero de frames respecto current_frame_position
        self.tags={}
        self.current_frame_position=0
        for aux_tags_data in aux_tags:
            self.tags[aux_tags_data['name']]=list(range(aux_tags_data['from'],aux_tags_data['to']+1))
        
        
        self.current_tag=list(self.tags.keys())[0]
        # Almacena el frame como key y una lista con [x,y,w,h]
        self.image_sheet_dict={}
        aux_image_sheet=config_data['frames']
        # Creacion de un dict para la duracion de cada frame
        self.frame_duration={}
        self.current_duration=0
        for aux_image_sheet_key,aux_image_sheet_data in aux_image_sheet.items():
            self.image_sheet_dict[int(aux_image_sheet_key)]=[aux_image_sheet_data['frame']['x'],aux_image_sheet_data['frame']['y'],aux_image_sheet_data['frame']['w'],aux_image_sheet_data['frame']['h']]
            self.frame_duration[int(aux_image_sheet_key)]=aux_image_sheet_data['duration']/1000*TPS
        
        # Carga de el sprite_sheet    
        self.original_sprite_sheet_image=load_image(image+'.png')  
        
        self.scale_image=TILE_SIZE_GENERAL_PIXEL[0]/TILE_SIZE_GENERAL[0]
        self.original_sprite_sheet_image=pygame.transform.scale(self.original_sprite_sheet_image, (int(self.original_sprite_sheet_image.get_width()*self.scale_image), int(self.original_sprite_sheet_image.get_height()*self.scale_image)))
            
        self.sprite_sheet_image=self.original_sprite_sheet_image.copy()
        
        
        self.images={}
#         self.original_images=self.images.copy()
        
        self.current_frame=self.tags[self.current_tag][0]
        
        
        self.generate_sprite_sheet_images(1)
        # Creacion de un dict de imagenes con key el frame
#         for frame,rect in self.image_sheet_dict.items():
#             self.images[frame] = self.sprite_sheet_image.subsurface(rect)
#             self.images[frame]=pygame.transform.scale(self.images[frame], (int(self.images[frame].get_width()*self.scale_image), int(self.images[frame].get_height()*self.scale_image)))
            
        # Creacion de una copia de la imagen original, para transformaciones
        
        
    def update(self):
        '''Encargado de ir rotando las imagenes de la animacion'''
        self.current_duration+=1
        if self.current_duration>self.frame_duration[self.current_frame]:
            if self.current_frame_position == len(self.tags[self.current_tag])-1:
                self.update_animation('end_animation')
            self.current_duration=0
            self.current_frame_position = (self.current_frame_position+1)%len(self.tags[self.current_tag])
            self.current_frame=self.tags[self.current_tag][self.current_frame_position]
            self.image=self.images[self.current_frame]
     
    def update_animation(self,input_action):
        '''Introduciendole el input deseado, se comprueba si desde la animacion que esta cambia a otra'''
        if input_action in self.animation_manager[self.current_tag]:
            self.current_tag=self.animation_manager[self.current_tag][input_action]
            
            if 'resetAnimation' in self.animation_manager[self.current_tag]['properties']:
                self.current_frame_position=0
        #Generacion experimental de particulas
            Particle_manager.getInstance().spawn(self.position_map,self.layer-0.1, 20,Particle_manager.SMOKE_PRESET) 
     
    def image_update(self, camera):
        '''Reescala las imagenes cuando es necesario'''
        self.sprite_sheet_image=pygame.transform.scale(self.original_sprite_sheet_image, (int(self.original_sprite_sheet_image.get_width()*camera.zoom*S_c.getInstance().w_factor_image), int(self.original_sprite_sheet_image.get_height()*camera.zoom*S_c.getInstance().h_factor_image))) 
        self.generate_sprite_sheet_images(camera.zoom)
     
     
    def generate_sprite_sheet_images(self,camera_zoom):    
        
        self.images={}
        for image_key in self.image_sheet_dict.keys():
            attr0=self.image_sheet_dict[image_key][0]*camera_zoom*S_c.getInstance().w_factor_image*self.scale_image
            attr1=self.image_sheet_dict[image_key][1]*camera_zoom*S_c.getInstance().h_factor_image*self.scale_image
            attr2=self.image_sheet_dict[image_key][2]*camera_zoom*S_c.getInstance().w_factor_image*self.scale_image
            attr3=self.image_sheet_dict[image_key][3]*camera_zoom*S_c.getInstance().h_factor_image*self.scale_image
            rect_in_sprite_sheet_image=pygame.Rect(attr0,attr1,attr2,attr3)
            
            self.images[image_key]=self.sprite_sheet_image.subsurface(rect_in_sprite_sheet_image)
        
        
        
        
        
        
        
        
        
                
            