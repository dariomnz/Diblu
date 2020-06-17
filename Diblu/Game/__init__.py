import pygame,sys,cProfile
from pygame.locals import *
from Game.constants import TPS

def main():
    pygame.init()
    
    clock = pygame.time.Clock()
    
    from Game.Components import Screen_container
    Screen_container.createInstance()
    from Game.Components.Screen_container import getInstance as S_c
    
    from Game.Components import Camera
    Camera.createInstance()
    from Game.Components.Camera import getInstance as camera
    
    from Game.Components.Text import Text
    control_text=Text([10,0])
    
    from Game.Components.Entities import Player
    player=Player([1,0],"slime",layer=2)
    
    
    from Game.Components.Tile import TILEMAP1
    from Game.Components.Map import Map
    terrain_map=Map(load=False)
    
    from Game import Particle_manager as P_m 
    from Game.Particle_manager import SMOKE_PRESET
    P_m.createInstance()
    from Game.Particle_manager import getInstance as Particle_manager
    
    
    run=True
    
    while (run):
        S_c().screen.fill((0,0,0))
        
        for e in pygame.event.get():
    #         For the exit
            if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                run = False
                
    #         For the player controls
            if e.type == KEYDOWN:
                if pygame.key.name(e.key) in player.controls_press.keys():
                    player.controls_press[pygame.key.name(e.key)]()
                #Prueba de creacion de particulas
                if pygame.key.name(e.key)=='p':
                    Particle_manager().spawn(player.position_map,player.layer-0.1, 20,SMOKE_PRESET)
            elif e.type == KEYUP:
                if pygame.key.name(e.key) in player.controls_release.keys():
                    player.controls_release[pygame.key.name(e.key)]()
            
    #         For the camera controls
            if e.type == MOUSEBUTTONDOWN:
                if e.button in camera().controls.keys():
                    aux_camera_zoom=camera().zoom
                    camera().controls[e.button]()
                    if aux_camera_zoom!=camera().zoom:
                        player.image_update()
                        TILEMAP1.image_update()
                        for chunk in terrain_map.chunks.values():
                            chunk.image_update()
           
    #         For the resizable
            if e.type == VIDEORESIZE:
                S_c().update_size([e.w,e.h])
                camera().screen_update()
                player.image_update()
                TILEMAP1.image_update()
                for chunk in terrain_map.chunks.values():
                    chunk.image_update()
    
    
    
        camera().update_position(player.position_map)
        
    
        # Dibujado de las layers
        S_c().draw_layers()
        
    #     Optimizacion de renderizado
    
        for chunk_key in camera().list_of_str_in_screen_chunks():
            if chunk_key in terrain_map.chunks:
                terrain_map.chunks[chunk_key].camera_update()
                terrain_map.chunks[chunk_key].add_self_layer()
        
        
#         for chunk in terrain_map.chunks.values():
#             chunk.camera_update(camera)
#             chunk.add_self_layer()
    #         chunk.draw()
    #      
        
        player.update()
        player.camera_update()
        S_c().add_to_self_layer(player)
    
        
        Particle_manager().camera_update()
        # Introducion en las layer para draw
        Particle_manager().add_to_self_layer()
        
        
        
        
        # Texto a mostrar por pantalla
        fps = "FPS: " + str(int(clock.get_fps()))
        player_x_text= " X: "+str(player.position_map[0])
        player_y_text= " Y: "+str(player.position_map[1])
        control_text.update_text(fps+player_x_text+player_y_text)
        control_text.draw()
        
        clock.tick(TPS)
        
        pygame.display.update()
#         run=False
        
#     terrain_map.save()
    pygame.quit()
    sys.exit()
    
    

if __name__=='__main__':
#     cProfile.run('main()')
    main()

















