### Quoridor AI contest ###

import sys

class Game:
    'Game class. Runs and displays a game of quoridor'

    def __init__(self, player1=0, player2=0):
        if player1 == 0:
            player1Name = input("Player 1 enter name: ")
            self.player1 = Human(player1Name)
        else:
            self.player1 = player1

        if player2 == 0:
            player2Name = input("Player 2 enter name: ")
            self.player2 = Human(player2Name)
        else:
            self.player2 = player2

        self.board = Board()

    def play(self):
        self.board.display()
        gameOver = False
        while not gameOver:
            gameOver = self.board.isGameOver()
            
            # player 1 turn
            move = self.player1.getMove(self.board)
            (isValid, error) = self.board.validMove(move)
            while not isValid:
                self.board.display()
                print(error)
                move = self.player1.getMove(self.board)
                (isValid, error) = self.board.validMove(move)
            self.board.update(move, 1)
            self.board.display()
            
            # player 2 turn
            move = self.player2.getMove(self.board)
            while not self.board.validMove(move):
                move = self.player2.getMove(self.board)
            self.board.update(move, 2)
            self.board.display()

        self.board.displayEndResult()

class Human:
    def __init__(self, name):
        self.name = name

    def getMove(self, board):
        return input(self.name + " enter a move: ")

class Board:
    'Board class. Stores the board data'

    def __init__(self):
        self.board = [
            [ 0, 0, 0, 0, 1, 0, 0, 0, 0 ],
            [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
            [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
            [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
            [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
            [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
            [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
            [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
            [ 0, 0, 0, 0, 2, 0, 0, 0, 0 ]
        ]

        self.wallsVertical = [
            [ 0, 0, 0, 0, 0, 0, 0, 0 ],
            [ 0, 0, 0, 0, 0, 0, 0, 0 ],
            [ 0, 0, 0, 0, 0, 0, 0, 0 ],
            [ 0, 0, 0, 0, 0, 0, 0, 0 ],
            [ 0, 0, 0, 0, 0, 0, 0, 0 ],
            [ 0, 0, 0, 0, 0, 0, 0, 0 ],
            [ 0, 0, 0, 0, 0, 0, 0, 0 ],
            [ 0, 0, 0, 0, 0, 0, 0, 0 ],
            [ 0, 0, 0, 0, 0, 0, 0, 0 ],
        ]
        
        self.wallsHorizontal = [
            [ 0, 0, 0, 0, 0, 0, 0, 0 ],
            [ 0, 0, 0, 0, 0, 0, 0, 0 ],
            [ 0, 0, 0, 0, 0, 0, 0, 0 ],
            [ 0, 0, 0, 0, 0, 0, 0, 0 ],
            [ 0, 0, 0, 0, 0, 0, 0, 0 ],
            [ 0, 0, 0, 0, 0, 0, 0, 0 ],
            [ 0, 0, 0, 0, 0, 0, 0, 0 ],
            [ 0, 0, 0, 0, 0, 0, 0, 0 ],
            [ 0, 0, 0, 0, 0, 0, 0, 0 ],
        ]
        
        self.moveDictionary = {
            "A":0,
            "B":1,
            "C":2,
            "D":3,
            "E":4,
            "F":5,
            "G":6,
            "H":7,
            "I":8
        }

    def wallsRemaining(self, player):
        count = 0
        for row in self.wallsVertical:
            for cell in row:
                if cell==player:
                    count += 1
        for row in self.wallsHorizontal:
            for cell in row:
                if cell==player:
                    count += 1
        return 8 - count
            

    def validMove(self, move):
        move = move.upper()
        rows = "123456789"
        columns = "ABCDEFGHI"
        if len(move)==4:
            # WALL
            if (move[0] in rows and move[1] in rows and move[2] in columns and move[3] in columns):
                if int(move[0])+1==int(move[1]) and int(self.moveDictionary.get(move[2]))+1==int(self.moveDictionary.get(move[3])):
                    return True, ""
                else:
                    return False, "Invalid format"
            if (move[0] in columns and move[1] in columns and move[2] in rows and move[3] in rows):
                if int(move[2])+1==int(move[3]) and int(self.moveDictionary.get(move[0]))+1==int(self.moveDictionary.get(move[1])):
                    return True, ""
                else:
                    return False, "Invalid format"

        elif len(move)==2:
            # STEP
            return True, ""
        else:
            return False, "Invalid move"

    def update(self, move, player):
        move = move.upper()
        if len(move) > 2:
            # WALL
            if move[0] in self.moveDictionary.keys():
                # VERTICAL
                i = self.moveDictionary.get(move[0])
                j = int(move[2])-1
                self.wallsVertical[i][j] = player
                
            else:
                # HORIZONTAL
                i = int(move[0])-1
                j = self.moveDictionary.get(move[2])
                self.wallsHorizontal[i][j] = player
                
        else:
            # STEP
            for i, row in enumerate(self.board):
                for j, cell in enumerate(row):
                    if cell==player:
                        self.board[i][j]=0
            i = int(move[1])-1
            j = self.moveDictionary.get(move[0])
            self.board[i][j] = player

    def displayEndResult(self):
        print("GAME OVER")

    def isGameOver(self):
        return False

    def display(self):
        # ascii art
        sys.stdout.write("               _____   _____   _____   _____   _____   _____   _____   _____   _____\n")
        for i in range(8):
            self.displayRow(9-i)
            self.displayGap(8-i)
        self.displayRow(1)
        sys.stdout.write("                 A       B       C       D       E       F       G       H       I\n")

    def displayRow(self, rowNumber):
        self.displayRowHelper(rowNumber, False, "|     |")
        self.displayRowHelper(rowNumber, True, "|     |")
        self.displayRowHelper(rowNumber, False, "|_____|")

    def displayRowHelper(self, rowNumber, center, cellString):
        if center:
            sys.stdout.write("            " + str(rowNumber) + " ")
        else:
            sys.stdout.write("              ")

        for i in range(8):
            if rowNumber==9:
                if self.wallsVertical[i][rowNumber-2] > 0:
                    if center and self.board[rowNumber-1][i]==1:
                        sys.stdout.write("|  1  |W")
                    elif center and self.board[rowNumber-1][i]==2:
                        sys.stdout.write("|  2  |W")
                    else:
                        sys.stdout.write(cellString+"W")
                else:
                    if center and self.board[rowNumber-1][i]==1:
                        sys.stdout.write("|  1  | ")
                    elif center and self.board[rowNumber-1][i]==2:
                        sys.stdout.write("|  2  | ")
                    else:
                        sys.stdout.write(cellString+" ")
            elif rowNumber==1:
                if self.wallsVertical[i][rowNumber-1] > 0:
                    if center and self.board[rowNumber-1][i]==1:
                        sys.stdout.write("|  1  |W")
                    elif center and self.board[rowNumber-1][i]==2:
                        sys.stdout.write("|  2  |W")
                    else:
                        sys.stdout.write(cellString+"W")
                else:
                    if center and self.board[rowNumber-1][i]==1:
                        sys.stdout.write("|  1  | ")
                    elif center and self.board[rowNumber-1][i]==2:
                        sys.stdout.write("|  2  | ")
                    else:
                        sys.stdout.write(cellString+" ")
            else:
                if self.wallsVertical[i][rowNumber-1] > 0 or self.wallsVertical[i][rowNumber-2] > 0:
                    if center and self.board[rowNumber-1][i]==1:
                        sys.stdout.write("|  1  |W")
                    elif center and self.board[rowNumber-1][i]==2:
                        sys.stdout.write("|  2  |W")
                    else:
                        sys.stdout.write(cellString+"W")
                else:
                    if center and self.board[rowNumber-1][i]==1:
                        sys.stdout.write("|  1  | ")
                    elif center and self.board[rowNumber-1][i]==2:
                        sys.stdout.write("|  2  | ")
                    else:
                        sys.stdout.write(cellString+" ")
        sys.stdout.write(cellString+"\n")
        
    def displayGap(self, gapNumber):
        if (self.wallsRemaining(1) > 8-gapNumber):
            sys.stdout.write(" WWWWWWWWWWWWW")
        else:
            sys.stdout.write("              ")
            
        i = 0
        while i < 8:
            if self.wallsHorizontal[gapNumber-1][i]==1 or self.wallsHorizontal[gapNumber-1][i]==2:
                sys.stdout.write(" WWWWWWWWWWWWW ")
                i += 2
            else:
                sys.stdout.write(" _____ ")
                i += 1
            if self.wallsVertical[i-1][gapNumber-1] > 0:
                sys.stdout.write("W")
            else:
                sys.stdout.write(" ")
        if i==8:
            sys.stdout.write(" _____ ")

        if (self.wallsRemaining(2) > 8-gapNumber):
            sys.stdout.write("WWWWWWWWWWWWW\n")
        else:
            sys.stdout.write("\n")
            


g = Game()
g.play()
