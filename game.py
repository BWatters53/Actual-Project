#############
# LIBRARIES #
#############
import pygame
import random as r
from scripts.entity import Entity, Player, Enemy, Guard, Soldier, Archer
from scripts.tile import Tile, BouncePad, MovingPlatform, Horizontal, Vertical, ClimbingWall
from scripts.utils import loadLevel, loadImg, animate, loadImages, loadSounds
from scripts.label import Label,Banner,Button, Textbox
from scripts.particle import Particle
from scripts.account import Account
from editor import Editor
from scripts.leaderboard import Leaderboard
pygame.init()
pygame.mixer.init()
#//////\\\\\\#
#=GAME CLASS=#
#\\\\\\//////#
class Game:
    #=##############=#
    # INITIALISATION #
    #=##############=#
    def __init__(self):
        self.name = "game"
        # Window
        self.windowWidth = 1500 # /3 = 500
        self.windowHeight = 780 # /3 = 260
        self.screen = pygame.display.set_mode((self.windowWidth,self.windowHeight))
        pygame.display.set_caption("Bobbin Dud")
        self.scaleFactor = 3
        self.display = pygame.Surface((self.windowWidth//self.scaleFactor +10, self.windowHeight//self.scaleFactor +10))
        self.mainFont1 = pygame.font.SysFont("oldenglishtext",100)
        self.mainFont2 = pygame.font.SysFont("oldenglishtext",50)
        # Game Running Variables
        self.pause = False
        self.running = True
        self.clock = pygame.time.Clock()
        self.deathCounter = 0
        self.assets = { # All Of The Frames For The Game
            # Player #
            "player":{"idle":{"frames":loadImages("bobbin_dud/idle"),"frameCounter":7},
                    "run":{"frames":loadImages("bobbin_dud/run"),"frameCounter":4},
                    "jump":{"frames":loadImages("bobbin_dud/jump"),"frameCounter":4},
                    "fall":{"frames":loadImages("bobbin_dud/fall"),"frameCounter":4},
                    "climb":{"frames":loadImages("bobbin_dud/climb"),"frameCounter":5},
                    "light_attack":{"frames":loadImages("bobbin_dud/light_attack"),"frameCounter":6},
                    "heavy_attack":{"frames":loadImages("bobbin_dud/heavy_attack"),"frameCounter":6},
                    "bow_attack":{"frames":loadImages("bobbin_dud/bow_attack"),"frameCounter":8},
            },
            # Enemies #
            "guard":{"idle":{"frames":loadImages("guard/idle"),"frameCounter":6},
                    "attack":{"frames":loadImages("guard/idle"),"frameCounter":7},
                    "light_attack":{"frames":loadImages("guard/light_attack"),"frameCounter":9}
            },
            "soldier":{"idle": {"frames":loadImages("soldier/idle"),"frameCounter":6},
                    "attack": {"frames":loadImages("soldier/idle"),"frameCounter":5},
                    "light_attack": {"frames":loadImages("soldier/light_attack"),"frameCounter":7},
            },
            "archer":{"idle": {"frames":loadImages("archer/idle"),"frameCounter":8},
                    "attack": {"frames":loadImages("archer/attack"),"frameCounter":8},# No animations here
                    "fall": {"frames":loadImages("archer/idle"),"frameCounter":8}, # Needed for loading levels
            },
            "knight":{"idle":{"frames":loadImages("knight/idle"),"frameCounter":8},
                    "charge":{"frames":loadImages("knight/charge"),"frameCounter":5},
            },
            "spikemole":{"up":{"frames":loadImages("spikemole/up"),"frameCounter":35},
                    "down":{"frames":loadImages("spikemole/down"),"frameCounter":5},
            },
            "final_boss":{"idle":{"frames":loadImages("final_boss/idle"),"frameCounter":7},
                    "attack":{"frames":loadImages("final_boss/attack"),"frameCounter":4},
                    "chase":{"frames":loadImages("final_boss/chase"),"frameCounter":6},
                    "partial_retreat":{"frames":loadImages("final_boss/partial_retreat"),"frameCounter":7},
                    "full_retreat":{"frames":loadImages("final_boss/full_retreat"),"frameCounter":8},
            },
            # Weaponary #
            "sword":loadImg("sword"),
            "spear":loadImg("spear"),
            "bow":loadImg("bow"),
            "enemy_bow":loadImg("enemy_bow"),
            "arrow":loadImg("arrow"),
            "coin":loadImg("coin"),
            "boss_sword_1":loadImg("boss_sword"),
            "boss_sword_2":loadImg("boss_sword_2"),
            # Tiles #
            "0":loadImages("tiles/tile/grass"),
            "1":loadImages("tiles/tile/dirt"),
            "2":loadImages("tiles/tile/stone"),
            "3":loadImages("decor"),
            "4":loadImages("tiles/moving_platform") + loadImages("tiles/climbing_wall") + loadImages("tiles/bounce_pad"),
            # Serfs #
            "serf":loadImages("serf"),
            # Main Menu #
            "logo":loadImg("logo"),
            # Olde Shoppe
            "olde_shoppe":loadImg("shoppe_1"),
        }
        self.state = "main_menu"

        # MUSIC & SFX
        self.bgMusic = pygame.mixer.Channel(1)
        self.bgMusic.set_volume(0.3)
        self.enemyMusic = pygame.mixer.Channel(3) # The enemies all share a channel
        self.projectileMusic = pygame.mixer.Channel(4)
        self.menuMusic = pygame.mixer.Channel(5)
        self.mute = False
        self.sounds = { # All The Sounds For The Game
            "background":loadSounds("background"),
            "validation":loadSounds("validation"),
            "error":loadSounds("error"),
            "leaderboard":loadSounds("leaderboard"),
            # Player Sounds #
            "grass":loadSounds("grass"),
            "stone":loadSounds("stone"),
            "jump":loadSounds("jump"),
            "bow":loadSounds("bow"),
            "climb":loadSounds("climb"),
            "light_attack":loadSounds("light_attack"),
            "heavy_attack":loadSounds("heavy_attack"),
            "death":loadSounds("death"),
            # Guard/Soldier # (Uses other sounds as well)
            "grunt":loadSounds("grunt"),
            # Spikemole Sound #
            "spikemole":loadSounds("spikemole"),
            # Final Boss Sounds #
            "boss_attack":loadSounds("boss_attack"),
            "partial_retreat":loadSounds("partial_retreat"),
            "full_retreat":loadSounds("full_retreat"),
            # Projectile Sounds #
            "arrow":loadSounds("arrow"),
            "coins":loadSounds("coins"),
        }

        # Map Variables
        self.scroll = [0,0]
        self.scrollThreshold = {"x":self.display.get_width()*(5/6), "y":self.display.get_height()*(5/6)}
        # Level Variables
        self.movement = [0,0]
        self.transitionCounter = 0
        self.projectiles = []
        self.particles = []
        self.bgMusic.play(self.sounds["background"][2], -1)
        self.loadGame(["BOBBIN DUD", "Loading..."],1)
        self.endGameCounter = 160
        self.screenshakeStrength = 0

        # Banner Variables
        self.gameBanner = loadImg("BannerBoard")
        self.inLevelBanners = [Banner(4,13,self.player.maxHP,"counter"), Banner(38,13,self.player.lives,"counter"),Banner(66,13,self.player.score,"counter")]
        self.inLevelLabels = [Label(7,2,"HP"),Label(27,2,"LIVES"),Label(55,2,"SCORE")]

        self.buttons = { # There are a lot of buttons, so this is an efficient way to store and call them
            "main_menu":[Button(15+self.display.get_width()//2,self.display.get_height()//2,"PLAY GAME","transition",destination="play_menu"),Button(15+self.display.get_width()//2,self.display.get_height()//2+20,"ACCOUNT MANAGEMENT","transition",destination="account_menu"),
                         Button(15+self.display.get_width()//2,self.display.get_height()//2+40,"LEADERBOARDS","transition",destination="leaderboards"),Button(15+self.display.get_width()//2,self.display.get_height()//2+60,"LEVEL EDITOR","transition",destination="editor")],
            "account_menu":[Button(10,10,"BACK","transition",destination="main_menu"), Button(self.display.get_width()//2-65,60,"CREATE ACCOUNT","transition",destination="account_creation"), Button(self.display.get_width()//2-20,40,"LOGIN","transition",destination="account_login")],
            "account_creation":[Button(0,150,"SUBMIT","submit",subtype="create_account"),Button(10,10,"BACK","transition",destination="account_menu")],
            "account_login":[Button(0,150,"SUBMIT","submit",subtype="validate_account"),Button(10,10,"BACK","transition",destination="account_menu")],
            "play_menu":[Button(self.display.get_width()//2-40,40,"PLAY CAMPAIGN","transition",destination="game"),Button(self.display.get_width()//2-35,60,"PLAY CUSTOM","transition",destination="custom"),Button(10,10,"BACK","transition",destination="main_menu")],
            "game":[Button(self.display.get_width()-34,2,"EXIT","transition",destination="play_menu")],
            "custom":[Button(self.display.get_width()-34,2,"EXIT","transition",destination="play_menu")],
            "olde_shoppe":[Button(self.display.get_width()*0.25,self.display.get_height()*0.9,"","upgrade","attack"),Button(self.display.get_width()*0.5,self.display.get_height()*0.9,"","upgrade","defence"),
                           Button(self.display.get_width()*0.75,self.display.get_height()*0.9,"","upgrade","speed"), Button(self.display.get_width()-90,30,"CONTINUE","transition",destination="game")],
            "editor":[Button(self.display.get_width()-42,self.display.get_height()-24,"BACK","transition",destination="main_menu")],
            "leaderboards":[Button(0,0,"BACK","transition",destination="main_menu")],
        }
        
        # Editor
        self.editor = Editor(self.display,self)

        # Account Menus
        self.menuFont = pygame.font.SysFont("Castellar", 20)
        self.accountMenuTextboxes = [Textbox(self.display.get_width()//2-85,70,"","Username"), Textbox(self.display.get_width()//2-85,120,"","Password")]
        self.shift = False
        self.shiftReferences = {"1":"!","2":"\"","3":"£","4":"$","5":"%","6":"^","7":"&","8":"*","9":"(","0":")","-":"_","=":"+","[":"{","]":"}","`":"¬",";":":","'":"@","#":"~","\\":"|","/":"?",",":"<",".":">"}
        self.createAccount("TEMP","1234") # GUEST account
        self.guest = self.loadAccount("TEMP")
        self.user = self.guest

        # Leaderboard Stuff
        self.leaderboards = [Leaderboard("MOST JUMPS",self.display.get_width()//2-245,30,self,"no. jumps"),Leaderboard("TOP SCORES",self.display.get_width()//2-80,25,self,"total score"),
                             Leaderboard("MOST DEATHS",self.display.get_width()//2+85,30,self,"no. deaths"),]

        # Testing Temps
        # self.player.score = 1000
    # Level Loading Adjustment
    def loadLevel(self,filename):
        tilemap,bouncepads,movingplatforms,climbingwalls,enemies,playerStart,decor,serfs = loadLevel(filename,self)
        return {"tilemap":tilemap,"bouncepads":bouncepads,"movingplatforms":movingplatforms,"climbingwalls":climbingwalls,"enemies":enemies,"playerStart":playerStart,"decor":decor,"serfs":serfs}
    # Used At The Start When Loading All the Data
    # Used At Game Over As Well
    def loadGame(self,text,level):
        self.screen.fill((48,52,29))
        self.loadingtext = [self.mainFont1.render(text[0],False,(137,87,39)),self.mainFont2.render(text[1],False,(137,87,39))]
        for index,item in enumerate(self.loadingtext):
            self.screen.blit(item,(self.screen.get_width()//2-item.get_width()//2, -((2-index)*100)+self.screen.get_height()//2-item.get_height()//2))
        pygame.display.update()
        self.currentLevel = level
        self.movement = [0,0]
        self.scrollTotal = [0,0]
        self.levels = {
            1:self.loadLevel("1"),
            2:self.loadLevel("2"),
            3:self.loadLevel("3"),
            "custom":self.loadLevel("temp"),
        }
        self.tilemap,self.bouncepads,self.movingplatforms,self.climbingwalls,self.enemies,self.playerStart,self.decor,self.serfs = [value for key,value in self.levels[self.currentLevel].items()]
        self.player = Player(self, self.playerStart[0], self.playerStart[1])
        pygame.time.delay(2500) # This can be removed if the game starts to take longer to load

    # ACCOUNT CREATION METHOD #
    def createAccount(self,username,password):
        if len(username)>0 and len(password)>0: # For validating length etc.
            file = open(f"accounts/{username}.txt", "w")
            try:
                if self.user.username == "TEMP":
                    file.write(f"[USERNAME]: {username}\n[PASSWORD]: {password}\n[STATS]:\n    [no. jumps]: {self.user.stats["no. jumps"]}\n    [total score]: {self.user.stats["total score"]}\n    [no. deaths]: {self.user.stats["no. deaths"]}\n[LEVEL]:\n")
                else:
                    file.write(f"[USERNAME]: {username}\n[PASSWORD]: {password}\n[STATS]:\n    [no. jumps]: 0\n    [total score]: 0\n    [no. deaths]: 0\n[LEVEL]:\n")
            except AttributeError:
                file.write(f"[USERNAME]: {username}\n[PASSWORD]: {password}\n[STATS]:\n    [no. jumps]: 0\n    [total score]: 0\n    [no. deaths]: 0\n[LEVEL]:\n")
            file.close()
            return "ACCOUNT SUCCESSFULLY CREATED"
        else:
            return "YOU ARE MISSING SOME CREDENTIALS"
    # ACCOUNT LOADING METHOD #
    def loadAccount(self,username):
        try:
            file = open(f"accounts/{username}.txt", "r")
            stats = {"no. jumps":0, "total score":0, "no. deaths":0}
            lines = file.readlines()
            for indx, line in enumerate(lines):
                if line[:10] == "[PASSWORD]":
                    password = line[12:]
                elif line[:15] == "    [no. jumps]":
                    stats["no. jumps"] = int(line[17:])
                elif line[:17] == "    [total score]":
                    stats["total score"] = int(line[19:])
                elif line[:16] == "    [no. deaths]":
                    stats["no. deaths"] = int(line[18:])
                elif line[:7] == "[LEVEL]":
                    tempFile = open("scripts/levels/temp.txt","w")
                    for line in lines[indx+1:]:
                        tempFile.write(str(line))
                    tempFile.close()
                    level = self.loadLevel("temp")
            file.close()
            return Account(stats,username,password,level)
        
        except FileNotFoundError:
            return "error"
        
    # ACCOUNT VALIDATION METHOD #
    def validateAccount(self,username,password):
        try:
            file = open(f"accounts/{username}.txt","r")
            for line in file.readlines():
                if line[:10] == "[PASSWORD]":
                    if password == line[12:-1]: # Removes the \n from the equation
                        return "WELCOME BACK!"
                    else:
                        return "INCORRECT PASSWORD"
        except FileNotFoundError:
            return "THAT USER DOES NOT EXIST"
        
    
    # Textbox Management
    def manageTextboxes(self,event):
        # For Typing In Textboxes Boxes
        if event.type == pygame.KEYDOWN:
            for textbox in self.accountMenuTextboxes:
                if textbox.focus and len(textbox.storedText) < 20:
                    match event.key:
                        case pygame.K_LSHIFT | pygame.K_RSHIFT | pygame.K_CAPSLOCK: # For Capitalisation
                            self.shift = not self.shift
                        case pygame.K_SPACE:
                            textbox.storedText += " "
                        case _:
                            if event.key >= 35 and event.key <= 122:
                                if event.key >= 97 and event.key <= 122 and self.shift:
                                    #print(65+(event.key-97), chr(65+(event.key-97))) # 65 is "A"
                                    textbox.storedText += chr(65+(event.key-97))
                                elif chr(event.key) in self.shiftReferences and self.shift: # Account for all other shifts
                                    textbox.storedText += self.shiftReferences[chr(event.key)]
                                else:
                                    #print(event.key,chr(event.key))
                                    textbox.storedText += chr(event.key)
                if textbox.focus and len(textbox.storedText) <= 20 and len(textbox.storedText) > 0:
                    if event.key == pygame.K_BACKSPACE:
                        textbox.storedText = textbox.storedText[:-1] # Remove The Final Character
                #print(textbox.storedText, len(textbox.storedText))
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
                self.shift = not self.shift
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for textbox in self.accountMenuTextboxes:
                if textbox.rect.collidepoint(self.mpos):
                    textbox.focus = True
                else:
                    textbox.focus = False

    #===========#
    #-MAIN LOOP-#
    #===========#
    def run(self):
        while self.running:
            # Rendering
            # Manage Screenshake
            self.screen.fill((135,206,225))
            self.screen.blit(pygame.transform.scale(self.display, (self.windowWidth + 30,self.windowHeight + 30)), (-10+self.screenshakeStrength*r.choice([-1,1]),-10+self.screenshakeStrength*r.choice([-1,1])))
            self.screenshakeStrength = max(0, self.screenshakeStrength-0.4)
            self.display.fill((135,206,225))
            # Mouse Management
            self.mpos = [pygame.mouse.get_pos()[0]//self.scaleFactor,pygame.mouse.get_pos()[1]//self.scaleFactor]

            # Game Management
            # Level Transition
            if len(self.enemies) == 0:
                flag = True
            else:
                flag = True
                for enemy in self.enemies:
                    if enemy.state not in ("up","down"): # i.e. not a spikemole
                        flag = False
            if flag:
                if self.currentLevel == "custom" or self.currentLevel == 3:
                    self.endGameCounter -= 1
                    if self.endGameCounter == 0:
                        self.loadGame(["CONGRATULATIONS","You Win!!!"],1)
                        self.user.updateStats()
                        self.state = "play_menu"
                else:
                    if self.currentLevel < 3:
                        self.state = "olde_shoppe" # The Olde Shoppe Will Not Appear At The End
                    self.particles = []
                    self.currentLevel += 1
                    if self.currentLevel < 4:
                        self.transitionCounter = 50
                        self.tilemap,self.bouncepads,self.movingplatforms,self.climbingwalls,self.enemies,self.playerStart,self.decor,self.serfs = [value for key,value in self.levels[self.currentLevel].items()]
                        self.player = Player(self,self.playerStart[0],self.playerStart[1],lives=self.player.lives,hp=self.player.maxHP,strengthMultiplier=self.player.strengthMultiplier,speed=self.player.speed,score=self.player.score) # Account For Upgraded values
                        self.scrollTotal = [0,0]
            
            if self.state in ("main_menu", "account_menu", "play_menu", "olde_shoppe","leaderboards"):
                if self.state == "account_menu":
                    self.stateText = self.menuFont.render("ACCOUNTS",False,(137,87,39))
                    self.display.blit(self.stateText,(self.display.get_width()//2-self.stateText.get_width()//2,4))
                elif self.state == "play_menu":
                    self.stateText = self.menuFont.render("PLAY",False,(137,87,39))
                    self.display.blit(self.stateText,(self.display.get_width()//2-self.stateText.get_width()//2,4))
                if self.state == "main_menu":
                    self.display.blit(self.assets["logo"],(self.display.get_width()//2-self.assets["logo"].get_width()//2,2))
                    self.display.blit(pygame.transform.scale(pygame.transform.flip(self.assets["player"]["bow_attack"]["frames"][0],True,False),
                                                             (self.assets["player"]["bow_attack"]["frames"][0].get_width()*7,self.assets["player"]["bow_attack"]["frames"][0].get_height()*7)),
                                                             (self.display.get_width()-self.assets["player"]["bow_attack"]["frames"][0].get_width()*7-40,97))
                    self.display.blit(pygame.transform.scale(self.assets["final_boss"]["attack"]["frames"][0],(self.assets["final_boss"]["attack"]["frames"][0].get_width()*7,self.assets["final_boss"]["attack"]["frames"][0].get_height()*7)),(40,97))
                    self.display.blit(pygame.transform.scale(self.assets["bow"],(self.assets["bow"].get_width()*7,self.assets["bow"].get_height()*7)),(self.display.get_width()-self.assets["bow"].get_width()*7-19,112))
                elif self.state == "olde_shoppe":
                    self.display.blit(self.assets["olde_shoppe"],(self.display.get_width()//2-self.assets["olde_shoppe"].get_width()//8-50,-5))
                    self.movement = [0,0]
                elif self.state == "leaderboards":
                    for leaderboard in self.leaderboards:
                        leaderboard.render()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        for button in self.buttons[self.state]:
                            if button.rect.collidepoint(self.mpos):
                                button.onClick(self)
            
            elif self.state in ("account_login", "account_creation"):
                if self.state == "account_login":
                    self.stateText = self.menuFont.render("LOGIN",False,(137,87,39))
                else:
                    self.stateText = self.menuFont.render("CREATE ACCOUNT",False,(137,87,39))
                self.display.blit(self.stateText,(self.display.get_width()//2-self.stateText.get_width()//2,4))
                for textbox in self.accountMenuTextboxes:
                    textbox.update()
                    textbox.render(self.display)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        for button in self.buttons[self.state]:
                            if button.rect.collidepoint(self.mpos):
                                button.onClick(self)
                    self.manageTextboxes(event)
            
            elif self.state == "editor":
                self.editor.run()                    

            #THE GAME
            elif self.state == "game" or self.state == "custom":
                # Music
                if not self.mute and self.bgMusic.get_volume() == 0:
                    self.bgMusic.set_volume(0.3)
                    if self.currentLevel == "custom" or self.currentLevel < 3:
                        self.bgMusic.play(self.sounds["background"][1],-1)
                    else:
                        self.bgMusic.play(self.sounds["background"][0],-1)
                # Settings Stuff
                self.channels = [self.projectileMusic,self.player.music,self.enemyMusic]
                for channel in self.channels:
                    if channel.get_busy() and self.mute:
                        channel.pause()
                for decoration in self.decor:
                    decoration.render(self,self.scroll)
                # Serfs
                for serf in self.serfs:
                    serf.update()
                    serf.render(self.scroll)
                self.scroll = [0,0]
                # Player Generation
                if self.player.alive:
                    self.player.update()
                    if self.player.climbing and self.player.stamina > self.player.climbCounter:
                        self.player.climb()
                    elif self.player.loading and self.player.bowAttackCooldown == 0:
                        self.player.changeState("bow_attack")
                        self.player.bowAttack()
                    elif self.player.lightAttacking:
                        self.player.changeState("light_attack")
                        self.player.lightAttack(self.player.sword)
                    elif self.player.heavyAttacking:
                        self.player.changeState("heavy_attack")
                        self.player.heavyAttack()
                    else:
                        self.player.sword.damage = 0
                    animate(self.player)
                    self.player.render()
                # Falling Player
                if self.player.fallCounter >= 90 and self.player.fallCounter%7 == 0:
                    self.player.hp = max(0, self.player.hp-r.randint(7,17)) # Death To The Void
                # Player Death
                if self.player.hp == 0 and self.player.alive:
                    self.player.alive = False
                    self.player.music.play(self.sounds["death"][1])
                    self.user.stats["no. deaths"] += 1
                    self.player.score -= self.player.pointsValue
                if not self.player.alive: # In Case Of Other Means Of Death
                    if self.deathCounter == 0:
                        self.deathCounter += 1
                        # Create A Coin Shower
                        for i in range(self.player.pointsValue):
                            self.particles.append(Particle(self.player.rect.centerx,self.player.rect.centery,"player",self))
                    elif self.deathCounter > 90:
                        if self.player.lives > 1:
                            self.player = Player(self, self.playerStart[0], self.playerStart[1],self.player.lives,score=self.player.score,hp=self.player.maxHP,strengthMultiplier=self.player.strengthMultiplier,speed=self.player.speed)
                            self.scroll = self.scrollTotal
                            self.scrollTotal = [0,0]
                            self.player.lives -= 1
                        else: # Go back to level 1
                            self.transitionCounter = 50
                            self.loadGame(["GAME OVER!!!", "You Lose"],1)
                            self.player.score = 0
                            self.buttons["olde_shoppe"] = [Button(self.display.get_width()*0.25,self.display.get_height()*0.9,"","upgrade","attack"),Button(self.display.get_width()*0.5,self.display.get_height()*0.9,"","upgrade","defence"),
                                                  Button(self.display.get_width()*0.75,self.display.get_height()*0.9,"","upgrade","speed"), Button(self.display.get_width()-90,30,"CONTINUE","transition",destination="game")]
                            self.bgMusic.play(self.sounds["background"][1],-1)
                        self.deathCounter = 0
                        self.player.alive = True
                    else:
                        self.deathCounter += 1

                # Map Generation
                for enemy in self.enemies:
                    if abs(enemy.rect.x-self.player.rect.x) < 500 and abs(enemy.rect.y-self.player.rect.y) < 260:# Lag Reduction
                        animate(enemy)
                        enemy.update()
                    enemy.render(self.scroll)
                for tile in self.tilemap:
                    tile.render(self, self.scroll)
                for bouncepad in self.bouncepads:
                    bouncepad.render(self, self.scroll)
                for movingplatform in self.movingplatforms:
                    movingplatform.update(self.scroll)
                    movingplatform.render(self, self.scroll)
                for climbingwall in self.climbingwalls:
                    climbingwall.render(self, self.scroll)
                # Projectile Rendering
                for projectile in self.projectiles.copy():
                    alive = projectile.update()
                    if not alive:
                        self.projectiles.remove(projectile)
                    projectile.render()
                # Particle Rendering
                for particle in self.particles:
                    particle.update()
                    particle.render()
                if self.pause:
                    pygame.draw.rect(self.display,"white",pygame.Rect((self.display.get_width()//2)-17,(self.display.get_height()//2)-20,15,40))
                    pygame.draw.rect(self.display,"white",pygame.Rect((self.display.get_width()//2)+3,(self.display.get_height()//2)-20,15,40))

                # Event Management
                for event in pygame.event.get():
                    # KEY PRESSES #
                    if event.type == pygame.KEYDOWN:
                        # SETTINGS
                        if event.key == pygame.K_m: # MUTE
                            self.mute = not self.mute
                            self.bgMusic.set_volume(0)
                            for channel in self.channels:
                                if not channel.get_busy() and not self.mute:
                                    channel.unpause()
                        if event.key == pygame.K_p: # PAUSE
                            self.pause = not self.pause
                        # MOVEMENT
                        if event.key in (pygame.K_a, pygame.K_LEFT):
                            self.movement[0] = 1
                        if event.key in (pygame.K_d, pygame.K_RIGHT):
                            self.movement[1] = 1
                        if event.key in (pygame.K_w, pygame.K_UP):
                            self.player.jump()
                        # SERFS
                        if event.key == pygame.K_q and not self.pause:
                            for serf in self.serfs:
                                if serf.valid and serf.alive:
                                    result = serf.rollReward()
                                    if result:
                                        serf.alive = False
                        # Temp Tests
                        if event.key == pygame.K_e:
                            print(self.particles)
                            print(f"SPEED {self.player.speed}\nATTACK {self.player.strengthMultiplier}\nHP {self.player.maxHP}\n {self.player.hp}\n LIVES {self.player.lives}\n SCORE {self.player.score}")
                        # MELEE ATTACKS
                        if not self.pause:
                            if event.key == pygame.K_x:
                                if self.player.lightAttackCooldown == 0 and not(self.player.lightAttacking):
                                    self.player.lightAttacking = True
                                    self.player.lightAttackDir = self.player.dir
                                    self.player.sword.damage = 5*self.player.strengthMultiplier
                            if event.key == pygame.K_z:
                                if self.player.heavyAttackCooldown == 0 and not(self.player.heavyAttacking):
                                    self.player.heavyAttacking = True
                                    self.player.heavyAttackDir = self.player.dir
                                    self.player.climbShock = 12 * self.player.heavyAttackDir # The Player Charges Forward (reusing old code)
                                    self.player.sword.attackX -= self.player.heavyAttackDir * (self.player.sword.rect.width + 15)
                        # KEY RELEASES #
                    if event.type == pygame.KEYUP:
                        if event.key in (pygame.K_a, pygame.K_LEFT):
                            self.movement[0] = 0
                        if event.key in (pygame.K_d, pygame.K_RIGHT):
                            self.movement[1] = 0
                    # BOW ATTACK
                    if not self.pause:
                        if event.type == pygame.MOUSEBUTTONDOWN: 
                            if event.button == 1:
                                if self.buttons[self.state][0].rect.collidepoint(self.mpos):
                                    self.buttons[self.state][0].onClick(self)
                                else:
                                    self.player.loading = True # Loading Arrow

                        if event.type == pygame.MOUSEBUTTONUP: 
                            if event.button == 1:
                                if self.player.loading:
                                    self.player.loading = False # Releasing Arrow
                                    self.player.bowAttack()
                    if event.type == pygame.QUIT:
                        self.running = False
            if self.state in ("olde_shoppe","game","custom"):
                # Banner Management
                self.display.blit(self.gameBanner,(-7,-4))
                stats = [self.player.hp,self.player.lives,self.player.score]
                for indx, banner in enumerate(self.inLevelBanners):
                    banner.update(stats[indx])
                    banner.render(self.display)
                for label in self.inLevelLabels:
                    label.render(self.display)  
                
            # Level Transition Management
            if self.transitionCounter > 0:
                self.transitionFont = pygame.font.SysFont("oldenglishtext",self.transitionCounter)
                self.transitionText = self.transitionFont.render("BOBBIN DUD",False,(137,87,39))
                self.transitionCounter -= 1
                width = self.transitionCounter*(self.display.get_width()//50)
                height = self.transitionCounter*(self.display.get_height()//50)
                pygame.draw.rect(self.display, (48,52,29), pygame.Rect((self.display.get_width()-width)//2,(self.display.get_height()-height)//2,width,height))
                self.display.blit(self.transitionText,((self.display.get_width()-width)//2 +(width-self.transitionText.get_width())//2,(self.display.get_height()+height//4)//2-self.transitionCounter))                

            # button management
            for button in self.buttons[self.state]:
                button.render(self.display)

            # SHOW USERNAME
            if self.state != "editor":
                self.usernameLabel = Label(self.display.get_width()-120,0,self.user.username)
                self.usernameLabel.render(self.display)
            # Clock/ Update Management
            self.clock.tick(60)
            pygame.display.update()

        self.user.updateStats()
        file = open("scripts/levels/temp.txt", "w")
        file.close()
        pygame.quit()

#-Launch the game
game = Game()
game.run()
