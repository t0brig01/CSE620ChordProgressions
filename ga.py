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
    ## nc = number of children
    nc = int(np.round(pc*npop/2)*2) 
    gamma = params.gamma
    mu = params.mu
    sigma = params.sigma
    
    
    # Empty Individual Template
    empty_individual = structure()
    empty_individual.position= None
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
        pop[i].position = np.random.uniform(varmin,varmax,nvar)
        pop[i].cost=costfunc(pop[i].position)
        if pop[i].cost > bestsol.cost:
            bestsol = pop[i].deepcopy()
        if pop[i].cost < worstsol.cost:
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
        if method == "sharing":
            sharing(pop,sigma,1)
        if method == "crowding":
            crowding(pop,npop,gamma,mu,sigma,varmin,varmax,costfunc)
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
            c1=mutate(c1, mu, sigma)
            c2=mutate(c2, mu, sigma)
            
            # Apply Bounds
            apply_bounds(c1, varmin, varmax)
            apply_bounds(c2, varmin, varmax)
            
            #Evaluate First Offspring
            c1.cost = costfunc(c1.position)
            if c1.cost > bestsol.cost:
                bestsol = c1.deepcopy()
            if c1.cost < worstsol.cost:
                worstsol = c1.deepcopy()
            
            #Evaluate Second Offspring
            c2.cost = costfunc(c2.position)
            if c2.cost > bestsol.cost:
                bestsol = c2.deepcopy()
            if c2.cost < worstsol.cost:
                worstsol = c2.deepcopy()

            #Add Offsprings to popc
            popc.append(c1)
            popc.append(c2)
            
        # Merge Sort and Select
        pop += popc 
        pop = sorted(pop, key=lambda x: x.cost,reverse=True)
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
     alpha = np.random.uniform(-gamma,1+gamma, *c1.position.shape)
     c1.position = alpha*p1.position + (1-alpha)*p2.position
     c2.position = alpha*p2.position + (1-alpha)*p1.position
     return c1, c2
    
def mutate(x, mu, sigma):
    y = x.deepcopy()
    flag = (np.random.rand(*x.position.shape) <= mu)
    ind = np.argwhere(flag)
    y.position[ind] += sigma*np.random.randn(*ind.shape)
    return y

def apply_bounds(x, varmin, varmax):
    x.position = np.maximum(x.position, varmin)
    x.position = np.minimum(x.position, varmax)
    
def roulette_wheel_selection(p):
    c=np.cumsum(p)
    r=sum(p)*np.random.rand()
    ind = np.argwhere(r <= c)
    return ind[0][0]
        
def d(p,c):
    return abs(sum(p.position)-sum(c.position))

def removearray(L,arr):
    ind = 0
    size = len(L)
    while ind != size and not np.array_equal(L[ind].position,arr.position):
        ind += 1
    if ind != size:
        L.pop(ind)
    else:
        raise ValueError('array not found in list.')
    return L

def sh(dist, sigmaShare,alpha):
    if dist < sigmaShare:
        return 1 - np.power(dist/sigmaShare,alpha)
    else:
        return 0
def crowding(pop,npop,gamma,mu,sigma,varmin,varmax,costfunc):
    q = np.random.permutation(npop)
    p1 = pop[q[0]]
    p2 = pop[q[1]]

    # Perform Crossover
    c1, c2=crossover(p1, p2, gamma)
    
    # Perform Mutation
    c1=mutate(c1, mu, sigma)
    c2=mutate(c2, mu, sigma)
    
    # Apply Bounds
    apply_bounds(c1, varmin, varmax)
    apply_bounds(c2, varmin, varmax)
    
    c1.cost = costfunc(c1.position)
    c2.cost = costfunc(c2.position)

    if (d(p1,c1) + d(p2,c2)) <= (d(p1,c2)+d(p2,c1)):
        if c1.cost > p1.cost:
            pop = removearray(pop,p1)
            pop.append(c1)
        if c2.cost > p2.cost:
            pop = removearray(pop,p2)
            pop.append(c2)
    else:
        if c2.cost > p1.cost:
            pop = removearray(pop,p1)
            pop.append(c2)
        if c1.cost > p2.cost:
            pop = removearray(pop,p2)
            pop.append(c1)

def sharing(pop,sigmaShare,alpha):
    for i in range(len(pop)):
        shSum = 0
        for j in range(len(pop)):
            if np.array_equal(pop[i].position,pop[j].position): continue
            shSum += sh(d(pop[i],pop[j]),sigmaShare,alpha)
        if shSum == 0: continue
        pop[i].cost = pop[i].cost / shSum
