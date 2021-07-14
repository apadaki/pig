import numpy as np
import matplotlib.pyplot as plt


def get_val(f, i, j):
    if i >= len(f):
        return 1
    if j >= len(f):
        return 0

    return f[i][j]

def get_probabilities(n, die=6):
    f = [[0 for i in range(n)] for j in range(n)]
    
    m = n-1

    for y in range(m, -1, -1):
        for x in range(m, -1, -1):
            if x == m and y == m:
                f[x][y] = die/(die+1)
            elif x == y:
                q = 0
                for i in range(2,7):
                    q += 1/6 * (1-get_val(f, x, x+i))
                f[x][y] = 6/7 * (q + 1/6)
            else:
                q1,q2 = 0,0
                for i in range(2,7):
                    q1 += 1/6 * (1-get_val(f, y, x+i))
                    q2 += 1/6 * (1-get_val(f, x, y+i))
                f[x][y] = (36*q1-6*q2+5)/35
                f[y][x] = (36*q2-6*q1+5)/35
    return f

def generate_prob_contour(prob_mat, filename='contour.png'):
    x = np.arange(0, 100, 1)
    y = np.arange(0, 100, 1)
    X, Y = np.meshgrid(x,y)
    Z = prob_mat[X,Y]
    fig, ax = plt.subplots()
    CS = ax.contour(X, Y, Z, levels=10)
    ax.clabel(CS, inline=True, fontsize=10)
    ax.set_title('Contour plot of probability matrix')
    ax.set_xlabel('current player score')
    ax.set_ylabel('other player score')
    
    plt.savefig(filename)
    

def hold(f, x, y, r):
    hold_val = 1-get_val(f, y, x+r)
    roll_val = 1/6 * (1-get_val(f, y, x))
    for i in range(2,7):
        roll_val += 1/6 * (1-get_val(f, y, x+r+i))
    return 1 if hold_val > roll_val else 0 

def save_matrix(prob_mat, filename='probabilities.txt'):
    with open(filename,'wb') as f:
        for line in prob_mat:
            np.savetxt(f, line)

def load_probabilities(filename='probabilities.txt'):
    return np.loadtxt(filename)


# f = get_probabilities(100)
# prob_mat = np.matrix(f)
# save_matrix(prob_mat)
# f = load_probabilities()
# generate_prob_counter(prob_mat)

