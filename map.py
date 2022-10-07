import pygame as pyg
from initializations import *

# 0 = free placement
# 1 = path start
# 2 = path
# 3 = path end
# 4 = obstructions
# 5 = turns


map1 = [
    [0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0],
    [0, 5, 2, 5, 0, 0, 0, 6, 0, 0, 5, 2, 3],
    [0, 2, 0, 2, 7, 0, 0, 0, 0, 0, 2, 0, 0],
    [1, 5, 0, 2, 0, 0, 5, 2, 5, 8, 2, 0, 0],
    [0, 0, 0, 2, 0, 0, 2, 0, 2, 0, 2, 0, 7],
    [0, 0, 0, 5, 2, 2, 5, 0, 2, 0, 2, 0, 0],
    [0, 6, 0, 0, 0, 7, 0, 0, 5, 2, 5, 6, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0]
]


map2 = [
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 8, 0, 2, 0, 7, 0, 0, 0, 0, 7, 0, 0],
    [0, 5, 2, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 2, 0, 0, 0, 5, 2, 2, 2, 2, 2, 5, 0],
    [0, 2, 0, 6, 0, 2, 0, 0, 0, 0, 0, 2, 0],
    [0, 2, 0, 0, 0, 2, 0, 0, 5, 2, 2, 5, 8],
    [0, 5, 2, 2, 2, 5, 6, 0, 2, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0]
]


map3 = [
    [0, 0, 5, 2, 2, 2, 2, 2, 5, 0, 0, 0, 0],
    [0, 6, 2, 0, 0, 0, 0, 0, 2, 7, 5, 2, 3],
    [0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0],
    [0, 0, 5, 2, 2, 2, 5, 0, 2, 0, 2, 0, 0],
    [0, 0, 0, 7, 6, 0, 2, 0, 2, 0, 2, 8, 0],
    [1, 2, 5, 0, 0, 0, 2, 0, 5, 2, 5, 0, 0],
    [0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 6, 0, 0],
    [8, 0, 5, 2, 2, 2, 5, 0, 0, 0, 0, 0, 0]
]


# blankMap = [
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# ]


def findStartTurnsAndEnd(Map):
    global start, end, turns, turn_directions, rawTurns, numberOfTurns
    numberOfTurns = 0
    rawTurns.clear()
    start.clear()
    turns.clear()
    end.clear
    turn_directions.clear()
    for count1, row in enumerate(Map):
        for count2, spot in enumerate(row):
            if spot == 1:
                if count1 == 0:
                    start.append([count2*80+40, -30])
                    turn_directions.append("down")
                    rawTurns.append([count2, count1])
                else:
                    start.append([-30, count1*80+40])
                    turn_directions.append("right")
                    rawTurns.append([count2, count1])
            elif spot == 5:
                numberOfTurns += 1
                turns.append([count2*80+40, count1*80+40])
            elif spot == 3:
                if count1 == 0:
                    end.append([count2*80+40, -35])
                else:
                    end.append([-35, count1*80+40])
    findTurnDirections(Map)


def lookAround(x, y, direction, Map):
    global rawTurns
    rawTurns.append([y, x])
    if direction == "right" or direction == "left":
        try:
            if Map[x + 1][y] == 2:
                turn_directions.append("down")
            else:
                turn_directions.append("up")
        except:
            turn_directions.append("up")
    elif direction == "down" or direction == "up":
        try:
            if Map[x][y + 1] == 2:
                turn_directions.append("right")
            else:
                turn_directions.append("left")
        except:
            turn_directions.append("left")


def findTurnDirections(Map):
    for i in range(numberOfTurns):
        if turn_directions[i] == 'right':
            spot = 0
            x = 0
            while spot != 5:
                x += 1
                spot = Map[rawTurns[i][1]][rawTurns[i][0]+x]
            lookAround(rawTurns[i][1], rawTurns[i]
                       [0]+x, turn_directions[i], Map)

        elif turn_directions[i] == 'left':
            spot = 0
            x = 0
            while spot != 5:
                x -= 1
                spot = Map[rawTurns[i][1]][rawTurns[i][0]+x]
            lookAround(rawTurns[i][1], rawTurns[i]
                       [0]+x, turn_directions[i], Map)

        elif turn_directions[i] == 'down':
            spot = 0
            x = 0
            while spot != 5:
                x += 1
                spot = Map[rawTurns[i][1]+x][rawTurns[i][0]]
            lookAround(rawTurns[i][1]+x, rawTurns[i]
                       [0], turn_directions[i], Map)

        elif turn_directions[i] == 'up':
            spot = 0
            x = 0
            while spot != 5:
                x -= 1
                spot = Map[rawTurns[i][1]+x][rawTurns[i][0]]
            lookAround(rawTurns[i][1]+x, rawTurns[i]
                       [0], turn_directions[i], Map)
