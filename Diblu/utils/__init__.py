import json,os
from builtins import str


def JSONParser(jsonfile)->dict:
    pathfile = os.path.join('..','data','json',jsonfile)
    
    with open(pathfile, 'r') as json_data:
        data = json.load(json_data)
        
    return data

def JSONsave(jsonfile,data):
    pathfile = os.path.join('..','data','json',jsonfile)
    with open(pathfile, 'w') as file:
        json.dump(data, file)


def pos2center(pos,size):
    return [pos[0]+size[0]//2,pos[1]+size[1]//2]

def center2pos(pos,size):
    return [pos[0]-size[0]//2,pos[1]-size[1]//2]

def size(screen):
    return [screen.get_width(),screen.get_height()]

def str2list4(string):
    split=string.split(';')
    return [int(split[0]),int(split[1]),int(split[2]),int(split[3])]

def str2list3(string):
    split=string.split(';')
    return [int(split[0]),int(split[1]),int(split[2])]

def str2list2(string):
    split=string.split(';')
    return [int(split[0]),int(split[1])]

def list2str4(listIn):
    return str(listIn[0])+';'+str(listIn[1])+';'+str(listIn[2])+';'+str(listIn[3])

def list2str3(listIn):
    return str(listIn[0])+';'+str(listIn[1])+';'+str(listIn[2])

def list2str2(listIn):
    return str(listIn[0])+';'+str(listIn[1])



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