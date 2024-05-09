# START OF FILE

from random import *
from GraphGames import *


'''
Kerry Ojakian (December 2019)

These are classes for playing and simulating cops and robbers.
It uses the collection of general classes from GraphGames.
'''

# ***************************************************************************
# ***************************************************************************
# *****             COP AND ROBBER GAME                                 *****
# ***************************************************************************
# ***************************************************************************

'''
Improvements in future:
    - Could make the random and ask-user strategy more generic, by
    making a Rules object an input to strategy, and it could give
    allowed-moves instead of all neighbors.
'''

class CopRobRules(Rules):

    def __init__(self, maxRounds):
        Rules.__init__(self, 2)
        self.numRounds = 0
        self.maxRounds = maxRounds


    def caught(self, cops, robber, pieceList):

        copPositions = pieceList.getPieces(0)
        robberPosition = pieceList.getPieces(1)

        for piece in robberPosition: # should be length 1 list for single robber
            robberLocation = piece.getLocation()

        for piece in copPositions:
            if piece.getLocation() == robberLocation:
                return piece.getID()

        # Otherwise, no cop has caught so return None
        return None
        

    # Over-riding empty gameStatus for Cops and Robbers
    def gameStatus(self, board, playerList, pieceList):
        
        cops = playerList[0]
        robber = playerList[1]

        if self.numRounds >= self.maxRounds:
            return 1 # robber win
        elif self.caught(cops, robber, pieceList) != None:
            return 0 # cop win
        else:
            return 'NOT_OVER'


    def update(self, playerMove):
        if playerMove.getPlayerNumber() == 1: # robber just moved
            self.numRounds += 1



class RandomStrategy(Strategy):

    def makeMove(self, playerNum, board, pieces, rules):
        'Moves to random neigbor'
        
        move = PlayerMove(playerNum)
        
        for piece in pieces:
            location = piece.getLocation()
            neighborList = board.getNeighbors(location)
            neighborIndex = randrange( len(neighborlist) )
            newLocation = neighborList[ neighborIndex ]
            piece.changeLocation( newLocation )
            move.addPieceMovement(piece, location, newLocation)

        return move
        


class AskUserStrategy(Strategy):

    def _movePiece(self, piece, board, move):

        location = piece.getLocation()

        if location == None:
            neighborList = board.getVertices()
            locationString = ' is not placed yet'
        else:
            neighborList = board.getNeighbors(location)
            locationString = ' is at ' + location

        pieceName = piece.getID() 

        while True:
            
            print(pieceName + locationString + '.  ', end = '')
            newLocation = input('Vertex to move to: ')
            
            if newLocation in neighborList:
                piece.changeLocation( newLocation )
                print(pieceName + ' moved to ' + newLocation + '.', end = '')
                move.addPieceMovement(piece, location, newLocation)
                break
            else:
                print('Invalid move! Try again.')


    def placePieces(self, playerNum, board, pieces, rules):

        move = PlayerMove()
        
        for piece in pieces:
            self._movePiece(piece, board, move)

        return move
    

    def makeMove(self, playerNum, board, pieces, rules):
        'Asks user where to move'

        move = PlayerMove()
        
        for piece in pieces:
            self._movePiece(piece, board, move)

        return move


class CopRobGame(Game):

    def __init__(self, board, numCops, copStrategy, robStrategy, maxRounds):

        # Create cop, player 0
        cop = Player(0, copStrategy)

        # Create robber, player 1
        robber = Player(1, robStrategy)

        # Create Piece List
        pieceList = PlayerPieceList(2)

        for i in range(numCops): # add numCops many cops
            copID = 'C' + str(i)
            pieceList.add(0, Piece(copID) )
            
        pieceList.addPiece(1, Piece('R')) # add one robber piece
        
        Game.__init__(board, CopRobberRules(maxRounds), [cop, robber], pieceList)
        


def testRandom():

    simpleBoard = Board()
    simpleBoard.createVertex('a')
    simpleBoard.createVertex('b')
    simpleBoard.createVertex('c')
    simpleBoard.createVertex('d')
    simpleBoard.createEdge('a', 'b')
    simpleBoard.createEdge('b', 'c')
    simpleBoard.createEdge('c', 'a')
    simpleBoard.createEdge('c', 'd') # Returns True
    simpleBoard.createEdge('d', 'c') # Returns False
    simpleBoard.display()

    robberStrategy = RandomStrategy()
    copStrategy = RandomStrategy()    
    
    simpleGame = CopRobGame(simpleBoard, robberStrategy, copStrategy, 2, 10)
    outcome = simpleGame.play()
    print(outcome)


def testAskUser():

    simpleBoard = Board()
    simpleBoard.createVertex('a')
    simpleBoard.createVertex('b')
    simpleBoard.createVertex('c')
    simpleBoard.createVertex('d')
    simpleBoard.createEdge('a', 'b')
    simpleBoard.createEdge('b', 'c')
    simpleBoard.createEdge('c', 'a')
    simpleBoard.createEdge('c', 'd') # Returns True
    simpleBoard.createEdge('d', 'c') # Returns False
    simpleBoard.display()

    robberStrategy = AskUserStrategy()
    copStrategy = AskUserStrategy()    
    
    simpleGame = CopRobGame(simpleBoard, robberStrategy, copStrategy, 2, 10)
    outcome = simpleGame.play()
    print(outcome)




# END OF FILE
