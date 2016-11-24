# -*- encoding: utf8 -*-

import core.config
import omok_client


BOARD_SIZE = core.config.BOARD_SIZE
EYE_OFFSET = 3
MY_ID = 0
DEPTH = 16
RATIO = 0.4


class Node(object):
    def __init__(self):
        pass
    def getchild(self):
        pass
    def value(self):
        pass


class OmokNode(Node):
    def __init__(self, board, my_id):
        self.board = board
        self.my_id = my_id

    def getmark0(self):
        mark = [x[:] for x in [[0] * BOARD_SIZE] * BOARD_SIZE]

        def foo(mark, x, y, dx, dy):
            begin = False
            count = 0

            while x >= 0 and x < BOARD_SIZE and y >= 0 and y < BOARD_SIZE:
                if begin == False and self.board[y][x] != 0:
                    begin = True
                    xs, ys = x, y
                    c = self.board[y][x]
                    count = 0

                if begin == True and self.board[y][x] != c:
                    begin = False
                    xe, ye = x, y

                    # record
                    if xs-dx >= 0 and xs-dx < BOARD_SIZE and ys-dy >= 0 and ys-dy < BOARD_SIZE: mark[ys-dy][xs-dx] += count * count
                    if x >= 0 and x < BOARD_SIZE and y >= 0 and y < BOARD_SIZE: mark[y][x] += count * count
                else:
                    count += 1
                    x += dx
                    y += dy
            
            if begin:
                # record
                if xs-dx >= 0 and xs-dx < BOARD_SIZE and ys-dy >= 0 and ys-dy < BOARD_SIZE: mark[ys-dy][xs-dx] += count * count
                if x >= 0 and x < BOARD_SIZE and y >= 0 and y < BOARD_SIZE: mark[y][x] += count * count
        

        for i in xrange(BOARD_SIZE):
            foo(mark, 0, i, 1, 0)
            foo(mark, i, 0, 0, 1)

            # todo: check
            foo(mark, 0, i, 1, 1)
            foo(mark, i+1, 0, 1, 1)

            foo(mark, i, 0, -1, 1)
            foo(mark, BOARD_SIZE-1, i, -1, 1)
        
        return mark

    def getmark2(self):
        mark = [x[:] for x in [[0] * BOARD_SIZE] * BOARD_SIZE]

        def ___(x, y, dx, dy, c):
            x += dx
            y += dy
            count = 0
            while x >= 0 and x < BOARD_SIZE and y >= 0 and y < BOARD_SIZE:
                if self.board[y][x] == c:
                    count += 1
                    x += dx
                    y += dy
                else:
                    break
            return count
            
        for y in xrange(BOARD_SIZE):
            for x in xrange(BOARD_SIZE):
                if self.board[y][x] == 0:
                    count = 0
                    count += ___(x, y, 0, 1, 1)
                    count += ___(x, y, 0, -1, 1)
                    count += ___(x, y, 1, 0, 1)
                    count += ___(x, y, -1, 0, 1)
                    count += ___(x, y, 1, 1, 1)
                    count += ___(x, y, -1, -1, 1)
                    count += ___(x, y, 1, -1, 1)
                    count += ___(x, y, -1, 1, 1)
                    mark[y][x] += count * count

                    count = 0
                    count += ___(x, y, 0, 1, 2)
                    count += ___(x, y, 0, -1, 2)
                    count += ___(x, y, 1, 0, 2)
                    count += ___(x, y, -1, 0, 2)
                    count += ___(x, y, 1, 1, 2)
                    count += ___(x, y, -1, -1, 2)
                    count += ___(x, y, 1, -1, 2)
                    count += ___(x, y, -1, 1, 2)
                    mark[y][x] += count * count

        return mark




    def getchild(self, depth=0):
        mark = self.getmark2()

        tmp = []
        for y in xrange(BOARD_SIZE):
            for x in xrange(BOARD_SIZE):
                if mark[y][x] > 0 and self.board[y][x] == 0:
                    tmp.append((x, y))

        # 둘 곳이 없으면 중앙 부터 시작
        if len(tmp) == 0:
            tmp.append((BOARD_SIZE/2, BOARD_SIZE/2))

        # 내부 평가가 높은 수로 정렬
        tmp = sorted(tmp, key=lambda _: mark[_[1]][_[0]], reverse=True)

        # 깊이가 깊어질수록 중요한 수만 평가
        length = len(tmp)
        length = max(1, int(length * RATIO ** (DEPTH - depth)))
        return tmp[0:length]
    

    def _value(self, oid):
        tmp = 0
        def ___(x, y, dx, dy):
            tmp = 0
            count = 0
            while x >= 0 and x < BOARD_SIZE and y >= 0 and y < BOARD_SIZE:
                if self.board[y][x] == oid:
                    count += 1
                else:
                    count = 0
                tmp += count * count
                x += dx
                y += dy
            return tmp
                
        for i in xrange(BOARD_SIZE):
            tmp += ___(0, i, 1, 0)
            tmp += ___(i, 0, 0, 1)

            tmp += ___(0, i, 1, 1)
            tmp += ___(i+1, 0, 1, 1)

            tmp += ___(i, 0, -1, 1)
            tmp += ___(BOARD_SIZE-1, i, -1, 1)

        return tmp        


    def value(self, my_id):
        return self._value(my_id) - self._value(EYE_OFFSET - my_id)


    def set_a(self, child):
        self.board[child[1]][child[0]] = self.my_id
    def set_b(self, child):
        self.board[child[1]][child[0]] = EYE_OFFSET - self.my_id
    def unset(self, child):
        self.board[child[1]][child[0]] = 0


    def wincheck(self, nX, nY, Type):
        x, y = nX, nY
        count = 0
        while (x > 0) and (self.board[y][x-1] == Type):
            x-=1
        while (x < BOARD_SIZE) and (self.board[y][x] == Type):
            count+=1
            x+=1
        if (count == 5):
            return True

        x, y = nX, nY
        count = 0
        while (y > 0) and (self.board[y-1][x] == Type):
            y-=1
        while (y < BOARD_SIZE) and (self.board[y][x] == Type):
            count+=1
            y+=1
        if (count == 5):
            return True
        
        x = nX
        y = nY
        count = 0
        
        while (x > 0) and (y > 0) and (self.board[y-1][x-1] == Type):
            x-=1
            y-=1
        while (x < BOARD_SIZE) and (y < BOARD_SIZE) and (self.board[y][x] == Type):
            count+=1
            x+=1
            y+=1
        if (count == 5):
            return True

        x = nX
        y = nY
        count = 0
        while (x < BOARD_SIZE - 1) and (y > 0) and (self.board[y-1][x+1] == Type):
            x+=1
            y-=1
        while (x >= 0) and (y < BOARD_SIZE) and (self.board[y][x] == Type):
            count+=1
            x-=1
            y+=1
        if (count == 5):
            return True

        return False


def minimax(node, child, depth, maximizingPlayer):
    if depth == 0 or not node.getchild():
        return (node.value(MY_ID), child)
    
    if maximizingPlayer:
        v = (-1000000, None)
        for child in node.getchild(depth):
            node.set_a(child)

            vv = minimax(node, child, depth-1, False)
            if vv[0] > v[0]:
                v = (vv[0], child)
            
            node.unset(child)
        return v
    else:
        v = (100000, None)
        for child in node.getchild(depth):
            node.set_b(child)

            vv = minimax(node, child, depth-1, True)
            if vv[0] < v[0]:
                v = (vv[0], child)

            node.unset(child)
        return v



def alphabeta(node, child, depth, a, b, maximizingPlayer):

    if child and node.wincheck(child[0], child[1], MY_ID):
        return (99999, child)

    if child and node.wincheck(child[0], child[1], EYE_OFFSET - MY_ID):
        return (-99999, child)

    if depth == 0 or not node.getchild():
        return (node.value(MY_ID), child)

    if maximizingPlayer:
        for child in node.getchild(depth):
            node.set_a(child)
            
            aa = alphabeta(node, child, depth-1, a, b, not maximizingPlayer)
            if aa[0] > a[0]:
                a = (aa[0], child)

            node.unset(child)
            if b[0] <= a[0]:
                break
        return a
    else:
        for child in node.getchild(depth):
            node.set_b(child)
            
            bb = alphabeta(node, child, depth-1, a, b, not maximizingPlayer)
            if bb[0] < b[0]:
                b = (bb[0], child)
            
            node.unset(child)
            if b[0] <= a[0]:
                break
        return b


def choose(my_id, px, py, board):
    '''
    my_id: 나의 식별자 (흑:1, 백:2)
    px, py: 방금전 상대편이 둔 수 (주의! 맨 처음 수는 -1, -1로 주어진다)
    board: 현재 상태 수
    '''

    #
    # 이 부분을 구현해주세요. 아래는 샘플 코드입니다.
    #
    MY_ID = my_id
    node = OmokNode(board, my_id)
    value, child = alphabeta(node, None, DEPTH, (-1000000, None), (1000000, None), True)
    # value, child = minimax(node, None, DEPTH, True)
    return child[0], child[1]


if __name__ == '__main__':

    game = omok_client.OmokClient(BOARD_SIZE)
    game.ready()
 
    while True:
        # sync
        status, x, y = game.get()
        if status == -1:
            break

        # 자신의 수 선택
        x, y = choose(game.my_id, x, y, game.board)

        # sync
        game.put(x, y)