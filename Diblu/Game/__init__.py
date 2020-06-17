import pygame,sys,cProfile
from pygame.locals import *
from Game.constants import TPS

def main():
    pygame.init()
    
    clock = pygame.time.Clock()
    
    from Game.Components import Screen_container as S_c
    S_c.createInstance()
    
    from Game.Components.Camera import Camera
    camera = Camera([0,0])
    
    from Game.Components.Text import Text
    control_text=Text([10,0])
    
    from Game.Components.Entities import Player
    player=Player([1,0],"slime",layer=2)
    
    
    from Game.Components.Tile import TILEMAP1
    from Game.Components.Map import Map
    terrain_map=Map(load=True)
    
    from Game import Particle_manager
    from Game.Particle_manager import SMOKE_PRESET
    Particle_manager.createInstance()
    
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
                if pygame.key.name(e.key)=='p':
                    Particle_manager.getInstance().spawn(player.position_map,player.layer-0.1, 20,SMOKE_PRESET)
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
                        TILEMAP1.image_update(camera)
                        for chunk in terrain_map.chunks.values():
                            chunk.image_update(camera)
           
    #         For the resizable
            if e.type == VIDEORESIZE:
                S_c.getInstance().update_size([e.w,e.h])
                camera.screen_update()
                player.image_update(camera)
                TILEMAP1.image_update(camera)
                for chunk in terrain_map.chunks.values():
                    chunk.image_update(camera)
    
    
    
        camera.update_position(player.position_map)
        
    
        # Dibujado de las layers
        S_c.getInstance().draw_layers()
        
    #     Optimizacion de renderizado
    
        for chunk_key in camera.list_of_str_in_screen_chunks():
            if chunk_key in terrain_map.chunks:
                terrain_map.chunks[chunk_key].camera_update(camera)
                terrain_map.chunks[chunk_key].add_self_layer()
        
        
#         for chunk in terrain_map.chunks.values():
#             chunk.camera_update(camera)
#             chunk.add_self_layer()
    #         chunk.draw()
    #      
        
        player.update()
        player.camera_update(camera)
        S_c.getInstance().add_to_self_layer(player)
    
        
        Particle_manager.getInstance().camera_update(camera)
        # Introducion en las layer para draw
        Particle_manager.getInstance().add_to_self_layer()
        
        
        
        
        # Texto a mostrar por pantalla
        fps = "FPS: " + str(int(clock.get_fps()))
        player_x_text= " X: "+str(player.position_map[0])
        player_y_text= " Y: "+str(player.position_map[1])
        control_text.update_text(fps+player_x_text+player_y_text)
        control_text.draw()
        
        clock.tick(TPS)
        pygame.display.update()
#         run=False
        
    terrain_map.save()
    pygame.quit()
    sys.exit()
    
    

if __name__=='__main__':
#     cProfile.run('main()')
    main()

















