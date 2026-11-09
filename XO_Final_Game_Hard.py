import random
import pygame
import sys
import time

# Initialize Pygame and set up the window:

pygame.init()
screen_length = 640
offset = 50
screen = pygame.display.set_mode((screen_length, screen_length))
font = pygame.font.SysFont('pixelifysans', 40)
color_background = (255, 239, 239)
color_lines = (255, 170, 184)
color_lines_win = (77, 103, 135)
X_Image = pygame.image.load('Heart.png')
X_Image = pygame.transform.scale(X_Image, (100, 100))
O_Image = pygame.image.load('Star.png')
O_Image = pygame.transform.scale(O_Image, (130,130))
O_Win_Text = font.render(f'Hearts Win', True, (255,255,255))
O_Win_Text_Rect = O_Win_Text.get_rect(center = (320,320))
X_Win_Text = font.render(f'Stars Win', True, (255,255,255))
X_Win_Text_Rect = X_Win_Text.get_rect(center = (320,320))
Draw_Text = font.render(f'Its a Tie', True, (255,255,255))
Draw_Text_Rect = X_Win_Text.get_rect(center = (320,320))
dim_overlay = pygame.Surface((640, 640)).convert_alpha()
dim_overlay.fill((0, 0, 0, 240))

# Create Clock

clock = pygame.time.Clock()

# Graphics:

screen.fill(color_background)
pygame.draw.aaline(screen, color_lines, (230, 50), (230, 590), 5)
pygame.draw.aaline(screen, color_lines, (410, 50), (410, 590), 5)
pygame.draw.aaline(screen, color_lines, (50, 230), (590, 230), 5)
pygame.draw.aaline(screen, color_lines, (50, 410), (590, 410), 5)
pygame.display.flip()

## Initiation:

user_moves_set = set()
computer_move_set = set()
best_move = set()
valid_move = {0,1,2,3,4,5,6,7,8}
position_List = []

# Game Logic:

comb_dict = {'comb1':{0,3,6},
            'comb2':{1,4,7},
            'comb3':{2,5,8},
            'comb4':{0,1,2},
            'comb5':{3,4,5},
            'comb6':{6,7,8},
            'comb7':{0,4,8},
            'comb8':{2,4,6}}

# Positions:

rectangles_dict = {'0' : pygame.Rect(50, 50, 180, 180),
                   '1' : pygame.Rect(230, 50, 180, 180),
                   '2' : pygame.Rect(410, 50, 180, 180),
                   '3' : pygame.Rect(50, 230, 180, 180),
                   '4' : pygame.Rect(230, 230, 180, 180),
                   '5' : pygame.Rect(410, 230, 180, 180),
                   '6' : pygame.Rect(50, 410, 180, 180),
                   '7' : pygame.Rect(230, 410, 180, 180),
                   '8' : pygame.Rect(410, 410, 180, 180)} 

# Functions: 

def computer_input():

    if 4 not in user_moves_set and 4 in valid_move:
        computer_move = 4 
        computer_move_set.add(computer_move)
        valid_move.remove(computer_move)
        result = set()
        result.add(computer_move)

    elif len(user_moves_set) < 3:
        for key, value in comb_dict.items():
            if user_moves_set.issubset(value):
                best_move.update(value)

        result = best_move & valid_move

        if len(result) == 0:
                computer_move = random.choice(list(valid_move))
                computer_move_set.add(computer_move)
                valid_move.remove(computer_move)
                best_move.clear()
        else:
            computer_move = random.choice(list(result))
            computer_move_set.add(computer_move)
            valid_move.remove(computer_move)
            best_move.clear()

    elif len(user_moves_set) >= 3:

        for key, value in comb_dict.items():
            Try = computer_move_set & value
            if len(Try) == 2:
                best_move.update(value)

        result = best_move & valid_move

        if len(result) == 0:

            for key, value in comb_dict.items():
                Try = user_moves_set & value
                if len(Try) == 2:
                    best_move.update(value)

            result = best_move & valid_move

            if len(result) == 0:
                    computer_move = random.choice(list(valid_move))
                    computer_move_set.add(computer_move)
                    valid_move.remove(computer_move)
                    best_move.clear()
        
            else:
                computer_move = random.choice(list(result))
                computer_move_set.add(computer_move)
                valid_move.remove(computer_move)
                best_move.clear()

        else:
            computer_move = random.choice(list(result))
            computer_move_set.add(computer_move)
            valid_move.remove(computer_move)
            best_move.clear()

    result.clear()
    O_Image_Rect = O_Image.get_rect(center = rectangles_dict[str(computer_move)].center)
    screen.blit(O_Image,O_Image_Rect)
    pygame.display.flip()

def check_win():
    for key, values in comb_dict.items():
        if values.issubset(user_moves_set):
            pygame.draw.aaline(screen, color_lines_win, (rectangles_dict[str(min(values))].center), (rectangles_dict[str(max(values))].center), 10)
            screen.blit(dim_overlay, (0, 0))
            screen.blit(X_Win_Text, X_Win_Text_Rect)
            pygame.display.flip()
            time.sleep(2)
            sys.exit()
        elif values.issubset(computer_move_set):
            pygame.draw.aaline(screen, color_lines_win, (rectangles_dict[str(min(values))].center), (rectangles_dict[str(max(values))].center), 10)
            screen.blit(dim_overlay, (0, 0))
            screen.blit(O_Win_Text, O_Win_Text_Rect)
            pygame.display.flip()
            time.sleep(2)
            sys.exit()
        elif len(user_moves_set) == 5:
            screen.blit(dim_overlay, (0, 0))
            screen.blit(Draw_Text, Draw_Text_Rect)
            pygame.display.flip()
            time.sleep(2)
            sys.exit()

def round():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:

                for key, value in rectangles_dict.items():
                    if value.collidepoint(event.pos):
                        user_move = int(key)
                        if user_move not in valid_move:
                            print('False Move')
                        else:
                            user_moves_set.add(user_move)
                            valid_move.remove((user_move))
                            X_Image_Rect = X_Image.get_rect(center = value.center)
                            screen.blit(X_Image, X_Image_Rect)
                            pygame.display.flip()
                            check_win()
                            computer_input()
                            check_win()

# Main Game Loop:

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        else:
            round()

    clock.tick(60)