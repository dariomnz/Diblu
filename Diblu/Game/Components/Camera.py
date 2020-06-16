from utils import pos2center, list2str2
from Game.constants import CHUNK_SIZE,TILE_SIZE_GENERAL_PIXEL
from Game.Components import Screen_container as S_c

class Camera():
    
    def __init__(self,position_map):
        self.position_map=position_map

        self.position_screen=pos2center([0,0],S_c.getInstance().get_screen_size())
        self.zoom=1
        self.max_zoom=4
        self.min_zoom=0.25
        #Encargado de identificar los controles con lo que hacen
        self.controls={
            2:self.zoom_reset,
            4:self.zoom_out,
            5:self.zoom_in
            }
        
    def update_position(self,position_to_folow):
        '''Actualiza la posicion'''
#         Partido de n para crear el movimiento suave
        self.position_map[0]+=((position_to_folow[0]-self.position_map[0])/40)
        self.position_map[1]+=((position_to_folow[1]-self.position_map[1])/40)
        

       
    def screen_update(self):
        '''Actualizar cuando se actualiza el tamano de la pantalla'''
        self.position_screen=pos2center([0,0],S_c.getInstance().get_screen_size())
        
    def list_of_str_in_screen_chunks(self):
        '''Devuelve una lista de identificadores chunks que hay en pantalla. Ej: '0;0' '''
        screen_size = S_c.getInstance().get_screen_size()
        #Actualizaciones para cuando se cambie la resolucion
        screen_size[0]//=S_c.getInstance().w_factor_position
        screen_size[1]//=S_c.getInstance().h_factor_position
        
#         Posiciones por pixeles en pantalla
#                   y1
#                    |
#         x1------------------x2
#                    |
#                   y2
        x1=self.position_map[0]-(screen_size[0]//2)
        x2=self.position_map[0]+(screen_size[0]//2)
        y1=self.position_map[1]-(screen_size[1]//2)
        y2=self.position_map[1]+(screen_size[1]//2)
        
#         Posiciones por posicion de chunk
        x1_chunk=int(x1//TILE_SIZE_GENERAL_PIXEL[0]//CHUNK_SIZE[0])
        x2_chunk=int(x2//TILE_SIZE_GENERAL_PIXEL[0]//CHUNK_SIZE[0])
        y1_chunk=int(y1//TILE_SIZE_GENERAL_PIXEL[1]//CHUNK_SIZE[1])
        y2_chunk=int(y2//TILE_SIZE_GENERAL_PIXEL[1]//CHUNK_SIZE[1])
                
        chunks_target=[]
        for x in range(x1_chunk,x2_chunk+1):
            for y in range(y1_chunk,y2_chunk+1):
                chunks_target.append(list2str2([x,y]))
        
        return chunks_target

    
    def zoom_reset(self):
        '''Resetea el zoom a 1'''
        self.zoom=1
        print('Zoom: '+str(self.zoom))
        
    def zoom_in(self):
        '''Disminuye el zoom, lo que hace las cosas en pantalla mas grandes'''
        self.zoom-=0.5
        if self.zoom<self.min_zoom:
            self.zoom=self.min_zoom
        print('Zoom: '+str(self.zoom))
        
    def zoom_out(self):
        '''Aumenta el zoom, lo que hace las cosas en pantalla mas pequenas'''
        self.zoom+=0.5
        if self.zoom>self.max_zoom:
            self.zoom=self.max_zoom
        print('Zoom: '+str(self.zoom))