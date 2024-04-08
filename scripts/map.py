import pygame

class Map:
    materials = {
        "grass": {
            "color": (0, 255, 0),
            "friction": 0.1
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
            fractions = self.map_object['fractions']
            cordinates = pygame.Rect([fractions[0]*self.screen.get_width(), fractions[1]*self.screen.get_height(), fractions[2]*self.screen.get_width(), fractions[3]*self.screen.get_height()])
            cordinates.normalize()
            self.hitboxes.append(cordinates)
        
    def draw(self):
        for self.map_object in self.map['objects']:
            fractions = self.map_object['fractions']
            cordinates = pygame.Rect([fractions[0]*self.screen.get_width(), fractions[1]*self.screen.get_height(), fractions[2]*self.screen.get_width(), fractions[3]*self.screen.get_height()])
            cordinates.normalize()
            pygame.draw.rect(self.screen, Map.materials[self.map_object['type']]['color'], cordinates)