import json,os


def JSONParser(jsonfile)->dict:
    '''Recoje los datos de un jsonfile y los devuelve en forma de dict'''
    pathfile = os.path.join('..','data','json',jsonfile)
    
    with open(pathfile, 'r') as json_data:
        data = json.load(json_data)
        
    return data

def JSONsave(jsonfile,data:dict):
    '''Guarda en el archivo jsonfile los datos de data'''
    pathfile = os.path.join('..','data','json',jsonfile)
    with open(pathfile, 'w') as file:
        json.dump(data, file)


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


#Pruebas
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