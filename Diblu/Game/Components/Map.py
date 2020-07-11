import random,noise,time
from Game.Components.Tile import Tile, TILEMAP1
from utils import JSONParser,JSONsave,str2list3, list2str3, list2str2, str2list2,\
    list2str4
from Game.constants import CHUNK_SIZE, TILE_TYPES,\
    TILE_SIZE, TILE_SIZE_GENERAL, TILE_SIZE_GENERAL_PIXEL,\
    AUTO_TILE_TYPE, CAPAS
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
    
    def update(self,sprite_collisions_list):
        '''Actualiza la posicion de todas sus tile'''
        for key,tile in sorted(list(self.tiles.items()),key=lambda x:str2list3(x[0])[2]):
            
            tile.update()
            tile.camera_update()
            S_c().add_to_self_layer(tile)
            # check_collisions
            for sprite in sprite_collisions_list:
                tile.check_collision(sprite)
            
        for item in self.items:
            item.update()
            item.camera_update()
            S_c().add_to_self_layer(item)
            # check_collisions
            for sprite in sprite_collisions_list:
                item.check_collision(sprite)
            # check_items_collisions
            for tile in self.tiles.values():
                item.check_collision(tile)
            for item2 in self.items:   
                if item!=item2:
                    item.check_collision(item2) 
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
        global _instance
        _instance=self
        
        self.chunk_limit=10
        
        # Si esta true lo carga sino genera un mapa nuevo
        # Estructura de chunks es un dict 'x,y' del chunk con un dict de tiles
        if load:
            self.map_load('world')
        else:
            self.chunks={}
#             self.generate_map([CHUNK_SIZE[0]*self.size_square_in_chunk,CHUNK_SIZE[1]*self.size_square_in_chunk])
        
        
        
    def save(self,player_pos):
        '''Guarda el mapa'''
        self.map_save('world',player_pos)
        
    
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
        
        self.player_saved_pos=map_data['player_saved_pos']
        
        from Game.Components.Item import Item
        
        for chunk_key in map_data['chunks'].keys():
            chunks[chunk_key]={}
            for tile_key,tile_data in map_data['chunks'][chunk_key]['tiles'].items():
                tile_position=str2list3(tile_key)
                super_layer=tile_position[2]
                chunk_position=str2list2(chunk_key)
    #             Tile_position= pos dentro chunk + el chunk en el que esta * su tamaño
                tile_position=[tile_position[0]+chunk_position[0]*CHUNK_SIZE[0],tile_position[1]+chunk_position[1]*CHUNK_SIZE[1]]#,tile_position[2]]
#                 print(tile_data)
                if super_layer==0:
                    chunks[chunk_key][tile_key]=Tile(tile_position,tile_data,tilemap,0)
                else:
                    chunks[chunk_key][tile_key]=Tile(tile_position,tile_data,tilemap)
    #             sys.exit()
            chunks[chunk_key]=Chunk([chunk_key,chunks[chunk_key]])
            
            
        logging.info('Time consumed in load the map: '+str(time.time()-start_time)+' seconds')
    #     print('Time consumed in load the map:',time.time()-start_time,' seconds')
        self.chunks=chunks
        
        # Carga de los items
        for chunk_key in map_data['chunks'].keys():
            for item_dict in map_data['chunks'][chunk_key]['items']:
                Item([item_dict['x'],item_dict['y']],item_dict['item_type'],amount=item_dict['amount'])



    def map_save(self,name,player_pos):
        '''Guarda los chunks en el mapa name'''
        start_time=time.time()
        map_data={'name':'world','seed1':self.seed1,'seed2':self.seed2,'player_saved_pos':player_pos}
        
        chunks_data={}
        for chunk_item in self.chunks.items():
            chunks_data[chunk_item[0]]={}
            chunks_data[chunk_item[0]]['tiles']={}
            for tile_key,tile_data in self.chunks[chunk_item[0]].tiles.items():
                chunks_data[chunk_item[0]]['tiles'][tile_key]=tile_data.tile_type
                
            chunks_data[chunk_item[0]]['items']=[]    
            for item in self.chunks[chunk_item[0]].items:
                item_data_dict={'x':item.position_map[0],'y':item.position_map[1],'item_type':item.item_type,'amount':item.amount}
                chunks_data[chunk_item[0]]['items'].append(item_data_dict)
                
        
        
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
#         self.seed1=65
#         self.seed2=41
        if not hasattr(self, 'seed1'):
            self.seed1 = int(random.random()*100)
        if not hasattr(self, 'seed2'):
            self.seed2 = int(random.random()*100)
        
        # Extension de 1 para comprobar los bordes del chunk
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
                
                
                noise_at_xy=noise_at_xy1+noise_at_xy2/2
                
                
                # Reducion por los bordes del mapa para que sea como una gran isla
                border_chunks=3
                
                noise_reduct_x=0
                noise_reduct_y=0
                
                if x<-(self.chunk_limit*CHUNK_SIZE[0])+CHUNK_SIZE[0]*border_chunks\
                or x>(self.chunk_limit*CHUNK_SIZE[0])-CHUNK_SIZE[0]*border_chunks: 
                    noise_reduct_x=abs(abs(x)-((self.chunk_limit*CHUNK_SIZE[0])-CHUNK_SIZE[0]*border_chunks))
                    
                if y<-(self.chunk_limit*CHUNK_SIZE[1])+CHUNK_SIZE[1]*border_chunks\
                or y>(self.chunk_limit*CHUNK_SIZE[1])-CHUNK_SIZE[1]*border_chunks:
                    noise_reduct_y=abs(abs(y)-((self.chunk_limit*CHUNK_SIZE[1])-CHUNK_SIZE[1]*border_chunks))
                    
                noise_reduct=1.1**(noise_reduct_x+noise_reduct_y)
                noise_at_xy-=noise_reduct/100
                    
                    
                if noise_at_xy< -0.6:
                    # Agua oscura
                    tile_type=2
                elif noise_at_xy< -0.3:
                    # Agua orilla
                    tile_type=1
                elif noise_at_xy< -0.1:
                    # Arena
                    tile_type=3
                elif noise_at_xy< 0.3:
                    # Cesped
                    tile_type=0
                elif noise_at_xy< 0.85:
                    # Cesped elevado
                    tile_type=4
                else:
                    # Acua con cesped elevado
                    tile_type=5
    
                      
                aux_tiles_data[list2str2([x,y])]=[x,y,tile_type]
        
        
        
        self.auto_tile(aux_tiles_data)
        
        # Eliminacion del exceso
        for key in list(aux_tiles_data.keys()):
            key_list=str2list2(key)
            if key_list[0] not in range(chunk_pos[0],chunk_pos[0]+CHUNK_SIZE[0]) or key_list[1] not in range(chunk_pos[1],chunk_pos[1]+CHUNK_SIZE[1]):
                    aux_tiles_data.pop(key)
        
        # Vuelta a el tamaño del mapa
        map_size[0]-=1
        map_size[1]-=1
        
        
        chunks[chunk_key]={}
    
        for tile in aux_tiles_data.values():
                tile_position_in_chunk=[tile[0]%CHUNK_SIZE[0],tile[1]%CHUNK_SIZE[1],0]
                tile_position_in_chunk_str=list2str3(tile_position_in_chunk)
                tile_position=[tile[0],tile[1]]
                
                # Comprobar que no es parte de un big_tile
                if tile[2]!=-10:
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
                    elif tile[2]==0 or tile[2]==4:
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
                    elif tile[2]==3:
                        numero_random=random.randint(300,450)
                        if numero_random in TILE_TYPES:
                            if TILE_TYPES[numero_random][2]!=TILE_SIZE_GENERAL[0] or TILE_TYPES[numero_random][3]!=TILE_SIZE_GENERAL[1]:
                                
                                self.generate_chunk_big_tile(tile[:2],chunk_key,tile[2], numero_random, chunks, aux_tiles_data)
                                
                            else:
        #                         layer
                                tile_position_in_chunk[2]=1
                                tile_position_in_chunk_str=list2str3(tile_position_in_chunk)
                                chunks[chunk_key][tile_position_in_chunk_str]=Tile(tile_position,numero_random,tilemap)
                    #Detalles del agua alta
                    elif tile[2]==5:
                        numero_random=random.randint(500,525)
                        if numero_random in TILE_TYPES:
                            if TILE_TYPES[numero_random][2]!=TILE_SIZE_GENERAL[0] or TILE_TYPES[numero_random][3]!=TILE_SIZE_GENERAL[1]:
                                
                                self.generate_chunk_big_tile(tile[:2],chunk_key,tile[2], numero_random, chunks, aux_tiles_data)
                                
                            else:
        #                         layer
                                tile_position_in_chunk[2]=1
                                tile_position_in_chunk_str=list2str3(tile_position_in_chunk)
                                chunks[chunk_key][tile_position_in_chunk_str]=Tile(tile_position,numero_random,tilemap)
                                
                    
    #     Tercero creacion del chunk
        chunks[chunk_key]=Chunk([chunk_key,chunks[chunk_key]])
         
        logging.info('Time consumed in generate the chunk {}: {} seconds'.format(chunk_key,(time.time()-start_time)))     
        
        for aux_key,aux_chunk in chunks.items():
            self.chunks[aux_key]=aux_chunk
        

    def auto_tile(self,aux_tiles_data):
        '''Formato aux_tiles_data key='x;y', valor=[x,y,type]'''
        capas=CAPAS
        capas_dict={}
        
        # Relleno de capas segun el tipo
                    
        for i in range(len(capas)):
            capa=capas[i]
            
            aux_capa={}
            for aux_key,aux_value in aux_tiles_data.items():
                aux_capa[aux_key]=aux_value.copy()
            capas_dict[capa]=aux_capa
            
            for aux_key,aux_value in list(capas_dict[capa].items()):
                if capa==capas[0]:
                    aux_value[2]=capa
                else:
                    if aux_value[2] in capas[i:]:
                        aux_value[2]=capa
                    else:
                        capas_dict[capa].pop(aux_key)
                    
        
        # Rellenado de la capa default
        for aux_key,aux_value in list(aux_tiles_data.items()):
            aux_tiles_data[aux_key][2]=capas[0]
    
        # Calculo de AUTO-TILE-BORDERS si no existe ya
        if not hasattr(self, 'AUTO_TILE_BORDERS'):
            self.AUTO_TILE_BORDERS={}
            for key_value,value_value in AUTO_TILE_TYPE.items():
                self.AUTO_TILE_BORDERS[list2str4(value_value)]=key_value
        
        # Insertado de una a una cada capa
        for capa in capas:  
            for aux_key,aux_value in capas_dict[capa].items():
                self.auto_one_tile(capas_dict[capa][aux_key],aux_tiles_data)
                             
        return aux_tiles_data
    
    
    def auto_one_tile(self,tile_data,aux_tiles_data):
        '''Cambia los neirbours de un tile
        Tile_data [x,y,type] and aux_tiles_data es el dict del mapa'''
        tile_type=tile_data[2]
        tile_pos=[tile_data[0],tile_data[1]]
        tile_pos_key=list2str2(tile_pos)
        neirbours=neirbours9(tile_pos, aux_tiles_data)
        list_pos_neirbours=list(neirbours.keys())
             
        
        for indice in range(len(list_pos_neirbours)):
            
            if indice==4:
                # Centro
                aux_tiles_data[tile_pos_key][2]=tile_type
            else:
                # Vecinos
                key_pos=list_pos_neirbours[indice]
                aux_type_neirbour=neirbours[key_pos]
                # Cojo los bordes actuales del vecino
                aux_borders=AUTO_TILE_TYPE[aux_type_neirbour].copy()
                # Cambio los necesarios
                aux_auto_tile_type=AUTO_TILE_TYPE[tile_type]
                if indice==0:
                    aux_borders[3]=aux_auto_tile_type[0]
                elif indice==1:
                    aux_borders[2]=aux_auto_tile_type[0]
                    aux_borders[3]=aux_auto_tile_type[1]
                elif indice==2:
                    aux_borders[2]=aux_auto_tile_type[1]
                elif indice==3:
                    aux_borders[1]=aux_auto_tile_type[0]
                    aux_borders[3]=aux_auto_tile_type[2]
                elif indice==5:
                    aux_borders[0]=aux_auto_tile_type[1]
                    aux_borders[2]=aux_auto_tile_type[3]
                elif indice==6:
                    aux_borders[1]=aux_auto_tile_type[2]
                elif indice==7:
                    aux_borders[0]=aux_auto_tile_type[2]
                    aux_borders[1]=aux_auto_tile_type[3]
                elif indice==8:
                    aux_borders[0]=aux_auto_tile_type[3]
                # Con el cambio calculo el nuevo tipo
                key_auto_tile_borders=list2str4(aux_borders)
                if key_auto_tile_borders in self.AUTO_TILE_BORDERS:
#                 if not -1 in aux_borders:
                    aux_type_neirbour=self.AUTO_TILE_BORDERS[key_auto_tile_borders]
                    # Le cambio el tipo
                    if key_pos in aux_tiles_data:
                        aux_tiles_data[key_pos][2]=aux_type_neirbour
                     
       
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
                    

        
# def upNeirbour(position,map_data):
#     '''Devuelve el vecino de arriba en str'''
#     #     Top
#     position_top=list2str2([position[0],position[1]-1])
#     if position_top in map_data:
#         return str(map_data[position_top][2])
#     else:
#         return '-1'   
    
# def neirbours4(position,map_data):  
#     '''Position in form [x,y] Map in form of a dic of [x,y,type]
#        Return format '0;0;0;0' '''
# #     -1 para cuando no hay vecino
# # Top;Down;Left;Right           tipo respectivo
#     neirbours4=[-1,-1,-1,-1]
#     
# #     Top
#     position_top=list2str2([position[0],position[1]-1])
#     if position_top in map_data:
#         neirbours4[0]=map_data[position_top][2]
# #     Down
#     position_down=list2str2([position[0],position[1]+1])
#     if position_down in map_data:
#         neirbours4[1]=map_data[position_down][2]
# #     Left
#     position_left=list2str2([position[0]-1,position[1]])
#     if position_left in map_data:
#         neirbours4[2]=map_data[position_left][2]
# #     Right
#     position_right=list2str2([position[0]+1,position[1]])
#     if position_right in map_data:
#         neirbours4[3]=map_data[position_right][2]
# 
#     return list2str4(neirbours4)

def neirbours9(position,map_data):  
    '''Position in form [x,y] Map in form of a dic of [x,y,type]
       Return format '0;0;0;0;0;0;0;0;0;' '''
#     -1 para cuando no hay vecino
# cornerTopLeft;Top;cornerTopRight;Left;center;Right;cornerDownLeft;Down;cornerDownRight      tipo respectivo
#     neirbours9=[-1,-1,-1,-1,-1,-1,-1,-1,-1]
    neirbours9={}
#     cornerTopLeft
    position_top=list2str2([position[0]-1,position[1]-1])
    if position_top in map_data:
        neirbours9[position_top]=map_data[position_top][2]
    else:
        neirbours9[position_top]=-1
#     Top
    position_top=list2str2([position[0],position[1]-1])
    if position_top in map_data:
        neirbours9[position_top]=map_data[position_top][2]
    else:
        neirbours9[position_top]=-1
#     cornerTopRight
    position_top=list2str2([position[0]+1,position[1]-1])
    if position_top in map_data:
        neirbours9[position_top]=map_data[position_top][2]
    else:
        neirbours9[position_top]=-1
#     Left
    position_left=list2str2([position[0]-1,position[1]])
    if position_left in map_data:
        neirbours9[position_left]=map_data[position_left][2]
    else:
        neirbours9[position_left]=-1
#     Center
    position_right=list2str2([position[0],position[1]])
    if position_right in map_data:
        neirbours9[position_right]=map_data[position_right][2]
    else:
        neirbours9[position_right]=-1
#     Right
    position_right=list2str2([position[0]+1,position[1]])
    if position_right in map_data:
        neirbours9[position_right]=map_data[position_right][2]
    else:
        neirbours9[position_right]=-1
#     cornerDownLeft
    position_down=list2str2([position[0]-1,position[1]+1])
    if position_down in map_data:
        neirbours9[position_down]=map_data[position_down][2]
    else:
        neirbours9[position_down]=-1
#     Down
    position_down=list2str2([position[0],position[1]+1])
    if position_down in map_data:
        neirbours9[position_down]=map_data[position_down][2]
    else:
        neirbours9[position_down]=-1
#     cornerDownRight
    position_down=list2str2([position[0]+1,position[1]+1])
    if position_down in map_data:
        neirbours9[position_down]=map_data[position_down][2]
    else:
        neirbours9[position_down]=-1
        
    return neirbours9
    