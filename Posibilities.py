import pygame

class posib():
    def __init__(self, group):
        self.full = False
        self.failed = False
        self.split = False
        self.group = group
#turn into a list of lists that keeps going untill all are full
#then count and add to the variable of the original list and return
def checkposib(sc):
    posible = True
    for a in sc.arround:
        if isinstance(a.type, int) and a.visible:
            ammount = int(a.type)
            invis = 0
            for suba in a.arround:
                if suba.flagged and suba.checked:
                    ammount -= 1
                elif not suba.visible and suba.checked:
                    invis += 1
            if ammount != 0:
                posible = False
    return posible

def posibilities(group):
    #only the ones arround are true checked
    for scuare in group:#only the NOT highlighted ones are checked
        for a in scuare.arround:
            a.checked = True
    for scuare in group:
        scuare.checked = False
    counter = [0 for i in range(len(group))]
    posibilities = [posib(group)]
    done = False

    """done: False len posib: 1
   not full check
   not full check
   split check"""

    while not done:#runs through all groups
        done = True
        for group in posibilities:#works on groups if obvious
            if not group.full:
                for scuare in group.group:
                    if not scuare.flagged and not scuare.visible:
                        obvious = False
                        mined = False
                        for a in scuare.arround:#arround each scuare
                            if isinstance(a.type, int) and a.visible:
                                ammount = int(a.type)
                                invis = 0
                                for a in scuare.arround:
                                    if a.flagged and a.checked:
                                        ammount -= 1
                                    elif not a.visible and a.checked:
                                        invis += 1
                                if ammount == 0:
                                    obvious = True
                                    mined = False
                                elif ammount == invis:
                                    obvious = True
                                    mined = True
                        if obvious:
                            print("obvious")
                            if mined:
                                scuare.flagged = True
                            else:
                                scuare.visible = True
                        else:
                            group.split = True

        reveal = False
        flag = False
        for group in posibilities:#split = True if its in a non obvious point
            if group.split:
                for scuare in group.group:
                    if not scuare.flagged and not scuare.visible:
                        scuare.visible = True
                        reveal = checkposib(scuare)
                        scuare.visible = False
                        scuare.flagged = True
                        flag = checkposib(scuare)
                        break
                if reveal:
                    newreveal = group.group[:]
                    for scuare in newreveal:
                        if not scuare.flagged and not scuare.visible:
                            print("split and revealed")
                            scuare.visible = True
                            break
                    posibilities.append(posib(newreveal))
                if flag:
                    newflag = group.group[:]
                    for scuare in newflag:
                        if not scuare.flagged and not scuare.visible:
                            print("split and flagged")
                            scuare.flagged = True
                            break
                    posibilities.append(posib(newflag))
        
        for group in posibilities:#done = True if all posibilities are revelaed or flagged
            if not group.full:
                group.full = True
                for scuare in group.group:
                    if not scuare.flagged or not scuare.visible:
                        print("not done")
                        done = False
                        group.full = False
        
        print("done:", done,"len posib:",len(posibilities))
    print("TOTAL POSIBILITIES:", len(posibilities))

    for group in posibilities:#adds to the counter list
        for scuare in group.group:
            if scuare.flagged:
                counter[group.group.index(scuare)] += 1
    return counter