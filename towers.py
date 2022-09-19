import pygame as pyg
from initializations import *
from math import atan, sin, cos


class Tower(pyg.sprite.Sprite):
    def __init__(self, texture, upgradeImages, range, damage, fps, number, ID, cost, explosive=False, blastRadius=0):
        super().__init__()
        self.image = texture
        self.rect = self.image.get_rect(
            topleft=(1055 + ((number % 2)*110), 165 + (number//2)*110))

        self.range = range
        self.damage = damage
        self.fps = fps
        self.explosive = explosive
        self.blastRadius = blastRadius
        self.ID = ID
        self.cost = cost
        self.upgradeImages = upgradeImages

        self.add(visibleSprite)
        self.add(towerSprite)


class ActiveTower(pyg.sprite.Sprite):
    def __init__(self, position, type):
        super().__init__()
        self.image = type[0]
        self.rect = self.image.get_rect(center=position)
        self.range = type[1]
        self.damage = type[2]
        self.fps = type[3]
        self.ID = type[4]
        self.explosive = type[6]
        self.blastRadius = type[7]
        self.cooldown = 10
        self.cost = type[8]
        self.upgrades = 0
        upgradeImages = type[5]

        self.upgrade1 = upgradeImages[0]
        self.upgrade2 = upgradeImages[1]
        self.upgrade3 = upgradeImages[2]
        self.upgrade4 = upgradeImages[3]
        self.basicTowerSpecial = False
        self.rangeTowerSpecial = False
        self.fastTowerSpecial = False
        self.damageTowerSpecial = False
        self.explosiveTowerSpecial = False

        self.add(visibleSprite)
        self.add(activeTowerSprite)

    def attack(self, target):
        target.takeDamage(self.damage)
        pyg.draw.line(screen, "red", self.rect.center, target.rect.center, 5)
        if self.damageTowerSpecial is True:
            if self.damageAttackCooldown == 0:
                self.damageTowerAttack(target)
            else:
                self.damageAttackCooldown -= 1
        elif self.rangeTowerSpecial is True:
            self.rangeTowerAttack(target)
        elif self.basicTowerSpecial is True:
            self.basicTowerAttack(target)
        self.cooldown = 30

    def explosiveAttack(self, target):
        target.takeDamage(self.damage)
        pyg.draw.line(screen, "red", self.rect.center,
                      target.rect.center, 10)
        screen.blit(explosionAnimation, target.rect)
        for sprite in enemySprite:
            if target != sprite:
                if ((target.rect.centerx-sprite.rect.centerx)**2+(target.rect.centery-sprite.rect.centery)**2)**(1/2) <= self.blastRadius:
                    sprite.takeDamage(self.damage)
                    if self.explosiveTowerSpecial is True:
                        self.explosiveTowerAttack(sprite)
        self.cooldown = 30

    def checkForAttacks(self):
        if self.cooldown > 0:
            self.cooldown -= self.fps
        if self.cooldown < 0:
            self.cooldown = 0
        if self.cooldown == 0:
            hits = 0
            for sprite in enemySprite:
                if ((sprite.rect.centerx - self.rect.centerx)**2 + (sprite.rect.centery - self.rect.centery)**2)**(1/2) <= self.range*100:
                    if hits == 0:
                        if self.explosive == False:
                            self.attack(sprite)
                        else:
                            self.explosiveAttack(sprite)
                        hits += 1
        if self.fastTowerSpecial is True:
            for sprite in enemySprite:
                if ((sprite.rect.centerx - self.rect.centerx)**2 + (sprite.rect.centery - self.rect.centery)**2)**(1/2) <= self.range*100:
                    self.fastTowerAttack(sprite)

    def updateImage(self):
        if self.upgrades == 1:
            self.image = self.upgrade1
        elif self.upgrades == 2:
            self.image = self.upgrade2
        elif self.upgrades == 3:
            self.image = self.upgrade3
        elif self.upgrades == 4:
            self.image = self.upgrade4
            self.specialUpgrade()

    def fastTowerAttack(self, target):
        if target.speedChanged is False:
            target.velocity[0] = target.velocity[0] / 2
            target.speedChanged = True

    def damageTowerAttack(self, target):
        if target.type == 'white':
            target.takeDamage(target.health*0.25)
        elif target.type == 'black':
            target.takeDamage(target.health*0.1)
        else:
            target.takeDamage(target.health)
        self.damageAttackCooldown = 5

    def rangeTowerAttack(self, target):
        if target.rect.centerx == self.rect.centerx:
            targetx = target.rect.centerx + 1
        else:
            targetx = target.rect.centerx
        targety = target.rect.centery
        selfx = self.rect.centerx
        selfy = self.rect.centery
        if target.rect.centerx > self.rect.centerx:
            angle = atan((targety-selfy)/(targetx-selfx))
            pyg.draw.line(screen, "red", self.rect.center,
                          (2000*cos(angle)+self.rect.centerx, 2000*sin(angle)+self.rect.centery), 5)
            for i in range(0, 2000, 2):
                for enemy in enemySprite:
                    if enemy.rect.collidepoint(2000*cos(angle)+self.rect.centerx, 2000*sin(angle)+self.rect.centery):
                        enemy.takeDamage(self.damage)
        else:
            angle = atan((targety-selfy)/(targetx-selfx))
            pyg.draw.line(screen, "red", self.rect.center,
                          (-2000*cos(angle)+self.rect.centerx, -2000*sin(angle)+self.rect.centery), 5)
            for i in range(0, 2000, 2):
                for enemy in enemySprite:
                    if enemy.rect.collidepoint(-2000*cos(angle)+self.rect.centerx, -2000*sin(angle)+self.rect.centery):
                        enemy.takeDamage(self.damage)

    def basicTowerAttack(self, target):
        for enemy in enemySprite:
            if enemy != target:
                if ((enemy.rect.centerx - self.rect.centerx)**2 + (enemy.rect.centery - self.rect.centery)**2)**(1/2) <= self.range*100:
                    enemy.takeDamage(self.damage)
                    pyg.draw.line(screen, "red", self.rect.center,
                                  enemy.rect.center, 5)

    def explosiveTowerAttack(self, target):
        for enemy in enemySprite:
            if ((enemy.rect.centerx - target.rect.centerx)**2+(enemy.rect.centery-target.rect.centery)**2)*(1/2) <= self.blastRadius:
                enemy.takeDamage(self.damage)
                screen.blit(explosionAnimation, enemy.rect)

    def specialUpgrade(self):
        if self.ID == "basic":
            self.basicTowerSpecial = True
        if self.ID == "range":
            self.rangeTowerSpecial = True
        if self.ID == "fast":
            self.fastTowerSpecial = True
        if self.ID == "explosive":
            self.explosiveTowerSpecial = True
        if self.ID == "damage":
            self.damageTowerSpecial = True
            self.damageAttackCooldown = 0


class HoverTower(pyg.sprite.Sprite):
    def __init__(self, texture, position):
        super().__init__()
        if texture == "red":
            self.image = pyg.Surface((80, 80))
            self.image.fill(texture)
        else:
            self.image = texture
        self.rect = self.image.get_rect(center=position)

        self.add(hoverSprite)


def createTowers():
    basicTower = Tower(basicTowerTexture, [
                       basicUpgrade1, basicUpgrade2, basicUpgrade3, basicUpgrade4], 1, 1, 0.5, 0, "basic", 2)
    fastTower = Tower(fastTowerTexture, [
                      fastUpgrade1, fastUpgrade2, fastUpgrade3, fastUpgrade4], 1, 0.5, 1.5, 1, "fast", 6)
    rangeTower = Tower(rangeTowerTexture, [
                       rangeUpgrade1, rangeUpgrade2, rangeUpgrade3, rangeUpgrade4], 3, 1, 0.25, 2, "range", 4)
    damageTower = Tower(damageTowerTexture, [
                        damageUpgrade1, damageUpgrade2, damageUpgrade3, damageUpgrade4], 0.8, 3, 0.5, 3, "damage", 8)
    explosiveTower = Tower(explosiveTowerTexture, [explosiveUpgrade1, explosiveUpgrade2, explosiveUpgrade3, explosiveUpgrade4], 1, 0.7,
                           0.7, 4, "explosive", 12, True, 120)
