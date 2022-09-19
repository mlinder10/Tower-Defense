import pygame as pyg
from sys import exit
from initializations import *
from map import *
from towers import *
from enemies import *


class Tile(pyg.sprite.Sprite):
    def __init__(self, position, type):
        super().__init__()
        if type == 'road':
            self.image = roadTexture
        elif type == 6:
            self.image = obstacle1Texture
        elif type == 7:
            self.image = obstacle2Texture
        elif type == 8:
            self.image = obstacle3Texture
        self.rect = self.image.get_rect(topleft=position)

        self.add(visibleSprite)
        self.add(obstructionSprite)
        if type == 'road':
            self.add(roadSprite)


class Background(pyg.sprite.Sprite):
    def __init__(self, x, y, background):
        super().__init__()
        self.image = background
        self.rect = self.image.get_rect(topleft=(x*40, y*40))

        self.add(backgroundSprite)


def createBackground(backgroundTexture):
    for i in range(16):
        for j in range(32):
            background = Background(j, i, backgroundTexture)


def readMap(map):
    visibleSprite.empty()
    roadSprite.empty()
    obstructionSprite.empty()
    for count, row in enumerate(map):
        for count2, spot in enumerate(row):
            if spot == 1 or spot == 2 or spot == 3 or spot == 5:
                xPos = count2*80
                yPos = count*80
                tile = Tile((xPos, yPos), 'road')
            elif spot == 6 or spot == 7 or spot == 8:
                xPos = count2*80
                yPos = count*80
                tile = Tile((xPos, yPos), spot)


def createGrid():
    for count, row in enumerate(Map):
        for count2, spot in enumerate(row):
            grid_surf = pyg.Surface((80, 80))
            grid_rect = grid_surf.get_rect(topleft=(count2*80, count*80))
            pyg.draw.rect(screen, "Black", grid_rect, 1)


def createSideBar():
    global background_image, background_rect, pauseImage, pauseRect
    background_image = pyg.Surface((240, 640))
    background_image.fill((100, 100, 100))
    background_rect = background_image.get_rect(topleft=(1040, 0))
    pauseImage = font2.render("||", False, "black")
    pauseRect = pauseImage.get_rect(bottomleft=(1060, 620))


def hoverAnimation():
    xpos = list(pyg.mouse.get_pos())[0]
    ypos = list(pyg.mouse.get_pos())[1]
    animate = True
    if xpos < 1040:
        surface = pyg.Surface((1040, 640), pyg.SRCALPHA)
        pyg.draw.circle(surface, (255, 255, 0, 100), [xpos, ypos], int(
            selectedTower[1]*100), int(selectedTower[1]*100))
        screen.blit(surface, (0, 0))
        for sprite in obstructionSprite:
            if sprite.rect.collidepoint([xpos, ypos]):
                animate = False
    if animate is False:
        hoverSprite.empty()
        hoverTower = HoverTower(
            "red", [xpos, ypos])
        hoverTower.add(hoverSprite)
    else:
        hoverSprite.empty()
        hoverTower = HoverTower(
            selectedTower[0], [xpos, ypos])
        hoverTower.add(hoverSprite)


def selectTower():
    global selectedTower
    for sprite in towerSprite:
        if sprite.rect.collidepoint(event.pos) and len(points) >= sprite.cost:
            selectedTower = [sprite.image, sprite.range,
                             sprite.damage, sprite.fps, sprite.ID, sprite.upgradeImages, sprite.explosive, sprite.blastRadius, sprite.cost]


def placeTower():
    global selectedTower, points
    place = True
    if event.pos[0] < 1040:
        for sprite in obstructionSprite:
            if sprite.rect.collidepoint(event.pos):
                place = False
    else:
        selectedTower = "none"
        place = False
        hoverSprite.empty()
    if place is True:
        xpos = (event.pos[0]//80)*80 + 40
        ypos = (event.pos[1]//80)*80 + 40
        newTower = ActiveTower([xpos, ypos], selectedTower)
        for i in range(selectedTower[7]):
            points.remove(points[-1])
        selectedTower = "none"
        hoverSprite.empty()


def checkPlayerHealth():
    global loss
    x = 0
    for i in range(len(playerHealth)):
        x += 1
    if x == 0:
        loss == True


def displayText():
    global speedCollideRect
    pyg.draw.rect(screen, (80, 80, 80), pyg.Rect(1170, 565, 110, 75))
    pyg.draw.rect(screen, 'black', pyg.Rect(1170, 565, 110, 75), 2)

    pyg.draw.rect(screen, (80, 80, 80), pyg.Rect(1040, 0, 240, 140))
    pyg.draw.rect(screen, 'black', pyg.Rect(1040, 0, 240, 140), 2)
    pyg.draw.rect(screen, 'black', pyg.Rect(1040, 0, 240, 640), 2)

    text_img = font.render(f"Round {len(rounds)}", False, "black")
    text_rect = text_img.get_rect(center=(600, 80))
    screen.blit(text_img, text_rect)
    points_img = font2.render(
        f"Points: {len(points)}", False, "black")
    points_rect = points_img.get_rect(center=(1160, 100))
    screen.blit(points_img, points_rect)
    health_img = font2.render(
        f"Health: {len(playerHealth)}", False, "black")
    health_rect = health_img.get_rect(center=(1160, 40))
    screen.blit(health_img, health_rect)
    speedImage = font2.render(f"{gameSpeed/30}x", False, "black")
    speedRect = speedImage.get_rect(bottomright=(1260, 620))
    speedCollideRect = pyg.Rect(1170, 565, 110, 75)
    screen.blit(speedImage, speedRect)


def upgradeScreen():
    global backCollideRect, destroyCollideRect, damageCollideRect, rangeCollideRect, fpsCollideRect
    surface = pyg.Surface((1040, 640), pyg.SRCALPHA)
    pyg.draw.circle(surface, (255, 255, 0, 100), upgradingTower.rect.center, int(
                    upgradingTower.range*100), int(upgradingTower.range*100))
    screen.blit(surface, (0, 0))
    screen.blit(background_image, background_rect)

    pyg.draw.rect(screen, (80, 80, 80), pyg.Rect(1040, 565, 60, 75))
    pyg.draw.rect(screen, 'black', pyg.Rect(1040, 565, 60, 75), 2)
    backCollideRect = pyg.Rect(1040, 565, 60, 75)
    backImage = font2.render("<", False, "Black")
    backRect = backImage.get_rect(bottomleft=(1060, 620))
    screen.blit(backImage, backRect)

    destroyImage = font3.render(
        f"Destroy Tower ({int(upgradingTower.cost/2)} point)", False, "black")
    destroyRect = destroyImage.get_rect(center=(1160, 170))
    destroyCollideRect = pyg.Rect(1040, 138, 240, 60)
    pyg.draw.rect(screen, (100, 100, 100), destroyCollideRect)
    pyg.draw.rect(screen, 'black', destroyCollideRect, 2)
    screen.blit(destroyImage, destroyRect)

    damageImage = font3.render(
        f"+1 damage | {(upgradingTower.upgrades + 1) * 10} points", False, "black")
    damageRect = damageImage.get_rect(center=(1160, 230))
    damageCollideRect = pyg.Rect(1040, 196, 240, 60)
    if upgradingTower.upgrades < 4:
        pyg.draw.rect(screen, (100, 100, 100), damageCollideRect)
        pyg.draw.rect(screen, 'black', damageCollideRect, 2)
        screen.blit(damageImage, damageRect)

    rangeImage = font3.render(
        f"+1 range | {(upgradingTower.upgrades + 1) * 10} points", False, "black")
    rangeRect = rangeImage.get_rect(center=(1160, 290))
    rangeCollideRect = pyg.Rect(1040, 254, 240, 60)
    if upgradingTower.upgrades < 4:
        pyg.draw.rect(screen, (100, 100, 100), rangeCollideRect)
        pyg.draw.rect(screen, 'black', rangeCollideRect, 2)
        screen.blit(rangeImage, rangeRect)

    fpsImage = font3.render(
        f"+1 fire rate | {(upgradingTower.upgrades + 1) * 10} points", False, "black")
    fpsRect = fpsImage.get_rect(center=(1160, 350))
    fpsCollideRect = pyg.Rect(1040, 312, 240, 60)
    if upgradingTower.upgrades < 4:
        pyg.draw.rect(screen, (100, 100, 100), fpsCollideRect)
        pyg.draw.rect(screen, 'black', fpsCollideRect, 2)
        screen.blit(fpsImage, fpsRect)


def initialText():
    global map1CollideRect, map2CollideRect, map3CollideRect, submitCollideRect
    titleText = font.render("Tower Defense", False, "Black")
    titleRect = titleText.get_rect(center=(640, 80))
    titleBackgroundRect = pyg.Rect(0, 0, 1280, 150)
    pyg.draw.rect(screen, (100, 100, 100), titleBackgroundRect)
    pyg.draw.rect(screen, 'black', titleBackgroundRect, 2)
    screen.blit(titleText, titleRect)

    map1Text = font2.render("Map1", False, "Black")
    map1Rect = map1Text.get_rect(center=(213, 180))
    map1CollideRect = pyg.Rect(0, 148, 426, 60)
    if Map == map1:
        pyg.draw.rect(screen, selectColor, map1CollideRect)
    else:
        pyg.draw.rect(screen, normalColor, map1CollideRect)
    pyg.draw.rect(screen, 'black', map1CollideRect, 2)
    screen.blit(map1Text, map1Rect)

    map2Text = font2.render("Map2", False, "Black")
    map2Rect = map1Text.get_rect(center=(640, 180))
    map2CollideRect = pyg.Rect(427, 148, 426, 60)
    if Map == map2:
        pyg.draw.rect(screen, selectColor, map2CollideRect)
    else:
        pyg.draw.rect(screen, normalColor, map2CollideRect)
    pyg.draw.rect(screen, 'black', map2CollideRect, 2)
    screen.blit(map2Text, map2Rect)

    map3Text = font2.render("Map3", False, "Black")
    map3Rect = map1Text.get_rect(center=(1066, 180))
    map3CollideRect = pyg.Rect(854, 148, 426, 60)
    if Map == map3:
        pyg.draw.rect(screen, selectColor, map3CollideRect)
    else:
        pyg.draw.rect(screen, normalColor, map3CollideRect)
    pyg.draw.rect(screen, 'black', map3CollideRect, 2)
    screen.blit(map3Text, map3Rect)

    submitText = font2.render("Choose", False, "Black")
    submitRect = submitText.get_rect(bottomleft=(20, 620))
    submitCollideRect = pyg.Rect(0, 570, 170, 70)
    pyg.draw.rect(screen, (100, 100, 100), submitCollideRect)
    pyg.draw.rect(screen, 'black', submitCollideRect, 2)
    screen.blit(submitText, submitRect)


def animateMap(map):
    mapRect = pyg.Rect(380, 260, 520, 320)
    enemyRect = pyg.Rect(880, 240, 120, 120)
    enemyRect2 = pyg.Rect(850, 210, 180, 180)
    if map == map1:
        screen.blit(map1Img, mapRect)
        pyg.draw.rect(screen, "Black", mapRect, 2)
        screen.blit(map1EnemyTexture, enemyRect)
    elif map == map2:
        screen.blit(map2Img, mapRect)
        pyg.draw.rect(screen, "Black", mapRect, 2)
        screen.blit(map2EnemyTexture, enemyRect2)
    elif map == map3:
        screen.blit(map3Img, mapRect)
        pyg.draw.rect(screen, "Black", mapRect, 2)
        screen.blit(map3EnemyTexture, enemyRect2)


def chooseMap(map):
    global roadTexture, Map, obstacle1Texture, obstacle2Texture, obstacle3Texture, rawTurns, start, turns, end, turn_directions, numberOfTurns
    if map == 'map1':
        Map = map1
        roadTexture = dirtTexture
        obstacle1Texture = rockTexture
        obstacle2Texture = treeTexture
        obstacle3Texture = branchTexture
        readMap(map1)
        createBackground(grassTexture)
        findStartTurnsAndEnd(map1)
    elif map == 'map2':
        Map = map2
        roadTexture = iceTexture
        obstacle1Texture = rockTexture
        obstacle2Texture = christmasTreeTexture
        obstacle3Texture = presentTexture
        readMap(map2)
        createBackground(snowTexture)
        findStartTurnsAndEnd(map2)
    elif map == 'map3':
        Map = map3
        roadTexture = waterTexture
        obstacle1Texture = coralTexture
        obstacle2Texture = kelpTexture
        obstacle3Texture = starfishTexture
        readMap(map3)
        createBackground(sandTexture)
        findStartTurnsAndEnd(map3)


Map = map1
roadTexture = dirtTexture
obstacle1Texture = rockTexture
obstacle2Texture = treeTexture
obstacle3Texture = branchTexture
readMap(map1)
createBackground(grassTexture)
findStartTurnsAndEnd(map1)

while deciding is True:
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            pyg.quit()
            exit()

        elif event.type == pyg.MOUSEBUTTONDOWN:
            if map1CollideRect.collidepoint(event.pos):
                chooseMap('map1')
            elif map2CollideRect.collidepoint(event.pos):
                chooseMap('map2')
            elif map3CollideRect.collidepoint(event.pos):
                chooseMap('map3')

            if submitCollideRect.collidepoint(event.pos):
                deciding = False

    screen.fill('gray')
    animateMap(Map)
    initialText()
    pyg.display.update()


createSideBar()
createTowers()


while loss is False:
    backgroundSprite.draw(screen)
    screen.blit(background_image, background_rect)
    pyg.draw.rect(screen, (80, 80, 80), pyg.Rect(1040, 565, 60, 75))
    pyg.draw.rect(screen, 'black', pyg.Rect(1040, 565, 60, 75), 2)
    pauseCollideRect = pyg.Rect(1040, 565, 60, 75)
    screen.blit(pauseImage, pauseRect)
    visibleSprite.draw(screen)

    checkPlayerHealth()

    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            pyg.quit()
            exit()
        elif event.type == pyg.MOUSEBUTTONDOWN:
            if speedCollideRect.collidepoint(event.pos):
                if gameSpeed == 30:
                    gameSpeed = 60
                else:
                    gameSpeed = 30

            if selectedTower == "none":

                if event.pos[0] > 1040 and upgrade is False:
                    selectTower()
                    if pauseCollideRect.collidepoint(event.pos):
                        pause = True
                        while pause is True:
                            surface = pyg.Surface((1280, 640), pyg.SRCALPHA)
                            pyg.draw.rect(
                                surface, (100, 100, 100, 5), pyg.Rect(0, 0, 1280, 640))
                            screen.blit(surface, (0, 0))
                            resumeImage = font2.render(
                                "Resume", False, "black")
                            resumeRect = resumeImage.get_rect(
                                center=(640, 320))
                            screen.blit(resumeImage, resumeRect)
                            for event in pyg.event.get():
                                if event.type == pyg.QUIT:
                                    pyg.quit()
                                    exit()
                                elif event.type == pyg.MOUSEBUTTONDOWN:
                                    if resumeRect.collidepoint(event.pos):
                                        pause = False
                            pyg.display.update()

                elif event.pos[0] < 1040 and upgrade is False:
                    for tower in activeTowerSprite:
                        if tower.rect.collidepoint(event.pos):
                            upgrade = True
                            upgradingTower = tower

                elif upgrade is True:
                    if backCollideRect.collidepoint(event.pos):
                        upgradingTower = 'none'
                        upgrade = False

                    elif destroyCollideRect.collidepoint(event.pos):
                        for i in range(int(upgradingTower.cost/2)):
                            points.append(1)
                        visibleSprite.remove(upgradingTower)
                        activeTowerSprite.remove(upgradingTower)
                        upgradingTower = 'none'
                        upgrade = False

                    elif damageCollideRect.collidepoint(event.pos):
                        if len(points) >= (upgradingTower.upgrades+1)*10 and upgradingTower.upgrades < 4:
                            for i in range((upgradingTower.upgrades+1)*10):
                                points.remove(points[-1])
                            upgradingTower.upgrades += 1
                            upgradingTower.damage += 1
                            upgradingTower.cost += (upgradingTower.upgrades+1)*10
                            ActiveTower.updateImage(upgradingTower)

                    elif rangeCollideRect.collidepoint(event.pos):
                        if len(points) >= (upgradingTower.upgrades+1)*10 and upgradingTower.upgrades < 4:
                            for i in range((upgradingTower.upgrades+1)*10):
                                points.remove(points[-1])
                            upgradingTower.upgrades += 1
                            upgradingTower.range += 0.1
                            upgradingTower.cost += (upgradingTower.upgrades+1)*10
                            ActiveTower.updateImage(upgradingTower)

                    elif fpsCollideRect.collidepoint(event.pos):
                        if len(points) >= (upgradingTower.upgrades+1)*10 and upgradingTower.upgrades < 4:
                            for i in range((upgradingTower.upgrades+1)*10):
                                points.remove(points[-1])
                            upgradingTower.upgrades += 1
                            upgradingTower.fps += 1
                            upgradingTower.cost += (upgradingTower.upgrades+1)*10
                            ActiveTower.updateImage(upgradingTower)

            else:
                placeTower()

    if upgrade is True:
        upgradeScreen()

    for sprite in enemySprite:
        Enemies.move(sprite)
        Enemies.checkAttack(sprite)
    spawnEnemies(spawnAlgoRed(rounds), spawnAlgoBlue(rounds),
                 spawnAlgoWhite(rounds), spawnAlgoBlack(rounds))
    for sprite in activeTowerSprite:
        ActiveTower.checkForAttacks(sprite)

    if selectedTower != "none":
        hoverAnimation()
        createGrid()

    hoverSprite.draw(screen)
    displayText()

    pyg.display.update()
    clock.tick(gameSpeed)
