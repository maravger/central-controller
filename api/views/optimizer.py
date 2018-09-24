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
HOSTS = len(settings.GLOBAL_SETTINGS['HOST_IPS']) 
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

def permutate_ntua():
    op1 = 0
    op2 = 1
    combinations = []
    for i in range(0, len(U_PES_MAX[0])):
        for j in range(0, len(U_PES_MAX[1])):
            if (U_PES_MAX[op1][i] + U_PES_MAX[op2][j]) <= MAX_TOTAL_CONT_PES:
                combination = [i, j]
                combinations.append(combination)

    for i in range(0,len(U_PES_MAX[2]),2):
        for j in range (0,len(U_PES_MAX[3]),2):
            if (U_PES_MAX[op1+2][i] + U_PES_MAX[op2+2][j]) <= MAX_TOTAL_CONT_PES:
                combination = [i,j]
                combinations.append(combination)
    return combinations

def optimize(combinations, predictedWorkload):
    n = len(combinations)
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
        lpsolve('add_constraint', lp, row3, LE, HOSTS)
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
    HOST_OPEN =  (lpsolve('get_objective', lp))
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
                final.append([0,0])

# start of second lp
    colno = []
    row = []

    lp = lpsolve('make_lp', 0, n)
    lpsolve('set_verbose', lp, IMPORTANT)


    for i in range (1,n+1):
        lpsolve('set_col_name', lp, i, 'p'+str(i))
        lpsolve('set_int', lp, i, True)


    lpsolve('set_add_rowmode', lp, True)


    # first    
    for i in range (0,n):
        colno.append(i+1)
        row.append(U_REQ_REF[0][combinations[i][0]])
        
    lpsolve('add_constraintex', lp, row, GE, predictedWorkload[0])


    #second
    colno1 = []
    row1 = []
    for i in range (0,n):
        colno1.append(i+1)
        row1.append(U_REQ_REF[1][combinations[i][1]])

    lpsolve('add_constraint', lp, row1, GE, predictedWorkload[1])

    #third

    colno2 = []
    row2 = []
    colno2 = [0] * n
    row2 = [0] * n

    for i in range (0,n):
        colno2[i] = i+1
        row2[i] = 1
        lpsolve('add_constraint', lp, row2, GE, 0)
        colno2 = [0] * n
        row2 = [0] * n


    colno3 = []
    row3 = []
    colno3 = [0] * n
    row3 = [0] * n

    for i in range (0,n):
        colno3[i] = i+1
        row3[i] = 1
        lpsolve('add_constraint', lp, row3, LE, HOST_OPEN)
        colno3 = [0] * n
        row3 = [0] * n


    colno4 = []
    row4 = []
    for i in range (0,n):
        colno4.append(i+1)
        row4.append(1)

    lpsolve('add_constraint', lp, row4, EQ, HOST_OPEN)


    lpsolve('set_add_rowmode', lp, False)
    colno5 = []
    row5 = []
    for i in range (0,n):
        colno5.append(i+1)
        row5.append(combinations[i][0]+int(combinations[i][1]))

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
    print len(temp[0])
    lpsolve('delete_lp', lp)
    for i in range(0, len(temp[0])):
        while (temp[0][i] > 0):
            temp[0][i] -= 1
            final.append(combinations[i])
    for i in range(len(final), HOSTS):
        final.append([0,0])

    return final
    #return [[1,1],[1,1]]


def optimize_ntua(combinations, predictedWorkload):
    n = 25
    n1 = 9
    ntotal = n + n1
    ncol=ntotal
    colno = []
    row = []

    lp = lpsolve('make_lp', 0, ntotal)
    lpsolve('set_verbose', lp, IMPORTANT)


    for i in range (1,ntotal+1):
        lpsolve('set_col_name', lp, i, 'p'+str(i))
        lpsolve('set_int', lp, i, True)


    lpsolve('set_add_rowmode', lp, True)

    # first    
    for i in range (0,ntotal):
        colno.append(i+1)
        if i <=24:
            row.append(U_REQ_REF[0][combinations[i][0]])
        else: 
            row.append(U_REQ_REF[2][combinations[i][0]])
    lpsolve('add_constraintex', lp, row, GE, predictedWorkload[0])


    #second
    colno1 = []
    row1 = []
    for i in range (0,ntotal):
        colno1.append(i+1)
        if i <=24:
            row1.append(U_REQ_REF[1][combinations[i][1]])
        else:    
            row1.append(U_REQ_REF[3][combinations[i][1]])

    lpsolve('add_constraint', lp, row1, GE, predictedWorkload[1])

    #third

    colno2 = []
    row2 = []
    colno2 = [0] * ntotal
    row2 = [0] * ntotal

    for i in range (0,ntotal):
        colno2[i] = i+1
        row2[i] = 1
        lpsolve('add_constraint', lp, row2, GE, 0)
        colno2 = [0] * ntotal
        row2 = [0] * ntotal


    colno3 = []
    row3 = []
    colno3 = [0] * ntotal
    row3 = [0] * ntotal
    HOSTS=1
    for i in range (0,ntotal):
        #colno3[i] = i+1
        if i<=24:
            colno3[i] = i+1
            row3[i] = 1
            lpsolve('add_constraint', lp, row3, LE, HOSTS)
        else:   
            colno3[i] = i+1 
            row3[i] = 1
            lpsolve('add_constraint', lp, row3, LE, 1)
        colno3 = [0] * ntotal
        row3 = [0] * ntotal

    colno4 = []
    row4 = []
    for i in range (0,ntotal):
        if i<=24:
            colno4.append(i+1)
            row4.append(1)
        else:
            colno4.append(i+1)
            row4.append(0)
           


    HOSTS = 1
    lpsolve('add_constraint', lp, row4, LE, HOSTS)

    colno7 = []
    row7 = []
    for i in range (0,ntotal):
        if i>24:
            colno7.append(i+1)
            row7.append(1)
        else:
            colno7.append(i+1)
            row7.append(0)

    HOSTS =1
    lpsolve('add_constraint', lp, row7, LE, HOSTS)
    HOSTS=2


    lpsolve('set_add_rowmode', lp, False)
    colno5 = []
    row5 = []
    for i in range (0,ntotal):
        colno5.append(i+1)
        row5.append(1)

    lpsolve('set_obj_fn', lp, row5)

    lpsolve('set_minim', lp)


    lpsolve('write_lp', lp, 'a.lp')
    #print (lpsolve('get_mat', lp, 1, 2))
    lpsolve('solve', lp)
    #print ("objective")
    #print (lpsolve('get_objective', lp))
    HOST_OPEN = (lpsolve('get_objective', lp))
    #print ("variables")

    #print (lpsolve('get_variables', lp))
    a = []
    a = (lpsolve('get_variables', lp)[0])


    HOST_NTUA=0
    HOSTS_EDGE=0
    for i in range (0,ntotal):
        #print ((combinations[i], i)  if a[i]>=1.0 else 'skata')
        if a[i] >= 1.0 and i < n:
            HOSTS_EDGE+=int(a[i])
        elif a[i]>=1.0 and i>=n:
            HOST_NTUA+=1

    #print HOSTS_EDGE , HOST_NTUA
    #print ("constraints")
    #print (lpsolve('get_constraints', lp))

    temp = []
    final = []
    temp = (lpsolve('get_variables', lp))
    #print len(temp[0])
    lpsolve('delete_lp', lp)
    for i in range(0, len(temp[0])):
        while (temp[0][i] > 0):
            temp[0][i] -= 1
            final.append(combinations[i])
    for i in range(len(final), HOSTS):
        final.append([0,0])



    #print final


    #print ("---------------------------------------------")
    #print ("start of second lp")


    n = 25
    n1 = 9
    ntotal = n + n1
    #print ntotal
    ncol=ntotal
    colno = []
    row = []

    lp = lpsolve('make_lp', 0, ntotal)
    lpsolve('set_verbose', lp, IMPORTANT)


    for i in range (1,ntotal+1):
        lpsolve('set_col_name', lp, i, 'p'+str(i))
        lpsolve('set_int', lp, i, True)


    lpsolve('set_add_rowmode', lp, True)


    # first    
    for i in range (0,ntotal):
        colno.append(i+1)
        if i <=24:
            row.append(U_REQ_REF[0][combinations[i][0]])
        else: 
            row.append(U_REQ_REF[2][combinations[i][0]])
    lpsolve('add_constraintex', lp, row, GE, predictedWorkload[0])


    #second
    colno1 = []
    row1 = []
    for i in range (0,ntotal):
        colno1.append(i+1)
        if i <=24:
            row1.append(U_REQ_REF[1][combinations[i][1]])
        else:    
            row1.append(U_REQ_REF[3][combinations[i][1]])

    lpsolve('add_constraint', lp, row1, GE, predictedWorkload[1])

    #third

    colno2 = []
    row2 = []
    colno2 = [0] * ntotal
    row2 = [0] * ntotal

    for i in range (0,ntotal):
        colno2[i] = i+1
        row2[i] = 1
        lpsolve('add_constraint', lp, row2, GE, 0)
        colno2 = [0] * ntotal
        row2 = [0] * ntotal


    colno3 = []
    row3 = []
    colno3 = [0] * ntotal
    row3 = [0] * ntotal
    HOSTS=1
    for i in range (0,ntotal):
        #colno3[i] = i+1
        if i<=24:
            colno3[i] = i+1
            row3[i] = 1
            lpsolve('add_constraint', lp, row3, LE, HOSTS)
        else:   
            colno3[i] = i+1 
            row3[i] = 1
            lpsolve('add_constraint', lp, row3, LE, 1)
        colno3 = [0] * ntotal
        row3 = [0] * ntotal

    colno4 = []
    row4 = []
    for i in range (0,ntotal):
        if i<=24:
            colno4.append(i+1)
            row4.append(1)
        else:
            colno4.append(i+1)
            row4.append(0)
           



    lpsolve('add_constraint', lp, row4, EQ, HOSTS_EDGE)

    colno7 = []
    row7 = []
    for i in range (0,ntotal):
        if i>24:
            colno7.append(i+1)
            row7.append(1)
        else:
            colno7.append(i+1)
            row7.append(0)


    lpsolve('add_constraint', lp, row7, EQ, HOST_NTUA)



    lpsolve('set_add_rowmode', lp, False)
    colno5 = []
    row5 = []
    for i in range (0,ntotal):
        colno5.append(i+1)
        row5.append(combinations[i][0]+int(combinations[i][1]))

    lpsolve('set_obj_fn', lp, row5)

    lpsolve('set_minim', lp)


    lpsolve('write_lp', lp, 'a.lp')
    #print (lpsolve('get_mat', lp, 1, 2))
    lpsolve('solve', lp)
    #print ("objective")
    #print (lpsolve('get_objective', lp))
    HOST_OPEN = (lpsolve('get_objective', lp))
    #print ("variables")

    print (lpsolve('get_variables', lp))
    a = []
    a = (lpsolve('get_variables', lp)[0])
    HOSTS=2
    temp = []
    final = []



    print a
    for i in range (0,ntotal):
        if a[i] >= 1.0 and i < n:
            while (a[i]>0):
     	        a[i] -= 1
    	        final.append(combinations[i])
       
        elif a[i]>=1.0 and i>=n:
    	    while (a[i]>0):
     	        a[i] -= 1
    	        final.append(combinations[i])
        if i == n-1:
     	    for j in range (len(final), 1):
    	        final.append([0,0])
    	
    for j in range (len(final), 2):
        final.append([0,0])

    return final

