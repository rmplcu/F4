import random

def print_mat(mat):
    for x in mat:
        print(x)

def is_sublist(lis, sub):
    for i in range(len(lis)):
        if lis[i] == sub[0]:
            n = 1
            while n<len(sub) and i+n<len(lis) and lis[i+n] == sub[n]:
                n+=1
            
            if n == len(sub):
                return True

    return False

def init_mat():
    mat = []
    for i in range(6):
        row = []
        for j in range(7):
            row.append(0)
    
        mat.append(row)

    return mat

def check_win(mat):
    #horizontal win
    for x in mat:
        if is_sublist(x,['X', 'X', 'X', 'X']): 
            return True, 'X'
        elif is_sublist(x, ['O', 'O', 'O', 'O']):
            return True, 'O'

    #vertical win
    for j in range(7):
        d = []        
        for i in range(6):
            d.append(mat[i][j])
        
        if is_sublist(d, ['X', 'X', 'X', 'X']): 
            return True, 'X'
        elif is_sublist(d, ['O', 'O', 'O', 'O']):
            return True, 'O'

    #diagonal1 win
    for i in range(3):
        for j in range(4):
            d = []
            for k in range(6):
                if j+k < 7 and i+k < 6:
                    d.append(mat[i+k][j+k])
                
            if is_sublist(d, ['X', 'X', 'X', 'X']): 
                return True, 'X'
            elif is_sublist(d, ['O', 'O', 'O', 'O']):
                return True, 'O'

    #diagonal2 win
    for i in range(3, 6):
        for j in range(4):
            d = []
            for k in range(6):
                if j+k < 7 and i-k >= 0:
                    d.append(mat[i-k][j+k])
            
            if is_sublist(d, ['X', 'X', 'X', 'X']): 
                return True, 'X'
            elif is_sublist(d, ['O', 'O', 'O', 'O']):
                return True, 'O'

    for x in mat:
        for j in x:
            if j == 0:
                return False, None

    return True, None

def is_final(mat):
    res, _ = check_win(mat)
    return res

def utility(mat):
    _, w = check_win(mat)
    if w == 'O':
        return 1
    elif w == 'X': 
        return -1 
    else: return 0

def is_legal(mat, action):
    for i in range(6):
        if mat[i][action] == 0: return True
    
    return False

def next_state(mat, action, char):
    for i in range(6):
        if mat[5-i][action] == 0:
            mat[5-i][action] = char
            return 5-i, action

def max_val(mat, alpha, beta, depth):
    if is_final(mat) or depth == 0: return (utility(mat), random.randint(0, 6))

    v = -10
    ac=None
    for a in range(7):
        if is_legal(mat, a):
            x, y = next_state(mat, a, 'O')
            mval, _ = min_val(mat, alpha, beta, depth-1)
            mat[x][y] = 0
            if mval > v:
                v = mval
                ac = a
            
            if v>=beta: return v, ac
            if v > alpha: alpha=v

    return (v, ac)

def min_val(mat, alpha, beta, depth):
    if is_final(mat) or depth == 0: return (utility(mat), random.randint(0, 6))

    v = 10
    ac=None
    for a in range(7):
        if is_legal(mat, a):
            x, y = next_state(mat, a, 'X')
            mval, _ = max_val(mat, alpha, beta, depth-1)
            mat[x][y] = 0
            if mval<v:
                v=mval
                ac=a
            
            if v <= alpha: return v, ac
            if v <beta :beta = v

    return (v, ac)

def alpha_beta_pruning(mat):   
    return max_val(mat, -10, 10, 6)