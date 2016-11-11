import pygame
from pygame.locals import *

import config

BOARD_SIZE = config.BOARD_SIZE
EYE_OFFSET = 3
BLACK = 1
WHITE = 2


class OmokScreen:

    def __init__(self):

        self.width = BOARD_SIZE * 30 + 30
        self.height = BOARD_SIZE * 30 + 30
        self.crossPoint = []
        for y in range(BOARD_SIZE):
            self.crossPoint.append([0] * BOARD_SIZE)
            for x in range(BOARD_SIZE):
                self.crossPoint[y][x] = [(x*30)+30, (y*30)+30]

        # screen init
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Omok')

        # create gackground
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        background.fill((250,250,250))


    def draw(self, map):
        if self.screen is None:
            return

        self.screen.fill((255, 204, 33))
        Color=(0, 0, 0)
        for i in range(BOARD_SIZE):
            pygame.draw.line(self.screen,
                                Color,
                                (self.crossPoint[i][0][0], self.crossPoint[i][0][1]),
                                (self.crossPoint[i][BOARD_SIZE -1 ][0], self.crossPoint[i][BOARD_SIZE - 1][1]))
            pygame.draw.line(self.screen,
                                Color,
                                (self.crossPoint[0][i][0], self.crossPoint[0][i][1]),
                                (self.crossPoint[BOARD_SIZE - 1][i][0], self.crossPoint[BOARD_SIZE - 1][i][1]))
            
        pygame.draw.circle(self.screen, Color, self.crossPoint[EYE_OFFSET-1][EYE_OFFSET-1], 3)
        pygame.draw.circle(self.screen, Color, self.crossPoint[EYE_OFFSET-1][BOARD_SIZE-EYE_OFFSET], 3)
        pygame.draw.circle(self.screen, Color, self.crossPoint[BOARD_SIZE-EYE_OFFSET][EYE_OFFSET-1], 3)
        pygame.draw.circle(self.screen, Color, self.crossPoint[BOARD_SIZE-EYE_OFFSET][BOARD_SIZE-EYE_OFFSET], 3)
        pygame.draw.circle(self.screen, Color, self.crossPoint[int(BOARD_SIZE/2)][int(BOARD_SIZE/2)], 3)

        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                if (map[y][x] == BLACK):
                    pygame.draw.circle(self.screen, (0, 0, 0), self.crossPoint[y][x], 14)
                elif (map[y][x] == WHITE):
                    pygame.draw.circle(self.screen, (255, 255, 255), self.crossPoint[y][x], 14)

        pygame.display.flip()

        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done=True # Flag that we are done so we exit this loop



    def get_player_input(self, board, turn):
        while True:
            for event in pygame.event.get():
                if (pygame.QUIT == event.type):
                    return
                
                if (pygame.KEYDOWN == event.type):   
                    if (pygame.K_ESCAPE == event.key):   
                        exit()

                if (pygame.MOUSEBUTTONDOWN == event.type):
                    button = pygame.mouse.get_pressed()
                    buttonType = 0
                    pos = pygame.mouse.get_pos()
                    x = int((pos[0] - 15) / 30)
                    y = int((pos[1] - 15) / 30)

                    if button[0] and x >= 0 and x < BOARD_SIZE and y >= 0 and y < BOARD_SIZE: 
                        if board[y][x] == 0:
                            return [x, y]
