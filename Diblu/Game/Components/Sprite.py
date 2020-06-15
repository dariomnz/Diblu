import pygame,os
from Game.Components.Image_item import Image_item
from utils import JSONParser, load_image
from Game.constants import TPS


class Sprite(pygame.sprite.Sprite,Image_item):
    '''Super clase de los sprites, hereda de pygame Sprite y de Image_item'''
    def __init__(self,position_map,image,screen_container):
        pygame.sprite.Sprite.__init__(self)
        Image_item.__init__(self,position_map,image,screen_container)
        
        
class AnimateSprite(pygame.sprite.Sprite,Image_item):
    '''Super clase de los sprites animados, hereda de pygame Sprite y de Image_item'''
    def __init__(self,position_map,image,screen_container):
        self.setup(image)
        
        image=self.images[0] 
        
        pygame.sprite.Sprite.__init__(self)
        Image_item.__init__(self,position_map,image,screen_container)
        
        # Escalamos todas las imagenes para que sean iguales
        for keys,value in self.images.items():
            image_size=[int(value.get_width()*self.scale_image),int(value.get_height()*self.scale_image)]
            self.images[keys]=pygame.transform.scale(value, (image_size[0], image_size[1]))
        
        
        
    def setup(self,image):
        '''Carga la configuracion del archivo .json de igual nombre'''
        config_data=JSONParser(image)
#         print(self.config_data['meta']['frameTags'])
        aux_tags=config_data['meta']['frameTags']
        
        # Creacion del animation_manager
        # Es un dict que tiene el estado como key y {las aciones(key) con los estados(value) a los que lleva} como value
        self.animation_manager=JSONParser(image+'_animation_manager')
        
        # Almacena las animaciones con el nombre como key y una lista con los frames
        self.tags={}
        self.current_frame_position=0
        for aux_tags_data in aux_tags:
            self.tags[aux_tags_data['name']]=list(range(aux_tags_data['from'],aux_tags_data['to']+1))
            
        self.current_tag=list(self.tags.keys())[0]
        # Almacena el frame como key y una lista con [x,y,w,h]
        self.image_sheet={}
        aux_image_sheet=config_data['frames']
        # Creacion de un dict para la duracion de cada frame
        self.frame_duration={}
        self.current_duration=0
        for aux_image_sheet_key,aux_image_sheet_data in aux_image_sheet.items():
            self.image_sheet[int(aux_image_sheet_key)]=[aux_image_sheet_data['frame']['x'],aux_image_sheet_data['frame']['y'],aux_image_sheet_data['frame']['w'],aux_image_sheet_data['frame']['h']]
            self.frame_duration[int(aux_image_sheet_key)]=aux_image_sheet_data['duration']/1000*TPS
        
        # Carga de el sprite_sheet     
        image+='.png'
#         file = os.path.join('..','data','images',image)
#         sprite_sheet=pygame.image.load(file).convert_alpha()
        sprite_sheet=load_image(image)  
        
        self.images={}
        self.current_frame=self.tags[self.current_tag][0]
        
        # Creacion de un dict de imagenes con key el frame
        for frame,rect in self.image_sheet.items():
            self.images[frame] = sprite_sheet.subsurface(rect)
            
        
    def update(self):
        
        self.current_duration+=1
        if self.current_duration>self.frame_duration[self.current_frame]:
            if self.current_frame_position == len(self.tags[self.current_tag])-1:
                self.update_animation('end_animation')
            self.current_duration=0
            self.current_frame_position = (self.current_frame_position+1)%len(self.tags[self.current_tag])
            self.current_frame=self.tags[self.current_tag][self.current_frame_position]
            self.image=self.images[self.current_frame]
            
     
    def update_animation(self,input_action):
        if input_action in self.animation_manager[self.current_tag]:
            self.current_tag=self.animation_manager[self.current_tag][input_action]
            
        
        
        
        
        
        
        
        
        
        
                
            