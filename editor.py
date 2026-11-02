#############
# LIBRARIES #
#############
import pygame
from scripts.entity import Enemy,Spikemole,Guard,Soldier,Archer,Player,Knight,FinalBoss
from scripts.tile import Tile, MovingPlatform, Vertical, Horizontal, BouncePad, ClimbingWall, Decor
from scripts.utils import loadLevel, loadImg, loadImages
from scripts.label import Serf
# Temporary Init Whilst This Is A Separate Program
pygame.init()


#""""""""""""""#
# EDITOR CLASS #
#\/\/\/\/\/\/\/#
class Editor:
    def __init__(self,display,game):
        self.name = "editor"
        self.display = display
        self.scrollThreshold = self.scrollThreshold = {"x":self.display.get_width()*(5/6), "y":self.display.get_height()*(5/6)}
        self.assets = { # All Of The Frames For The Game
            # Player #
            "player":{"idle":{"frames":loadImages("bobbin_dud/idle"),"frameCounter":7},},
            # Enemies #
            "guard":{"idle":{"frames":loadImages("guard/idle"),"frameCounter":6},},
            "soldier":{"idle": {"frames":loadImages("soldier/idle"),"frameCounter":6},},
            "archer":{"idle": {"frames":loadImages("archer/idle"),"frameCounter":8},},
            "knight":{"idle":{"frames":loadImages("knight/idle"),"frameCounter":8},},
            "spikemole":{"down":{"frames":loadImages("spikemole/down"),"frameCounter":5},},
            "final_boss":{"idle":{"frames":loadImages("final_boss/idle"),"frameCounter":7},},
            # Serfs #
            "serf":loadImages("serf"),
            # Weaponary #
            "sword":loadImg("sword"),
            "spear":loadImg("spear"),
            "bow":loadImg("bow"),
            "enemy_bow":loadImg("enemy_bow"),
            "boss_sword_1":loadImg("boss_sword"),
            "boss_sword_2":loadImg("boss_sword_2"),
            "arrow":loadImg("arrow"),
            # Tiles #
            "0":loadImages("tiles/tile/grass"),
            "1":loadImages("tiles/tile/dirt"),
            "2":loadImages("tiles/tile/stone"),
            "3":loadImages("decor"), # Decor Will Be Here
            "4":loadImages("tiles/moving_platform") + loadImages("tiles/climbing_wall") + loadImages("tiles/bounce_pad"),
            "5":[loadImg("guard/idle/1"), loadImg("soldier/idle/1"), loadImg("archer/idle/1"), loadImg("knight/idle/1"), loadImg("spikemole/down/1"), loadImg("final_boss/idle/1")],
            "6":[loadImg("bobbin_dud/idle/1")],
            "7":loadImages("serf"),
        } # So That Everything Loads Correctly
        self.running = True
        self.game = game

        # Mouse
        self.tile = 0                      
        self.type = 0
        self.tilepos = (0,0)
        # Functions
        self.tab = False
        self.ctrl = False
        self.shift = False
        self.movingplatform = False
        self.movingPlatformX = 0
        self.movingPlatformY = 0
        self.scroll = [0,0]
        self.scrollValue = 16
        self.applyScroll = [0,0] # Scroll To Change So That The Player Is In Frame At The Start
        self.offgrid = False
        self.saveCounter = 0
        # Tilemap
        self.tilesize = 16
        # Font And Text
        self.font = pygame.font.SysFont("Arial",10) # definitely experimental as font size
        self.controlText = "" # This shows the controls
        self.editorText = self.font.render("Editor",False,"white")

    # Main Loop #
    def run(self):
        # When integrated, this will become and if statement
        # General Screen Stuff
        self.display.fill((25,25,25))
        # Create A List Of All Rects For Ease Of Searching
        self.allTiles = [tile.rect for tile in self.tilemap]+[tile.rect for tile in self.movingplatforms]+[tile.rect for tile in self.bouncepads]+[tile.rect for tile in self.climbingwalls] + [enemy.rect for enemy in self.enemies]
        if self.playerStart != None:
            self.playerStart = (self.playerStart[0]+self.scroll[0], self.playerStart[1]+self.scroll[1])
            self.allTiles.append(pygame.Rect(self.playerStart[0],self.playerStart[1],10,10))
            self.player = Player(self,self.playerStart[0], self.playerStart[1],gameType="editor")
        # Rendering Entities
        for decoration in self.decor:
            decoration.render(self,self.scroll)
        if self.playerStart != None:
            self.display.blit(self.player.img, (self.player.rect.x, self.player.rect.y))
        for enemy in self.enemies:
            enemy.render(self.scroll)
        # Rendering Tilemap
        for tile in self.tilemap:
            tile.render(self,self.scroll)
        for movingplatform in self.movingplatforms:
            movingplatform.render(self,self.scroll)
            movingplatform.update(self.scroll,"editor") # Important To Make Sure That It Saves Properly
        for bouncepad in self.bouncepads:
            bouncepad.render(self,self.scroll)
        for climbingwall in self.climbingwalls:
            climbingwall.render(self,self.scroll)
        for serf in self.serfs:
            serf.render(self.scroll)
        self.scroll = [0,0]
        
        # Mouse Position And Current Tile
        self.mpos = pygame.mouse.get_pos()
        self.mRect = pygame.Rect(self.mpos[0]/3-1,self.mpos[1]/3+1,2,2)
        # Display The Correct Image On The Mouse
        match self.type:
            case 0|1|2:
                self.mTile = Tile(self.type,0,0,self,self.tile)
            case 3:
                self.mTile = Decor(0,0,self,self.tile)
            case 4:
                match self.tile:
                    case 0|1:
                        self.mTile = MovingPlatform(2,0,0,self,self.tile)
                    case 2|3|4|5:
                        self.mTile = ClimbingWall(0,0,self,self.tile)
                    case 6:
                        self.mTile = BouncePad(0,0,self)
            case 5:
                match self.tile:
                    case 0:
                        self.mTile = Spikemole(self,0,0)
                    case 1:
                        self.mTile = Guard(self,0,0)
                    case 2:
                        self.mTile = Soldier(self,0,0)
                    case 3:
                        self.mTile = Archer(self,0,0)
                    case 4:
                        self.mTile = Knight(self,0,0)
                    case 5:
                        self.mTile = FinalBoss(self,0,0)
                    case _:
                        self.mTile = ""
            case 6:
                self.mTile = Player(self,0,0,gameType="editor")
            case 7:
                self.mTile = Serf(self,0,0,self.tile)
            case _:
                self.mTile = ""

        try:
            if self.offgrid: # If Offgrid, Centre the Mouse on The Tile
                self.tilepos = (self.mpos[0]/3-self.mTile.img.get_width()/2,self.mpos[1]/3-self.mTile.img.get_height()/2)
            else: # If Ongrid, The Tiles Should Snap To An Invisible Grid
                if self.type == 5 and self.tile == 0: # Spikemole
                    self.tilepos = (int((self.mpos[0]/3)/self.tilesize) * self.tilesize+5,int((self.mpos[1]/3)/self.tilesize)*self.tilesize+11) # Put it in the bottom middle of the tile
                elif self.type == 5 and self.tile == 4: # Knight
                    self.tilepos = (int((self.mpos[0]/3)/self.tilesize) * self.tilesize,int((self.mpos[1]/3)/self.tilesize)*self.tilesize+6)
                else:
                    self.tilepos = (int((self.mpos[0]/3)/self.tilesize) * self.tilesize,int((self.mpos[1]/3)/self.tilesize)*self.tilesize)
            #self.mTile.img.set_alpha(80)
            self.display.blit(self.mTile.img,self.tilepos)
        except AttributeError:
            pass

        # ON SCREEN TEXT #
        #- Editor/ Saving
        if self.saveCounter > 0: # Show This During The Saving Process
            self.editorText = self.font.render("saving level",False,"red")
            self.saveCounter -= 1
        else: # Show This Otherwise
            self.editorText = self.font.render("Editor",False,"white")
        self.display.blit(self.editorText, (4,4))

        #- Moving Platform Instructions
        if self.movingplatform:
            self.controlText = ["PLACING MOVING PLATFORMS:","- Left Click Vertically Below Your First","  Platform To Create A Vertically","  Moving Platform",
                                "- Left Click Horizontally Across","  From Your First Platform To Create","  A Horizontally Moving Platform","- Right Click To Exit"]
        #- General Instructions
        elif self.tab:
            self.controlText = ["CONTROLS:","- Left Click To Place Tiles","- Right Click To Delete Tiles","- Use 'G' To Toggle Off-Grid","- Use Arrow Keys To Scroll",
                                "- Use The Scroll Wheel To Change","  Tile","- Use SHIFT And The Scroll Wheel","  To Change Tile Type","- Press CTRL and 'S' To Save","- Press TAB To Close This Menu"]
        #- "Press Tab To See Controls"
        else:
            self.controlText = ["Press TAB To See Controls"]
        #- Actually Render It
        for line in self.controlText:
            self.display.blit(self.font.render(line,False,"white"), (-4+self.display.get_width()*(5/7),4+self.controlText.index(line)*11))

        # EVENTS #
        for event in pygame.event.get():
            # QUIT
            if event.type == pygame.QUIT:
                self.game.running = False
            # MOUSE
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left Click
                    flag = True
                    for button in self.game.buttons[self.game.state]:
                        if button.rect.collidepoint(self.game.mpos):
                            flag = False
                            button.onClick(self.game)
                    if flag: # You Cannot Click The Button And Place A Tile At The Same Time
                        if self.movingplatform: # Placing The End Location For A Moving Platform
                            x = self.tilepos[0]
                            y = self.tilepos[1]
                            if x == self.movingPlatformX and y > self.movingPlatformY + self.tilesize: # Placing A Vertically Moving Platform
                                self.movingplatforms = self.movingplatforms[:-1] # Remove The Placeholders
                                self.movingplatforms.append(Vertical(2,self.movingPlatformX,self.movingPlatformY,y,self,self.tile))
                                self.movingplatform = False
                            elif y == self.movingPlatformY and x > self.movingPlatformX + self.tilesize: # Placing A Horizontally Moving Platform
                                self.movingplatforms = self.movingplatforms[:-1]
                                self.movingplatforms.append(Horizontal(2,self.movingPlatformX,x,self.movingPlatformY,self,self.tile))
                                self.movingplatform = False
                            else:
                                self.movingplatform = True
                        else:
                            if not self.offgrid: # i.e. Ongrid
                                x = self.tilepos[0]
                                y = self.tilepos[1]
                                if self.type in (0,1,2): # Normal Tiles
                                    flag = True
                                    for tile in self.allTiles:
                                        if tile.x == x and tile.y == y: # Is There Anything In That Spot
                                            flag = False
                                    if flag:
                                        self.tilemap.append(Tile(self.type,x,y,self,self.tile))
                                if self.type == 3: # Decor
                                    self.decor.append(Decor(x,y,self,self.tile))
                                if self.type == 4: # Special Tiles
                                    if self.tile in (0,1): # Moving Platforms
                                        flag = True
                                        for tile in self.allTiles:
                                            if tile.x in (x, self.tilesize+x) and tile.y == y: # Moving Platforms Are Twice As Long
                                                flag = False
                                        if flag: # If The Placement Is Valid, Create A Moving Platform Template
                                            self.movingplatform = True
                                            self.movingPlatformX = x
                                            self.movingPlatformY = y
                                            self.movingplatforms += [MovingPlatform(4,x,y,self,self.tile)] # Placeholders
                                    elif self.tile in (2,3,4,5): # Climbing Walls
                                        flag = True
                                        for i in range(8):
                                            for tile in self.allTiles:
                                                if tile.x==x and tile.y==y+(i*self.tilesize):
                                                    flag = False
                                        if flag:
                                            self.climbingwalls.append(ClimbingWall(x,y,self,self.tile))
                                    else: # Bounce Pads
                                        flag = True
                                        for tile in self.allTiles:
                                            if tile.x in (x, x+self.tilesize) and tile.y==y:
                                                flag = False
                                        if flag:
                                            self.bouncepads.append(BouncePad(x+4,y,self))
                                if self.type == 5: # Enemies
                                    flag = True
                                    for tile in self.allTiles:
                                        if tile.x == x and tile.y == y:
                                            flag = False
                                    if flag:
                                        if self.tile == 0:
                                            self.enemies.append(Spikemole(self,x,y))
                                        elif self.tile == 1:
                                            self.enemies.append(Guard(self,x,y))
                                        elif self.tile == 2:
                                            self.enemies.append(Soldier(self,x,y))
                                        elif self.tile == 3:
                                            self.enemies.append(Archer(self,x,y))
                                        elif self.tile == 4:
                                            flag = True
                                            for tile in self.allTiles:
                                                if tile.collidepoint((x,y)) or tile.collidepoint((x+self.tilesize,y)) or tile.collidepoint((x+self.tilesize,y+self.tilesize)) or tile.collidepoint((x,y+self.tilesize)):
                                                    flag = False
                                            if flag:
                                                self.enemies.append(Knight(self,x,y))
                                        elif self.tile == 5:
                                            self.enemies.append(FinalBoss(self,x,y))
                                if self.type == 6: # The Player's Starting Location
                                    if self.playerStart == None: # To Prevent Placing It Twice
                                        flag = True
                                        for tile in self.allTiles:
                                            if tile.x == x and tile.y == y:
                                                flag = False
                                        if flag:
                                            self.playerStart = (x,y)
                                if self.type == 7: # Serfs
                                    flag = True
                                    for tile in self.allTiles:
                                        if tile.x == x and tile.y == y:
                                            flag = False
                                    if flag:
                                        self.serfs.append(Serf(self,x,y,self.tile))

                            else: # Offgrid So Much Simpler- Less Checking Required
                                x = self.tilepos[0]
                                y = self.tilepos[1]
                                match self.type:
                                    case 0|1|2: # Normal Tiles
                                        self.tilemap.append(Tile(self.type,x,y,self,self.tile))
                                    case 3: # Decor
                                        self.decor.append(Decor(x,y,self,self.tile))
                                    case 4: # Special Tiles
                                        match self.tile:
                                            case 0|1: # Moving Platforms
                                                self.movingplatform = True
                                                self.movingPlatformX = x
                                                self.movingPlatformY = y
                                                self.movingplatforms += [MovingPlatform(4,x,y,self,self.tile)] # Placeholders
                                            case 2|3|4|5: # Climbing Walls
                                                self.climbingwalls.append(ClimbingWall(x,y,self,self.tile))
                                            case 6: # Bounce Pads
                                                self.bouncepads.append(BouncePad(x,y,self))
                                            case _:
                                                print("error")
                                    case 5: # Enemies
                                        match self.tile:
                                            case 0:
                                                self.enemies.append(Spikemole(self,x,y))
                                            case 1:
                                                self.enemies.append(Guard(self,x,y))
                                            case 2:
                                                self.enemies.append(Soldier(self,x,y))
                                            case 3:
                                                self.enemies.append(Archer(self,x,y))
                                            case 4:
                                                self.enemies.append(Knight(self,x,y))
                                            case 5:
                                                self.enemies.append(FinalBoss(self,x,y))
                                    case 6: # The Player's Starting Position
                                        if self.playerStart != None:
                                            self.playerStart = (self.mpos[0]/3,self.mpos[1]/3)
                                    case 7: # Serfs
                                        self.serfs.append(Serf(self,x,y,self.tile))
                                    case _:
                                        print("error")
                if event.button == 3: # Right Click
                    # Delete Tiles
                    if not self.movingplatform:
                        for tile in self.allTiles.copy()+[tile.rect for tile in self.decor.copy()]+[serf.rect for serf in self.serfs]: # Avoid Errors With The List Changing Length
                            if self.mRect.colliderect(tile): # Find A Rect That Has Been Collided With
                                # Break The List Of All Tiles Down, And Check The Index To See Which Tile To Delete
                                self.allTiles += [tile.rect for tile in self.decor] + [serf.rect for serf in self.serfs]
                                indx =  self.allTiles.index(tile)
                                self.allTiles.remove(tile)
                                if indx < len(self.tilemap):
                                    self.tilemap.remove(tile)
                                elif indx < len(self.tilemap) + len(self.movingplatforms):
                                    self.movingplatforms.remove(tile)
                                elif indx < len(self.tilemap) + len(self.movingplatforms) + len(self.bouncepads):
                                    self.bouncepads.remove(tile)
                                elif indx < len(self.tilemap) + len(self.movingplatforms) + len(self.bouncepads) + len(self.climbingwalls):
                                    self.climbingwalls.remove(tile)
                                elif indx < len(self.tilemap) + len(self.movingplatforms) + len(self.bouncepads) + len(self.climbingwalls) + len(self.enemies): # Include Player Start
                                    self.enemies.remove(tile)
                                elif (indx < len(self.tilemap) + len(self.movingplatforms) + len(self.bouncepads) + len(self.climbingwalls) + len(self.enemies) + 1) and self.playerStart != None:
                                    self.playerStart = None
                                elif ((indx < len(self.tilemap) + len(self.movingplatforms) + len(self.bouncepads) + len(self.climbingwalls) + len(self.enemies) + len(self.decor) + 1) and self.playerStart != None) or ((indx < len(self.tilemap) + len(self.movingplatforms) + len(self.bouncepads) + len(self.climbingwalls) + len(self.enemies) + len(self.decor)) and self.playerStart == None): 
                                    self.decor.remove(tile)
                                else:
                                    self.serfs.remove(tile)
                    else:
                        self.movingplatform = False # Cancel Creating A Moving Platform
                        self.movingPlatformX = 0
                        self.movingPlatformY = 0
                        self.movingplatforms = self.movingplatforms[:-2]
                if event.button == 4: # Scroll Up
                    if not self.movingplatform:
                        if self.shift: # When Shifting, Change The Type Of Tile
                            self.tile = 0
                            self.type = (self.type+1) % 8 # Avoid Errors Of Reaching The End Of The List By Making It Circular
                        else: # When Not Shifting, Move Within The Type List
                            self.tile = (self.tile+1) % len(self.assets[str(self.type)])
                if event.button == 5: # Scroll Down
                    if not self.movingplatform:
                        if self.shift: # Same Here
                            self.tile = 0
                            self.type = (self.type-1) % 8
                        else:
                            self.tile = (self.tile-1) % len(self.assets[str(self.type)])

            # Keys Pressed
            if event.type == pygame.KEYDOWN:
                if not self.movingplatform:
                    # Toggles
                    if event.key == pygame.K_TAB:
                        self.tab = not self.tab
                    if event.key == pygame.K_g:
                        self.offgrid = not self.offgrid
                    # Saving
                    if event.key in (pygame.K_LCTRL, pygame.K_RCTRL):
                        self.ctrl = True
                    if event.key == pygame.K_s and self.ctrl:
                        self.saveLevel("temp")
                    # Shifting
                    if event.key == pygame.K_LSHIFT:
                        self.shift = True
                #Scroll Control
                if event.key == pygame.K_UP:
                    self.scroll[1] = self.scrollValue
                if event.key == pygame.K_DOWN:
                    self.scroll[1] = -1*self.scrollValue
                if event.key == pygame.K_LEFT:
                    self.scroll[0] = self.scrollValue
                if event.key == pygame.K_RIGHT:
                    self.scroll[0] = -1*self.scrollValue
                self.movingPlatformX += self.scroll[0]
                self.movingPlatformY += self.scroll[1]
            # Keys Released - Suggesting The Action Is No Longer Being Performed
            if not self.movingplatform:
                if event.type == pygame.KEYUP:
                    if event.key in (pygame.K_RCTRL,pygame.K_LCTRL):
                        self.ctrl = False
                    if event.key == pygame.K_LSHIFT:
                        self.shift = False

    def saveLevel(self,filename):
        # Is There A Start Position For The Player?
        if self.playerStart != None:
            # Making Sure That The Start Position Is Valid For The Player, By Applying A Scroll To Everything To Move The Player Back Into ~Centre Of The Window
            #- X
            if self.display.get_width()-self.scrollThreshold["x"] > self.playerStart[0]: # Is The Player Left Of The Window?
                self.applyScroll[0] += int((self.display.get_width()-self.scrollThreshold["x"]-self.playerStart[0] + self.display.get_width()/2)/self.tilesize +1) * self.tilesize
            elif self.playerStart[0] > self.scrollThreshold["x"]: # Is The Player Right Of The Window?
                self.applyScroll[0] -= int((self.playerStart[0]-self.scrollThreshold["x"] + self.display.get_width()/2)/self.tilesize +1) * self.tilesize
            else:
                self.applyScroll[0] = 0 # It is in frame- no changes need applying
            #- Y
            if self.display.get_height()-self.scrollThreshold["y"] > self.playerStart[1]: # Is The Player Above The Window?
                self.applyScroll[1] += int((self.display.get_height()-self.scrollThreshold["y"]-self.playerStart[1] + self.display.get_height()/2)/self.tilesize +1) * self.tilesize
            elif self.playerStart[1] > self.scrollThreshold["y"]: # Is The Player Below The Window?
                self.applyScroll[1] -= int((self.playerStart[1]-self.scrollThreshold["y"]+self.display.get_height()/2)/self.tilesize +1) * self.tilesize
            else:
                self.applyScroll[1] = 0 # It is in frame- no changes need applying

        self.saveCounter = 300 # Used To Tell The Player That Their Level Is Saving
        file = open("scripts/levels/"+filename+".txt", "w")
        file.write("tilemap: ")
        for tile in self.tilemap: # Save Tilemap
            file.write(str([tile.type,tile.tile,tile.rect.x+self.applyScroll[0],tile.rect.y+self.applyScroll[1]])+";")
        file.write("\nbouncepads: ")
        for bouncepad in self.bouncepads: # Save Bouncepads
            file.write(str([bouncepad.rect.x+self.applyScroll[0],bouncepad.rect.y+self.applyScroll[1]])+";")
        file.write("\nmovingplatforms: ") # Save Moving Platforms
        horizontal = "\nhorizontal: "
        vertical = "\nvertical: "
        for movingplatform in self.movingplatforms:
            if movingplatform.moveType == "h": # Horizontal
                horizontal += str([movingplatform.speed,movingplatform.startX+self.applyScroll[0],movingplatform.endX+self.applyScroll[0],movingplatform.rect.y+self.applyScroll[1],movingplatform.tile])+";"
            elif movingplatform.moveType == "v": # Vertical
                vertical += str([movingplatform.speed,movingplatform.rect.x+self.applyScroll[0],movingplatform.startY+self.applyScroll[1],movingplatform.endY+self.applyScroll[1],movingplatform.tile])+";"
        file.write(horizontal+vertical)
        file.write("\nclimbingwalls: ") # Save Climbing Walls
        for climbingwall in self.climbingwalls:
            file.write(str([climbingwall.rect.x+self.applyScroll[0],climbingwall.rect.y+self.applyScroll[1],climbingwall.tile])+";")
        file.write("\ndecor: ") # Decoration
        for decoration in self.decor:
            file.write(str([decoration.rect.x+self.applyScroll[0],decoration.rect.y+self.applyScroll[1],decoration.tile])+";")
        file.write("\nenemies: ")
        spikemole = "\nspikemoles: " 
        guard = "\nguards: "
        soldier = "\nsoldiers: "
        archer = "\narchers: "
        knight = "\nknights: "
        finalBoss = "\nfinal_bosses: "
        for enemy in self.enemies:
            data = (str([enemy.rect.x + self.applyScroll[0],enemy.rect.y + self.applyScroll[1]]) + ";")
            if enemy.name == "spikemole":
                spikemole += data
            elif enemy.name == "guard":
                guard += data
            elif enemy.name == "soldier":
                soldier += data
            elif enemy.name == "archer":
                archer += data
            elif enemy.name == "knight":
                knight += data
            elif enemy.name == "final_boss":
                finalBoss += data
        file.write(spikemole+guard+soldier+archer+knight+finalBoss)
        if self.playerStart != None:
            file.write("\nplayer start: "+str((self.playerStart[0]+self.applyScroll[0],self.playerStart[1]+self.applyScroll[1])))
        else:
            file.write("\nplayer start: None")
        file.write("\nserfs: ")
        for serf in self.serfs:
            file.write(str([serf.rect.x + self.applyScroll[0],serf.rect.y + self.applyScroll[1],serf.type]) + ";") # game can be easily added in
        file.close()

# Temporarily, Keep The Editor Separate
#Editor().run()