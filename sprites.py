import pygame
from config import *
import random

class Lion(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        #need to add hunger, thirst, mating to all animals which dictates their movement - hunger move to prey animal - thirst move towards water - mate -move towards female/male counterpart 
        self.groups = game.all_sprites, game.boundary
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.game =game
        self.image = pygame.image.load("images/lion.png").convert()
        self.image = pygame.transform.scale(self.image,(GRIDWIDTH,GRIDHEIGHT))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.neighbors = []
        self.rect.x = x*GRIDWIDTH
        self.rect.y = y*GRIDHEIGHT
        self.hunger_limit = max_hunger_limit
        self.hunting = False 
        self.can_hunt = False
        self.thirst_limit = max_thirst_limit
        self.closest_water = ()
        self.thirsty = True
        self.can_breed = False
        self.breeding = False
        self.breeding_cooldown = 100
        self.gender = random.choice(['m','f'])

    def move(self, dx=0, dy=0):
        if not self.collide_with_walls(dx,dy):
            self.x += dx
            self.y += dy

    def getlocation(self):
        return (self.x, self.y)
    
    def get_neighbors(self):
        self.neighbors = []
        self.neighbors.append((self.x+1,self.y))
        self.neighbors.append((self.x-1,self.y))
        self.neighbors.append((self.x,self.y+1))
        self.neighbors.append((self.x,self.y-1))

        return self.neighbors
            
    def collide_with_walls(self, dx=0, dy=0):
        for  bound in self.game.boundary:
            if bound.x == self.x + dx and bound.y == self.y + dy:
                return True
        for mount in self.game.mountain:
            if mount.x == self.x + dx and mount.y == self.y + dy:
                return True
        for w in self.game.water:
            if w.x == self.x + dx and w.y == self.y + dy:
                return True       
        return False

    def update(self):
        self.rect.x = self.x * GRIDWIDTH
        self.rect.y = self.y * GRIDHEIGHT

    def hunt(self):
        if self.hunger_limit<10:
            #locate nearest prey
            #dont do anything 
            self.hunting = True
            pass

    def drink(self):    
        self.thirst = False
        self.thirst_limit = max_thirst_limit

    def breed(self):
        if self.can_breed and self.breeding:
            #then cannot breed 
            pass
        else: 
            #start looking for the nearest female. 
            pass

class Wolf(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.boundary
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.game =game
        self.image = pygame.image.load("images/wolf.png").convert()
        self.image = pygame.transform.scale(self.image,(GRIDWIDTH,GRIDHEIGHT))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x*GRIDWIDTH
        self.rect.y = y*GRIDHEIGHT

    def move(self, dx=0, dy=0):
        if not self. collide_with_walls(dx,dy):
            self.x += dx
            self.y += dy

    def collide_with_walls(self, dx=0, dy=0):
        for  bound in self.game.boundary:
            if bound.x == self.x + dx and bound.y == self.y + dy:
                return True
        for mount in self.game.mountain:
            if mount.x == self.x + dx and mount.y == self.y + dy:
                return True
        for w in self.game.water:
            if w.x == self.x + dx and w.y == self.y + dy:
                return True       
        return False

    def update(self):
        self.rect.x = self.x * GRIDWIDTH
        self.rect.y = self.y * GRIDHEIGHT

class Rabbit(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.boundary
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.game =game
        self.image = pygame.image.load("images/rabbit.png").convert()
        self.image = pygame.transform.scale(self.image,(GRIDWIDTH,GRIDHEIGHT))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x*GRIDWIDTH
        self.rect.y = y*GRIDHEIGHT

    def move(self, dx=0, dy=0):
        if not self. collide_with_walls(dx,dy):
            self.x += dx
            self.y += dy

    def collide_with_walls(self, dx=0, dy=0):
        for  bound in self.game.boundary:
            if bound.x == self.x + dx and bound.y == self.y + dy:
                return True
        for mount in self.game.mountain:
            if mount.x == self.x + dx and mount.y == self.y + dy:
                return True
        for w in self.game.water:
            if w.x == self.x + dx and w.y == self.y + dy:
                return True       
        return False

    def update(self):
        self.rect.x = self.x * GRIDWIDTH
        self.rect.y = self.y * GRIDHEIGHT

class Deer(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.boundary
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.game =game
        self.image = pygame.image.load("images/deer.png").convert()
        self.image = pygame.transform.scale(self.image,(GRIDWIDTH,GRIDHEIGHT))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x*GRIDWIDTH
        self.rect.y = y*GRIDHEIGHT

    def move(self, dx=0, dy=0):
        if not self. collide_with_walls(dx,dy):
            self.x += dx
            self.y += dy

    def collide_with_walls(self, dx=0, dy=0):
        for  bound in self.game.boundary:
            if bound.x == self.x + dx and bound.y == self.y + dy:
                return True
        for mount in self.game.mountain:
            if mount.x == self.x + dx and mount.y == self.y + dy:
                return True
        for w in self.game.water:
            if w.x == self.x + dx and w.y == self.y + dy:
                return True       
        return False

    def update(self):
        self.rect.x = self.x * GRIDWIDTH
        self.rect.y = self.y * GRIDHEIGHT

class Mountain(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.mountain
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.game =game
        self.image = pygame.image.load("images/mountain.png").convert()
        self.image = pygame.transform.scale(self.image,(GRIDWIDTH,GRIDHEIGHT))
        self.rect = self.image.get_rect()
        self.x = x 
        self.y = y
        self.rect.x = x*GRIDWIDTH
        self.rect.y = y*GRIDHEIGHT

class Boundary(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.boundary
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.game =game
        self.image = pygame.image.load("images/wall.png").convert()
        self.image = pygame.transform.scale(self.image,(GRIDWIDTH,GRIDHEIGHT))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x*GRIDWIDTH
        self.rect.y = y*GRIDHEIGHT

class Water(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.water
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.game =game
        self.image = pygame.image.load("images/water.png").convert()
        self.image = pygame.transform.scale(self.image,(GRIDWIDTH,GRIDHEIGHT))
        self.rect = self.image.get_rect()
        self.x = x 
        self.y = y
        self.rect.x = x*GRIDWIDTH
        self.rect.y = y*GRIDHEIGHT

class Grass(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.grass
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.game =game
        self.image = pygame.image.load("images/grass.png").convert()
        self.image = pygame.transform.scale(self.image,(GRIDWIDTH,GRIDHEIGHT))
        self.rect = self.image.get_rect()
        self.x = x 
        self.y = y
        self.rect.x = x*GRIDWIDTH
        self.rect.y = y*GRIDHEIGHT

