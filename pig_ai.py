import numpy as np
import matplotlib.pyplot as plt


def get_val(f, i, j):
    if i >= len(f):
        return 1
    if j >= len(f):
        return 0

    return f[i][j]

def get_probabilities(n, die=6):
    print('computing AI probabilities...')
    f = [[0 for i in range(n)] for j in range(n)]
    
    m = n-1

    for y in range(m, -1, -1):
        for x in range(m, -1, -1):
            if x == m and y == m:
                f[x][y] = die/(die+1)
            elif x == y:
                q = 0
                for i in range(2,die+1):
                    q += 1/die * (1-get_val(f, x, x+i))
                f[x][y] = die/(die+1) * (q + 1/die)
            else:
                q1,q2 = 0,0
                for i in range(2,die+1):
                    q1 += 1/die * (1-get_val(f, y, x+i))
                    q2 += 1/die * (1-get_val(f, x, y+i))
                f[x][y] = (die**2*q1-die*q2+die-1)/(die**2-1)
                f[y][x] = (die**2*q2-die*q1+die-1)/(die**2-1)
    print('...finished computing AI probabilities\n')
    
    return f

def generate_prob_contour(prob_mat, target=100, filename='images/prob_contour.png'):
    x = np.arange(0, target, 1)
    y = np.arange(0, target, 1)
    X, Y = np.meshgrid(x,y)
    Z = prob_mat[X,Y]
    fig, ax = plt.subplots()
    CS = ax.contour(X, Y, Z, levels=10)
    ax.clabel(CS, inline=True, fontsize=10)
    ax.set_title('Probability matrix contour')
    ax.set_xlabel('current player score')
    ax.set_ylabel('other player score')
    print('saved AI probability contour to {}\n'.format(filename))
    plt.savefig(filename)

def generate_cutoff_contour(f, target=100, filename='images/cutoff_contour.png'):
    g = [[0 for i in range(target)] for j in range(target)]

    for i in range(100):
        for j in range(100):
            for r in range(100):
                if hold(f,i,j,r)[0]:
                    g[i][j] = r
                    break
    cutoff_mat = np.matrix(g)
    x = np.arange(0, target, 1)
    y = np.arange(0, target, 1)
    X, Y = np.meshgrid(x,y)
    Z = cutoff_mat[X,Y]
    fig, ax = plt.subplots()
    CS = ax.contour(X, Y, Z, levels=20)
    ax.clabel(CS, inline=True, fontsize=10, fmt = '%d')
    ax.set_title('Minimum number of points before holding')
    ax.set_xlabel('current player score')
    ax.set_ylabel('other player score')
    print('saved cutoff contour to {}\n'.format(filename))
    plt.savefig(filename)

    

def hold(f, x, y, r, die=6):
    hold_val = 1-get_val(f, y, x+r)
    roll_val = 1/die * (1-get_val(f, y, x))
    for i in range(2,die+1):
        roll_val += 1/die * (1-get_val(f, y, x+r+i))
    return [(1 if hold_val > roll_val else 0), hold_val, roll_val] 

def save_matrix(prob_mat, filename='probabilities.txt'):
    with open(filename,'wb') as f:
        for line in prob_mat:
            np.savetxt(f, line)
    print('saved AI probability matrix to {}\n'.format(filename))

def load_probabilities(filename='probabilities.txt'):
    print('AI probabilities loaded\n')
    return np.loadtxt(filename)

if __name__ == '__main__':
    # f = get_probabilities(100)
    # generate_cutoff_contour(f)
    # prob_mat = np.matrix(f)
    # generate_prob_contour(prob_mat)
    # save_matrix(prob_mat)
    # f = load_probabilities()

