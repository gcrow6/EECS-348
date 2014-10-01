from time import time
from copy import deepcopy
class SexyBeards:

    def __init__(self):
        self.board = [[' ']*8 for i in range(8)]
        self.size = 8
        self.board[4][4] = 'W'
        self.board[3][4] = 'B'
        self.board[3][3] = 'W'
        self.board[4][3] = 'B'
        # a list of unit vectors (row, col)
        self.moveCount = 4
        self.firstPlayer = None
        self.directions = [ (-1,-1), (-1,0), (-1,1), (0,-1),(0,1),(1,-1),(1,0),(1,1)]
        self.openingMoveList = []
#prints the boards
    def PrintBoard(self):

        # Print column numbers
        print("  ",end="")
        for i in range(self.size):
            print(i+1,end=" ")
        print()

        # Build horizontal separator
        linestr = " " + ("+-" * self.size) + "+"

        # Print board
        for i in range(self.size):
            print(linestr)                       # Separator
            print(i+1,end="|")                   # Row number
            for j in range(self.size):
                print(self.board[i][j],end="|")  # board[i][j] and pipe separator 
            print()                              # End line
        print(linestr)

#checks every direction fromt the position which is input via "col" and "row", to see if there is an opponent piece
#in one of the directions. If the input position is adjacent to an opponents piece, this function looks to see if there is a
#a chain of opponent pieces in that direction, which ends with one of the players pieces.    
    def islegal(self, row, col, player, opp):
        if(self.get_square(row,col)!=" "):
            return False
        for Dir in self.directions:
            for i in range(self.size):
                if  ((( row + i*Dir[0])<self.size)  and (( row + i*Dir[0])>=0 ) and (( col + i*Dir[1])>=0 ) and (( col + i*Dir[1])<self.size )):
                    #does the adjacent square in direction dir belong to the opponent?
                    if self.get_square(row+ i*Dir[0], col + i*Dir[1])!= opp and i==1 : #no
                        #no pieces will be flipped in this direction, so skip it
                        break
                    #yes the adjacent piece belonged to the opponent, now lets see if there are a chain
                    #of opponent pieces
                    if self.get_square(row+ i*Dir[0], col + i*Dir[1])==" " and i!=0 :
                        break

                    #with one of player's pieces at the other end
                    if self.get_square(row+ i*Dir[0], col + i*Dir[1])==player and i!=0 and i!=1 :
                        #set a flag so we know that the move was legal
                        return True
        return False
        
#returns true if the square was played, false if the move is not allowed
    def place_piece(self, row, col, player, opp):
        if(self.get_square(row,col)!=" "):
            return False
        
        if(player == opp):
            print("player and opponent cannot be the same")
            return False
        
        legal = False
        #for each direction, check to see if the move is legal by seeing if the adjacent square
        #in that direction is occuipied by the opponent. If it isnt check the next direction.
        #if it is, check to see if one of the players pieces is on the board beyond the oppponents piece,
        #if the chain of opponents pieces is flanked on both ends by the players pieces, flip
        #the opponents pieces 
        for Dir in self.directions:
            #look across the length of the board to see if the neighboring squares are empty,
            #held by the player, or held by the opponent
            for i in range(self.size):
                if  ((( row + i*Dir[0])<self.size)  and (( row + i*Dir[0])>=0 ) and (( col + i*Dir[1])>=0 ) and (( col + i*Dir[1])<self.size )):
                    #does the adjacent square in direction dir belong to the opponent?
                    if self.get_square(row+ i*Dir[0], col + i*Dir[1])!= opp and i==1 : # no
                        #no pieces will be flipped in this direction, so skip it
                        break
                    #yes the adjacent piece belonged to the opponent, now lets see if there are a chain
                    #of opponent pieces
                    if self.get_square(row+ i*Dir[0], col + i*Dir[1])==" " and i!=0 :
                        break

                    #with one of player's pieces at the other end
                    if self.get_square(row+ i*Dir[0], col + i*Dir[1])==player and i!=0 and i!=1 :
                        #set a flag so we know that the move was legal
                        legal = True
                        self.flip_tiles(row, col, Dir, i, player)
                        break
        return legal

#Places piece of opponent's color at (row,col) and then returns 
#  the best move, determined by the make_move(...) function
    def play_square(self, row, col, playerColor, oppColor):        
        # Place a piece of the opponent's color at (row,col)
        if ((row,col) != (-1,-1)):
            self.place_piece(row,col,oppColor,playerColor)
            self.moveCount+=1;
        
        # Determine best move and and return value to Matchmaker
        move = -1
        if(self.moveCount<=8):
            move = self.opening_moves(playerColor, oppColor, row,col)
        if(move == -1):
            print(self.moveCount)
            if(self.moveCount <= 14 or self.moveCount >=40 or len(self.legal_moves(playerColor, oppColor))<=5):
                move = self.alphabeta(playerColor, oppColor, time(),4)
            else:
                move = self.alphabeta(playerColor, oppColor, time(),3)
        print(move)
        if((move[0],move[1])!=(-1,-1)):
            self.place_piece(move[0], move[1],playerColor, oppColor)
            self.moveCount+=1
        print(self.evaluate(playerColor, oppColor))
        return move

#sets all tiles along a given direction (Dir) from a given starting point (col and row) for a given distance
# (dist) to be a given value ( player )
    def flip_tiles(self, row, col, Dir, dist, player):
        for i in range(dist):
            self.board[row+ i*Dir[0]][col + i*Dir[1]] = player
        return True
    
#returns the value of a square on the board
    def get_square(self, row, col):
        return self.board[row][col]
    
    def legal_moves(self, playerColor, oppColor):
        moves = []
        for row in range(self.size):
            for col in range(self.size):
                if(self.islegal(row, col, playerColor, oppColor)):
                    moves.append((row,col))
        return moves
    
    
    def game_over(self, playerColor, oppColor):
        if (self.moves == 64 or self.all_pieces(playerColor, oppColor)):
            return True
        return False
    
    def all_pieces(self,player,opp):
        playerC = None
        for i in range(self.size):
            for j in range(self.size):
                if(playerC!= None and self.get_square(i,j)!=playerC and self.get_square(i, j) != " "): 
                    return False
                if(self.get_square(i,j) != " " and playerC== None):
                    playerC = self.get_square(i,j)
                    
    def alphabeta(self, player, opp, mytime, depth):
        max_score = -10000000000
        max_move = (-1,-1)
        
        moves = self.legal_moves(player,opp)
        moves = self.reorder_moves(moves)
        print("ordered moves:",moves)
        for move in moves:
            temp_board = deepcopy(self)
            temp_board.place_piece(move[0],move[1], player, opp)
            
            best = temp_board.minimize(player, opp, mytime, depth, max_score)
            print(move,":", best)
            if(best > max_score):
                max_score = best
                max_move = move
            if(time() - mytime >= 14): #some threshold for when we are running out of time.
                break
        print("best move score:", max_score)
        return max_move
    
    def minimize(self, player,  opp, mytime, depth, alpha):
        min_score = 100000000000
        if((depth==0) or ((time() - mytime) >=14)):
            min_score = self.evaluate(player, opp)
            return min_score
        if((self.legal_moves(opp,player) == [])):
            return self.maximize(player, opp, mytime, depth-1, min_score)
        
        moves = self.reorder_moves(self.legal_moves(opp,player))
        for move in moves:
            if((time() - mytime) >=14):
                return -10000000000
            temp_board = deepcopy(self)
            temp_board.place_piece(move[0], move[1], opp, player)
            score = temp_board.maximize(player,opp,mytime,depth-1,min_score)
            if (score < min_score):
                min_score = score
                if(score<alpha):
                    return min_score
        #print("min value found", min_score)
        return min_score

    def maximize(self, player, opp, mytime, depth, beta):
        max_score = -10000000000
        if((depth==0) or ((time() - mytime) >=14)):
            max_score = self.evaluate(player, opp)
            return max_score
        if(self.legal_moves(player,opp)==[]):
            return self.minimize(player,opp,mytime,depth-1,max_score)
        
       
        moves = self.reorder_moves(self.legal_moves(player,opp))
        for move in moves:
            if((time() - mytime) >=14):
                return -100000000000000
            temp_board = deepcopy(self)
            temp_board.place_piece(move[0], move[1], player, opp)
            score = temp_board.minimize(player,opp,mytime,depth-1,max_score)
            if (score > max_score):
                max_score = score
                if(score>beta):
                    return max_score
        #print("max value found", max_score)
        return max_score
       
    def opening_moves(self, player, opp, orow, ocol):
        if(self.firstPlayer == None and ((orow,ocol) == (-1,-1))):
            self.firstPlayer = True
        if (self.firstPlayer):
            if(player == "W"):
                opp_play= (orow, 7-ocol)
            else:
                opp_play = (orow, ocol)
            self.openingMoveList.append(opp_play)
            if(self.moveCount >=4):
                if(self.moveCount >=6):
                    if(self.moveCount >=8):
                        if(opp_play == (2,4)):
                            play =(3,5)
                        elif(opp_play == (4,2)):
                            play= (3,1)
                        elif(opp_play == (3,1)):
                            play= (2,5)
                        elif(opp_play == (5,4)):
                            play= (4,5)
                        else:
                            return -1#just minimax
                    if(opp_play == (2,2)):
                        play= (2,3)
                    elif(opp_play == (2,4)):
                        play= (5,5)
                    elif(opp_play == (4,2)):
                        play= (5,3)
                else:
                    play = (3, 2)
            if(player == "W"):
                myplay = (play[0], 7-play[1])
                play = myplay
        else:
            if(player == "B"):
                opp_play= (orow, 7-ocol)
            else:
                opp_play = (orow, ocol)
            self.openingMoveList.append(opp_play)
            if(self.moveCount >=5):
                if(self.moveCount >=7):
                    if(self.openingMoveList[0] ==(3,2)):
                        if(opp_play ==(4,5)):
                            play = (3,1)
                        elif (opp_play == (5, 5)):
                            play = (5, 4)
                        else:
                            return -1#just minimax
                    if(self.openingMoveList[0] ==(2,3)):
                        if(opp_play ==(5,4)):
                            play = (1,3)
                        elif (opp_play == (5, 5)):
                            play = (4, 5)
                        else:
                            return -1#just minimax
                        
                    if(self.openingMoveList[0] ==(5,4)):
                        if(opp_play ==(2,2)):
                            play = (3,2)
                        elif (opp_play == (2, 3)):
                            play = (6, 4)
                        else:
                            return -1#just minimax
                    if(self.openingMoveList[0] ==(4,5)):
                        if(opp_play ==(2,2)):
                            play = (2,3)
                        elif (opp_play == (3, 2)):
                            play = (4, 6)
                        else:
                            return -1#just minimax
                if(opp_play == (3,2)):
                    play = (2, 4)
                if(opp_play == (2,3)):
                    play = (4, 2)
                if(opp_play == (5,4)):
                    play = (3, 5)
                if(opp_play == (4,5)):
                    play = (5, 3)
            if(player == "B"):
                myplay = (play[0], 7-play[1])
                play = myplay
        return play
       
    def evaluate(self, player, opp):
        player_score  = 0;
        opp_score = 0;    
        square_weights = [
                  [ 500, -100, 100,  3,  3, 100, -100,  500],
                  [-100, -200,  -2, -2, -2,  -2, -200, -100],
                  [ 100,   -2,  80,  1,  1,  80,   -2,  100],
                  [   3,   -2,   1,  1,  1,   1,   -2,    3],
                  [   3,   -2,   1,  1,  1,   1,   -2,    3],
                  [ 100,   -2,  80,  1,  1,  80,   -2,  100],
                  [-100, -200,  -2, -2, -2,  -2, -200, -100],
                  [ 500, -100, 100,  3,  3, 100, -100,  500]]
        for row in range(self.size):
            for col in range(self.size):
                if (self.board[row][col]==player):
                    player_score += square_weights[row][col]  
                if (self.board[row][col]==opp):
                    opp_score += square_weights[row][col]  
        
        #print("our board score:",player_score)
        #print("their board score:",opp_score)             
        player_score += 50 * len(self.legal_moves(player,opp))
        opp_score += 50 * len(self.legal_moves(opp,player))
        #print("our mobility score:", 100*len(self.legal_moves(player,opp)))
        #print("their mobility score:",100*len(self.legal_moves(opp,player)))
        player_score += (0.33 * (self.count_pieces(player) / (self.moveCount)) * (2 ** (self.moveCount/4)))
        opp_score += (0.33 * self.count_pieces(opp) / (self.moveCount) * (2 ** (self.moveCount/4)))
        #print("our piece score:",0.01 * (self.count_pieces(player) / (self.moveCount + 4)) * (2 ** (self.moveCount/4)))
        #print("their piece score:",0.01 * self.count_pieces(opp) / (self.moveCount + 4) * (2 ** (self.moveCount/4)))
        #print("our score", player_score)
        #print("their score",opp_score)
        #print("final score", player_score-opp_score)
        return (player_score - opp_score)
    
    
    def count_pieces(self, player):
        count = 0
        for i in range(self.size):
            for j in range(self.size):
                if (self.board[i][j]==player):
                    count+=1
        return count
    
    def reorder_moves(self, moves):
        square_weights =[
                  [ 500, -100, 100,  3,  3, 100, -100,  500],
                  [-100, -200,  -2, -2, -2,  -2, -200, -100],
                  [ 100,   -2,  80,  1,  1,  80,   -2,  100],
                  [   3,   -2,   1,  1,  1,   1,   -2,    3],
                  [   3,   -2,   1,  1,  1,   1,   -2,    3],
                  [ 100,   -2,  80,  1,  1,  80,   -2,  100],
                  [-100, -200,  -2, -2, -2,  -2, -200, -100],
                  [ 500, -100, 100,  3,  3, 100, -100,  500]]
        best_moves = []
        for move in moves:
            best_moves.append((move, square_weights[move[0]][move[1]]))
        return [a[0] for a in sorted(best_moves, key=lambda move: move[1], reverse=True)]

