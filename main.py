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