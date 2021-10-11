from enum import Enum
import pygame
import copy
import random

size = 8

white = (235,235,235)
darkGray = (200,200,200)
gray = (100,100,100)
black = (0,0,0)
green = (40,200,20)
red = (255,0,0)
lilla = (255,0,255)
blue = (0,255,0)
yellow = (255,255,0)

# Size of piece: 45x45
imSize = 45
display_width = 8*imSize
display_height = 8*imSize
gameDisplay = pygame.display.set_mode((display_width+1,display_height + 30))

pygame.init()
clock = pygame.time.Clock()

image_BP = pygame.image.load("blackPawn.png")
image_BR = pygame.image.load("blackRook.png")
image_BB = pygame.image.load("blackBishop.png")
image_BQ = pygame.image.load("blackQueen.png")
image_BK = pygame.image.load("blackKing.png")
image_BN = pygame.image.load("blackKnight.png")
image_Bdot = pygame.image.load("blackDot.png")
image_WP = pygame.image.load("whitePawn.png")
image_WR = pygame.image.load("whiteRook.png")
image_WB = pygame.image.load("whiteBishop.png")
image_WQ = pygame.image.load("whiteQueen.png")
image_WK = pygame.image.load("whiteKing.png")
image_WN = pygame.image.load("whiteKnight.png")
image_Wdot = pygame.image.load("whiteDot.png")

class Type(Enum):
    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6
    
class Color(Enum):
    NONE = 0
    WHITE = 1
    BLACK = 2

class Piece(object):
    def __init__(self,type,color,row,col):
        self.type = type
        self.color = color
        self.row = row
        self.col = col

def changeColor(color):
    if color == Color.WHITE:
        return Color.BLACK
    return Color.WHITE

def center_message(msg,color,y):
    font = pygame.font.SysFont('lucidagrande', 20)
    textSurf = font.render(msg,True,color)
    textRect = textSurf.get_rect()
    textRect.center = (display_width/2,y)
    gameDisplay.blit(textSurf, textRect)
    

class Board(object):
    def __init__(self):
        
        self.castlingWhiteLeft = True
        self.castlingWhiteRight = True
        self.castlingBlackLeft = True
        self.castlingBlackRight = True
        
        self.pieces = [0]*32
        # Color.WHITE self.pieces
        self.pieces[0] = Piece(Type.PAWN,Color.WHITE,1,0)
        self.pieces[1] = Piece(Type.PAWN,Color.WHITE,1,1)
        self.pieces[2] = Piece(Type.PAWN,Color.WHITE,1,2)
        self.pieces[3] = Piece(Type.PAWN,Color.WHITE,1,3)
        self.pieces[4] = Piece(Type.PAWN,Color.WHITE,1,4)
        self.pieces[5] = Piece(Type.PAWN,Color.WHITE,1,5)
        self.pieces[6] = Piece(Type.PAWN,Color.WHITE,1,6)
        self.pieces[7] = Piece(Type.PAWN,Color.WHITE,1,7)
        self.pieces[8] = Piece(Type.ROOK,Color.WHITE,0,0)
        self.pieces[9] = Piece(Type.KNIGHT,Color.WHITE,0,1)
        self.pieces[10] = Piece(Type.BISHOP,Color.WHITE,0,2)
        self.pieces[11] = Piece(Type.QUEEN,Color.WHITE,0,3)
        self.pieces[12] = Piece(Type.KING,Color.WHITE,0,4)
        self.pieces[13] = Piece(Type.BISHOP,Color.WHITE,0,5)
        self.pieces[14] = Piece(Type.KNIGHT,Color.WHITE,0,6)
        self.pieces[15] = Piece(Type.ROOK,Color.WHITE,0,7)
        # Color.BLACK self.pieces
        self.pieces[16] = Piece(Type.PAWN,Color.BLACK,6,0)
        self.pieces[17] = Piece(Type.PAWN,Color.BLACK,6,1)
        self.pieces[18] = Piece(Type.PAWN,Color.BLACK,6,2)
        self.pieces[19] = Piece(Type.PAWN,Color.BLACK,6,3)
        self.pieces[20] = Piece(Type.PAWN,Color.BLACK,6,4)
        self.pieces[21] = Piece(Type.PAWN,Color.BLACK,6,5)
        self.pieces[22] = Piece(Type.PAWN,Color.BLACK,6,6)
        self.pieces[23] = Piece(Type.PAWN,Color.BLACK,6,7)
        self.pieces[24] = Piece(Type.ROOK,Color.BLACK,7,0)
        self.pieces[25] = Piece(Type.KNIGHT,Color.BLACK,7,1)
        self.pieces[26] = Piece(Type.BISHOP,Color.BLACK,7,2)
        self.pieces[27] = Piece(Type.QUEEN,Color.BLACK,7,3)
        self.pieces[28] = Piece(Type.KING,Color.BLACK,7,4)
        self.pieces[29] = Piece(Type.BISHOP,Color.BLACK,7,5)
        self.pieces[30] = Piece(Type.KNIGHT,Color.BLACK,7,6)
        self.pieces[31] = Piece(Type.ROOK,Color.BLACK,7,7)
    
    def copy(self,pieces):
        copyBoard = self
        copyBoard.pieces = pieces
        return copyBoard
    
    def isEmpty(self,row,col):
        for p in self.pieces:
            if p.row == row and p.col == col:
                return False
        return True

    def countTiles(self,piece,dx,dy,moves):
        i = 1
        while piece.row + i*dy < size and piece.row + i*dy >= 0 and piece.col + i*dx < size and piece.col + i*dx >= 0:
            for p in self.pieces:
                if p.row == (piece.row + i*dy) and p.col == piece.col + i*dx:
                    if p.color == piece.color:
                        return
                    else:
                        moves.append([piece.row + i*dy,piece.col + i*dx])
                        return
            moves.append([piece.row + i*dy,piece.col + i*dx])
            i += 1
        return
        
    def getLegalMovesNaiv(self,piece):
        moves = []
        
        if piece.type == Type.PAWN:
            if piece.color == Color.BLACK:
                if piece.row == 6 and self.isEmpty(4,piece.col) and self.isEmpty(5,piece.col):
                    moves = [[5,piece.col],[4,piece.col]]
                elif self.isEmpty(piece.row - 1,piece.col):
                    moves = [[piece.row - 1,piece.col]]
                for p in self.pieces:
                    if [piece.row - 1,piece.col] in moves and [p.row,p.col] == [piece.row - 1,piece.col]:
                        moves.remove([p.row,p.col])
                    if p.row == piece.row - 1 and (p.col == piece.col - 1 or p.col == piece.col + 1) and p.color == Color.WHITE:
                        moves.append([p.row,p.col])
            else:
                if piece.row == 1 and self.isEmpty(2,piece.col) and self.isEmpty(3,piece.col):
                    moves = [[2,piece.col],[3,piece.col]]
                elif self.isEmpty(piece.row + 1,piece.col):
                    moves = [[piece.row + 1,piece.col]]
                for p in self.pieces:
                    if [piece.row + 1,piece.col] in moves and [p.row,p.col] == [piece.row + 1,piece.col]:
                        moves.remove([p.row,p.col])
                    if p.row == piece.row + 1 and (p.col == piece.col - 1 or p.col == piece.col + 1) and p.color == Color.BLACK:
                        moves.append([p.row,p.col])
                        
        elif piece.type == Type.KNIGHT:
            moves = [[piece.row + 2, piece.col + 1],[piece.row + 2, piece.col - 1],[piece.row - 2, piece.col + 1],[piece.row - 2, piece.col - 1],[piece.row + 1, piece.col + 2],[piece.row + 1, piece.col - 2],[piece.row - 1, piece.col + 2],[piece.row - 1, piece.col - 2]]
            temp = []
            for m in moves:
                if m[0] >= 0 and m[1] >= 0 and m[0] < size and m[1] < size:
                    temp.append(m)
            moves = temp
            for p in self.pieces:
                if p.color == piece.color and [p.row,p.col] in moves:
                    moves.remove([p.row,p.col])
                    
        elif piece.type == Type.ROOK:
            self.countTiles(piece,1,0,moves)
            self.countTiles(piece,0,1,moves)
            self.countTiles(piece,-1,0,moves)
            self.countTiles(piece,0,-1,moves)
        
        elif piece.type == Type.BISHOP:
            self.countTiles(piece,1,1,moves)
            self.countTiles(piece,1,-1,moves)
            self.countTiles(piece,-1,1,moves)
            self.countTiles(piece,-1,-1,moves)
        
        elif piece.type == Type.QUEEN:
            self.countTiles(piece,1,0,moves)
            self.countTiles(piece,0,1,moves)
            self.countTiles(piece,-1,0,moves)
            self.countTiles(piece,0,-1,moves)
            self.countTiles(piece,1,1,moves)
            self.countTiles(piece,1,-1,moves)
            self.countTiles(piece,-1,1,moves)
            self.countTiles(piece,-1,-1,moves)
            
        elif piece.type == Type.KING:
            moves = [[piece.row + 1, piece.col],[piece.row, piece.col + 1],[piece.row - 1, piece.col],[piece.row, piece.col - 1],[piece.row + 1, piece.col + 1],[piece.row + 1, piece.col - 1],[piece.row - 1, piece.col + 1],[piece.row - 1, piece.col - 1]]
            temp = []
            for m in moves:
                if m[0] >= 0 and m[1] >= 0 and m[0] < size and m[1] < size:
                    temp.append(m)
            moves = temp
            for p in self.pieces:
                if p.color == piece.color and [p.row,p.col] in moves:
                    moves.remove([p.row,p.col])
        
        return moves
    
    
    def getLegalMoves(self,piece):
        moves = self.getLegalMovesNaiv(piece)
        tempMoves = copy.deepcopy(moves)
        if piece.type == Type.KING:
            if piece.color == Color.BLACK:
                if self.castlingBlackLeft:
                    castlingBlackLeftPossible = True
                    for p in self.pieces:
                        if p.row == 7 and (p.col == 2 or p.col == 3):
                                castlingBlackLeftPossible = False
                                break
                    if  castlingBlackLeftPossible:
                        for p in self.pieces:
                            if p.color == Color.WHITE:
                                pMoves = self.getLegalMovesNaiv(p)
                                if [7,2] in pMoves or [7,3] in pMoves or [7,4] in pMoves:
                                    castlingBlackLeftPossible = False
                                    break
                    if castlingBlackLeftPossible:
                        moves.append("castlingBlackLeft")
                        
                if self.castlingBlackRight:
                    castlingBlackRightPossible = True
                    for p in self.pieces:
                        if p.row == 7 and (p.col == 5 or p.col == 6):
                                castlingBlackRightPossible = False
                                break
                    if  castlingBlackRightPossible:
                        for p in self.pieces:
                            if p.color == Color.WHITE:
                                pMoves = self.getLegalMovesNaiv(p)
                                if [7,4] in pMoves or [7,5] in pMoves or [7,6] in pMoves:
                                    castlingBlackRightPossible = False
                                    break
                    if castlingBlackRightPossible:
                        moves.append("castlingBlackRight")   
                                 
            else:
                if self.castlingWhiteLeft:
                    castlingWhiteLeftPossible = True
                    for p in self.pieces:
                        if p.row == 0 and (p.col == 2 or p.col == 3):
                                castlingWhiteLeftPossible = False
                                break
                    if  castlingWhiteLeftPossible:
                        for p in self.pieces:
                            if p.color == Color.BLACK:
                                pMoves = self.getLegalMovesNaiv(p)
                                if [0,2] in pMoves or [0,3] in pMoves or [0,4] in pMoves:
                                    castlingWhiteLeftPossible = False
                                    break
                    if castlingWhiteLeftPossible:
                        moves.append("castlingWhiteLeft")
                        
                if self.castlingWhiteRight:
                    castlingWhiteRightPossible = True
                    for p in self.pieces:
                        if p.row == 0 and (p.col == 5 or p.col == 6):
                                castlingWhiteRightPossible = False
                                break
                        
                    if  castlingWhiteRightPossible:
                        for p in self.pieces:
                            if p.color == Color.BLACK:
                                pMoves = self.getLegalMovesNaiv(p)
                                if [0,4] in pMoves or [0,5] in pMoves or [0,6] in pMoves:
                                    castlingWhiteRightPossible = False
                                    break
                    if castlingWhiteRightPossible:
                        moves.append("castlingWhiteRight")
            
            
        j = None
        for i in range(len(self.pieces)):
            if self.pieces[i] == piece:
                j = i
        for m in tempMoves:
            tempBoard = copy.deepcopy(self)
            tempBoard.movePiece(tempBoard.pieces[j],m)
            if tempBoard.checkCheck(piece.color):
                moves.remove(m)
            
        return moves
    
    def printPiece(self,piece):
        if piece.color == Color.WHITE:
            if piece.type == Type.PAWN:
                print("| P |",end="")
            elif piece.type == Type.KNIGHT:
                print("| N |",end="")
            elif piece.type == Type.ROOK:
                print("| R |",end="")
            elif piece.type == Type.BISHOP:
                print("| B |",end="")
            elif piece.type == Type.QUEEN:
                print("| Q |",end="")
            elif piece.type == Type.KING:
                print("| K |",end="")
        else:
            if piece.type == Type.PAWN:
                print("| p |",end="")
            elif piece.type == Type.KNIGHT:
                print("| n |",end="")
            elif piece.type == Type.ROOK:
                print("| r |",end="")
            elif piece.type == Type.BISHOP:
                print("| b |",end="")
            elif piece.type == Type.QUEEN:
                print("| q |",end="")
            elif piece.type == Type.KING:
                print("| k |",end="")
            
    def  checkCheck(self,turn):
        for p in self.pieces:
            if p.type == Type.KING and p.color == turn:
                for q in self.pieces:
                    if q.color != turn:
                        moves = self.getLegalMovesNaiv(q)
                        if [p.row,p.col] in moves:
                            return True
        return False
    
    def printBoard(self):
        for i in range(size-1,-1,-1):
            for j in range(size+1):
                print("-----",end = "")
            print()
            print("  ",end="")
            print(i,end="")
            print("  ",end="")
            for j in range(size):
                noPiece = True
                for p in self.pieces:
                    if p.row == i and p.col == j:
                        self.printPiece(p)
                        noPiece = False
                if noPiece:
                    print("|   |",end ="")
            print()

        for j in range(size+1):
            print("-----",end = "")
        print()
        print("     ",end="")
        for j in range(size):
            print("| ",end = "")
            print(j,end="")
            print(" |",end = "")
        print()
        
    def movePiece(self,piece,move):
        if move == "castlingBlackLeft":
            piece.col = 2
            for p in self.pieces:
                if p.row == piece.row and p.col == 0:
                    p.col = 3
        elif move == "castlingBlackRight":
            piece.col = 6
            for p in self.pieces:
                if p.row == piece.row and p.col == 7:
                    p.col = 5
        elif move == "castlingWhiteLeft":
            piece.col = 2
            for p in self.pieces:
                if p.row == piece.row and p.col == 0:
                    p.col = 3
        elif move == "castlingWhiteRight":
            piece.col = 6
            for p in self.pieces:
                if p.row == piece.row and p.col == 7:
                    p.col = 5
        else:
            temp = self.pieces
            for p in temp:
                if [p.row,p.col] == move:
                    self.pieces.remove(p)
            
            if piece.type == Type.KING:
                if piece.color == Color.BLACK:
                    self.castlingBlackLeft = False
                    self.castlingBlackRight = False
                else:
                    self.castlingWhiteLeft = False
                    self.castlingWhiteRight = False
            elif piece.type == Type.ROOK:
                if piece.color == Color.BLACK:
                    if piece.row == 7:
                        if piece.col == 0:
                            self.castlingBlackLeft = False
                        elif piece.col == 7:
                            self.castlingBlackRight = False
                else:
                    if piece.row == 0:
                        if piece.col == 0:
                            self.castlingWhiteLeft = False
                        elif piece.col == 7:
                            self.castlingWhiteRight = False
            
            piece.row = move[0]
            piece.col = move[1]
            if piece.type == Type.PAWN:
                if piece.row == size-1 or piece.row == 0:
                    return True
        return False
    
    def getPlayerPiece(self,turn):
        while True:
            row = int(input("Row: "))
            col = int(input("Column: "))
            for p in self.pieces:
                if p.row == row and p.col == col and p.color == turn:
                    return p
            print("No piece found, input new position.")

    def drawGetPlayerPiece(self,row,col,turn):
        for p in self.pieces:
            if p.row == row and p.col == col and p.color == turn:
                return p
            print("No piece found, input new position.")
        
        
    def move(self,turn):
        piece = self.getPlayerPiece(turn)
        moves = self.getLegalMoves(piece)
        while True:
            try:
                row = int(input("Row (or 'b' to go back): "))
                col = int(input("Column: "))
            except ValueError:
                piece = self.getPlayerPiece(turn)
                moves = self.getLegalMoves(piece)
            else:
                if [row,col] in moves:
                    self.movePiece(piece,[row,col])
                    break
                else:
                    print("Not a legal move.")
    
    def drawFindMove(self,row,col,turn,piece):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if (display_width/size*col + display_width/size) > mouse[0] > display_width/size*col and (display_height/size*row + display_height/size) > mouse[1] > display_height/size*row:
            
                pygame.draw.rect(gameDisplay,darkGray,(j*display_width/N,i*display_height/N,display_width/N,display_height/N))
                if click[0] == True:
                    print(self.drawGetPlayerPiece(i,j,turn).type)


            
    def gameOver(self,turn):
        gameOver = True
        for p in self.pieces:
            if p.color == turn and self.getLegalMoves(p) != []:
                gameOver = False
        
        return gameOver
                

    def playAI(self):
        playerColor = Color.WHITE
        AIColor = Color.BLACK
        while not self.gameOver(playerColor):
            piece = self.draw(playerColor)
            while not self.drawSelected(piece):
                piece = self.draw(playerColor)
            if self.gameOver(AIColor):
                self.drawFinishedBoard(playerColor)
            self.drawThinking(AIColor)
            (p,m) = self.getOptimalMove(AIColor)
            self.movePiece(p,m)
            if self.gameOver(playerColor):
                self.drawFinishedBoard(AIColor)
    

    def play(self):
        
        turn = Color.WHITE
        while not self.gameOver(turn):
            piece = self.draw(turn)
            while not self.drawSelected(piece):
                piece = self.draw(turn)
    
            if turn == Color.WHITE:
                turn = Color.BLACK
            else:
                turn = Color.WHITE
        
    
        if turn == Color.WHITE:
            self.drawFinishedBoard(Color.BLACK)
        else:
            self.drawFinishedBoard(Color.WHITE)
        
        """
        self.printBoard()
        while not self.gameOver():
            self.draw(turn)
        
            if turn == Color.WHITE:
                print("Turn: WHITE")
            else:
                print("Turn: BLACK")
            self.move(turn)
            self.printBoard()
            if turn == Color.WHITE:
                turn = Color.BLACK
            else:
                turn = Color.WHITE
                """
        """
        if turn == Color.WHITE:
            print("Black player won!")
        else:
            print("White player won!")
    """

    def drawPiece(self,piece):
        if piece.type == Type.PAWN:
            if piece.color == Color.BLACK:
                image = image_BP
            else:
                image = image_WP
        elif piece.type == Type.ROOK:
            if piece.color == Color.BLACK:
                image = image_BR
            else:
                image = image_WR
        elif piece.type == Type.KNIGHT:
            if piece.color == Color.BLACK:
                image = image_BN
            else:
                image = image_WN
        elif piece.type == Type.BISHOP:
            if piece.color == Color.BLACK:
                image = image_BB
            else:
                image = image_WB
        elif piece.type == Type.QUEEN:
            if piece.color == Color.BLACK:
                image = image_BQ
            else:
                image = image_WQ
        elif piece.type == Type.KING:
            if piece.color == Color.BLACK:
                image = image_BK
            else:
                image = image_WK
                
        gameDisplay.blit(image,(piece.col*imSize,(7-piece.row)*imSize))
    
    def drawMoves(self,color,moves):
            if color == Color.WHITE:
                image = image_Wdot
            else:
                image = image_Bdot
                
            for m in moves:
                if m == "castlingBlackLeft":
                    gameDisplay.blit(image_Bdot,(2*imSize,0))
                elif m == "castlingBlackRight":
                    gameDisplay.blit(image_Bdot,(6*imSize,0))
                elif m == "castlingWhiteLeft":
                    gameDisplay.blit(image_Wdot,(2*imSize,7*imSize))
                elif m == "castlingWhiteRight":
                    gameDisplay.blit(image_Wdot,(6*imSize,7*imSize))
                else:
                    gameDisplay.blit(image,(m[1]*imSize,(7-m[0])*imSize))

    def draw(self,turn):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            gameDisplay.fill(white)
            for i in range(size):
                for j in range(size):
                    pygame.draw.rect(gameDisplay, (40*((i+j+1)%2) + 150,40*((i+j+1)%2)+150,40*((i+j+1)%2)+150), ((i*display_width/size,j*display_height/size),(display_width/size,display_height/size)))
            
            for p in self.pieces:
                self.drawPiece(p)
                    
            for i in range(size+1):
                pygame.draw.line(gameDisplay,black,(display_width/size*i,0),(display_width/size*i,display_height))
                pygame.draw.line(gameDisplay,black,(0,display_height/size*i),(display_width,display_height/size*i))      
            
            if turn == Color.WHITE:
                center_message("Turn: White",black,size*imSize+15)
            else:
                center_message("Turn: Black",black,size*imSize+15)
                
            
            if pygame.mouse.get_pressed()[0]:
                mousePos = pygame.mouse.get_pos()
                col = int(mousePos[0]/imSize)
                row = 7 - int(mousePos[1]/imSize)
                for p in self.pieces:
                    if p.row == row and p.col == col and p.color == turn:
                        return p
                
            pygame.display.update()
            clock.tick(10)
    
    def drawFinishedBoard(self,turn):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            gameDisplay.fill(white)
            for i in range(size):
                for j in range(size):
                    pygame.draw.rect(gameDisplay, (40*((i+j+1)%2) + 150,40*((i+j+1)%2)+150,40*((i+j+1)%2)+150), ((i*display_width/size,j*display_height/size),(display_width/size,display_height/size)))
            
            for p in self.pieces:
                self.drawPiece(p)
                    
            for i in range(size+1):
                pygame.draw.line(gameDisplay,black,(display_width/size*i,0),(display_width/size*i,display_height))
                pygame.draw.line(gameDisplay,black,(0,display_height/size*i),(display_width,display_height/size*i))
            
            if turn == Color.WHITE:
                center_message("White Won",black,size*imSize+15)
            else:
                center_message("Black Won",black,size*imSize+15)
                
            pygame.display.update()
            clock.tick(10)
    
    def drawThinking(self,turn):
        gameDisplay.fill(white)
        for i in range(size):
            for j in range(size):
                pygame.draw.rect(gameDisplay, (40*((i+j+1)%2) + 150,40*((i+j+1)%2)+150,40*((i+j+1)%2)+150), ((i*display_width/size,j*display_height/size),(display_width/size,display_height/size)))
        
        for p in self.pieces:
            self.drawPiece(p)
                
        for i in range(size+1):
            pygame.draw.line(gameDisplay,black,(display_width/size*i,0),(display_width/size*i,display_height))
            pygame.draw.line(gameDisplay,black,(0,display_height/size*i),(display_width,display_height/size*i))
        
        if turn == Color.WHITE:
            center_message("White is thinking",black,size*imSize+15)
        else:
            center_message("Black is thinking",black,size*imSize+15)
            
        pygame.display.update()
            
            
    def drawSelected(self,piece):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            
            for i in range(size):
                for j in range(size):
                    pygame.draw.rect(gameDisplay, (40*((i+j+1)%2) + 150,40*((i+j+1)%2)+150,40*((i+j+1)%2)+150), ((i*display_width/size,j*display_height/size),(display_width/size,display_height/size)))
            
            for p in self.pieces:
                self.drawPiece(p)
                    
            for i in range(size):
                pygame.draw.line(gameDisplay,black,(display_width/size*i,0),(display_width/size*i,display_height))
                pygame.draw.line(gameDisplay,black,(0,display_height/size*i),(display_width,display_height/size*i))
            
            pygame.draw.rect(gameDisplay, (220,220,220), ((piece.col*imSize+1,(7-piece.row)*imSize+1),(display_width/size-2,display_height/size-2)),2)
            
            moves = self.getLegalMoves(piece)
            
            self.drawMoves(piece.color,moves)
            
            if pygame.mouse.get_pressed()[0]:
                mousePos = pygame.mouse.get_pos()
                col = int(mousePos[0]/imSize)
                row = 7 - int(mousePos[1]/imSize)
                if [row,col] == [7,2] and piece.type == Type.KING and piece.color == Color.BLACK and "castlingBlackLeft" in moves:
                    self.movePiece(piece,"castlingBlackLeft")
                    return True
                elif [row,col] == [7,6] and piece.type == Type.KING and piece.color == Color.BLACK and "castlingBlackRight" in moves:
                    self.movePiece(piece,"castlingBlackRight")
                    return True
                elif [row,col] == [0,2] and piece.type == Type.KING and piece.color == Color.WHITE and "castlingWhiteLeft" in moves:
                    self.movePiece(piece,"castlingWhiteLeft")
                    return True
                elif [row,col] == [0,6] and piece.type == Type.KING and piece.color == Color.WHITE and "castlingWhiteRight" in moves:
                    self.movePiece(piece,"castlingWhiteRight")
                    return True
                elif [row,col] in moves:
                    if self.movePiece(piece,[row,col]):
                        piece.type = self.changePawn(piece.color)
                    return True
                elif [row,col] != [piece.row,piece.col]:
                    return False
            
            pygame.display.update()
            clock.tick(10)
    
    def changePawn(self,turn):
        while True:            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            gameDisplay.fill(white)
            for i in range(size):
                for j in range(size):
                    pygame.draw.rect(gameDisplay, (40*((i+j+1)%2) + 150,40*((i+j+1)%2)+150,40*((i+j+1)%2)+150), ((i*display_width/size,j*display_height/size),(display_width/size,display_height/size)))
            
            for p in self.pieces:
                self.drawPiece(p)
                    
            for i in range(size+1):
                pygame.draw.line(gameDisplay,black,(display_width/size*i,0),(display_width/size*i,display_height))
                pygame.draw.line(gameDisplay,black,(0,display_height/size*i),(display_width,display_height/size*i))
            
            center_message("Trade your pawn",black,size*imSize+15)
               
            pygame.draw.rect(gameDisplay, (220,220,220), ((2*imSize-2,(7-3)*imSize-2),(4*imSize+4,imSize+4)))
            pygame.draw.rect(gameDisplay, (0,0,0), ((2*imSize-2,(7-3)*imSize-2),(4*imSize+4,imSize+4)),2)                
            if turn == Color.BLACK:
                gameDisplay.blit(image_BQ,(2*imSize,(7-3)*imSize))
                gameDisplay.blit(image_BN,(3*imSize,(7-3)*imSize))
                gameDisplay.blit(image_BR,(4*imSize,(7-3)*imSize))
                gameDisplay.blit(image_BB,(5*imSize,(7-3)*imSize))
            else:
                gameDisplay.blit(image_WQ,(2*imSize,(7-3)*imSize))
                gameDisplay.blit(image_WN,(3*imSize,(7-3)*imSize))
                gameDisplay.blit(image_WR,(4*imSize,(7-3)*imSize))
                gameDisplay.blit(image_WB,(5*imSize,(7-3)*imSize))
            if pygame.mouse.get_pressed()[0]:
                mousePos = pygame.mouse.get_pos()
                col = int(mousePos[0]/imSize)
                row = 7 - int(mousePos[1]/imSize)
                if row == 3:
                    if col == 2:
                        return Type.QUEEN
                    elif col == 3:
                        return Type.KNIGHT
                    elif col == 4:
                        return Type.ROOK
                    elif col == 5:
                        return Type.BISHOP
            pygame.display.update()
            clock.tick(10)
    
    def getOptimalMove(self,turn):
        optimalMove = None
        for i in range(len(self.pieces)):
            p = self.pieces[i]
            if p.color == turn:
                moves = self.getLegalMoves(p)
                for m in moves:
                    moveValue = self.getMoveValue(turn,i,m,turn,1)
                    if optimalMove == None:
                        optimalPiece = p
                        optimalMove = m
                        optimalMoveValue = moveValue
                    elif moveValue > optimalMoveValue:
                        optimalPiece = p
                        optimalMove = m
                        optimalMoveValue = moveValue
                    elif moveValue == optimalMoveValue and random.randrange(10) > 7:
                        optimalPiece = p
                        optimalMove = m
                        optimalMoveValue = moveValue
        return (optimalPiece,optimalMove)
    
    def isQuiet(self,pieceNumber,move):
        return self.isEmpty(move[0],move[1])
        """
        quiet = self.isEmpty(move[0],move[1])
        if quiet:
            boardCopy = copy.deepcopy(self)
            if boardCopy.movePiece(boardCopy.pieces[pieceNumber],move):
                boardCopy.pieces[pieceNumber].type == Type.QUEEN
            m = boardCopy.getLegalMoves(boardCopy.pieces[pieceNumber])
            for mo in m:
                quiet = boardCopy.isEmpty(mo[0],mo[1])
                
                """
    
    def evaluateBoard(self,turn):
        value = 0
        for p in self.pieces:
            moves = self.getLegalMoves(p)
            if p.color == turn:
                    for m in moves:
                        for q in self.pieces:
                            if m==[q.row,q.col]:
                                if q.type == Type.QUEEN:
                                    value += 9
                                elif q.type == Type.ROOK:
                                    value += 5
                                elif q.type == Type.BISHOP or q.type == Type.KNIGHT:
                                    value += 3
                                else:
                                    value += 1
            else:
                for m in moves:
                    for q in self.pieces:
                        if m==[q.row,q.col]:
                            if q.type == Type.QUEEN:
                                value -= 90
                            elif q.type == Type.ROOK:
                                value -= 50
                            elif q.type == Type.BISHOP or q.type == Type.KNIGHT:
                                value -= 30
                            else:
                                value -= 10
                
            if p.type == Type.PAWN:
                if p.color == turn:
                    value += 100
                    value += len(moves)
                else:
                    value -= 100
                    value -= len(moves)
            elif p.type == Type.ROOK:
                if p.color == turn:
                    value += 500
                    value += len(moves)
                else:
                    value -= 500
                    value -= len(moves)
            elif p.type == Type.KNIGHT:
                if p.color == turn:
                    value += 300
                    value += len(moves)
                else:
                    value -= 300
                    value -= len(moves)
            elif p.type == Type.BISHOP:
                if p.color == turn:
                    value += 300
                    value += len(moves)
                else:
                    value -= 300
                    value -= len(moves)
            elif p.type == Type.QUEEN:
                if p.color == turn:
                    value += 900
                    value += len(moves)
                else:
                    value -= 900
                    value -= len(moves)
            elif p.type == Type.KING:
                if p.color == turn:
                    value -= 2*len(moves)
                else:
                    value += 2*len(moves)
                
        
        if self.gameOver(turn):
            value -= 100000
        
        return value
    
    def getMoveValue(self,origTurn,pieceNumber, move, turn, counter): 
        boardCopy = copy.deepcopy(self)
        if boardCopy.movePiece(boardCopy.pieces[pieceNumber],move):
            boardCopy.pieces[pieceNumber].type == Type.QUEEN
        notTurn = changeColor(turn)
        boardEval = boardCopy.evaluateBoard(notTurn)
        if counter == 0 or boardCopy.gameOver(notTurn) or self.isQuiet(pieceNumber,move):
            return -1*boardEval
        moveValues = []
        for i in range(len(boardCopy.pieces)):
            p = boardCopy.pieces[i]
            if p.color == notTurn:
                for m in boardCopy.getLegalMoves(p):
                    secondBoardCopy = copy.deepcopy(boardCopy)
                    if secondBoardCopy.movePiece(secondBoardCopy.pieces[i],m):
                        secondBoardCopy.pieces[i].type == Type.QUEEN
                    naiveMoveValue = secondBoardCopy.evaluateBoard(turn)
                    del(secondBoardCopy)
                    if abs(naiveMoveValue-boardEval) >= 150:
                        moveValues.append(boardCopy.getMoveValue(origTurn,i,m,notTurn,counter-1))
                    else:
                        moveValues.append(naiveMoveValue)
        if origTurn == turn:
            moveValues = [-x for x in moveValues]
        return min(moveValues)


brett = Board()
brett.play()
