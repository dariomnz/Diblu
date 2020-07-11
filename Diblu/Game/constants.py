
#TPS
TPS=60

# ImageSheet1
ITEMSSHEET1_NAME='itemssheet1'

# Respecto al tipo de item, su posicion en el itemsheet 0,1 y su tama�o 2,3
ITEMS_TYPE={
    'wood_log':[96,96,16,16],
    'leaf':[64,128,16,16],
    'rock':[64,112,16,16],
    'iron_ingot':[64,96,16,16],
    
    }


# Tilemap1
TILEMAP1_NAME='tilemap1'
# Pixels iniciales
TILE_SIZE_GENERAL=(16,16)
# Pixels en pantalla
TILE_SIZE_GENERAL_PIXEL=(48,48)
# Escala de las imagenes
DEFAULT_SCALE=3
# Escala de los items
ITEMS_SCALE=2
# Tiles
CHUNK_SIZE=(16,16)

# Capas de los tipos de tile principal para generar el mapa
CAPAS=[5,4,0,3,1,2]
# Respecto al tipo de tile, su posicion en el tilemap 0,1 y su tama�o 2,3
TILE_TYPES = {
    #vacio
    -10:[0,0,0,0],
    #Terreno cesped -.|
    0:[0,0,16,16],
    #Terreno cesped elevado
    4:[64,0,16,16],
    #Terreno agua con cesped elevado
    5:[80,0,16,16],
    #Terreno agua orilla ~~~
    1:[16,0,16,16],
    #Terreno agua oscura ~~~
    2:[32,0,16,16],
    #Terreno arena
    3:[48,0,16,16],
    
      
    # Union cesped-arena
    11:[0,16,16,16],   12:[16,16,16,16],   13:[32,16,16,16],
    14:[0,32,16,16],                       15:[32,32,16,16],
    16:[0,48,16,16],   17:[16,48,16,16],   18:[32,48,16,16], 
    
    19:[48,16,16,16],    20:[64,16,16,16],
    21:[48,32,16,16],    22:[64,32,16,16],
    23:[48,48,16,16],    24:[64,48,16,16],
    
      
    # Union arena-agua
    25:[0,64,16,16],   26:[16,64,16,16],   27:[32,64,16,16],
    28:[0,80,16,16],                       29:[32,80,16,16],
    30:[0,96,16,16],   31:[16,96,16,16],   32:[32,96,16,16], 
    
    33:[48,64,16,16],    34:[64,64,16,16],
    35:[48,80,16,16],    36:[64,80,16,16],
    37:[48,96,16,16],    38:[64,96,16,16],
    
      
    # Union agua orilla-agua oscura
    39:[0,112,16,16],   40:[16,112,16,16],   41:[32,112,16,16],
    42:[0,128,16,16],                        43:[32,128,16,16],
    44:[0,144,16,16],   45:[16,144,16,16],   46:[32,144,16,16], 
    
    47:[48,112,16,16],    48:[64,112,16,16],
    49:[48,128,16,16],    50:[64,128,16,16],
    51:[48,144,16,16],    52:[64,144,16,16],
    
    # Union cesped elevado-cesped
    53:[80,16,16,16],   54:[96,16,16,16],   55:[112,16,16,16],
    56:[80,32,16,16],                       57:[112,32,16,16],
    58:[80,48,16,16],   59:[96,48,16,16],   60:[112,48,16,16], 
    
    61:[128,16,16,16],    62:[144,16,16,16],
    63:[128,32,16,16],    64:[144,32,16,16],
    65:[128,48,16,16],    66:[144,48,16,16],
    
    # Union agua - cesped elevado
    67:[80,64,16,16],   68:[96,64,16,16],   69:[112,64,16,16],
    70:[80,80,16,16],                       71:[112,80,16,16],
    72:[80,96,16,16],   73:[96,96,16,16],   74:[112,96,16,16], 
    
    75:[128,64,16,16],    76:[144,64,16,16],
    77:[128,80,16,16],    78:[144,80,16,16],
    79:[128,96,16,16],    80:[144,96,16,16],
    
    
    
 
#     #arreglo grafico de 8               #arreglo grafico de 9
#     19:[0,32,16,16],                        20:[64,32,16,16],
#     #arreglo grafico de 14               #arreglo grafico de 15
#     21:[0,112,16,16],                        22:[64,112,16,16],
#      
#     #Bordes de arena con cesped
#     24:[96,16,16,16],   25:[112,16,16,16],   26:[128,16,16,16], 
#     27:[96,32,16,16],                         28:[128,32,16,16],
#     29:[96,48,16,16],                         30:[128,48,16,16],
#     31:[80,80,16,16],                         34:[144,80,16,16],
#     32:[96,80,16,16],   35:[112,112,16,16],   33:[128,80,16,16], 
     
     
     
     
#Decoracion del agua
    #Burbujas
    100:[0,176,16,16],
    #Nenufares peque�os
    101:[16,176,16,16],
    #Nenufares grandes
    102:[32,176,16,16],
#     #Roca peque�a acuatica
#     103:[48,176,16,16],
#     #Roca grande acuatica
#     104:[0,192,32,32],
     
     
#Decoracion del cesped
    #Hierba 1
    200:[64,176,16,16],
    #Hierba 2
    201:[80,176,16,16],
    #Hierba 3
    202:[96,176,16,16],
    #Hierba 4
    203:[112,176,16,16],
    #Hierba 5
    204:[128,176,16,16],
    #Hierba 6
    205:[64,192,16,16],
    #Hierba 7
    206:[80,192,16,16],
    #Hierba 8
    207:[96,192,16,16],
    #Hierba 9
    208:[112,192,16,16],
    #Hierba 10
    209:[128,192,16,16],
    #Flor 1
    218:[144,176,16,16],
     
    #Roca 1
    210:[32,192,16,16],
    #Roca 2
    211:[32,208,16,16],
    #Roca 3
    212:[64,208,16,16],
     
    #Arbol grande 1
    213:[0,224,48,80],
    #Arbol mediano 1
    214:[48,224,32,48],
    #Arbol mediano 2
    215:[80,224,32,48],
    #Arbol mediano 3
    216:[112,224,32,48],
     
    #Roca mediana
    217:[48,192,16,32],
     
#Decoracion de la arena
    # Estrella 1
    300:[160,176,16,16],
    # Estrella 2
    301:[176,176,16,16],
    # Concha 1
    302:[192,176,16,16],
    # Concha 2
    303:[208,176,16,16],
    # Concha 3
    304:[224,176,16,16],
    # Coco 1
    305:[160,192,16,16],
    # Coco 2
    306:[176,192,16,16],
    # Coco 3
    307:[192,192,16,16],
    # Coco 4
    308:[208,192,32,16],
    # Coco 5
    309:[160,208,16,16],
    # Coco 6
    310:[176,208,16,16],
    # Hierba 1
    311:[192,208,16,16],
    # Hierba 2
    312:[208,208,16,16],
    # Hierba 3
    313:[224,208,16,16],
    # Piedra 1
    314:[160,224,16,16],
    # Piedra 2
    315:[176,224,16,16],
    # Piedra 3
    316:[192,224,16,16],
    # Piedra 4
    317:[208,224,32,16],
    # Piedra 5
    318:[160,240,32,32],
    # Piedra 6
    319:[192,240,16,32],
    # Flores 1
    320:[208,240,16,32],
     
    #Palmera 1
    321:[0,304,48,64],
    #Palmera 2
    322:[48,304,48,64],
    #Palmera 3
    323:[0,368,48,64],
    #Palmera 4
    324:[48,368,48,64],
    
#Decoracion agua alta
    500:[16,160,16,16],
    501:[32,160,16,16],
     
    }

AUTO_TILE_TYPE={
    #Contiene el tipo, y una lista con los vecinos respecto
    # [topleft, topright, downleft, downright]
    
    # Vacio
    -1:[-1,-1,-1,-1],
    # Cesped
    0:[0,0,0,0],
    # Cesped elevado
    4:[4,4,4,4],
    # Agua con cesped elevado
    5:[5,5,5,5],
    # Auga orilla
    1:[1,1,1,1],
    # Agua oscura
    2:[2,2,2,2],
    # Arena
    3:[3,3,3,3],
    
    # Union cesped 0-arena 3
    
    11:[0,0,0,3],   12:[0,0,3,3],   13:[0,0,3,0],
    14:[0,3,0,3],                   15:[3,0,3,0],
    16:[0,3,0,0],   17:[3,3,0,0],   18:[3,0,0,0], 
    
    19:[0,3,3,0],    20:[3,0,0,3],
    21:[3,3,3,0],    22:[3,3,0,3],
    23:[3,0,3,3],    24:[0,3,3,3],
    
      
    # Union arena 3-agua 1
    25:[3,3,3,1],   26:[3,3,1,1],   27:[3,3,1,3],
    28:[3,1,3,1],                   29:[1,3,1,3],
    30:[3,1,3,3],   31:[1,1,3,3],   32:[1,3,3,3], 
    
    33:[3,1,1,3],    34:[1,3,3,1],
    35:[1,1,1,3],    36:[1,1,3,1],
    37:[1,3,1,1],    38:[3,1,1,1],
    
      
    # Union agua orilla 1-agua oscura 2
    39:[1,1,1,2],   40:[1,1,2,2],   41:[1,1,2,1],
    42:[1,2,1,2],                   43:[2,1,2,1],
    44:[1,2,1,1],   45:[2,2,1,1],   46:[2,1,1,1], 
    
    47:[1,2,2,1],    48:[2,1,1,2],
    49:[2,2,2,1],    50:[2,2,1,2],
    51:[2,1,2,2],    52:[1,2,2,2],
    
    # Union cesped 0-cesped elevado 4
    53:[0,0,0,4],   54:[0,0,4,4],   55:[0,0,4,0],
    56:[0,4,0,4],                   57:[4,0,4,0],
    58:[0,4,0,0],   59:[4,4,0,0],   60:[4,0,0,0], 
    
    61:[0,4,4,0],    62:[4,0,0,4],
    63:[4,4,4,0],    64:[4,4,0,4],
    65:[4,0,4,4],    66:[0,4,4,4],
    
    
    # Union agua 5 - cesped elevado 4
    67:[4,4,4,5],   68:[4,4,5,5],   69:[4,4,5,4],
    70:[4,5,4,5],                   71:[5,4,5,4],
    72:[4,5,4,4],   73:[5,5,4,4],   74:[5,4,4,4], 
    
    75:[4,5,5,4],    76:[5,4,4,5],
    77:[5,5,5,4],    78:[5,5,4,5],
    79:[5,4,5,5],    80:[4,5,5,5],
    
    }

# AUTO_TILE_BORDERS={
    #Contiene el tipo, y una lista con los vecinos respecto
    # [topleft, topright, downleft, downright]
    
#     # Cesped
#     '-1;-1;-1;-1':-1,
#     # Cesped
#     '0;0;0;0':0,
#     # Auga orilla
#     '1;1;1;1':1,
#     # Agua oscura
#     '2;2;2;2':2,
#     # Arena
#     '3;3;3;3':3,
#     
#     # Union cesped-arena
#     
#     '0;0;0;3':11,   '0;0;3;3':12,  '0;0;3;0':13,
#     '0;3;0;3':14,                  '3;0;3;0':15,
#     '0;3;0;0':16,   '3;3;0;0':17,  '3;0;0;0':18,
#     
#     '0;3;3;0':19,   '3;0;0;3':20,
#     '3;3;3;0':21,   '3;3;0;3':22,
#     '3;0;3;3':23,   '0;3;3;3':24,
#       
#     # Union arena 3-agua 1
#     '3;3;3;1':25,   '3;3;1;1':26,   '3;3;1;3':27,
#     '3;1;3;1':28,                   '1;3;1;3':29,
#     '3;1;3;3':30,   '1;1;3;3':31,   '1;3;3;3':32, 
#     
#     '3;1;1;3':33,    '1;3;3;1':34,
#     '1;1;1;3':35,    '1;1;3;1':36,
#     '1;3;1;1':37,    '3;1;1;1':38,
#     
#       
#     # Union agua orilla 1-agua oscura 2
#     '1;1;1;2':39,   '1;1;2;2':40,   '1;1;2;1':41,
#     '1;2;1;2':42,                   '2;1;2;1':43,
#     '1;2;1;1':44,   '2;2;1;1':45,   '2;1;1;1':46, 
#     
#     '1;2;2;1':47,    '2;1;1;2':48,
#     '2;2;2;1':49,    '2;2;1;2':50,
#     '2;1;2;2':51,    '1;2;2;2':52,
    
#     }

# Tamano de un tipo de tile en tiles
TILE_SIZE=lambda tile_type: [TILE_TYPES[tile_type][2]//TILE_SIZE_GENERAL[0],TILE_TYPES[tile_type][3]//TILE_SIZE_GENERAL[1]]

# 
# # Respecto a los tipos de vecino el tipo de tile correspondiente con 4 vecinos
# # Top;Down;Left;Right           tipo respectivo
# #La generacion funciona de izquierda a derecha y de arriba a abajo
# TILE_TYPES_4NEIGHBOUR_FIX={
# # Sirve para arreglar algun error grafico
#     '2;8;0;6':5,
#     '2;8;0;10':5,
#     '2;12;0;6':5,
#     '2;12;0;10':5,
#     '2;8;0;9':5,
#     '2;12;0;9':5,
#     '2;16;0;6':5,
#     '2;16;0;10':5,
#     '2;16;0;9':5,
# 
#     
#     '4;9;6;0':7,
#     '4;9;11;0':7,
#     '4;13;6;0':7,
#     '4;13;11;0':7,
#     '4;18;6;0':7,
#     '4;18;11;0':7,
#     
#     '2;10;2;6':19,
#     '2;10;3;6':19,
#     '2;10;2;10':19,
#     '2;10;3;10':19,
#     
#     '2;10;2;9':19,
#     '2;10;3;9':19,
#     
#     '4;11;6;3':20,
#     '4;11;6;4':20,
#     '4;11;11;3':20,
#     '4;11;11;4':20,
#     
#     '4;11;19;3':20,
#     '4;11;19;4':20,
#     '4;11;5;3':20,
#     '4;11;5;4':20,
#     '4;11;8;3':20,
#     '4;11;8;4':20,
#     
#     '8;12;16;1':21,
#     '8;12;17;1':21,
#     '8;16;16;1':21,
#     '8;16;17;1':21,
#     '19;12;16;1':21,
#     '19;12;17;1':21,
#     '19;16;16;1':21,
#     '19;16;17;1':21,
#     
#     '9;13;1;17':22,
#     '9;13;1;18':22,
#     '9;18;1;17':22,
#     '9;18;1;18':22,
#     '20;13;1;17':22,
#     '20;13;1;18':22,
#     '20;18;1;17':22,
#     '20;18;1;18':22,
#     
#     
#     '24;0;24;0':29,
#     '24;0;25;0':29,
#     '27;0;24;0':29,
#     '27;0;25;0':29,
#     
#     '26;0;0;25':30,
#     '26;0;0;26':30,
#     '28;0;0;25':30,
#     '28;0;0;26':30,
#     
#     '0;27;31;0':32,
#     '0;27;35;0':32,
#     '0;31;31;0':32,
#     '0;31;35;0':32,
#     
#     '0;28;0;34':33,
#     '0;28;0;35':33,
#     '0;34;0;34':33,
#     '0;34;0;35':33,
#     
#     }
# 
# 
# 
# # Respecto a los tipos de vecino el tipo de tile correspondiente con 8 vecinos y el central
# # cornerTopLeft;Top;cornerTopRight;Left;center;Right;cornerDownLeft;Down;cornerDownRight      tipo respectivo
# #La generacion funciona de izquierda a derecha y de arriba a abajo
# TILE_TYPES_9NEIGHBOUR1 = {
#     #Para abajo
#     
#     #Para quitar entradas de 1
#     '1;1;1;0;1;0;0;0;0':0,
#     '0;0;0;0;1;0;1;1;1':0,
#     '1;0;0;1;1;0;1;0;0':0,
#     '0;0;1;0;1;1;0;0;1':0,
#     
#     '0;0;0;23;0;23;23;23;23':23,
#     '23;23;23;23;0;23;0;0;0':23,
#     '0;23;23;0;0;23;0;23;23':23,
#     '23;23;0;23;0;0;23;23;0':23,
#     }
# 
# 
# TILE_TYPES_9NEIGHBOUR2 = {
#     #Para poner bordes
#     '0;0;0;0;1;1;0;1;1':2,
#     '0;0;0;0;1;1;1;1;1':2,
#     '0;0;1;0;1;1;1;1;1':2,
#     '0;0;1;0;1;1;0;1;1':2,
#     
#     '0;0;0;1;1;1;1;1;1':3,
#     '0;0;1;1;1;1;1;1;1':3,
#     '1;0;0;1;1;1;1;1;1':3,
#     '1;0;1;1;1;1;1;1;1':3,
#     
#     '0;0;0;1;1;0;1;1;0':4,
#     '0;0;0;1;1;0;1;1;1':4,
#     '1;0;0;1;1;0;1;1;1':4,
#     '1;0;0;1;1;0;1;1;0':4,
#     
#     '0;1;1;1;1;1;1;1;1':8,
# 
#     '1;1;0;1;1;1;1;1;1':9,
#     
#     '0;1;1;0;1;1;0;1;1':12,
#     '1;1;1;0;1;1;0;1;1':12,
#     '0;1;1;0;1;1;1;1;1':12,
#     '1;1;1;0;1;1;1;1;1':12,
#     
#     '1;1;0;1;1;0;1;1;0':13,
#     '1;1;1;1;1;0;1;1;0':13,
#     '1;1;0;1;1;0;1;1;1':13,
#     '1;1;1;1;1;0;1;1;1':13,
#     
#     '1;1;1;1;1;1;0;1;1':14,
#     
#     '1;1;1;1;1;1;1;1;0':15,
#     
#     '0;1;1;0;1;1;0;0;0':16,
#     '1;1;1;0;1;1;0;0;0':16,
#     '1;1;1;0;1;1;0;0;1':16,
#     '0;1;1;0;1;1;0;0;1':16,
#     
#     '1;1;1;1;1;1;0;0;0':17,
#     '1;1;1;1;1;1;1;0;0':17,
#     '1;1;1;1;1;1;0;0;1':17,
#     '1;1;1;1;1;1;1;0;1':17,
#     
#     '1;1;0;1;1;0;0;0;0':18,
#     '1;1;1;1;1;0;0;0;0':18,
#     '1;1;1;1;1;0;1;0;0':18,
#     '1;1;0;1;1;0;1;0;0':18,
# }
#     
# TILE_TYPES_9NEIGHBOUR3 ={
#     # Para union de la arena 0 y el cesped 23
#     '23;23;23;23;0;0;23;0;0':24,
#     '23;23;23;23;0;0;0;0;0':24,
#     '23;23;0;23;0;0;0;0;0':24,
#     '23;23;0;23;0;0;23;0;0':24,
#     
#     '23;23;23;0;0;0;0;0;0':25,
#     '23;23;0;0;0;0;0;0;0':25,
#     '0;23;23;0;0;0;0;0;0':25,
#     '0;23;0;0;0;0;0;0;0':25,
# 
#     '23;23;23;0;0;23;0;0;23':26,
#     '23;23;23;0;0;23;0;0;0':26,
#     '0;23;23;0;0;23;0;0;0':26,
#     '0;23;23;0;0;23;0;0;23':26,
#     
#     '23;0;0;23;0;0;23;0;0':27,
#     '0;0;0;23;0;0;23;0;0':27,
#     '23;0;0;23;0;0;0;0;0':27,
#     '0;0;0;23;0;0;0;0;0':27,
#     
#     '0;0;23;0;0;23;0;0;23':28,
#     '0;0;0;0;0;23;0;0;23':28,
#     '0;0;23;0;0;23;0;0;0':28,
#     '0;0;0;0;0;23;0;0;0':28,
#     
#     '23;0;0;0;0;0;0;0;0':29,
#     
#     '0;0;23;0;0;0;0;0;0':30,
#     
#     '0;0;0;0;0;0;23;0;0':32,
#     
#     '0;0;0;0;0;0;0;0;23':33,
# 
#     '23;0;0;23;0;0;23;23;23':31,
#     '0;0;0;23;0;0;23;23;23':31,
#     '0;0;0;23;0;0;23;23;0':31,
#     '23;0;0;23;0;0;23;23;0':31,
# 
#     '0;0;0;0;0;0;23;23;23':35,
#     '0;0;0;0;0;0;0;23;23':35,
#     '0;0;0;0;0;0;23;23;0':35,
#     '0;0;0;0;0;0;0;23;0':35,
# 
#     '0;0;23;0;0;23;23;23;23':34,
#     '0;0;0;0;0;23;23;23;23':34,
#     '0;0;0;0;0;23;0;23;23':34,
#     '0;0;23;0;0;23;0;23;23':34,
#     }
# 
# 
# TILE_TYPES_UPNEIGHBOUR = {
#     #Para los bordes inferiores
#     '3':6,
#     '8':10,
#     '9':11
#     }

CURSOR_CROSS = ( "                                ",
                 "    XXXXXXXX        XXXXXXXX    ",
                 "   X........X      X........X   ",
                 "  X.........X      X.........X  ",
                 " X..........X      X..........X ",
                 " X...XXXXXXX        XXXXXXX...X ",
                 " X...X                    X...X ",
                 " X...X                    X...X ",
                 " X...X                    X...X ",
                 " X...X         XX         X...X ",
                 " X...X        X..X        X...X ",
                 " X...X        X..X        X...X ",
                 "  XXX         X..X         XXX  ",
                 "              X..X              ",
                 "          XXXXX..XXXXX          ",
                 "         X......,.....X         ",#Mitad
                 "         X............X         ",#
                 "          XXXXX..XXXXX          ",
                 "              X..X              ",
                 "  XXX         X..X         XXX  ",
                 " X...X        X..X        X...X ",
                 " X...X        X..X        X...X ",
                 " X...X         XX         X...X ",
                 " X...X                    X...X ",
                 " X...X                    X...X ",
                 " X...X                    X...X ",
                 " X...XXXXX            XXXXX...X ",
                 " X........X          X........X ",
                 "  X.......X          X.......X  ",
                 "   X......X          X......X   ",
                 "    XXXXXX            XXXXXX    ",
                 "                                ")



