import pygame
import sys
import json
from scripts.map import Map


class Editor:
    def __init__(self, option, level):
        pygame.init()
        pygame.font.init()
        self.option = option
        self.level = level
        self.screen = pygame.Surface((256, 144))
        self.display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.scale = self.display.get_width() / self.screen.get_width()
    
    def run(self):
        maps = json.load(open('maps.json'))
        sideview = True
        img_load = pygame.image.load
        selected_block = 0
        blocks = [img_load('textures/grass.png')]
        block_type = ['grass']
        map_template = {"side":{"blocks":[{"position":[0.0,-1.0],"type":"grass"},{"position":[1.0,-1.0],"type":"grass"},{"position":[2.0,-1.0],"type":"grass"},{"position":[3.0,-1.0],"type":"grass"},{"position":[4.0,-1.0],"type":"grass"},{"position":[5.0,-1.0],"type":"grass"},{"position":[6.0,-1.0],"type":"grass"},{"position":[7.0,-1.0],"type":"grass"},{"position":[8.0,-1.0],"type":"grass"},{"position":[9.0,-1.0],"type":"grass"},{"position":[10.0,-1.0],"type":"grass"},{"position":[11.0,-1.0],"type":"grass"},{"position":[12.0,-1.0],"type":"grass"},{"position":[13.0,-1.0],"type":"grass"},{"position":[14.0,-1.0],"type":"grass"},{"position":[15.0,-1.0],"type":"grass"},{"position":[16.0,0.0],"type":"grass"},{"position":[16.0,1.0],"type":"grass"},{"position":[16.0,2.0],"type":"grass"},{"position":[16.0,3.0],"type":"grass"},{"position":[16.0,4.0],"type":"grass"},{"position":[16.0,5.0],"type":"grass"},{"position":[16.0,6.0],"type":"grass"},{"position":[16.0,7.0],"type":"grass"},{"position":[16.0,8.0],"type":"grass"},{"position":[15.0,9.0],"type":"grass"},{"position":[14.0,9.0],"type":"grass"},{"position":[13.0,9.0],"type":"grass"},{"position":[12.0,9.0],"type":"grass"},{"position":[11.0,9.0],"type":"grass"},{"position":[10.0,9.0],"type":"grass"},{"position":[9.0,9.0],"type":"grass"},{"position":[8.0,9.0],"type":"grass"},{"position":[7.0,9.0],"type":"grass"},{"position":[6.0,9.0],"type":"grass"},{"position":[5.0,9.0],"type":"grass"},{"position":[4.0,9.0],"type":"grass"},{"position":[3.0,9.0],"type":"grass"},{"position":[2.0,9.0],"type":"grass"},{"position":[1.0,9.0],"type":"grass"},{"position":[0.0,9.0],"type":"grass"},{"position":[-1.0,8.0],"type":"grass"},{"position":[-1.0,7.0],"type":"grass"},{"position":[-1.0,6.0],"type":"grass"},{"position":[-1.0,5.0],"type":"grass"},{"position":[-1.0,4.0],"type":"grass"},{"position":[-1.0,3.0],"type":"grass"},{"position":[-1.0,2.0],"type":"grass"},{"position":[-1.0,1.0],"type":"grass"},{"position":[-1.0,0.0],"type":"grass"}],"goal":"WIP"},"top":{"blocks":[{"position":[5,3],"type":"grass"}],"goal":"WIP"}}

        if self.option == 'e':
            map = Map(self.screen, maps[self.level])
        else:
            map = Map(self.screen, map_template)
        
        while True:
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                        
                    case pygame.KEYUP:
                        match event.key:
                            case pygame.K_ESCAPE:
                                pygame.quit()
                                sys.exit()
                                
                            case pygame.K_f:
                                sideview = not sideview
                                
                            case pygame.K_s:
                                if self.option == 'e':
                                    maps[self.level] = {'side': map.side_map, 'top': map.top_map}
                                else:
                                    maps.append({'side': map.side_map, 'top': map.top_map})
                                    
                                file = open('maps.json', 'w')
                                file.write(json.dumps(maps, indent=4))
                                file.close()
                                    
                    case pygame.MOUSEWHEEL:
                        if selected_block + event.y < len(blocks)-1 and selected_block + event.y > 0:
                            selected_block += event.y
                        
                    case pygame.MOUSEBUTTONUP:
                        if event.button == pygame.BUTTON_LEFT:
                            if sideview:
                                removed = False
                                for object in map.side_map['blocks']:
                                    if object['position'] == [x/16, y/16]:
                                        object_index = map.side_map['blocks'].index(object)
                                        map.side_map['blocks'].pop(object_index)
                                        map.side_hitboxes.pop(object_index)
                                        map.side_textures.pop(object_index)
                                        removed = True
                                if not removed:
                                    map.side_map['blocks'].append({'position': [x/16,y/16], 'type': block_type[selected_block]})
                                    map.side_hitboxes.append(pygame.Rect(x, y, 16, 16))
                                    map.side_textures.append(blocks[selected_block])
                            else:
                                removed = False
                                for object in map.top_map['blocks']:
                                    if object['position'] == [x/16, y/16]:
                                        object_index = map.top_map['blocks'].index(object)
                                        map.top_map['blocks'].pop(object_index)
                                        map.top_hitboxes.pop(object_index)
                                        map.top_textures.pop(object_index)
                                        removed = True
                                if not removed:
                                    map.top_map['blocks'].append({'position': [x/16,y/16], 'type': block_type[selected_block]})
                                    map.top_hitboxes.append(pygame.Rect(x, y, 16, 16))
                                    map.top_textures.append(blocks[selected_block])
                                
            self.screen.fill((100, 100, 100))
            
            x, y = pygame.mouse.get_pos()
            # make x, y snap to 16x16 grid
            base = 16 * self.scale
            x = base * round((x - base/2)/base) / self.scale
            y = base * round((y - base/2)/base) / self.scale
            
            self.screen.blit(blocks[selected_block], (x, y))
            
            
            if sideview:
                map.draw_side()
            else:
                map.draw_top()
            
            self.display.blit(pygame.transform.scale(self.screen, self.display.get_size()), (0, 0))
            pygame.display.update()


option = input('edit or add, e/a: ')
if option == 'e':
    level = input('which map index: ')
else:
    level = '0'
Editor(option, int(level)).run()