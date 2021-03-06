#Student name: Ben Huang
#Student ID: 21020526

import pygame
from config import *
import random

class Lion(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        #need to add hunger, thirst, mating to all animals which dictates their movement - hunger move to prey animal - thirst move towards water - mate -move towards female/male counterpart 
        self.groups = game.all_sprites, game.lion_group
        self._layer = 2
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.name = random.choice(['A','B','C'])+ str(random.randint(0,5))
        self.gender = random.choice(['m','f'])
        self.game =game
        self.image = pygame.image.load("images/lion.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,(GRIDWIDTH,GRIDHEIGHT))
        self.rect = self.image.get_rect()
        self.font = pygame.font.SysFont("sans",20)
        self.text = self.font.render(str(self.name) + str(self.gender),True, RED)
        self.image.blit(self.text,[0,0])
        self.x = x
        self.y = y
        self.neighbors = []
        self.rect.x = x*GRIDWIDTH
        self.rect.y = y*GRIDHEIGHT
        self.hunger_limit = max_hunger_limit
        self.thirst_limit = max_thirst_limit
        self.closest_water = ()
        self.can_breed = False
        self.mated = False
        self.time = pygame.time.get_ticks()
        self.breedingCooldown = 0
        self.reproduction_level = 100
        self.life_time = 0
        self.death = lion_death_timer

    def move(self, dx=0, dy=0):
        if not self.collide_with_entity(dx,dy):
            self.x += dx
            self.y += dy

    def getlocation(self):
        return (self.x, self.y)
    
    def get_neighbors(self,neighbour_option):
        self.neighbors = []
        if neighbour_option == 0:
            self.neighbors.append((self.x+1,self.y))
            self.neighbors.append((self.x-1,self.y))
            self.neighbors.append((self.x,self.y+1))
            self.neighbors.append((self.x,self.y-1))

        elif neighbour_option == 1:
            self.neighbors.append((self.x+1,self.y))
            self.neighbors.append((self.x-1,self.y))
            self.neighbors.append((self.x,self.y+1))
            self.neighbors.append((self.x,self.y-1))
            self.neighbors.append((self.x+1,self.y+1))
            self.neighbors.append((self.x-1,self.y-1))
            self.neighbors.append((self.x+1,self.y-1))
            self.neighbors.append((self.x-1,self.y+1))
    
        return self.neighbors
            
    def collide_with_entity(self, dx=0, dy=0):
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
        

    def ate(self):
        self.hunger_limit = max_hunger_limit

    def drink(self):    
        self.thirst = False
        self.thirst_limit = max_thirst_limit

    def reproduce(self):
        self.mated = True
        self.reproduction_level = 100
        self.can_breed = False
        self.breedingCooldown = lion_breeding_cooldown

class Wolf(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.wolf_group
        self._layer = 2
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.game =game
        self.neighbors = []
        self.name =  random.choice(['A','B','C'])+ str(random.randint(0,5))
        self.gender = random.choice(['m','f'])
        self.image = pygame.image.load("images/wolf.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,(GRIDWIDTH,GRIDHEIGHT))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x*GRIDWIDTH
        self.rect.y = y*GRIDHEIGHT
        self.font = pygame.font.SysFont("sans",20)
        self.text = self.font.render(str(self.name) + str(self.gender),True, RED)
        self.image.blit(self.text,[0,0])
        self.hunger_limit = max_hunger_limit
        self.hungry = True 
        self.thirst_limit = max_thirst_limit
        self.closest_water = ()
        self.can_breed = False
        self.mated = False
        self.time = pygame.time.get_ticks()
        self.breedingCooldown = 0
        self.reproduction_level = 100
        self.life_time = 0 
        self.wolf = wolf_death_timer


    def getlocation(self):
        return (self.x, self.y)
    
    def get_neighbors(self,neighbour_option):
        self.neighbors = []
        if neighbour_option == 0:
            self.neighbors.append((self.x+1,self.y))
            self.neighbors.append((self.x-1,self.y))
            self.neighbors.append((self.x,self.y+1))
            self.neighbors.append((self.x,self.y-1))

        elif neighbour_option == 1:
            self.neighbors.append((self.x+1,self.y))
            self.neighbors.append((self.x-1,self.y))
            self.neighbors.append((self.x,self.y+1))
            self.neighbors.append((self.x,self.y-1))
            self.neighbors.append((self.x+1,self.y+1))
            self.neighbors.append((self.x-1,self.y-1))
            self.neighbors.append((self.x+1,self.y-1))
            self.neighbors.append((self.x-1,self.y+1))

        return self.neighbors

    def move(self, dx=0, dy=0):
        if not self. collide_with_entity(dx,dy):
            self.x += dx
            self.y += dy

    def collide_with_entity(self, dx=0, dy=0):
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

    def ate(self):
        self.hunger_limit = max_hunger_limit

    def drink(self):    
        self.thirst = False
        self.thirst_limit = max_thirst_limit

    def reproduce(self):
        self.mated = True
        self.reproduction_level = 100
        self.can_breed = False
        self.breedingCooldown = wolf_breeding_cooldown

class Rabbit(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.rabbit_group
        self._layer = 2
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.name =  random.choice(['A','B','C'])+ str(random.randint(0,5))
        self.gender = random.choice(['m','f'])
        self.game =game
        self.image = pygame.image.load("images/rabbit.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,(GRIDWIDTH,GRIDHEIGHT))
        self.rect = self.image.get_rect()
        self.neighbors = []
        self.x = x
        self.y = y
        self.rect.x = x*GRIDWIDTH
        self.rect.y = y*GRIDHEIGHT
        self.x = x
        self.y = y
        self.neighbors = []
        self.font = pygame.font.SysFont("sans",20)
        self.text = self.font.render(str(self.name) + str(self.gender),True, RED)
        self.image.blit(self.text,[0,0])
        self.hunger_limit = max_hunger_limit
        self.thirst_limit = max_thirst_limit
        self.closest_water = ()
        self.can_breed = False
        self.mated = False
        self.time = pygame.time.get_ticks()
        self.breedingCooldown = 0
        self.reproduction_level = 100
        self.life_time = 0 
        self.death_timer = rabbit_death_timer

    def move(self, dx=0, dy=0):
        if not self. collide_with_entity(dx,dy):
            self.x += dx
            self.y += dy

    def get_neighbors(self,neighbour_option):
        self.neighbors = []
        if neighbour_option == 0:
            self.neighbors.append((self.x+1,self.y))
            self.neighbors.append((self.x-1,self.y))
            self.neighbors.append((self.x,self.y+1))
            self.neighbors.append((self.x,self.y-1))

        elif neighbour_option == 1:
            self.neighbors.append((self.x+1,self.y))
            self.neighbors.append((self.x-1,self.y))
            self.neighbors.append((self.x,self.y+1))
            self.neighbors.append((self.x,self.y-1))
            self.neighbors.append((self.x+1,self.y+1))
            self.neighbors.append((self.x-1,self.y-1))
            self.neighbors.append((self.x+1,self.y-1))
            self.neighbors.append((self.x-1,self.y+1))

        return self.neighbors

    def getlocation(self):
        return (self.x, self.y)

    def collide_with_entity(self, dx=0, dy=0):
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
    
    def ate(self):
        self.hunger_limit = max_hunger_limit

    def drink(self):    
        self.thirst = False
        self.thirst_limit = max_thirst_limit

    def reproduce(self):
        self.mated = True
        self.reproduction_level = 100
        self.can_breed = False
        self.breedingCooldown = rabbit_breeding_cooldown

class Mountain(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.mountain
        self._layer = 2
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.game =game
        self.image = pygame.image.load("images/mountain.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,(GRIDWIDTH,GRIDHEIGHT))
        self.rect = self.image.get_rect()
        self.x = x 
        self.y = y
        self.rect.x = x*GRIDWIDTH
        self.rect.y = y*GRIDHEIGHT
    def getlocation(self):
            return (self.x, self.y)

class Boundary(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.boundary
        pygame.sprite.Sprite.__init__(self,self.groups)
        self._layer = 2
        self.game =game
        self.image = pygame.image.load("images/wall.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,(GRIDWIDTH,GRIDHEIGHT))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x*GRIDWIDTH
        self.rect.y = y*GRIDHEIGHT
    def getlocation(self):
        return (self.x, self.y)

class Water(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.water
        pygame.sprite.Sprite.__init__(self,self.groups)
        self._layer = 2
        self.game =game
        self.image = pygame.image.load("images/water.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,(GRIDWIDTH,GRIDHEIGHT))
        self.rect = self.image.get_rect()
        self.x = x 
        self.y = y
        self.rect.x = x*GRIDWIDTH
        self.rect.y = y*GRIDHEIGHT
    def getlocation(self):
            return (self.x, self.y)

class Grass(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.grass_group
        self._layer = 1
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.game =game
        self.image = pygame.image.load("images/grass.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,(GRIDWIDTH,GRIDHEIGHT))
        self.rect = self.image.get_rect()
        self.cooldown = grass_grow_time
        self.x = x 
        self.y = y
        self.rect.x = x*GRIDWIDTH
        self.rect.y = y*GRIDHEIGHT
        self.time = pygame.time.get_ticks()

    def getlocation(self):
            return (self.x, self.y)
    


class Soil(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.soil_group
        self._layer = 1
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.game =game
        self.image = pygame.image.load("images/soil.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,(GRIDWIDTH,GRIDHEIGHT))
        self.rect = self.image.get_rect()
        self.x = x 
        self.y = y
        self.rect.x = x*GRIDWIDTH
        self.rect.y = y*GRIDHEIGHT
        
    def getlocation(self):
            return (self.x, self.y)

