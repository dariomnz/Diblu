from utils import center2pos
from Game.Components.Sprite import AnimateSprite
from Game.Components import Screen_container as S_c


class Player(AnimateSprite):
    '''Clase del jugador'''
    def __init__(self,position_map,name,layer):
        super().__init__(position_map,name,layer)
        
        self.position_camera=[0,0]
        
        self.direction={'back':0,'front':0,'left':0,'right':0}
        self.original_vel=1
        self.sprint_vel=20
        self.vel=self.original_vel
        
        
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
        
    
    def draw(self):
        '''Pinta al jugador en su posicion de la camara centrado'''
        S_c.getInstance().screen.blit(self.image,center2pos(self.position_camera,self.get_image_size()))
                         
    def update(self):
        '''Actualiza la posicion en el mapa del jugador'''
       
            
        self.position_map[0]=self.position_map[0]+((self.direction['right']-self.direction['left'])*self.vel)
        self.position_map[1]=self.position_map[1]+((self.direction['front']-self.direction['back'])*self.vel)
        
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