import pygame
from Game.Components.Image_item  import Image_item
from utils import JSONParser, load_image, getRect
from Game.constants import TPS,DEFAULT_SCALE
from Game.Components.Screen_container import getInstance as S_c
from Game.Components.Camera import getInstance as camera


class Sprite(pygame.sprite.Sprite,Image_item):
    '''Super clase de los sprites, hereda de pygame Sprite y de Image_item'''
    def __init__(self,position_map,name,layer=None):
        self.collisions=[]
        self.collision_type='None'
        pygame.sprite.Sprite.__init__(self)
        Image_item.__init__(self,position_map,name,layer)
        
        self.float_position_map=[self.position_map[0],self.position_map[1]]
    
    def update(self):
        self.clear_collision()
        
        
        self.position_map[0]=int(self.float_position_map[0])
        self.position_map[1]=int(self.float_position_map[1])
        
        super().update()
    
    def clear_collision(self):
        self.collisions.clear()

        
    def repel(self,self_cB_map,sprite_cB_map):
        
        repel_vel=[0,0]
#         print(sprite_cB_map.center)
        repel_vel[0]=(self_cB_map.center[0]-sprite_cB_map.center[0])/15
        repel_vel[1]=(self_cB_map.center[1]-sprite_cB_map.center[1])/15
        
        self.float_position_map[0]+=repel_vel[0]
        self.float_position_map[1]+=repel_vel[1]
        
        
        
        
    def check_collision(self,sprite):
        '''Actualiza la posicion de las cB_rect_map y comprueba colisiones'''
        # Comprobacion de la colision   
        for collision_type,rect in self.cB_rect_map.items():
            list_rects=list(sprite.cB_rect_map.values())
            list_index_rect=rect.collidelistall(list_rects)
            for index_rect in list_index_rect:
                if index_rect!=-1:
                    collision_type_sprite=list(sprite.cB_rect_map.keys())[index_rect]
                    self.collisions.append({'self_type':collision_type,'self_rect':rect,'sprite':sprite,'sprite_type':collision_type_sprite,'sprite_rect':list_rects[index_rect]})
                    if not (collision_type=='item_body' and collision_type_sprite=='item_body'):
                        sprite.collisions.append({'self_type':collision_type_sprite,'self_rect':list_rects[index_rect],'sprite':self,'sprite_type':collision_type,'sprite_rect':rect})
#                     return True
#         return False
    
    def update_collision(self):
        self.update_cB_rect()
        # Actualizacion con la posicion en el mapa        
        for collision_type in self.cB_rect.keys():
            self.cB_rect_map[collision_type][0]=self.cB_rect[collision_type][0]+self.position_map[0]
            self.cB_rect_map[collision_type][1]=self.cB_rect[collision_type][1]+self.position_map[1]    
            
    
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
        last_scale=self.scale_image
        self.scale_image=1
        super().__init__(position_map,image,layer)
        
        self.scale_image=last_scale
        
        
        
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
        
        self.scale_image=DEFAULT_SCALE
        
        self.sprite_sheet_image=self.original_sprite_sheet_image.copy()
        
        
        self.images={}
        
        self.current_frame=self.tags[self.current_tag][0]
               
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

        super().update()
     
    def update_animation(self,input_action):
        '''Introduciendole el input deseado, se comprueba si desde la animacion que esta cambia a otra'''
        if input_action in self.animation_manager[self.current_tag]:
            if 'resetAnimation' in self.animation_manager[self.current_tag]['properties']:
                self.current_frame_position=0
                
            self.current_tag=self.animation_manager[self.current_tag][input_action]
                
        #Generacion experimental de particulas
#             Particle_manager.getInstance().spawn(self.position_map.center,self.layer-0.1, 20,Particle_manager.SMOKE_PRESET) 
     
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
        
        self.cB_data=JSONParser(name+'-collisionBox')
        
        self.original_image_sprite_sheet_collision_box={}
        
        for collision_type,image_name in self.cB_data.items():
            self.original_image_sprite_sheet_collision_box[collision_type]=load_image(image_name)
        
#         self.original_image_sprite_sheet_collision_box=load_image(name+'-collisionBox.png')
         
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
            
            for collision_type,aux_image_sprite_sheet_collisionBox in self.image_sprite_sheet_collision_box.items(): 
            
                aux_cB_image=aux_image_sprite_sheet_collisionBox.subsurface(rect_in_sprite_sheet_image) 
                
                aux_mask=pygame.mask.from_surface(aux_cB_image, 127)
    #             self.cB_rects[image_key]=[getRect(aux_mask.outline())]   
                aux_outline=aux_mask.outline()
                
                if image_key not in self.cB_rects:
                    self.cB_rects[image_key]={}
                    
                if len(aux_outline)>0:
                    self.cB_rects[image_key][collision_type]=getRect(aux_mask.outline())
                else:
                    self.cB_rects[image_key]={}
    #                 self.cB_rects[image_key].append(getRect(aux_outline))  
  
    def update_cB_rect(self):
        self.cB_rect={}
        self.cB_rect_map={}
        for collision_type,rect in self.cB_rects[self.current_frame].items():
            self.cB_rect[collision_type]=rect.copy()
            self.cB_rect_map[collision_type]=rect.copy()
        
        
        
        
                
            