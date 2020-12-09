# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 15:09:33 2020

@author: sshaf
"""

import numpy as np
from ypstruct import structure

def run(problem, params, method="classic"):
    
    # Problem Informtaion
    costfunc = problem.costfunc
    nvar = problem.nvar
    key = problem.key

    # Parameters
    maxit = params.maxit
    npop = params.npop
    beta = params.beta
    pc = params.pc

    varmin = 48
    varmax = 83

    nc = int(np.round(pc * npop / 2) * 2) 
    gamma = params.gamma
    mu = params.mu
    
    
    # Empty Individual Template
    empty_individual = structure()
    empty_individual.chords = None
    empty_individual.cost = None
    
    # BestSolution Ever found
    bestsol = empty_individual.deepcopy()
    bestsol.cost = np.inf

    # WorstSolution Ever found
    worstsol = empty_individual.deepcopy()
    worstsol.cost = np.NINF
    
    # Initialiaze Population
    pop = empty_individual.repeat(npop)
    for i in range(npop):
        pop[i].chords = initChords(getNotesInKey(key),nvar)
        pop[i].cost = costfunc(pop[i].chords,nvar)
        if pop[i].cost < bestsol.cost:
            bestsol = pop[i].deepcopy()
        if pop[i].cost > worstsol.cost:
            worstsol = pop[i].deepcopy()

    # Best Cost of iterations
    bestcost = np.empty(maxit)
    
    # Worst Cost of iterations
    worstcost = np.empty(maxit)
    
    # Main Loop of GA
    for it in range(maxit):
        costs = np.array([ x.cost for x in pop])
        avg_cost = np.mean(costs)
        if avg_cost != 0:
            costs = costs / avg_cost
        probs = np.exp(-beta * costs)

        popc = []
        for _ in range(nc // 2):
            
            # Parent Selection (Random)
            q = np.random.permutation(npop)
            p1 = pop[q[0]]
            p2 = pop[q[1]]
            
            #Perform Roulette Wheel Selection
            p1 = pop[roulette_wheel_selection(probs)]
            p2 = pop[roulette_wheel_selection(probs)]
            
            # Perform Crossover
            c1, c2 = crossover(p1, p2, gamma)
            
            # Perform Mutation
            c1 = mutate(c1, key, mu)
            c2 = mutate(c2, key, mu)
            
            # Apply Bounds
            apply_bounds(c1, varmin, varmax)
            apply_bounds(c2, varmin, varmax)
            
            #Evaluate First Offspring
            c1.cost = costfunc(c1.chords,nvar)
            if c1.cost < bestsol.cost:
                bestsol = c1.deepcopy()
            if c1.cost > worstsol.cost:
                worstsol = c1.deepcopy()
            
            #Evaluate Second Offspring
            c2.cost = costfunc(c2.chords,nvar)
            if c2.cost < bestsol.cost:
                bestsol = c2.deepcopy()
            if c2.cost > worstsol.cost:
                worstsol = c2.deepcopy()

            #Add Offsprings to popc
            popc.append(c1)
            popc.append(c2)
            
        # Merge Sort and Select
        pop += popc 
        pop = sorted(pop, key=lambda x: x.cost)
        pop = pop[0:npop]
        
        #Store Best Cost
        bestcost[it] = bestsol.cost
        
        #Store Worst Cost
        worstcost[it] = pop[-1].cost
        
        #Show Iteration Information
#        print("Iteration {}: Best Cost = {} / Worst Cost = {}".format(it,
#        bestcost[it], worstcost[it]))
    
            
    #Output
    out = structure()
    out.pop = pop
    out.bestsol = bestsol
    out.bestcost = bestcost 
    out.worstsol = worstsol
    out.worstcost = worstcost
    return out

def crossover(p1, p2, gamma=0.1):
    c1 = p1.deepcopy()
    c2 = p1.deepcopy()

    if np.random.rand() < gamma:
        y = np.random.randint(0,len(c1.chords))
        c1f = c1.chords[0:y]
        c1l = c1.chords[y:-1]
        c2f = c2.chords[0:y]
        c2l = c2.chords[y:-1]
        c1.chords = c1f + c2l
        c2.chords = c2f + c1l
    return c1, c2

def mutate(x, key, mu):
    y = x.deepcopy()
    if np.random.rand() < mu:
        y.chords[np.random.randint(0,len(y.chords))] = createChord(getNotesInKey(key))
    return y

def apply_bounds(x, varmin, varmax):
    for chord in x.chords:
        chord = np.maximum(chord, varmin)
        chord = np.minimum(chord, varmax)
    
def roulette_wheel_selection(p):
    c = np.cumsum(p)
    r = sum(p) * np.random.rand()
    ind = np.argwhere(r <= c)
    return ind[0][0]

def removearray(L,arr):
    ind = 0
    size = len(L)
    while ind != size and not np.array_equal(L[ind].chords,arr.chords):
        ind += 1
    if ind != size:
        L.pop(ind)
    else:
        raise ValueError('array not found in list.')
    return L

def initChords(key,nvar):
    chordprog = []
    for _ in range(nvar):
        chordprog.append(createChord(key))

    return chordprog

def createChord(key):
    n1 = np.random.choice(key) + (np.random.choice([4,5,6]) * 12)
    n2 = np.random.choice(key) + (np.random.choice([4,5,6]) * 12)

    chord = []
    if n1 == n2:
        chord.append(n1)
        chord.append(n2)
    else:
        chord.append(min(n1,n2))
        chord.append(max(n1,n2))
    return chord

def getNotesInKey(keyString):
    '''FOR NOW WE ARE ONLY DOING C NATURAL MAJOR'''
    key = [0,2,4,5,7,9,11] 
    return key
