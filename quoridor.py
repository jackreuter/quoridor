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
            (isValid, error) = self.board.validMove(move, 1)
            while not isValid:
                self.board.display()
                print(error)
                move = self.player1.getMove(self.board)
                (isValid, error) = self.board.validMove(move, 1)
            self.board.update(move, 1)
            self.board.display()

            # player 2 turn
            move = self.player2.getMove(self.board)
            (isValid, error) = self.board.validMove(move, 2)
            while not isValid:
                self.board.display()
                print(error)
                move = self.player2.getMove(self.board)
                (isValid, error) = self.board.validMove(move, 2)
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
        
    def getPlayerPosition(self, player):
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                if cell==player:
                    return i, j
        return -1, -1

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
            

    def validMove(self, move, player):
        move = move.upper()
        if not self.validFormat(move):
            return False, "Invalid format"
        else:
            return self.legalMove(move, player)

    def validFormat(self, move):
        rows = "123456789"
        columns = "ABCDEFGHI"
        if len(move)==4:
            # WALL
            if (move[0] in rows and move[1] in rows and move[2] in columns and move[3] in columns):
                if int(move[0])+1==int(move[1]) and int(self.moveDictionary.get(move[2]))+1==int(self.moveDictionary.get(move[3])):
                    return True
                else:
                    return False
            if (move[0] in columns and move[1] in columns and move[2] in rows and move[3] in rows):
                if int(move[2])+1==int(move[3]) and int(self.moveDictionary.get(move[0]))+1==int(self.moveDictionary.get(move[1])):
                    return True
                else:
                    return False

        elif len(move)==2:
            # MOVEMENT
            if (move[0] in columns and move[1] in rows):
                return True
            else:
                return False
        else:
            return False

    def legalMove(self, move, player):
        (isLegal, error) = True, ""
        if len(move) == 4:
            # WALL
            if move[0] in self.moveDictionary.keys():
                # VERTICAL
                i = self.moveDictionary.get(move[0])
                j = int(move[2])-1
                # check if wall exists
                if self.wallsVertical[i][j] > 0:
                    return False, "wall already exists"
                # check if crossing
                if self.wallsHorizontal[j][i] > 0:
                    return False, "walls cannot intersect"
                else:
                    # check if overlaps
                    if j == 0:
                        if self.wallsVertical[i][j+1] > 0:
                            return False, "walls cannot overlap"
                    elif j == 7:
                        if self.wallsVertical[i][j-1] > 0:
                            return False, "walls cannot overlap"
                    else:
                        if self.wallsVertical[i][j-1] > 0 or self.wallsVertical[i][j+1] > 0:
                            return False, "walls cannot overlap"
                
            else:
                # HORIZONTAL
                i = int(move[0])-1
                j = self.moveDictionary.get(move[2])
                # check if wall exists
                if self.wallsHorizontal[i][j] > 0:
                    return False, "wall already exists"
                # check if crossing
                elif self.wallsVertical[j][i] > 0:
                    return False, "walls cannot intersect"
                else:
                    # check if overlaps
                    if j == 0:
                        if self.wallsHorizontal[i][j+1] > 0:
                            return False, "walls cannot overlap"
                    elif j == 7:
                        if self.wallsHorizontal[i][j-1] > 0:
                            return False, "walls cannot overlap"
                    else:
                        if self.wallsHorizontal[i][j-1] > 0 or self.wallsHorizontal[i][j+1] > 0:
                            return False, "walls cannot overlap"

        if len(move) == 2: 
            # MOVEMENT
            # check adjacency
            (x, y) = self.getPlayerPosition(player)
            i = int(move[1])-1
            j = self.moveDictionary.get(move[0])
            if not (((i == x+1 or i == x-1) and (j == y)) or ((i == x) and (j == y+1 or j == y-1))):
                print(x,y,i,j)
                return False, "must move to an adjacent square"
            else:
                # check walls
                if (j == y):
                    if (i == x+1):
                        # NORTH
                        if (y == 0):
                            if (self.wallsHorizontal[x][y] > 0):
                                return False, "cannot move through wall"
                            else:
                                return True, ""
                        elif (y == 8):
                            if (self.wallsHorizontal[x][y-1] > 0):
                                return False, "cannot move through wall"
                            else:
                                return True, ""
                        else:
                            if (self.wallsHorizontal[x][y] > 0 or self.wallsHorizontal[x][y-1] > 0):
                                return False, "cannot move through wall"
                            else:
                                return True, ""
                        return True, ""
                    elif (i == x-1):
                        # SOUTH
                        if (y == 0):
                            if (self.wallsHorizontal[x-1][y] > 0):
                                return False, "cannot move through wall"
                            else:
                                return True, ""
                        elif (y == 8):
                            if (self.wallsHorizontal[x-1][y-1] > 0):
                                return False, "cannot move through wall"
                            else:
                                return True, ""
                        else:
                            if (self.wallsHorizontal[x-1][y] > 0 or self.wallsHorizontal[x-1][y-1] > 0):
                                return False, "cannot move through wall"
                            else:
                                return True, ""
                        return True, ""
                    else:
                        return False, "coding error"
                elif (i == x):
                    if (j == y+1):
                        # EAST
                        if (x == 0):
                            if (self.wallsVertical[y][x] > 0):
                                return False, "cannot move through wall"
                            else:
                                return True, ""
                        elif (x == 8):
                            if (self.wallsVertical[y][x-1] > 0):
                                return False, "cannot move through wall"
                            else:
                                return True, ""
                        else:
                            if (self.wallsVertical[y][x] > 0 or self.wallsVertical[y][x-1] > 0):
                                return False, "cannot move through wall"
                            else:
                                return True, ""
                        return True, ""
                    elif (j == y-1):
                        # WEST
                        if (x == 0):
                            if (self.wallsVertical[y-1][x] > 0):
                                return False, "cannot move through wall"
                            else:
                                return True, ""
                        elif (x == 8):
                            if (self.wallsVertical[y-1][x-1] > 0):
                                return False, "cannot move through wall"
                            else:
                                return True, ""
                        else:
                            if (self.wallsVertical[y-1][x] > 0 or self.wallsVertical[y-1][x-1] > 0):
                                return False, "cannot move through wall"
                            else:
                                return True, ""
                        return True, ""
                    else:
                        return False, "coding error"
                else:
                    return False, "coding error"
        return isLegal, error

    def update(self, move, player):
        move = move.upper()
        if len(move) > 2:
            # WALL
            if move[0] in self.moveDictionary.keys():
                # VERTICAL
                i = self.moveDictionary.get(move[0])
                j = int(move[2])-1
                self.wallsVertical[i][j] = player
                print (i,j)
                
            else:
                # HORIZONTAL
                i = int(move[0])-1
                j = self.moveDictionary.get(move[2])
                self.wallsHorizontal[i][j] = player
                print (i,j)
                
        else:
            # MOVEMENT
            (x, y) = self.getPlayerPosition(player)
            self.board[x][y]=0
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
        for row in self.board:
            print(row)

    def displayRow(self, rowNumber):
        self.displayRowHelper(rowNumber, False, "|     |")
        self.displayRowHelper(rowNumber, True, "|     |")
        self.displayRowHelper(rowNumber, False, "|_____|")

    def displayRowHelper(self, rowNumber, center, cellString):
        if center:
            sys.stdout.write("            " + str(rowNumber) + " ")
        else:
            sys.stdout.write("              ")

        for i in range(9):
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
        sys.stdout.write("\n")
        
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
