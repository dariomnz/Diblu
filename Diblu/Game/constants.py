
# Tilemap1
TILEMAP1_NAME='tilemap1.png'
# Pixels iniciales
TILE_SIZE_GENERAL=(16,16)
# Pixels en pantalla
TILE_SIZE_GENERAL_PIXEL=(32,32)
# Tiles
CHUNK_SIZE=(8,8)
# Respecto al tipo de tile, su posicion en el tilemap 0,1 y su tamaño 2,3
TILE_TYPES = {
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
    #104:[0,192,32,32]
    
    }

# Respecto a los tipos de vecino el tipo de tile correspondiente con 4 vecinos
# Top;Down;Left;Right           tipo respectivo
#La generacion funciona de izquierda a derecha y de arriba a abajo
TILE_TYPES_4NEIGHBOUR = {
    #Para abajo
    '0;8;0;8':2,
    '0;8;0;1':2,
    '0;1;0;8':2,
    
    '0;1;3;-1':3,
    '0;1;-1;1':3,
    '0;1;2;1':3,
    '0;1;3;1':3,
    '0;1;3;8':3,
    '0;1;9;1':3,
    '0;1;2;8':3,
    '0;1;8;8':3,

    '0;9;3;0':4,
    '0;9;9;0':4,
    '0;1;3;0':4,
    '0;1;9;0':4,
    
    '2;1;0;1':5,
    '2;8;0;1':5,
    '14;1;0;1':5,
    '14;8;0;1':5,
      
    '3;1;6;-1':6,
    '3;1;5;1':6,
    '3;1;6;1':6,
    '3;1;8;1':6,
    '3;1;11;1':6,
    '3;1;5;9':6,
    '3;1;6;9':6,
    '3;1;8;9':6,
    '3;1;11;9':6,
      
    '4;1;6;0':7,
    '4;1;11;0':7,
    '4;9;6;0':7,
    '4;9;11;0':7,
     
    '8;1;5;1':10,
    '8;1;6;1':10,
    '8;1;8;1':10,
      
    '9;1;1;1':11,
    '9;1;1;9':11,
    
    '9;15;1;1':11,
      
    '-1;1;0;1':12,
    '-1;8;0;1':12,
    '5;1;0;1':12,
    '12;1;0;1':12,
    '14;1;0;1':12,
    '5;8;0;1':12,
    '12;8;0;1':12,
    '14;8;0;1':12,
      
    '-1;1;1;0':13,
    '-1;9;1;0':13,
    '7;1;1;0':13,
    '13;1;1;0':13,
    '15;1;1;0':13,
    '7;9;1;0':13,
    '13;9;1;0':13,
    '15;9;1;0':13,

    '5;0;0;1':16,
    '12;0;0;1':16,
    '14;0;0;1':16,
    '5;0;0;14':16,
    '12;0;0;14':16,
    '14;0;0;14':16,
      
    '1;0;17;-1':17,
    '1;0;-1;1':17,
    '1;0;15;1':17,
    '1;0;16;1':17,
    '1;0;17;1':17,
    '1;0;15;14':17,
    '1;0;16;14':17,
    '1;0;17;14':17,
    
    '4;0;15;0':18,
    '4;0;16;0':18,
    '4;0;17;0':18,
    '7;0;15;0':18,
    '7;0;16;0':18,
    '7;0;17;0':18,
    '13;0;15;0':18,
    '13;0;16;0':18,
    '13;0;17;0':18,
    '15;0;15;0':18,
    '15;0;16;0':18,
    '15;0;17;0':18,
    }


# Respecto a los tipos de vecino el tipo de tile correspondiente con 4 vecinos
# Sirve para arreglar algun error grafico
# Top;Down;Left;Right           tipo respectivo
#La generacion funciona de izquierda a derecha y de arriba a abajo
TILE_TYPES_4NEIGHBOUR_FIX={
    '2;10;2;6':19,
    '2;10;3;6':19,
    '2;10;2;10':19,
    '2;10;3;10':19,
    
    '4;11;6;3':20,
    '4;11;6;4':20,
    '4;11;11;3':20,
    '4;11;11;4':20,
    }



# Respecto a los tipos de vecino el tipo de tile correspondiente con 8 vecinos
# cornerTopLeft;Top;cornerTopRight;Left;Right;cornerDownLeft;Down;cornerDownRight      tipo respectivo
#La generacion funciona de izquierda a derecha y de arriba a abajo
TILE_TYPES_8NEIGHBOUR = {
    #Para abajo
    
    #Para quitar entradas de 1
    '1;1;1;0;0;0;0;0':0,
    '0;0;0;0;0;1;1;1':0,
    '1;0;0;1;0;1;0;0':0,
    '0;0;1;0;1;0;0;1':0,
    
    '0;0;0;0;1;1;1;1':2,
    '0;0;0;0;1;0;1;1':2,
    '0;0;1;0;1;0;1;1':2,
    
    '0;1;1;1;1;1;1;1':8,
    '0;1;1;1;1;8;1;1':8,
    '0;1;1;2;1;1;1;1':8,
    '0;1;1;2;1;8;1;1':8,
    '0;2;1;1;1;1;1;1':8,
    '0;2;1;1;1;8;1;1':8,
    '0;12;1;2;1;12;1;1':8,
    
    '1;1;0;1;1;1;1;1':9,
    '9;1;0;1;1;1;1;1':9,
    
    '1;1;1;1;1;0;1;1':14,
    '2;8;1;1;1;0;1;1':14,
    '14;1;1;1;1;0;1;1':14,
    
    '1;1;1;1;1;1;1;0':15,
    '1;1;1;1;1;15;1;0':15,
    '1;1;1;14;1;1;1;0':15,
    '1;9;1;1;1;1;1;0':15,
    '1;9;1;1;1;15;1;0':15,
    
    
    '9;1;1;1;1;1;1;0':15,
    '8;1;1;1;1;0;1;1':14,
    }





