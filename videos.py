def find_best_move(current_board, player, algorithm_index):
    # This is the start of the instructions for the AI to pick its move.
    # It needs the current board, the AI's symbol ('X' or 'O'), and which AI strategy to use.

    opponent = 'O' if player == 'X' else 'X'
    # This line just figures out what the other player's symbol is.

    empty_cells = get_empty_cells(current_board)
    # It gets a list of all the spots on the board that are empty.

    if not empty_cells:
        # If there are no empty spots left on the board:
        return (-1, -1)
        # It means the game is full, so it returns a special value (-1, -1) to show it couldn't find a move.

    win_move = find_win_or_block(current_board, player)
    # It calls another function to see if the AI can win in just one move.
    if win_move:
        # If that function found a winning move:
        return win_move
        # The AI takes that winning move immediately.

    block_move = find_win_or_block(current_board, opponent)
    # If the AI can't win, it calls the same function to see if the *opponent* can win in one move.
    if block_move:
        # If the opponent can win:
        return block_move
        # The AI takes that spot to block the opponent.

    # If no immediate win or block is needed, the AI uses the strategy you chose:

    if algorithm_index == AI_BLOCK_FORK:
        # If the chosen strategy is "Block Fork":
        if current_board[1][1] is None:
             # Check if the center square is empty.
             return (1, 1)
             # If it is, the AI takes the center square (often a good move).

        block_fork_move = find_fork(current_board, opponent)
        # If the center is taken, it calls a function to see if the opponent can set up a "fork" (two ways to win).
        if block_fork_move:
            # If the opponent *can* set up a fork:
            return block_fork_move
            # The AI takes the spot that blocks the opponent's fork.

        empty_cells = get_empty_cells(current_board)
        # Get the list of empty spots again (in case the board changed slightly in checks).
        if empty_cells:
            # If there are still empty spots:
            return empty_cells[0]
            # The AI just picks the very first empty spot it finds.
        else:
            # If somehow there are no empty spots left (shouldn't happen here):
            return (-1, -1)
            # Return the "no move found" value.


    elif algorithm_index == AI_BLOCK_THREATS:
        # If the chosen strategy is "Block Threats":
        block_threat_move = find_block_threat_move(current_board, opponent)
        # Call a function to see if the opponent has any "threats" (like two in a row that aren't a win yet).
        if block_threat_move:
             # If the opponent has a threat:
             return block_threat_move
             # The AI takes the spot that blocks that threat.
        return empty_cells[0]
        # If no threats are found, the AI picks the first empty spot.

    elif algorithm_index == AI_MINIMAX:
        # If the chosen strategy is "Minimax" (the thinking ahead one):
        best_score = -float('inf')
        # Start with a very low score (because the AI wants the highest score).
        best_move = (-1, -1)
        # Start with no best move found yet.

        for r, c in empty_cells:
            # Look at each empty spot as a possible move.
            current_board[r][c] = player
            # Temporarily put the AI's symbol in that spot.
            score = minimax(current_board, 0, False, player)
            # Call the Minimax brain to see what score the opponent would allow from this new board state.
            current_board[r][c] = None
            # Take the symbol back (undo the temporary move).

            if score > best_score:
                # If the score from this move is better than the best score found so far:
                best_score = score
                # Update the best score.
                best_move = (r, c)
                # Remember this move as the best one so far.

        return best_move if best_move != (-1, -1) else empty_cells[0]
        # After checking all moves, return the move that gave the best score. If no move was found (shouldn't happen), take the first empty spot.

    elif algorithm_index == AI_MINIMAX_BLOCK_FORK:
        # If the strategy is "Minimax + Block Fork":
        block_fork_move = find_fork(current_board, opponent)
        # First, check if the opponent can set up a fork.
        if block_fork_move:
            # If they can, block the fork immediately.
            return block_fork_move

        # If no fork needs blocking, use the Minimax brain (similar to AI_MINIMAX):
        best_score = -float('inf')
        best_move = (-1, -1)
        alpha = -float('inf') # These are for Alpha-Beta Pruning, even if the basic minimax is called.
        beta = float('inf')

        for r, c in empty_cells:
            current_board[r][c] = player
            score = minimax(current_board, 0, False, player) # Calls basic minimax
            current_board[r][c] = None
            if score > best_score:
                best_score = score
                best_move = (r, c)
            alpha = max(alpha, best_score) # Alpha update (part of pruning logic)

        return best_move if best_move != (-1, -1) else empty_cells[0]
        # Return the best move found by Minimax, or the first empty spot.

    elif algorithm_index == AI_MINIMAX_BLOCK_THREATS:
        # If the strategy is "Minimax + Block Threats":
        block_threat_move = find_block_threat_move(current_board, opponent)
        # First, check if the opponent has any threats.
        if block_threat_move:
             # If they do, block the threat immediately.
             return block_threat_move

        # If no threats need blocking, use the Minimax brain (similar to AI_MINIMAX):
        best_score = -float('inf')
        best_move = (-1, -1)
        alpha = -float('inf') # Alpha-Beta variables
        beta = float('inf')
        for r, c in empty_cells:
            current_board[r][c] = player
            score =minimax(current_board, 0, False, player) # Calls basic minimax
            current_board[r][c] = None
            if score > best_score:
                best_score = score
                best_move = (r, c)
            alpha = max(alpha, best_score) # Alpha update

        return best_move if best_move != (-1, -1) else empty_cells[0]
        # Return the best move found by Minimax, or the first empty spot.

    elif algorithm_index == AI_MINIMAX_ALPHA_BETA:
        # If the strategy is "Minimax + Alpha-Beta Pruning" (the super-fast thinking ahead):
        best_score = -float('inf')
        best_move = (-1, -1)
        alpha = -float('inf') # Initialize Alpha (our best guaranteed score)
        beta = float('inf') # Initialize Beta (opponent's best guaranteed score against us)

        for r, c in empty_cells:
            # Look at each empty spot as a possible move.
            current_board[r][c] = player
            # Temporarily make our move.
            score = minimax_alpha_beta(current_board, 0, False, player, alpha, beta)
            # Call the Alpha-Beta Minimax brain to get the score from this move, passing alpha and beta.
            current_board[r][c] = None
            # Undo the move.

            if score > best_score:
                # If this move's score is better than the best found so far:
                best_score = score
                best_move = (r, c)
            alpha = max(alpha, best_score)
            # Update Alpha: Our best guaranteed score is now the highest score we've seen so far.

            # Note: The pruning check (if beta <= alpha: break) happens *inside* the minimax_alpha_beta function itself.

        return best_move if best_move != (-1, -1) else empty_cells[0]
        # Return the best move found by the Alpha-Beta Minimax.

    elif algorithm_index == AI_MINIMAX_HEURISTIC_REDUCTION:
        # If the strategy is "Minimax + Heuristic Reduction":
        fork_move = find_fork(current_board, player)
        # Check if the AI can create a fork.
        block_fork_move = find_fork(current_board, opponent)
        # Check if the opponent can create a fork.

        if fork_move:
             # If the AI can create a fork:
             return fork_move
             # Take that move.
        if block_fork_move:
             # If the opponent can create a fork (and we couldn't create our own):
             return block_fork_move
             # Block the opponent's fork.

        # If no fork situations, use the Alpha-Beta Minimax brain:
        best_score = -float('inf')
        best_move = (-1, -1)
        alpha = -float('inf') # Alpha-Beta variables
        beta = float('inf')

        for r, c in empty_cells:
            current_board[r][c] = player
            score = minimax_alpha_beta(current_board, 0, False, player, alpha, beta) # Calls Alpha-Beta Minimax
            current_board[r][c] = None

            if score > best_score:
                best_score = score
                best_move = (r, c)
            alpha = max(alpha, best_score) # Alpha update

        return best_move if best_move != (-1, -1) else empty_cells[0]
        # Return the best move found by Alpha-Beta Minimax.


    elif algorithm_index == AI_MINIMAX_SYMMETRY_REDUCTION:
        # If the strategy is "Minimax + Symmetry Reduction" (the one with memory):
        canonical_board_tuple = canonicalize_board(current_board)
        # Convert the current board into its unique "standard" version (the canonical form).

        if canonical_board_tuple in memoization_table:
            # Check if this standard board version is already in the AI's memory bank.
            canonical_best_move = memoization_table[canonical_board_tuple]
            # If yes, get the best move that was previously calculated for this standard board.
            transformed_move = transform_move(canonical_best_move, current_board, canonical_board_tuple)
            # Translate that move from the standard board's position back to the original board's position.
            if 0 <= transformed_move[0] < 3 and 0 <= transformed_move[1] < 3 and current_board[transformed_move[0]][transformed_move[1]] is None:
                 # Check if the translated move is valid on the current board (within bounds and empty).
                 return transformed_move
                 # If valid, use this remembered and translated move.
            else:
                 # If the translated move is somehow invalid (shouldn't happen often):
                 print("Warning: Symmetry transformation resulted in an invalid move. Recalculating.")
                 # Print a warning and proceed to calculate the move the hard way.

        # If the standard board was NOT in the memory bank, or the translated move was invalid, calculate it:
        best_score = -float('inf')
        best_move = (-1, -1)
        alpha = -float('inf') # Alpha-Beta variables
        beta = float('inf')

        for r, c in empty_cells:
            current_board[r][c] = player
            score = minimax_alpha_beta(current_board, 0, False, player, alpha, beta) # Calls Alpha-Beta Minimax
            current_board[r][c] = None

            if score > best_score:
                best_score = score
                best_move = (r, c)
            alpha = max(alpha, best_score) # Alpha update

        if best_move != (-1, -1):
             # If a valid best move was found by calculation:
             memoization_table[canonical_board_tuple] = best_move
             # Store this calculated best move in the memory bank for this standard board version.

        return best_move if best_move != (-1, -1) else empty_cells[0]
        # Return the calculated best move, or the first empty spot.


    else:
        # If the algorithm index doesn't match any known strategy (an error):
        print(f"Warning: Unknown AI algorithm index: {algorithm_index}. Using first empty cell.")
        # Print a warning message.
        return empty_cells[0]
        # Just pick the first empty spot as a fallback.