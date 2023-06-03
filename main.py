import pygame
import sys
import os
# Initialize pygame
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(os.path.join(os.getcwd(),'background_music.mp3'))


# Set the screen dimensions
screen_width, screen_height = 1080,2400
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the colors
BLACK = (0, 0, 0)
WHITE = (0,0,0)
BLUE = (135, 206, 235)
RED = (144, 238, 144)
R = (255, 0, 0)
B = (0, 0, 255)

# Set the font
font = pygame.font.SysFont(None, 200)

# Load the sound effects
touch_sound = pygame.mixer.Sound("touch.mp3")

# Set the background music
pygame.mixer.music.load("background_music.mp3")
#pygame.mixer.music.load("touch.mp3")

pygame.mixer.music.play(-1)  # -1 indicates loop indefinitely

# Set the game variables
cell_size = 200
cell_spacing = 20
board_size = cell_size * 3 + cell_spacing * 2
board_x = (screen_width - board_size) // 2
board_y = (screen_height - board_size) // 2
game_board = [["", "", ""],
              ["", "", ""],
              ["", "", ""]]
current_player = "X"
game_over = False

def check_game_over():
    for row in game_board:
        if row[0] == row[1] == row[2] != "":
            return True
    for col in range(3):
        if game_board[0][col] == game_board[1][col] == game_board[2][col] != "":
            return True
    if game_board[0][0] == game_board[1][1] == game_board[2][2] != "":
        return True
    if game_board[0][2] == game_board[1][1] == game_board[2][0] != "":
        return True
    if all(game_board[i][j] != "" for i in range(3) for j in range(3)):
        return True
    return False

def handle_click(pos):
    global current_player, game_over
    if not game_over:
        row = (pos[1] - board_y) // (cell_size + cell_spacing)
        col = (pos[0] - board_x) // (cell_size + cell_spacing)
        if game_board[row][col] == "":
            game_board[row][col] = current_player
            touch_sound.play()
            if check_game_over():
                game_over = True
            current_player = "O" if current_player == "X" else "X"

def restart_game():
    global game_board, current_player, game_over
    game_board = [["", "", ""], ["", "", ""], ["", "", ""]]
    current_player = "X"
    game_over = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if restart_button_rect.collidepoint(event.pos):
                restart_game()
            else:
                handle_click(event.pos)

    screen.fill(BLACK)

    for row in range(3):
        for col in range(3):
            cell_x = board_x + col * (cell_size + cell_spacing) + cell_spacing
            cell_y = board_y + row * (cell_size + cell_spacing) + cell_spacing
            pygame.draw.rect(screen, BLUE, (cell_x, cell_y, cell_size, cell_size))

    for row in range(3):
        for col in range(3):
            cell_value = game_board[row][col]
            if cell_value != "":
                cell_text = font.render(cell_value, True, WHITE)
                cell_text_rect = cell_text.get_rect(center=(board_x + col * (cell_size + cell_spacing) + cell_size // 2,
                                                             board_y + row * (cell_size + cell_spacing) + cell_size // 2))
                screen.blit(cell_text, cell_text_rect)

    restart_button_text = font.render("Restart", True, B)
    restart_button_rect = restart_button_text.get_rect(center=(screen_width // 2, board_y + board_size + 100))
    pygame.draw.rect(screen, RED, restart_button_rect)
    screen.blit(restart_button_text, restart_button_rect)

    if game_over:
        message = ""
        if check_game_over():
            winner = "O" if current_player == "X" else "X"
            message = f"{winner} wins!"
        else:
            message = "It's a tie!"
        message_text = font.render(message, True, R)
        message_rect = message_text.get_rect(center=(screen_width // 2, board_y - 100))
        screen.blit(message_text, message_rect)

    pygame.display.update()

pygame.quit()
sys.exit()
