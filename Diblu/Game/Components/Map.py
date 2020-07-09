import random,noise,time
from Game.Components.Tile import Tile, TILEMAP1
from utils import JSONParser,JSONsave,str2list3, list2str3, list2str2, str2list2,\
    list2str4, list2str9
from Game.constants import CHUNK_SIZE, TILE_TYPES,\
    TILE_TYPES_4NEIGHBOUR_FIX,\
    TILE_TYPES_9NEIGHBOUR1, TILE_TYPES_9NEIGHBOUR2, TILE_TYPES_UPNEIGHBOUR,\
    TILE_SIZE, TILE_SIZE_GENERAL, TILE_SIZE_GENERAL_PIXEL,\
    TILE_TYPES_9NEIGHBOUR3
from Game.Components.Screen_container import getInstance as S_c
import logging
# import sys

class Chunk():
    
    def __init__(self,chunk_data):
        '''chunk_data is a list, in [0]:the string of position, in [1] a dict with tiles'''
        self.position=str2list2(chunk_data[0])
        self.position_map=[self.position[0]*CHUNK_SIZE[0]*TILE_SIZE_GENERAL[0],self.position[1]*CHUNK_SIZE[1]*TILE_SIZE_GENERAL[1]]
        self.tiles=chunk_data[1]
        
        self.items=[]
        
#         self.tile_group=list(self.tiles.values())
    
        
#     def draw(self):
#         '''Dibuja todas las tiles del chunk por capas'''
#         #Ordenacion por capas
#         self.tile_group.sort(key=lambda tile:tile.layer)
#          
#         for tile in self.tile_group:
#             tile.draw()
            
    def camera_update(self):
        '''Actualiza la posicion de todas sus tile'''
        for tile in self.tiles.values():
            tile.camera_update()
            
        for item in self.items:
            item.camera_update()
    
    def update(self):
        '''Actualiza la posicion de todas sus tile'''
        for tile in self.tiles.values():
            tile.update()
            
        for item in self.items:
            item.update()
            
    def image_update(self):
        '''Actualiza la imagen de todas sus tile'''
        for tile in self.tiles.values():
            tile.image_update()    
            
        for item in self.items:
            item.image_update()
    
    def check_collisions(self,sprite):
        for tile in self.tiles.values():
            tile.check_collision(sprite)
            
        for item in self.items:
            item.check_collision(sprite)
    
    def check_items_collisions(self):
        for item in self.items:
            for tile in self.tiles.values():
                item.check_collision(tile)
            for item2 in self.items:   
                if item!=item2:
                    item.check_collision(item2) 
    
    def add_self_layer(self):
        '''Se anaden a su layer'''
#         print(sorted(list(self.tiles.items()),key=lambda x:str2list3(x[0])[2]))
        for tile in sorted(list(self.tiles.items()),key=lambda x:str2list3(x[0])[2]):
            S_c().add_to_self_layer(tile[1])
            
        for item in self.items:
            S_c().add_to_self_layer(item)
        
    
    def del_layer(self):
        '''Elimina de las layers el chunk'''
        for tile in self.tiles.values():
            tile.del_layer()    
            
    def del_item(self,item):
        '''Elimina el item del chunk'''
        if item in self.items:
            self.items.pop(self.items.index(item))
            


def getInstance():
    return _instance

def createInstance(load):
    Map(load)
                
class Map():
    
    def __init__(self,load=True):
#         self.size_square_in_chunk=16
        self.size_square_in_chunk=24
        # Si esta true lo carga sino genera un mapa nuevo
        # Estructura de chunks es un dict 'x,y' del chunk con un dict de tiles
        if load:
            self.map_load('world')
        else:
            self.chunks={}
#             self.generate_map([CHUNK_SIZE[0]*self.size_square_in_chunk,CHUNK_SIZE[1]*self.size_square_in_chunk])
        
        global _instance
        _instance=self
        
    def save(self):
        '''Guarda el mapa'''
        self.map_save('world')
        
    
    def chunk_in_item(self,position_map):
        '''Apartir de position_map devuelve el chunk en el que esta'''
        
        aux_size=CHUNK_SIZE[0]*TILE_SIZE_GENERAL_PIXEL[0]
        
        aux_x=(position_map.x-(position_map.width+1))//aux_size
        aux_y=(position_map.y-(position_map.height+1))//aux_size
        
        chunk_key=list2str2([aux_x,aux_y])
        
        if chunk_key in self.chunks:
            return self.chunks[chunk_key]
        else:
            return None
        
        

    def map_load(self,name):
        '''Carga el mapa name'''
        start_time=time.time()
        tilemap = TILEMAP1
        chunks={}
        map_data = JSONParser(name)
        self.seed1=map_data['seed1']
        
        self.seed2=map_data['seed2']
        
        for chunk_data in map_data['chunks'].items():
            chunks[chunk_data[0]]={}
            for tile_data in map_data['chunks'][chunk_data[0]].items():
                tile_position=str2list3(tile_data[0])
                chunk_position=str2list2(chunk_data[0])
    #             Tile_position= pos dentro chunk + el chunk en el que esta * su tamaño
                tile_position=[tile_position[0]+chunk_position[0]*CHUNK_SIZE[0],tile_position[1]+chunk_position[1]*CHUNK_SIZE[1]]#,tile_position[2]]
                
                if tile_position==0:
                    chunks[chunk_data[0]][tile_data[0]]=Tile(tile_position,tile_data[1],tilemap,0)
                else:
                    chunks[chunk_data[0]][tile_data[0]]=Tile(tile_position,tile_data[1],tilemap)
    #             sys.exit()
            chunks[chunk_data[0]]=Chunk([chunk_data[0],chunks[chunk_data[0]]])
            
        logging.info('Time consumed in load the map: '+str(time.time()-start_time)+' seconds')
    #     print('Time consumed in load the map:',time.time()-start_time,' seconds')
        self.chunks=chunks



    def map_save(self,name):
        '''Guarda los chunks en el mapa name'''
        start_time=time.time()
        map_data={'name':'world','seed1':self.seed1,'seed2':self.seed2}
    
        chunks_data={}
        for chunk_item in self.chunks.items():
            chunks_data[chunk_item[0]]={}
            for tile_data in self.chunks[chunk_item[0]].tiles.items():
                chunks_data[chunk_item[0]][tile_data[0]]=tile_data[1].tile_type
    
        map_data['chunks']=chunks_data
        
        JSONsave(name, map_data)
        logging.info('Time consumed in save the map: '+str(time.time()-start_time)+' seconds')
    #     print('Time consumed in save the map:',time.time()-start_time,' seconds')
        
        
    def generate_chunk_map(self,chunk_key):
        '''map_size is the number or tiles [tiles_w,tiles_h], it must be multiple of 16'''
        
        chunk_pos=str2list2(chunk_key)
        
        chunk_pos[0]*=CHUNK_SIZE[0]
        chunk_pos[1]*=CHUNK_SIZE[1]
        
        
#         print(chunk_key,chunk_pos)
        
        start_time=time.time()
        map_size=[chunk_pos[0]//2,chunk_pos[1]//2]
        tilemap = TILEMAP1
        chunks={}
        aux_tiles_data={}
    #     scale = 18
        scale1 = 50
        octaves1 = 8
        persistence1 = -0.5
        lacunarity1 = -0.4
        scale2 = 15
        octaves2 = 8
        persistence2 = -0.3
        lacunarity2 = 0.7
        random.seed()
        if not hasattr(self, 'seed1'):
            self.seed1 = int(random.random()*100)
        if not hasattr(self, 'seed2'):
            self.seed2 = int(random.random()*100)
        
        # Extension de 1 para comprobar los bordes
        map_size[0]+=1
        map_size[1]+=1
        
        for x in range(chunk_pos[0]-2,chunk_pos[0]+CHUNK_SIZE[0]+2):
            for y in range(chunk_pos[1]-2,chunk_pos[1]+CHUNK_SIZE[0]+2):
                
                noise_at_xy1=noise.pnoise2(x/scale1,
                                                y/scale1,
                                                octaves=octaves1,
                                                persistence=persistence1,
                                                lacunarity=lacunarity1,
                                                repeatx=99999999,#map_size[0],
                                                repeaty=99999999,#map_size[1],
                                                base=self.seed1)
                noise_at_xy2=noise.pnoise2(x/scale2,
                                                y/scale2,
                                                octaves=octaves2,
                                                persistence=persistence2,
                                                lacunarity=lacunarity2,
                                                repeatx=99999999,#map_size[0],
                                                repeaty=99999999,#map_size[1],
                                                base=self.seed2)
                
                
                noise_at_xy=noise_at_xy1+noise_at_xy2
                
                if noise_at_xy< -0.2:
                    # Agua
                    tile_type=1
                elif noise_at_xy< 0.1:
                    # Arena
                    tile_type=0
                else:
                    # Cesped
                    tile_type=23
    
                      
                aux_tiles_data[list2str2([x,y])]=[x,y,tile_type]
        
        
        
#         print(chunk_key,aux_tiles_data)
        aux_tiles_data=self.adapt_borders(aux_tiles_data)
        
        # Eliminacion del exceso
        for key in list(aux_tiles_data.keys()):
            key_list=str2list2(key)
            if key_list[0] not in range(chunk_pos[0],chunk_pos[0]+CHUNK_SIZE[0]) or key_list[1] not in range(chunk_pos[1],chunk_pos[1]+CHUNK_SIZE[1]):
                    aux_tiles_data.pop(key)
        
        # Vuelta a el tamaño del mapa
        map_size[0]-=1
        map_size[1]-=1
        
        
#     #     Primero crecion de chunks vacions en el dict chunks
#         for x in range(-map_size[0]//CHUNK_SIZE[0],map_size[0]//CHUNK_SIZE[0]):
#             for y in range(-map_size[1]//CHUNK_SIZE[1],map_size[1]//CHUNK_SIZE[1]):
#                 chunk_position=list2str2([x,y])
#                 chunks[chunk_position]={}

        chunks[chunk_key]={}
    #     Segundo creacion de los tile de cada chunk guardados en un dict
        for tile in aux_tiles_data.values():
#             if tile[0]>chunk_pos[0] and tile[0]<chunk_pos[0]+CHUNK_SIZE[0] and tile[1]>chunk_pos[1] and tile[1]<chunk_pos[0]+CHUNK_SIZE[0]:
                tile_position_in_chunk=[tile[0]%CHUNK_SIZE[0],tile[1]%CHUNK_SIZE[1],0]
                tile_position_in_chunk_str=list2str3(tile_position_in_chunk)
                tile_position=[tile[0],tile[1]]
#                 chunk_key=list2str2([tile[0]//8,tile[1]//8])
                
                if tile[2]!=-10:
#                     print(chunk_key)
                    chunks[chunk_key][tile_position_in_chunk_str]=Tile(tile_position,tile[2],tilemap,0)
                
                #Anadido de detalles en la layer 1
        
                tile_position_in_chunk[2]=1
                tile_position_in_chunk_str=list2str3(tile_position_in_chunk)
                if tile_position_in_chunk_str not in chunks[chunk_key]:
                    #Detalles del agua
                    if tile[2]==1:
                        numero_random=random.randint(100,150)
                        if numero_random in TILE_TYPES:
                            if TILE_TYPES[numero_random][2]!=TILE_SIZE_GENERAL[0] or TILE_TYPES[numero_random][3]!=TILE_SIZE_GENERAL[1]:
                                
                                self.generate_chunk_big_tile(tile[:2],chunk_key,tile[2], numero_random, chunks, aux_tiles_data)
        
                            else:
                                #layer
                                tile_position_in_chunk[2]=1
                                tile_position_in_chunk_str=list2str3(tile_position_in_chunk)
                                chunks[chunk_key][tile_position_in_chunk_str]=Tile(tile_position,numero_random,tilemap)
                    #Detalles del cesped
                    elif tile[2]==23:
                        numero_random=random.randint(200,280)
                        if numero_random in TILE_TYPES:
                            if TILE_TYPES[numero_random][2]!=TILE_SIZE_GENERAL[0] or TILE_TYPES[numero_random][3]!=TILE_SIZE_GENERAL[1]:
                                
                                self.generate_chunk_big_tile(tile[:2],chunk_key,tile[2], numero_random, chunks, aux_tiles_data)
                                
                            else:
        #                         layer
                                tile_position_in_chunk[2]=1
                                tile_position_in_chunk_str=list2str3(tile_position_in_chunk)
                                chunks[chunk_key][tile_position_in_chunk_str]=Tile(tile_position,numero_random,tilemap)
                    #Detalles de la arena
                    elif tile[2]==0:
                        numero_random=random.randint(300,450)
                        if numero_random in TILE_TYPES:
                            if TILE_TYPES[numero_random][2]!=TILE_SIZE_GENERAL[0] or TILE_TYPES[numero_random][3]!=TILE_SIZE_GENERAL[1]:
                                
                                self.generate_chunk_big_tile(tile[:2],chunk_key,tile[2], numero_random, chunks, aux_tiles_data)
                                
                            else:
        #                         layer
                                tile_position_in_chunk[2]=1
                                tile_position_in_chunk_str=list2str3(tile_position_in_chunk)
                                chunks[chunk_key][tile_position_in_chunk_str]=Tile(tile_position,numero_random,tilemap)
                                
                    
    #     Tercero creacion de los chunks
#         for x in range(-map_size[0]//CHUNK_SIZE[0],map_size[0]//CHUNK_SIZE[0]):
#             for y in range(-map_size[1]//CHUNK_SIZE[1],map_size[1]//CHUNK_SIZE[1]):
#                 chunk_position=list2str2([x,y])
        chunks[chunk_key]=Chunk([chunk_key,chunks[chunk_key]])
         
        logging.info('Time consumed in generate the map: '+str(time.time()-start_time)+' seconds')       
    #     print('Time consumed in generate the map:',time.time()-start_time,' seconds')
        
        for aux_key,aux_chunk in chunks.items():
            self.chunks[aux_key]=aux_chunk    
        
    def generate_map(self,map_size):
        '''map_size is the number or tiles [tiles_w,tiles_h], it must be multiple of 16'''
        if map_size[0]%16!=0 or map_size[1]%16!=0:
            print('Generacion de mapa incorrecta,map_size tiene que ser multiplo de 16')
            return None
        
        start_time=time.time()
        map_size=[map_size[0]//2,map_size[1]//2]
        tilemap = TILEMAP1
        chunks={}
        aux_tiles_data={}
    #     scale = 18
        scale1 = 50
        octaves1 = 8
        persistence1 = -0.5
        lacunarity1 = -0.4
        scale2 = 15
        octaves2 = 8
        persistence2 = -0.3
        lacunarity2 = 0.7
        random.seed()
        if not hasattr(self, 'seed1'):
            self.seed1 = int(random.random()*100)
        if not hasattr(self, 'seed2'):
            self.seed2 = int(random.random()*100)
        
        # Extension de 1 para comprobar los bordes
        map_size[0]+=1
        map_size[1]+=1
        
        for x in range(-map_size[0],map_size[0]):
            for y in range(-map_size[1],map_size[1]):
                noise_at_xy1=noise.pnoise2(x/scale1,
                                                y/scale1,
                                                octaves=octaves1,
                                                persistence=persistence1,
                                                lacunarity=lacunarity1,
                                                repeatx=99999999,#map_size[0],
                                                repeaty=99999999,#map_size[1],
                                                base=self.seed1)
                noise_at_xy2=noise.pnoise2(x/scale2,
                                                y/scale2,
                                                octaves=octaves2,
                                                persistence=persistence2,
                                                lacunarity=lacunarity2,
                                                repeatx=99999999,#map_size[0],
                                                repeaty=99999999,#map_size[1],
                                                base=self.seed2)
                
                
                noise_at_xy=noise_at_xy1+noise_at_xy2
                
                if noise_at_xy< -0.2:
                    # Agua
                    tile_type=1
                elif noise_at_xy< 0.1:
                    # Arena
                    tile_type=0
                else:
                    # Cesped
                    tile_type=23
    
                      
                aux_tiles_data[list2str2([x,y])]=[x,y,tile_type]
        
        
        
        aux_tiles_data=self.adapt_borders(aux_tiles_data)
        
        # Vuelta a el tamaño del mapa
        map_size[0]-=1
        map_size[1]-=1
        
    #     Primero crecion de chunks vacions en el dict chunks
        for x in range(-map_size[0]//CHUNK_SIZE[0],map_size[0]//CHUNK_SIZE[0]):
            for y in range(-map_size[1]//CHUNK_SIZE[1],map_size[1]//CHUNK_SIZE[1]):
                chunk_position=list2str2([x,y])
                chunks[chunk_position]={}
    
    #     Segundo creacion de los tile de cada chunk guardados en un dict
        for tile in aux_tiles_data.values():
            if tile[0]>-map_size[0] and tile[0]<map_size[0] and tile[1]>-map_size[1] and tile[1]<map_size[1]:
                tile_position_in_chunk=[tile[0]%CHUNK_SIZE[0],tile[1]%CHUNK_SIZE[1],0]
                tile_position_in_chunk_str=list2str3(tile_position_in_chunk)
                tile_position=[tile[0],tile[1]]
                chunk_position=list2str2([tile[0]//8,tile[1]//8])
                if tile[2]!=-10:
                    chunks[chunk_position][tile_position_in_chunk_str]=Tile(tile_position,tile[2],tilemap,0)
                
                #Anadido de detalles en la layer 1
        
                tile_position_in_chunk[2]=1
                tile_position_in_chunk_str=list2str3(tile_position_in_chunk)
                if tile_position_in_chunk_str not in chunks[chunk_position]:
                    #Detalles del agua
                    if tile[2]==1:
                        numero_random=random.randint(100,150)
                        if numero_random in TILE_TYPES:
                            if TILE_TYPES[numero_random][2]!=TILE_SIZE_GENERAL[0] or TILE_TYPES[numero_random][3]!=TILE_SIZE_GENERAL[1]:
                                
                                self.generate_big_tile(tile[:2],tile[2], numero_random, chunks, aux_tiles_data)
        
                            else:
                                #layer
                                tile_position_in_chunk[2]=1
                                tile_position_in_chunk_str=list2str3(tile_position_in_chunk)
                                chunks[chunk_position][tile_position_in_chunk_str]=Tile(tile_position,numero_random,tilemap)
                    #Detalles del cesped
                    elif tile[2]==23:
                        numero_random=random.randint(200,280)
                        if numero_random in TILE_TYPES:
                            if TILE_TYPES[numero_random][2]!=TILE_SIZE_GENERAL[0] or TILE_TYPES[numero_random][3]!=TILE_SIZE_GENERAL[1]:
                                
                                self.generate_big_tile(tile[:2],tile[2], numero_random, chunks, aux_tiles_data)
                                
                            else:
        #                         layer
                                tile_position_in_chunk[2]=1
                                tile_position_in_chunk_str=list2str3(tile_position_in_chunk)
                                chunks[chunk_position][tile_position_in_chunk_str]=Tile(tile_position,numero_random,tilemap)
                    #Detalles de la arena
                    elif tile[2]==0:
                        numero_random=random.randint(300,450)
                        if numero_random in TILE_TYPES:
                            if TILE_TYPES[numero_random][2]!=TILE_SIZE_GENERAL[0] or TILE_TYPES[numero_random][3]!=TILE_SIZE_GENERAL[1]:
                                
                                self.generate_big_tile(tile[:2],tile[2], numero_random, chunks, aux_tiles_data)
                                
                            else:
        #                         layer
                                tile_position_in_chunk[2]=1
                                tile_position_in_chunk_str=list2str3(tile_position_in_chunk)
                                chunks[chunk_position][tile_position_in_chunk_str]=Tile(tile_position,numero_random,tilemap)
                                
                    
    #     Tercero creacion de los chunks
        for x in range(-map_size[0]//CHUNK_SIZE[0],map_size[0]//CHUNK_SIZE[0]):
            for y in range(-map_size[1]//CHUNK_SIZE[1],map_size[1]//CHUNK_SIZE[1]):
                chunk_position=list2str2([x,y])
                chunks[chunk_position]=Chunk([chunk_position,chunks[chunk_position]])
         
        logging.info('Time consumed in generate the map: '+str(time.time()-start_time)+' seconds')       
    #     print('Time consumed in generate the map:',time.time()-start_time,' seconds')
        self.chunks=chunks
    
    def adapt_borders(self,aux_tiles_data):
        #Aux_tiles_data siempre va a ser de 1 o 0, es en change_data cuando se actualizan a los bordes
        
        #Primera pasada para quitar las salidas de 1 solo de agua, sobre la original
        for aux_tiles_data_key,aux_tiles_data_item in aux_tiles_data.items():
            key_tile_tipe_neirbours=neirbours9([aux_tiles_data_item[0],aux_tiles_data_item[1]],aux_tiles_data)
            if key_tile_tipe_neirbours in TILE_TYPES_9NEIGHBOUR1:
                aux_tiles_data[aux_tiles_data_key]=[aux_tiles_data_item[0],aux_tiles_data_item[1],TILE_TYPES_9NEIGHBOUR1[key_tile_tipe_neirbours]]
        
        #Genero una copia para no reescribir aux_tiles_data
        change_data=aux_tiles_data.copy()
        
        #Segunda pasada para los bordes principales del agua
        for change_data_key,change_data_item in aux_tiles_data.items():
            key_tile_tipe_neirbours=neirbours9([change_data_item[0],change_data_item[1]],aux_tiles_data)
            if key_tile_tipe_neirbours in TILE_TYPES_9NEIGHBOUR2:
                change_data[change_data_key]=[change_data_item[0],change_data_item[1],TILE_TYPES_9NEIGHBOUR2[key_tile_tipe_neirbours]]
         
        #Tercera para poner la parte de abajo de los bordes de arriba
        for change_data_key,change_data_item in change_data.items():
            key_tile_tipe_neirbours=upNeirbour([change_data_item[0],change_data_item[1]],change_data)
            if key_tile_tipe_neirbours in TILE_TYPES_UPNEIGHBOUR:
                change_data[change_data_key]=[change_data_item[0],change_data_item[1],TILE_TYPES_UPNEIGHBOUR[key_tile_tipe_neirbours]]
        
        
        # Copia interna
        change_data_sand={}
        
        for aux_key,aux_value in aux_tiles_data.items():
            change_data_sand[aux_key]=aux_value.copy()
        
        # Elimminado del agua
        for aux_tiles_data_key in list(change_data_sand.keys()):
            if change_data_sand[aux_tiles_data_key][2]==1:
                change_data_sand[aux_tiles_data_key][2]=0
        
        #Cuarta pasada para los bordes principales de la arena
        for change_data_key,change_data_item in change_data_sand.items():
            key_tile_tipe_neirbours=neirbours9([change_data_item[0],change_data_item[1]],change_data_sand)
            if key_tile_tipe_neirbours in TILE_TYPES_9NEIGHBOUR3:
                change_data[change_data_key]=[change_data_item[0],change_data_item[1],TILE_TYPES_9NEIGHBOUR3[key_tile_tipe_neirbours]] 
         
        #Quinta pasada para realizar el arreglo de unas texturas    
        for change_data_key,change_data_item in change_data.items():
            key_tile_tipe_neirbours=neirbours4([change_data_item[0],change_data_item[1]],change_data)
            if key_tile_tipe_neirbours in TILE_TYPES_4NEIGHBOUR_FIX:
                change_data[change_data_key]=[change_data_item[0],change_data_item[1],TILE_TYPES_4NEIGHBOUR_FIX[key_tile_tipe_neirbours]]
         
        return change_data
       
    def generate_chunk_big_tile(self,position,chunk_key,parent_tile_type,tile_type,chunks,map_data):
        '''Encargado de poner tiles que ocupen mas de 1 tile
            position=[x,y]
            parent_tile_type= tipo de tile del suelo
            tile_type= tipo de tile actual
            tiles_size=[w,h] en tiles
            chunks es dict de datos
            map_data dict de 'x;y':[x,y,type]'''
        
        tilemap = TILEMAP1
        chunk_position=chunk_key
        tile_position_in_chunk=[position[0]%CHUNK_SIZE[0],position[1]%CHUNK_SIZE[1],1]
        
        #Comprobacion de que no esta en bordes de chunk
        if not (tile_position_in_chunk[0]<CHUNK_SIZE[0]-(TILE_SIZE(tile_type)[0]-1) and tile_position_in_chunk[1]<CHUNK_SIZE[1]-(TILE_SIZE(tile_type)[1]-1)):
            return
    
        #Comprobacion de que tiene espacio
        for x in range(TILE_SIZE(tile_type)[0]):
            for y in range(TILE_SIZE(tile_type)[1]):
                
                aux_tile_position=[position[0]+x,position[1]+y]
                if list2str2(aux_tile_position) in map_data:
                    #Respecto a si esta en tierra o agua
                    if map_data[list2str2(aux_tile_position)][2]!=parent_tile_type:
                    #Como no tiene sale
                        return
                    #Respecto a si ya esta ocupada posicion
                    aux_tile_position_in_chunk=[tile_position_in_chunk[0]+x,tile_position_in_chunk[1]+y,1]
                    aux_tile_position_in_chunk_str=list2str3(aux_tile_position_in_chunk)
                    if aux_tile_position_in_chunk_str in chunks[chunk_position]:
                        return
                else:
                    return
        # Creacion de las tiles necesarias        
        for x in range(TILE_SIZE(tile_type)[0]):
            for y in range(TILE_SIZE(tile_type)[1]):
                if x==0 and y==0:
                    aux_tile_position_in_chunk=[tile_position_in_chunk[0]+x,tile_position_in_chunk[1]+y,1]
                    aux_tile_position_in_chunk_str=list2str3(aux_tile_position_in_chunk)
                    chunks[chunk_position][aux_tile_position_in_chunk_str]=Tile(position,tile_type,tilemap)
                else:
                    aux_tile_position_in_chunk=[tile_position_in_chunk[0]+x,tile_position_in_chunk[1]+y,1]
                    aux_tile_position_in_chunk_str=list2str3(aux_tile_position_in_chunk)
                    position[0]+=x
                    position[1]+=y
                    chunks[chunk_position][aux_tile_position_in_chunk_str]=Tile(position,-10,tilemap)
                    
    def generate_big_tile(self,position,parent_tile_type,tile_type,chunks,map_data):
        '''Encargado de poner tiles que ocupen mas de 1 tile
            position=[x,y]
            parent_tile_type= tipo de tile del suelo
            tile_type= tipo de tile actual
            tiles_size=[w,h] en tiles
            chunks es dict de datos
            map_data dict de 'x;y':[x,y,type]'''
        
        tilemap = TILEMAP1
        chunk_position=list2str2([position[0]//8,position[1]//8])
        tile_position_in_chunk=[position[0]%CHUNK_SIZE[0],position[1]%CHUNK_SIZE[1],1]
        
        #Comprobacion de que no esta en bordes de chunk
        if not (tile_position_in_chunk[0]<CHUNK_SIZE[0]-(TILE_SIZE(tile_type)[0]-1) and tile_position_in_chunk[1]<CHUNK_SIZE[1]-(TILE_SIZE(tile_type)[1]-1)):
            return
    
        #Comprobacion de que tiene espacio
        for x in range(TILE_SIZE(tile_type)[0]):
            for y in range(TILE_SIZE(tile_type)[1]):
                
                aux_tile_position=[position[0]+x,position[1]+y]
                if list2str2(aux_tile_position) in map_data:
                    #Respecto a si esta en tierra o agua
                    if map_data[list2str2(aux_tile_position)][2]!=parent_tile_type:
                    #Como no tiene sale
                        return
                    #Respecto a si ya esta ocupada posicion
                    aux_tile_position_in_chunk=[tile_position_in_chunk[0]+x,tile_position_in_chunk[1]+y,1]
                    aux_tile_position_in_chunk_str=list2str3(aux_tile_position_in_chunk)
                    if aux_tile_position_in_chunk_str in chunks[chunk_position]:
                        return
                else:
                    return
        # Creacion de las tiles necesarias        
        for x in range(TILE_SIZE(tile_type)[0]):
            for y in range(TILE_SIZE(tile_type)[1]):
                if x==0 and y==0:
                    aux_tile_position_in_chunk=[tile_position_in_chunk[0]+x,tile_position_in_chunk[1]+y,1]
                    aux_tile_position_in_chunk_str=list2str3(aux_tile_position_in_chunk)
                    chunks[chunk_position][aux_tile_position_in_chunk_str]=Tile(position,tile_type,tilemap)
                else:
                    aux_tile_position_in_chunk=[tile_position_in_chunk[0]+x,tile_position_in_chunk[1]+y,1]
                    aux_tile_position_in_chunk_str=list2str3(aux_tile_position_in_chunk)
                    position[0]+=x
                    position[1]+=y
                    chunks[chunk_position][aux_tile_position_in_chunk_str]=Tile(position,-10,tilemap)
        
    
        
def upNeirbour(position,map_data):
    '''Devuelve el vecino de arriba en str'''
    #     Top
    position_top=list2str2([position[0],position[1]-1])
    if position_top in map_data:
        return str(map_data[position_top][2])
    else:
        return '-1'   
    
def neirbours4(position,map_data):  
    '''Position in form [x,y] Map in form of a dic of [x,y,type]
       Return format '0;0;0;0' '''
#     -1 para cuando no hay vecino
# Top;Down;Left;Right           tipo respectivo
    neirbours4=[-1,-1,-1,-1]
    
#     Top
    position_top=list2str2([position[0],position[1]-1])
    if position_top in map_data:
        neirbours4[0]=map_data[position_top][2]
#     Down
    position_down=list2str2([position[0],position[1]+1])
    if position_down in map_data:
        neirbours4[1]=map_data[position_down][2]
#     Left
    position_left=list2str2([position[0]-1,position[1]])
    if position_left in map_data:
        neirbours4[2]=map_data[position_left][2]
#     Right
    position_right=list2str2([position[0]+1,position[1]])
    if position_right in map_data:
        neirbours4[3]=map_data[position_right][2]

    return list2str4(neirbours4)

def neirbours9(position,map_data):  
    '''Position in form [x,y] Map in form of a dic of [x,y,type]
       Return format '0;0;0;0;0;0;0;0;0;' '''
#     -1 para cuando no hay vecino
# cornerTopLeft;Top;cornerTopRight;Left;center;Right;cornerDownLeft;Down;cornerDownRight      tipo respectivo
    neirbours8=[-1,-1,-1,-1,-1,-1,-1,-1,-1]
    
#     cornerTopLeft
    position_top=list2str2([position[0]-1,position[1]-1])
    if position_top in map_data:
        neirbours8[0]=map_data[position_top][2]
#     Top
    position_top=list2str2([position[0],position[1]-1])
    if position_top in map_data:
        neirbours8[1]=map_data[position_top][2]
#     cornerTopRight
    position_top=list2str2([position[0]+1,position[1]-1])
    if position_top in map_data:
        neirbours8[2]=map_data[position_top][2]
#     Left
    position_left=list2str2([position[0]-1,position[1]])
    if position_left in map_data:
        neirbours8[3]=map_data[position_left][2]
#     Center
    position_right=list2str2([position[0],position[1]])
    if position_right in map_data:
        neirbours8[4]=map_data[position_right][2]
#     Right
    position_right=list2str2([position[0]+1,position[1]])
    if position_right in map_data:
        neirbours8[5]=map_data[position_right][2]
#     cornerDownLeft
    position_down=list2str2([position[0]-1,position[1]+1])
    if position_down in map_data:
        neirbours8[6]=map_data[position_down][2]
#     Down
    position_down=list2str2([position[0],position[1]+1])
    if position_down in map_data:
        neirbours8[7]=map_data[position_down][2]
#     cornerDownRight
    position_down=list2str2([position[0]+1,position[1]+1])
    if position_down in map_data:
        neirbours8[8]=map_data[position_down][2]
        
    return list2str9(neirbours8)
    