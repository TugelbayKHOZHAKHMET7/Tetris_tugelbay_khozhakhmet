#game_tetris
import pygame
from copy import deepcopy 
from random import choice, randrange

width, hight = 10, 20
rec_scale = 35  
game_cons = width * rec_scale, hight * rec_scale 
whole_cons = 750, 795 
FPS = 60

pygame.init()
cons_screen = pygame.display.set_mode(whole_cons) 
game_screen = pygame.Surface(game_cons) 
clock = pygame.time.Clock()

grid = [pygame.Rect(x * rec_scale, y * rec_scale, rec_scale, rec_scale) for x in range(width) for y in range(hight)]

figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
               [(0, -1), (-1, -1), (-1, 0), (0, 0)],
               [(-1, 0), (-1, 1), (0, 0), (0, -1)],
               [(0, 0), (-1, 0), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, 0)]]

figures = [[pygame.Rect(x + width // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
figure_rect = pygame.Rect(0, 0, rec_scale - 2, rec_scale - 2)
field = [[0 for i in range(width)] for j in range(hight)]

anim_count, anim_speed, anim_limit = 0, 60, 2000

cons_picture = pygame.image.load('env_phon.jpg').convert() 
game_cons_picture = pygame.image.load('priroda.jpg').convert() 

main_type = pygame.font.Font('FiraMono-Medium.ttf', 65) 
font = pygame.font.Font('FiraMono-Medium.ttf', 45) 

title_tetris = main_type.render('TETRIS', True, pygame.Color('darkorange'))
pl_score = font.render('баллы:', True, pygame.Color('green')) 
pl_record = font.render('рекорд:', True, pygame.Color('purple'))

make_color = lambda : (randrange(30, 256), randrange(30, 256), randrange(30, 256))

piece, next_piece = deepcopy(choice(figures)), deepcopy(choice(figures))
color, next_color = make_color(), make_color()

score, lines = 0, 0
scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}


def check_borders():
    if piece[i].x < 0 or piece[i].x > width-1:
        return False
    elif piece[i].y > hight - 1 or field[piece[i].y][piece[i].x]:
        return False
    return True


def get_record():
    try:
        with open('record') as f:
            return f.readline()
    except FileNotFoundError:
        with open('record', 'w') as f:
            f.write('0')


def set_record(record, score):
    rec = max(int(record), score)
    with open('record', 'w') as f:
        f.write(str(rec))


while True:
    record = get_record()
    dx, rotate = 0, False
    cons_screen.blit(cons_picture, (0, 0))
    cons_screen.blit(game_screen, (20, 20))
    game_screen.blit(game_cons_picture, (0, 0))
    for i in range(lines):
        pygame.time.wait(200)
   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dx = -1
            elif event.key == pygame.K_RIGHT:
                dx = 1
            elif event.key == pygame.K_DOWN:
                anim_limit = 100
            elif event.key == pygame.K_UP:
                rotate = True
    
    piece_old = deepcopy(piece)
    for i in range(4):
        piece[i].x += dx
        if not check_borders():
            piece = deepcopy(piece_old)
            break
    anim_count += anim_speed
    if anim_count > anim_limit:
        anim_count = 0
        piece_old = deepcopy(piece)
        for i in range(4):
            piece[i].y += 1
            if not check_borders():
                for i in range(4):
                    field[piece_old[i].y][piece_old[i].x] = color
                piece, color = next_piece, next_color
                next_piece, next_color = deepcopy(choice(figures)), make_color()
                anim_limit = 2000
                break
   
    center = piece[0]
    piece_old = deepcopy(piece)
    if rotate:
        for i in range(4):
            x = piece[i].y - center.y
            y = piece[i].x - center.x
            piece[i].x = center.x - x
            piece[i].y = center.y + y
            if not check_borders():
                figure = deepcopy(piece_old)
                break
    line, lines = hight - 1, 0
    for row in range(hight - 1, -1, -1):
        count = 0
        for i in range(width):
            if field[row][i]:
                count += 1
            field[line][i] = field[row][i]
        if count < width:
            line -= 1
        else:
            anim_speed += 3
            lines += 1
    
    score += scores[lines]
    [pygame.draw.rect(game_screen, (40, 40, 40), i_rect, 1) for i_rect in grid]
    for i in range(4):
        figure_rect.x = piece[i].x * rec_scale
        figure_rect.y = piece[i].y * rec_scale
        pygame.draw.rect(game_screen, color, figure_rect)
    for y, raw in enumerate(field):
        for x, col in enumerate(raw):
            if col:
                figure_rect.x, figure_rect.y = x * rec_scale, y * rec_scale
                pygame.draw.rect(game_screen, col, figure_rect)
    for i in range(4):
        figure_rect.x = next_piece[i].x * rec_scale + 380
        figure_rect.y = next_piece[i].y * rec_scale + 185
        pygame.draw.rect(cons_screen, next_color, figure_rect)
   
    cons_screen.blit(title_tetris, (485, -10))
    cons_screen.blit(pl_score, (535, 550)) #535,780
    cons_screen.blit(font.render(str(score), True, pygame.Color('black')), (550, 600))
    cons_screen.blit(pl_record, (525, 650))
    cons_screen.blit(font.render(record, True, pygame.Color('gold')), (550, 710))
    
    for i in range(width):
        if field[0][i]:
            set_record(record, score)
            field = [[0 for i in range(width)] for i in range(hight)]
            anim_count, anim_speed, anim_limit = 0, 60, 2000
            score = 0
            for rectangles in grid:
                pygame.draw.rect(game_screen, make_color(), rectangles)
                cons_screen.blit(game_screen, (20, 20))
                pygame.display.flip()
                clock.tick(200)

    pygame.display.flip()
    clock.tick(FPS)
