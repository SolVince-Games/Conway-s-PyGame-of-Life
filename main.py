# - Imports - #
from copy import deepcopy
import pygame
from os import environ as osEnviron

# - Inits - #
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()

# - Create window - #
global display_width,display_height,scale

def setSize(x: int,y: int):
    global display_width,display_height
    (display_width,display_height) = (x,y)
    osEnviron['SDL_VIDEO_CENTERED'] = '1'
    return pygame.display.set_mode((display_width, display_height))

screen = setSize(10,10)
pygame.display.set_caption('Conway\'s PyGame of Life')
# - Create window - #

# - Load assets - #
assets = {
    'images':{
        'buttons':{
            'unpressed':{
                'back':pygame.image.load(f'images/back.png').convert_alpha(),
                'forward':pygame.image.load(f'images/forward.png').convert_alpha(),
                'play':pygame.image.load(f'images/play.png').convert_alpha(),
                'pause':pygame.image.load(f'images/pause.png').convert_alpha(),
                'pencil':pygame.image.load(f'images/pencil.png').convert_alpha(),
                'eraser':pygame.image.load(f'images/eraser.png').convert_alpha()
            },
            'pressed':{
                'back':pygame.image.load(f'images/back_pressed.png').convert_alpha(),
                'forward':pygame.image.load(f'images/forward_pressed.png').convert_alpha(),
                'play':pygame.image.load(f'images/play_pressed.png').convert_alpha(),
                'pause':pygame.image.load(f'images/pause_pressed.png').convert_alpha(),
                'pencil':pygame.image.load(f'images/pencil_pressed.png').convert_alpha(),
                'eraser':pygame.image.load(f'images/eraser_pressed.png').convert_alpha()
            }
        },
        'cursors':{
            'add':pygame.image.load(f'images/cursor_add.png').convert_alpha(),
            'kill':pygame.image.load(f'images/cursor_kill.png').convert_alpha(),
        }
    }
}
mouseSpriteRect = assets['images']['cursors']['add'].get_rect()
# - Load assets - #

# - Load controls - #
controls = {
}
# - Load controls - #

# - Define variables - # 
frameRate = 60
(screenGridWidth,screenGridHeight) = (24,16)
# - Define variables - # 

# - Tiles - #
Tiles = {}
class Tile():
    def __init__(self,pos) -> None:
        global Tiles
        self.pos = pos
        Tiles[self.pos] = self
    def kill(self):
        Tiles.pop(self.pos)
def getTileAlive(pos: tuple):
    if pos in Tiles.keys():
        return Tiles[pos]
    else:
        return None
def addTile(pos: tuple):
    Tiles[pos] = Tile(pos)
# - Tiles - #

# - Gui Buttons - #
GuiButtonsGroup = pygame.sprite.Group()
GuiButtons = {}
class GuiButton():
    def __init__(self,id,i) -> None:
        self.sprite = pygame.sprite.Sprite()
        self.sprite.unpressedImage = assets['images']['buttons']['unpressed'][id]
        self.sprite.pressedImage = assets['images']['buttons']['pressed'][id]
        self.sprite.image = self.sprite.unpressedImage
        self.sprite.rect = self.sprite.image.get_rect()
        self.sprite.rect.topleft = (210+i*(60+12),524)
        self.pressed = False
        self.id = id
    def setPressing(self,value: bool):
        if value:
            self.sprite.image = self.sprite.pressedImage
        else:
            self.sprite.image = self.sprite.unpressedImage
for i,id in enumerate('back play pause forward pencil eraser'.split(' ')):
    playPauseGap = 0
    if i > 1:
        playPauseGap = 1
    button = GuiButton(id,i-playPauseGap)
    GuiButtons[id] = (button)
    if i != 2:
        GuiButtonsGroup.add(button.sprite)

my_font = pygame.font.SysFont('Comic Sans MS', 30)

# - Main game loop - #
setSize(32*screenGridWidth+1,32*screenGridHeight+1+83)
replay = True
while replay:
    running = True
    closed = False
    paused = True
    editing = False
    visibleTopLeft = (0,0)
    step = 0
    Steps = {0:deepcopy(Tiles)}
    stepsPerSecond = 1
    frame = 0
    while running and not closed:
        clock.tick(frameRate)
        # - Events - #
        for event in pygame.event.get():
            # - Detect window closed - #
            if event.type == pygame.QUIT:
                closed = True
                replay = False
            # - Detect window closed - #
            # - Input - #
            mousebuttons = pygame.mouse.get_pressed()
            mousePos = pygame.mouse.get_pos()
            for button in GuiButtons.values():
                button.setPressing(mousebuttons[0] == 1 and button.sprite.rect.collidepoint(mousePos) and (button.sprite in GuiButtonsGroup.sprites()))
            if event.type == pygame.MOUSEBUTTONUP:
                for button in GuiButtons.values():
                    button.pressed = button.sprite.rect.collidepoint(mousePos) and (button.sprite in GuiButtonsGroup.sprites())
                    if button.pressed:
                        print(f'{button.id} pressed!')
                if editing:
                    clickedTilePos = (mousePos[0] // 32,mousePos[1] // 32)
                    if (clickedTilePos[0] >= 0 and clickedTilePos[0] < screenGridWidth) and (clickedTilePos[1] >= 0 and clickedTilePos[1] < screenGridHeight):
                        tilePos = (visibleTopLeft[0]+clickedTilePos[0],visibleTopLeft[1]+clickedTilePos[1])
                        if editing == 'add':
                            addTile(tilePos)
                        elif getTileAlive(tilePos):
                            getTileAlive(tilePos).kill()
            # - Input - # 
        # - Events - #
        # - Game Logic - #
            # -  Input - #
        for id,button in GuiButtons.items():
            if button.pressed:
                if not id in ['pencil','eraser']:
                    editing = False
                else:
                    editing = {'pencil':'add','eraser':'kill'}[id]
                if id == 'back':
                    step -= 1
                    if step < 0: step = 0
                    if not step in Steps.keys():
                        Steps[step] = deepcopy(Tiles)
                    else:
                        Tiles = Steps[step]
                elif id == 'forward':
                    step += 1
                    if step < 0: step = 0
                    if not step in Steps.keys():
                        Steps[step] = deepcopy(Tiles)
                    else:
                        Tiles = Steps[step]
                if id == 'play':
                    paused = False
                else:
                    paused = True
                    frame = 0
        if paused:
            GuiButtonsGroup.remove(GuiButtons['pause'].sprite)
            GuiButtonsGroup.add(GuiButtons['play'].sprite)
        else:
            GuiButtonsGroup.remove(GuiButtons['play'].sprite)
            GuiButtonsGroup.add(GuiButtons['pause'].sprite)
        for id,button in GuiButtons.items():
            button.pressed = False
        # -  Input - #
        
        if not step in Steps.keys() or Steps[step] != Tiles:
            Steps[step] = deepcopy(Tiles)
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            print(list(Steps[step].keys()))

        # - Game Logic - #
        # - Rendering - #
            # - Layer Setup - #
        screen.fill((0,0,0))
        GuiLayer = pygame.Surface((display_width,display_height)).convert_alpha()
        GuiLayer.fill((0,0,0,0))
        maxTileX = screenGridWidth-1
        maxTileY = screenGridHeight-1
        if len(Steps[step].keys()) > 0:
            maxTileX = max(max([pos[0] for pos in Steps[step].keys()]),maxTileX)
            maxTileY = max(max([pos[1] for pos in Steps[step].keys()]),maxTileY)
        GameLayer = pygame.Surface((32*(maxTileX+1),32*(maxTileY+1))).convert_alpha()
        GameLayer.fill((0,0,0,0))
            # - Layer Setup - #
            # - Custom Cursor - #
        if editing:
            pygame.mouse.set_visible(False)
            mouseSpriteRect.topleft = pygame.mouse.get_pos()
            # - Custom Cursor - #
            # - Tiles - #
        for pos,tile in Steps[step].items():
            pygame.draw.rect(GameLayer,(200,200,200), pygame.Rect(32*pos[0], 32*pos[1], 32, 32))
            # - Tiles - #
            # - Grid - #
        for x in range(screenGridWidth):
            pygame.draw.line(GuiLayer, (255,255,255), (32*x,0), (32*x,display_height-83-1))
        pygame.draw.line(GuiLayer, (255,255,255), (display_width-1,0), (display_width-1,display_height-83-1))
        for y in range(screenGridHeight):
            pygame.draw.line(GuiLayer, (255,255,255), (0,32*y), (display_width,32*y))
        pygame.draw.line(GuiLayer, (255,255,255), (0,display_height-83-1), (display_width,display_height-83-1))
            # - Grid - #
            # - GUI Bar - #
        pygame.draw.line(GuiLayer, (255,255,255), (0,display_height-82), (display_width,display_height-82), 3)
        pygame.draw.line(GuiLayer, (255,255,255), (0,display_height-3), (display_width,display_height-3), 4)
        pygame.draw.line(GuiLayer, (255,255,255), (display_width-3,display_height-82), (display_width-3,display_height), 4)
        pygame.draw.line(GuiLayer, (255,255,255), (1,display_height-82), (1,display_height), 4)
        GuiButtonsGroup.draw(GuiLayer)
            # - GUI Bar - #

        if editing == 'add':
            pygame.draw.circle(GuiLayer,(0,255,0,128),(16,16),15)
        elif editing == 'kill':
            pygame.draw.circle(GuiLayer,(255,0,0,128),(16,16),15)
        text_surface = my_font.render(str(step), False, (0, 0, 255))
        GuiLayer.blit(text_surface,(display_width-text_surface.get_width(),0))
        temp = text_surface.get_height()
        text_surface = my_font.render(str(stepsPerSecond), False, (0, 0, 255))
        GuiLayer.blit(text_surface,(display_width-text_surface.get_width(),temp))

        screen.blit(GameLayer,(0-visibleTopLeft[0]*32,0-visibleTopLeft[1]*32))
        screen.blit(GuiLayer,(0,0))
        if editing:
            screen.blit(assets['images']['cursors'][editing],mouseSpriteRect)
        pygame.display.flip()
        # - Rendering - #
        if not paused:
            if frame == (frameRate // stepsPerSecond):
                step += 1
                if not step in Steps.keys():
                    Steps[step] = deepcopy(Tiles)
                else:
                    Tiles = Steps[step]
            frame += 1
            if frame > frameRate:
                frame = 00