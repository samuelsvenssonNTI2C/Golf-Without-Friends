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
        sideview = True
        win = False
        font = pygame.font.Font(size = 30)
        
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
                            if golf_ball.resultant == [0, 0]:
                                sideview = not sideview
                                golf_ball.in_block = True
                                if sideview:
                                    golf_ball.depth = golf_ball.y
                                    golf_ball.y = self.screen.get_height() - 16 - golf_ball.radius # put golf ball on ground
                                else:
                                    golf_ball.y = golf_ball.depth 
                            
                        if event.key == pygame.K_TAB:
                            if current_map_index < len(maps)-1:
                                current_map_index += 1
                                map = Map(self.screen, maps[current_map_index])
                            else:
                                raise 'you won'
                                         
            
            if not sideview:
                golf_ball.on_ground = True
                
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
            collided_with = golf_ball.move(hitboxes, current_map)
            if collided_with != -1 and collided_with < len(current_map['blocks']):
                if not golf_ball.in_block and sideview:
                    golf_ball.friction(map.materials[current_map['blocks'][collided_with]['type']]['friction'])
                if current_map['blocks'][collided_with]['type'] == 'victory_block':
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
                        golf_ball = Ball(self.screen, self.scale, map.side_map['starting_point'])
                        sideview = True
                    else:
                        raise Exception('you won')
                    
            self.display.blit(font.render('Shots: ' + str(golf_ball.shots), True, (0, 0, 0)), (20, 20))
            pygame.display.update()

            clock.tick(fps)      # sets framerate to 60 fps 

Game().run()