import json,os,pygame
from pygame.locals import RLEACCEL
from Game.constants import TILE_SIZE_GENERAL, TILE_SIZE_GENERAL_PIXEL
import logging

def load_image(name, colorkey = None):
    """Carga la imagen de nombre 'name' desde
       el directorio 'datadir'"""
    fullname = os.path.join('..','data','images',name)

    image = pygame.image.load(fullname)
    
    if colorkey is not None:
        image = image.convert()
        
    if colorkey == -1:
        colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    else:
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
            
    scale_image=TILE_SIZE_GENERAL_PIXEL[0]/TILE_SIZE_GENERAL[0]
    original_image_size=[int(image.get_width()*scale_image),int(image.get_height()*scale_image)]
    image=pygame.transform.scale(image, (original_image_size[0], original_image_size[1]))
                    
    return image


def JSONParser(jsonfile)->dict:
    '''Recoje los datos de un jsonfile y los devuelve en forma de dict'''
    jsonfile+='.json'
    pathfile = os.path.join('..','data','json',jsonfile)
    
    with open(pathfile, 'r') as json_data:
        data = json.load(json_data)
        
    return data

def JSONsave(jsonfile,data:dict):
    '''Guarda en el archivo jsonfile los datos de data'''
    jsonfile+='.json'
    pathfile = os.path.join('..','data','json',jsonfile)
    with open(pathfile, 'w') as file:
        json.dump(data, file, indent=4)


def pos2center(pos,size):
    '''Transforma una posicion con un tamano en su posicion central'''
    return [pos[0]+size[0]//2,pos[1]+size[1]//2]

def center2pos(pos,size):
    '''Transforma una posicion con su tamano en la representacion de ella en pygame'''
    return [pos[0]-size[0]//2,pos[1]-size[1]//2]

def str2list9(string):
    '''format '0;0;0;0;0;0;0;0;0' '''
    split=string.split(';')
    return [int(split[0]),int(split[1]),int(split[2]),int(split[3]),int(split[4]),int(split[5]),int(split[6]),int(split[7]),int(split[8])]

def str2list4(string):
    '''format '0;0;0;0' '''
    split=string.split(';')
    return [int(split[0]),int(split[1]),int(split[2]),int(split[3])]

def str2list3(string):
    '''format '0;0;0' '''
    split=string.split(';')
    return [int(split[0]),int(split[1]),int(split[2])]

def str2list2(string):
    '''format '0;0' '''
    split=string.split(';')
    return [int(split[0]),int(split[1])]

def list2str9(listIn):
    '''format '0;0;0;0;0;0;0;0;0' '''
    return str(listIn[0])+';'+str(listIn[1])+';'+str(listIn[2])+';'+str(listIn[3])+';'+str(listIn[4])+';'+str(listIn[5])+';'+str(listIn[6])+';'+str(listIn[7])+';'+str(listIn[8])

def list2str4(listIn):
    '''format '0;0;0;0' '''
    return str(listIn[0])+';'+str(listIn[1])+';'+str(listIn[2])+';'+str(listIn[3])

def list2str3(listIn):
    '''format '0;0;0' '''
    return str(listIn[0])+';'+str(listIn[1])+';'+str(listIn[2])

def list2str2(listIn):
    '''format '0;0' '''
    return str(listIn[0])+';'+str(listIn[1])

def nearValue(value_to_check,value,range_to_check):
    '''Comprueba si value_to_check esta cerca de value con un rango de error de range_to_check'''
    return (value-range_to_check)<value_to_check<(value+range_to_check)

def getRect(pointList):
#     if len(pointList)!=4:
#         logging.ERROR('The point list:'+str(pointList)+' has less than 4 points')
# #         print('The point list has less than 4 points') 
#         return None
#     print(pointList)
    minPoint=pointList[0]
    for point in pointList:
        if point[0]<minPoint[0] or point[1]<minPoint[1]:
            minPoint=point

    pointList.remove(minPoint)
    maxX=minPoint[0]
    maxY=minPoint[1]
    for point in pointList:
        if maxX<point[0]:
            maxX=point[0]
        if maxY<point[1]:
            maxY=point[1]
            
    return pygame.rect.Rect(minPoint,[maxX-minPoint[0],maxY-minPoint[1]])
    
#Pruebas

# print(getRect([(10,4),(10,10),(15,4),(15,10)]))
# <rect(10, 4, 5, 6)>
# d={1:'123123',0:'123',5:'a',3:'d'}
# print(nearValue(0.521234, 0.5, 0.01))

# print(list2str3([1,2,3]))
# print(str2list3('1;2;3')[:2])
# data=JSONParser('world.json')
# 
# print(data)
# 
# data['data']={'0:0':1,'-1:0':1}
# 
# print(data)
# 
# JSONsave('world.json', data)