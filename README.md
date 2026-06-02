# ChessEndings
A Python chess endgame solver using IDDFS and Minimax to calculate forced wins in up to 5 moves for simplified board states.


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
*   **Board Representation:** (e.g., A 2D array / list of lists, or a 1D array, or a custom class).
*   **Move Generation:** (e.g., A function that generates all legal pseudo-moves and filters out moves that leave the King in check).
*   **Search Function:** The IDDFS/Minimax recursive function. 

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

To verify the correct behavior of the program, the following test cases are provided in the `tests/` folder:
1.  **Test 1 (Mate in 1):** A simple King and Queen vs. King scenario where white can checkmate in exactly 1 move. Verifies basic checkmate detection.
2.  **Test 2 (Mate in 3):** A more complex scenario requiring IDDFS to search deeper while avoiding stalemates.
3.  **Test 3 (Unwinnable / Draw):** A position where white cannot force a win within 5 moves. Verifies that the program stops correctly and does not crash or loop infinitely.

## 8. Final Sigh

The transition from planning to use BFS to actually implementing Minimax with IDDFS was the most challenging part of this project. Modeling the opponent's legal moves and handling edge cases like stalemate required significant debugging. However, it was highly rewarding to see the algorithm successfully solve complex endgames without running out of memory.
