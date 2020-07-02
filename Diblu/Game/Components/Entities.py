# from utils import center2pos
from Game.Components.Sprite import AnimateSprite
# from Game.Components.Screen_container import getInstance as S_c
# import pygame


class Player(AnimateSprite):
    '''Clase del jugador'''
    def __init__(self,position_map,name,layer=None):
        super().__init__(position_map,name,layer)
        
#         self.position_camera.move([0,0])
        
        self.direction={'back':0,'front':0,'left':0,'right':0}
        self.original_vel=2
        self.sprint_vel=20
        self.vel=self.original_vel
        
        self.original_layer=self.layer
        
        
        #Encargado de identificar los controles de pulsar una tecla
        self.controls_press={
            'w':self.set_move_up,
            's':self.set_move_down,
            'a':self.set_move_left,
            'd':self.set_move_right,
            'left shift':self.set_sprint
            }
        
        #Encargado de identificar los controles de soltar una tecla
        self.controls_release={
            'w':self.del_move_up,
            's':self.del_move_down,
            'a':self.del_move_left,
            'd':self.del_move_right,
            'left shift':self.del_sprint
            }

                 
    def update(self):
        '''Actualiza la posicion en el mapa del jugador'''
        self.update_collision()
        self.layer=self.cB_rect_map['jump_body'].bottom+100
        
        for collision in self.collisions:
            if collision['self_type'].startswith('jump_body') and (collision['sprite_type'].startswith('block') or collision['sprite_type'].startswith('water')):
                
#                 self.add_layer_above(collision['sprite'])
#                 sprite.do_transparent(100,1)
                self.repel(collision['self_rect'],collision['sprite_rect'])
            if collision['self_type'].startswith('body') and collision['sprite_type'].startswith('jump_block'):
                self.add_layer_above(collision['sprite'])
                self.repel(collision['self_rect'],collision['sprite_rect'])
                
            if collision['sprite_type'].startswith('tree_leave'):
#                 # Transparencia de arboles al pasar por ellos
                self.add_layer_below(collision['sprite'])
                
#                 print(sprite.image.get_alpha())
                collision['sprite'].do_transparent(0.5)
#                 print(sprite.image.get_alpha())
#                 sprite.image.set_alpha(200)
#             self.clear_collision(collision['sprite'])
        
        
        if self.current_tag.startswith('jump'):
            if self.current_frame_position>2 and self.current_frame_position<12:
                
#                 self.last_position=self.float_position_map.copy()
                     
                self.float_position_map[0]=self.float_position_map[0]+((self.direction['right']-self.direction['left'])*self.vel)
                self.float_position_map[1]=self.float_position_map[1]+((self.direction['front']-self.direction['back'])*self.vel)
                
#                 for collision in self.collisions:
#                     if collision['self_type'].startswith('jump_body') and (collision['sprite_type'].startswith('block') or collision['sprite_type'].startswith('water')):
#                         self.float_position_map[0]=self.float_position_map[0]-((self.direction['right']-self.direction['left'])*self.vel*1.5)
#                         self.float_position_map[1]=self.float_position_map[1]-((self.direction['front']-self.direction['back'])*self.vel*1.5)
                
                
        self.position_map[0]=int(self.float_position_map[0])
        self.position_map[1]=int(self.float_position_map[1])
        
        # Comprobaciones para las animaciones
        if self.direction['back']==1:   
            self.update_animation('press_w')
        elif self.direction['front']==1:
            self.update_animation('press_s')
        elif self.direction['left']==1:
            self.update_animation('press_a')
        elif self.direction['right']==1:
            self.update_animation('press_d')
        
        super().update()
        
    def repel(self,self_cB_map,sprite_cB_map):
        
        repel_vel=[0,0]
        x_div=((self_cB_map.center[0]-sprite_cB_map.center[0])/10)
        if x_div==0:
            repel_vel[0]=0
        else:
            repel_vel[0]=self.vel/x_div
         
        y_div=((self_cB_map.center[1]-sprite_cB_map.center[1])/10)
        if y_div==0:
            repel_vel[1]=0
        else:
            repel_vel[1]=self.vel/y_div   


            
        self.float_position_map[0]+=repel_vel[0]
        self.float_position_map[1]+=repel_vel[1]

        
        
    #Multiplicadores de movimiento, para los controles
    #Press
    def set_move_up(self):
        self.direction['back']=1
    def set_move_down(self):
        self.direction['front']=1
    def set_move_left(self):
        self.direction['left']=1
    def set_move_right(self):
        self.direction['right']=1
    def set_sprint(self):
        self.vel=self.sprint_vel
    
    #Release 
    def del_move_up(self):
        self.direction['back']=0
    def del_move_down(self):
        self.direction['front']=0
    def del_move_left(self):
        self.direction['left']=0
    def del_move_right(self):
        self.direction['right']=0
    def del_sprint(self):
        self.vel=self.original_vel