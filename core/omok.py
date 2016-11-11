import config

BOARD_SIZE = config.BOARD_SIZE
EYE_OFFSET = 3
BLACK = 1
WHITE = 2


class Omok:

    def __init__(self):
        self.map = []
        self.players = []
        self.screen = None
        self.turn = BLACK

        for y in range(BOARD_SIZE):
            self.map.append([0] * BOARD_SIZE)
            for x in range(BOARD_SIZE):
                self.map[y][x] = 0


    def newgame(self, players, screen=None):

        self.players = players
        self.turn = BLACK
        self.screen = screen

        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                self.map[y][x] = 0
        

    def wincheck(self, nX, nY, Type):
        x, y = nX, nY
        count = 0
        while (x > 0) and (self.map[y][x-1] == Type):
            x-=1
        while (x < BOARD_SIZE) and (self.map[y][x] == Type):
            count+=1
            x+=1
        if (count == 5):
            return True

        x, y = nX, nY
        count = 0
        while (y > 0) and (self.map[y-1][x] == Type):
            y-=1
        while (y < BOARD_SIZE) and (self.map[y][x] == Type):
            count+=1
            y+=1
        if (count == 5):
            return True
        
        x = nX
        y = nY
        count = 0
        
        while (x > 0) and (y > 0) and (self.map[y-1][x-1] == Type):
            x-=1
            y-=1
        while (x < BOARD_SIZE) and (y < BOARD_SIZE) and (self.map[y][x] == Type):
            count+=1
            x+=1
            y+=1
        if (count == 5):
            return True

        x = nX
        y = nY
        count = 0
        while (x < BOARD_SIZE - 1) and (y > 0) and (self.map[y-1][x+1] == Type):
            x+=1
            y-=1
        while (x >= 0) and (y < BOARD_SIZE) and (self.map[y][x] == Type):
            count+=1
            x-=1
            y+=1
        if (count == 5):
            return True

        return False


    def isDrawGame(self):
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                if self.map[y][x] == 0:
                    return False
        return True


    def draw(self, screen):
        if screen is None:
            return

        screen.draw(self.map)
        

    def get_input(self):
        if self.turn == BLACK:
            input = self.players[0](self.map, self.turn)
        else:
            input = self.players[1](self.map, self.turn)
        x = input[0]
        y = input[1]
        return x, y
            

    def step(self, x, y):
        self.map[y][x] = self.turn
        self.draw(self.screen)
                    
        if self.wincheck(x, y, self.turn):
            return self.turn
        
        if self.isDrawGame():
            return 0
        
        self.turn = 3 - self.turn

        # -1 mean is progress
        return -1


    def main(self):
        while True:
            x, y = self.get_input()
            ret = self.step(x, y)
            if ret != -1:
                return ret
   

if __name__ == "__main__":
    import omok_vanilla_ai
    import omok_screen

    screen = omok_screen.OmokScreen()
    game = Omok()

    for i in range(100):
        game.newgame([screen.get_player_input, omok_vanilla_ai.AI], screen)
        game.draw(screen)
        win = game.main()
        if win == BLACK:
            print("BLACK WIN")
        elif win == WHITE:
            print("WHITE WIN")
        else:
            print("DRAW")
