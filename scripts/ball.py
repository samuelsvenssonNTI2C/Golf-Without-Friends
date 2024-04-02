import pygame
import math

class Ball():
    def __init__(self, screen, start_x, start_y):
        self.x = start_x
        self.y = start_y
        self.screen = screen
        self.selected = False
        self.radius = 10
        self.hitbox = pygame.Rect(self.x-self.radius, self.y-self.radius, self.radius*2, self.radius*2)
        self.vectors = {
            "gravity": [0, 0],
            "velocity": [0, 0]
        }
        self.gravity_acceleration = 0.03    # acceleration in px/frame
        
        self.on_ground = False
        self.colliding = 0      # -1 -> horizontal, 0 -> no, 1 -> vertical
        self.collison_velocity_loss = 0.4
        self.resultant = [0, 0]
        
    def shoot(self):
        velocity_factor = 0.06
        max_strength = 5          # max velocity
        x, y = pygame.mouse.get_pos()
        # x, y offset from object
        rel_x = (x - self.x)*velocity_factor
        rel_y = (y - self.y)*velocity_factor
        strength = math.hypot(rel_x, rel_y)
        if  strength > max_strength:
            rel_x *= max_strength/strength
            rel_y *= max_strength/strength
            strength = max_strength
        
        # shoot power line
        if strength < max_strength/2:        # line color changes based on velocity: g -> low, b -> mid, r -> high
            pygame.draw.line(self.screen, (0, 255 - 255*(strength/(max_strength/2)), 255*(strength/(max_strength/2))), (self.x, self.y), (x, y), 3)
        else:
            pygame.draw.line(self.screen, (255*(((strength-max_strength/2)*2)/max_strength), 0, 255 - 255*(((strength-max_strength/2)*2)/max_strength)), (self.x, self.y), (x, y), 3)
        
        # release shoot
        if pygame.mouse.get_pressed(3)[0] == False:
            self.selected = False
            self.vectors["velocity"] = [-rel_x, rel_y]
            print(self.vectors["velocity"])
    
    # movement of object
    def move(self):
        for vector in self.vectors:
            self.resultant[0] += self.vectors[vector][0]
            self.resultant[1] += self.vectors[vector][1]
            
        if self.colliding == 1:
            self.resultant[0] *= -(1-self.collison_velocity_loss)
        elif self.colliding == -1:
            self.resultant[1] *= -(1-self.collison_velocity_loss)
        
        if math.hypot(self.resultant[0], self.resultant[1]) < 0.01:
            self.resultant = [0, 0]
            
        self.x += self.resultant[0]
        self.y += self.resultant[1]
        
        self.vectors["velocity"] = [0, 0]
        
    def gravity(self):
        if not self.on_ground:
            self.vectors["gravity"][1] = 0.03     # gravity acceleration in px/frame
        else:
            self.vectors["gravity"][1] = 0
    
    def friction(self, friction):
        self.resultant[0] *= (1-friction)
        #self.resultant[1] *= (1-friction)
    
    def collision(self, vertical):
        if vertical:
            self.colliding = 1
        else:
            self.colliding = -1
            self.on_ground = True
        
    #draw object and save hitbox
    def update(self):
        self.hitbox = pygame.draw.circle(self.screen, (255, 255, 255), (self.x, self.y), self.radius)