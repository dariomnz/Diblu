import pygame


class Screen_container(pygame.Surface):

    def __init__(self):
        monitor_info=pygame.display.Info()
        monitor_w=monitor_info.current_w
        monitor_h=monitor_info.current_h
        
        
        monitor_scaled=2
        self.initial_size=[monitor_w//monitor_scaled,monitor_h//monitor_scaled]
        
        self.new_size=self.initial_size.copy()
        self.screen=pygame.display.set_mode(self.initial_size,pygame.RESIZABLE)
        
        pygame.display.set_caption("Diblu")
        
        self.w_factor_position=1
        self.h_factor_position=1
        
        self.w_factor_image=1
        self.h_factor_image=1
    
    def mean_factor_position(self):
        return (self.w_factor_position+self.h_factor_position)/2
    
    def update_size(self,new_size):
        self.new_size=new_size
        self.update_factor_image()
        self.update_factor_position()
        
        self.screen=pygame.display.set_mode(new_size,pygame.RESIZABLE)
        
    def update_factor_position(self):
        self.w_factor_position=self.new_size[0]/self.screen.get_width()
        self.h_factor_position=self.new_size[1]/self.screen.get_height()
        
    def update_factor_image(self):
        self.w_factor_image=self.new_size[0]/self.initial_size[0]
        self.h_factor_image=self.new_size[1]/self.initial_size[1]
        
    def get_screen_size(self):
        return [self.screen.get_width(),self.screen.get_height()]