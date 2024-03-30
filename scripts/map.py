import pygame

class Map:
    def __init__(self, screen, dict):
        self.screen = screen
        self.map = dict
        self.hitboxes = []
        for self.map_object in self.map['objects']:
            self.hitboxes.append(pygame.Rect(self.map_object['cordinates']))
        
    def draw(self):
        for self.map_object in self.map['objects']:
            pygame.draw.rect(self.screen, self.map_object['color'], self.map_object['cordinates'])