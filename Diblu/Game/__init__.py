import pygame,sys,os,logging,cProfile
from pygame.locals import *
from Game.constants import TPS
import profile
import pstats

def main():
    pygame.init()
    pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])
    
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
    player=Player([0,0],"slime",layer=2)
    
    
    from Game.Components.Tile import TILEMAP1
    from Game.Components.Map import Map
    terrain_map=Map(load=True)
    
    from Game import Particle_manager as P_m 
    from Game.Particle_manager import SMOKE_PRESET
    P_m.createInstance()
    from Game.Particle_manager import getInstance as Particle_manager
    
    
    run=True
    debug_text=True
    
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
                if pygame.key.name(e.key)=='f3':
                    if debug_text:
                        debug_text=False
                    else:
                        debug_text=True
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
    
    
    
        camera().update_position(player.position_map.center)
        
    
        # Dibujado de las layers
        S_c().draw_layers()
        
    #     Optimizacion de renderizado
#         isWaterCollision=False
        for chunk_key in camera().list_of_str_in_screen_chunks():
            if chunk_key in terrain_map.chunks:
                terrain_map.chunks[chunk_key].camera_update()
                terrain_map.chunks[chunk_key].add_self_layer()
                terrain_map.chunks[chunk_key].check_collisions(player)
#                     isWaterCollision=True

        
        
#         for chunk in terrain_map.chunks.values():
#             chunk.camera_update(camera)
#             chunk.add_self_layer()
    #         chunk.draw()
    #      
#         print(player.collisions)
#         print(player.image.get_alpha())
        player.update()
        player.camera_update()
        S_c().add_to_self_layer(player)
    
        
        Particle_manager().camera_update()
        # Introducion en las layer para draw
        Particle_manager().add_to_self_layer()
        
        
        
#         print(terrain_map.chunks['0;0'].tiles['4;0;0'].collisionBox.image)
#         player_mask=pygame.mask.from_surface(player.collisionBox.image,0)
#         points=player_mask.outline()
# #         print(points)
#         pygame.draw.polygon(player.image, (0,0,0), points)    
#         aux_cB_rect=[player.cB_rect[0][0]+player.position_map[0],player.cB_rect[0][1]+player.position_map[1],player.cB_rect[0][2],player.cB_rect[0][3]]
#         pygame.draw.rect(S_c().screen, (0,0,0), aux_cB_rect, 0)
#         S_c().screen.blit(terrain_map.chunks['0;0'].tiles['4;0;0'].collisionBox.image,[10,10])
#         (player_mask.to_surface(S_c().screen))
        
#         for chunk in terrain_map.chunks.values():
#             for tile in chunk.tiles.values():
#                 if pygame.sprite.collide_mask(tile.collisionBox, player.collisionBox):
#                     isWaterCollision=True
        
        
        if debug_text:
            # Texto a mostrar por pantalla
            fps = "FPS: " + str(int(clock.get_fps()))
            player_x_text= " X: "+str(player.position_map[0])
            player_y_text= " Y: "+str(player.position_map[1])
#             isWaterCollision_str= ' Water: '+str(isWaterCollision)
            control_text.update_text(fps+player_x_text+player_y_text)#+isWaterCollision_str)
            control_text.draw()
#             print(player.cB_rect_map)
        
        clock.tick(TPS)
        
        pygame.display.update([0,0,S_c().get_screen_size()[0],S_c().get_screen_size()[1]])
#         run=False
        
    terrain_map.save()
    pygame.quit()
    sys.exit()
    
def setUp_logger():
    #Configuracion del logger
    logger = logging.getLogger()
    
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(os.path.join('..','data','logging.log'),mode='w')
    ch = logging.StreamHandler()
    
    fh.setLevel(logging.DEBUG)
    ch.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s: %(message)s', datefmt='%m/%d/%Y %H:%M:%S')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    logger.addHandler(fh)
    logger.addHandler(ch)

if __name__=='__main__':
    setUp_logger()
    
    # Codigo para hacer un profile
#     file_profiling=os.path.join('..','data','profiling')
#     cProfile.run('main()',filename=file_profiling)
# 
#     p = pstats.Stats(file_profiling)
#     p.strip_dirs().sort_stats(1).print_stats()
#     p.sort_stats('cumulative').print_stats(10)
    main()

















