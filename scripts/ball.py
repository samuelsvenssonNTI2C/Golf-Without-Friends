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
    def move(self, hitboxes):
        for vector in self.vectors:
            self.resultant[0] += self.vectors[vector][0]
            self.resultant[1] += self.vectors[vector][1]
            
        collided_with = self.collision(self.resultant, hitboxes)
        
        if math.hypot(self.resultant[0], self.resultant[1]) < 0.01 or (self.rect != -1 and math.hypot(self.resultant[0], self.resultant[1]) <= 0.3):
            self.resultant = [0, 0]
            
        self.x += self.resultant[0]
        self.y += self.resultant[1]
        
        self.vectors["velocity"] = [0, 0]
        
        return collided_with
    
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
    
    def collision(self, delta, hitboxes):
        self.on_ground = False
        test_rect = pygame.Rect([self.hitbox[0] + delta[0], self.hitbox[1] + delta[1], self.hitbox[2], self.hitbox[3]])
        self.rect = test_rect.collidelist(hitboxes)
        if self.rect != -1:
                                # golf_ball.friction(map.materials[current_map['blocks'][rect]['type']]['friction'])
            x, y, w, h = hitboxes[self.rect]
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
                if test_rect.clipline(line):
                    if line[0][1] == line[1][1]:  # if line is horizontal (start y = end y)                        self.resultant[1] = -self.resultant[1]
                        self.on_ground = True
                        self.resultant[1] = -self.resultant[1] * self.collison_velocity_loss
                        print('horizontal collision')
                    elif line[0][0] == line[1][0]:    # if line is vertical (start x = end x)
                        self.resultant[0] = -self.resultant[0] * self.collison_velocity_loss
                        print('vertical collision')
                    break
        return self.rect
        
    #draw object and save hitbox
    def update(self):
        self.hitbox = pygame.draw.circle(self.screen, (255, 255, 255), (self.x, self.y), self.radius)