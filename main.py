# - Imports - #
import pygame
import os

# - Inits - #
pygame.init()
clock = pygame.time.Clock()

# - Create window - #
global display_width,display_height,scale

def setSize(x: int,y: int):
    global display_width,display_height
    (display_width,display_height) = (x,y)
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    return pygame.display.set_mode((display_width, display_height))

def setScale(_scale: int):
    global scale
    scale = _scale
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    return pygame.display.set_mode((scale*display_width, scale*display_height))

display = setSize(10,10)
setScale(1)
pygame.display.set_caption('Conway\'s PyGame of Life')
# - Create window - #

# - Load assets - #
# - Load assets - #

# - Load controls - #
controls = {
}
# - Load controls - #

# - Define variables - # 
frameRate = 60
(screenGridWidth,screenGridHeight) = (24,16)
# - Define variables - # 

# - Main game loop - #
setSize(8*screenGridWidth+1,8*screenGridHeight+1)
setScale(4)
replay = True
while replay:
    running = True
    closed = False
    paused = False
    while running and not closed:
        clock.tick(frameRate)
        for event in pygame.event.get():
            # Detect window closed
            if event.type == pygame.QUIT:
                closed = True
                replay = False
        # - Rendering - #
            screen = pygame.surface.Surface((display_width,display_height))
            screen.fill((0,0,0))
            scaled = pygame.transform.scale(screen, display.get_size())
            display.blit(scaled, (0, 0))
            # - Grid - #
            for x in range(screenGridWidth):
                pygame.draw.line(display, (200,200,200), (8*scale*x,0), (8*scale*x,display_height*scale))
            pygame.draw.line(display, (200,200,200), (display_width*scale-1,0), (display_width*scale-1,display_height*scale))
            # - Grid - #
            pygame.display.flip()