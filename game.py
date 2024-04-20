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
        self.scale = self.display.get_width() / self.screen.get_width()
    def run(self):
        clock = pygame.time.Clock()
        golf_ball = Ball(self.screen, self.scale, 100, 100)
        normal_fps = 60
        fast_fps = 600
        fps = normal_fps
        maps = json.load(open('maps.json'))
        map = Map(self.screen, maps[0])
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
                            
                        if event.key == pygame.K_TAB:
                            print('next map')
                            map = Map(self.screen, maps[1])
                            
            
            if not self.sideview:
                golf_ball.on_ground = True
                golf_ball.friction(0.02)    # friction in topview
            golf_ball.gravity()
            
            
            if self.sideview:
                map.draw_side()
                hitboxes = map.side_hitboxes
                current_map = map.side_map
            else:
                map.draw_top()
                hitboxes = map.top_hitboxes
                current_map = map.top_map
            
            # collision
            golf_ball.on_ground = False
            golf_ball.colliding = 0
            rect = golf_ball.hitbox.collidelist(hitboxes)
            if rect != -1 and golf_ball.has_collided_with != rect:
                golf_ball.friction(map.materials[current_map['blocks'][rect]['type']]['friction'])
                x, y, w, h = hitboxes[rect]
                x1, y1 = x, y
                x2, y2 = x + w, y
                x3, y3 = x, y + h
                x4, y4 = x + w, y + h
 
                lines = [
                    ((x1, y1), (x2, y2)),
                    ((x1, y1), (x3, y3)),
                    ((x2, y2), (x4, y4)),
                    ((x3, y3), (x4, y4))]
                
                for line in lines:
                    if golf_ball.hitbox.clipline(line):
                        golf_ball.collision(line[0][0] == line[1][0])
                        break
            golf_ball.has_collided_with = rect
            
            if golf_ball.selected == True:
                golf_ball.shoot()                 
            
            golf_ball.move()
            
            golf_ball.update()
            
            
            self.display.blit(pygame.transform.scale(self.screen, self.display.get_size()), (0, 0))
            pygame.display.update()

            clock.tick(fps)      # sets framerate to 60 fps 

Game().run()