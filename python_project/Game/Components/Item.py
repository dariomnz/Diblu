import pygame
from utils import  load_image, JSONParser, getRect
from Game.Components.Sprite import Sprite
from Game.constants import ITEMSSHEET1_NAME, ITEMS_TYPE, ITEMS_SCALE
from Game.Components.Screen_container import getInstance as S_c
from Game.Components.Camera import getInstance as camera
from Game.Components.Map import getInstance as terrain_map
from Game.Components.Text import Text


class ItemsSheet(Sprite):
    '''Clase que se encarga de guardar el tilemap'''
    def __init__(self,name):
        
        self.original_image=load_image(name+'.png',ITEMS_SCALE)
        
        self.scale_image=ITEMS_SCALE
        
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
            self.original_image_tilemap_collision_box[collision_type]=load_image(image_name,ITEMS_SCALE)
        
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
    def __init__(self,position_map,item_type,amount=1,itemssheet=None,layer=None):
        self.item_type=item_type
        if itemssheet==None:
            self.itemssheet=ITEMSSHEET1
        else:
            self.itemssheet=itemssheet
        
        image=self.itemssheet.image_items[self.item_type]
        
        self.scale_image=1
        super().__init__(position_map,image,layer)
        
        self.chunk=terrain_map().chunk_in_item(self.position_map)
        self.chunk.items.append(self)
        
        self.amount=amount
        self.amount_limit=999
        self.text_amount=Text((0,0),size=15)
        
        self.image_update()
        
        self.setUp_collisionBox()
        
     
    def update(self):
        
        self.update_collision()
#         print(self.collisions)
#         print(self.position_map)
        for collision in self.collisions:
            # Para revotar en bloques o jugador
            if collision['sprite_type'].startswith('jump_body') or collision['sprite_type'].startswith('jump_block') or collision['sprite_type'].startswith('block'):
                self.repel(collision['self_rect'],collision['sprite_rect'])
                
            # Para empujar otros items
            if collision['sprite_type'].startswith('item_body'):
                if self.item_type==collision['sprite'].item_type:
                    if (self.amount+collision['sprite'].amount)<=self.amount_limit:
                        collision['sprite'].delete_self()
                        self.add_amount(collision['sprite'].amount)
                
                self.repel(collision['self_rect'],collision['sprite_rect'])
                
            # Para ponerse detras de las tiles altas
            if collision['sprite_type'].startswith('tall_tile'):
                self.add_layer_below(collision['sprite'])
                collision['sprite'].do_transparent(0.5)
                
        super().update()
        
    def repel(self,self_cB_map,sprite_cB_map):
        
        repel_vel=[0,0]
        repel_vel[0]=(self_cB_map.center[0]-sprite_cB_map.center[0])/25
        repel_vel[1]=(self_cB_map.center[1]-sprite_cB_map.center[1])/25
        
        self.float_position_map[0]+=repel_vel[0]
        self.float_position_map[1]+=repel_vel[1]
        
        self.position_map[0]=int(self.float_position_map[0])
        self.position_map[1]=int(self.float_position_map[1])
        
        self.layer=self.position_map.bottom+48
        
        new_chunk=terrain_map().chunk_in_item(self.position_map)
        
        if self.chunk!=new_chunk:
            self.chunk.del_item(self)
            self.chunk=new_chunk
            if self.chunk:
                self.chunk.items.append(self)
    
    def add_amount(self,amount=1):
        self.amount+=amount
        self.image_update()
        
     
    def delete_self(self):
        self.chunk.del_item(self)
        self.clear_collision()
        
                       
    def image_update(self):
        '''Actualiza la imagen escalada, cogiendola del tilemap ya escalado'''
        self.image=self.itemssheet.image_items[self.item_type].copy()
        
        new_size=int(self.text_amount.original_size*S_c().h_factor_image*camera().zoom)
        self.text_amount.update_size(new_size)
        self.text_amount.update_text(self.amount)
        self.text_amount.draw_in(self.image)

    def setUp_collisionBox(self): 
        
        self.cB_rect={}
        self.cB_rect_map={}
        for collision_type,rect in self.itemssheet.cB_rects[self.item_type].items():
            self.cB_rect[collision_type]=rect.copy()
            self.cB_rect_map[collision_type]=rect.copy()
        
        self.update_collision()
        

# ITEMS={}
# 
# for item_type in ITEMS_TYPE.keys():
#     ITEMS[item_type]=Item([0,0],item_type,ITEMSSHEET1)
        
        
        
        
        