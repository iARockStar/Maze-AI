import numpy as np
import pygame
import colors
from params import *
from Environment import Board
from Agent import Agent

# initialize:
FPS = 60
pygame.init()
WIN = pygame.display.set_mode((width, height))
pygame.display.set_caption("Search Game")

# setting start and end point :
start = {'x': 6, 'y': 0}
end = {'x': 12, 'y': 0}

gameBoard = Board(start, end)
agent = Agent(gameBoard)


def main():
    run = True
    clock = pygame.time.Clock()
    WIN.fill(colors.black)
    counter = 0
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        gameBoard.draw_world(WIN)
        # pos = pygame.mouse.get_pos()
        # # gets the current mouse coords
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     for i in range(rows):
        #         for j in range(cols):
        #             rect = gameBoard.boardArray[i][j]
        #             if rect.is_inside_me(pos):
        #
        #                 if event.button == 1:
        #                     gameBoard.boardArray[i][j].block()
        #                 if event.button == 3:
        #                     gameBoard.boardArray[i][j].unblock()
        # array = []
        # for i in range(rows):
        #     array.append([])
        #     for j in range(cols):
        #         if gameBoard.boardArray[i][j].isBlocked:
        #             array[i].append(0)
        #         else:
        #             array[i].append(1)
        # array = np.array(array)
        # np.save("./Mazes/new_maze3.npy", array, allow_pickle=True)

        if counter < 1:
            #ask = input("Choose your desired function to solve the maze: 1.bfs 2.dfs 3.a_star\n ")
            #if ask == "1":
            agent.bfs(gameBoard)
            #elif ask == "2":
            #agent.dfs(gameBoard)
            #else:
            #agent.a_star(gameBoard)

        counter = counter + 1

    pygame.quit()

main()
