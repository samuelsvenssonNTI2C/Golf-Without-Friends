import pygame

class Map:
    materials = {
        "grass": {
            "friction": 0.15,
            "texture": pygame.image.load('textures/grass.png')
        },
        "ice": {
            "friction": 0.02,
            "texture": pygame.image.load('textures/grass.png')
        }
    }
    
    def __init__(self, screen, dict):
        self.screen = screen
        self.map = dict
        self.hitboxes = []
        self.textures = []
        for map_object in self.map['blocks']:            
            rect = pygame.Rect([map_object['position'][0]*16, map_object['position'][1]*16, 16, 16])
            self.hitboxes.append(rect)
            self.textures.append(Map.materials[map_object['type']]['texture'])
            
    def draw(self):
        for object in self.hitboxes:
            self.screen.blit(self.textures[self.hitboxes.index(object)], (object[0], object[1]))