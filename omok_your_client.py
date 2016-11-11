# -*- encoding: utf8 -*-

import core.config
import omok_client


BOARD_SIZE = core.config.BOARD_SIZE
EYE_OFFSET = 3


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