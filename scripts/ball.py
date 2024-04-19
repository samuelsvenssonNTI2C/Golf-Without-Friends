import pygame
import math

class Ball():
    def __init__(self, screen, window_scale, start_x, start_y):
        self.x = start_x
        self.y = start_y
        self.window_scale = window_scale
        self.abs_x = start_x * self.window_scale
        self.abs_y = start_y * self.window_scale
        self.screen = screen
        self.selected = False
        self.radius = 2.5
        self.hitbox = pygame.Rect(self.x-self.radius, self.y-self.radius, self.radius*2, self.radius*2)
        self.vectors = {
            "gravity": [0, 0],
            "velocity": [0, 0]
        }
        self.gravity_acceleration = 0.027    # acceleration in px/frame
        
        self.on_ground = False
        self.colliding = 0      # -1 -> horizontal, 0 -> no, 1 -> vertical
        self.collison_velocity_loss = 0.5
        self.resultant = [0, 0]
        self.has_collided_with = -1
        
    # controls the shootong of the ball and adds a velocity vector to the ball
    def shoot(self):
        velocity_factor = 0.01
        max_strength = 2.6       # max velocity
        x, y = pygame.mouse.get_pos()
        # x, y offset from object
        rel_x = (x - self.abs_x)*velocity_factor
        rel_y = (y - self.abs_y)*velocity_factor
        strength = math.hypot(rel_x, rel_y)
        if  strength > max_strength:
            rel_x *= max_strength/strength
            rel_y *= max_strength/strength
            strength = max_strength
        
        # shoot power line
        if strength < max_strength/2:        # line color changes based on velocity: g -> low, b -> mid, r -> high
            pygame.draw.line(self.screen, (0, 255 - 255*(strength/(max_strength/2)), 255*(strength/(max_strength/2))), (self.x-1, self.y-1), (x/self.window_scale, y/self.window_scale), 2)
        else:
            pygame.draw.line(self.screen, (255*(((strength-max_strength/2)*2)/max_strength), 0, 255 - 255*(((strength-max_strength/2)*2)/max_strength)), (self.x-1, self.y-1), (x/self.window_scale, y/self.window_scale), 2)
        
        # release shoot
        if pygame.mouse.get_pressed(3)[0] == False:
            self.selected = False
            self.vectors["velocity"] = [-rel_x, -rel_y]
    
    # movement of object
    def move(self):
        for vector in self.vectors:
            self.resultant[0] += self.vectors[vector][0]
            self.resultant[1] += self.vectors[vector][1]
            
        if self.colliding == 1:
            self.resultant[0] *= -(1-self.collison_velocity_loss)
        elif self.colliding == -1:
            self.resultant[1] *= -(1-self.collison_velocity_loss)
        
        if math.hypot(self.resultant[0], self.resultant[1]) < 0.01 or (self.has_collided_with != -1 and math.hypot(self.resultant[0], self.resultant[1]) <= 0.3):
            self.resultant = [0, 0]
            
        self.x += self.resultant[0]
        self.y += self.resultant[1]
        
        self.vectors["velocity"] = [0, 0]
    
    # adds a gravity vector to the ball
    def gravity(self):
        if not self.on_ground:
            self.vectors["gravity"][1] = self.gravity_acceleration
        else:
            self.vectors["gravity"][1] = 0
    
    # reduces tha balls speed based on object it contacts
    def friction(self, friction):
        self.resultant[0] *= (1-friction)
        self.resultant[1] *= (1-friction)
    
    def collision(self, vertical):
        if vertical:
            self.colliding = 1
        else:
            self.colliding = -1
            self.on_ground = True
        
    #draw object and save hitbox
    def update(self):
        self.hitbox = pygame.draw.circle(self.screen, (255, 255, 255), (self.x, self.y), self.radius)