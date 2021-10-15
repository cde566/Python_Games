import pygame
from pygame.color import THECOLORS as COLORS

def draw_matrix_box(screen, cur_i, cur_j):
    # black background
    screen.fill(COLORS['black'])

    # draw game box (x1,y1)->(width,height)
    pygame.draw.rect(screen,COLORS['white'],(0,0,300,900),5)
    pygame.draw.rect(screen,COLORS['white'],(300,0,300,900),5)
    pygame.draw.rect(screen,COLORS['white'],(600,0,300,900),5)

    pygame.draw.rect(screen,COLORS['white'],(0,0,900,300),5)
    pygame.draw.rect(screen,COLORS['white'],(0,300,900,300),5)
    pygame.draw.rect(screen,COLORS['white'],(0,600,900,300),5)
    
    pygame.draw.rect(screen,COLORS['white'],(0,0,600,600),5)
    
    pygame.draw.rect(screen,COLORS['grey'],(cur_j*100+5, cur_i*100+5, 100-15, 100-15), 0)

def draw_number(screen, MATRIX, BLANK_IJ, txtsize_60):
    for i in range(len(MATRIX)):
        for j in range(len(MATRIX[0])):
            _color = check_color(MATRIX, i, j) if (i, j) in BLANK_IJ else COLORS['white']
            txt = txtsize_60.render(str(MATRIX[i][j] if MATRIX[i][j] not in [0,'0'] else ''),True,_color)
            x, y = j*100+35, i*100+15
            screen.blit(txt, (x,y))

def draw_context(screen, cur_blank_size, cur_change_size, time_txt, txtsize_50):
    txt = txtsize_50.render('Blank: '+str(cur_blank_size)
                        +'  Change: '+str(cur_change_size)
                        +'  Time: '+time_txt
                        ,True,COLORS['white']
                        )
    x, y = 20, 910
    screen.blit(txt, (x, y))
    
def time_calculate(time_state):
    if int(time_state/1000)>60:
        time_txt = f"{int(time_state/1000/60)} min {int((time_state/1000)%60)} sec"
    else:
        time_txt = f"{int(time_state/1000)} sec"
    return time_txt   
    
def print_matrix(matrix):
    print('—'*19)
    for row in matrix:
        print('|'+'|'.join([str(col) for col in row])+'|')
        print('—'*19)

def check_duplicate(matrix, i, j, number):
    ## 確認列
    if number in matrix[i]:
        return False
    ## 確認行
    if number in [row[j] for row in matrix]:
        return False
    group_i, group_j = int(i/3), int(j/3)
    ## 確認方格
    if number in [matrix[i][j] for i in range(group_i*3, (group_i+1)*3) for j in range(group_j*3, (group_j+1)*3)]:
        return False
    return True

def check_complete(matrix_all, matrix, time_all, time):
    if matrix_all == matrix:
        if time <= time_all:
            return True, True
        else:
            return True, False
    return False, False

def check_color(matrix,i,j):
    _matrix = [[col for col in row]for row in matrix]
    _matrix[i][j] = 0
    if check_duplicate(_matrix,i,j,matrix[i][j]):
        return COLORS['green']
    return COLORS['red']
