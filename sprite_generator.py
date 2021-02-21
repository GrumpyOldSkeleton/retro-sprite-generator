import pygame
import random
import palettes

NUMBER_OF_COLOURS = 4
PIXEL_SIZE  = 4
SPRITES_ACROSS = 16
SPRITES_DOWN = 8
SPRITE_SPACING = 10
SPRITE_WIDTH = 10
SPRITE_HEIGHT = 6
SPACING_X = (SPRITE_WIDTH + SPRITE_SPACING) * PIXEL_SIZE
SPACING_Y = (SPRITE_HEIGHT + SPRITE_SPACING) * PIXEL_SIZE
MARGIN_X = (SPRITE_WIDTH * PIXEL_SIZE) // 2
MARGIN_Y = (SPRITE_HEIGHT * PIXEL_SIZE) // 2

SCREEN_WIDTH = SPACING_X * SPRITES_ACROSS
SCREEN_HEIGHT = SPACING_Y * SPRITES_DOWN

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()




class Ship():
    
    def __init__(self, n, x, y):

        self.highlight = False
        self.number = n
        self.offx = x
        self.offy = y
        self.width = SPRITE_WIDTH * PIXEL_SIZE
        self.height = SPRITE_HEIGHT * PIXEL_SIZE
        self.image = []
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = pygame.Rect(MARGIN_X + self.offx, MARGIN_Y + self.offy, self.width, self.height)
        self.palette = []
        
    def makePalette(self):
        
        self.palette = random.sample(palettes.COLOUR_PALETTE, NUMBER_OF_COLOURS)
            
    def render(self):
        
        x = 0
        y = 0

        for line in self.image:
            for pixel in line:
                pygame.draw.rect(self.surface, pixel, [x, y, PIXEL_SIZE, PIXEL_SIZE])
                x += PIXEL_SIZE
            y += PIXEL_SIZE
            x = 0
            
    def backfill(self):
        
        self.image = []        

        for n in range(0, SPRITE_HEIGHT):
            line = [palettes.COLOUR_BACKGROUND_MASK for i in range(0,SPRITE_WIDTH)]
            self.image.append(line)
            
    def makeIt(self):
        
        for line in self.image:
            for n in range(0, SPRITE_WIDTH // 2):
                colour = palettes.COLOUR_BLACK
                x = random.random()
                if x < 0.4:
                    colour = self.palette[random.randint(0,len(self.palette)-1)]
                line[n] = colour
                line[-n-1] = colour
        
    def generate(self):
        
        self.makePalette()
        self.backfill()
        self.makeIt()    
        self.render()

    def draw(self):
        
        screen.blit(self.surface, (MARGIN_X + self.offx, MARGIN_Y + self.offy))
        
        if self.highlight:
            pygame.draw.rect(screen, (255,0,0), [MARGIN_X + self.offx, MARGIN_Y + self.offy, self.width, 4])
            

class SpriteSheet():
    
    def __init__(self):
        
        self.ships = []
        
    def render(self):
        
        self.ships = []
        n = 0
        for y in range(0, SPRITES_DOWN):
            for x in range(0, SPRITES_ACROSS):
                ship = Ship(n, x * SPACING_X, y * SPACING_Y)
                ship.generate()
                self.ships.append(ship)
                n += 1

    def draw(self):
        
        for ship in self.ships:
            ship.draw()

    def getSpriteAt(self, mx, my):
        
        for ship in self.ships:
            if ship.rect.collidepoint((mx, my)):
                ship.highlight = not ship.highlight
    

random.seed(1)

spritesheet = SpriteSheet()
spritesheet.render()
    
running = True
while running:
    
    mousex, mousey = pygame.mouse.get_pos()
    
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                running = False
            elif (e.key == pygame.K_SPACE):
                spritesheet.render()
            
        if e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 1: # left click
                spritesheet.getSpriteAt(mousex, mousey)
            
    screen.fill((0, 0, 0))
    
    spritesheet.draw()
        
    clock.tick(60)
    pygame.display.flip()

