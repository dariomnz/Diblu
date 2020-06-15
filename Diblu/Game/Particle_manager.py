import random
import pygame

SMOKE_PRESET=[(255,255,255),(214,214,214),(180,180,180),(150,150,150),(130,130,130)]
class Particle_manager():
    
    def __init__(self,screen_container):
        # Formato [position_map,position_camera, velocity, timer, color]
        self.particles=[]
        self.screen_container=screen_container
        
        
    def spawn(self,position_map,number,preset):
        for x in range(number):
            self.particles.append([position_map.copy(),[0,0],[random.randint(0,20)/10-1,random.randint(0,20)/10-1],random.randint(8,10),preset[random.randint(0,len(preset)-1)]])
        
        
    def camera_update(self,camera):
        for particle in self.particles:
            particle[1][0]=((particle[0][0]-camera.position_map[0])*camera.zoom*self.screen_container.w_factor_position)+camera.position_screen[0]
            particle[1][1]=((particle[0][1]-camera.position_map[1])*camera.zoom*self.screen_container.w_factor_position)+camera.position_screen[1]
        
        
    def draw(self):
#         pass
        for particle in self.particles:
            particle[0][0] += particle[2][0]
            particle[0][1] += particle[2][1]
            particle[3]-=0.1
            particle[2][1] +=0.03
            pygame.draw.circle(self.screen_container.screen, particle[4], [int(particle[1][0]),int(particle[1][1])] , int(particle[3]))
            if particle[3] <=0:
                self.particles.remove(particle)