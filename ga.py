# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 15:09:33 2020

@author: sshaf
"""

import numpy as np
from ypstruct import structure

def run(problem, params, method = "classic"):
    
    # Problem Informtaion
    costfunc = problem.costfunc
    nvar = problem.nvar
    varmin = problem.varmin
    varmax = problem.varmax
    
    # Parameters
    maxit = params.maxit
    npop = params.npop
    beta = params.beta
    pc =params.pc

    nc = int(np.round(pc*npop/2)*2) 
    gamma = params.gamma
    mu = params.mu
    
    
    # Empty Individual Template
    empty_individual = structure()
    empty_individual.chords= None
    empty_individual.cost = None
    
    # BestSolution Ever found
    bestsol = empty_individual.deepcopy()
    bestsol.cost = np.NINF

    # WorstSolution Ever found
    worstsol = empty_individual.deepcopy()
    worstsol.cost = np.inf
    
    # Initialiaze Population
    pop = empty_individual.repeat(npop)
    for i in range (npop):
        pop[i].chords = initChords(varmax,varmin,nvar)
        pop[i].cost=costfunc(pop[i].chords)
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
        avg_cost= np.mean(costs)
        if avg_cost != 0:
            costs = costs/avg_cost
        probs = np.exp(-beta*costs)

        #Niching methods
        # if method == "crowding":
        #     crowding(pop,npop,gamma,mu,sigma,varmin,varmax,costfunc)

        popc = []
        for _ in range(nc//2):
            
            # Parent Selection (Random)
            q = np.random.permutation(npop)
            p1 = pop[q[0]]
            p2 = pop[q[1]]
            
            #Perform Roulette Wheel Selection
            p1 = pop[roulette_wheel_selection(probs)]
            p2 = pop[roulette_wheel_selection(probs)]
            
            # Perform Crossover
            c1, c2=crossover(p1, p2, gamma)
            
            # Perform Mutation
            c1=mutate(c1, mu)
            c2=mutate(c2, mu)
            
            # Apply Bounds
            apply_bounds(c1, varmin, varmax)
            apply_bounds(c2, varmin, varmax)
            
            #Evaluate First Offspring
            c1.cost = costfunc(c1.chords)
            if c1.cost < bestsol.cost:
                bestsol = c1.deepcopy()
            if c1.cost > worstsol.cost:
                worstsol = c1.deepcopy()
            
            #Evaluate Second Offspring
            c2.cost = costfunc(c2.chords)
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
        print("Iteration {}: Best Cost = {} / Worst Cost = {}".format(it, bestcost[it], worstcost[it]))
    
            
    #Output
    out = structure()
    out.pop=pop
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

def mutate(x, mu):
    y = x.deepcopy()
    if np.random.rand() < mu:
        if np.random.rand() <= .5:
            y.chords[np.random.randint(0,len(y.chords))][np.random.randint(0,len(y.chords[0]))] = y.chords[np.random.randint(0,len(y.chords))][np.random.randint(0,len(y.chords[0]))] - 1
        if np.random.rand() >= .5:
            y.chords[np.random.randint(0,len(y.chords))][np.random.randint(0,len(y.chords[0]))] = y.chords[np.random.randint(0,len(y.chords))][np.random.randint(0,len(y.chords[0]))] + 1
    return y

def apply_bounds(x, varmin, varmax):
    for chord in x.chords:
        chord = np.maximum(chord, varmin)
        chord = np.minimum(chord, varmax)
    
def roulette_wheel_selection(p):
    c=np.cumsum(p)
    r=sum(p)*np.random.rand()
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

def initChords(varmax,varmin,nvar):
    chordprog = []
    for _ in range(0,nvar):
        chord = np.random.randint(varmin,varmax,size=(2))
        chord.sort()
        chordprog.append(chord)

    return chordprog
