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
        self.frame = 0
            
    def draw(self, cordinates):
        cordinates = [cordinates[i] + self.offsets[i] for i in range(2)]
        drawing_surface = pygame.Surface(self.images[self.frame].get_size(), pygame.SRCALPHA, 32)
        drawing_surface = drawing_surface.convert_alpha()
        drawing_surface.fill((0, 0, 0))
        drawing_surface.fill((0, 0, 0, 0))
        drawing_surface.blit(self.images[self.frame], (0, 0))
        self.screen.blit(drawing_surface, cordinates)
        if self.frame < len(self.images)-1:
            self.frame += 1
            return False
        else:
            self.frame = 0
            return True