import pygame
import numpy as np
import time

class Map():
    def __init__(self):
        self.MapSize_Arr = [50,50]
        self.Map_Arr = None
        self.MapGenerate()
        self.platform_height = None

    def MapGenerate(self):
        self.Map_Arr = np.zeros(self.MapSize_Arr,int)
        self.Map_Arr[:, self.MapSize_Arr[0] // 2:] = 1

class Renderer():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("BlockWorld2D")

        self.DisplaySize_Arr = [500,500]
        self.Scale = [1,1]
        self.Viewport = pygame.display.set_mode(self.DisplaySize_Arr)

    def RenderIn(self, Map):
        WorldArr = Map.Map_Arr
        WorldArrSize = Map.MapSize_Arr
        self.Scale = self.DisplaySize_Arr[0] / WorldArrSize[0], self.DisplaySize_Arr[1] / WorldArrSize[1] 

        for i in range(len(WorldArr[0])):
            for j in range(len(WorldArr[1])):
                if WorldArr[i][j] == 0:
                    pygame.draw.rect(self.Viewport,(0,0,255),[i*self.Scale[0],j*self.Scale[1],self.Scale[0],self.Scale[1]])

                elif WorldArr[i][j] == 1:
                    pygame.draw.rect(self.Viewport,(0,255,0),[i*self.Scale[0],j*self.Scale[1],self.Scale[0],self.Scale[1]],1)


    def RenderInPlayer(self, Player):
        PlayerPos = Player.PlayerLoc
        image = pygame.image.load('idle.png')
        image = image.convert()
        self.Viewport.blit(image,[PlayerPos[0]*self.Scale[0],(PlayerPos[1]-0.5)*self.Scale[1],self.Scale[0],self.Scale[1]])


class Player():
    def __init__(self):
        self.Spawn_Arr = [2,2]
        self.PlayerLoc = self.Spawn_Arr

        self.PlayerAccel = 1
        self.Falling = False
        self.JumpHeight = 2
    
    def PlayerFCollision(self,Map,PlayerPos):
        PlayerX = int(PlayerPos[0])
        PlayerY = int(PlayerPos[1])

        if Map[PlayerX][PlayerY] == 1:
            print("error Ground")
        else:
            self.PlayerLoc = PlayerPos
            print(PlayerPos)

    def Gravity(self,Map):
        PlayerX = int(self.PlayerLoc[0])
        PlayerY = int(self.PlayerLoc[1])
        if Map[PlayerX][PlayerY+1] == 0:
            print(Map[PlayerX][PlayerY+1])
            self.PlayerLoc[1] += 1*self.PlayerAccel
            self.Falling = True
        else:
            self.Falling = False
        


    def Controller(self,Map,Render):
        self.Gravity(Map)

        self.keys = pygame.key.get_pressed()

        if self.keys[pygame.K_w] or self.keys[pygame.K_SPACE]:
            if self.Falling == False:
                PlayerPos = [self.PlayerLoc[0],self.PlayerLoc[1] - self.JumpHeight]
                self.PlayerFCollision(Map,PlayerPos)
            else:
                print("falling")

        if self.keys[pygame.K_s]:
            PlayerPos = [self.PlayerLoc[0],self.PlayerLoc[1] + 1]
            self.PlayerFCollision(Map,PlayerPos)

        if self.keys[pygame.K_a]:
            PlayerPos = [self.PlayerLoc[0] - 1,self.PlayerLoc[1]]
            self.PlayerFCollision(Map,PlayerPos)

        if self.keys[pygame.K_d]:
            PlayerPos = [self.PlayerLoc[0] + 1,self.PlayerLoc[1]]
            self.PlayerFCollision(Map,PlayerPos)

        mouse_presses = pygame.mouse.get_pressed()

        if mouse_presses[0]:
            Pos = pygame.mouse.get_pos()
            adjustedPos = [round(Pos[0] // Render[0]), round(Pos[1] // Render[1])]
            Map[adjustedPos[0]][adjustedPos[1]] = 0
            print("clicked at: ", adjustedPos)

        if mouse_presses[2]:
            Pos = pygame.mouse.get_pos()
            adjustedPos = [round(Pos[0] // Render[0]), round(Pos[1] // Render[1])]
            Map[adjustedPos[0]][adjustedPos[1]] = 1
            print("clicked at: ", adjustedPos)

MapRef = Map()
RendRef = Renderer()
PlayerRef = Player()

clock = pygame.time.Clock()

startTimeControls = time.time()
while True:
    PlayerRef.Controller(MapRef.Map_Arr,RendRef.Scale)

    RendRef.Viewport.fill((0,0,0))
    RendRef.RenderIn(MapRef)
    RendRef.RenderInPlayer(PlayerRef)
    pygame.display.update()

    clock.tick(30)
    if pygame.event.get() == pygame.QUIT:
        pygame.quit()
        break
