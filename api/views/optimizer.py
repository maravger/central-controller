from django.conf import settings
from lpsolve55 import *

U_PES_MIN = settings.GLOBAL_SETTINGS['U_PES_MIN']
U_PES_MAX = settings.GLOBAL_SETTINGS['U_PES_MAX']
U_REQ_MIN = settings.GLOBAL_SETTINGS['U_REQ_MIN']
U_REQ_MAX = settings.GLOBAL_SETTINGS['U_REQ_MAX']
X_ART_REF = settings.GLOBAL_SETTINGS['X_ART_REF']
U_PES_REF = settings.GLOBAL_SETTINGS['U_PES_REF']
U_REQ_REF = settings.GLOBAL_SETTINGS['U_REQ_REF']

K1 = settings.GLOBAL_SETTINGS['K1']
K2 = settings.GLOBAL_SETTINGS['K2']
MAX_TOTAL_CONT_PES = settings.GLOBAL_SETTINGS['MAX_TOTAL_CONT_PES']
HOSTS = 2 
def permutate():
    op1 = 0
    op2 = 1
    combinations = []
    for i in range(0, len(U_PES_MAX[0])):
        for j in range(0, len(U_PES_MAX[1])):
            if (U_PES_MAX[op1][i] + U_PES_MAX[op2][j]) <= MAX_TOTAL_CONT_PES:
                combination = [i, j]
                combinations.append(combination)

    return combinations
#    print combinations


def optimize(combinations, predictedWorkload):
    n = len(combinations)
    print n
    ncol = n
    colno = []
    row = []

    lp = lpsolve('make_lp', 0, n)
    lpsolve('set_verbose', lp, IMPORTANT)

    for i in range(1, n + 1):
        lpsolve('set_col_name', lp, i, 'p' + str(i))
        lpsolve('set_int', lp, i, True)

    lpsolve('set_add_rowmode', lp, True)

    # first
    for i in range(0, n):
        colno.append(i + 1)
        row.append(U_REQ_REF[0][combinations[i][0]])

    lpsolve('add_constraintex', lp, row, GE, predictedWorkload[0])

    # second
    colno1 = []
    row1 = []
    for i in range(0, n):
        colno1.append(i + 1)
        row1.append(U_REQ_REF[1][combinations[i][1]])
    lpsolve('add_constraint', lp, row1, GE, predictedWorkload[1])

    # third

    colno2 = []
    row2 = []
    colno2 = [0] * n
    row2 = [0] * n

    for i in range(0, n):
        colno2[i] = i + 1
        row2[i] = 1
        lpsolve('add_constraint', lp, row2, GE, 0)
        colno2 = [0] * n
        row2 = [0] * n

    colno3 = []
    row3 = []
    colno3 = [0] * n
    row3 = [0] * n

    for i in range(0, n):
        colno3[i] = i + 1
        row3[i] = 1
        lpsolve('add_constraint', lp, row3, LE, 3)
        colno3 = [0] * n
        row3 = [0] * n

    colno4 = []
    row4 = []
    for i in range(0, n):
        colno4.append(i + 1)
        row4.append(1)

    lpsolve('add_constraint', lp, row4, LE, HOSTS)
    lpsolve('set_add_rowmode', lp, False)
    colno5 = []
    row5 = []
    for i in range(0, n):
        colno5.append(i + 1)
        row5.append(1)

    lpsolve('set_obj_fn', lp, row5)

    lpsolve('set_minim', lp)

    lpsolve('write_lp', lp, 'a.lp')
    #print (lpsolve('get_mat', lp, 1, 2))
    lpsolve('solve', lp)
    #print ("objective")
    print (lpsolve('get_objective', lp))
    #print ("variables")
    #print (lpsolve('get_variables', lp))
    #print ("constraints")
    #print (lpsolve('get_constraints', lp))

    temp = []
    final = []
    temp = (lpsolve('get_variables', lp))
    lpsolve('delete_lp', lp)

    print len(temp[0])
    for i in range(0, len(temp[0])):
        while (temp[0][i] > 0):
            temp[0][i] -= 1
            final.append(combinations[i])
    for i in range(len(final), HOSTS):
                final.append([1,1])
    #
    #print final
    #return final
    return [[1,1],[1,1]]




