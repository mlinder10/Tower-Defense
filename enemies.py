import pygame as pyg
from initializations import *


class Enemies(pyg.sprite.Sprite):
    def __init__(self, image, position, damage, speed, health, type):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=position)

        self.damage = damage
        self.speed = speed
        self.velocity = [self.speed, turn_directions[0]]
        self.health = health
        self.turnsMade = 0
        self.speedChanged = False
        self.type = type

        self.add(visibleSprite)
        self.add(enemySprite)
        if self.type == "red":
            self.add(redEnemies)
        elif self.type == "blue":
            self.add(blueEnemies)
        elif self.type == "white":
            self.add(whiteEnemies)
        elif self.type == "black":
            self.add(blackEnemies)

    def findVelocity(self):
        self.velocity[1] = turn_directions[self.turnsMade]
        self.velocity[0] = self.speed
        self.speedChanged = False

    def lookForTurn(self):
        for turn in turns:

            if self.velocity[1] == "right":
                if 0 <= turn[0] - self.rect.centerx <= 2:
                    self.rect.centerx = turn[0]
            elif self.velocity[1] == "left":
                if 0 <= self.rect.centerx - turn[0] <= 2:
                    self.rect.centerx = turn[0]
            if self.velocity[1] == "down":
                if 0 <= turn[1] - self.rect.centery <= 2:
                    self.rect.centery = turn[1]
            elif self.velocity[1] == "up":
                if 0 <= self.rect.centery - turn[1] <= 2:
                    self.rect.centery = turn[1]

            if self.rect.center[0] == turn[0] and self.rect.center[1] == turn[1]:
                self.turnsMade += 1
                self.findVelocity()

    def move(self):
        if self.velocity[1] == "right":
            self.rect.x += self.velocity[0]
        elif self.velocity[1] == "left":
            self.rect.x -= self.velocity[0]
        elif self.velocity[1] == "down":
            self.rect.y += self.velocity[0]
        elif self.velocity[1] == "up":
            self.rect.y -= self.velocity[0]
        self.lookForTurn()
        if self.velocity[0] != self.speed:
            self.findVelocity()

    def takeDamage(self, damage):
        global redsKilled, bluesKilled, whitesKilled, blacksKilled, points
        self.health -= damage
        if self.health <= 0:
            points.append(1)
            visibleSprite.remove(self)
            enemySprite.remove(self)
            if self.type == "red":
                self.remove(redEnemies)
                redsKilled += 1
            elif self.type == "blue":
                self.remove(blueEnemies)
                bluesKilled += 1
            elif self.type == "white":
                self.remove(whiteEnemies)
                whitesKilled += 1
            elif self.type == "black":
                self.remove(blackEnemies)
                blacksKilled += 1

    def checkAttack(self):
        global playerHealth, redsKilled, bluesKilled, whitesKilled, blacksKilled
        if self.rect.right >= 1040 or self.rect.bottom >= 640:
            for i in range(self.damage):
                playerHealth.remove(playerHealth[-1])
            visibleSprite.remove(self)
            enemySprite.remove(self)
            if self.type == "red":
                self.remove(redEnemies)
                redsKilled += 1
            elif self.type == "blue":
                self.remove(blueEnemies)
                bluesKilled += 1
            elif self.type == "white":
                self.remove(whiteEnemies)
                whitesKilled += 1
            elif self.type == "black":
                self.remove(blackEnemies)
                blacksKilled += 1


def spawnEnemies(reds, blues, whites, blacks):
    global spawnCooldown, redsKilled, bluesKilled, whitesKilled, blacksKilled, rounds

    if spawnCooldown > 0:
        spawnCooldown -= 1
    r = 0
    b = 0
    w = 0
    bl = 0

    for enemies in redEnemies:
        r += 1
    for enemies in blueEnemies:
        b += 1
    for enemies in whiteEnemies:
        w += 1
    for enemies in blackEnemies:
        bl += 1

    if r + redsKilled < reds and spawnCooldown == 0:
        enemy = Enemies(
            redEnemyTexture, start[0], 1, 2, healthAlgoRed(rounds), "red")
        spawnCooldown = 40

    elif b + bluesKilled < blues and spawnCooldown == 0:
        enemy = Enemies(
            blueEnemyTexture, start[0], 2, 2, healthAlgoBlue(rounds), "blue")
        spawnCooldown = 40

    elif w + whitesKilled < whites and spawnCooldown == 0:
        enemy = Enemies(
            whiteEnemyTexture, start[0], 5, 2, healthAlgoWhite(rounds), "white")
        spawnCooldown = 40

    elif bl + blacksKilled < blacks and spawnCooldown == 0:
        enemy = Enemies(
            blackEnemyTexture, start[0], 10, 2, healthAlgoBlack(rounds), "black")
        spawnCooldown = 40

    if reds + blues + whites + blacks == redsKilled + bluesKilled + whitesKilled + blacksKilled:
        rounds.append(1)
        redsKilled = 0
        bluesKilled = 0
        whitesKilled = 0
        blacksKilled = 0


def spawnAlgoRed(rounds):
    return len(rounds)+2


def healthAlgoRed(rounds):
    health = len(rounds)//2 + 3
    if health > 10:
        health = 10
    return health


def spawnAlgoBlue(rounds):
    if len(rounds) < 5:
        return 0
    elif 5 <= len(rounds) < 20:
        return len(rounds) - 4
    else:
        return 15


def healthAlgoBlue(rounds):
    health = len(rounds) + 5
    if health > 50:
        health = 50
    return health


def spawnAlgoWhite(rounds):
    if len(rounds) < 20:
        return 0
    elif 20 <= len(rounds) < 30:
        return len(rounds) - 19
    else:
        return 10


def healthAlgoWhite(rounds):
    health = len(rounds) * 2
    if health > 100:
        health = 100
    return health


def spawnAlgoBlack(rounds):
    if len(rounds) < 30:
        return 0
    else:
        return len(rounds) - 29


def healthAlgoBlack(rounds):
    health = len(rounds) * 3
    if health > 200:
        health = 200
    return health
