import pygame

class Map:
    materials = {
        "grass": {
            "color": (0, 255, 0),
            "friction": 0.05
        },
        "ice": {
            "color": (200, 200, 255),
            "friction": 0.02
        }
    }
    
    def __init__(self, screen, dict):
        self.screen = screen
        self.map = dict
        self.hitboxes = []
        for self.map_object in self.map['objects']:
            self.hitboxes.append(pygame.Rect(self.map_object['cordinates']))
        
    def draw(self):
        for self.map_object in self.map['objects']:
            pygame.draw.rect(self.screen, Map.materials[self.map_object['type']]['color'], self.map_object['cordinates'])