# Chess Endgame Solver

## 1. Brief Description
This project is a Python-based chess endgame solver. It reads a simplified chess board position and determines whether a player can force a win within a small, user-defined number of moves (up to 4-5). If a victory is possible, the program advises the user on the correct winning move.

## 2. Detailed Specification
The program acts as an oracle for chess endgames with a low number of pieces. 
*   **Allowed Pieces:** King, Queen, Rook, and Bishop.
*   **Excluded Rules:** Pawns and Knights are not included. As a result, pawn-specific rules (like *en passant* or promotion) are omitted. Complex movement rules such as castling are also excluded to simplify the simulation logic.
*   **Depth Limit:** The maximum search depth is limited to 4 to 5 moves. 
*   **Execution:** The program is non-interactive during the calculation phase. It reads the board state from a predefined text file and outputs the result directly.

## 3. Algorithm & Justification
**Chosen Algorithm:** Iterative Deepening Depth-First Search (IDDFS) combined with Minimax logic.

**Discussion of Alternative (Breadth-First Search):** 
Initially, Breadth-First Search (BFS) was considered because it naturally finds the shortest path to a goal. However, it was rejected for two critical reasons:
1.  **Memory constraints:** In Python, a pure BFS queue storing all possible board states up to a depth of 5 would rapidly exhaust available system memory.
2.  **Opponent Logic:** Pure BFS is unsuitable for two-player adversarial games because it cannot evaluate the opponent's defensive counter-moves. 

IDDFS with Minimax perfectly resolves these issues. It maintains the memory efficiency of a Depth-First Search while guaranteeing that the shortest path to victory is found (replicating the primary benefit of BFS). Furthermore, the Minimax logic accurately simulates an opponent trying to delay or prevent the win.

## 4. Program Structure & Data
*   **Board Representation:** The chessboard is represented as a 2D list (an 8x8 matrix) containing strings for empty squares (`.`) and pieces (`K`, `Q`, `R`, `B`, `k`, `q`, `r`, `b`).
*   **Move Generation:** Handled by `get_pseudo_legal_moves` (which generates all geometrically possible moves based on directional vectors) and filtered by `get_legal_moves`. The latter simulates each move and utilizes an optimized `is_check` function to ensure the king is not left in check.
*   **Search Function:** Implemented via `iddfs()` as the outer iterative loop, which progressively increases the depth and drives the recursive `minimax()` function with Alpha-Beta pruning to find the optimal defensive or offensive paths.

## 5. Input Data Representation

The input is provided via a plain text file containing an 8x8 matrix representing the chessboard.
*   The file must contain exactly 8 lines.
*   Each line must contain exactly 8 characters separated by spaces.
*   Empty squares are represented by a specific character (e.g., `.`).
*   Pieces are represented by letters: `K` (King), `Q` (Queen), `R` (Rook), `B` (Bishop).
*   *White pieces* are uppercase (`K`), *Black pieces* are lowercase (`k`).

**Example of an input file:**
```
. . . . . . . .
. k . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . K . . . .
. . . . Q . . .
```

## 6. Output Data Interpretation
The program will print the result directly to the console. 
*   If a forced win is found within the specified depth, it will print: `Win found in [X] moves. Play: [Piece] from [Start Square] to [End Square].`
*   If no forced win is possible within the limit, it will print: `No forced win found within [X] moves.`

## 7. Test Cases

To verify the correct behavior of the program, the following test cases are provided in the project root directory and executed via the test suite:
1.  **Invalid Board Validation (`invalid_board.txt`):** Contains an illegal piece (`p` for pawn) and irregular row lengths. Verifies that the validation logic properly flags corrupted input and stops the engine.
2.  **Unwinnable / Draw (`no_mate.txt`):** A position where White cannot force a win within the search limit. Verifies that the program exits correctly and returns `None` instead of looping infinitely.
3.  **Mate in 1 (`mate_in_1.txt`):** A simple King and Rook vs. King scenario where White can checkmate in exactly 1 move (depth 1). Verifies basic checkmate detection.
4.  **Mate in 2 (`mate_in_2.txt`):** A ladder mate setup with two Rooks requiring a 2-move forced sequence (found at depth 3 plies). Verifies the adversarial Minimax logic against optimal defense.
5.  **Mate in 3 (`mate_in_3.txt`):** A deeper ladder mate setup requiring a 3-move sequence (found at depth 5 plies). Verifies that IDDFS correctly finds the shortest path to checkmate.

## 8. How to Run Tests
You can execute the built-in test suite directly from the terminal using Python's `unittest` module:
```bash
python -m unittest Unit_Test.py
```