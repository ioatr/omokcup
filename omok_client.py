# -*- encoding: utf8 -*-

import sys

import core.config

BOARD_SIZE = core.config.BOARD_SIZE
EYE_OFFSET = 3


class OmokClient:

    def __init__(self, board_size):
        # 초기화
        self.board_size = board_size
        self.board = [x[:] for x in [[0] * BOARD_SIZE] * BOARD_SIZE]
        return


    def _get(self):
        # 호스트와 통신
        return sys.stdin.readline().rstrip()


    def _put(self, text):
        # 호스트와 통신
        print text
        sys.stdout.flush()


    def get(self):
        # 호스트에게 상태와 상대의 좌표를 가져온다.
        tmp = self._get()
        if tmp == 'quit':
            return -1

        x, y = map(int, tmp.split())
        if x != -1 or y != -1:
            self.board[y][x] = EYE_OFFSET - self.my_id

        return 1, x, y
        

    def put(self, x, y):
        self.board[y][x] = self.my_id
        # 나의 수(좌표)를 호스트에게 알려준다.
        self._put('{} {}'.format(x, y))


    def ready(self):
        # 호스트로부터 아이디를 가져옵니다.
        self.my_id = int(self._get())



def choose(my_id, px, py, board):
    '''
    my_id: 나의 식별자 (흑:1, 백:2)
    px, py: 방금전 상대편이 둔 수 (주의! 맨 처음 수는 -1, -1로 주어진다)
    board: 현재 상태 수
    '''

    #
    # 이 부분을 구현해주세요. 아래는 샘플 코드입니다.
    #
    for y in xrange(BOARD_SIZE):
        for x in xrange(BOARD_SIZE):
            if board[y][x] == 0:
                return x, y    


if __name__ == '__main__':

    game = OmokClient(BOARD_SIZE)
    game.ready()
 
    while True:
        # sync
        status, x, y = game.get()
        if status == -1:
            break

        # 오목을 구현하세요
        x, y = choose(game.my_id, x, y, game.board)

        # sync
        game.put(x, y)

# TODO: add screen
