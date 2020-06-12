import pygame,os


class Image_item():
    
    def __init__(self,position_map,image,screen_container):
        scale_image=2
        self.screen_container=screen_container
        self.screen=screen_container.screen
        if isinstance(image, str):
            file = os.path.join('..','data','images',image)
            self.original_image=pygame.image.load(file).convert_alpha()
        else:
            self.original_image=image
        
        self.original_image_size=[int(self.original_image.get_width()*scale_image),int(self.original_image.get_height()*scale_image)]
        self.original_image=pygame.transform.scale(self.original_image, (self.original_image_size[0], self.original_image_size[1]))
        self.image=self.original_image.copy()
        
        self.position_map=position_map
        self.position_map[0]*=scale_image
        self.position_map[1]*=scale_image
        self.position_camera=position_map.copy()
        self.rect=[self.position_camera[0],self.position_camera[1],self.original_image_size[0],self.original_image_size[1]]
        
    def draw(self):
        self.screen.blit(self.image,self.position_camera)
        
    def update(self):
        pass
    
    def camera_update(self,camera):
        self.rect=[self.position_camera[0],self.position_camera[1],self.original_image_size[0],self.original_image_size[1]]
        self.position_camera[0]=((self.position_map[0]-camera.position_map[0])*camera.zoom*self.screen_container.w_factor_position)+camera.position_screen[0]
        self.position_camera[1]=((self.position_map[1]-camera.position_map[1])*camera.zoom*self.screen_container.h_factor_position)+camera.position_screen[1]
        
    def image_update(self,camera):
        self.image=pygame.transform.scale(self.original_image, (int(self.original_image_size[0]*camera.zoom*self.screen_container.w_factor_image), int(self.original_image_size[1]*camera.zoom*self.screen_container.h_factor_image)))
        
    def get_image_size(self):
        return [self.image.get_width(),self.image.get_height()]
        