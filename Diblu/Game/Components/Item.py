import pygame
from utils import  load_image, JSONParser, getRect
from Game.Components.Sprite import Sprite
from Game.constants import TILE_SIZE_GENERAL, TILE_TYPES,\
    TILE_SIZE_GENERAL_PIXEL, ITEMSSHEET1_NAME, ITEMS_TYPE
from Game.Components.Screen_container import getInstance as S_c
from Game.Components.Camera import getInstance as camera


class ItemsSheet(Sprite):
    '''Clase que se encarga de guardar el tilemap'''
    def __init__(self,name):
        
        self.original_image=load_image(name+'.png')
        
        self.scale_image=TILE_SIZE_GENERAL_PIXEL[0]/TILE_SIZE_GENERAL[0]
        
        self.image=self.original_image.copy()
        
        self.original_image_size=[self.image.get_width(),self.image.get_height()]
        
        self.setUp_collisionBox(name)
        
        self.generate_sheet()
     
    def image_update(self):
        '''Actualiza la imagen escalada'''
        self.image=pygame.transform.scale(self.original_image, (int(self.original_image.get_width()*camera().zoom*S_c().w_factor_image), int(self.original_image.get_height()*camera().zoom*S_c().h_factor_image)))
       
        self.generate_sheet()
        
        
    def generate_sheet(self):
        self.image_items={}
        for item_type in ITEMS_TYPE.keys():
            attr0=ITEMS_TYPE[item_type][0]*camera().zoom*S_c().w_factor_image*self.scale_image
            attr1=ITEMS_TYPE[item_type][1]*camera().zoom*S_c().h_factor_image*self.scale_image
            attr2=ITEMS_TYPE[item_type][2]*camera().zoom*S_c().w_factor_image*self.scale_image
            attr3=ITEMS_TYPE[item_type][3]*camera().zoom*S_c().h_factor_image*self.scale_image
            rect_in_tilemap=pygame.Rect(attr0,attr1,attr2,attr3)
            self.image_items[item_type]=self.image.subsurface(rect_in_tilemap)
            
                    
    def setUp_collisionBox(self,name):
        
        self.cB_data=JSONParser(name+'-collisionBox')
        
        #Diccionario con los tipos de colisiones, y su lista de imagenes
        self.original_image_tilemap_collision_box={}
         
        
        for collision_type,image_name in self.cB_data.items():
            self.original_image_tilemap_collision_box[collision_type]=load_image(image_name)
        
        self.image_tilemap_collision_box=self.original_image_tilemap_collision_box.copy()
          
        self.generate_cB_rects()
        
    def generate_cB_rects(self):             
        '''Formato de cB_rects key tile type con valor una lista de rect'''
        self.cB_rects={}
        for item_type in ITEMS_TYPE.keys():
            attr0=ITEMS_TYPE[item_type][0]*camera().zoom*S_c().w_factor_image*self.scale_image
            attr1=ITEMS_TYPE[item_type][1]*camera().zoom*S_c().h_factor_image*self.scale_image
            attr2=ITEMS_TYPE[item_type][2]*camera().zoom*S_c().w_factor_image*self.scale_image
            attr3=ITEMS_TYPE[item_type][3]*camera().zoom*S_c().h_factor_image*self.scale_image
            rect_in_tilemap_image=pygame.Rect(attr0,attr1,attr2,attr3)
             
            for collision_type,aux_image_tilemap_collisionBox in self.image_tilemap_collision_box.items(): 
#                 for aux_image_tilemap_collisionBox in tilemap_collisionBox:
                aux_cB_image=aux_image_tilemap_collisionBox.subsurface(rect_in_tilemap_image) 
                  
                aux_mask=pygame.mask.from_surface(aux_cB_image, 127)
                if item_type not in self.cB_rects:
                    self.cB_rects[item_type]={}
                     
                aux_outline=aux_mask.outline()
                if len(aux_outline)>0:
                    self.cB_rects[item_type][collision_type]=getRect(aux_outline)
#                     print(self.cB_rects)  
        
        
ITEMSSHEET1=ItemsSheet(ITEMSSHEET1_NAME)

        
class Item(Sprite):
    '''Porcion de un chunk para mostrar objetos'''
    def __init__(self,position_map,item_type,itemssheet,layer=None):
        self.item_type=item_type
        self.itemssheet=itemssheet
        
        image=self.itemssheet.image_items[self.item_type]
        
        super().__init__(position_map,image,layer)
        
        self.setUp_collisionBox()
     
#     def update(self):
#         if self.delay_transparent!=0:
#             self.delay_transparent-=1
#             if self.delay_transparent==0:
#                 self.image=self.tilemap.image_tiles[self.tile_type]
#         super().update()
           
    def image_update(self):
        '''Actualiza la imagen escalada, cogiendola del tilemap ya escalado'''
        self.image=self.itemssheet.image_items[self.item_type]

    def setUp_collisionBox(self): 
        
        self.cB_rect={}
        self.cB_rect_map={}
        for collision_type,rect in self.itemssheet.cB_rects[self.item_type].items():
            self.cB_rect[collision_type]=rect.copy()
            self.cB_rect_map[collision_type]=rect.copy()
        
        self.update_collision()

ITEMS={}

for item_type in ITEMS_TYPE.keys():
    ITEMS[item_type]=Item([0,0],item_type,ITEMSSHEET1)
        
        
        
        
        