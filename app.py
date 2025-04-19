import pygame
import sys
import random
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
OUTER_WIDTH, OUTER_HEIGHT = 800, 800  # Initial dimensions for outer space
INNER_WIDTH, INNER_HEIGHT = 600, 600  # Inner square for the game
screen = pygame.display.set_mode((OUTER_WIDTH, OUTER_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Tic Tac Toe")

# Colors
WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)

# Fonts
font = pygame.font.SysFont("Arial", 60, bold=True)
small_font = pygame.font.SysFont("Arial", 30, bold=True)

# Game variables
board = [["" for _ in range(3)] for _ in range(3)]
current_player = "X"
winner = None
game_over = False

# Player names and symbols
player_names = {"X": "", "O": ""}
player_symbols = {"Player 1": "X", "Player 2": "O"}

# Winner counters
winner_counters = {"X": 0, "O": 0}

# Function to get player names and symbols
def get_player_info():
    global player_names, current_player
    input_active = [False, False]
    player_texts = ["", ""]
    symbol_chosen = [False, False]
    start_game = False

    while not start_game:
        screen.fill(WHITE)
        for i in range(2):
            prompt_text = small_font.render(f"Enter Player {i + 1} Name:", True, BLACK)
            input_box = pygame.Rect(OUTER_WIDTH // 2 - 100, OUTER_HEIGHT // 4 + i * 200, 200, 50)
            dropdown_box = pygame.Rect(OUTER_WIDTH // 2 + 110, OUTER_HEIGHT // 4 + i * 200, 50, 50)
            prompt_x = input_box.x + (input_box.width + dropdown_box.width) // 2 - prompt_text.get_width() // 2
            screen.blit(prompt_text, (prompt_x, input_box.y - 40))
            
            color = ORANGE if input_active[i] else BLACK
            pygame.draw.rect(screen, color, input_box, 2)
            text_surface = small_font.render(player_texts[i], True, BLACK)
            screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))
            input_box.w = max(200, text_surface.get_width() + 10)

            # Draw dropdown for symbols
            pygame.draw.rect(screen, BLACK, dropdown_box, 2)
            symbol_surface = small_font.render(player_symbols[f"Player {i + 1}"], True, BLACK)
            screen.blit(symbol_surface, (dropdown_box.x + 5, dropdown_box.y + 5))

        # Draw Start button
        start_button = pygame.Rect(OUTER_WIDTH // 2 - 100, OUTER_HEIGHT // 2 + 250, 200, 50)
        pygame.draw.rect(screen, ORANGE, start_button)
        start_text = small_font.render("Start", True, PURPLE)
        screen.blit(start_text, (start_button.x + (start_button.w - start_text.get_width()) // 2, start_button.y + (start_button.h - start_text.get_height()) // 2))

        # Draw Quit button
        quit_button = pygame.Rect(OUTER_WIDTH // 2 - 100, OUTER_HEIGHT // 2 + 320, 200, 50)
        pygame.draw.rect(screen, ORANGE, quit_button)
        quit_text = small_font.render("Quit", True, PURPLE)
        screen.blit(quit_text, (quit_button.x + (quit_button.w - quit_text.get_width()) // 2, quit_button.y + (quit_button.h - quit_text.get_height()) // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(2):
                    input_box = pygame.Rect(OUTER_WIDTH // 2 - 100, OUTER_HEIGHT // 4 + i * 200, 200, 50)
                    dropdown_box = pygame.Rect(OUTER_WIDTH // 2 + 110, OUTER_HEIGHT // 4 + i * 200, 50, 50)
                    if input_box.collidepoint(event.pos):
                        input_active[i] = not input_active[i]
                    else:
                        input_active[i] = False
                    if dropdown_box.collidepoint(event.pos):
                        player_symbols[f"Player {i + 1}"] = "O" if player_symbols[f"Player {i + 1}"] == "X" else "X"
                if start_button.collidepoint(event.pos) and all(player_texts):
                    player_names[player_symbols["Player 1"]] = player_texts[0]
                    player_names[player_symbols["Player 2"]] = player_texts[1]
                    start_game = True
                if quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.KEYDOWN:
                for i in range(2):
                    if input_active[i]:
                        if event.key == pygame.K_RETURN:
                            input_active[i] = False
                        elif event.key == pygame.K_BACKSPACE:
                            player_texts[i] = player_texts[i][:-1]
                        elif len(player_texts[i]) < 10:
                            player_texts[i] += event.unicode

# Draw the board
def draw_board():
    screen.fill(WHITE)
    # Draw the inner game area
    pygame.draw.rect(screen, BLACK, ((OUTER_WIDTH - INNER_WIDTH) // 2, (OUTER_HEIGHT - INNER_HEIGHT) // 2, INNER_WIDTH, INNER_HEIGHT), 5)
    for row in range(1, 3):
        pygame.draw.line(screen, ORANGE, ((OUTER_WIDTH - INNER_WIDTH) // 2, (OUTER_HEIGHT - INNER_HEIGHT) // 2 + row * INNER_HEIGHT // 3), 
                         ((OUTER_WIDTH + INNER_WIDTH) // 2, (OUTER_HEIGHT - INNER_HEIGHT) // 2 + row * INNER_HEIGHT // 3), 5)
        pygame.draw.line(screen, ORANGE, ((OUTER_WIDTH - INNER_WIDTH) // 2 + row * INNER_WIDTH // 3, (OUTER_HEIGHT - INNER_HEIGHT) // 2), 
                         ((OUTER_WIDTH - INNER_WIDTH) // 2 + row * INNER_WIDTH // 3, (OUTER_HEIGHT + INNER_HEIGHT) // 2), 5)
    for row in range(3):
        for col in range(3):
            if board[row][col] != "":
                text = font.render(board[row][col], True, BLACK)
                text_rect = text.get_rect(center=((OUTER_WIDTH - INNER_WIDTH) // 2 + col * INNER_WIDTH // 3 + INNER_WIDTH // 6, 
                                                  (OUTER_HEIGHT - INNER_HEIGHT) // 2 + row * INNER_HEIGHT // 3 + INNER_HEIGHT // 6))
                screen.blit(text, text_rect)

    # Display current player's turn
    turn_text = small_font.render(f"{player_names[current_player]}'s Turn ({current_player})", True, BLACK)
    screen.blit(turn_text, (OUTER_WIDTH // 2 - turn_text.get_width() // 2, 10))

# Check for a win
def check_win():
    global winner, game_over
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] != "":
            winner = board[row][0]
            game_over = True
            return
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != "":
            winner = board[0][col]
            game_over = True
            return
    if board[0][0] == board[1][1] == board[2][2] != "" or board[0][2] == board[1][1] == board[2][0] != "":
        winner = board[1][1]
        game_over = True
        return
    if all(board[row][col] != "" for row in range(3) for col in range(3)):
        game_over = True

# Draw winning effect
def draw_winning_effect():
    for _ in range(10):  # Subtle confetti effect
        for _ in range(20):
            x = random.randint(0, OUTER_WIDTH)
            y = random.randint(0, OUTER_HEIGHT)
            color = random.choice([RED, GREEN, BLUE])
            pygame.draw.circle(screen, color, (x, y), 5)
        pygame.display.flip()
        pygame.time.delay(100)

# Reset the game
def reset_game():
    global board, current_player, winner, game_over
    board = [["" for _ in range(3)] for _ in range(3)]
    current_player = "X"
    winner = None
    game_over = False

# Main loop
get_player_info()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.VIDEORESIZE:
            OUTER_WIDTH, OUTER_HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((OUTER_WIDTH, OUTER_HEIGHT), pygame.RESIZABLE)
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if not game_over:
                row, col = (y - (OUTER_HEIGHT - INNER_HEIGHT) // 2) // (INNER_HEIGHT // 3), (x - (OUTER_WIDTH - INNER_WIDTH) // 2) // (INNER_WIDTH // 3)
                if 0 <= row < 3 and 0 <= col < 3 and board[row][col] == "":
                    board[row][col] = current_player
                    check_win()
                    if game_over and winner:
                        print("WON")
                        winner_counters[winner] += 1
                    current_player = "O" if current_player == "X" else "X"
            # Check if the "Play Again" button is clicked
            if OUTER_WIDTH - 210 <= x <= OUTER_WIDTH - 10 and 10 <= y <= 60:
                reset_game()
            # Check if the "New Game" button is clicked
            if 10 <= x <= 210 and 10 <= y <= 60:
                get_player_info()
                reset_game()
            # Check if the "Quit Game" button is clicked
            if OUTER_WIDTH - 210 <= x <= OUTER_WIDTH - 10 and OUTER_HEIGHT - 60 <= y <= OUTER_HEIGHT - 10:
                pygame.quit()
                sys.exit()

    draw_board()
    # Draw "Play Again" button at the top right corner
    pygame.draw.rect(screen, ORANGE, (OUTER_WIDTH - 210, 10, 200, 50))
    play_again_text = small_font.render("Play Again", True, PURPLE)
    play_again_shadow = small_font.render("Play Again", True, ORANGE)
    screen.blit(play_again_shadow, (OUTER_WIDTH - 208, 12))
    screen.blit(play_again_text, (OUTER_WIDTH - 210 + (200 - play_again_text.get_width()) // 2, 10 + (50 - play_again_text.get_height()) // 2))

    # Draw "New Game" button at the top left corner
    pygame.draw.rect(screen, ORANGE, (10, 10, 200, 50))
    new_game_text = small_font.render("New Game", True, PURPLE)
    new_game_shadow = small_font.render("New Game", True, ORANGE)
    screen.blit(new_game_shadow, (12, 12))
    screen.blit(new_game_text, (10 + (200 - new_game_text.get_width()) // 2, 10 + (50 - new_game_text.get_height()) // 2))

    # Draw "Quit Game" button at the bottom right corner
    pygame.draw.rect(screen, ORANGE, (OUTER_WIDTH - 210, OUTER_HEIGHT - 60, 200, 50))
    quit_game_text = small_font.render("Quit Game", True, PURPLE)
    quit_game_shadow = small_font.render("Quit Game", True, ORANGE)
    screen.blit(quit_game_shadow, (OUTER_WIDTH - 208, OUTER_HEIGHT - 58))
    screen.blit(quit_game_text, (OUTER_WIDTH - 210 + (200 - quit_game_text.get_width()) // 2, OUTER_HEIGHT - 60 + (50 - quit_game_text.get_height()) // 2))

    if game_over:
        if winner:
            text = small_font.render(f"{player_names[winner]} ({winner}) WINS!", True, RED)
            shadow = small_font.render(f"{player_names[winner]} ({winner}) WINS!", True, BLACK)
            screen.blit(shadow, (OUTER_WIDTH // 2 - text.get_width() // 2 + 2, OUTER_HEIGHT // 2 - text.get_height() // 2 + 2))
            screen.blit(text, (OUTER_WIDTH // 2 - text.get_width() // 2, OUTER_HEIGHT // 2 - text.get_height() // 2))
            draw_winning_effect()
        else:
            text = small_font.render("It's a draw!", True, RED)
            shadow = small_font.render("It's a draw!", True, BLACK)
            screen.blit(shadow, (OUTER_WIDTH // 2 - text.get_width() // 2 + 2, OUTER_HEIGHT // 2 - text.get_height() // 2 + 2))
            screen.blit(text, (OUTER_WIDTH // 2 - text.get_width() // 2, OUTER_HEIGHT // 2 - text.get_height() // 2))

    # Display winner counters at the bottom left corner
    counter_text_x = small_font.render(f"{player_names['X']} (X): {winner_counters['X']} wins", True, BLACK)
    counter_text_o = small_font.render(f"{player_names['O']} (O): {winner_counters['O']} wins", True, BLACK)
    counter_text_y = OUTER_HEIGHT - 60 - (OUTER_HEIGHT - INNER_HEIGHT) // 2 - counter_text_x.get_height() // 2
    screen.blit(counter_text_x, (10, OUTER_HEIGHT - 60 - counter_text_x.get_height() - 10))
    screen.blit(counter_text_o, (10, OUTER_HEIGHT - 30 - counter_text_o.get_height() - 10))
    pygame.display.flip()

pygame.quit()
sys.exit()
