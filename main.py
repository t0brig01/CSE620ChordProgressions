import numpy as np
import math
import matplotlib.pyplot as plt
from ypstruct import structure
import ga
import csv
import abjad 
import midi
import pygame

#parameters
pM = 0.01
pC = 0.8
trial_count = 1
convert = ['c','cs','d','ds','e','f','fs','g','gs','a','as','b']

#Camparing the notes within each generated chord
def check_interval(chord):
    res = 0
    #Higher than an octave = bad
    if chord[1] - chord[0] > 12 or chord[1] - chord[0] < 0:
        res += 15
    #same note = bad
    if chord[0] == chord[1]:
        res += 15
    #0 and 11 sounds bad
    if chord[1] - chord[0] == 11:
        res += 15
    #Clashing bad
    if chord[1] - chord[0] == 1 or chord[1] - chord[0] == 2:
        res += 15
    return res

#Comparing between two chords to avoid consecutive fifhts and octave, and
#intervals bigger than a fifth
def check_2_chords(c1, c2):
    res = 0

    # Check for 5° and 8°
    ite1 = map(lambda x, y: y - x, c1[:-1], c1[1:])
    ite2 = map(lambda x, y: y - x, c2[:-1], c2[1:])
    for inter1, inter2 in zip(ite1, ite2):
        if inter1 == 7 and inter2 == 7:
            res += 15
        elif inter1 == 0 and inter2 == 0:
            res += 15
        elif inter1 == 12 and inter2 == 12:
            res += 15

    if c1[0] == c2[0] and c1[1] == c2[1]:
        res += 30
        
    # check for large intervals
    for note1, note2 in zip(c1, c2):
        if abs(note1 - note2) == 7:  # 7 equals 5° interval
            res -= 1
    return res

#Evaluate chords based on metrics
def evaluteError(chords,nvar):
    #passes pop.chords
    res = 0
    if len(chords) < nvar:
        res += 100
    for i in range(len(chords)):
        res += check_interval(chords[i])
        if chords[i - 1] is None:
            continue
        else:
            res += check_2_chords(chords[i],chords[i - 1])
    return res

#create measures of generated music
def ChordProgToPic(pop):
    chords = []
    for chord in pop.chords:
        chordString = ""
        for note in chord:
            chordString += convert[note % 12]
            if np.floor(note / 12) - 1 == 4:
                chordString += "' "
            elif np.floor(note / 12) - 1 == 5:
                chordString += "'' "
            elif np.floor(note / 12) - 1 == 6:
                chordString += "''' "
            else:
                chordString += " "
        chords.append(abjad.Chord("<" + chordString + ">4"))
    container = abjad.Container(chords)
    abjad.show(container)

problem = structure()
##definition of cost function
problem.costfunc = evaluteError

##defenition of search space
problem.nvar = 8
problem.key = "CnM" # C natural Major

#GA Parameters
params = structure()
## maximum iteration
params.maxit = 100  
params.npop = 50
params.beta = 1
params.pc = 1
params.gamma = pC
## mutation parameters
params.mu = pM
params.sigma = 0.1

x = 0
max = []
min = []
avg = []

while x < trial_count:
    #Run GA
    out = ga.run(problem, params,"classic")
    max.append(np.max(out.bestcost))
    min.append(np.min(out.worstcost))
    avg.append(sum(out.bestcost) / len(out.bestcost))
    print("Run " + str(x + 1) + " done")
    x += 1

print("Max: " + str(np.max(max)))
print("Min: " + str(np.min(min)))
print("Average: " + str(sum(avg) / trial_count))

print(out.bestsol)
ChordProgToPic(out.bestsol)
midi.run(out.bestsol)

#play midi output
pygame.init()
pygame.mixer.music.load("output.mid")
pygame.mixer.music.play()
length = pygame.time.get_ticks()
while pygame.mixer.music.get_busy():
    pygame.time.wait(length)