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
        
    def shoot(self):
        velocity_factor = 0.002     # velocity factor
        max_velocity = 0.3          # max velocity
        x, y = pygame.mouse.get_pos()
        # x, y offset from object
        rel_x = x - self.x
        rel_y = y - self.y
        hypotenuse = math.hypot(rel_x, rel_y)
        if hypotenuse != 0:      # divide by zero error
            direction = math.asin(rel_y / hypotenuse)
        velocity = min(hypotenuse*velocity_factor, max_velocity)
        
        # shoot power line
        if velocity < max_velocity/2:        # line color changes based on velocity: g -> low, b -> mid, r -> high
            pygame.draw.line(self.screen, (0, 255 - 255*(velocity/(max_velocity/2)), 255*(velocity/(max_velocity/2))), (self.x, self.y), (x, y), 3)
        else:
            pygame.draw.line(self.screen, (255*(((velocity-max_velocity/2)*2)/max_velocity), 0, 255 - 255*(((velocity-max_velocity/2)*2)/max_velocity)), (self.x, self.y), (x, y), 3)
        
        # release shoot
        if pygame.mouse.get_pressed(3)[0] == False:
            self.selected = False
            if rel_x > 0:
                return (velocity, -direction+math.pi)
            else:
                return (velocity, direction)
        else:
            return (0, 0)
    
    # movement of object
    def move(self, velocity, direction):
        x_movement = velocity*math.cos(direction)
        y_movement = velocity*math.sin(direction)
        self.x += x_movement
        self.y -= y_movement
        velocity -= 0.0001
        return velocity
        
    #draw object and save hitbox
    def update(self):
        self.hitbox = pygame.draw.circle(self.screen, (255, 255, 255), (self.x, self.y), self.radius)
