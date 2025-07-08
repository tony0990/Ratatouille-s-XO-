import pygame
import sys
import copy # a hard copy for the board if things goes bad
from pygame import mixer
from datetime import datetime #player timer
import os #for paths
import time #Ai respond time
 #Get paths
script_dir = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(script_dir, "fx")

def get_asset_path(filename):
    return os.path.join(ASSETS_DIR, filename)

pygame.init()
mixer.init()

WIDTH, HEIGHT = 1280, 721 #main screen
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe!")
#board size , (space from top,right,bottom,left) , space for squares to play in it
OLD_BOARD_SIZE = 900
BOARD_OFFSET_900 = 33
CELL_SIZE_900 = 278

SCALED_BOARD_SIZE = HEIGHT #fit the board to the height we have (721)
BOARD_TOP_LEFT_X = (WIDTH - SCALED_BOARD_SIZE) // 1
BOARD_TOP_LEFT_Y = (HEIGHT - SCALED_BOARD_SIZE) // 1

SCALED_BOARD_OFFSET = int(0.0370 * SCALED_BOARD_SIZE) #ratio of top offset
SCALED_CELL_SIZE = int(0.31 * SCALED_BOARD_SIZE)
CELL_DRAW_SIZE = SCALED_CELL_SIZE
# for things to fit
BOARD_DRAW_OFFSET_X = BOARD_TOP_LEFT_X + SCALED_BOARD_OFFSET
BOARD_DRAW_OFFSET_Y = BOARD_TOP_LEFT_Y + SCALED_BOARD_OFFSET
BOARD_DRAW_END_X = BOARD_TOP_LEFT_X + SCALED_BOARD_OFFSET + 3 * SCALED_CELL_SIZE
BOARD_DRAW_END_Y = BOARD_TOP_LEFT_Y + SCALED_BOARD_OFFSET + 3 * SCALED_CELL_SIZE


BG_COLOR = (214, 201, 227)
MENU_COLOR = (180, 160, 200)
BUTTON_COLOR = (150, 130, 180)
HOVER_COLOR = (120, 100, 150)
TEXT_COLOR = (255, 255, 255)

TIMER_COLOR = (255, 0, 0)
WIN_LINE_COLOR = (255, 0, 0)

try:
    custom_font_path = get_asset_path("DancingScript-VariableFont_wght.ttf")
    font_large = pygame.font.Font(custom_font_path, 80)
    font_medium = pygame.font.Font(custom_font_path, 50)
    font_timer = pygame.font.Font(custom_font_path, 60)
    font_small = pygame.font.Font(custom_font_path, 30)
    font_game_over_msg = pygame.font.Font(custom_font_path, 60)
    font_game_over_button = pygame.font.Font(custom_font_path, 40)
    font_loaded_success = True
except pygame.error as e:
    print(f"Warning: Could not load font file: {e}. Falling back to system fonts.")
    font_large = pygame.font.SysFont('Arial', 80)
    font_medium = pygame.font.SysFont('Arial', 50)
    font_timer = pygame.font.SysFont('Arial', 60)
    font_small = pygame.font.SysFont('Arial', 30)
    font_game_over_msg = pygame.font.SysFont('Arial', 60, bold=True)
    font_game_over_button = pygame.font.SysFont('Arial', 40)
    font_loaded_success = False


try:
    BOARD_IMG_ORIGINAL = pygame.image.load(get_asset_path("Board.png")).convert_alpha()
    BOARD_IMG = pygame.transform.smoothscale(BOARD_IMG_ORIGINAL, (SCALED_BOARD_SIZE, SCALED_BOARD_SIZE))

    X_IMG_ORIGINAL = pygame.image.load(get_asset_path("X.png")).convert_alpha()
    O_IMG_ORIGINAL = pygame.image.load(get_asset_path("O.png")).convert_alpha()

    IMG_PADDING_RATIO = 60/278 #for x and o
    new_img_padding = int(IMG_PADDING_RATIO * CELL_DRAW_SIZE)
    scaled_size = max(10, CELL_DRAW_SIZE - 2 * new_img_padding)
    X_IMG = pygame.transform.smoothscale(X_IMG_ORIGINAL, (scaled_size, scaled_size))
    O_IMG = pygame.transform.smoothscale(O_IMG_ORIGINAL, (scaled_size, scaled_size))



    COVER_IMG = pygame.image.load(get_asset_path("cover.png")).convert_alpha()
    COVER2_IMG = pygame.image.load(get_asset_path("cover2.png")).convert_alpha()
    GAME_BG_IMG_ORIGINAL = pygame.image.load(get_asset_path("cover3.png")).convert_alpha()
    GAME_BG_IMG = pygame.transform.smoothscale(GAME_BG_IMG_ORIGINAL, (WIDTH, HEIGHT))


    HAPPY_IMG_FULL = pygame.image.load(get_asset_path("happy.png")).convert_alpha()
    SAD_IMG_FULL = pygame.image.load(get_asset_path("sad.png")).convert_alpha()
    DRAW_IMG_FULL = pygame.image.load(get_asset_path("draw.png")).convert_alpha()

    if COVER_IMG.get_size() != (WIDTH, HEIGHT):
         print(f"Warning: cover.png size {COVER_IMG.get_size()} does not match screen size {(WIDTH, HEIGHT)}. Scaling.")
         COVER_IMG = pygame.transform.smoothscale(COVER_IMG, (WIDTH, HEIGHT)) #makes image looks good even it's smaller
    if COVER2_IMG.get_size() != (WIDTH, HEIGHT):
         print(f"Warning: cover2.png size {COVER2_IMG.get_size()} does not match screen size {(WIDTH, HEIGHT)}. Scaling.")
         COVER2_IMG = pygame.transform.smoothscale(COVER2_IMG, (WIDTH, HEIGHT))

    GAMEOVER_IMG_SIZE = 200
    HAPPY_IMG_SCALED = pygame.transform.smoothscale(HAPPY_IMG_FULL, (GAMEOVER_IMG_SIZE, GAMEOVER_IMG_SIZE))
    SAD_IMG_SCALED = pygame.transform.smoothscale(SAD_IMG_FULL, (GAMEOVER_IMG_SIZE, GAMEOVER_IMG_SIZE))
    DRAW_IMG_SCALED = pygame.transform.smoothscale(DRAW_IMG_FULL, (GAMEOVER_IMG_SIZE, GAMEOVER_IMG_SIZE))


except pygame.error as e:
    print(f"Error loading images: {e}")
    BOARD_IMG = pygame.Surface((SCALED_BOARD_SIZE, SCALED_BOARD_SIZE))
    BOARD_IMG.fill(BG_COLOR)
    #to draw the 2 vertical and horizontal lines for the game and thickness is 4
    pygame.draw.line(BOARD_IMG, (0,0,0), (SCALED_BOARD_OFFSET + SCALED_CELL_SIZE, SCALED_BOARD_OFFSET), (SCALED_BOARD_OFFSET + SCALED_CELL_SIZE, SCALED_BOARD_OFFSET + 3 * SCALED_CELL_SIZE), 4)
    pygame.draw.line(BOARD_IMG, (0,0,0), (SCALED_BOARD_OFFSET + 2 * SCALED_CELL_SIZE, SCALED_BOARD_OFFSET), (SCALED_BOARD_OFFSET + 2 * SCALED_CELL_SIZE, SCALED_BOARD_OFFSET + 3 * SCALED_CELL_SIZE), 4)
    pygame.draw.line(BOARD_IMG, (0,0,0), (SCALED_BOARD_OFFSET, SCALED_BOARD_OFFSET + SCALED_CELL_SIZE), (SCALED_BOARD_OFFSET + 3 * SCALED_CELL_SIZE, SCALED_BOARD_OFFSET + SCALED_CELL_SIZE), 4)
    pygame.draw.line(BOARD_IMG, (0,0,0), (SCALED_BOARD_OFFSET, SCALED_BOARD_OFFSET + 2 * SCALED_CELL_SIZE), (SCALED_BOARD_OFFSET + 3 * SCALED_CELL_SIZE, SCALED_BOARD_OFFSET + 2 * SCALED_CELL_SIZE), 4)

    img_size = max(10, CELL_DRAW_SIZE - 2 * int(IMG_PADDING_RATIO * CELL_DRAW_SIZE))
    X_IMG = pygame.Surface((img_size, img_size), pygame.SRCALPHA) #new empty image / make it square / make it transparency
    #draws the horizontal lines for x
    pygame.draw.line(X_IMG, (200, 0, 0), (0, 0), (img_size, img_size), 15)
    pygame.draw.line(X_IMG, (200, 0, 0), (img_size, 0), (0, img_size), 15)
    O_IMG = pygame.Surface((img_size, img_size), pygame.SRCALPHA)
    pygame.draw.circle(O_IMG, (0, 0, 200), (img_size // 2, img_size // 2), img_size // 2 - 5, 15)


    COVER_IMG = pygame.Surface((WIDTH, HEIGHT))
    COVER_IMG.fill(MENU_COLOR)
    COVER2_IMG = pygame.Surface((WIDTH, HEIGHT))
    COVER2_IMG.fill(MENU_COLOR)
    GAME_BG_IMG = pygame.Surface((WIDTH, HEIGHT))
    GAME_BG_IMG.fill(BG_COLOR)

    if not font_loaded_success:
        fallback_text = pygame.font.SysFont('Arial', 80).render("Tic Tac Toe", True, TEXT_COLOR)
    else:
        fallback_text = font_large.render("Tic Tac Toe", True, TEXT_COLOR)



    HAPPY_IMG_FULL = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    HAPPY_IMG_FULL.fill((0, 255, 0, 50))
    SAD_IMG_FULL = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    SAD_IMG_FULL.fill((255, 0, 0, 50))
    DRAW_IMG_FULL = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    DRAW_IMG_FULL.fill((100, 100, 255, 50))

    GAMEOVER_IMG_SIZE = 200
    HAPPY_IMG_SCALED = pygame.transform.smoothscale(HAPPY_IMG_FULL, (GAMEOVER_IMG_SIZE, GAMEOVER_IMG_SIZE))
    SAD_IMG_SCALED = pygame.transform.smoothscale(SAD_IMG_FULL, (GAMEOVER_IMG_SIZE, GAMEOVER_IMG_SIZE))
    DRAW_IMG_SCALED = pygame.transform.smoothscale(DRAW_IMG_FULL, (GAMEOVER_IMG_SIZE, GAMEOVER_IMG_SIZE))


try:
    mixer.music.load(get_asset_path("LeFestin.wav"))
    click_sound = mixer.Sound(get_asset_path("click_sound.wav"))
    win_sound = mixer.Sound(get_asset_path("win_sound.wav"))
    lose_sound = mixer.Sound(get_asset_path("Lose.wav"))
    draw_sound = mixer.Sound(get_asset_path("draw.wav"))
    time_warning_sound = mixer.Sound(get_asset_path("TimeWarning.wav"))
    game_background_sound = mixer.Sound(get_asset_path("game.wav"))
    sound_loaded = True
except pygame.error as e:
    print(f"Error loading sounds: {e}")
    click_sound = win_sound = lose_sound = draw_sound = time_warning_sound = None
    sound_loaded = False


board = None
graphical_board = None
to_move = None
game_finished = None
winner = None
winning_line = None
player_symbol = None
ai_opponent_index = None
game_active = False

player_turn_start_time = None
TIME_LIMIT = 15
TIME_WARNING_THRESHOLD = 4
time_warning_played = False

ai_turn_start_time_perf = None
ai_thinking_duration = None

memoization_table = {}

STATE_START_MENU = 0
STATE_AI_SELECTION = 1
STATE_SYMBOL_SELECTION = 2
STATE_GAME_ACTIVE = 3
STATE_GAME_OVER = 4
current_state = STATE_START_MENU

AI_BLOCK_FORK = 2
AI_BLOCK_THREATS = 99
AI_MINIMAX = 100
AI_MINIMAX_BLOCK_FORK = 101
AI_MINIMAX_BLOCK_THREATS = 102
AI_MINIMAX_ALPHA_BETA = 103
AI_MINIMAX_HEURISTIC_REDUCTION = 104
AI_MINIMAX_SYMMETRY_REDUCTION = 105


ai_options = [
    "Minimax",
    "Heuristic: Block Fork",
    "Heuristic: Block Threats",
    "Minimax + Block Fork",
    "Minimax + Block Threats",
    "Minimax + Alpha-Beta Pruning",
    "Heuristic Reduction",
    "Symmetry Reduction"
]

ai_menu_map = {
    0: AI_MINIMAX,
    1: AI_BLOCK_FORK,
    2: AI_BLOCK_THREATS,
    3: AI_MINIMAX_BLOCK_FORK,
    4: AI_MINIMAX_BLOCK_THREATS,
    5: AI_MINIMAX_ALPHA_BETA,
    6: AI_MINIMAX_HEURISTIC_REDUCTION,
    7: AI_MINIMAX_SYMMETRY_REDUCTION
}


start_menu_buttons = []
ai_selection_buttons = []
symbol_selection_buttons = []
game_over_buttons = []

def play_sound(sound): #win/lose/draw
    if sound and pygame.mixer.get_init() and sound_loaded:
        try:
            sound.play()
        except pygame.error as e:
            print(f"Error playing sound: {e}")


def play_music(music_filename): #main music
     if pygame.mixer.get_init() and sound_loaded:
         try:
             full_path = get_asset_path(music_filename)
             mixer.music.stop()
             mixer.music.load(full_path)
             mixer.music.play(-1)
         except pygame.error as e:
             print(f"Error playing music file ({music_filename}): {e}")

def stop_music():
    if pygame.mixer.get_init() and sound_loaded:
        mixer.music.stop()

def play_game_background_sound():#game music
    if game_background_sound and pygame.mixer.get_init() and sound_loaded:
        try:
            game_background_sound.play(-1)
        except pygame.error as e:
            print(f"Error playing game background sound: {e}")

def stop_game_background_sound():
    if game_background_sound and pygame.mixer.get_init() and sound_loaded:
        try:
            game_background_sound.stop()
        except pygame.error as e:
            print(f"Error stopping game background sound: {e}")


def draw_button(text, x, y, width, height, hover=False): #text in button , top-left coordinates , size
    button_surface = pygame.Surface((width, height), pygame.SRCALPHA)

    bg_color = HOVER_COLOR if hover else BUTTON_COLOR

    semi_transparent_color = (bg_color[0], bg_color[1], bg_color[2], 150)
    pygame.draw.rect(button_surface, semi_transparent_color, (0, 0, width, height), border_radius=10) # redius makes the rectangle rounded

    button_font_size = 50 if len(text) < 35 else 40
    if font_loaded_success:
        button_font = pygame.font.Font(get_asset_path("DancingScript-VariableFont_wght.ttf"), button_font_size)
    else:
        button_font = pygame.font.SysFont('Arial', button_font_size)

    button_text_surf = button_font.render(text, True, TEXT_COLOR) # changes text to pygamesurface(image) to make it smoother
    button_text_rect = button_text_surf.get_rect(center=(width / 2, height / 2)) # text in rectangle
    button_surface.blit(button_text_surf, button_text_rect) # copies the pixels of img from one surface to another (source, destination)

    SCREEN.blit(button_surface, (x, y)) # cpying the images in the main game screen

    return pygame.Rect(x, y, width, height)


def draw_start_menu():
    SCREEN.blit(COVER_IMG, (0, 0))
    buttons = []
    button_width = 300
    button_height = 70
    button_spacing = 20
    button_margin = 50

    total_buttons_height = 2 * button_height + button_spacing
    start_y = HEIGHT - total_buttons_height - button_margin
    new_game_rect = draw_button("New Game", button_margin, start_y, button_width, button_height)
    buttons.append(new_game_rect)
    exit_rect = draw_button("Exit", button_margin, start_y + button_height + button_spacing, button_width, button_height)
    buttons.append(exit_rect)

    if pygame.mixer.get_init() and sound_loaded and not mixer.music.get_busy():
         play_music("LeFestin.wav")

    pygame.display.flip()
    return buttons


def draw_main_menu(title, options):
    SCREEN.blit(COVER2_IMG, (0, 0))
    if font_loaded_success:
        title_surf = pygame.font.Font(get_asset_path("DancingScript-VariableFont_wght.ttf"), 80).render(title, True, TEXT_COLOR)
    else:
        title_surf = pygame.font.SysFont('Arial', 80).render(title, True, TEXT_COLOR)

    title_rect = title_surf.get_rect(center=(WIDTH / 2, HEIGHT / 8))
    SCREEN.blit(title_surf, title_rect)
    buttons = []
    num_options = len(options)
    button_width = min(WIDTH - 80, 800)
    button_height = 60
    button_gap = 15

    total_buttons_height = num_options * button_height + (num_options - 1) * button_gap

    available_height = HEIGHT - title_rect.bottom - 40

    if total_buttons_height > available_height:
        button_height = max(40, int(available_height / num_options - button_gap))
        total_buttons_height = num_options * button_height + (num_options - 1) * button_gap

    start_y = title_rect.bottom + (available_height - total_buttons_height) // 2


    for i, option in enumerate(options):
        btn_x = WIDTH / 2 - button_width / 2
        btn_y = start_y + i * (button_height + button_gap)
        btn_rect = draw_button(option, btn_x, btn_y, button_width, button_height)
        buttons.append(btn_rect)


    if pygame.mixer.get_init() and sound_loaded and not mixer.music.get_busy():
         play_music("LeFestin.wav")

    pygame.display.flip()
    return buttons


def draw_game_over_message(winner_symbol, player_sym):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    SCREEN.blit(overlay, (0, 0))


    message = ""
    game_over_image_full = None

    if winner_symbol == 'DRAW':
        message = "It's a draw"
        game_over_image_full = DRAW_IMG_FULL
    elif winner_symbol == player_sym:
        message = "YOU WIN !"
        game_over_image_full = HAPPY_IMG_FULL
    else:
        message = "You lose.."
        game_over_image_full = SAD_IMG_FULL

    if game_over_image_full:
        image_with_elements = game_over_image_full.copy() # draw the player status without changing the image

        msg_surf = font_game_over_msg.render(message, True, (255, 255, 255)) #Enables anti-aliasing for smooth text / msg color

        msg_rect_on_image = msg_surf.get_rect(center=(image_with_elements.get_width() / 2, image_with_elements.get_height() / 2 - 50)) #center text

        image_with_elements.blit(msg_surf, msg_rect_on_image)

        image_rect_on_screen = image_with_elements.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        SCREEN.blit(image_with_elements, image_rect_on_screen)


def draw_game_over_button(mouse_pos):
    button_text = "Back to Menu"
    button_width = 300
    button_height = 70
    button_margin_bottom = 30

    button_x = WIDTH / 2 - button_width / 2
    button_y = HEIGHT - button_height - button_margin_bottom

    button_rect = pygame.Rect(button_x, button_y, button_width, button_height) #detect if i click on the button

    is_hover = button_rect.collidepoint(mouse_pos) #mouse cursor is currently touching

    button_surface = pygame.Surface((button_width, button_height), pygame.SRCALPHA)

    bg_color = (255, 255, 255, 150)
    pygame.draw.rect(button_surface, bg_color, (0, 0, button_width, button_height), border_radius=10)

    button_text_surf = font_game_over_button.render(button_text, True, (255, 255, 255))
    button_text_rect = button_text_surf.get_rect(center=(button_width / 2, button_height / 2))
    button_surface.blit(button_text_surf, button_text_rect)

    SCREEN.blit(button_surface, (button_x, button_y))

    return button_rect


def draw_board_and_pieces():
    SCREEN.blit(GAME_BG_IMG, (0, 0))

    SCREEN.blit(BOARD_IMG, (BOARD_TOP_LEFT_X, BOARD_TOP_LEFT_Y))

    for r in range(3):
        for c in range(3):
            if graphical_board[r][c][0] is not None:
                SCREEN.blit(graphical_board[r][c][0], graphical_board[r][c][1])

    if game_finished and winner not in ['DRAW', None] and winning_line:
        draw_winning_line()

    if game_active and not game_finished:
        if to_move == player_symbol and player_turn_start_time:
            elapsed = (datetime.now() - player_turn_start_time).total_seconds()
            remaining = max(0, TIME_LIMIT - elapsed)
            timer_color = TIMER_COLOR if remaining < (TIME_WARNING_THRESHOLD + 1) else TEXT_COLOR
            global time_warning_played
            if remaining < TIME_WARNING_THRESHOLD and not time_warning_played:
                play_sound(time_warning_sound)
                time_warning_played = True
            elif remaining >= (TIME_WARNING_THRESHOLD + 1):
                time_warning_played = False
            timer_text = font_timer.render(f"Time: {int(remaining)}s", True, timer_color)
            SCREEN.blit(timer_text, (WIDTH - timer_text.get_width() - 1000, 650))

        elif to_move != player_symbol:
            active_ai_name = "AI Thinking"
            display_name_key = next((key for key, value in ai_menu_map.items() if value == ai_opponent_index), None)
            if display_name_key is not None and display_name_key < len(ai_options):
                 active_ai_name = f"AI ({ai_options[display_name_key]})"

            display_ai_name = active_ai_name[:25] + "..." if len(active_ai_name) > 28 else active_ai_name
            thinking_text = font_medium.render(display_ai_name, True, TEXT_COLOR)
            SCREEN.blit(thinking_text, (20, 20))


    if game_active and pygame.mixer.get_init() and sound_loaded and mixer.music.get_busy():
         stop_music()

    pygame.display.flip()


def draw_winning_line():
    line_type, index = winning_line
    start_pos = None
    end_pos = None
    center_offset = CELL_DRAW_SIZE / 2

    board_start_x = BOARD_DRAW_OFFSET_X
    board_start_y = BOARD_DRAW_OFFSET_Y
    board_end_x = BOARD_DRAW_OFFSET_X + 3 * CELL_DRAW_SIZE
    board_end_y = BOARD_DRAW_OFFSET_Y + 3 * CELL_DRAW_SIZE

    line_margin = CELL_DRAW_SIZE * 0.15

    if line_type == 'row':
        y = board_start_y + index * CELL_DRAW_SIZE + center_offset
        start_pos = (board_start_x + line_margin, y)
        end_pos = (board_end_x - line_margin, y)
    elif line_type == 'col':
        x = board_start_x + index * CELL_DRAW_SIZE + center_offset
        start_pos = (x, board_start_y + line_margin)
        end_pos = (x, board_end_y - line_margin)
    elif line_type == 'diag':
        if index == 0:
            start_pos = (board_start_x + line_margin, board_start_y + line_margin)
            end_pos = (board_end_x - line_margin, board_end_y - line_margin)
        else:
            start_pos = (board_end_x - line_margin, board_start_y + line_margin)
            end_pos = (board_start_x + line_margin, board_end_y - line_margin)

    if start_pos and end_pos:
        pygame.draw.line(SCREEN, WIN_LINE_COLOR, start_pos, end_pos, 15)

def reset_game():
    global board, graphical_board, to_move, game_finished, winner, winning_line
    global game_active
    global player_turn_start_time, TIME_LIMIT, TIME_WARNING_THRESHOLD, time_warning_played
    global ai_turn_start_time_perf, ai_thinking_duration
    global memoization_table

    board = [[None for _ in range(3)] for _ in range(3)]
    graphical_board = [[[None, None] for _ in range(3)] for _ in range(3)]
    to_move = 'X'
    game_finished = False
    winner = None
    winning_line = None
    game_active = True

    player_turn_start_time = None
    time_warning_played = False

    ai_turn_start_time_perf = None
    ai_thinking_duration = None

    memoization_table = {}

    if player_symbol == 'O' and to_move == 'X':
         ai_turn_start_time_perf = time.perf_counter()
         pygame.time.set_timer(pygame.USEREVENT + 1, 500, 1)
    elif player_symbol == 'X':
         player_turn_start_time = datetime.now()


    draw_board_and_pieces()


def update_graphical_board(r, c, symbol):
    img = X_IMG if symbol == 'X' else O_IMG

    center_x = BOARD_DRAW_OFFSET_X + c * CELL_DRAW_SIZE + CELL_DRAW_SIZE / 2
    center_y = BOARD_DRAW_OFFSET_Y + r * CELL_DRAW_SIZE + CELL_DRAW_SIZE / 2

    rect = img.get_rect(center=(center_x, center_y))
    graphical_board[r][c] = [img, rect]


def add_XO(r, c):
    global board, to_move, game_finished, winner, winning_line
    global current_state, game_active
    global player_turn_start_time, time_warning_played
    global ai_turn_start_time_perf, ai_thinking_duration

    if not game_active or game_finished or 0 > r or r > 2 or 0 > c or c > 2 or board[r][c] is not None:
        return

    current_player = to_move
    board[r][c] = current_player
    update_graphical_board(r, c, current_player)
    play_sound(click_sound)

    win_info = check_win_pure(board)
    if win_info:
        game_finished = True
        winner = win_info['winner']
        winning_line = win_info.get('line')
        stop_game_background_sound()
        if winner == player_symbol:
             play_sound(win_sound)
        elif winner != 'DRAW':
             play_sound(lose_sound)
        else:
             play_sound(draw_sound)

        to_move = None
        game_active = False
        current_state = STATE_GAME_OVER
        stop_music()
        ai_turn_start_time_perf = None
        ai_thinking_duration = None
        player_turn_start_time = None
        time_warning_played = False
    else:
        to_move = 'O' if current_player == 'X' else 'X'
        if to_move == player_symbol:
            player_turn_start_time = datetime.now()
            time_warning_played = False
            ai_turn_start_time_perf = None
            ai_thinking_duration = None
        else:
            player_turn_start_time = None
            ai_turn_start_time_perf = time.perf_counter()
            ai_thinking_duration = None
            pygame.time.set_timer(pygame.USEREVENT + 1, 500, 1)

    draw_board_and_pieces()


def check_win_pure(current_board):
    for r in range(3):
        if current_board[r][0] == current_board[r][1] == current_board[r][2] and current_board[r][0] is not None:
            return {'winner': current_board[r][0], 'line': ('row', r)}

    for c in range(3):
        if current_board[0][c] == current_board[1][c] == current_board[2][c] and current_board[0][c] is not None:
            return {'winner': current_board[0][c], 'line': ('col', c)}

    if current_board[0][0] == current_board[1][1] == current_board[2][2] and current_board[0][0] is not None:
            return {'winner': current_board[0][0], 'line': ('diag', 0)}
    if current_board[0][2] == current_board[1][1] == current_board[2][0] and current_board[0][2] is not None:
            return {'winner': current_board[0][2], 'line': ('diag', 1)}

    if all(cell is not None for row in current_board for cell in row):
        return {'winner': 'DRAW'}

    return None


def get_empty_cells(current_board):
    return [(r, c) for r in range(3) for c in range(3) if current_board[r][c] is None]
#list of all the empty spots on the board


def find_win_or_block(current_board, symbol):
    empty_cells = get_empty_cells(current_board)
    for r, c in empty_cells:
        temp_board = copy.deepcopy(current_board)
        temp_board[r][c] = symbol
        win_info = check_win_pure(temp_board)
        if win_info and win_info['winner'] == symbol:
            return (r, c)
    return None


def find_fork(current_board, symbol):
    empty_cells = get_empty_cells(current_board)

    for r, c in empty_cells:
        temp_board = copy.deepcopy(current_board)
        temp_board[r][c] = symbol

        if check_win_pure(temp_board) and check_win_pure(temp_board)['winner'] == symbol:
             continue

        winning_opportunities = 0
        potential_next_moves = get_empty_cells(temp_board)
        for r2, c2 in potential_next_moves:
            temp_board_2 = copy.deepcopy(temp_board)
            temp_board_2[r2][c2] = symbol
            if check_win_pure(temp_board_2) and check_win_pure(temp_board_2)['winner'] == symbol:
                 winning_opportunities += 1

        if winning_opportunities >= 2:
            return (r, c)

    return None


def find_block_threat_move(current_board, opponent_symbol):
    empty_cells = get_empty_cells(current_board)

    lines = []
    for r in range(3): lines.append([(r, c) for c in range(3)])
    for c in range(3): lines.append([(r, c) for r in range(3)])
    lines.append([(i, i) for i in range(3)])
    lines.append([(i, 2 - i) for i in range(3)])

    for line_coords in lines:
        line_values = [current_board[r][c] for r, c in line_coords]

        if line_values.count(opponent_symbol) == 2 and line_values.count(None) == 1:
            for r_spot, c_spot in line_coords:
                if current_board[r_spot][c_spot] is None:
                    return (r_spot, c_spot)

    return None

def minimax(current_board, depth, is_maximizing, player):
    opponent = 'O' if player == 'X' else 'X'
    result = check_win_pure(current_board)

    if result:
        if result['winner'] == player:
            return 10 - depth
        elif result['winner'] == opponent:
            return depth - 10
        else:
            return 0

    if is_maximizing:
        best_score = -float('inf') #assuming the worst possible score.
        for r, c in get_empty_cells(current_board):
            current_board[r][c] = player
            score = minimax(current_board, depth + 1, False, player)
            current_board[r][c] = None
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for r, c in get_empty_cells(current_board):
            current_board[r][c] = opponent
            score = minimax(current_board, depth + 1, True, player)
            current_board[r][c] = None
            best_score = min(score, best_score)
        return best_score

def minimax_alpha_beta(current_board, depth, is_maximizing, player, alpha, beta):
    opponent = 'O' if player == 'X' else 'X'
    result = check_win_pure(current_board)

    if result:
        if result['winner'] == player:
            return 10 - depth
        elif result['winner'] == opponent:
            return depth - 10
        else:
            return 0

    if is_maximizing:
        best_score = -float('inf')
        for r, c in get_empty_cells(current_board):
            current_board[r][c] = player
            score = minimax_alpha_beta(current_board, depth + 1, False, player, alpha, beta)
            current_board[r][c] = None
            best_score = max(score, best_score)

            alpha = max(alpha, best_score)
            if beta <= alpha:   # If the opponent's "best" move (beta) is already worse than our "best" move (alpha),

                break

        return best_score
    else:
        best_score = float('inf')
        for r, c in get_empty_cells(current_board):
            current_board[r][c] = opponent
            score = minimax_alpha_beta(current_board, depth + 1, True, player, alpha, beta)
            current_board[r][c] = None
            best_score = min(score, best_score)

            beta = min(beta, best_score)
            if beta <= alpha:# If our "best" score (alpha) is already better than the opponent's "best" move (beta),

                break

        return best_score

def board_to_tuple(current_board):
    return tuple('' if cell is None else cell for row in current_board for cell in row)

def tuple_to_board(board_tuple):
    board_list = [[None for _ in range(3)] for _ in range(3)]
    for i in range(9):
        board_list[i // 3][i % 3] = None if board_tuple[i] == '' else board_tuple[i]
    return board_list

def rotate_board(current_board):
    return [list(row) for row in zip(*current_board[::-1])] #rotats the board upside down and zip to swape the columns and rows

def flip_board_horizontal(current_board):
    return [row[::-1] for row in current_board] #swape the board from left to right and reverse the order for each item in the row

def get_all_symmetries(current_board):
    symmetries = [copy.deepcopy(current_board)]
    rotated_board = copy.deepcopy(current_board)

    for _ in range(3):# It rotates the board 3 times (90, 180, 270 degrees)

        rotated_board = rotate_board(rotated_board)
        symmetries.append(copy.deepcopy(rotated_board)) # Adds each rotated version to the list of symmetries

    for sym in symmetries.copy():
        flipped_sym = flip_board_horizontal(sym)
        if flipped_sym not in symmetries:
            symmetries.append(flipped_sym)

    return symmetries

def canonicalize_board(current_board):
    symmetries = get_all_symmetries(current_board)
    canonical_tuple = min(board_to_tuple(sym) for sym in symmetries) # It converts each symmetrical board view into a flat list (tuple)
    return canonical_tuple

def transform_move(move, original_board, canonical_board_tuple):
    r, c = move
    original_tuple = board_to_tuple(original_board)

    symmetries_with_moves = []
    temp_board = copy.deepcopy(original_board)
    temp_r, temp_c = r, c

    for i in range(4):
        symmetries_with_moves.append((board_to_tuple(temp_board), (temp_r, temp_c)))
        temp_board = rotate_board(temp_board)
        temp_r, temp_c = temp_c, 2 - temp_r

    temp_board = flip_board_horizontal(copy.deepcopy(original_board))
    temp_r, temp_c = r, c
    temp_r, temp_c = temp_r, 2 - temp_c
    symmetries_with_moves.append((board_to_tuple(temp_board), (temp_r, temp_c)))

    temp_board = rotate_board(temp_board)
    temp_r, temp_c = temp_c, 2 - temp_r
    symmetries_with_moves.append((board_to_tuple(temp_board), (temp_r, temp_c)))

    temp_board = rotate_board(temp_board)
    temp_r, temp_c = temp_c, 2 - temp_r
    symmetries_with_moves.append((board_to_tuple(temp_board), (temp_r, temp_c)))

    temp_board = rotate_board(temp_board)
    temp_r, temp_c = temp_c, 2 - temp_r
    symmetries_with_moves.append((board_to_tuple(temp_board), (temp_r, temp_c)))


    for sym_tuple, transformed_move in symmetries_with_moves:
        if sym_tuple == canonical_board_tuple:
            if 0 <= transformed_move[0] < 3 and 0 <= transformed_move[1] < 3 and original_board[transformed_move[0]][transformed_move[1]] is None:
                 return transformed_move
            else:
                 print("Warning: Symmetry move transformation resulted in an invalid move. Recalculating.")

    return move


def find_best_move(current_board, player, algorithm_index):
    opponent = 'O' if player == 'X' else 'X'
    empty_cells = get_empty_cells(current_board)

    if not empty_cells:
        return (-1, -1)

    win_move = find_win_or_block(current_board, player)
    if win_move:
        return win_move

    block_move = find_win_or_block(current_board, opponent)
    if block_move:
        return block_move

    if algorithm_index == AI_BLOCK_FORK:
        if current_board[1][1] is None:
             return (1, 1)

        block_fork_move = find_fork(current_board, opponent)
        if block_fork_move:
            return block_fork_move

        empty_cells = get_empty_cells(current_board)
        if empty_cells:
            return empty_cells[0]
        else:
            return (-1, -1)


    elif algorithm_index == AI_BLOCK_THREATS:
        block_threat_move = find_block_threat_move(current_board, opponent)
        if block_threat_move:
             return block_threat_move
        return empty_cells[0]

    elif algorithm_index == AI_MINIMAX:
        best_score = -float('inf')
        best_move = (-1, -1)

        for r, c in empty_cells:
            current_board[r][c] = player
            score = minimax(current_board, 0, False, player)
            current_board[r][c] = None

            if score > best_score:
                best_score = score
                best_move = (r, c)

        return best_move if best_move != (-1, -1) else empty_cells[0]

    elif algorithm_index == AI_MINIMAX_BLOCK_FORK:
        block_fork_move = find_fork(current_board, opponent)
        if block_fork_move:
            return block_fork_move

        best_score = -float('inf')
        best_move = (-1, -1)
        alpha = -float('inf')
        beta = float('inf')

        for r, c in empty_cells:
            current_board[r][c] = player
            score = minimax(current_board, 0, False, player)
            current_board[r][c] = None
            if score > best_score:
                best_score = score
                best_move = (r, c)
            alpha = max(alpha, best_score)


        return best_move if best_move != (-1, -1) else empty_cells[0]

    elif algorithm_index == AI_MINIMAX_BLOCK_THREATS:
        block_threat_move = find_block_threat_move(current_board, opponent)
        if block_threat_move:
             return block_threat_move

        best_score = -float('inf')
        best_move = (-1, -1)
        alpha = -float('inf')
        beta = float('inf')
        for r, c in empty_cells:
            current_board[r][c] = player
            score =minimax(current_board, 0, False, player)
            current_board[r][c] = None
            if score > best_score:
                best_score = score
                best_move = (r, c)
            alpha = max(alpha, best_score)

        return best_move if best_move != (-1, -1) else empty_cells[0]

    elif algorithm_index == AI_MINIMAX_ALPHA_BETA:
        best_score = -float('inf')
        best_move = (-1, -1)
        alpha = -float('inf')
        beta = float('inf')

        for r, c in empty_cells:
            current_board[r][c] = player
            score = minimax_alpha_beta(current_board, 0, False, player, alpha, beta)
            current_board[r][c] = None

            if score > best_score:
                best_score = score
                best_move = (r, c)
            alpha = max(alpha, best_score)


        return best_move if best_move != (-1, -1) else empty_cells[0]

    elif algorithm_index == AI_MINIMAX_HEURISTIC_REDUCTION:
        fork_move = find_fork(current_board, player)
        block_fork_move = find_fork(current_board, opponent)

        if fork_move:
             return fork_move
        if block_fork_move:
             return block_fork_move

        best_score = -float('inf')
        best_move = (-1, -1)
        alpha = -float('inf')
        beta = float('inf')

        for r, c in empty_cells:
            current_board[r][c] = player
            score = minimax_alpha_beta(current_board, 0, False, player, alpha, beta)
            current_board[r][c] = None

            if score > best_score:
                best_score = score
                best_move = (r, c)
            alpha = max(alpha, best_score)

        return best_move if best_move != (-1, -1) else empty_cells[0]


    elif algorithm_index == AI_MINIMAX_SYMMETRY_REDUCTION:
        canonical_board_tuple = canonicalize_board(current_board)

        if canonical_board_tuple in memoization_table:
            canonical_best_move = memoization_table[canonical_board_tuple]
            transformed_move = transform_move(canonical_best_move, current_board, canonical_board_tuple)
            if 0 <= transformed_move[0] < 3 and 0 <= transformed_move[1] < 3 and current_board[transformed_move[0]][transformed_move[1]] is None:
                 return transformed_move
            else:
                 print("Warning: Symmetry transformation resulted in an invalid move. Recalculating.")

        best_score = -float('inf')
        best_move = (-1, -1)
        alpha = -float('inf')
        beta = float('inf')

        for r, c in empty_cells:
            current_board[r][c] = player
            score = minimax_alpha_beta(current_board, 0, False, player, alpha, beta)
            current_board[r][c] = None

            if score > best_score:
                best_score = score
                best_move = (r, c)
            alpha = max(alpha, best_score)

        if best_move != (-1, -1):
             memoization_table[canonical_board_tuple] = best_move

        return best_move if best_move != (-1, -1) else empty_cells[0]


    else:
        print(f"Warning: Unknown AI algorithm index: {algorithm_index}. Using first empty cell.")
        return empty_cells[0]


running = True
play_music("LeFestin.wav")

game_over_menu_button_rect = None

while running:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()

        if current_state == STATE_START_MENU:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if start_menu_buttons[0].collidepoint(event.pos):
                        current_state = STATE_AI_SELECTION
                        play_sound(click_sound)
                    elif start_menu_buttons[1].collidepoint(event.pos):
                        running = False
                        sys.exit()

        elif current_state == STATE_AI_SELECTION:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i, button in enumerate(ai_selection_buttons):
                        if button.collidepoint(event.pos):
                            ai_opponent_index = ai_menu_map[i]
                            current_state = STATE_SYMBOL_SELECTION
                            play_sound(click_sound)

                            break

        elif current_state == STATE_SYMBOL_SELECTION:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if symbol_selection_buttons[0].collidepoint(event.pos):
                        player_symbol = 'X'
                        stop_music()
                        reset_game()
                        play_game_background_sound()
                        current_state = STATE_GAME_ACTIVE
                        play_sound(click_sound)

                    elif symbol_selection_buttons[1].collidepoint(event.pos):
                        player_symbol = 'O'
                        stop_music()
                        reset_game()
                        play_game_background_sound()
                        current_state = STATE_GAME_ACTIVE
                        play_sound(click_sound)


        elif current_state == STATE_GAME_ACTIVE:

            if not game_finished:
                if to_move == player_symbol:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            mouse_x, mouse_y = event.pos
                            if BOARD_DRAW_OFFSET_X <= mouse_x <= BOARD_DRAW_END_X and \
                               BOARD_DRAW_OFFSET_Y <= mouse_y <= BOARD_DRAW_END_Y:
                                clicked_row = int((mouse_y - BOARD_DRAW_OFFSET_Y) // CELL_DRAW_SIZE)
                                clicked_col = int((mouse_x - BOARD_DRAW_OFFSET_X) // CELL_DRAW_SIZE)
                                add_XO(clicked_row, clicked_col)

                    if player_turn_start_time:
                         elapsed = (datetime.now() - player_turn_start_time).total_seconds()
                         if elapsed >= TIME_LIMIT:
                             print(f"{player_symbol} timed out!")
                             game_finished = True
                             winner = 'O' if player_symbol == 'X' else 'X'
                             winning_line = None
                             game_active = False
                             current_state = STATE_GAME_OVER
                             play_music("LeFestin.wav")


                elif to_move != player_symbol:
                    if event.type == pygame.USEREVENT + 1:
                         if game_active and not game_finished and to_move != player_symbol:
                             ai_turn_start_time_perf = time.perf_counter()

                             ai_move = find_best_move(board, to_move, ai_opponent_index)


                             if ai_turn_start_time_perf is not None:
                                 ai_thinking_duration = (time.perf_counter() - ai_turn_start_time_perf)
                                 ai_turn_start_time_perf = None
                                 print(f"AI ({ai_options[next(key for key, value in ai_menu_map.items() if value == ai_opponent_index)]}) Thought: {ai_thinking_duration * 1000:.3f} ms")


                             if ai_move != (-1, -1):
                                 add_XO(ai_move[0], ai_move[1])
                             else:
                                 print("AI could not find a move!")
                                 game_finished = True
                                 winner = 'DRAW'
                                 winning_line = None
                                 game_active = False
                                 current_state = STATE_GAME_OVER
                                 play_music("LeFestin.wav")


        elif current_state == STATE_GAME_OVER:

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if game_over_menu_button_rect and game_over_menu_button_rect.collidepoint(event.pos):
                        current_state = STATE_START_MENU
                        play_sound(click_sound)
                        reset_game()
                        game_active = False
                        winner = None
                        winning_line = None
                        board = None
                        graphical_board = None
                        game_over_menu_button_rect = None


    if current_state == STATE_START_MENU:
        start_menu_buttons = draw_start_menu()
        ai_selection_buttons = []
        symbol_selection_buttons = []
        game_over_buttons = []
        game_over_menu_button_rect = None

    elif current_state == STATE_AI_SELECTION:
        ai_selection_buttons = draw_main_menu("Select AI Opponent", ai_options)
        start_menu_buttons = []
        symbol_selection_buttons = []
        game_over_buttons = []
        game_over_menu_button_rect = None

    elif current_state == STATE_SYMBOL_SELECTION:
        symbol_selection_buttons = draw_main_menu("Play as...", ["X", "O"])
        start_menu_buttons = []
        ai_selection_buttons = []
        game_over_buttons = []
        game_over_menu_button_rect = None

    elif current_state == STATE_GAME_ACTIVE:
        draw_board_and_pieces()
        start_menu_buttons = []
        ai_selection_buttons = []
        symbol_selection_buttons = []
        game_over_buttons = []
        game_over_menu_button_rect = None

    elif current_state == STATE_GAME_OVER:
        draw_game_over_message(winner, player_symbol)
        game_over_menu_button_rect = draw_game_over_button(mouse_pos)
        start_menu_buttons = []
        ai_selection_buttons = []
        symbol_selection_buttons = []
        game_over_buttons = []

    pygame.display.flip()


pygame.quit()
sys.exit()
