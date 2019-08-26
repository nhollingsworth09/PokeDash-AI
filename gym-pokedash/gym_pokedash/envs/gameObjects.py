"""
This module houses the game's moving objects
"""
import pygame 

class Player():
    def __init__(self, win, x, y):
        self.sprites = Spritesheet('./sprites/pikachu_running_bw.png', 4, 1)
        self.x = x
        self.y = y
        self.initY = y
                
        self.score = 0
        self.height = self.sprites.cellHeight
        self.width = self.sprites.cellWidth
        self.isJump = False
        self.isDead = False
        self.jumpCount = 9
        self.hitbox = (self.x + 15, self.y, self.width, self.height)
        self.rect = (self.x, self.y, self.x + self.width - 15, self.y + self.height)

        self.line = pygame.draw.line(win,
                                     (0,255,0), (75, (self.rect[1] + self.rect[3])/2),
                                     (1000, (self.rect[1] + self.rect[3])/2),
                                     1)

    
    def draw(self, win, cellIndex):
        
        #-- Update edges during run loop
        self.hitbox = (self.x + 20, self.y +5, self.width - 25  , self.height - 10)
        self.rect = (self.x, self.y, self.x + self.hitbox[2], self.y + self.hitbox[3])
        
        win.blit(self.sprites.sheet, (self.x, self.y), self.sprites.cells[cellIndex])

class Cactus():
    def __init__(self, path, x, y, vel, version):
        self.cactusIdx = version
        self.image = [pygame.image.load('./assets/cactus%s.png' % frame) for frame in range(1,4)]
        
        #-- Rescaling
        for img in range(0,3):
            if img == 0:
                self.image[img] = pygame.transform.scale(self.image[img], (30,60))
            elif img == 1:
                self.image[img] = pygame.transform.scale(self.image[img], (50,60))
            elif img == 2:
                self.image[img] = pygame.transform.scale(self.image[img], (72,48))
            
        
        #-- Obsticle generated off-screen then scrolls in
        self.x = x
        self.y = y
        
        self.width = 0
        self.height = 0
        
        if self.cactusIdx == 0:
            self.rightx = self.x + 60
        elif self.cactusIdx == 1:
            self.rightx = self.x + 60
        elif self.cactusIdx == 2:
            self.rightx = self.x + 40

        #-- Align cactus vertically
        if self.cactusIdx == 0 or self.cactusIdx == 1:
            self.y = self.y + 55
        if self.cactusIdx == 2: 
            self.y = self.y + 70
            
        self.initX = self.x
        self.onScreen = True
        self.vel = vel
    
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.rect = (self.x, self.y, self.x + self.hitbox[2], self.y + self.hitbox[3])
        self.onScreen = True
        
    def draw(self, win):        
        
        #-- Define right edge of cactus
        if self.cactusIdx == 0:
            self.width = self.image[self.cactusIdx].get_rect().width
            self.height = self.image[self.cactusIdx].get_rect().height
        elif self.cactusIdx == 1:
            self.width = self.image[self.cactusIdx].get_rect().width
            self.height = self.image[self.cactusIdx].get_rect().height
        elif self.cactusIdx == 2:
            self.width = self.image[self.cactusIdx].get_rect().width
            self.height = self.image[self.cactusIdx].get_rect().height
        
        #-- Update edges during run loop
        self.rect = (self.x, self.y, self.x + self.width, self.y + self.height)
        self.hitbox = (self.x, self.y, self.width, self.height)

        win.blit(self.image[self.cactusIdx], (self.x, self.y))

class Scoreboard():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.value = 0
        self.font = pygame.font.SysFont('comicsans', 20, True)

class Background():
    def __init__(self, path, x, y, vel):
        self.bg = pygame.image.load(path)
        self.x = x
        self.y = y
        
        
        self.initX = x
        self.rightx = self.x + 1200
        self.vel = vel
        
        self.rect = self.bg.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height

    def bg_draw(self, win):
        if self.rightx <= 0:
            self.x = 1200
            self.rightx = self.x + 1200
            
        win.blit(self.bg, (self.x, self.y))

class Spritesheet():
	def __init__(self, filepath, cols, rows):
		self.sheet = pygame.image.load(filepath).convert_alpha()
		
		self.cols = cols
		self.rows = rows
		self.totalCellCount = cols * rows

		#Gets the dimensions of cell sheet		
		self.rect = self.sheet.get_rect()

		self.cellWidth = self.rect.width / cols
		self.cellHeight = self.rect.height / rows
		self.cellCenter = (self.cellWidth/2, self.cellHeight/2)

		#Create a list of cells/sprites
		self.cells = list([((index % cols) * self.cellWidth, int(index / cols)* self.cellHeight, self.cellWidth, self.cellHeight) for index in range(self.totalCellCount)])
		