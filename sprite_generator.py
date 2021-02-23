import pygame
import random
import palettes
import masks

# -----------------------------------------------------------
# settings 
# -----------------------------------------------------------

# choose which palette to use
PALETTE = palettes.PALETTE_PICO8

# set the number of colours to randomly pick from the palette
# for each sprite
NUMBER_OF_COLOURS = 3

# the visual scale of the each pixel on screen
# 3 or 4 looks good
PIXEL_SIZE = 4

# the actual size of the sprite
SPRITE_WIDTH = 10
SPRITE_HEIGHT = 8

# the sprite mask to use. 
# the mask constrains the shape of the sprite
# set to None if not using mask
SPRITE_MASK = masks.MASK_6X10_NARROW_WAIST 

# the number of sprites on the spritesheet
SPRITES_ACROSS = 8
SPRITES_DOWN = 8

# -----------------------------------------------------------
# end settings
# -----------------------------------------------------------

# the spacing between sprites in actual pixels
SPRITE_SPACING = 10
SPACING_X = (SPRITE_WIDTH + SPRITE_SPACING) * PIXEL_SIZE
SPACING_Y = (SPRITE_HEIGHT + SPRITE_SPACING) * PIXEL_SIZE
MARGIN_X  = (SPRITE_WIDTH * PIXEL_SIZE) // 2
MARGIN_Y  = (SPRITE_HEIGHT * PIXEL_SIZE) // 2

SCREEN_WIDTH  = SPACING_X * SPRITES_ACROSS
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
        
        self.palette = random.sample(PALETTE, NUMBER_OF_COLOURS)
        
    def setPalette(self, p):
        
        self.palette = p
        
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
    
    def getThreshold(self, x, y):
        
        # higher values of t returned mean more likely to colour cell
        t = 0.7
                
        if x == 0:
            t -= 0.1 # edge cells are more likely to stay black
        elif x == 1:
            t -= 0.05 # 2nd row in from edge slightly less likely
            
        if y == 0 or y == SPRITE_HEIGHT-1: # bias top/bottom rows to be more black
            t -= 0.1
            
        # if using a mask
        if SPRITE_MASK is not None:
            
            try:
                if SPRITE_MASK[y][x] == 0:
                    t -= 0.5
            except IndexError:
                # ignore mask not fitting
                pass

        return t
        
    def makeIt(self):
        
        for y, line in enumerate(self.image):
            for x in range(0, SPRITE_WIDTH // 2):
                r = random.random()
                
                threshold = self.getThreshold(x,y)
                    
                if r < threshold:
                    colour = self.palette[random.randint(0,len(self.palette)-1)]
                    line[x] = colour
                    line[-x-1] = colour
        
    def generate(self):
        
        if len(self.palette) == 0:
            self.makePalette()
            
        self.backfill()
        self.makeIt()    
        self.render()

    def draw(self):
        
        screen.blit(self.surface, (MARGIN_X + self.offx, MARGIN_Y + self.offy))
        
        if self.highlight:
            pygame.draw.rect(screen, (255,255,255), [MARGIN_X + self.offx - 10, MARGIN_Y + self.offy - 10, self.width + 20, self.height + 20], 1)
            

class SpriteSheet():
    
    def __init__(self):
        
        self.ships = []
        self.selected = []
        self.selected_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.show_selected = False
        self.seed = 1
        
    def stepSeed(self, n):
        
        self.seed += n
        random.seed(self.seed)
        
    def render(self):
        
        self.stepSeed(1)
        
        self.ships = []
        n = 0
        for y in range(0, SPRITES_DOWN):
            for x in range(0, SPRITES_ACROSS):
                ship = Ship(n, x * SPACING_X, y * SPACING_Y)
                ship.generate()
                self.ships.append(ship)
                n += 1

    def drawSelected(self):
        
        self.selected_surface.fill(palettes.COLOUR_BACKGROUND_MASK)

        offsetx = 0
        offsety = 0

        for image in self.selected:
            
            x = 0
            y = 0
            
            for line in image:
                for pixel in line:
                    pygame.draw.rect(self.selected_surface, pixel, [offsetx + x, offsety + y, PIXEL_SIZE, PIXEL_SIZE])
                    x += PIXEL_SIZE
                y += PIXEL_SIZE
                x = 0
                
            offsetx += (SPRITE_WIDTH * PIXEL_SIZE) + 10
            
            if offsetx >= SCREEN_WIDTH:
                offsety += (SPRITE_HEIGHT * PIXEL_SIZE) + 10
                offsetx = 0
                
        screen.blit(self.selected_surface, (0,0))
        
    def draw(self):
        
        if self.show_selected:
            self.drawSelected()
        else:
            for ship in self.ships:
                ship.draw()

    def getSpriteAt(self, mx, my):
        
        for ship in self.ships:
            if ship.rect.collidepoint((mx, my)):
                ship.highlight = not ship.highlight
                if ship.highlight:
                    copyimage = ship.image[:]
                    self.selected.append(copyimage)
                else:
                    self.selected.remove(ship.image)
                


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
            elif (e.key == pygame.K_p):
                spritesheet.show_selected = not spritesheet.show_selected
            elif (e.key == pygame.K_s):
                #pygame.image.save(spritesheet.selected_surface, 'save.png')
                pygame.image.save(screen, 'save_screen.png')
                
            
        if e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 1: # left click
                spritesheet.getSpriteAt(mousex, mousey)
            
    screen.fill((0, 0, 0))
    
    spritesheet.draw()
        
    clock.tick(60)
    pygame.display.flip()

