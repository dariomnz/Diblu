# from utils import center2pos
from Game.Components.Sprite import AnimateSprite
import pygame
from Game.Components.Item import Item
# from Game.Components.Screen_container import getInstance as S_c
# import pygame


class Player(AnimateSprite):
    '''Clase del jugador'''
    def __init__(self,position_map,name,layer=None):
        super().__init__(position_map,name,layer)
        
#         self.position_camera.move([0,0])
        
        self.direction={'back':0,'front':0,'left':0,'right':0}
        self.original_vel=1
        self.original_jump_vel=2
        self.sprint_vel=20
        self.vel=self.original_vel
        
        self.original_layer=self.layer
        
        
        #Encargado de identificar los controles de pulsar una tecla
        self.controls_press={
            'w':self.set_move_up,
            's':self.set_move_down,
            'a':self.set_move_left,
            'd':self.set_move_right,
            'space':self.set_jump,
            'left shift':self.set_sprint
            }
        
        #Encargado de identificar los controles de soltar una tecla
        self.controls_release={
            'w':self.del_move_up,
            's':self.del_move_down,
            'a':self.del_move_left,
            'd':self.del_move_right,
            'space':self.del_jump,
            'left shift':self.del_sprint
            }

                 
    def update(self):
        '''Actualiza la posicion en el mapa del jugador'''
        self.update_collision()
        self.layer=self.cB_rect_map['body'].bottom+100
        
        for collision in self.collisions:
            if collision['self_type'].startswith('body') and (collision['sprite_type'].startswith('block') or collision['sprite_type'].startswith('water')):
                self.repel_block(collision['self_rect'],collision['sprite_rect'])
                
            if collision['self_type'].startswith('jump_body') and collision['sprite_type'].startswith('jump_block'):
                    self.repel(collision['self_rect'],collision['sprite_rect'])
#                 if isinstance(collision['sprite'],Item):
#                     print('asdff')
#                     #arreglar
#                     collision['sprite'].repel(collision['sprite_rect'],collision['self_rect'])
                
            if collision['sprite_type'].startswith('tall_tile'):
#                 # Transparencia de arboles al pasar por ellos
                self.add_layer_below(collision['sprite'])
                
                collision['sprite'].do_transparent(0.5)
        
        
        if self.current_tag.startswith('jump'):
            #Solo se mueve en el momento que esta en el aire
            if self.current_frame_position>2 and self.current_frame_position<12:
                     
                self.float_position_map[0]=self.float_position_map[0]+((self.direction['right']-self.direction['left'])*self.vel)
                self.float_position_map[1]=self.float_position_map[1]+((self.direction['front']-self.direction['back'])*self.vel)
        
        if self.current_tag.startswith('run'):      
#             if self.current_frame_position>3:
            self.float_position_map[0]=self.float_position_map[0]+((self.direction['right']-self.direction['left'])*self.vel)
            self.float_position_map[1]=self.float_position_map[1]+((self.direction['front']-self.direction['back'])*self.vel)  
                
        
        # Comprobaciones para las animaciones
        if self.vel==1:
            if self.direction['back']==1:   
                self.update_animation('run_w')
            elif self.direction['front']==1:
                self.update_animation('run_s')
            elif self.direction['left']==1:
                self.update_animation('run_a')
            elif self.direction['right']==1:
                self.update_animation('run_d')
        elif self.vel==2:
            if self.direction['back']==1:   
                self.update_animation('jump_w')
            elif self.direction['front']==1:
                self.update_animation('jump_s')
            elif self.direction['left']==1:
                self.update_animation('jump_a')
            elif self.direction['right']==1:
                self.update_animation('jump_d')
            
        
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
        
    def repel_block(self,self_cB_map,sprite_cB_map):
        
        repel_vel=[0,0]
#         x_div=((self_cB_map.center[0]-sprite_cB_map.center[0])/10)
#         if x_div==0:
#             repel_vel[0]=0
#         else:
#             repel_vel[0]=self.vel
#          
#         y_div=((self_cB_map.center[1]-sprite_cB_map.center[1])/10)
#         if y_div==0:
#             repel_vel[1]=0
#         else:
#             repel_vel[1]=self.vel  
            
#         if self_cB_map.centerx<=sprite_cB_map.centerx:
#             if self_cB_map.centery<=sprite_cB_map.bottom-(self_cB_map.height//2) and self_cB_map.centery>=sprite_cB_map.top+(self_cB_map.height//2):
#                 repel_vel[0]=-self.vel
#         else:
#             if self_cB_map.centery<=sprite_cB_map.bottom-(self_cB_map.height//2) and self_cB_map.centery>=sprite_cB_map.top+(self_cB_map.height//2):
#                 repel_vel[0]=self.vel
# 
#         if self_cB_map.centery<=sprite_cB_map.centery:
#             if self_cB_map.centerx<=sprite_cB_map.left+(self_cB_map.width//2) and self_cB_map.centery>=sprite_cB_map.right-(self_cB_map.width//2):
#                 repel_vel[1]=self.vel
#         else:
#             if self_cB_map.centerx<=sprite_cB_map.left+(self_cB_map.width//2) and self_cB_map.centery>=sprite_cB_map.right-(self_cB_map.width//2):
#                 repel_vel[1]=-self.vel

        aux_size=[sprite_cB_map.height-self.vel*2,sprite_cB_map.width-self.vel*2]
        left_sprite_cB_map=pygame.rect.Rect([sprite_cB_map.x-sprite_cB_map.width,sprite_cB_map.y],aux_size)
        right_sprite_cB_map=pygame.rect.Rect([sprite_cB_map.x+sprite_cB_map.width,sprite_cB_map.y],aux_size)
        
        top_sprite_cB_map=pygame.rect.Rect([sprite_cB_map.x,sprite_cB_map.y-sprite_cB_map.height],aux_size)
        bottom_sprite_cB_map=pygame.rect.Rect([sprite_cB_map.x,sprite_cB_map.y+sprite_cB_map.height],aux_size)
        
        
        if self_cB_map.colliderect(left_sprite_cB_map):
            repel_vel[0]=-self.vel
        if self_cB_map.colliderect(right_sprite_cB_map):
            repel_vel[0]=self.vel
        if self_cB_map.colliderect(top_sprite_cB_map):
            repel_vel[1]=-self.vel
        if self_cB_map.colliderect(bottom_sprite_cB_map):
            repel_vel[1]=self.vel
        
        
            
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
    def set_jump(self):
        self.vel=self.original_jump_vel
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
    def del_jump(self):
        self.vel=self.original_vel
    def del_sprint(self):
        self.vel=self.original_vel