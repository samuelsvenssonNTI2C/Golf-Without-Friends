import pygame
import sys
import json
import math
from scripts.ball import Ball
from scripts.map import Map
from scripts.animation import Animation
import time

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.Surface((256, 144))
        self.display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.display = pygame.display.set_mode((512, 288))
        self.scale = self.display.get_width() / self.screen.get_width()
    def run(self):
        clock = pygame.time.Clock()
        
        normal_fps = 60
        fast_fps = 600
        fps = normal_fps
        maps = json.load(open('maps.json'))
        current_map_index = 0
        map = Map(self.screen, maps[current_map_index])
        current_map = map.side_map
        golf_ball = Ball(self.screen, self.scale, map.side_map['starting_point'])
        goal_animation = Animation(self.display, 'animations/goal_confetti', 0.4, (-64, -100))
        # goal_animation.offsets = (1, 1)
        sideview = True
        win = False
        
        frame = 0
        
        while True:
            self.screen.blit(Map.background[current_map['background']]['texture'], (0, 0))
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    
                    case pygame.MOUSEBUTTONDOWN:
                        if golf_ball.resultant == [0, 0]:
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
                            sideview = not sideview
                            golf_ball.in_block = True
                            
                        if event.key == pygame.K_TAB:
                            if current_map_index < len(maps)-1:
                                current_map_index += 1
                                map = Map(self.screen, maps[current_map_index])
                            else:
                                raise 'you won'
                                         
            
            if not sideview or golf_ball.in_block:
                golf_ball.on_ground = True
            else:
                golf_ball.on_ground = False
                
            golf_ball.gravity()
            
            
            if sideview:
                map.draw_side()
                hitboxes = map.side_hitboxes
                current_map = map.side_map
            else:
                map.draw_top()
                hitboxes = map.top_hitboxes
                current_map = map.top_map
            
            
            if golf_ball.selected == True:
                golf_ball.shoot()           
            
            golf_ball.friction(Map.background[current_map['background']]['friction'])  # constant friction from background
            collided_with = golf_ball.move(hitboxes)
            if collided_with != -1 and collided_with < len(current_map['blocks']):
                golf_ball.friction(map.materials[current_map['blocks'][collided_with]['type']]['friction'])
                if current_map['blocks'][collided_with]['type'] == 'victory_block' and math.hypot(golf_ball.resultant[0], golf_ball.resultant[1]) < 0.3:
                    win = True
                    winblock_index = collided_with

            golf_ball.update()
            
            self.display.blit(pygame.transform.scale(self.screen, self.display.get_size()), (0, 0))
            
            if win:
                goal_animation.draw(([cord * 16 * self.scale for cord in current_map['blocks'][winblock_index]['position']]), frame)
                if frame < goal_animation.number_of_frames-1:
                    frame += 1
                else:
                    win = False
                    if current_map_index < len(maps)-1:
                        current_map_index += 1
                        map = Map(self.screen, maps[current_map_index])
                    else:
                        raise Exception('you won')
                
            pygame.display.update()

            clock.tick(fps)      # sets framerate to 60 fps 

Game().run()