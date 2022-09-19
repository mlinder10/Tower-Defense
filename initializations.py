import pygame as pyg
pyg.init()

screen = pyg.display.set_mode((1280, 640))
clock = pyg.time.Clock()
pyg.display.set_caption("Tower Defense")
gameSpeed = 30

Map = 'none'
roadTexture = 'none'
obstacle1Texture = 'none'
obstacle2Texture = 'none'
obstacle3Texture = 'none'

normalColor = (100, 100, 100)
selectColor = (150, 150, 150)

backgroundSprite = pyg.sprite.Group()
visibleSprite = pyg.sprite.Group()
towerSprite = pyg.sprite.Group()
roadSprite = pyg.sprite.Group()
obstructionSprite = pyg.sprite.Group()
activeTowerSprite = pyg.sprite.Group()
hoverSprite = pyg.sprite.Group()
enemySprite = pyg.sprite.Group()
redEnemies = pyg.sprite.Group()
blueEnemies = pyg.sprite.Group()
whiteEnemies = pyg.sprite.Group()
blackEnemies = pyg.sprite.Group()
upgradeSprite = pyg.sprite.Group()

initial_direction = 'right'
selectedTower = "none"
rounds = [1]
deciding = True

numberOfTurns = 0
rawTurns = []
start = []
turns = []
end = []
turn_directions = []

redsKilled = 0
bluesKilled = 0
whitesKilled = 0
blacksKilled = 0
spawnCooldown = 0

playerHealth = []
for i in range(10):
    playerHealth.append(1)
loss = False

points = []
for i in range(4000):
    points.append(1)

upgrade = False
upgradingTower = 'none'

font = pyg.font.Font(None, 100)
font2 = pyg.font.Font(None, 50)
font3 = pyg.font.Font(None, 27)


iceTexture = pyg.image.load("Images/iceTexture.png").convert_alpha()
snowTexture = pyg.image.load("Images/snowTexture.png").convert_alpha()
christmasTreeTexture = pyg.image.load(
    "Images/christmasTreeTexture.png").convert_alpha()
presentTexture = pyg.image.load("Images/presentTexture.png").convert_alpha()

waterTexture = pyg.image.load("Images/waterTexture.png").convert_alpha()
sandTexture = pyg.image.load("Images/sandTexture.png").convert_alpha()
kelpTexture = pyg.image.load("Images/kelpTexture.png").convert_alpha()
coralTexture = pyg.image.load("Images/coralTexture.png").convert_alpha()
starfishTexture = pyg.image.load("Images/starfishTexture.png").convert_alpha()

dirtTexture = pyg.image.load("Images/dirtTexture.png").convert_alpha()
grassTexture = pyg.image.load("Images/background.png").convert_alpha()
rockTexture = pyg.image.load("Images/rockTexture.png").convert_alpha()
treeTexture = pyg.image.load("Images/treeTexture.png").convert_alpha()
branchTexture = pyg.image.load("Images/branchTexture.png").convert_alpha()


map1EnemyTexture = pyg.image.load(
    "Images/map1EnemyTexture.png").convert_alpha()
map2EnemyTexture = pyg.image.load(
    "Images/map2EnemyTexture.png").convert_alpha()
map3EnemyTexture = pyg.image.load(
    "Images/map3EnemyTexture.png").convert_alpha()

map1Img = pyg.image.load("Images/map1.png")
map2Img = pyg.image.load("Images/map2.png")
map3Img = pyg.image.load("Images/map3.png")


redEnemyTexture = pyg.image.load("Images/redEnemyTexture.png").convert_alpha()
blueEnemyTexture = pyg.image.load(
    "Images/blueEnemyTexture.png").convert_alpha()
whiteEnemyTexture = pyg.image.load(
    "Images/whiteEnemyTexture.png").convert_alpha()
blackEnemyTexture = pyg.image.load(
    "Images/blackEnemyTexture.png").convert_alpha()


# snowRedEnemyTexture = pyg.image.load("Images/snowRedEnemyTexture.png").convert_alpha()
# snowBlueEnemyTexture = pyg.image.load("Images/snowBlueEnemyTexture.png").convert_alpha()
# snowWhiteEnemyTexture = pyg.image.load("Images/snowWhiteEnemyTexture.png").convert_alpha()
# snowBlackEnemyTexture = pyg.image.load("Images/snowBlackEnemyTexture.png").convert_alpha()


# waterRedEnemyTexture = pyg.image.load("Images/waterRedEnemyTexture.png").convert_alpha()
# waterBlueEnemyTexture = pyg.image.load("Images/waterBlueEnemyTexture.png").convert_alpha()
# waterWhiteEnemyTexture = pyg.image.load("Images/waterWhiteEnemyTexture.png").convert_alpha()
# waterBlackEnemyTexture = pyg.image.load("Images/waterBlackEnemyTexture.png").convert_alpha()


explosionAnimation = pyg.image.load(
    "Images/explosionAnimation.png").convert_alpha()


basicTowerTexture = pyg.image.load(
    "Images/basicTower/basicTower.png").convert_alpha()
basicUpgrade1 = pyg.image.load(
    "Images/basicTower/basicUpgrade1.png").convert_alpha()
basicUpgrade2 = pyg.image.load(
    "Images/basicTower/basicUpgrade2.png").convert_alpha()
basicUpgrade3 = pyg.image.load(
    "Images/basicTower/basicUpgrade3.png").convert_alpha()
basicUpgrade4 = pyg.image.load(
    "Images/basicTower/basicUpgrade4.png").convert_alpha()

fastTowerTexture = pyg.image.load(
    "Images/fastTower/fastTower.png").convert_alpha()
fastUpgrade1 = pyg.image.load(
    "Images/fastTower/fastUpgrade1.png").convert_alpha()
fastUpgrade2 = pyg.image.load(
    "Images/fastTower/fastUpgrade2.png").convert_alpha()
fastUpgrade3 = pyg.image.load(
    "Images/fastTower/fastUpgrade3.png").convert_alpha()
fastUpgrade4 = pyg.image.load(
    "Images/fastTower/fastUpgrade4.png").convert_alpha()

rangeTowerTexture = pyg.image.load(
    "Images/rangeTower/rangeTower.png").convert_alpha()
rangeUpgrade1 = pyg.image.load(
    "Images/rangeTower/rangeUpgrade1.png").convert_alpha()
rangeUpgrade2 = pyg.image.load(
    "Images/rangeTower/rangeUpgrade2.png").convert_alpha()
rangeUpgrade3 = pyg.image.load(
    "Images/rangeTower/rangeUpgrade3.png").convert_alpha()
rangeUpgrade4 = pyg.image.load(
    "Images/rangeTower/rangeUpgrade4.png").convert_alpha()

damageTowerTexture = pyg.image.load(
    "Images/damageTower/damageTower.png").convert_alpha()
damageUpgrade1 = pyg.image.load(
    "Images/damageTower/damageUpgrade1.png").convert_alpha()
damageUpgrade2 = pyg.image.load(
    "Images/damageTower/damageUpgrade2.png").convert_alpha()
damageUpgrade3 = pyg.image.load(
    "Images/damageTower/damageUpgrade3.png").convert_alpha()
damageUpgrade4 = pyg.image.load(
    "Images/damageTower/damageUpgrade4.png").convert_alpha()

explosiveTowerTexture = pyg.image.load(
    "Images/explosiveTower/explosiveTower.png").convert_alpha()
explosiveUpgrade1 = pyg.image.load(
    "Images/explosiveTower/explosiveUpgrade1.png").convert_alpha()
explosiveUpgrade2 = pyg.image.load(
    "Images/explosiveTower/explosiveUpgrade2.png").convert_alpha()
explosiveUpgrade3 = pyg.image.load(
    "Images/explosiveTower/explosiveUpgrade3.png").convert_alpha()
explosiveUpgrade4 = pyg.image.load(
    "Images/explosiveTower/explosiveUpgrade4.png").convert_alpha()
