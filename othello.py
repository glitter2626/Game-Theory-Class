# -*- coding: utf-8 -*-

from bitarray import bitarray
import copy


EMPTY, BLACK, WHITE = '.', '@', 'O'
PIECES = (EMPTY, BLACK, WHITE)
PLAYERS = {BLACK: 'Black', WHITE: 'White'}

DOWN_MASK = bitarray('0') * 8 + bitarray('1') * 56
UP_MASK = bitarray('1') * 56 + bitarray('0') * 8 
RIGHT_MASK = bitarray('0111111101111111011111110111111101111111011111110111111101111111')
LEFT_MASK  = bitarray('1111111011111110111111101111111011111110111111101111111011111110')

SQUARES = [i for i in range(0, 64)]

SQUARE_WEIGHTS = [
     120, -20,  20,   5,   5,  20, -20, 120,   
     -20, -40,  -5,  -5,  -5,  -5, -40, -20,   
      20,  -5,  15,   3,   3,  15,  -5,  20,   
       5,  -5,   3,   3,   3,   3,  -5,   5,   
       5,  -5,   3,   3,   3,   3,  -5,   5,   
      20,  -5,  15,   3,   3,  15,  -5,  20,   
     -20, -40,  -5,  -5,  -5,  -5, -40, -20,   
     120, -20,  20,   5,   5,  20, -20, 120,   
]


class Othello:
    
    def __init__(self):
        self.whiteBB = bitarray(64)
        self.whiteBB[:] = 0
        self.whiteBB[28], self.whiteBB[35] = 1, 1
        
        self.blackBB = bitarray(64)
        self.blackBB[:] = 0
        self.blackBB[27], self.blackBB[36] = 1, 1
        
        self.legalBB = self.blackBB | self.whiteBB
        
    def leftshift(self, BB, count):
        return BB[count:] + (bitarray('0') * count)

    def rightshift(self, BB, count):
        return (bitarray('0') * count) + BB[:-count]
    
    def __str__(self):
        self.legalBB = self.whiteBB | self.blackBB
        strBB = "  "
        strBB += " ".join(map(str, range(0, 8))) + "\n"
        for i in range(0, 8):
            strBB += str(i) + " "
            for j in range(0, 8):   
                if self.legalBB[i * 8 + j] and self.whiteBB[i * 8 + j]:
                    strBB += WHITE + " "
                elif self.legalBB[i * 8 + j] and self.blackBB[i * 8 + j]:
                    strBB += BLACK + " "
                else:
                    strBB += EMPTY + " "
            strBB += "\n"
        return strBB
    
    def is_valid(self, move):
        return isinstance(move, int) and move in SQUARES
    
    def opponent(self, player):
        return BLACK if player is WHITE else WHITE
        
    def remain_squares(self, blackBB, whiteBB):
        placedBB = blackBB | whiteBB
        total = 0
        for i in SQUARES:
            if(placedBB[i] == False):
                total += 1
        return total
        
    def end_game(self, blackBB, whiteBB):
        black_score = 0
        white_score = 0
        for i in SQUARES:
            if blackBB[i]:
                black_score += 1
            if whiteBB[i]:
                white_score += 1
        
        if(black_score > white_score):
            print("Black Player Win!")
        elif(white_score > black_score):
            print("White Player Win!")
        else:
            print("Draw!")
        
    def evaluation(self, blackBB, whiteBB):
        total = 0
        for i in SQUARES:
            if blackBB[i]:
                total += SQUARE_WEIGHTS[i]
            elif whiteBB[i]:
                total -= SQUARE_WEIGHTS[i]
        return total
        
    def alpha_beta_pruning(self, blackBB, whiteBB, depth, alpha, beta, player):
        movelist = self.find_legalmove(blackBB, whiteBB, player)
        
        if (depth == 0) | (movelist == []):
            return self.evaluation(blackBB, whiteBB), None
            
        if(player == BLACK):
            value1 = alpha
            move1 = None
            for i in movelist:
                blackBB_cp = copy.deepcopy(blackBB)
                whiteBB_cp = copy.deepcopy(whiteBB)
                blackBB_cp[i] = 1
                value2, move2 = self.alpha_beta_pruning(blackBB_cp, whiteBB_cp, depth-1, value1, beta, WHITE)
                
                if value2 > value1:
                    value1 = value2
                    move1 = i
                
                if value1 >= beta:
                    break
            return value1, move1
            
        else:
            value1 = beta
            move1 = None
            for i in movelist:
                blackBB_cp = copy.deepcopy(blackBB)
                whiteBB_cp = copy.deepcopy(whiteBB)
                whiteBB_cp[i] = 1
                value2, move2 = self.alpha_beta_pruning(blackBB_cp, whiteBB_cp, depth-1, alpha, value1, BLACK)
                
                if value2 < value1:
                    value1 = value2
                    move1 = i
                
                if value1 <= alpha:
                    break
            return value1, move1
                    
        
        
    
    def find_legalmove(self, blackBB, whiteBB, player):
        legalmove = 64 * bitarray('0')
        curBB = blackBB if player is BLACK else whiteBB
        oppBB = whiteBB if player is BLACK else blackBB
        eptBB = ~(curBB | oppBB)
        
        #DOWN
        potentialmove = self.rightshift(curBB, 8) & DOWN_MASK & oppBB
        
        while potentialmove.any():
            tmp = self.rightshift(potentialmove, 8) & DOWN_MASK
            legalmove |= tmp & eptBB
            potentialmove = tmp & oppBB
            
        #UP
        potentialmove = self.leftshift(curBB, 8) & UP_MASK & oppBB
        
        while potentialmove.any():
            tmp = self.leftshift(potentialmove, 8) & UP_MASK
            legalmove |= tmp & eptBB
            potentialmove = tmp & oppBB
            
        #LEFT
        potentialmove = self.leftshift(curBB, 1) & LEFT_MASK & oppBB
        
        while potentialmove.any():
            tmp = self.leftshift(potentialmove, 1) & LEFT_MASK
            legalmove |= tmp & eptBB
            potentialmove = tmp & oppBB
            
        #RIGHT
        potentialmove = self.rightshift(curBB, 1) & RIGHT_MASK & oppBB
        
        while potentialmove.any():
            tmp = self.rightshift(potentialmove, 1) & RIGHT_MASK
            legalmove |= tmp & eptBB
            potentialmove = tmp & oppBB
            
        #DOWN RIGHT
        potentialmove = self.rightshift(curBB, 9) & DOWN_MASK & RIGHT_MASK & oppBB
        
        while potentialmove.any():
            tmp = self.rightshift(potentialmove, 9) & DOWN_MASK & RIGHT_MASK
            legalmove |= tmp & eptBB
            potentialmove = tmp & oppBB
            
        #DOWN LEFT
        potentialmove = self.rightshift(curBB, 7) & DOWN_MASK & LEFT_MASK & oppBB
        
        while potentialmove.any():
            tmp = self.rightshift(potentialmove, 7) & DOWN_MASK & LEFT_MASK
            legalmove |= tmp & eptBB
            potentialmove = tmp & oppBB
            
        #UP RIGHT
        potentialmove = self.leftshift(curBB, 7) & UP_MASK & RIGHT_MASK & oppBB
        
        while potentialmove.any():
            tmp = self.leftshift(potentialmove, 7) & UP_MASK & RIGHT_MASK
            legalmove |= tmp & eptBB
            potentialmove = tmp & oppBB
            
        #UP LEFT
        potentialmove = self.leftshift(curBB, 9) & UP_MASK & LEFT_MASK & oppBB
        
        while potentialmove.any():
            tmp = self.leftshift(potentialmove, 9) & UP_MASK & LEFT_MASK
            legalmove |= tmp & eptBB
            potentialmove = tmp & oppBB
            
        movepos = [i for i in SQUARES if legalmove[i] ]
        
        return movepos
    
    def make_move(self, blackBB, whiteBB, pos, player):
        curBB = blackBB if player is BLACK else whiteBB
        oppBB = whiteBB if player is BLACK else blackBB
        posBB = bitarray('0') * 64
        posBB[pos] = 1
        endpos = bitarray('0') * 64
        flipBB = bitarray('0') * 64
        legalmove = self.find_legalmove(blackBB, whiteBB, player)

        if self.is_valid(pos) and pos in legalmove:        
            curBB[pos] = 1
        else:
            print("Can't move to position %d" % pos)
            return False
        
        #DOWN
        potentialmove = self.rightshift(posBB, 8) & DOWN_MASK & oppBB
        
        while potentialmove.any():
            tmp = self.rightshift(potentialmove, 8) & DOWN_MASK
            endpos |= tmp & curBB
            potentialmove = tmp & oppBB
            
        while endpos.any():
            endpos = self.leftshift(endpos, 8) & UP_MASK & oppBB
            if endpos.any():
                flipBB |= endpos
            else:
                break
            
        #UP
        potentialmove = self.leftshift(posBB, 8) & UP_MASK & oppBB
        
        while potentialmove.any():
            tmp = self.leftshift(potentialmove, 8) & UP_MASK
            endpos |= tmp & curBB
            potentialmove = tmp & oppBB
            
        while endpos.any():
            endpos = self.rightshift(endpos, 8) & DOWN_MASK & oppBB
            if endpos.any():
                flipBB |= endpos
            else:
                break
            
        #RIGHT
        potentialmove = self.rightshift(posBB, 1) & RIGHT_MASK & oppBB
        
        while potentialmove.any():
            tmp = self.rightshift(potentialmove, 1) & RIGHT_MASK
            endpos |= tmp & curBB
            potentialmove = tmp & oppBB
            
        while endpos.any():
            endpos = self.leftshift(endpos, 1) & LEFT_MASK & oppBB
            if endpos.any():
                flipBB |= endpos
            else:
                break
            
        #LEFT
        potentialmove = self.leftshift(posBB, 1) & LEFT_MASK & oppBB
        
        while potentialmove.any():
            tmp = self.leftshift(potentialmove, 1) & LEFT_MASK
            endpos |= tmp & curBB
            potentialmove = tmp & oppBB
            
        while endpos.any():
            endpos = self.rightshift(endpos, 1) & RIGHT_MASK & oppBB
            if endpos.any():
                flipBB |= endpos
            else:
                break
            
        #DOWN RIGHT
        potentialmove = self.rightshift(posBB, 9) & DOWN_MASK & RIGHT_MASK & oppBB
        
        while potentialmove.any():
            tmp = self.rightshift(potentialmove, 9) & DOWN_MASK & RIGHT_MASK
            endpos |= tmp & curBB
            potentialmove = tmp & oppBB
            
        while endpos.any():
            endpos = self.leftshift(endpos, 9) & UP_MASK & LEFT_MASK & oppBB
            if endpos.any():
                flipBB |= endpos
            else:
                break
            
        #DOWN LEFT
        potentialmove = self.rightshift(posBB, 7) & DOWN_MASK & LEFT_MASK & oppBB
        
        while potentialmove.any():
            tmp = self.rightshift(potentialmove, 7) & DOWN_MASK & LEFT_MASK
            endpos |= tmp & curBB
            potentialmove = tmp & oppBB
            
        while endpos.any():
            endpos = self.leftshift(endpos, 7) & UP_MASK & RIGHT_MASK & oppBB
            if endpos.any():
                flipBB |= endpos
            else:
                break
            
        #UP RIGHT
        potentialmove = self.leftshift(posBB, 7) & UP_MASK & RIGHT_MASK & oppBB
        
        while potentialmove.any():
            tmp = self.leftshift(potentialmove, 7) & UP_MASK & RIGHT_MASK
            endpos |= tmp & curBB
            potentialmove = tmp & oppBB
            
        while endpos.any():
            endpos = self.rightshift(endpos, 7) & DOWN_MASK & LEFT_MASK & oppBB
            if endpos.any():
                flipBB |= endpos
            else:
                break
            
        #UP LEFT
        potentialmove = self.leftshift(posBB, 9) & UP_MASK & LEFT_MASK & oppBB
        
        while potentialmove.any():
            tmp = self.leftshift(potentialmove, 9) & UP_MASK & LEFT_MASK
            endpos |= tmp & curBB
            potentialmove = tmp & oppBB
            
        while endpos.any():
            endpos = self.rightshift(endpos, 9) & DOWN_MASK & RIGHT_MASK & oppBB
            if endpos.any():
                flipBB |= endpos
            else:
                break
            
        curBB |= flipBB
        oppBB &= ~flipBB
        
        return True

        
depth = 7
game = Othello()
black_pass = False
white_pass = False

while True:
    #Black Player Move
    print("Black Player Turn.")
    if game.find_legalmove(game.blackBB, game.whiteBB, BLACK) == []:
        black_pass = True
        if white_pass:
            game.end_game(game.blackBB, game.whiteBB)
            break
    else:
        black_pass = False
    
    if black_pass == False:
        if game.remain_squares(game.blackBB, game.whiteBB) < 20:
            depth = 10    
        value, pos = game.alpha_beta_pruning(game.blackBB, game.whiteBB, depth, -99999, 99999, BLACK)
        game.make_move(game.blackBB, game.whiteBB, pos, BLACK)
        print(game)
    else:
        print("Black Player doesnt have legal move, Pass.")
        
    #White Player Move 
    print("White Player Turn.")
    if game.find_legalmove(game.blackBB, game.whiteBB, WHITE) == []:
        white_pass = True
        if black_pass:
            game.end_game(game.blackBB, game.whiteBB)
            break
    else:
        white_pass = False
    
    if white_pass == False:
        pos = input(">Input:")
        while game.make_move(game.blackBB, game.whiteBB, int(pos), WHITE) == False:
            pos = input(">Input:")
        print(game)
    else:
        print("White Player doesnt have legal move, Pass.")
    
    