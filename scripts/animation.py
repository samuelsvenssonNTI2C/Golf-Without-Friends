import os
import pygame

class Animation():
    def __init__(self, screen, folder_name, scale, offsets):
        self.screen = screen
        self.images = []
        self.offsets = offsets
        for image in os.listdir(folder_name):
            self.images.append(pygame.transform.scale_by(pygame.image.load(folder_name + '/' + image), scale))
        self.number_of_frames = len(self.images)
            
    def draw(self, cordinates, frame):
        cordinates = [cordinates[i] + self.offsets[i] for i in range(2)]
        drawing_surface = pygame.Surface(self.images[frame].get_size(), pygame.SRCALPHA, 32)
        drawing_surface = drawing_surface.convert_alpha()
        drawing_surface.fill((0, 0, 0))
        drawing_surface.fill((0, 0, 0, 0))
        drawing_surface.blit(self.images[frame], (0, 0))
        self.screen.blit(drawing_surface, cordinates)
