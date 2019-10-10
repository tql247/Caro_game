#!/usr/bin/env python
# coding: utf-8

# In[1]:


turn_form = {'player': 'o', 'bot': 'x'}
table_dgr = {2: 1, 3: 20, 4: 45, 5: 150, 1: 0, 0: 0}


# In[2]:


def get_list_point(state, turn):
    '''
        state: [[]]
        turn: string, 'player' or 'bot'
        return: list of coordinate
    '''
    ls_point = list()
    for row in range(state.__len__()):
        for cell in range(state.__len__()):
            if state[row][cell] == turn_form[turn]:
                ls_point.append(str(row) + '-' + str(cell))
    return ls_point


# In[3]:


def forward(ls_point, num_point):
    '''
        ls_point: list()
        num_point: list()
        return: new num_point if next point can make a line with previous
    '''
    x_src, y_src = list(map(int,num_point[-1].split('-')))
    x_pre, y_pre = list(map(int,num_point[-2].split('-')))
    x_next, y_next = x_src + (x_src - x_pre), y_src + (y_src - y_pre)
    if str(x_next) + '-' + str(y_next) in ls_point:
        num_point.append(str(x_next) + '-' + str(y_next))
        return forward(ls_point, num_point)


# In[4]:


def near(point_src, point_des):
    '''
        point_src: str, coordinate of source point, 'x-y'
        point_des: str, coordinate of destination point, 'x-y'
        return: boolean, True if it close together and False if not
    '''
    x_src, y_src = list(map(int,point_src.split('-')))
    x_des, y_des = list(map(int,point_des.split('-')))
    return abs(x_src - x_des) <= 1 and abs(y_src - y_des) <= 1


# In[5]:


def count_line(state, score, turn):
    '''
        score: int, number of point in line that current turn want to find
        turn: string, 'player' or 'bot'
        return: number of line such that point >= score
    '''
    ls_point = get_list_point(state, turn)
    if score == 1:
        return ls_point.__len__()
    num_line = 0
    for point_src in ls_point[:-1]:
        num_point = [point_src, ]
        for point_des in ls_point[ls_point.index(point_src) + 1:]:
            if near(point_src, point_des):
                num_point.append(point_des)
                forward(ls_point, num_point)
            else:
                continue
            if num_point.__len__() >= score:
                num_line += 1
            num_point = [point_src, ]
    return num_line


# In[6]:


def count_score(state, turn):
    '''
        state: [[]]
        turn: string, 'bot' or player
        return: int, score for each line contain more than 2 points
    '''
#     state = state.get_value()
    table_score = {5: 70, 4:30, 3:10, 2:2}
    total_score = 0
    for score in table_score:
        total_score += count_line(state, score, turn)*table_score[score]
    return total_score


# In[7]:


def continue_line(ls_opp_point, src, des):
    
    x_step, y_step = int(des.split('-')[0]) - int(src.split('-')[0]), int(des.split('-')[1]) - int(src.split('-')[1])
    curr_point = list(map(int, des.split('-')))
    line = [src, des]
    while str(curr_point[0] + x_step) + '-' + str(curr_point[1] + y_step) in ls_opp_point:
        curr_point = curr_point[0] + x_step, curr_point[1] + y_step
        line += [str(curr_point[0]) + '-' + str(curr_point[1])]
    
    return line


# In[8]:


def is_stuck(state, line, opp): 
    x_step, y_step = int(line[-1].split('-')[0]) - int(line[-2].split('-')[0]), int(line[-1].split('-')[1]) - int(line[-2].split('-')[1])
    border_head = int(line[0].split('-')[0]) - x_step, int(line[0].split('-')[1]) - y_step
    border_tail = int(line[-1].split('-')[0]) + x_step, int(line[-1].split('-')[1]) + y_step
    edge_A = False
    edge_B = False
    if border_head[0] >= 0 and border_head[0] < state.__len__() and border_head[1] >= 0 and border_head[1] < state.__len__():
        if state[border_head[0]][border_head[1]] == turn_form[opp]:
            edge_A = True
    else:
        edge_A = True
        
    if border_tail[0] >= 0 and border_tail[0] < state.__len__() and border_tail[1] >= 0 and border_tail[1] < state.__len__():
        
        if state[border_tail[0]][border_tail[1]] == turn_form[opp]:
            edge_B = True
        
    else:
        edge_B = True
    
    return edge_A and edge_B


# In[9]:


def less_dangerous(state, max_dgr, turn):
    if max_dgr.__len__() == 0:
        return 0
#     print(is_stuck(state, max_dgr, turn))
    x_step, y_step = int(max_dgr[-1].split('-')[0]) - int(max_dgr[-2].split('-')[0]), int(max_dgr[-1].split('-')[1]) - int(max_dgr[-2].split('-')[1])
    if max_dgr.__len__() < 3:
        return table_dgr[max_dgr.__len__()]
    elif max_dgr.__len__() == 3:
        border_head = int(max_dgr[0].split('-')[0]) - x_step, int(max_dgr[0].split('-')[1]) - y_step
        border_tail = int(max_dgr[-1].split('-')[0]) + x_step, int(max_dgr[-1].split('-')[1]) + y_step
        try:
            if state[border_head[0]][border_head[1]] == '.' and state[border_tail[0]][border_tail[1]] == '.':
                return - table_dgr[max_dgr.__len__()]*max_dgr.__len__()
            elif state[border_head[0]][border_head[1]] == '.' or state[border_tail[0]][border_tail[1]] == '.':
                return -table_dgr[max_dgr.__len__()]
            else:
                return table_dgr[max_dgr.__len__()]*3
        except:
            return table_dgr[max_dgr.__len__()]
    else:
        border_head = int(max_dgr[0].split('-')[0]) - x_step, int(max_dgr[0].split('-')[1]) - y_step
        border_tail = int(max_dgr[-1].split('-')[0]) + x_step, int(max_dgr[-1].split('-')[1]) + y_step
        try:
            if (state[border_head[0]][border_head[1]] == '.' and state[border_tail[0]][border_tail[1]] == '.') or is_stuck(state, max_dgr, turn):
                return table_dgr[max_dgr.__len__()]*5
            else:
                return - table_dgr[max_dgr.__len__()]*5
        except:
            return table_dgr[max_dgr.__len__()]


# In[10]:


def striping(state, potential_point, border):
    try:
        if state[potential_point[0]][potential_point[1]] != state[border[0]][border[1]] and state[potential_point[0]][potential_point[1]] != '.' and state[border[0]][border[1]] != '.':
            return True
        return False
    except:
        return False


# In[11]:


def potential(state, max_dgr):
    if max_dgr.__len__() < 2:
        return 0
    
    x_step, y_step = int(max_dgr[-1].split('-')[0]) - int(max_dgr[-2].split('-')[0]), int(max_dgr[-1].split('-')[1]) - int(max_dgr[-2].split('-')[1])
    
    potential_point_head = int(max_dgr[0].split('-')[0]) - 2*x_step, int(max_dgr[0].split('-')[1]) - 2*y_step
    potential_point_tail = int(max_dgr[-1].split('-')[0]) + 2*x_step, int(max_dgr[-1].split('-')[1]) + 2*y_step
    border_head = int(max_dgr[0].split('-')[0]) - x_step, int(max_dgr[0].split('-')[1]) - y_step
    border_tail = int(max_dgr[-1].split('-')[0]) + x_step, int(max_dgr[-1].split('-')[1]) + y_step
    
    if striping(state, potential_point_head, border_head) or striping(state, potential_point_tail, border_tail):
        return max_dgr.__len__() + 2
    return 0


# In[12]:


def is_in_set(setA, setB):
    for item in setA:
        if item not in setB:
            return False
    return True


# In[13]:


def is_in_ls_set(setA, ls):
    for setitem in ls:
        if is_in_set(setA, setitem):
            return True
    return False


# In[14]:


def count_point_in_opp_line(state, turn):
    opp = 'no one'
    if turn == 'bot':
        opp = 'player'
    else:
        opp = 'bot'
    ls_opp_point = get_list_point(state, opp)
    max_dgr = list()
    ban_line = list()
    potential_point = 0
    for src in ls_opp_point[:-1]:
        for des in ls_opp_point[ls_opp_point.index(src) + 1:]:
            if near(src, des):
                level_dgr = continue_line(ls_opp_point, src, des)
                if is_stuck(state, level_dgr, turn):
                    ban_line.append(level_dgr)
                elif max_dgr.__len__() < level_dgr.__len__() and not is_in_ls_set(level_dgr, ban_line):
                    max_dgr = level_dgr
                if potential_point < len(level_dgr) + 2:
                    potential_point = potential(state, level_dgr)
#     print(less_dangerous(state, max_dgr))
#     print(potential(state, max_dgr))
    return less_dangerous(state, max_dgr, turn) + table_dgr[min(potential_point, 5)] - ban_line.__len__()*5 #+ drop_plot(state, ls_opp_point)


# In[15]:


def profit(state, turn):
    '''
        state: a Node
        turn: player or bot
        return: int (value of profit)
    '''
    score_make_line = count_score(state, turn)
    score_in_opp_line = count_point_in_opp_line(state, turn)
#     score_opp_in_line = count_opp_in_line(state, turn)
#     print(score_make_line)
#     print(score_in_opp_line)
    return score_make_line + score_in_opp_line #- score_opp_in_line


# In[16]:


cs = [['.', '.', '.', '.', '.', '.'], 
      ['.', '.', 'o', 'o', 'o', '.'], 
      ['.', '.', '.', '.', '.', '.'],
      ['.', 'o', '.', 'x', '.', '.'],
      ['.', '.', '.', 'x', 'x', 'x'],
      ['.', '.', '.', '.', '.', '.']]
profit(cs, 'bot')


# In[17]:


def copy_state(state):
    state_cpy = list()
    for e in state:
        state_cpy.append(list(e))
    return state_cpy


# In[18]:


def get_ls_plot(state):
    ls_blank_plot = list()
    ls_filled_plot = list()
    for row in range(state.__len__()):
        for col in range(state[0].__len__()):
            if state[row][col] == '.':
                ls_blank_plot.append(str(row) + '-' + str(col))
            else:
                ls_filled_plot.append(str(row) + '-' + str(col))
    return ls_blank_plot, ls_filled_plot


# In[19]:


def move(state, blank_plot, turn):
    state_cpy = copy_state(state)
    x, y = list(map(int, blank_plot.split('-')))
    state_cpy[x][y] = turn_form[turn]
    return state_cpy


# In[20]:


def can_move(state, turn):
    '''
        state: current state of game
        return: list of new state
    '''
    ls_blank_plot, ls_filled_plot = get_ls_plot(state)
    ls_new_move = list()
    for blank_plot in ls_blank_plot:
        for filled_plot in ls_filled_plot:
            if near(blank_plot, filled_plot):
                ls_new_move.append(move(state, blank_plot, turn))
                break
    if ls_filled_plot.__len__() == 0:
        return [move(state, str(state.__len__()//2) + '-' + str(state.__len__()//2), turn)]
    return ls_new_move


# In[21]:


def get_max(crr_state, parent_value):
    '''
        state: a Node
        return: a Node with max profit
    '''
    best_node = [[]]
    max_profit = - 10000
    for move in can_move(crr_state, 'bot'):
        if parent_value < profit(move, 'bot') and parent_value != -10000:
            return [False, None, None]
        
        if max_profit < profit(move, 'bot'):
            max_profit = profit(move, 'bot')
            best_node = move
    return [True, max_profit, best_node]


# In[22]:


def get_min(crr_state, parent_value):
    '''
        state: a Node
        return: a Node with min profit
    '''
    best_node = [[]]
    min_profit = 10000
    for move in can_move(crr_state, 'player'):
        if parent_value > profit(move, 'player') and parent_value != 10000:
            return [False, None, None]
        
        if min_profit > profit(move, 'player'):
            min_profit = profit(move, 'player')
            best_node = move
    return [True, min_profit, best_node]


# In[23]:


def mini_max(crr_state, deepth, get_max_profit, parent_value):
    '''
        state: a Node, current state of game
        crr_path: list(), the predict move of both player
        deepth: int, high of tree
        return: new state
        
        - Calculate profit(state) in list of can_move(state)
        - Best move is min or max profit(state) depend of deep value
    '''
    if deepth == 1:
        if get_max_profit:
            return get_max(crr_state, parent_value)
        return get_min(crr_state, parent_value)
    else:
        if get_max_profit:
            best_node = [[]]
            parent_value = - parent_value
            for move in can_move(crr_state, 'bot'):
                get_value = mini_max(move, deepth - 1, not get_max_profit, parent_value)
                
                if not get_value[0]:
                    continue
                
                if get_value[1] > parent_value:
                    parent_value = get_value[1]
                    best_node = move
            return [True, parent_value, best_node]
        else:
            best_node = [[]]
            parent_value = - parent_value
            for move in can_move(crr_state, 'player'):
                get_value = mini_max(move, deepth - 1, not get_max_profit, parent_value)
                
                if not get_value[0]:
                    continue
                
                if get_value[1] < parent_value:
                    parent_value = get_value[1]
                    best_node = move
            return [True, parent_value, best_node]


# In[24]:


def bot_turn(crr_state, deepth):
    '''
        crr_state: a Node
        return: new state (best move get in minimax(state))
    '''
    new_state = mini_max(crr_state, deepth, True, 10000)[2]
    return new_state


# In[25]:


def finish(state):
    '''
        state: current state of game
        return: True, winner (winner: bot or player)
        - True: 5 point in line
    '''
    if get_ls_plot(state)[0].__len__() == 0:
        return False, 'no one'
    elif count_line(state, 5, 'bot') > 0:
        return True, 'bot'
    elif count_line(state, 5, 'player') > 0:
        return True, 'player'
    return False, 'no one'


# In[26]:


# cs = [['o', '.', '.', '.', '.'], 
#       ['x', 'o', '.', '.', '.'], 
#       ['x', '.', 'o', '.', '.'],
#       ['.', 'x', '.', 'x', '.'],
#       ['.', 'x', '.', '.', 'o']]
# display(cs)


# In[27]:




def player_turn(state, plot):
    '''
        state: current state of game
        return: new state with that move
    '''
    new_state = move(state, plot, 'player')
    return new_state




def display(state):
    '''
        Node: a Class
        print(state)
    '''
    for row in range(state.__len__()):
        for col in range(state[0].__len__()):
            if state[row][col] == turn_form['player']:
                put_a_point(col + 0.5, row + 0.05, 'player')
            elif state[row][col] == turn_form['bot']:
                put_a_point(col + 0.5, row + 0.05, 'bot')







def load_game():
    num_plot = 20   #int(input('Number x Number plot: '))
    state_initial = [['.' for col in range(num_plot)] for row in range(num_plot)]
    return state_initial


deep = 1
main_state = load_game()


size = 20

import turtle
import time
def caro_game(x, y):
    '''
        declare: deep
        state: Node class
    '''
    global main_state, deep
    # deep = int(input('Enter the level of game: '))
    # state = load_game()
    x, y = int(x), int(y)
    main_state = player_turn(main_state, str(y) + '-' + str(x))
    caro.penup()
    display(main_state)
    
    
    if not finish(main_state)[0]:
        main_state = bot_turn(main_state, deep)
        display(main_state)
        
        if finish(main_state)[0]:
            print('Bot win!')
    
    elif finish(main_state)[1] == 'player':
        print('You win!')
    else:
        print('No more blank plot!')
    # time.sleep(5.5)


caro = turtle.Turtle()
caro.penup()

def put_a_point(x, y, turn):
    if turn == 'bot':
        caro.color('red')
    else:
        caro.color('blue')
    caro.goto(x , y)
    caro.pendown()
    caro.begin_fill()
    caro.circle(0.45)
    caro.end_fill()
    caro.penup()
    caro.hideturtle()


# Graphics





screen = turtle.Screen()
screen.onclick(caro_game)
screen.setup(screen.screensize()[1]*2,screen.screensize()[1]*2)
screen.setworldcoordinates(-1,size,size,-1)
screen.bgcolor('white')
screen.tracer(500)


border = turtle.Turtle()
border.speed(9)
border.penup()

side = (size-1)/2

i=-1
for start in range(size):
    border.goto(start,side + side *i)    
    border.pendown()
    i*=-1
    border.goto(start,side + side *i)     
    border.penup()
    
i=1
for start in range(size):
    border.goto(side + side *i,start)
    border.pendown()
    i *= -1
    border.goto(side + side *i,start)
    border.penup()


screen.listen()
screen.mainloop()

turtle.done()


# In[ ]:


# caro_game()


# In[ ]:




