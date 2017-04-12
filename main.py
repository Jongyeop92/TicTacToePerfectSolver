# -*- coding: utf8 -*-

import pickle
import copy


EMPTY = '_'
X     = 'X'
O     = 'O'


class Position:

    def __init__(self):
        self.WIDTH     = 3
        self.HEIGHT    = 3
        self.WIN_COUNT = 3

        self.moves  = 0
        self.directionPairList = [[(-1, 0), ( 1,  0)],
                                  [(-1, 1), ( 1, -1)],
                                  [( 0, 1), ( 0, -1)],
                                  [( 1, 1), (-1, -1)]]

        self.board = [[EMPTY, EMPTY, EMPTY],
                      [EMPTY, EMPTY, EMPTY],
                      [EMPTY, EMPTY, EMPTY]]

    def canPlay(self, y, x):
        return self.board[y][x] == EMPTY

    def play(self, y, x, color):
        self.board[y][x] = color
        self.moves += 1

    def playList(positionList):
        for y, x, color in positionList:
            self.play(y, x)

    def isWinningMove(self, y, x, color):
        for directionPair in self.directionPairList:
            sameCount = 1
            for direction in directionPair:
                dy, dx = direction
                nowY, nowX = y, x

                while self.isInBoard(nowY + dy, nowX + dx):
                    nowY += dy
                    nowX += dx

                    if self.board[nowY][nowX] == color:
                        sameCount += 1
                    else:
                        break

            if sameCount == self.WIN_COUNT:
                return True

        return False

    def isInBoard(self, y, x):
        return 0 <= y and y < self.HEIGHT and 0 <= x and x < self.WIDTH

    def key(self):
        return ''.join(''.join(row) for row in self.board)


def saveObject(obj, fileName):
    with open(fileName, "wb") as f:
        pickle.dump(obj, f)


def loadObject(fileName):
    with open(fileName, "rb") as f:
        return pickle.load(f)


def negamax(p, nowColor, nextColor):

    if tt.get(p.key()) != None:
        return tt[p.key()]

    if p.moves == p.WIDTH * p.HEIGHT:
        return [(0, None)]

    for y in range(p.HEIGHT):
        for x in range(p.WIDTH):
            if p.canPlay(y, x) and p.isWinningMove(y, x, nowColor):
                return [((p.WIDTH * p.HEIGHT + 1 - p.moves) / 2, (y, x))]

    bestScore = -p.WIDTH * p.HEIGHT
    bestMove = None

    resultList = []

    for y in range(p.HEIGHT):
        for x in range(p.WIDTH):
            if p.canPlay(y, x):
                copyP = copy.deepcopy(p)
                copyP.play(y, x, nowColor)

                score, move = max(negamax(copyP, nextColor, nowColor))

                resultList.append((-score, (y, x)))

                if(-score > bestScore):
                    bestScore = -score
                    bestMove = move
            else:
                resultList.append(None)

    if tt.get(p.key()) == None:
        tt[p.key()] = resultList

    return resultList


def test():

    p = Position()

    assert p.board == [[EMPTY, EMPTY, EMPTY],
                       [EMPTY, EMPTY, EMPTY],
                       [EMPTY, EMPTY, EMPTY]]

    assert p.canPlay(0, 0) == True
    assert p.canPlay(2, 2) == True

    p.play(0, 0, X)
    assert p.canPlay(0, 0) == False
    assert p.key() == X + EMPTY * 8

    p.play(0, 1, X)
    p.play(1, 0, X)
    assert p.isWinningMove(0, 2, X) == True
    assert p.isWinningMove(2, 0, X) == True
    assert p.isWinningMove(1, 1, X) == False

    p2 = Position()
    print negamax(p2, X, O)
    

    print "Success"


ttFileName = "tictactoe_tt"

try:
    tt = loadObject(ttFileName)
except:
    tt = {}

def main():

    p = Position()

    print negamax(p, X, O)

    saveObject(tt, ttFileName)


if __name__ == "__main__":
    #test()
    main()
