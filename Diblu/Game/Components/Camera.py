from utils import pos2center
class Camera():
    
    def __init__(self,position_map,screen_container):
        self.screen_container=screen_container
        self.position_map=position_map
        self.position_screen=pos2center([0,0],self.screen_container.get_screen_size())
        self.zoom=1
        self.max_zoom=2
        self.min_zoom=0.1
        self.controls={
            2:self.zoom_reset,
            4:self.zoom_out,
            5:self.zoom_in
            }
        
    def update_position(self,position_to_folow):
        self.position_map[0]+=((position_to_folow[0]-self.position_map[0])/10)
        self.position_map[1]+=((position_to_folow[1]-self.position_map[1])/10)
        
    def screen_update(self):
        self.position_screen=pos2center([0,0],self.screen_container.get_screen_size())
        
    def zoom_reset(self):
        self.zoom=1
        print('Zoom: '+str(self.zoom))
        
    def zoom_in(self):
        self.zoom-=0.1
        if self.zoom<self.min_zoom:
            self.zoom=self.min_zoom
        print('Zoom: '+str(self.zoom))
        
    def zoom_out(self):
        self.zoom+=0.1
        if self.zoom>self.max_zoom:
            self.zoom=self.max_zoom
        print('Zoom: '+str(self.zoom))