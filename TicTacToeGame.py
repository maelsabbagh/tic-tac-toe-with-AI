import random
import math

oo = 0x3f3f3f3f3f3f3f3f


class TicTacToe:

    def __init__(self):
        """Initialize with empty board"""
        self.board = [" ", " ", " ",
                      " ", " ", " ",
                      " ", " ", " "]

    def show(self):
        """Format and print board"""
        print("""
          {} | {} | {}
         -----------
          {} | {} | {}
         -----------
          {} | {} | {}
        """.format(*self.board))

    def clearBoard(self):
        self.board = [" ", " ", " ",
                      " ", " ", " ",
                      " ", " ", " "]

    def whoWon(self):
        if self.checkWin() == "X":
            return "X"
        elif self.checkWin() == "O":
            return "O"
        elif self.gameOver() == True:
            return "Nobody"

    def availableMoves(self):
        """Return empty spaces on the board"""
        moves = []
        for i in range(0, len(self.board)):
            if self.board[i] == " ":
                moves.append(i)
        return moves

    def getMoves(self, player):
        """Get all moves made by a given player"""
        moves = []
        for i in range(0, len(self.board)):
            if self.board[i] == player:
                moves.append(i)
        return moves

    def makeMove(self, position, player):
        """Make a move on the board"""
        if self.board[position] == " ":
            self.board[position] = player
            return True
        elif self.board[position] != " " and player is " ":
            self.board[position] = player
            return True
        else:
            print("Invalid Move")
            return False

    def checkWin(self):
        """Return the player that wins the game"""
        combos = ([0, 1, 2], [3, 4, 5], [6, 7, 8],
                  [0, 3, 6], [1, 4, 7], [2, 5, 8],
                  [0, 4, 8], [2, 4, 6])

        for player in ("X", "O"):
            positions = self.getMoves(player)
            for combo in combos:
                win = True
                for pos in combo:
                    if pos not in positions:
                        win = False
                if win:
                    return player

    def gameOver(self):
        """Return True if X wins, O wins, or draw, else return False"""
        if self.checkWin() != None:
            return True
        for i in self.board:
            if i == " ":
                return False
        return True

    def minimax(self, node, depth, player):
        """
        Recursively analyze every possible game state and choose
        the best move location.
        node - the board
        depth - how far down the tree to look
        player - what player to analyze best move for (currently setup up ONLY for "O")

        """
        if self.gameOver():
            b = self.whoWon()
            if b == "O":
                return 1
            elif b == "X":
                return -1
            else:
                return 0

        if player == "O":
            val = -oo
            for child in self.availableMoves():
                self.makeMove(child, player)
                val = max(val, self.minimax(node, depth - 1, changePlayer(player)))
                self.makeMove(child, " ")
            return val
        else:
            val = oo
            for child in self.availableMoves():
                self.makeMove(child, player)
                val = min(val, self.minimax(node, depth - 1, changePlayer(player)))
                self.makeMove(child, " ")
            return val

    def alphabeta(self, node):
        val = self.min_val(node, -oo, oo)
        return val

    def max_val(self, node, alpha, beta):
        if self.gameOver():
            b = self.whoWon()
            if b == "O":
                return 1
            elif b == "X":
                return -1
            else:
                return 0
        val = -oo
        for child in self.availableMoves():
            self.makeMove(child, "O")
            val = max(val, self.min_val(node, alpha, beta))
            self.makeMove(child, " ")
            if val >= beta:
                return val
            alpha = max(alpha, val)
        return val

    def min_val(self, node, alpha, beta):
        if self.gameOver():
            b = self.whoWon()
            if b == "O":
                return 1
            elif b == "X":
                return -1
            else:
                return 0
        val = oo
        for child in self.availableMoves():
            self.makeMove(child, "X")
            val = min(val, self.max_val(node, alpha, beta))
            self.makeMove(child, " ")
            if val <= alpha:
                return val
            beta = min(beta, val)
        return val


def changePlayer(player):
    """Returns the opposite player given any player"""
    if player == "X":
        return "O"
    else:
        return "X"


def make_best_move(board, depth, player):
    """
    Controllor function to initialize minimax and keep track of optimal move choices
    board - what board to calculate best move for
    depth - how far down the tree to go
    player - who to calculate best move for (Works ONLY for "O" right now)
    """
    neutralValue = 0
    choices = []
    for move in board.availableMoves():
        board.makeMove(move, player)
        #moveValue = board.minimax(board, depth - 1, changePlayer(player))
        moveValue = board.alphabeta(board)
        board.makeMove(move, " ")

        if moveValue > neutralValue:
            choices = [move]
            break
        elif moveValue == neutralValue:
            choices.append(move)
    print("choices: ", choices)

    if len(choices) > 0:
        return random.choice(choices)
    else:
        return random.choice(board.availableMoves())


# Actual game
if __name__ == '__main__':
    game = TicTacToe()
    game.show()

    while game.gameOver() == False:

        isValid = False
        while not isValid:
            person_move = int(input("You are X: Choose number from 1-9: "))
            isValid = game.makeMove(person_move - 1, "X")
        game.show()

        if game.gameOver() == True:
            break

        print("Computer choosing move...")
        ai_move = make_best_move(game, -1, "O")
        game.makeMove(ai_move, "O")
        game.show()

print("Game Over. " + game.whoWon() + " Wins")
