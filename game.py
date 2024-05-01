import pygame
import sys
import json
import math
from scripts.ball import Ball
from scripts.map import Map

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.Surface((256, 144))
        self.display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.display = pygame.display.set_mode((512, 288))
        self.scale = self.display.get_width() / self.screen.get_width()
    def run(self):
        clock = pygame.time.Clock()
        golf_ball = Ball(self.screen, self.scale, 100, 100)
        normal_fps = 60
        fast_fps = 600
        fps = normal_fps
        maps = json.load(open('maps.json'))
        map = Map(self.screen, maps[2])
        self.sideview = True
        
        while True:
            self.screen.fill((100, 100, 100))
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    
                    case pygame.MOUSEBUTTONDOWN:
                        if golf_ball.resultant == [0, 0] and golf_ball.hitbox.collidepoint(pygame.mouse.get_pos()[0]/self.scale, pygame.mouse.get_pos()[1]/self.scale):
                            golf_ball.selected = True
                            
                    case pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            fps = fast_fps
                            
                    case pygame.KEYUP:
                        if event.key == pygame.K_SPACE:
                            fps = normal_fps
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()
                        if event.key == pygame.K_f:
                            self.sideview = not self.sideview
                            golf_ball.in_block = True
                            
                        if event.key == pygame.K_TAB:
                            print('next map')
                            map = Map(self.screen, maps[1])
                            
            
            if not self.sideview or golf_ball.in_block:
                golf_ball.on_ground = True
                golf_ball.friction(0.02)    # friction in topview
            else:
                golf_ball.on_ground = False
                
            golf_ball.gravity()
            
            
            if self.sideview:
                map.draw_side()
                hitboxes = map.side_hitboxes
                current_map = map.side_map
            else:
                map.draw_top()
                hitboxes = map.top_hitboxes
                current_map = map.top_map
            
            if golf_ball.selected == True:
                golf_ball.shoot()           
            
            collided_with = golf_ball.move(hitboxes)
            if collided_with != -1 and collided_with < len(current_map['blocks']):
                golf_ball.friction(map.materials[current_map['blocks'][collided_with]['type']]['friction'])
            
            golf_ball.update()
            
            
            self.display.blit(pygame.transform.scale(self.screen, self.display.get_size()), (0, 0))
            pygame.display.update()

            clock.tick(fps)      # sets framerate to 60 fps 

Game().run()