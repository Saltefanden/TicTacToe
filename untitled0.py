# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 22:37:24 2021

@author: NMDL
"""

from abc import ABCMeta, abstractmethod
import random


class Counter:
    def __init__(self, string):
        self.label = string

    def __str__(self):
        return self.label


class Move:
    """Represents move made by a player, depends on the x and y coordinate and
    the counter of the player passed to it"""
    def __init__(self, counter, x, y):
        self.x = x
        self.y = y
        self.counter = counter


class Player(metaclass=ABCMeta):
    
    def __init__(self,board):
        self.board = board
        self._counter = None

    
    @property
    def counter(self):
        return self._counter

    
    @counter.setter
    def counter(self,value):
        self._counter = value


    @abstractmethod
    def get_move(self): pass

    def __str__(self):
        return self.__class__.__name__ + '[' + str(self.counter) + ']'


class HumanPlayer(Player):
    def __init__(self,board):
        super().__init__(board)


    def _get_user_input(self,prompt):
        invalid_input = True
        while invalid_input:
            print(prompt)
            user_input = input()
            if not user_input.isdigit():
                print('Input must be a number')
            else:
                user_input_int = int(user_input)
                if user_input_int not in range(1,4):
                    print('Input must be between 1 and 3')
                else:
                    invalid_input = False
        return user_input_int - 1

    def get_move(self):
        while True:
            row = self._get_user_input('Please input desired row number: ')
            col = self._get_user_input('Please input desired column number: ')
            if self.board.is_empty_cell(row,col):
                return Move(self.counter, row, col)
            else:
                print('Position occupied')
                print('Try again you nerd')


class ComputerPlayer(Player):
    def __init__(self, board):
        super().__init__(board)
    
    def randomly_select_cell(self):
        while True:
            row = random.randint(0,2)
            col = random.randint(0,2)
            if self.board.is_empty_cell(row,col):
                return Move(self.counter, row, col)
    
    def get_move(self):
        if self.board.is_empty_cell(1,1):
            return Move(self.counter, 1,1)
        elif self.board.is_empty_cell(0,0):
            return Move(self.counter, 0,0)
        elif self.board.is_empty_cell(2,2):
            return Move(self.counter, 2,2)
        elif self.board.is_empty_cell(0,2):
            return Move(self.counter, 0,2)
        elif self.board.is_empty_cell(2,0):
            return Move(self.counter, 2,0)
        else:
            return self.randomly_select_cell()

class Board:
    def __init__(self):
        self.cells = [['   ','   ','   '],['   ','   ','   '],['   ','   ','   ']]
        self.sep = '\n' + ('-'*13) + '\n'

    def __str__(self):
        row1 = (' ' + str(self.cells[0][0]) + '|' + str(self.cells[0][1]) 
                + '|' + str(self.cells[0][2]) + ' ' )
        row2 = (' ' + str(self.cells[1][0]) + '|' + str(self.cells[1][1]) 
                + '|' + str(self.cells[1][2]) + ' ' )
        row3 = (' ' + str(self.cells[2][0]) + '|' + str(self.cells[2][1]) 
                + '|' + str(self.cells[2][2]) + ' ' )
        return row1 + self.sep + row2 + self.sep + row3
        

    def add_move(self,move):
        row = self.cells[move.x]
        row[move.y] = ' '+ move.counter + ' '


    def is_empty_cell(self, row, col):
        return not bool(self.cells[row][col].strip())


    def cell_contains(self,counter,row,col):
        return self.cells[row][col].strip() == counter


    def is_full(self):
        for row in range(3):
            for col in range(3):
                if self.is_empty_cell(row,col):
                    return False
        return True

    def check_for_winner(self,player):
        c = player.counter
        return (# across the top
                (self.cell_contains(c, 0, 0) 
                 and self.cell_contains(c, 0, 1) 
                 and self.cell_contains(c, 0, 2)) 
                or # across the middle
                (self.cell_contains(c, 1, 0) 
                 and self.cell_contains(c, 1, 1) 
                 and self.cell_contains(c, 1, 2)) 
                or # across the bottom 
                (self.cell_contains(c, 2, 0) 
                 and self.cell_contains(c, 2, 1) 
                 and self.cell_contains(c, 2, 2))
                or # down the left side
                (self.cell_contains(c, 0, 0) 
                 and self.cell_contains(c, 1, 0) 
                 and self.cell_contains(c, 2, 0)) 
                or # down the middle
                (self.cell_contains(c, 0, 1) 
                 and self.cell_contains(c, 1, 1) 
                 and self.cell_contains(c, 2, 1))
                or # down the right side 
                (self.cell_contains(c, 0, 2) 
                 and self.cell_contains(c, 1, 2) 
                 and self.cell_contains(c, 2, 2))
                or # diagonal
                (self.cell_contains(c, 0, 0) 
                 and self.cell_contains(c, 1, 1) 
                 and self.cell_contains(c, 2, 2)) 
                or # other diagonal
                (self.cell_contains(c, 0, 2) 
                 and self.cell_contains(c, 1, 1) 
                 and self.cell_contains(c, 2, 0)))


class Game:
    def __init__(self):
        self.board = Board()
        self.human = HumanPlayer(self.board)
        self.computer = ComputerPlayer(self.board)
        self.next_player = None
        self.winner = None
    
    def select_player_counter(self):
        counter = ''
        while not (counter == 'X' or counter == 'O'):
            print('Do you want to be x or o?')
            counter = input().upper()
            if counter not in ['O', 'X']:
                print('Input must be x or o')
            else:
                self.human.counter = counter
                self.computer.counter = ({'X','O'} - set(counter)).pop()

    def select_player_to_go_first(self):
        if random.randint(0,1) == 0:
            self.next_player = self.human
        else:
            self.next_player = self.computer


    def play(self):
        print('Welcome to TIC TAC TOE')
        self.select_player_counter()
        self.select_player_to_go_first()
        print(self.next_player, ' will go first')
        while self.winner is None:
            if self.next_player == self.human:
                print(self.board)
                print('Your move human nerd')
                move = self.human.get_move()
                self.board.add_move(move)
                if self.board.check_for_winner(self.human):
                    self.winner = self.human
                else:
                    self.next_player = self.computer
            else:
                print('Computers move')
                move = self.computer.get_move()
                self.board.add_move(move)
                if self.board.check_for_winner(self.computer):
                    self.winner = self.computer
                else:
                    self.next_player = self.human
            
            if self.winner is not None:
                print('Winner is the ' + str(self.winner))
            elif self.board.is_full():
                print('This was another fucking draw')
                break
        print(self.board)


def main():
    #x = Counter('X')
    #o = Counter('O')
    game = Game()
    game.play()

if __name__ == '__main__':
    main()