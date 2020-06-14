
#TPS
TPS=60

# Tilemap1
TILEMAP1_NAME='tilemap1'
# Pixels iniciales
TILE_SIZE_GENERAL=(16,16)
# Pixels en pantalla
TILE_SIZE_GENERAL_PIXEL=(48,48)
# Tiles
CHUNK_SIZE=(8,8)
# Respecto al tipo de tile, su posicion en el tilemap 0,1 y su tamaño 2,3
TILE_TYPES = {
    #vacio
    -10:[0,16,16,16],
    #Terreno cesped -.|
    0:[0,0,16,16],
    #Terreno agua ~~~
    1:[16,0,16,16],
    #top-left cesped-agua   #top cesped-agua   #top-right cesped-agua
    #        .--                ---                --.
    #        |~~                ###                ~~|
    #        |~~                ###                ~~|
    2:[16,16,16,16],    3:[32,16,16,16],    4:[48,16,16,16],
    #left-rock cesped-agua  #down of top cesped-agua #right-rock cesped-agua
    #        |##                ###                ##|
    #        |##                ###                ##|
    #        |~~                ~~~                ~~|
    5:[16,32,16,16],    6:[32,32,16,16],    7:[48,32,16,16],
    #down-right cesped-agua                #down-left cesped-agua
    #        -|~                                   ~|-
    #        -.~                                   ~.-
    #        ~~~                                   ~~~
    8:[16,48,16,16],                        9:[48,48,16,16],
    #down of down-right cesped-agua     #down of down-left cesped-agua
    #        ##~                                   ~##
    #        ##~                                   ~##
    #        ~~~                                   ~~~
    10:[16,64,16,16],                        11:[48,64,16,16],
    #left cesped-agua                      #right cesped-agua
    #        |~~                                   ~~|
    #        |~~                                   ~~|
    #        |~~                                   ~~|
    12:[0,80,16,16],                        13:[64,80,16,16],
    #up-right cesped-agua                #up-left cesped-agua
    #        ~~~                                   ~~~
    #        -.~                                   ~.-
    #        -|~                                   ~|-
    14:[16,96,16,16],                        15:[48,96,16,16],
    #down-left cesped-agua   #down cesped-agua   #down-right cesped-agua
    #        |~~                ~~~                ~~|
    #        |~~                ~~~                ~~|
    #        .--                ---                --.
    16:[16,112,16,16],   17:[32,112,16,16],   18:[48,112,16,16],  

    #arreglo grafico de 8               #arreglo grafico de 9
    19:[0,32,16,16],                        20:[64,32,16,16],
    #arreglo grafico de 14               #arreglo grafico de 15
    21:[0,112,16,16],                        22:[64,112,16,16],
    
#Decoracion del agua
    #Burbujas
    100:[0,176,16,16],
    #Nenufares pequeños
    101:[16,176,16,16],
    #Nenufares grandes
    102:[32,176,16,16],
    #Roca pequeña acuatica
    103:[48,176,16,16],
    #Roca grande acuatica
    104:[0,192,32,32]
    
    }




# Respecto a los tipos de vecino el tipo de tile correspondiente con 4 vecinos
# Top;Down;Left;Right           tipo respectivo
#La generacion funciona de izquierda a derecha y de arriba a abajo
TILE_TYPES_4NEIGHBOUR_FIX={
# Sirve para arreglar algun error grafico
    '2;8;0;6':5,
    '2;8;0;10':5,
    '2;12;0;6':5,
    '2;12;0;10':5,
    '2;8;0;9':5,
    '2;12;0;9':5,
    '2;16;0;6':5,
    '2;16;0;10':5,
    '2;16;0;9':5,

    
    '4;9;6;0':7,
    '4;9;11;0':7,
    '4;13;6;0':7,
    '4;13;11;0':7,
    '4;18;6;0':7,
    '4;18;11;0':7,
    
    '8;12;16;1':21,
    '8;12;17;1':21,
    '8;16;16;1':21,
    '8;16;17;1':21,
    
    '9;13;1;17':22,
    '9;13;1;18':22,
    '9;18;1;17':22,
    '9;18;1;18':22,
    
    '2;10;2;6':19,
    '2;10;3;6':19,
    '2;10;2;10':19,
    '2;10;3;10':19,
    
    '2;10;2;9':19,
    '2;10;3;9':19,
    
    '4;11;6;3':20,
    '4;11;6;4':20,
    '4;11;11;3':20,
    '4;11;11;4':20,
    
    '4;11;19;3':20,
    '4;11;19;4':20,
    '4;11;5;3':20,
    '4;11;5;4':20,
    '4;11;8;3':20,
    '4;11;8;4':20,
    }



# Respecto a los tipos de vecino el tipo de tile correspondiente con 8 vecinos y el central
# cornerTopLeft;Top;cornerTopRight;Left;center;Right;cornerDownLeft;Down;cornerDownRight      tipo respectivo
#La generacion funciona de izquierda a derecha y de arriba a abajo
TILE_TYPES_9NEIGHBOUR1 = {
    #Para abajo
    
    #Para quitar entradas de 1
    '1;1;1;0;1;0;0;0;0':0,
    '0;0;0;0;1;0;1;1;1':0,
    '1;0;0;1;1;0;1;0;0':0,
    '0;0;1;0;1;1;0;0;1':0,
    }


TILE_TYPES_9NEIGHBOUR2 = {
    #Para poner bordes
    '0;0;0;0;1;1;0;1;1':2,
    '0;0;0;0;1;1;1;1;1':2,
    '0;0;1;0;1;1;1;1;1':2,
    '0;0;1;0;1;1;0;1;1':2,
    
    '0;0;0;1;1;1;1;1;1':3,
    '0;0;1;1;1;1;1;1;1':3,
    '1;0;0;1;1;1;1;1;1':3,
    '1;0;1;1;1;1;1;1;1':3,
    
    '0;0;0;1;1;0;1;1;0':4,
    '0;0;0;1;1;0;1;1;1':4,
    '1;0;0;1;1;0;1;1;1':4,
    '1;0;0;1;1;0;1;1;0':4,
    
    '0;1;1;1;1;1;1;1;1':8,

    '1;1;0;1;1;1;1;1;1':9,
    
    '0;1;1;0;1;1;0;1;1':12,
    '1;1;1;0;1;1;0;1;1':12,
    '0;1;1;0;1;1;1;1;1':12,
    '1;1;1;0;1;1;1;1;1':12,
    
    '1;1;0;1;1;0;1;1;0':13,
    '1;1;1;1;1;0;1;1;0':13,
    '1;1;0;1;1;0;1;1;1':13,
    '1;1;1;1;1;0;1;1;1':13,
    
    '1;1;1;1;1;1;0;1;1':14,
    
    '1;1;1;1;1;1;1;1;0':15,
    
    '0;1;1;0;1;1;0;0;0':16,
    '1;1;1;0;1;1;0;0;0':16,
    '1;1;1;0;1;1;0;0;1':16,
    '0;1;1;0;1;1;0;0;1':16,
    
    '1;1;1;1;1;1;0;0;0':17,
    '1;1;1;1;1;1;1;0;0':17,
    '1;1;1;1;1;1;0;0;1':17,
    '1;1;1;1;1;1;1;0;1':17,
    
    '1;1;0;1;1;0;0;0;0':18,
    '1;1;1;1;1;0;0;0;0':18,
    '1;1;1;1;1;0;1;0;0':18,
    '1;1;0;1;1;0;1;0;0':18
    }


TILE_TYPES_UPNEIGHBOUR = {
    #Para los bordes inferiores
    '3':6,
    '8':10,
    '9':11
    }

CURSOR_CROSS = ( "                        ",
                 "    XXXXXX    XXXXXX    ",
                 "   X......X  X......X   ",
                 "  XX......X  X......XX  ",
                 " X..XXXXXX    XXXXXX..X ",
                 " X..X              X..X ",
                 " X..X              X..X ",
                 " X..X              X..X ",
                 " X..X      XX      X..X ",
                 " X..X     X..X     X..X ",
                 "  XX     XX..XX     XX  ",
                 "        X..,...X        ",#Mitad
                 "        X......X        ",#
                 "  XX     XX..XX     XX  ",
                 " X..X     X..X     X..X ",
                 " X..X      XX      X..X ",
                 " X..X              X..X ",
                 " X..X              X..X ",
                 " X..X              X..X ",
                 " X..XXXXXX    XXXXXX..X ",
                 "  XX......X  X......XX  ",
                 "   X......X  X......X   ",
                 "    XXXXXX    XXXXXX    ",
                 "                        ")



