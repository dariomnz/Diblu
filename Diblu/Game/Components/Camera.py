from utils import pos2center, list2str2
from Game.constants import CHUNK_SIZE, TILE_SIZE_GENERAL,\
    TILE_SIZE_GENERAL_PIXEL
class Camera():
    
    def __init__(self,position_map,screen_container):
        self.screen_container=screen_container
        self.position_map=position_map
        self.position_chunk=[0,0]
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
#         Partido de 10 para crear el movimiento suave
        self.position_map[0]+=((position_to_folow[0]-self.position_map[0])/20)
        self.position_map[1]+=((position_to_folow[1]-self.position_map[1])/20)
        
        self.position_chunk=[self.position_map[0]//TILE_SIZE_GENERAL[0]//CHUNK_SIZE[0],self.position_map[1]//TILE_SIZE_GENERAL[1]//CHUNK_SIZE[1]]
        
    def screen_update(self):
        self.position_screen=pos2center([0,0],self.screen_container.get_screen_size())
        
    def list_of_str_in_screen_chunks(self):
        screen_size = self.screen_container.get_screen_size()
#                   y1
#                    |
#         x1------------------x2
#                    |
#                   y2
        x1=self.position_map[0]-(screen_size[0]//2)
        x2=self.position_map[0]+(screen_size[0]//2)
        y1=self.position_map[1]-(screen_size[1]//2)
        y2=self.position_map[1]+(screen_size[1]//2)
        
        x1_chunk=int(x1//TILE_SIZE_GENERAL_PIXEL[0]//CHUNK_SIZE[0])
        x2_chunk=int(x2//TILE_SIZE_GENERAL_PIXEL[0]//CHUNK_SIZE[0])
        y1_chunk=int(y1//TILE_SIZE_GENERAL_PIXEL[1]//CHUNK_SIZE[1])
        y2_chunk=int(y2//TILE_SIZE_GENERAL_PIXEL[1]//CHUNK_SIZE[1])
        
#         print('x1,y1',[x1,y1])
#         print('x1_chunk,y1_chunk',[x1_chunk,y1_chunk])
#         print('x2,y2',[x2,y2])
#         print('x2_chunk,y2_chunk',[x2_chunk,y2_chunk])
        
        chunks_target=[]
        for x in range(x1_chunk,x2_chunk+1):
            for y in range(y1_chunk,y2_chunk+1):
                chunks_target.append(list2str2([x,y]))
        
#         print(chunks_target)
        return chunks_target
    
#         screen_size = self.screen_container.get_screen_size()
#         screen_size[0]=screen_size[0]//TILE_SIZE_GENERAL[0]//CHUNK_SIZE[0]
#         screen_size[1]=screen_size[1]//TILE_SIZE_GENERAL[1]//CHUNK_SIZE[1]
# #         print(screen_size)
#         chunks_target=[]
#         for x in range(-screen_size[0]//2,screen_size[0]//2):
#             for y in range(-screen_size[1]//2,screen_size[1]//2):
#                 chunks_target.append(list2str2([int(self.position_chunk[0]-x),int(self.position_chunk[1]-y)]))
#         print(chunks_target)
#         return chunks_target
              
            
    
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