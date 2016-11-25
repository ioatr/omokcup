# -*- encoding: utf8 -*-

import core.config
import omok_client
import random

BOARD_SIZE = core.config.BOARD_SIZE
EYE_OFFSET = 3

def IsValidIndex(index):
    return 0 <= index and index < BOARD_SIZE

def GetStone(board, px, py):
    if IsValidIndex(px) and IsValidIndex(py):
        return board[py][px]
    else:
        return -1

def CountOneSide(board, id, px, py, dx, dy):
    cx = px
    cy = py

    contiCnt = 0
    nonContiCnt = 0
    maxLength = 0

    isConti = True
    closed = False
    stop = False

    prevStone = -1

    while True:
        cx += dx
        cy += dy
        stone = GetStone(board, cx, cy)
        if stone == id:
            if not stop:
                if isConti:
                    contiCnt += 1
                nonContiCnt += 1
            maxLength += 1
        elif stone == 0:
            if not isConti:
                stop = True
            isConti = False
            maxLength += 1
        elif stone == -1:
            if prevStone == id:
                closed = True
            break
        else:
            if prevStone == id:
                closed = True
            break
        prevStone = stone

    return contiCnt, nonContiCnt, closed, maxLength

def CountTwoSide(board, id, px, py, dx, dy):
    (contiCnt1, nonContiCnt1, closed1, maxLength1) = CountOneSide(board, id, px, py, dx, dy)
    (contiCnt2, nonContiCnt2, closed2, maxLength2) = CountOneSide(board, id, px, py, -dx, -dy)

    contiCnt = 1 + contiCnt1 + contiCnt2
    n = nonContiCnt1 + contiCnt2
    m = contiCnt1 + nonContiCnt2
    nonContiCnt = 1 + max(n, m)

    maxLength = maxLength1 + maxLength2 + 1
    if maxLength < 5:
        closed1 = True
        closed2 = True

    closeCount = 0
    if closed1:
        closeCount += 1
    if closed2:
        closeCount += 1

    if closed1 and closed2 and nonContiCnt + 1 < 5:
        contiCnt = 0
        nonContiCnt = 0

    return (contiCnt, nonContiCnt, closeCount)

def GetBoardInfo(board, id):
    boardInfo = {}
    directions = ((1, 1), (1, 0), (0, 1), (1, -1))
    for y in xrange(BOARD_SIZE):
        for x in xrange(BOARD_SIZE):
            if board[y][x] == 0:
                info = []
                for direction in directions:
                    info.append(CountTwoSide(board, id, x, y, direction[0], direction[1]))
                boardInfo[(x, y)] = info

    return boardInfo

POINT_GRADE1 = 10000000000
POINT_GRADE2 = 1000000000
POINT_GRADE3 = 100000000
POINT_GRADE4 = 10000000
POINT_GRADE5 = 1000000
POINT_GRADE6 = 100000
POINT_GRADE7 = 10000
POINT_GRADE8 = 1000
POINT_GRADE9 = 100
POINT_GRADE10 = 10
POINT_GRADE11 = 1
POINT_GRADE12 = 0.9
POINT_GRADE13 = 0.1
POINT_GRADE14 = 0.01
POINT_GRADE15 = 0.005
POINT_GRADE16 = 0.003
POINT_GRADE17 = 0.001

def CalcPoints(myBoardInfo, yourBoardInfo):
    pointInfo = {}
    highPoint = 0

    for key in myBoardInfo.keys():
        value = myBoardInfo[key]
        pointInfo[key] = 0
        numConut = {3:0, 4:0}
        for (contiCnt, nonContiCnt, closeCount) in value:
            if contiCnt == nonContiCnt:
                if contiCnt == 5:
                    pointInfo[key] += POINT_GRADE1
                elif contiCnt == 4:
                    if closeCount == 0:
                        pointInfo[key] += POINT_GRADE3
                    elif closeCount == 1:
                        pointInfo[key] += POINT_GRADE12
                        numConut[4] += 1
                elif contiCnt == 3:
                    if closeCount == 0:
                        pointInfo[key] += POINT_GRADE13
                        numConut[3] += 1
                    elif closeCount == 1:
                        pointInfo[key] += POINT_GRADE15
                elif contiCnt == 2:
                    if closeCount == 0:
                        pointInfo[key] += POINT_GRADE14
                    elif closeCount == 1:
                        pointInfo[key] += POINT_GRADE16
            else:
                if contiCnt == 5:
                    pointInfo[key] += POINT_GRADE1
                elif nonContiCnt == 4:
                    if closeCount == 0:
                        pointInfo[key] += POINT_GRADE11
                        numConut[4] += 1
                    elif closeCount == 1:
                        pointInfo[key] += POINT_GRADE12
                        numConut[4] += 1
                elif nonContiCnt == 3:
                    if closeCount == 0:
                        pointInfo[key] += POINT_GRADE13
                        numConut[3] += 1
                    elif closeCount == 1:
                        pointInfo[key] += POINT_GRADE15
                elif nonContiCnt == 2:
                    if closeCount == 0:
                        pointInfo[key] += POINT_GRADE14
                    elif closeCount == 1:
                        pointInfo[key] += POINT_GRADE16

        if (numConut[4] > 1):
            pointInfo[key] += POINT_GRADE5
        elif (numConut[4] > 0 and numConut[3] > 0):
            pointInfo[key] += POINT_GRADE7
        elif (numConut[3] > 1):
            pointInfo[key] += POINT_GRADE9

    for key in yourBoardInfo.keys():
        value = yourBoardInfo[key]
        numConut = {3:0, 4:0}
        for (contiCnt, nonContiCnt, closeCount) in value:
            if contiCnt == nonContiCnt:
                if contiCnt == 5:
                    pointInfo[key] += POINT_GRADE2
                elif contiCnt == 4:
                    if closeCount == 0:
                        pointInfo[key] += POINT_GRADE4
                    elif closeCount == 1:
                        pointInfo[key] += POINT_GRADE13
                        numConut[4] += 1
                elif contiCnt == 3:
                    if closeCount == 0:
                        pointInfo[key] += POINT_GRADE14
                        numConut[3] += 1
                    elif closeCount == 1:
                        pointInfo[key] += POINT_GRADE16
                elif contiCnt == 2:
                    if closeCount == 0:
                        pointInfo[key] += POINT_GRADE15
                    elif closeCount == 1:
                        pointInfo[key] += POINT_GRADE17
            else:
                if contiCnt == 5:
                    pointInfo[key] += POINT_GRADE2
                elif nonContiCnt == 4:
                    if closeCount == 0:
                        pointInfo[key] += POINT_GRADE12
                        numConut[4] += 1
                    elif closeCount == 1:
                        pointInfo[key] += POINT_GRADE13
                        numConut[4] += 1
                elif nonContiCnt == 3:
                    if closeCount == 0:
                        pointInfo[key] += POINT_GRADE14
                        numConut[3] += 1
                    elif closeCount == 1:
                        pointInfo[key] += POINT_GRADE16
                elif nonContiCnt == 2:
                    if closeCount == 0:
                        pointInfo[key] += POINT_GRADE15
                    elif closeCount == 1:
                        pointInfo[key] += POINT_GRADE17

        if (numConut[4] > 1):
            pointInfo[key] += POINT_GRADE6
        elif (numConut[4] > 0 and numConut[3] > 0):
            pointInfo[key] += POINT_GRADE8
        elif (numConut[3] > 1):
            pointInfo[key] += POINT_GRADE10

        if pointInfo[key] > highPoint:
            highPoint = pointInfo[key]

    return pointInfo, highPoint

def GetCandidate(pointInfo, matchPoint):
    candidate = []
    for key in pointInfo.keys():
        point = pointInfo[key]
        if point == matchPoint:
            candidate.append(key)

    return candidate

def choose(my_id, px, py, board):
    '''
    my_id: 나의 식별자 (흑:1, 백:2)
    px, py: 방금전 상대편이 둔 수 (주의! 맨 처음 수는 -1, -1로 주어진다)
    board: 현재 상태 수
    '''
    if px == -1 and py == -1:
        return int(BOARD_SIZE / 2), int(BOARD_SIZE / 2)

    yourId = 1
    if my_id == 1:
        yourId = 2

    myBoardInfo = GetBoardInfo(board, my_id)
    yourBoardInfo = GetBoardInfo(board, yourId)
    
    (pointInfo, highPoint) = CalcPoints(myBoardInfo, yourBoardInfo)
    candidate = GetCandidate(pointInfo, highPoint)
    
    return random.choice(candidate)
    
if __name__ == '__main__':

    game = omok_client.OmokClient(BOARD_SIZE)
    game.ready()
 
    while True:
        # sync
        status, x, y = game.get()
        if status == -1:
            break

        # 자신의 수 선택
        '''
        board = []
        for x in xrange(BOARD_SIZE):
            board.append([])
            for y in xrange(BOARD_SIZE):
                board[x].append(0)
        board[0][0] = 2
        '''
        x, y = choose(game.my_id, x, y, game.board)
        #x, y = choose(1, 0, 0, board)

        # sync
        game.put(x, y)