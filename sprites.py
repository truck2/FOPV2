import pygame
from config import *
import random

class Lion(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        #need to add hunger, thirst, mating to all animals which dictates their movement - hunger move to prey animal - thirst move towards water - mate -move towards female/male counterpart 
        self.groups = game.all_sprites, game.lion_group
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.name =  random.choice(['A','B','C'])+ str(random.randint(0,5))
        self.gender = random.choice(['m','f'])
        self.game =game
        self.image = pygame.image.load("images/lion.png").convert()
        self.image = pygame.transform.scale(self.image,(GRIDWIDTH,GRIDHEIGHT))
        self.rect = self.image.get_rect()
        self.font = pygame.font.SysFont("sans",30)
        self.text = self.font.render(str(self.name) + str(self.gender),True, BLACK)
        self.image.blit(self.text,[0,0])
        self.x = x
        self.y = y
        self.neighbors = []
        self.rect.x = x*GRIDWIDTH
        self.rect.y = y*GRIDHEIGHT
        self.hunger_limit = max_hunger_limit
        self.hungry = True 
        self.can_hunt = False
        self.thirst_limit = max_thirst_limit
        self.closest_water = ()
        self.thirsty = True
        self.can_breed = False
        self.mated = True
        self.breeding = False
        self.breedingCooldown = 500
        self.reproduction_level = 100

    def move(self, dx=0, dy=0):
        if not self.collide_with_entity(dx,dy):
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
        for l in self.game.lion_group:
            if l.x == self.x + dx and l.y == self.y + dy:
                return True
        for wo in self.game.wolf_group:
            if wo.x == self.x + dx and wo.y == self.y + dy:
                return True
        for d in self.game.deer_group:
            if d.x == self.x + dx and d.y == self.y + dy:
                return True
        for r in self.game.rabbit_group:
            if r.x == self.x + dx and r.y == self.y + dy:
                return True
        return False

    def update(self):
        self.rect.x = self.x * GRIDWIDTH
        self.rect.y = self.y * GRIDHEIGHT

    def ate(self):
        self.hungry = False
        self.hunger_limit = max_hunger_limit

    def drink(self):    
        self.thirst = False
        self.thirst_limit = max_thirst_limit

    def reproduce(self):
        self.mated = True
        self.reproduction_level == 100
        self.can_breed = False
        self.breedingCooldown = 5000

class Wolf(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.wolf_group
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.game =game
        self.neighbors = []
        self.name =  random.choice(['A','B','C'])+ str(random.randint(0,5))
        self.gender = random.choice(['m','f'])
        self.image = pygame.image.load("images/wolf.png").convert()
        self.image = pygame.transform.scale(self.image,(GRIDWIDTH,GRIDHEIGHT))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x*GRIDWIDTH
        self.rect.y = y*GRIDHEIGHT
        self.stamina =50
        self.font = pygame.font.SysFont("sans",30)
        self.text = self.font.render(str(self.name) + str(self.gender),True, BLACK)
        self.image.blit(self.text,[0,0])
        self.hunger_limit = max_hunger_limit
        self.hungry = True 
        self.can_hunt = False
        self.thirst_limit = max_thirst_limit
        self.closest_water = ()
        self.thirsty = True
        self.can_breed = False
        self.mated = True
        self.breeding = False
        self.breedingCooldown = 500
        self.reproduction_level = 100

    def getlocation(self):
        return (self.x, self.y)
    
    def get_neighbors(self):
        self.neighbors = []
        self.neighbors.append((self.x+1,self.y))
        self.neighbors.append((self.x-1,self.y))
        self.neighbors.append((self.x,self.y+1))
        self.neighbors.append((self.x,self.y-1))

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
        for l in self.game.lion_group:
            if l.x == self.x + dx and l.y == self.y + dy:
                return True
        for wo in self.game.wolf_group:
            if wo.x == self.x + dx and wo.y == self.y + dy:
                return True
        for d in self.game.deer_group:
            if d.x == self.x + dx and d.y == self.y + dy:
                return True
        for r in self.game.rabbit_group:
            if r.x == self.x + dx and r.y == self.y + dy:
                return True
        return False

    def update(self):
        self.rect.x = self.x * GRIDWIDTH
        self.rect.y = self.y * GRIDHEIGHT

    def ate(self):
        self.hungry = False
        self.hunger_limit = max_hunger_limit

    def drink(self):    
        self.thirst = False
        self.thirst_limit = max_thirst_limit

    def reproduce(self):
        self.mated = True
        self.reproduction_level == 100
        self.can_breed = False
        self.breedingCooldown = 5000

class Rabbit(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.rabbit_group
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.name =  "Rabbit "+ str(random.randint(0,5)) + str(str(random.randint(5,10)))
        self.game =game
        self.image = pygame.image.load("images/rabbit.png").convert()
        self.image = pygame.transform.scale(self.image,(GRIDWIDTH,GRIDHEIGHT))
        self.rect = self.image.get_rect()
        self.neighbors = []
        self.x = x
        self.y = y
        self.rect.x = x*GRIDWIDTH
        self.rect.y = y*GRIDHEIGHT

    def move(self, dx=0, dy=0):
        if not self. collide_with_entity(dx,dy):
            self.x += dx
            self.y += dy

    def get_neighbors(self):
        self.neighbors = []
        self.neighbors.append((self.x+1,self.y))
        self.neighbors.append((self.x-1,self.y))
        self.neighbors.append((self.x,self.y+1))
        self.neighbors.append((self.x,self.y-1))

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
        for l in self.game.lion_group:
            if l.x == self.x + dx and l.y == self.y + dy:
                return True
        for wo in self.game.wolf_group:
            if wo.x == self.x + dx and wo.y == self.y + dy:
                return True
        for d in self.game.deer_group:
            if d.x == self.x + dx and d.y == self.y + dy:
                return True
        for r in self.game.rabbit_group:
            if r.x == self.x + dx and r.y == self.y + dy:
                return True
        return False

    def update(self):
        self.rect.x = self.x * GRIDWIDTH
        self.rect.y = self.y * GRIDHEIGHT

class Deer(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.deer_group
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.game =game
        self.image = pygame.image.load("images/deer.png").convert()
        self.image = pygame.transform.scale(self.image,(GRIDWIDTH,GRIDHEIGHT))
        self.rect = self.image.get_rect()
        self.neighbors = []
        self.x = x
        self.y = y
        self.rect.x = x*GRIDWIDTH
        self.rect.y = y*GRIDHEIGHT
    
    def get_neighbors(self):
        self.neighbors = []
        self.neighbors.append((self.x+1,self.y))
        self.neighbors.append((self.x-1,self.y))
        self.neighbors.append((self.x,self.y+1))
        self.neighbors.append((self.x,self.y-1))

        return self.neighbors

    def getlocation(self):
        return (self.x, self.y)

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
        for l in self.game.lion_group:
            if l.x == self.x + dx and l.y == self.y + dy:
                return True
        for wo in self.game.wolf_group:
            if wo.x == self.x + dx and wo.y == self.y + dy:
                return True
        for d in self.game.deer_group:
            if d.x == self.x + dx and d.y == self.y + dy:
                return True
        for r in self.game.rabbit_group:
            if r.x == self.x + dx and r.y == self.y + dy:
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
    def getlocation(self):
            return (self.x, self.y)

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
    def getlocation(self):
            return (self.x, self.y)

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

    def getlocation(self):
            return (self.x, self.y)

