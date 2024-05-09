# START OF FILE

# I USED PIP TO INSTALL.
# FROM: https://networkx.github.io/
from networkx import *


'''
Kerry Ojakian (December 2019)

This is general platform for simulating graph games.
Many classes here are intended as abstract classes.  Child
classes should typically be made when applied to specific games.
'''


# ***************************************************************************
# ***************************************************************************
# *****             START OF GENERIC ABSTRACT CLASSES                   *****
# ***************************************************************************
# ***************************************************************************

'''
***** SOME GENERAL REMARKS *****
We will have players numbered 0, 1, ..., N-1, where N = number of players.
A player list will refer to a list of Player objects.
A piece list will refer to a PlayerPieceList object.
We say that a player list and a piece list 'correspond' if:
    - they are the same length, and
    - position i in both refers to player number i
'''


class Game:
    '''
    This class runs the play and simulation of the game, assuming the
    board, rules, and players (with their strategies) are set up.
    '''

    def __init__(self, board, rules, playerList, pieceList):
        self.board = board
        self.rules = rules
        self.playerList = playerList
        self.playerPieces = pieceList
        numPlayers = len( self.playerList )


    def play(self):
        'Basic play simulation which just gives end result for efficiency'
    
        # Initial placement
        for player in self.playerList:
            playerMove = player.placePieces(self.board, self.pieceList, self.rules)
            self.rules.update( playerMove )
            
        # Play rounds
        playerTurn = 0
        gameStatus = self.rules.gameStatus(self.board, self.playerList, self.playerPieces)
        while gameStatus == 'NOT_OVER':
            currentPlayer = self.playerList[playerTurn]
            playerMove = currentPlayer.makeMove(self.board, self.playerPieces, self.rules)
            self.rules.update( playerMove )
            gameStatus = self.rules.gameStatus(self.board, self.playerList, self.playerPieces)
            playerTurn = (playerTurn + 1) % numPlayers

        return gameStatus


    # Q: WAY TO EFFICIENTLY PUT IF IN LOOP FOR MORE INVOLVED MODE.
    # SHOULD UPDATE ...
    '''
    def playDetailed(self):
        'Play simulation which gives end result and the play sequence'

        playSequence = []

        # Initial placement
        for player in playerList:
            player.placePieces(self.board):
            # could put in class sequence of initial move?

        # Play rounds
        playerTurn = 0
        numPlayers = len(playerList)
        while self.rules.gameStatus(self.board, self.playerList) == 'NOT_OVER':
            currentPlayer = self.playerList[playerTurn]
            startPosition = currentPlayer.getPosition()
            currentPlayer.makeMove(self.board)
            endPosition = currentPlayer.getPosition()
            playSequence.append( (playerTurn, startPosition, endPosition) )
            playerTurn = (playerTurn + 1) % numPlayers

        return self.rules.gameStatus(self.board, self.playerList), \
               playSequence
    '''
   

        

class Piece:
    'Stores info for an individual player piece'

    def __init__(self, ID):
        self.ID = ID
        self.location = None


    def getID(self):
        return self.ID


    def getLocation(self):
        return self.location


    def changeLocation(self, newLoc):
        self.location = newLoc



class PlayerPieceList:
    '''
    Stores all player piece info.
    If there are N players, the players are reference by numbers 0, 1, ..., N-1
    '''

    def __init__(self, numPlayers):
        self.pieceSets = [set()] * numPlayers


    def addPiece(self, playerNum, piece):
        self.pieceSets[ playerNum ].add( piece )


    def getPieces(self, playerNum):
        return self.pieceSets[ playerNum ]


    def display(self):
        positionSet = set()
        for playerNum in range( len( self.pieceSets ) ):
            print('Player ' + str(playerNum) + ': ', end = '')
            print(self.pieceSets[ playerNum ])
        

    
class Board:
    'The board on which the game is played'
    
    def __init__(self):
        self.graph = Graph()
    

    def createVertex(self, nodeName):
        self.graph.add_node(nodeName)


    def createEdge(self, a, b):
        'Adds edge and returns True if both vertices are in the graph. False otherwise'
        if a in self.graph.nodes and b in self.graph.nodes:
            self.graph.add_edge(a, b)
            return True
        else:
            return False


    def getVertices(self):
        return self.graph.nodes


    def getNeighbors(self, x):
        'Returns the neighbors of vertex x as a list'
        return list(self.graph[x].keys())
        

    def display(self):
        print("Vertices: ", end ='')
        print(self.graph.nodes)
        print("Edges: ", end ='')
        print(self.graph.edges)



class Rules:
    '''
    For now, just used for game status check.
    Later it could vet a strategy by going throught the polynomially many possibilities
    before game play.
    '''

    def __init__(self, numPlayers):
        self.numPlayers = numPlayers


    def gameStatus(self, board, playerList, pieceList):
        #Child class should specify!!
        '''
        Input: Board and list of Players and a PlayerPieces.
        The list of Players and the piece list of PlayerPieces correspond.
        Output: Status of the game, indicated as follows
           'NOT_OVER' if no winner
           'DRAW' if the game is over with no winner
           The integer of the winning player (if there is a winner) 
        '''

        # Default return that should be over-ridden in child class
        return 'NOT_OVER' 


    def update(playerMove):
        # Child class can update to make any modifications based on player moves.
        pass


class PlayerMove:
    'Stores info for the move of a player'
    
    def __init__(self, playerNum):
        self.playerNumber = playerNum
        self.moves = []


    def addPieceMovement(self, piece, startVertex, endVertex):
        self.moves.append( [piece, startVertex, endVertex] )


    def getPlayerNum(self):
        return self.playerNumber
    

    def getMoves(self):
        return self.moves



class Strategy:
    '''
    This is an object which stores a player strategy.
    Should follow rules of the game (though is not currently formally enforced).
    Later, could have Rules object vet a strategy prior to play,
    rather than during, for efficiency reasons.

    A particular instance could do placePieces and makeMove as same method,
    but separated for possible efficiency reasons.
    '''

    def __init__(self):
        pass


    def placePieces(self, playerNumber, board, pieces, rules):
        # Child class should specify!!
        '''
        Input: Board and list of pieces
        Output: PlayerMove object
        Modifies the pieces in the list in accordance with the strategy,
        to place at their initial positions.
        '''
        
        return PlayerMove(playerNumber)
    

    def makeMove(self, playerNumber, board, pieces, rules):
        # Child class should specify!!
        '''
        Input: Board and list of pieces
        No output.
        Modifies the pieces in the list in accordance with the strategy.
        '''

        return PlayerMove(playerNumber)



class Player:

    def __init__(self, playerNum, strategy):
        '''
        The player number should be a number between 0 and N-1, where N = number of players.
        The player number should correspond to this players pieces in some externally
        stored pieces list.
        '''
        
        self.playerNumber = playerNum
        self.strategy = strategy


    def placePieces(self, board, pieceList, rules):
        playerMove = self.strategy.placePieces(self.playerNumber, board, pieceList, rules)
        rules.update(playerMove)
        return playerMove


    def makeMove(self, board, pieceList, rules):
        playerMove = self.strategy.makeMove(self.playerNumber, board, pieceList, rules)
        rules.update(playerMove)
        return playerMove



# ***************************************************************************
# ***************************************************************************
# *****             END OF GENERIC ABSTRACT CLASSES                     *****
# ***************************************************************************
# ***************************************************************************

# END OF FILE
