import pygame,sys
from pygame.locals import *
from Game.Components.Screen import Screen_container
from Game.Components.Camera import Camera
from Game.Components.Entities import Player
from Game.Components.Text import Text
from Game.Components.Map import Map

pygame.init()

clock = pygame.time.Clock()

screen_container = Screen_container()

camera = Camera([0,0],screen_container)

control_text=Text([10,0],screen_container)

player=Player([0,0],"slime",screen_container)

terrain_map=Map(screen_container,load=True)

run=True

while (run):
    screen_container.screen.fill((0,0,0))
    
    for e in pygame.event.get():
#         For the exit
        if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
            run = False
            
#         For the player controls
        if e.type == KEYDOWN:
            if pygame.key.name(e.key) in player.controls_press.keys():
                player.controls_press[pygame.key.name(e.key)]()
        elif e.type == KEYUP:
            if pygame.key.name(e.key) in player.controls_release.keys():
                player.controls_release[pygame.key.name(e.key)]()
        
#         For the camera controls
        if e.type == MOUSEBUTTONDOWN:
            if e.button in camera.controls.keys():
                camera.controls[e.button]()
                player.image_update(camera)
                for chunk in terrain_map.chunks.values():
                    chunk.image_update(camera)
       
#         For the resizable
        if e.type == VIDEORESIZE:
            screen_container.update_size([e.w,e.h])
            camera.screen_update()
            player.image_update(camera)
            for chunk in terrain_map.chunks.values():
                chunk.image_update(camera)



    camera.update_position(player.position_map)
    
#     Optimizacion de renderizado
    
    for chunk_key in camera.list_of_str_in_screen_chunks():
        if chunk_key in terrain_map.chunks:
            terrain_map.chunks[chunk_key].camera_update(camera)
            terrain_map.chunks[chunk_key].draw()   
    
    
#     for chunk in terrain_map.chunks.values():
#         chunk.camera_update(camera)
#         chunk.draw()
     
    
    player.update()
    player.camera_update(camera)
    player.draw()
    
    
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























