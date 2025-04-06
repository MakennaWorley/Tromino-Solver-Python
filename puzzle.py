import argparse

from sympy import false

import draw


# class of board
# every board is an object of the class Board 
class Board:
    def __init__(self, left, right, bottom, top):
        self.left, self.right, self.bottom, self.top = left, right, bottom, top

    # call this method to return four boundaries of the board 
    def get_boundary(self):
        return self.left, self.right, self.bottom, self.top


class Puzzle:
    def __init__(self, size, block):
        # size is the size of board. 
        # block is the position (x,y) of the block 

        # fill the initial block as black
        draw.draw_one_square(block, 'k')
        # draw the grid on the board 
        draw.grid(size)

        self.blocks = []

        # create the board at full size 
        board = Board(1, size, 1, size)
        # call solve to fill the Tromino recursively using divide and conquer 
        self.solve(block, board)

        # show and save the result in a picture 
        draw.save_and_show(size, block)

    def solve(self, block, board):
        # block is a position (row, column) and board is an object of Board class
        # recursively call solve() on four small size boards with only one block on each board
        # stop the recursive call when reaching to the base case, which is board 2*2
        #
        # call draw.draw_one_tromino(type, board) to draw one type of tromino at the center of the board. The type of the tromino is an integer 1 to 4 as explained in the instruction and the board is an object of Board class where you want to draw the tromino at its center.

        left, right, bottom, top = board.get_boundary()
        # your code goes here:

        if right - left == 1 and top - bottom == 1: #base case 2x2
            #print("Last block to be placed", block, "on", left, right, bottom, top)
            if block == (right, top):
                #print("1")
                draw.draw_one_tromino(1, board)
            elif block == (left, top):
                #print("2")
                draw.draw_one_tromino(2, board)
            elif block == (left, bottom):
                #print("3")
                draw.draw_one_tromino(3, board)
            else:
                #print("4")
                draw.draw_one_tromino(4, board)
            #print('Finished current quadrant')
            return

        mid_x = (left + right) // 2
        mid_y = (bottom + top) // 2
        #print("mid x", mid_x, " mid y", mid_y)

        q1 = Board(mid_x + 1, right, mid_y + 1, top)
        q2 = Board(left, mid_x, mid_y + 1, top)
        q3 = Board(left, mid_x, bottom, mid_y)
        q4 = Board(mid_x + 1, right, bottom, mid_y)

        #print(q1.get_boundary(), q2.get_boundary(), q3.get_boundary(), q4.get_boundary())
        #print("block:", block)

        list_of_boards = [q1, q2, q3, q4]

        piece_type = self.get_tromino_type(block, list_of_boards)

        # place a tromino piece such that all quads have same number of free blocks
        draw.draw_one_tromino(piece_type, board)
        #print(board.get_boundary())
        #print("placed piece", piece_type)

        match piece_type:
            case 1:
                self.solve(block, q1)
            case 2:
                self.solve(block, q2)
            case 3:
                self.solve(block, q3)
            case 4:
                self.solve(block, q4)

        if piece_type != 1:
            #self.solve((mid + 1, mid + 1), q1)
            # print((mid + 1, mid + 1), q1.get_boundary())
            self.solve((mid_x + 1, mid_y + 1), q1)
        if piece_type != 2:
            #self.solve((mid, mid + 1), q2)
            # print((mid, mid + 1), q2.get_boundary())
            self.solve((mid_x, mid_y + 1), q2)
        if piece_type != 3:
            #self.solve((mid, mid), q3)
            #print((mid, mid), q3.get_boundary())
            self.solve((mid_x, mid_y), q3)
        if piece_type != 4:
            #self.solve((mid + 1, mid), q4)
            #print((mid + 1, mid), q4.get_boundary())
            self.solve((mid_x + 1, mid_y), q4)

        #print(self.blocks)

        while self.blocks:
            removed_list = self.blocks.pop(0)
            #print(removed_list[0], removed_list[1].get_boundary())
            self.solve(removed_list[0], removed_list[1])


    def get_tromino_type(self, block, list):
        # return the type of the tromino you should draw based on the position of the block and the board.
        # your code goes here:
        board_num = 0
        for board in list:
            board_num += 1
            left, right, bottom, top = board.get_boundary()
            if left <= block[0] <= right and bottom <= block[1] <= top:
                return board_num


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='puzzle')

    parser.add_argument('-size', dest='size', required=True, type=int, help='size of the board: 2^n')
    parser.add_argument('-block', dest='block', required=True, nargs='+', type=int,
                        help='position of the initial block')

    args = parser.parse_args()

    # size must be a positive integer 2^n
    # block must be two integers between 1 and size 
    game = Puzzle(args.size, tuple(args.block))

    # game = puzzle(8, (1,1))
    # python puzzle.py -size 8 -block 1 1
