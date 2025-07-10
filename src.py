import pygame
import sys
import random
import numpy as np
from pygame.locals import *   # Common Pygame constants (e.g., QUIT, MOUSEBUTTONDOWN)

# Initialize pygame
pygame.init()

# Colors (Red, Green, Blue) - 0 means no intensity (dark), 255 means full intensity (bright)
WHITE = (255, 255, 255)        # Background & grid lines
BLACK = (0, 0, 0)              # Text, Borders and Misses
BLUE = (0, 0, 255)             # Player ship color

RED = (255, 0, 0)              # Hard Color & AI ship color(only visible internally)
YELLOW = (255, 255, 0)         # Moderate button
GREEN = (0, 255, 0)            # Easy button & Hits

GRAY = (200, 200, 200)
LIGHT_BLUE = (173, 216, 230)   # Game background


# Game constants
CELL_SIZE = 40
MARGIN = 100
FONT_SIZE = 25

class BattleshipGame:
    def __init__(self):
        # screen dimensions
        self.screen_width = 1200
        self.screen_height = 700

        # Initializes a game window with title
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Battleship Game')
        self.font = pygame.font.SysFont('Arial', FONT_SIZE)
        self.big_font = pygame.font.SysFont('Arial', 45)
        
        self.level = None
        self.board_size = None
        
        self.player_board = None
        self.ai_board = None
        
        self.player_hits = None
        self.ai_hits = None

        self.player_conquered = 0
        self.ai_conquered = 0
        
        self.game_state = "SELECT_LEVEL"  # SELECT_LEVEL, PLACING_SHIPS, PLAYER_TURN, AI_TURN, GAME_OVER
        self.message = ""
        
        self.selected_ship_count = 0
        self.total_ships = 8
        
    def initialize_boards(self):
        if self.level == "Easy":
            self.board_size = 6
        elif self.level == "Moderate":
            self.board_size = 8
        elif self.level == "Hard":
            self.board_size = 10
        
        # Initialize boards with zeros
        self.player_board = np.zeros((self.board_size, self.board_size), dtype=int)
        self.ai_board = np.zeros((self.board_size, self.board_size), dtype=int)
        
        # Place AI ships (2's)
        self.place_ai_ships()
        
        self.player_hits = set()
        self.ai_hits = set()
        self.selected_ship_count = 0

        self.message = f"Place your {self.total_ships} ships."

        #self.message = f"Place your {self.total_ships} ships."
        
    def place_ai_ships(self):  # from line 68
        # Place AI ships randomly 
        ships_placed = 0
        while ships_placed < self.total_ships:
            x = random.randint(0, self.board_size - 1)  # self.board_size // 2
            y = random.randint(0, self.board_size - 1)  # generates random x, y co-ordinates
            if self.ai_board[y][x] == 0:
                self.ai_board[y][x] = 2
                ships_placed += 1
    
    def draw_board(self, board, x_offset, y_offset, hide_ships=False):   # on line 154, 160
        for y in range(self.board_size):
            for x in range(self.board_size):
                rect = pygame.Rect(x_offset + x * CELL_SIZE, y_offset + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)  # pygame.Rect(x, y, width, height)
                pygame.draw.rect(self.screen, WHITE, rect)
                pygame.draw.rect(self.screen, BLACK, rect, 1)
                
                # Draw cell content
                if board[y][x] == 1 and not hide_ships:    # Player ship
                    pygame.draw.rect(self.screen, BLUE, rect)
                elif board[y][x] == 2 and not hide_ships:  # AI ship
                    pygame.draw.rect(self.screen, RED, rect)
                elif board[y][x] == -1:  # Miss
                    pygame.draw.circle(self.screen, BLACK, rect.center, 7)
                elif board[y][x] == -2:  # Hit
                    pygame.draw.circle(self.screen, GREEN, rect.center, 7)
    
    def draw_grid_coordinates(self, x_offset, y_offset):
        # Draw letters (A, B, C...) at the top
        for i in range(self.board_size):
            text = self.font.render(chr(65 + i), True, BLACK)
            self.screen.blit(text, (x_offset + i * CELL_SIZE + CELL_SIZE // 2 - text.get_width() // 2, y_offset - FONT_SIZE))
        
        # Draw numbers (1, 2, 3...) on the side
        for i in range(self.board_size):
            text = self.font.render(str(i + 1), True, BLACK)
            self.screen.blit(text, (x_offset - FONT_SIZE, y_offset + i * CELL_SIZE + CELL_SIZE // 2 - text.get_height() // 2))
    
    def draw_level_selection(self):
        self.screen.fill(WHITE)

        title = self.big_font.render("BATTLESHIP GAME", True, BLACK)
        self.screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, 100))
        
        subtitle = self.font.render("Select Difficulty Level:", True, BLACK)
        self.screen.blit(subtitle, (self.screen_width // 2 - subtitle.get_width() // 2, 200))
        
        # Easy button
        easy_rect = pygame.Rect(self.screen_width // 2 - 100, 250, 200, 50)
        pygame.draw.rect(self.screen, GREEN, easy_rect)
        pygame.draw.rect(self.screen, BLACK, easy_rect, 2)
        easy_text = self.font.render("Easy (6x6)", True, BLACK)
        self.screen.blit(easy_text, (easy_rect.centerx - easy_text.get_width() // 2, easy_rect.centery - easy_text.get_height() // 2))
        
        # Moderate button
        moderate_rect = pygame.Rect(self.screen_width // 2 - 100, 320, 200, 50)
        pygame.draw.rect(self.screen, YELLOW, moderate_rect)
        pygame.draw.rect(self.screen, BLACK, moderate_rect, 2)
        moderate_text = self.font.render("Moderate (8x8)", True, BLACK)
        self.screen.blit(moderate_text, (moderate_rect.centerx - moderate_text.get_width() // 2, moderate_rect.centery - moderate_text.get_height() // 2))
        
        # Hard button
        hard_rect = pygame.Rect(self.screen_width // 2 - 100, 390, 200, 50)
        pygame.draw.rect(self.screen, RED, hard_rect)
        pygame.draw.rect(self.screen, BLACK, hard_rect, 2)
        hard_text = self.font.render("Hard (10x10)", True, BLACK)
        self.screen.blit(hard_text, (hard_rect.centerx - hard_text.get_width() // 2, hard_rect.centery - hard_text.get_height() // 2))
        
        return easy_rect, moderate_rect, hard_rect
    
    def draw_game_screen(self):
        self.screen.fill(LIGHT_BLUE)
        
        # Draw player board (left)
        player_label = self.font.render("Your Ships", True, BLACK)
        self.screen.blit(player_label, (MARGIN + (self.board_size * CELL_SIZE) // 2 - player_label.get_width() // 2, FONT_SIZE - 5))
        self.draw_board(self.player_board, MARGIN, MARGIN )  # from line 85
        self.draw_grid_coordinates(MARGIN, MARGIN )
        
        # Draw AI board (right) 
        ai_label = self.font.render("Enemy Waters", True, BLACK)
        self.screen.blit(ai_label, (self.screen_width - MARGIN - (self.board_size * CELL_SIZE) // 2 - ai_label.get_width() // 2, FONT_SIZE - 5))
        self.draw_board(self.ai_board, self.screen_width - MARGIN - self.board_size * CELL_SIZE, MARGIN , hide_ships=True)  # from line 85
        self.draw_grid_coordinates(self.screen_width - MARGIN - self.board_size * CELL_SIZE, MARGIN )
        
        # Draw game message
        message_text = self.font.render(self.message, True, BLACK)
        self.screen.blit(message_text, (self.screen_width // 2 - message_text.get_width() // 2, self.screen_height - 100))

        player_hits = self.font.render(f"Ships Hit: {self.ai_conquered}", True, BLACK)
        self.screen.blit(player_hits, (self.screen_width // 2 - message_text.get_width() // 2 + 2.8*MARGIN, self.screen_height - 150))

        ai_hits = self.font.render(f"Ships Hit: {self.player_conquered}", True, BLACK)  # from line 72
        self.screen.blit(ai_hits, (self.screen_width // 2 - message_text.get_width() // 2 - 2.2*MARGIN, self.screen_height - 150))

        # Draw ship placement counter if in placing phase
        if self.game_state == "PLACING_SHIPS":
            counter_text = self.font.render(f"Ships placed: {self.selected_ship_count}/{self.total_ships}", True, BLACK)
            self.screen.blit(counter_text, (self.screen_width // 2 - counter_text.get_width() // 2, self.screen_height - FONT_SIZE - 50))
    
    def handle_level_selection(self, pos):
        easy_rect, moderate_rect, hard_rect = self.draw_level_selection()
        
        if easy_rect.collidepoint(pos):
            self.level = "Easy"
            self.initialize_boards()
            self.game_state = "PLACING_SHIPS"
        elif moderate_rect.collidepoint(pos):
            self.level = "Moderate"
            self.initialize_boards()
            self.game_state = "PLACING_SHIPS"
        elif hard_rect.collidepoint(pos):
            self.level = "Hard"
            self.initialize_boards()
            self.game_state = "PLACING_SHIPS"
    
    def handle_ship_placement(self, pos):
        pass
    
    def handle_player_attack(self, pos):
        # Check if click is within AI board
        board_start_x = self.screen_width - MARGIN - self.board_size * CELL_SIZE
        board_start_y = MARGIN
        board_x = int((pos[0] - board_start_x) // CELL_SIZE)
        board_y = int((pos[1] - board_start_y) // CELL_SIZE)
        
        if (0 <= board_x < self.board_size and 0 <= board_y < self.board_size and (board_y, board_x) not in self.player_hits):
            self.player_hits.add((board_y, board_x))
            
            if self.ai_board[board_y][board_x] == 2:  # Hit
                self.ai_board[board_y][board_x] = -2
                self.message = "Hit! Your turn again"
                self.ai_conquered += 1
                
                # Check if all AI ships are sunk
                if all(2 not in row for row in self.ai_board):
                    self.game_state = "GAME_OVER"
                    self.message = "You won! All enemy ships destroyed"
                else:
                    # Player gets another turn after hit
                    return
            else:  # Miss
                self.ai_board[board_y][board_x] = -1
                self.message = "Miss! Enemy's turn"
                self.game_state = "AI_TURN"
    
    def ai_turn(self):
        # Simple AI: random choice
        while True:
            x = random.randint(0, self.board_size - 1)
            y = random.randint(0, self.board_size - 1)
            
            if (y, x) not in self.ai_hits: # and x < self.board_size // 2:  # AI only attacks left half
                self.ai_hits.add((y, x))
                
                if self.player_board[y][x] == 1:  # Hit
                    self.player_board[y][x] = -2
                    self.message = "Enemy hit your ship! Their turn again"
                    self.player_conquered += 1
                    
                    # Check if all player ships are sunk
                    if all(1 not in row for row in self.player_board):
                        self.game_state = "GAME_OVER"
                        self.message = "You lost! All your ships destroyed"
                    else:
                        # AI gets another turn after hit
                        self.ai_turn()
                else:  # Miss
                    self.player_board[y][x] = -1
                    self.message = "Enemy missed! Your turn"
                    self.game_state = "PLAYER_TURN"
                break
    
    def run(self):
        clock = pygame.time.Clock()
        
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    if self.game_state == "SELECT_LEVEL":
                        self.handle_level_selection(event.pos)
                    elif self.game_state == "PLACING_SHIPS":
                        self.handle_ship_placement(event.pos)
                    elif self.game_state == "PLAYER_TURN":
                        self.handle_player_attack(event.pos)
            
            if self.game_state == "AI_TURN":
                self.ai_turn()
            
            if self.game_state == "SELECT_LEVEL":
                self.draw_level_selection()
            else:
                self.draw_game_screen()
            
            pygame.display.flip()
            clock.tick(30)

if __name__ == "__main__":
    game = BattleshipGame()
    game.run()
