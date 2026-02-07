import math
import copy

X = "X"
O = "O"
EMPTY = None

def initial_state():
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    
    if terminal(board):
        return None
    return O if x_count > o_count else X
def actions(board):
    possible_moves = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_moves.add((i, j))
    return possible_moves

def result(board, action):
    if board[action[0]][action[1]] is not EMPTY:
        raise Exception("Invalid Move")
    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = player(board)
    return new_board

def winner(board):
    for row in board:
        if row[0] == row[1] == row[2] and row[0] is not EMPTY:
            return row[0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not EMPTY:
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not EMPTY:
        return board[0][2]
    return None

def terminal(board):
    if winner(board) is not None:
        return True
    for row in board:
        if EMPTY in row:
            return False
    return True

def utility(board):
    win = winner(board)
    if win == X: return 1
    if win == O: return -1
    return 0

def minimax(board):
    if terminal(board):
        return None
    curr_player = player(board)
    if curr_player == X:
        best_val = -math.inf
        best_move = None
        for action in actions(board):
            move_val = min_value(result(board, action), -math.inf, math.inf)
            if move_val > best_val:
                best_val = move_val
                best_move = action
        return best_move
    else:
        best_val = math.inf
        best_move = None
        for action in actions(board):
            move_val = max_value(result(board, action), -math.inf, math.inf)
            if move_val < best_val:
                best_val = move_val
                best_move = action
        return best_move

def max_value(board, alpha, beta):
    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action), alpha, beta))
        alpha = max(alpha, v)
        if beta <= alpha: break
    return v

def min_value(board, alpha, beta):
    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action), alpha, beta))
        beta = min(beta, v)
        if beta <= alpha: break
    return v