import pygame as pg
from pygame.locals import *
from forza4_ai import alpha_beta_pruning
from forza4_ai import check_win
from forza4_ai import is_legal

#Colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (0, 255, 0)

#Dimensions
WIDTH = 800
HEIGHT = 600

def init_mat():
    mat = []
    for i in range(6):
        row = []
        for j in range(7):
            row.append(0)
        
        mat.append(row)

    return mat

def handle_click(screen, ev, mat):
    x = (ev.pos[0]-20)//114
    y = 0
    if x>=0 and x<7 and is_legal(mat, x):
        for i in range(6):
            if mat[5-i][x] == 0:
                y = 5-i
                mat[y][x] = 'X'
                break
    
        pg.draw.circle(screen, YELLOW, (x*WIDTH//7 + 50, y*HEIGHT//6 + 45), 30)
        pg.display.flip()
        _, ac = alpha_beta_pruning(mat)
        z=0
        for i in range(6):
            if mat[5-i][ac] == 0:
                z = 5-i
                mat[z][ac] = 'O'
                break
        pg.draw.circle(screen, RED, (ac*WIDTH//7 + 50, z*HEIGHT//6 + 45), 30)
        pg.display.flip()

def print_mat(mat):
    for x in mat:
        print(x)

def reset(mat):
    for x in mat:
        for i in range(7):
            x[i] = 0

def draw_grid(screen):
    col = (WIDTH -20) // 7
    row = (HEIGHT-20) // 6
    for i in range(col):
        pg.draw.line(screen, BLUE, (i*col +10, 10), (i*col +10, HEIGHT-10), 10)
    
    for i in range(row):
        pg.draw.line(screen, BLUE, (10, i*row +10), (WIDTH-10, i*row +10), 10)
    
    pg.display.flip()

def start():
    #init grid
    GRID = init_mat()
    
    #init window
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Forza 4")
    
    #drawing grid
    draw_grid(screen)

    #init font
    pg.font.init()
    myfont = pg.font.SysFont('Comic Sans MS', 100)

    done = False
    while not done:
        end, w = check_win(GRID)       
        if not w: 
            w = "It's a tie" 
        elif w=='X':
            w="Yellow wins"
        elif w == 'O': w = 'Red wins'
        if end:
            #if the game is over displays the winner
            textsurface = myfont.render(w, False, (255, 255, 255))
            screen.blit(textsurface, (WIDTH//2 - 100, HEIGHT//2 - 100))
            pg.display.flip() 

            #wait for user's click
            con = True            
            while con:
                for ev in  pg.event.get():
                    if ev.type == QUIT:
                        pg.quit()
                    elif ev.type == MOUSEBUTTONDOWN or ev.type == KEYDOWN:
                        con = False
            
            #resetting the game on user's click
            reset(GRID)
            end = False 
            screen = pg.display.set_mode((WIDTH, HEIGHT))
            draw_grid(screen)

        for ev in  pg.event.get():
            if ev.type == QUIT:
                done = True
            elif ev.type == MOUSEBUTTONDOWN:
                handle_click(screen, ev, GRID)
            
    pg.quit()

start()