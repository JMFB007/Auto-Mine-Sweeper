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
    for sc in group:
        for a in sc.arround:
            a.checked = True
    for sc in group:
        sc.checked = False
    counter = [0 for i in range(len(group))]
    posibilities = [posib(group)]
    done = False
    while not done:#runs through all groups
        done = True
        for g in posibilities:#list of groups
            print("over")
            #print("   pos a:",len(posibilities))
            if not g.full:
                for sc in g.group:#group of scuares
                    if not sc.flagged or not sc.visible:
                        obvious = False
                        mined = False
                        for a in sc.arround:#arround each scuare
                            if isinstance(a.type, int) and a.visible:
                                ammount = int(a.type)
                                invis = 0
                                for a in sc.arround:
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
                            if mined:
                                sc.flagged = True
                            else:
                                sc.visible = True
                        else:
                            g.split = True
                            sc.visible = True
                            if checkposib(sc):
                                posibilities.append(posib(g.group))
                            sc.visible = False
                            sc.flagged = True
                            if not checkposib(sc):
                                posibilities.append(posib(g.group))
                            g.failed = True
                            break
            g.full = True
            for sc in g.group:#checks if full
                if not sc.flagged and not sc.visible:
                    done = False
                    g.full = False
        x = True
        while x:
            x = False
            for g in posibilities:
                if g.failed:
                    posibilities.remove(g)
                    x = True
                    break
                if g.split:
                    pass
        print("done?", done)
    print("   posibilities:", len(posibilities))
    for g in posibilities:#adds to the counter list
        for sc in g.group:
            if sc.flagged:
                counter[g.group.index(sc)] += 1
    return counter