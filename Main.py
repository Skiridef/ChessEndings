import sys

DIRECTIONS = {
    'K': [(-1, 0), (1, 0), (0, -1), (0, 1), (1, -1), (-1, -1), (-1, 1), (1,1)],
    'Q': [(-1, 0), (1, 0), (0, -1), (0, 1), (1, -1), (-1, -1), (-1, 1), (1,1)],
    'B': [(-1, -1), (-1, 1), (1, -1), (1, 1)],
    'R': [(-1, 0), (1, 0), (0, -1), (0, 1)]
}


def read_board(filepath):
    """
    Reads a board file and returns it as a list
    :param filepath: path to the board file
    :return: An 8x8 matrix of the board
    """
    board = []
    with open(filepath) as file:
        lines = file.readlines()
        for line in lines:
            row = line.strip().split(" ")
            if row:
                board.append(row)
    return board

def validate_board(board):
    """
    Validates that the board is valid
    :param board: an 8x8 matrix of the board
    :return: True if the board is valid, False otherwise
    """
    if len(board) != 8:
        print(f"Invalid board: Expected 8 rows, got {len(board)}")
        return False
    allowed_chars = {'.', 'K', 'k', 'Q', 'q', 'R', 'r', 'B', 'b'}
    white_kings = 0
    black_kings = 0
    for row in range(8):
        if len(board[row]) != 8:
            print(f"Invalid board: Row {row+1} must contain exactly 8 characters")
            return False
        for column in range(8):
            piece = board[row][column]
            if piece not in allowed_chars:
                print(f'Invalid board: Piece {piece} not allowed')
                return False
            if piece == 'K':
                white_kings += 1
            elif piece == 'k':
                black_kings += 1
    if white_kings != 1:
        print(f"Invalid board: White Kings count is {white_kings}, but must be only one")
        return False
    if black_kings != 1:
        print(f"Invalid board: Black Kings count is {black_kings}, but must be only one")
        return False
    return True

def get_pseudo_legal_moves(board, row, col):
    """
    Generates a list of all possible moves that can be made
    :param board: an 8x8 matrix of the board
    :param row: current row
    :param col: current column
    :return: list of possible moves
    """
    piece = board[row][col]
    if piece == '.':
        return []
    possible_moves = []
    piece_type = piece.upper()
    is_white = piece.isupper()
    for dr, dc in DIRECTIONS[piece_type]:
        current_r, current_c = row + dr, col + dc
        while True:
            if not (0 <= current_r < 8 and 0 <= current_c < 8):
                break
            else:
                target_piece = board[current_r][current_c]
                if target_piece == '.':
                    possible_moves.append(((row, col),(current_r, current_c)))
                    current_r, current_c = current_r + dr, current_c + dc
                elif target_piece.isupper() != is_white:
                    possible_moves.append(((row, col),(current_r, current_c)))
                    break
                else:
                    break
                if piece_type == 'K':
                    break
    return possible_moves

def is_check(board, is_white):
    """
    Checks if the board is white or black
    :param board: an 8x8 matrix of the board
    :param is_white: boolean indicating if the board is white or black
    :return: True if the board is white or black, False otherwise
    """
    king_pos = None
    target_king = 'K' if is_white else 'k'
    for row in range(8):
        for col in range(8):
            if board[row][col] == target_king:
                king_pos = (row, col)
                break
        if king_pos:
            break
    for row in range(8):
        for col in range(8):
            enemy_pieces = board[row][col]
            if enemy_pieces == '.':
                continue
            if enemy_pieces.isupper() != is_white:
                enemy_moves = get_pseudo_legal_moves(board, row, col)
                for move in enemy_moves:
                    end_pos = move[1]
                    if end_pos == king_pos:
                        return True
    return False

def get_legal_moves(board, is_white):
    """
    Generates all legal moves that can be made
    :param board: an 8x8 matrix of the board
    :param is_white: boolean indicating if the board is white or black
    :return: list of legal moves
    """
    legal_moves = []
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece == '.':
                continue
            if piece.isupper() == is_white:
                pseudo_moves = get_pseudo_legal_moves(board, row, col)
                for move in pseudo_moves:
                    start_row, start_col = move[0]
                    end_row, end_col = move[1]
                    target_piece = board[end_row][end_col]
                    board[end_row][end_col] = piece
                    board[start_row][start_col] = '.'
                    if not is_check(board, is_white):
                        legal_moves.append(move)
                    board[start_row][start_col] = piece
                    board[end_row][end_col] = target_piece
    return legal_moves

def minimax(board, depth, alpha, beta, is_white, maximizing_player):
    """
    Minimax algorithm with alpha-beta pruning
    """
    legal_moves = get_legal_moves(board, is_white)
    if len(legal_moves) == 0:
        if is_check(board, is_white):
            #Checkmate
            return -float('inf') if maximizing_player else float('inf')
        #Stalemate
        return 0
    if depth == 0:
        #No close mate
        return 0

    #Recursive function
    if maximizing_player:
        max_evaluation = -float('inf')
        for move in legal_moves:
            (start_row, start_col), (end_row, end_col) = move
            #Make move
            captured_piece = board[end_row][end_col]
            board[end_row][end_col] = board[start_row][start_col]
            board[start_row][start_col] = '.'
            #Recursion
            evaluation = minimax(board, depth - 1, alpha, beta, not is_white, False)
            #Unmake move
            board[start_row][start_col] = board[end_row][end_col]
            board[end_row][end_col] = captured_piece
            #Update alpha-beta and max eval
            max_evaluation = max(max_evaluation, evaluation)
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break #Beta pruning
        return max_evaluation
    else:
        min_evaluation = float('inf')
        for move in legal_moves:
            (start_row, start_col), (end_row, end_col) = move
            #Make move
            captured_piece = board[end_row][end_col]
            board[end_row][end_col] = board[start_row][start_col]
            board[start_row][start_col] = '.'
            #Recursion
            evaluation = minimax(board, depth - 1, alpha, beta, not is_white, True)
            #Unmake move
            board[start_row][start_col] = board[end_row][end_col]
            board[end_row][end_col] = captured_piece
            #Update alpha-beta and min eval
            min_evaluation = min(min_evaluation, evaluation)
            beta = min(beta, evaluation)
            if beta <= alpha:
                break #Alpha pruning
        return min_evaluation

def iddfs(board, max_depth, is_white_start=True):
    """
    Iterative DFS algorithm to find the shortest path to mate
    :param board: an 8x8 matrix of the board 
    :param max_depth: maximum depth to search
    :param is_white_start: True if white moves first
    :return: tuple(depth, move) if winning move found, None otherwise
    """
    for current_depth in range(1, max_depth + 1):
        legal_moves = get_legal_moves(board, is_white_start)
        for move in legal_moves:
            (start_row, start_col), (end_row, end_col) = move
            #First move
            captured_piece = board[end_row][end_col]
            board[end_row][end_col] = board[start_row][start_col]
            board[start_row][start_col] = '.'
            #Call minimax for enemy, in case move is winning - we wait for float('inf')
            evalution = minimax(board, current_depth - 1, -float('inf'), float('inf'), not is_white_start, False)
            #Unmake move
            board[start_row][start_col] = board[end_row][end_col]
            board[end_row][end_col] = captured_piece
            #Check for guaranteed mate
            if evalution == float('inf'):
                return current_depth, move
        return None

def format_move(move):
    """
    Helper function to format the move for printing
    """
    (start_row, start_col), (end_row, end_col) = move
    start_square = f"{chr(start_col + 97)}{8 - start_row}"
    end_square = f"{chr(end_col + 97)}{8 - end_row}"
    return f"from {start_square} to {end_square}"

if __name__ == '__main__':
    filepath = sys.argv[1] if len(sys.argv) > 1 else "board.txt"
    max_search_depth = 5
    try:
        my_board = read_board(filepath)
    except FileNotFoundError:
        print("File not found")
        sys.exit(1)
    if validate_board(my_board):
        print(f"Searching for forced mate up to depth {max_search_depth} moves deep...")
        result = iddfs(my_board, max_search_depth, is_white_start=True)
        if result:
            depth, winning_move = result
            piece = my_board[winning_move[0][0]][winning_move[0][1]]
            move_str = format_move(winning_move)
            print(f"Win found in {depth} moves! Play: {piece} {move_str}")
        else:
            print(f"No forced win found within {max_search_depth} moves!")
    else:
        print("Engine stopped due to invalid board")












