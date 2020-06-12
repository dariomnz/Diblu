
# Pixels iniciales
TILE_SIZE_GENERAL=(16,16)
# Pixels en pantalla
TILE_SIZE_GENERAL_PIXEL=(32,32)
# Tiles
CHUNK_SIZE=(8,8)
# Respecto al tipo de tile, su posicion en el tilemap 0,1 y su tamaño 2,3
TILE_TYPES = {
    #Terreno cesped
    0:[0,0,16,16],
    #Terreno agua
    1:[16,0,16,16],
    #Terreno top_left cesped-agua
    2:[0,16,16,16],
    #Terreno top cesped-agua
    3:[16,16,16,16],
    #Terreno top-right cesped-agua
    4:[32,16,16,16],
    #Terreno left cesped-agua
    5:[0,32,16,16],
    #Terreno down of top cesped-agua
    6:[16,32,16,16],
    #Terreno right cesped-agua
    7:[32,32,16,16],
    
    #Burbujas
    100:[0,96,16,16],
    #Nenufares pequeños
    101:[16,96,16,16],
    #Nenufares grandes
    102:[32,96,16,16],
    #Roca pequeña acuatica
    103:[48,96,16,16]
    
    }
# Respecto a los tipos de vecino el tipo de tile correspondiente
# Top;Down;Left;Right
TILE_TYPES_NEIGHBOUR = {
    '0;5;3;0':2,
    '0;6;2;3':3,
    '0;7;3;0':4
    }