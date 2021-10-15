import sys, random
import pygame
from misc import *

def build_game(matrix, i, j, number):
    if i>8 or j>8:
        return matrix
    if check_duplicate(matrix, i, j, number):        
        _matrix = [[col for col in row] for row in matrix]
        _matrix[i][j] = number
        next_i, next_j = (i+1, 0) if j==8 else (i, j+1)
        _list = number_list
        random.shuffle(_list)
        for _number in _list:
            __matrix = build_game(_matrix, next_i, next_j, _number)
            if __matrix and sum([sum(row) for row in __matrix])==(sum(range(1,10))*9):
                return __matrix
    return None

def make_a_matrix(matrix, number_list, blank_size=10):
    matrix_all = build_game(matrix, 0, 0, random.choice(number_list))
    blank_pos = set()
    while len(list(blank_pos))<blank_size:
        blank_pos.add(str(random.choice([0,1,2,3,4,5,6,7,8]))+','+str(random.choice([0,1,2,3,4,5,6,7,8])))
    
    matrix_blank = [[col for col in row] for row in matrix_all]
    blank_ij = []
    for ij in list(blank_pos):
        i, j = int(ij.split(',')[0]), int(ij.split(',')[1])
        blank_ij.append((i, j))
        matrix_blank[i][j] = 0
    return matrix_all, matrix_blank, blank_ij

if __name__ == "__main__":
    
    blank_size = int(sys.argv[1])
    
    # init pygame
    pygame.init()
    
    # set config
    number_list = [1,2,3,4,5,6,7,8,9]
    matrix = [([0]*9) for i in range(9)]
    screen_size = (900, 1000)
    txtsize_60 = pygame.font.SysFont("Times", 60)
    txtsize_50 = pygame.font.SysFont("Times", 50)
    
    # variable parameter
    cur_i, cur_j = 0, 0
    cur_blank_size = blank_size
    cur_change_size = 0
    
    # create
    screen = pygame.display.set_mode(screen_size)
    MATRIX_ANSWER, MATRIX, BLANK_IJ = make_a_matrix(matrix, number_list, blank_size=blank_size)
    print_matrix(MATRIX)
    
    TIME_ANS = 60*1000*cur_blank_size
    
    # main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: ##256
                running = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN: ##1025
                cur_j, cur_i = int(event.pos[0]/100),int(event.pos[1]/100)
            elif event.type == pygame.KEYUP: ##769
                if chr(event.key) in ['1','2','3','4','5','6','7','8','9'] and (cur_i, cur_j) in BLANK_IJ:
                    MATRIX[cur_i][cur_j] = int(chr(event.key))
                    cur_blank_size = sum([1 if col==0 or col=='0' else 0 for row in MATRIX for col in row])
                    cur_change_size +=1
        # time
        TIME_STATE = pygame.time.get_ticks()
        time_txt = time_calculate(TIME_STATE)
        # background & choose
        draw_matrix_box(screen, cur_i, cur_j)
        # numbers
        draw_number(screen, MATRIX, BLANK_IJ, txtsize_60)
        # context & time
        draw_context(screen, cur_blank_size, cur_change_size, time_txt,txtsize_50)
        
        # update
        pygame.display.update()
    
        # check ans and complete time
        WIN_CHECK, TIME_CHECK = check_complete(MATRIX_ANSWER, MATRIX, TIME_ANS, TIME_STATE)
        if WIN_CHECK and TIME_CHECK:
            print(f"You win, Completed in time: {time_txt}!!")
            running = False
        elif WIN_CHECK and (not TIME_CHECK):
            print(f"Completed, But out of time: {time_txt}.")
            running = False

    pygame.quit()