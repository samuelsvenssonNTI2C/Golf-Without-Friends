import pygame
import math
import time

class Ball():
    def __init__(self, screen, window_scale, start_cordinates):
        self.x, self.y = start_cordinates
        self.depth = screen.get_height()/2
        self.window_scale = window_scale
        self.abs_x, self.abs_y = [cord * window_scale for cord in start_cordinates]        
        self.screen = screen
        self.selected = False
        self.has_been_selected = False
        self.radius = 2
        self.hitbox = pygame.Rect(self.x-self.radius, self.y-self.radius, self.radius*2, self.radius*2)
        self.vectors = {
            "gravity": [0, 0],
            "velocity": [0, 0]
        }
        self.gravity_acceleration = 0.027    # acceleration in px/frame
        
        self.on_ground = False
        self.collision_rect = -1
        self.collison_velocity_loss = 0.5
        self.resultant = [0, 0]
        self.in_block = False
        self.shots = 0
        
    # controls the shootong of the ball and adds a velocity vector to the ball
    def shoot(self):
        velocity_factor = 0.010
        max_strength = 2       # max velocity
        x, y = pygame.mouse.get_pos()
        if not self.has_been_selected:
            self.start_x, self.start_y = pygame.mouse.get_pos()
        self.has_been_selected = True
        # x, y offset from object
        rel_x = (x - self.start_x)*velocity_factor
        rel_y = (y - self.start_y)*velocity_factor
        strength = math.hypot(rel_x, rel_y)
        if strength > max_strength:
            rel_x *= max_strength/strength
            rel_y *= max_strength/strength
            strength = max_strength
        
        # shoot power line
        if strength < max_strength/2:        # line color changes based on velocity: g -> low, b -> mid, r -> high
            pygame.draw.line(self.screen, (0, 255 - 255*(strength/(max_strength/2)), 255*(strength/(max_strength/2))), (self.start_x/self.window_scale - 1, self.start_y/self.window_scale - 1), (x/self.window_scale, y/self.window_scale), 2)
        else:
            pygame.draw.line(self.screen, (255*(((strength-max_strength/2)*2)/max_strength), 0, 255 - 255*(((strength-max_strength/2)*2)/max_strength)), (self.start_x/self.window_scale - 1, self.start_y/self.window_scale - 1), (x/self.window_scale, y/self.window_scale), 2)
        pygame.draw.circle(self.screen, (255, 255, 255), (self.start_x/self.window_scale, self.start_y/self.window_scale), self.radius*0.5)
        
        # release shoot
        if pygame.mouse.get_pressed(3)[0] == False:
            self.selected = False
            self.has_been_selected = False
            self.vectors["velocity"] = [-rel_x, -rel_y]
            self.shots += 1
    
    # movement of the ball
    def move(self, hitboxes, map):
        collided_with = -1
        
        for vector in self.vectors:
            self.resultant[0] += self.vectors[vector][0]
            self.resultant[1] += self.vectors[vector][1]
        
        if math.hypot(self.resultant[0], self.resultant[1]) < self.gravity_acceleration or (self.on_ground and math.hypot(self.resultant[0], self.resultant[1]) <= 0.3):
            self.resultant = [0, 0]
        else:
            self.collision('x', hitboxes, map)
            if self.collision_rect != -1:
                collided_with = self.collision_rect
            self.x += self.resultant[0]
            self.collision('y', hitboxes, map)
            if self.collision_rect != -1 and (map['blocks'][collided_with]['type'] != 'victory_block' or collided_with == -1):
                collided_with = self.collision_rect
            self.y += self.resultant[1]
            self.abs_x = self.x * self.window_scale
            self.abs_y = self.y * self.window_scale
        
        self.vectors["velocity"] = [0, 0]

        return collided_with
    
    # adds a gravity vector to the ball
    def gravity(self):
        if not self.on_ground:
            self.vectors["gravity"][1] = self.gravity_acceleration
        else:
            self.vectors["gravity"][1] = 0
    
    # reduces the balls speed based on object it contacts
    def friction(self, friction):
        friction *= 1 if self.in_block else 1
        self.resultant[0] *= (1-friction)
        self.resultant[1] *= (1-friction)
    
    def collision(self, direction, hitboxes, map):
        self.collision_rect = -1
        
        if self.hitbox.collidelist(hitboxes) == -1:
            self.in_block = False
            
        if direction == 'x':
            test_rect = pygame.Rect([self.hitbox[0] + round_away_from_zero(self.resultant[0]), self.hitbox[1], self.hitbox[2], self.hitbox[3]])
            self.collision_rect = test_rect.collidelist(hitboxes)
            if self.collision_rect != -1 and (map['blocks'][self.collision_rect]['type'] != map['blocks'][self.hitbox.collidelist(hitboxes)]['type'] or self.hitbox.collidelist(hitboxes) == -1):
                    self.resultant[0] = -self.resultant[0] * self.collison_velocity_loss
        
        if direction == 'y':
            test_rect = pygame.Rect([self.hitbox[0], self.hitbox[1] + round_away_from_zero(self.resultant[1]), self.hitbox[2], self.hitbox[3]])
            self.collision_rect = test_rect.collidelist(hitboxes)
            if self.collision_rect != -1 and (map['blocks'][self.collision_rect]['type'] != map['blocks'][self.hitbox.collidelist(hitboxes)]['type'] or self.hitbox.collidelist(hitboxes) == -1):
                self.resultant[1] = -self.resultant[1] * self.collison_velocity_loss
    
            self.on_ground = self.hitbox.move(0, 1).collidelist(hitboxes) != -1 and (map['blocks'][self.collision_rect]['type'] != map['blocks'][self.hitbox.collidelist(hitboxes)]['type'] or self.hitbox.collidelist(hitboxes) == -1)
        
    #draw object and save hitbox
    def update(self):
        self.hitbox = pygame.draw.circle(self.screen, (255, 255, 255), (self.x, self.y), self.radius)

def round_away_from_zero(var):
    if var < 0:
        return math.floor(var)
    elif var > 0:
        return math.ceil(var)
    else:
        return 0
    