import pygame
import sys
from scripts.ball import Ball

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000,600))
        
    def run(self):
        golf_ball = Ball(self.screen, 100, 100)
        v, dir = 0, 0
        
        while True:
            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    
                    case pygame.MOUSEBUTTONDOWN:
                        if v == 0 and golf_ball.hitbox.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                            golf_ball.selected = True
                    
            if golf_ball.selected == True:
                v, dir = golf_ball.shoot()
                print(v)
            
            if v > 0:
                v = golf_ball.move(v, dir)
            else:
                v = 0
                  
            golf_ball.update()
            pygame.display.update()

Game().run()