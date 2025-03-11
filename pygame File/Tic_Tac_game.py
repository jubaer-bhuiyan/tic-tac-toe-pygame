import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = WIDTH // 3
LINE_COLOR = (0, 0, 0)
BG_COLOR = (255, 255, 255)
X_COLOR = (200, 0, 0)
O_COLOR = (0, 0, 200)
TEXT_COLOR = (0, 0, 0)
LINE_WIDTH = 10
FONT = pygame.font.Font(None, 50)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe - AI Mode")
screen.fill(BG_COLOR)

# Board setup
board = [[None] * 3 for _ in range(3)]
current_player = "X"
game_over = False
ai_difficulty = 0.8  # 80% AI plays optimally, 20% it makes a mistake

def draw_grid():
    for i in range(1, 3):
        pygame.draw.line(screen, LINE_COLOR, (i * GRID_SIZE, 0), (i * GRID_SIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, i * GRID_SIZE), (WIDTH, i * GRID_SIZE), LINE_WIDTH)

def draw_xo():
    for row in range(3):
        for col in range(3):
            if board[row][col] == "X":
                pygame.draw.line(screen, X_COLOR, (col * GRID_SIZE + 20, row * GRID_SIZE + 20),
                                 ((col + 1) * GRID_SIZE - 20, (row + 1) * GRID_SIZE - 20), LINE_WIDTH)
                pygame.draw.line(screen, X_COLOR, ((col + 1) * GRID_SIZE - 20, row * GRID_SIZE + 20),
                                 (col * GRID_SIZE + 20, (row + 1) * GRID_SIZE - 20), LINE_WIDTH)
            elif board[row][col] == "O":
                pygame.draw.circle(screen, O_COLOR, (col * GRID_SIZE + GRID_SIZE // 2, row * GRID_SIZE + GRID_SIZE // 2),
                                   GRID_SIZE // 2 - 20, LINE_WIDTH)

def display_message(text):
    text_surface = FONT.render(text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT - 50))
    screen.blit(text_surface, text_rect)

def check_winner():
    for row in board:
        if row[0] == row[1] == row[2] and row[0] is not None:
            return row[0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]
    return None

def best_move():
    if random.random() > ai_difficulty:  # 20% chance of making a random move
        available_moves = [(r, c) for r in range(3) for c in range(3) if board[r][c] is None]
        if available_moves:
            row, col = random.choice(available_moves)
            board[row][col] = "O"
            return
    
    best_score = -float("inf")
    move = None
    for row in range(3):
        for col in range(3):
            if board[row][col] is None:
                board[row][col] = "O"
                score = minimax(board, 0, False)
                board[row][col] = None
                if score > best_score:
                    best_score = score
                    move = (row, col)
    if move:
        board[move[0]][move[1]] = "O"

def minimax(board, depth, is_maximizing):
    winner = check_winner()
    if winner == "X":
        return -10 + depth
    elif winner == "O":
        return 10 - depth
    elif all(board[row][col] is not None for row in range(3) for col in range(3)):
        return 0
    
    if is_maximizing:
        best_score = -float("inf")
        for row in range(3):
            for col in range(3):
                if board[row][col] is None:
                    board[row][col] = "O"
                    score = minimax(board, depth + 1, False)
                    board[row][col] = None
                    best_score = max(best_score, score)
        return best_score
    else:
        best_score = float("inf")
        for row in range(3):
            for col in range(3):
                if board[row][col] is None:
                    board[row][col] = "X"
                    score = minimax(board, depth + 1, True)
                    board[row][col] = None
                    best_score = min(best_score, score)
        return best_score

def reset_game():
    global board, current_player, game_over
    board = [[None] * 3 for _ in range(3)]
    current_player = "X"
    game_over = False
    screen.fill(BG_COLOR)
    draw_grid()

draw_grid()

# Game loop
while True:
    screen.fill(BG_COLOR)
    draw_grid()
    draw_xo()
    
    winner = check_winner()
    if winner or all(board[row][col] is not None for row in range(3) for col in range(3)):
        game_over = True
        display_message(f"{winner if winner else 'Draw'}! Press 'R' to restart.")
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and current_player == "X" and not game_over:
            x, y = event.pos
            row, col = y // GRID_SIZE, x // GRID_SIZE
            if board[row][col] is None:
                board[row][col] = "X"
                current_player = "O"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_game()
    
    if current_player == "O" and not game_over:
        best_move()
        current_player = "X"
    
    pygame.display.flip()
