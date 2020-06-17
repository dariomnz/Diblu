import random,noise,time
from Game.Components.Tile import Tile,TileMap,Chunk
from utils import JSONParser,JSONsave,str2list3, list2str3, list2str2, str2list2,\
    list2str4, list2str9
from Game.constants import CHUNK_SIZE, TILE_TYPES, TILEMAP1_NAME,\
    TILE_TYPES_4NEIGHBOUR_FIX,\
    TILE_TYPES_9NEIGHBOUR1, TILE_TYPES_9NEIGHBOUR2, TILE_TYPES_UPNEIGHBOUR,\
    TILE_SIZE


class Map():
    
    def __init__(self,load=True):
        self.size_square_in_chunk=8
        # Si esta true lo carga sino genera un mapa nuevo
        # Estructura de chunks es un dict 'x,y' del chunk con un dict de tiles
        if load:
            self.chunks=map_load('world')
        else:
            self.chunks=generate_map([CHUNK_SIZE[0]*self.size_square_in_chunk,CHUNK_SIZE[0]*self.size_square_in_chunk])
        
        
    def save(self):
        '''Guarda el mapa'''
        map_save(self.chunks, 'world')
        

def map_load(name):
    '''Carga el mapa name'''
    start_time=time.time()
    tilemap = TileMap(TILEMAP1_NAME)
    chunks={}
    map_data = JSONParser(name)
    
    
    for chunk_data in map_data['chunks'].items():
        chunks[chunk_data[0]]={}
        for tile_data in map_data['chunks'][chunk_data[0]].items():
            tile_position=str2list3(tile_data[0])
            chunk_position=str2list2(chunk_data[0])
#             Tile_position= pos dentro chunk + el chunk en el que esta * su tamaño
            tile_position=[tile_position[0]+chunk_position[0]*CHUNK_SIZE[0],tile_position[1]+chunk_position[1]*CHUNK_SIZE[1],tile_position[2]]

            chunks[chunk_data[0]][tile_data[0]]=Tile(tile_position[:2],tile_position[2],tile_data[1],tilemap)
        chunks[chunk_data[0]]=Chunk([chunk_data[0],chunks[chunk_data[0]]])
    print('Time consumed in load the map:',time.time()-start_time,' seconds')
    return chunks



def map_save(chunks,name):
    '''Guarda los chunks en el mapa name'''
    start_time=time.time()
    map_data={'name':'world'}

    chunks_data={}
    for chunk_item in chunks.items():
        chunks_data[chunk_item[0]]={}
        for tile_data in chunks[chunk_item[0]].tiles.items():
            chunks_data[chunk_item[0]][tile_data[0]]=tile_data[1].tile_type

    map_data['chunks']=chunks_data
    
    JSONsave(name, map_data)
    print('Time consumed in save the map:',time.time()-start_time,' seconds')
    
    
    
    
def generate_map(map_size):
    '''map_size is the number or tiles [tiles_w,tiles_h], it must be multiple of 16'''
    if map_size[0]%16!=0 or map_size[1]%16!=0:
        print('Generacion de mapa incorrecta,map_size tiene que ser multiplo de 16')
        return None
    
    start_time=time.time()
    map_size=[map_size[0]//2,map_size[1]//2]
    tilemap = TileMap(TILEMAP1_NAME)
    chunks={}
    aux_tiles_data={}
    scale = 25
    octaves = 4
    persistence = 0.5
    lacunarity = 1.0
    random.seed()
    seed = int(random.random()*100)
    
    for x in range(-map_size[0],map_size[0]):
        for y in range(-map_size[1],map_size[1]):
            noise_at_xy=noise.pnoise2(x/scale,
                                            y/scale,
                                            octaves=octaves,
                                            persistence=persistence,
                                            lacunarity=lacunarity,
                                            repeatx=map_size[0],
                                            repeaty=map_size[1],
                                            base=seed)
            if noise_at_xy< 0.1:
                # Cesped
                tile_type=0
            else:
                # Agua
                tile_type=1
                  
            aux_tiles_data[list2str2([x,y])]=[x,y,tile_type]
    
    
    
    aux_tiles_data=adapt_borders(aux_tiles_data)
    
#     Primero cracion de chunks vacions en el dict chunks
    for x in range(-map_size[0]//CHUNK_SIZE[0],map_size[0]//CHUNK_SIZE[0]):
        for y in range(-map_size[1]//CHUNK_SIZE[1],map_size[1]//CHUNK_SIZE[1]):
            chunk_position=list2str2([x,y])
            chunks[chunk_position]={}

#     Segundo creacion de los tile de cada chunk guardados en un dict
    for tile in aux_tiles_data.values():
        tile_position_in_chunk=[tile[0]%CHUNK_SIZE[0],tile[1]%CHUNK_SIZE[1],0]
        tile_position_in_chunk_str=list2str3(tile_position_in_chunk)
        tile_position=[tile[0],tile[1]]
        chunk_position=list2str2([tile[0]//8,tile[1]//8])
        if tile[2]!=-10:
            chunks[chunk_position][tile_position_in_chunk_str]=Tile(tile_position,0,tile[2],tilemap)
        
        #Anadido de detalles en la layer 1

        tile_position_in_chunk[2]=1
        tile_position_in_chunk_str=list2str3(tile_position_in_chunk)
        if tile_position_in_chunk_str not in chunks[chunk_position]:
            #Detalles del agua
            if tile[2]==1:
                numero_random=random.randint(100,150)
                if numero_random in TILE_TYPES:
                    if numero_random==104:
                        
                        generate_big_tile(tile[:2],tile[2], numero_random, chunks, aux_tiles_data)

                    else:
                        #layer
                        tile_position_in_chunk[2]=1
                        tile_position_in_chunk_str=list2str3(tile_position_in_chunk)
                        chunks[chunk_position][tile_position_in_chunk_str]=Tile(tile_position,1,numero_random,tilemap)
            #Detalles del cesped
            elif tile[2]==0:
                numero_random=random.randint(200,280)
                if numero_random in TILE_TYPES:
                    if numero_random in [213,214,215,216]:
                        
                        generate_big_tile(tile[:2],tile[2], numero_random, chunks, aux_tiles_data)
                        
                    else:
#                         layer
                        tile_position_in_chunk[2]=1
                        tile_position_in_chunk_str=list2str3(tile_position_in_chunk)
                        chunks[chunk_position][tile_position_in_chunk_str]=Tile(tile_position,1,numero_random,tilemap)
#     Tercero creacion de los chunks
    for x in range(-map_size[0]//CHUNK_SIZE[0],map_size[0]//CHUNK_SIZE[0]):
        for y in range(-map_size[1]//CHUNK_SIZE[1],map_size[1]//CHUNK_SIZE[1]):
            chunk_position=list2str2([x,y])
            chunks[chunk_position]=Chunk([chunk_position,chunks[chunk_position]])
            
    print('Time consumed in generate the map:',time.time()-start_time,' seconds')
    return chunks

def adapt_borders(aux_tiles_data):
    #Aux_tiles_data siempre va a ser de 1 o 0, es en change_data cuando se actualizan a los bordes
    
    #Primera pasada para quitar las salidas de 1 solo de agua, sobre la original
    for aux_tiles_data_key,aux_tiles_data_item in aux_tiles_data.items():
        key_tile_tipe_neirbours=neirbours9([aux_tiles_data_item[0],aux_tiles_data_item[1]],aux_tiles_data)
        if key_tile_tipe_neirbours in TILE_TYPES_9NEIGHBOUR1:
            aux_tiles_data[aux_tiles_data_key]=[aux_tiles_data_item[0],aux_tiles_data_item[1],TILE_TYPES_9NEIGHBOUR1[key_tile_tipe_neirbours]]
    
    #Genero una copia para no reescribir aux_tiles_data
    change_data=aux_tiles_data.copy()
    
    #Segunda pasada para los bordes principales
    for change_data_key,change_data_item in aux_tiles_data.items():
        key_tile_tipe_neirbours=neirbours9([change_data_item[0],change_data_item[1]],aux_tiles_data)
        if key_tile_tipe_neirbours in TILE_TYPES_9NEIGHBOUR2:
            change_data[change_data_key]=[change_data_item[0],change_data_item[1],TILE_TYPES_9NEIGHBOUR2[key_tile_tipe_neirbours]]
     
    #Tercera para poner la parte de abajo de los bordes de arriba
    for change_data_key,change_data_item in change_data.items():
        key_tile_tipe_neirbours=upNeirbour([change_data_item[0],change_data_item[1]],change_data)
        if key_tile_tipe_neirbours in TILE_TYPES_UPNEIGHBOUR:
            change_data[change_data_key]=[change_data_item[0],change_data_item[1],TILE_TYPES_UPNEIGHBOUR[key_tile_tipe_neirbours]]
     
    #Cuarta pasada para realizar el arreglo de unas texturas    
    for change_data_key,change_data_item in change_data.items():
        key_tile_tipe_neirbours=neirbours4([change_data_item[0],change_data_item[1]],change_data)
        if key_tile_tipe_neirbours in TILE_TYPES_4NEIGHBOUR_FIX:
            change_data[change_data_key]=[change_data_item[0],change_data_item[1],TILE_TYPES_4NEIGHBOUR_FIX[key_tile_tipe_neirbours]]
     
    return change_data
   
def generate_big_tile(position,parent_tile_type,tile_type,chunks,map_data):
    '''Encargado de poner tiles que ocupen mas de 1 tile
        position=[x,y]
        parent_tile_type= tipo de tile del suelo
        tile_type= tipo de tile actual
        tiles_size=[w,h] en tiles
        chunks es dict de datos
        map_data dict de 'x;y':[x,y,type]'''
    
    tilemap = TileMap(TILEMAP1_NAME)
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
                chunks[chunk_position][aux_tile_position_in_chunk_str]=Tile(position,1,tile_type,tilemap)
            else:
                aux_tile_position_in_chunk=[tile_position_in_chunk[0]+x,tile_position_in_chunk[1]+y,1]
                aux_tile_position_in_chunk_str=list2str3(aux_tile_position_in_chunk)
                position[0]+=x
                position[1]+=y
                chunks[chunk_position][aux_tile_position_in_chunk_str]=Tile(position,1,-10,tilemap)
    
    
        
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
    