import pygame,sys
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()

from Game.Components import Screen_container as S_c
S_c.createInstance()

from Game.Components.Camera import Camera
camera = Camera([0,0])

from Game.Components.Text import Text
control_text=Text([10,0])

from Game.Components.Entities import Player
player=Player([1,0],"slime",layer=0)

from Game.Components.Map import Map
terrain_map=Map(load=True)

from Game import Particle_manager
from Game.Particle_manager import SMOKE_PRESET
particle_manager=Particle_manager.createInstance()

run=True

while (run):
    S_c.getInstance().screen.fill((0,0,0))
    
    for e in pygame.event.get():
#         For the exit
        if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
            run = False
            
#         For the player controls
        if e.type == KEYDOWN:
            if pygame.key.name(e.key) in player.controls_press.keys():
                player.controls_press[pygame.key.name(e.key)]()
            #Prueba de creacion de particulas
#             if pygame.key.name(e.key)=='p':
#                 Particle_manager.getInstance().spawn(player.position_map, 20,SMOKE_PRESET)
        elif e.type == KEYUP:
            if pygame.key.name(e.key) in player.controls_release.keys():
                player.controls_release[pygame.key.name(e.key)]()
        
#         For the camera controls
        if e.type == MOUSEBUTTONDOWN:
            if e.button in camera.controls.keys():
                aux_camera_zoom=camera.zoom
                camera.controls[e.button]()
                if aux_camera_zoom!=camera.zoom:
                    player.image_update(camera)
                    for chunk in terrain_map.chunks.values():
                        chunk.image_update(camera)
       
#         For the resizable
        if e.type == VIDEORESIZE:
            S_c.getInstance().update_size([e.w,e.h])
            camera.screen_update()
            player.image_update(camera)
            for chunk in terrain_map.chunks.values():
                chunk.image_update(camera)



    camera.update_position(player.position_map)
    
#     Optimizacion de renderizado
    
    S_c.getInstance().draw_layers()
    
    for chunk_key in camera.list_of_str_in_screen_chunks():
        if chunk_key in terrain_map.chunks:
            terrain_map.chunks[chunk_key].camera_update(camera)
            terrain_map.chunks[chunk_key].add_self_layer()
    
    
#     for chunk in terrain_map.chunks.values():
#         
#         chunk.camera_update(camera)
#         chunk.add_self_layer()
#         chunk.draw()
     
    
    player.update()
    player.camera_update(camera)
#     player.draw()
    player._add_layer(player.layer)

    Particle_manager.getInstance().camera_update(camera)
    Particle_manager.getInstance().draw()
    
    
    
    
    
    
    
    
    fps = "FPS: " + str(int(clock.get_fps()))
    player_x_text= " X: "+str(player.position_map[0])
    player_y_text= " Y: "+str(player.position_map[1])
    control_text.update_text(fps+player_x_text+player_y_text)
    control_text.draw()
    
    clock.tick(60)
    pygame.display.update()
    
#     run=False
    
terrain_map.save()
pygame.quit()
sys.exit()























