import random
import pygame
from Game.Components import Screen_container as S_c
from Game.Components.Camera import getInstance as camera

SMOKE_PRESET=[[lambda :random.randint(0,20)/10-1,lambda :random.randint(0,20)/10-1],lambda :random.randint(3,6),(80,80,80)]

# [(230,230,230),(214,214,214),(180,180,180),(150,150,150),(130,130,130)]

def getInstance():
    return _instance

def createInstance():
    Particle_manager()

class Particle_manager():
    
    def __init__(self):
        self.particle_gloups=[]
        
        global _instance
        _instance=self
        
        
    def spawn(self,position_map,layer,number,preset):
        new_particle_group=Particle_group()
        
        new_particle_group.spawn(position_map,layer, number, preset)
        
        self.particle_gloups.append(new_particle_group)
        
    def camera_update(self):
        for particle in self.particle_gloups:
            particle.camera_update()
        
        
    def add_to_self_layer(self):
        for particle in self.particle_gloups:
            S_c.getInstance().add_to_layer(particle,particle.layer)

                
                
class Particle_group():
    
    def __init__(self):
        # Formato [position_map,position_camera, velocity, timer, color]
        self.particles=[]
        
    def spawn(self,position_map,layer,number,preset):
        self.layer=layer
        loop_index=0
        while loop_index<number:
            self.particles.append(Particle([position_map[0],position_map[1]],preset))
#                 [position_map.copy(),[0,0],[random.randint(0,20)/10-1,random.randint(0,20)/10-1],random.randint(3,6),preset[random.randint(0,len(preset)-1)]])
            loop_index+=1
            
            
    def camera_update(self):
        for particle in self.particles:
            particle.camera_update()
        
        
    def draw(self):
        for particle in self.particles:
            particle.draw()
            if particle.timer <=0:
                self.particles.remove(particle) 
    
    
            
class Particle():
    
    def __init__(self,position_map,preset):
        '''Formato de preset= [velocity,timer,color]'''
        self.position_map=position_map
        self.position_camera=self.position_map.copy()
        
        self.velocity=[preset[0][0](),preset[0][1]()]
       
        
        self.timer=preset[1]()
        self.color=preset[2]      
            
    def camera_update(self):
        self.position_camera[0]=((self.position_map[0]-camera().position_map[0])*camera().zoom*S_c.getInstance().w_factor_position)+camera().position_screen[0]
        self.position_camera[1]=((self.position_map[1]-camera().position_map[1])*camera().zoom*S_c.getInstance().w_factor_position)+camera().position_screen[1]
        
    def draw(self):
        
        self.position_map[0] += self.velocity[0]
        self.position_map[1] += self.velocity[1]
#         print(self.position_map)
        self.timer-=0.1
        self.update_color_bright()
#             particle.velocity[1] +=0.03
        pygame.draw.circle(S_c.getInstance().screen, self.color, [int(self.position_camera[0]),int(self.position_camera[1])] , int(self.timer*2))
                
    
    def update_color_bright(self):
        update_factor=3
        r=self.color[2]+update_factor
        g=self.color[1]+update_factor
        b=self.color[0]+update_factor
        if r>255:
            r=255
        if g>255:
            g=255
        if b>255:
            b=255
        
        self.color=(r,g,b)
        
    def update_color_dark(self): 
        update_factor=3
        r=self.color[2]-update_factor
        g=self.color[1]-update_factor
        b=self.color[0]-update_factor
        if r<0:
            r=0
        if g<0:
            g=0
        if b<0:
            b=0
        
        self.color=(r,g,b)        
            
            
            
            
            
            
            