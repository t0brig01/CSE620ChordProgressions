import numpy as np
import numpy as np
import math
import matplotlib.pyplot as plt
from ypstruct import structure
import ga
import csv

#parameters
pM = 0.1
pC = 0.1
trial_count = 1
benchmark = 4 #use 1 or 4

OPTIONS_M = ((0, -3, 5),
             (0, -3, 5),
             (0, -4, 5),
             (0, -3, 6),
             (0, -3, 5),
             (0, -4, 5),
             (0, -4, 5)
             )
OPTIONS_m = ((0, -4, 5),
             (0, -4, 5),
             (0, -3, 5),
             (0, -3, 5),
             (0, -4, 5),
             (0, -3, 6),
             (0, 5)
             )
MOD_M = ('M', 'm', 'm', 'M', 'M', 'm', 'd')
MOD_m = ('m', 'd', 'M', 'm', 'M', 'M', 'M')

def check_interval(chord):
    res = 0
    if chord[2] - chord[1] > 12 or chord[2] - chord[1] < 0:
        res += 15
    if chord[3] - chord[2] > 12 or chord[3] - chord[2] < 0:
        res += 15

    if chord[1] == chord[2] or chord[2] == chord[3]:
        res += 1.4
    return res

def check_2_chords(c1, c2):
    res = 0

    # Check for 5° and 8°
    ite1 = map(lambda x, y: y - x, c1[:-1], c2[1:])
    ite2 = map(lambda x, y: y - x, c1[:-1], c2[1:])
    for inter1, inter2 in zip(ite1, ite2):
        if inter1 == 7 and inter2 == 7:
            res += 15
        elif inter1 == 0 and inter2 == 0:
            res += 15
        elif inter1 == 12 and inter2 == 12:
            res += 15

    # Check for big intervals
    for note1, note2 in zip(c1[1:], c2[1:]):
        if abs(note1 - note2) >= 7:  # 7 equals 5° interval
            res += .7

    return res
'''fix this'''
def evalNumErr(ton, individual):
    #Fitness function
    res = 0
    for prev, item, nex in neighborhood(individual):
        res += check_interval(item[0])
        if prev is None:
            if item[1] != 0:
                res += 6
            continue
        else:
            if prev[1] in [4, 6] and item[1] in [3, 1]:
                res += 20
            res += check_2_chords(prev[0], item[0])
        if nex is None:
            if item[1] in [1, 2, 3, 4, 5, 6]:
                res += 6
    return (res,)

problem= structure()
##definition of cost function
problem.costfunc = evalNumErr
##defenition of search space
problem.nvar = 4
problem.varmin = 0 
problem.varmax = 1 

#GA Parameters
params=structure()
## maximum iteration
params.maxit = 100  

params.npop = 50
params.beta = 1

params.pc = 1
params.gamma = pC
## mutation parameters
params.mu = pM
params.sigma = 0.1

x=0
max = []
min = []
avg = []
#Classic
#Sharing
while x < trial_count:
    #Run GA
    out = ga.run(problem, params,"classic")
    max.append(np.max(out.bestcost))
    min.append(np.min(out.worstcost))
    avg.append(sum(out.bestcost)/len(out.bestcost))
    print("Run " + str(x+1) + " done")
    x += 1

print("Max: " + str(np.max(max)))
print("Min: "+ str(np.min(avg)))
print("Average: "+ str(sum(avg)/10))
#Results
#plt.plot(out.bestcost)
plt.plot(out.bestcost, label = "best")
plt.plot(out.worstcost, label = "worst")
plt.axis([0,params.maxit,0,1])
plt.xlabel("Iteration")
plt.ylabel("Best Cost")
plt.title("Genetic Algorithm (GA)")
plt.grid(True)
plt.legend()
plt.show()