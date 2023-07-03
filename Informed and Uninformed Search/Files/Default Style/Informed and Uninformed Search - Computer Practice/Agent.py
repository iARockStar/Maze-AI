from params import *
from tile import Tile
import colors
import math


class Agent:
    def __init__(self, board):

        self.position = board.get_agent_pos()
        self.current_state = board.get_current_state()

    def get_position(self):
        return self.position

    def set_position(self, position, board):
        self.position = position
        board.set_agent_pos(position)
        board.update_board(self.current_state)

    def percept(self, board):
        self.current_state = board.get_current_state()

    def move(self, board, new_pos):
        current_pos = self.get_position()
        x, y = current_pos[0], current_pos[1]
        board.colorize(x, y, colors.red)

        self.set_position(new_pos, board)

    @staticmethod
    def get_actions(board, s):
        position_x = s.get_coordinates()[0]
        position_y = s.get_coordinates()[1]
        right_tile = Tile(13, 13)
        left_tile = Tile(13, 13)
        up_tile = Tile(13, 13)
        down_tile = Tile(13, 13)
        if position_x + 1 < cols:
            right_tile = board.boardArray[position_x + 1][position_y]
        if position_x > 0:
            left_tile = board.boardArray[position_x - 1][position_y]
        if position_y > 0:
            up_tile = board.boardArray[position_x][position_y - 1]
        if position_y + 1 < rows:
            down_tile = board.boardArray[position_x][position_y + 1]
        return down_tile, left_tile, right_tile, up_tile

    def bfs(self, board):
        self.percept(board)
        source = self.find_source(board)
        queue = []
        source.is_visited = True
        queue.append(source)
        expand_limit = 0
        while queue:

            s = queue.pop(0)

            down_tile, left_tile, right_tile, up_tile = self.get_actions(board, s)

            if s.isGoal:
                s.pathColor()
                self.find_source(board).color = colors.startColor
                self.find_dest(board).color = colors.endColor
                return
            if expand_limit < 34:
                self.move(board, (s.get_coordinates()[0], s.get_coordinates()[1]))
            self.check_neighbor(board, expand_limit, queue, right_tile, s)
            self.check_neighbor(board, expand_limit, queue, left_tile, s)
            self.check_neighbor(board, expand_limit, queue, down_tile, s)
            self.check_neighbor(board, expand_limit, queue, up_tile, s)
            expand_limit = expand_limit + 1

    def check_neighbor(self, board, expand_limit, queue, right_tile, s):
        if right_tile.get_coordinates()[0] < 13 and not right_tile.is_visited \
                and not right_tile.is_blocked():
            queue.append(right_tile)
            right_tile.is_visited = True
            right_tile.parent = s


    def dfs(self, board):
        self.percept(board)

        source = self.find_source(board)

        self.dfs_recursive(0, source, board)

    def dfs_recursive(self, expand_limit, new_tile, board):
        new_tile.is_visited = True
        expand_limit += 1
        if expand_limit < 25:
            self.move(board,
                      (new_tile.get_coordinates()[0], new_tile.get_coordinates()[1]))
        down_tile, left_tile, right_tile, up_tile = self.get_actions(board, new_tile)

        if new_tile.isGoal:
            new_tile.pathColor()
            self.find_source(board).color = colors.startColor
            self.find_dest(board).color = colors.endColor
            return

        self.call_dfs(board, new_tile, right_tile, expand_limit)
        self.call_dfs(board, new_tile, left_tile, expand_limit)
        self.call_dfs(board, new_tile, down_tile, expand_limit)
        self.call_dfs(board, new_tile, up_tile, expand_limit)

    def call_dfs(self, board, new_tile, right_tile, expand_limit):
        if right_tile.get_coordinates()[0] < 13 and not right_tile.is_visited \
                and not right_tile.is_blocked():
            right_tile.parent = new_tile
            self.dfs_recursive(expand_limit, right_tile, board)

    def a_star(self, board):
        self.percept(board)
        open_list = []
        closed_list = []
        source = self.find_source(board)

        dest = self.find_dest(board)
        source.dist = 0
        closed_list.append(source)

        down_tile, left_tile, right_tile, up_tile = self.get_actions(board, source)

        self.check_neighbor_aStar(open_list, right_tile, source)
        self.check_neighbor_aStar(open_list, left_tile, source)
        self.check_neighbor_aStar(open_list, down_tile, source)
        self.check_neighbor_aStar(open_list, up_tile, source)

        expand_limit = 0
        tiles_length = rows * cols
        for _ in range(tiles_length):
            for j in open_list:
                j.a_star_func = j.dist + abs(j.get_coordinates()[0] - dest.get_coordinates()[0]) \
                                + abs(j.get_coordinates()[1] - dest.get_coordinates()[1])
            min = math.inf
            min_idx = None
            for j in open_list:
                if j not in closed_list and not j.is_blocked():
                    if j.a_star_func < min:
                        min = j.a_star_func
                        min_idx = j

            if min_idx is not None:
                expand_limit += 1
                closed_list.append(min_idx)
                open_list.remove(min_idx)
                if expand_limit < 34:
                    self.move(board, (min_idx.get_coordinates()[0], min_idx.get_coordinates()[1]))
                if min_idx.isGoal:

                    min_idx.pathColor()
                    self.find_source(board).color = colors.startColor
                    self.find_dest(board).color = colors.endColor
                    return

                down_tile, left_tile, right_tile, up_tile = self.get_actions(board, min_idx)

                self.expand(closed_list, min_idx, open_list, right_tile)
                self.expand(closed_list, min_idx, open_list, left_tile)
                self.expand(closed_list, min_idx, open_list, down_tile)
                self.expand(closed_list, min_idx, open_list, up_tile)

    def find_dest(self, board):
        dest = None
        for i in range(rows):
            for j in range(cols):
                if board.boardArray[i][j].isGoal:
                    dest = board.boardArray[i][j]
        return dest

    @staticmethod
    def expand(closed_list, min_idx, open_list, right_tile):
        if right_tile.get_coordinates()[0] < 13 \
                and right_tile not in closed_list \
                and min_idx.dist + 1 < right_tile.dist \
                and not right_tile.is_blocked():
            right_tile.dist = min_idx.dist + 1
            right_tile.parent = min_idx
            open_list.append(right_tile)

    @staticmethod
    def check_neighbor_aStar(open_list, right_tile, source):
        if right_tile.get_coordinates()[0] < 13:
            right_tile.dist = 1
            open_list.append(right_tile)
            right_tile.parent = source

    @staticmethod
    def find_source(board):
        source = None
        for i in range(rows):
            for j in range(cols):
                if board.boardArray[i][j].isStart:
                    source = board.boardArray[i][j]
        return source
