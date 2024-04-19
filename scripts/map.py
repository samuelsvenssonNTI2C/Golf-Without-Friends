import pygame

class Map:
    materials = {
        "grass": {
            "friction": 0.15,
            "side_texture": pygame.image.load('textures/grass.png'),
            "top_texture": pygame.image.load('textures/grass.png')
        },
        "ice": {
            "friction": 0.02,
            "side_texture": pygame.image.load('textures/grass.png'),
            "top_texture": pygame.image.load('textures/grass.png')
        }
    }
    
    def __init__(self, screen, dict):
        self.screen = screen
        self.side_map = dict['side']
        self.top_map = dict['top']
        self.side_hitboxes = []
        self.side_textures = []
        self.top_hitboxes = []
        self.top_textures = []
        for map_object in self.side_map['blocks']:            
            rect = pygame.Rect([map_object['position'][0]*16, map_object['position'][1]*16, 16, 16])
            self.side_hitboxes.append(rect)
            self.side_textures.append(Map.materials[map_object['type']]['side_texture'])
            
        for map_object in self.top_map['blocks']:            
            rect = pygame.Rect([map_object['position'][0]*16, map_object['position'][1]*16, 16, 16])
            self.top_hitboxes.append(rect)
            self.top_textures.append(Map.materials[map_object['type']]['side_texture'])
            
    def draw_side(self):
        for object in self.side_hitboxes:
            self.screen.blit(self.side_textures[self.side_hitboxes.index(object)], (object[0], object[1]))
    
    def draw_top(self):
        for object in self.top_hitboxes:
            self.screen.blit(self.top_textures[self.top_hitboxes.index(object)], (object[0], object[1]))