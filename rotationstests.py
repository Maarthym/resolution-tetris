#test d'utilisation de matrices rotations pour calculer les rotations des différents tetrominos

Rpis2 = [[0,-1],
         [1,0]]

def rotation(mat):
    """
    à un couple (i,j) de coordonnées dans une matrice carrée de taille impaire, on effectue la rotation centrée en c =(n-1)/2
    alors (i',j') = (c,c) + R_{pi/2}((i-c,j-c)) = (c,c) + (j-c, c-i)
    """
    n = len(mat)#supposée carrée de taille impaire
    c = (n-1)//2
    res = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if mat[i][j] == 1:
                res[j][2*c-i] = 1
    return res

ligne = [[0,0,0,0,0],[0,0,0,0,0], [0,1,1,1,1],[0,0,0,0,0],[0,0,0,0,0]]
l1 = [[0,0,1],[1,1,1], [0,0,0]]
l2 = [[1,0,0],[1,1,1], [0,0,0]]
c = [[0,1,1],[0,1,1], [0,0,0]]
z1 = [[1,1,0],[0,1,1], [0,0,0]]
z2 = [[0,1,1],[1,1,0], [0,0,0]]
t = [[0,1,0],[1,1,1], [0,0,0]]


def printmat(m):
    print("")
    for line in m:
        print(line)
    print("")

def transpose(mat):
    return [[mat[j][i] for j in range(len(mat))] for i in range(len(mat))]
