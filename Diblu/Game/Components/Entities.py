from utils import center2pos
from Game.Components.Sprite import Sprite



class Player(Sprite):
    
    def __init__(self,position_map,image,screen_container):
        super().__init__(position_map,image,screen_container)
        
        self.position_camera=[0,0]
        
        self.direction={'UP':0,'DOWN':0,'LEFT':0,'RIGHT':0}
        self.original_vel=1
        self.vel=self.original_vel
        
        self.controls_press={
            'w':self.set_move_up,
            's':self.set_move_down,
            'a':self.set_move_left,
            'd':self.set_move_right
            }
        self.controls_release={
            'w':self.del_move_up,
            's':self.del_move_down,
            'a':self.del_move_left,
            'd':self.del_move_right
            }
        
    
    def draw(self):
        self.screen.blit(self.image,center2pos(self.position_camera,self.get_image_size()))
                         
    def update(self):
        self.position_map[0]=self.position_map[0]+((self.direction['RIGHT']-self.direction['LEFT'])*self.vel)
        self.position_map[1]=self.position_map[1]+((self.direction['DOWN']-self.direction['UP'])*self.vel)
    
    
    def set_move_up(self):
        self.direction['UP']=1
    def set_move_down(self):
        self.direction['DOWN']=1
    def set_move_left(self):
        self.direction['LEFT']=1
    def set_move_right(self):
        self.direction['RIGHT']=1
        
    def del_move_up(self):
        self.direction['UP']=0
    def del_move_down(self):
        self.direction['DOWN']=0
    def del_move_left(self):
        self.direction['LEFT']=0
    def del_move_right(self):
        self.direction['RIGHT']=0