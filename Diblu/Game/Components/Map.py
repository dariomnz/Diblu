import random,noise
from Game.Components.Tile import Tile,TileMap,Chunk,tile_size
from utils import JSONParser,JSONsave,str2list, list2str
from Game.constants import CHUNK_SIZE

class Map():
    
    def __init__(self,screen):
#         Estructura: 'x;y':{'x;y':tile}
        self.chunks=map_load('world.json', screen)
        self.size_square_in_chunk=16
#         self.chunks=generate_map([CHUNK_SIZE[0]*self.size_square_in_chunk,CHUNK_SIZE[0]*self.size_square_in_chunk],screen)
        
        
        
    def save(self):
        map_save(self.chunks, 'world.json')
        





def map_load(name,screen):
    tilemap = TileMap('tilemap1.gif')
    chunks={}
    map_data = JSONParser(name)
    
    
    for chunk_data in map_data['chunks'].items():
        chunks[chunk_data[0]]={}
        for tile_data in map_data['chunks'][chunk_data[0]].items():
            tile_position=str2list(tile_data[0])
            chunk_position=str2list(chunk_data[0])
#             Tile_position= pos dentro chunk + el chunk en el que esta * su tamaño
            tile_position=[tile_position[0]+chunk_position[0]*CHUNK_SIZE[0],tile_position[1]+chunk_position[1]*CHUNK_SIZE[1]]

            chunks[chunk_data[0]][tile_data[0]]=Tile(tile_position,tile_data[1],tilemap,screen)
        chunks[chunk_data[0]]=Chunk([chunk_data[0],chunks[chunk_data[0]]])

    return chunks



def map_save(chunks,name):
    map_data={'name':'world'}

    chunks_data={}
    for chunk_item in chunks.items():
        chunks_data[chunk_item[0]]={}
        for tile_data in chunks[chunk_item[0]].tiles.items():
            chunks_data[chunk_item[0]][tile_data[0]]=tile_data[1].tile_type

    map_data['chunks']=chunks_data
    
    JSONsave(name, map_data)
    
    
    
    
def generate_map(map_size,screen):
    '''map_size is the number or tiles [tiles_w,tiles_h], it must be multiple of 16'''
    if map_size[0]%16!=0 or map_size[1]%16!=0:
        print('Generacion de mapa incorrecta,map_size tiene que ser multiplo de 16')
        return None
    
    map_size=[map_size[0]//2,map_size[1]//2]
    tilemap = TileMap('tilemap1.gif')
    chunks={}
    aux_tiles_data=[]
#     size=10
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
                tile_type=0
#             elif noise_at_xy< 0.20:
#                 tile_type=0
            else:
                tile_type=1
            print('noise at: X',x,' Y: ',y,'noise: ',noise_at_xy)   
            aux_tiles_data.append([x,y,tile_type])
                
#     Primero cracion de chunks vacions en el dict chunks
    for x in range(-map_size[0]//CHUNK_SIZE[0],map_size[0]//CHUNK_SIZE[0]):
        for y in range(-map_size[1]//CHUNK_SIZE[1],map_size[1]//CHUNK_SIZE[1]):
            chunk_position=list2str([x,y])
            chunks[chunk_position]={'0;0':None}

#     Segundo creacion de los tile de cada chunk guardados en un dict
    for tile in aux_tiles_data:
        tile_position_in_chunk=[tile[0]%CHUNK_SIZE[0],tile[1]%CHUNK_SIZE[1]]
        tile_position_in_chunk_str=list2str(tile_position_in_chunk)
        tile_position=[tile[0],tile[1]]
        chunk_position=list2str([tile[0]//8,tile[1]//8])
        chunks[chunk_position][tile_position_in_chunk_str]=Tile(tile_position,tile[2],tilemap,screen)
            
#     Tercero creacion de los chunks
    for x in range(-map_size[0]//CHUNK_SIZE[0],map_size[0]//CHUNK_SIZE[0]):
        for y in range(-map_size[1]//CHUNK_SIZE[1],map_size[1]//CHUNK_SIZE[1]):
            chunk_position=list2str([x,y])
            chunks[chunk_position]=Chunk([chunk_position,chunks[chunk_position]])
            
    return chunks

        