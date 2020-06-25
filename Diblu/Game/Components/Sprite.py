import pygame
from Game.Components.Image_item  import Image_item
from utils import JSONParser, load_image, getRect
from Game.constants import TPS, TILE_SIZE_GENERAL_PIXEL, TILE_SIZE_GENERAL
from Game.Components.Screen_container import getInstance as S_c
from Game.Components.Camera import getInstance as camera
from Game import Particle_manager


class Sprite(pygame.sprite.Sprite,Image_item):
    '''Super clase de los sprites, hereda de pygame Sprite y de Image_item'''
    def __init__(self,position_map,name,layer):
        pygame.sprite.Sprite.__init__(self)
        Image_item.__init__(self,position_map,name,layer)
    
    def check_collision(self,sprite):
        '''Actualiza la posicion de las cB_rect_map y comprueba colisiones'''
        
        # Comprobacion de la colision   
        for rect in self.cB_rect_map:
            if rect.collidelist(sprite.cB_rect_map)!=-1:
                return True
        return False
    
    def update_collision(self):
        self.update_cB_rect()
#         print(self.cB_rect)
        # Actualizacion con la posicion en el mapa 
#         print(self.position_map)           
        for index in range(len(self.cB_rect)):
            self.cB_rect_map[index][0]=self.cB_rect[index][0]+self.position_map[0]
            self.cB_rect_map[index][1]=self.cB_rect[index][1]+self.position_map[1]    
            
#         print(self.cB_rect)
    
    def setUp_collisionBox(self,name):
        '''Metodo para override'''
        pass
    
    def generate_cB_rects(self): 
        '''Metodo para override'''
        pass
    
    def update_cB_rect(self):
        '''Metodo para override'''
        pass

    
        
class AnimateSprite(Sprite):
    '''Super clase de los sprites animados, hereda de pygame Sprite y de Image_item'''
    def __init__(self,position_map,name,layer):
        self.setup(name)
        
        image=self.images[0] 
        
        
        super().__init__(position_map,image,layer)
        # Escalamos todas las imagenes para que sean iguales
#         for keys,value in self.images.items():
#             image_size=[int(value.get_width()*self.scale_image),int(value.get_height()*self.scale_image)]
#             self.images[keys]=pygame.transform.scale(value, (image_size[0], image_size[1]))
        
        
        
    def setup(self,name):
        '''Carga la configuracion del archivo .json de igual nombre'''
        config_data=JSONParser(name)

        aux_tags=config_data['meta']['frameTags']
        
        # Creacion del animation_manager
        # Es un dict que tiene el estado como key y {las aciones(key) con los estados(value) a los que lleva} como value
        self.animation_manager=JSONParser(name+'_animation_manager')
        
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
        self.original_sprite_sheet_image=load_image(name+'.png')  
        
        self.scale_image=TILE_SIZE_GENERAL_PIXEL[0]/TILE_SIZE_GENERAL[0]
#         self.original_sprite_sheet_image=pygame.transform.scale(self.original_sprite_sheet_image, (int(self.original_sprite_sheet_image.get_width()*self.scale_image), int(self.original_sprite_sheet_image.get_height()*self.scale_image)))
            
        self.sprite_sheet_image=self.original_sprite_sheet_image.copy()
        
        
        self.images={}
#         self.original_images=self.images.copy()
        
        self.current_frame=self.tags[self.current_tag][0]
        
#         self.collisionBox=CollisionBox(name,'AnimateSprite')
        
        self.generate_sprite_sheet_images(1)
        
        self.setUp_collisionBox(name)
        
        
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
#             self.update_cB_rect()
            # Para colisiones
#             self.collisionBox.image=self.collisionBox.image_collision_box[self.current_frame]
     
    def update_animation(self,input_action):
        '''Introduciendole el input deseado, se comprueba si desde la animacion que esta cambia a otra'''
        if input_action in self.animation_manager[self.current_tag]:
            if 'resetAnimation' in self.animation_manager[self.current_tag]['properties']:
                self.current_frame_position=0
                
            self.current_tag=self.animation_manager[self.current_tag][input_action]
                
        #Generacion experimental de particulas
            Particle_manager.getInstance().spawn(self.position_map.center,self.layer-0.1, 20,Particle_manager.SMOKE_PRESET) 
     
    def image_update(self):
        '''Reescala las imagenes cuando es necesario'''
        self.sprite_sheet_image=pygame.transform.scale(self.original_sprite_sheet_image, (int(self.original_sprite_sheet_image.get_width()*camera().zoom*S_c().w_factor_image), int(self.original_sprite_sheet_image.get_height()*camera().zoom*S_c().h_factor_image))) 
        # para colisiones
#         self.collisionBox.image_sprite_sheet_collision_box=pygame.transform.scale(self.collisionBox.original_image_sprite_sheet_collision_box, (int(self.collisionBox.original_image_sprite_sheet_collision_box.get_width()*camera().zoom*S_c().w_factor_image), int(self.collisionBox.original_image_sprite_sheet_collision_box.get_height()*camera().zoom*S_c().h_factor_image))) 
       
        self.generate_sprite_sheet_images(camera().zoom)
     
     
    def generate_sprite_sheet_images(self,camera_zoom):    
        
        self.images={}
        for image_key in self.image_sheet_dict.keys():
            attr0=self.image_sheet_dict[image_key][0]*camera_zoom*S_c().w_factor_image*self.scale_image
            attr1=self.image_sheet_dict[image_key][1]*camera_zoom*S_c().h_factor_image*self.scale_image
            attr2=self.image_sheet_dict[image_key][2]*camera_zoom*S_c().w_factor_image*self.scale_image
            attr3=self.image_sheet_dict[image_key][3]*camera_zoom*S_c().h_factor_image*self.scale_image
            rect_in_sprite_sheet_image=pygame.Rect(attr0,attr1,attr2,attr3)
            
            self.images[image_key]=self.sprite_sheet_image.subsurface(rect_in_sprite_sheet_image)
            # Para colisiones
#             self.collisionBox.image_collision_box[image_key]=self.collisionBox.image_sprite_sheet_collision_box.subsurface(rect_in_sprite_sheet_image)
    
    def setUp_collisionBox(self,name): 
        self.original_image_sprite_sheet_collision_box=load_image(name+'-collisionBox.png')
         
        self.image_sprite_sheet_collision_box=self.original_image_sprite_sheet_collision_box.copy()
         
        self.generate_cB_rects() 
        self.cB_rect=self.cB_rects[0]
        self.cB_rect_map=self.cB_rect.copy()
        
    def generate_cB_rects(self): 
        
        self.cB_rects={}
        for image_key in self.image_sheet_dict.keys():
            attr0=self.image_sheet_dict[image_key][0]*camera().zoom*S_c().w_factor_image*self.scale_image
            attr1=self.image_sheet_dict[image_key][1]*camera().zoom*S_c().h_factor_image*self.scale_image
            attr2=self.image_sheet_dict[image_key][2]*camera().zoom*S_c().w_factor_image*self.scale_image
            attr3=self.image_sheet_dict[image_key][3]*camera().zoom*S_c().h_factor_image*self.scale_image
            rect_in_sprite_sheet_image=pygame.Rect(attr0,attr1,attr2,attr3)
            
            aux_cB_image=self.image_sprite_sheet_collision_box.subsurface(rect_in_sprite_sheet_image) 
            
            aux_mask=pygame.mask.from_surface(aux_cB_image, 127)
            self.cB_rects[image_key]=[getRect(aux_mask.outline())]   
  
    def update_cB_rect(self):
        self.cB_rect=[]
        self.cB_rect_map=[]
        for rect in self.cB_rects[self.current_frame]:
            self.cB_rect.append(rect.copy())
            self.cB_rect_map.append(rect.copy())  
        
        
        
        
                
            