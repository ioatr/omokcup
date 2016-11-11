import math

MAX_HAZARD = math.exp(5)

def GetFavorableValue(map, nX, nY, Type):
     
    x, y, count, hazard = nX, nY, 0, 0 
    Map = map[:]
    BOARD_SIZE = len(Map)

    for i in range(BOARD_SIZE):
        Map[i] = map[i][:]
        
    Map[nY][nX] = Type

    while (x > 0) and (Map[y][x-1] == Type):
        x-=1
    while (x < BOARD_SIZE) and (Map[y][x] == Type):
        count+=1
        x+=1
    if (count > 5):
        count = 2
    hazard += math.exp(count) / MAX_HAZARD
    
    x, y, count = nX, nY, 0  

    while (y > 0) and (Map[y-1][x] == Type):
        y-=1
    while (y < BOARD_SIZE) and (Map[y][x] == Type):
        count+=1
        y+=1
    if (count > 5):
        count = 2
    hazard += math.exp(count) / MAX_HAZARD
    
    x, y, count = nX, nY, 0
    while (x > 0) and (y > 0) and (Map[y-1][x-1] == Type):
        x-=1
        y-=1
    while (x < BOARD_SIZE) and (y < BOARD_SIZE) and (Map[y][x] == Type):
        count+=1
        x+=1
        y+=1
    if (count > 5):
        count = 2
    hazard += math.exp(count) / MAX_HAZARD
    
    x, y, count = nX, nY, 0
    while (x < BOARD_SIZE-1) and (y > 0) and (Map[y-1][x+1] == Type):
        x+=1
        y-=1
    while (x >= 0) and (y < BOARD_SIZE) and (Map[y][x] == Type):
        count+=1
        x-=1
        y+=1
    if (count > 5):
        count = 2
    hazard += math.exp(count) / MAX_HAZARD
    
    return hazard

def GetFavorablePos(map, Type):
    FavorableList = []
    BOARD_SIZE = len(map)
    
    for y in range(BOARD_SIZE):
        FavorableList.append([0] * BOARD_SIZE)
        for x in range(BOARD_SIZE):
            if map[y][x] == 0:
                FavorableList[y][x] = GetFavorableValue(map, x, y, Type)
            else:
                FavorableList[y][x] = 0
    
    max = 0
    FavorX, FavorY = -1, -1
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if (FavorableList[y][x] > max):
                max = FavorableList[y][x]
                FavorX = x
                FavorY = y
    return [FavorX, FavorY, max]


def AI(board, turn):
    Cpu = GetFavorablePos(board, turn)
    User = GetFavorablePos(board, 3 - turn)

    if (Cpu[2] >= User[2]):
        return Cpu
    else:
        return User