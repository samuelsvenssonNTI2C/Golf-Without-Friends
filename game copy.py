import pygame
import sys
import json
import math
from scripts.ball import Ball
from scripts.map import Map

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((700,400))
        
    def run(self):
        clock = pygame.time.Clock()
        golf_ball = Ball(self.screen, 100, 100)
        v, dir = 0, 0
        gravity = 0
        collision_factor = 0.8
        map = Map(self.screen, json.load(open('maps.json'))['map_1'])
        
        while True:
            fps = 60
            
            self.screen.fill((0, 0, 0))
            map.draw()
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    
                    case pygame.MOUSEBUTTONDOWN:
                        if v == 0 and golf_ball.hitbox.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                            golf_ball.selected = True
                            
                    case pygame.K_SPACE:
                        fps = 300
            
            
            # collision              
            for rect in map.hitboxes:
                x, y, w, h = rect
                x1, y1 = x, y
                x2, y2 = x + w, y
                x3, y3 = x, y + h
                x4, y4 = x + w, y + h
    
                lines = [
                    ((x1, y1), (x2, y2)),
                    ((x1, y1), (x3, y3)),
                    ((x2, y2), (x4, y4)),
                    ((x3, y3), (x4, y4))]
                
                on_ground = False
                for line in lines:
                    if golf_ball.hitbox.clipline(line):
                        v *= collision_factor
                        if line[0][0] == line[1][0]: # is vertical line
                            dir = math.pi - dir
                        else:
                            dir = -dir
                            gravity = -gravity*collision_factor
                            on_ground = True
            
            if not on_ground:
                gravity += 0.01
            
            golf_ball.gravity(gravity)
            
            if golf_ball.selected == True:
                v, dir = golf_ball.shoot()
            
            if v > 0:
                v = golf_ball.move(v, dir)
            else:
                v = 0
            golf_ball.update()
            pygame.display.update()
            
            clock.tick(fps)      # sets framerate to 60 fps 

Game().run()