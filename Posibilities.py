import pygame
from Scuare import Scuare

class posib():
    def __init__(self, group):
        self.full = False
        self.failed = False
        self.split = False
        self.group = group
#multiplies by 2^n
def checkposib(sc):#reveal, flag
    flag = True
    reveal = True
    c = sc.copy()
    c.flagged = True
    for a in c.arround:
        if isinstance(a.type, int) and a.visible and a.checked:#each number arround the scuare
            ammount = int(a.type)
            flagged = 0
            invis = 0
            for sa in a.arround:#arround the numbers
                if sa.flagged:
                    flagged += 1
                if not sa.visible and not sa.flagged:
                    invis += 1
            print("ammount < flagged: ", ammount < flagged)
            print("(flagged < ammount) and (invis == 0): ", (flagged + invis < ammount))
            if ammount < flagged or (flagged + invis < ammount):#imposible
                flag = False
    c.flagged = False
    c.visible = True
    for a in c.arround:
        if isinstance(a.type, int) and a.visible and a.checked:#each number arround the scuare
            ammount = int(a.type)
            flagged = 0
            invis = 0
            for sa in a.arround:#arround the numbers
                if sa.flagged:
                    flagged += 1
                if not sa.visible and not sa.flagged:
                    invis += 1
            print("ammount < flagged: ", ammount < flagged)
            print("(flagged < ammount) and (invis == 0): ", (flagged + invis < ammount))
            if ammount < flagged or (flagged + invis < ammount):#imposible
                reveal = False
    return reveal, flag

def obviousmined(sc):#flag, show
    flag = False
    show = False
    for a in sc.arround:
        if isinstance(a.type, int) and a.visible and a.checked:
            ammount = int(a.type)
            flagged = 0
            invis = 0
            for b in a.arround:
                if b.flagged:
                    flagged += 1
                elif not b.visible and not b.flagged:
                    invis += 1
            if ammount - flagged == invis:#100% all mines
                flag = True
            if ammount == flagged:#100% all safe amount - flagged
                show = True
    return flag, show

def acc(posibilities):
    total = len(posibilities)
    split = 0
    full = 0
    failed = 0
    for group in posibilities:
        if group.split:
            split += 1
        if group.full:
            full += 1
        if group.failed:
            failed += 1
    print(f"TOTAL: {total}, tbd: {total-split-full-failed}, split: {split}, full: {full}, failed: {failed}")

def posibilities(group):
    for scuare in group:#only the checked ones should be taken into account
        scuare.checked = False
    counter = [0 for i in range(len(group))]
    ax = []
    for sc in group:
        ax.append(sc.copy())
    posibilities = [posib(ax)]
    done = False
    while not done:#runs through all groups
        acc(posibilities)
        done = True
        for group in posibilities:# X works on groups if obvious
            if not group.full:
                for scuare in group.group:
                    if not scuare.flagged and not scuare.visible:
                        flag, show = obviousmined(scuare)
                        if flag:
                            scuare.flagged = True
                        elif show:
                            scuare.visible = True
                        else:
                            group.split = True
        acc(posibilities)
        reveal = False
        flag = False
        for group in posibilities:# X split = True if its in a non obvious point
            if group.split:
                for scuare in group.group:
                    if not scuare.flagged and not scuare.visible:
                        reveal, flag = checkposib(scuare)
                        break
                print(f"reveal: {reveal}, flag: {flag}")
                if reveal:
                    newreveal = []
                    for sc in group.group:
                        newreveal.append(sc.copy())
                    full = True
                    for scuare in newreveal:
                        if not scuare.flagged and not scuare.visible:
                            full = False
                            scuare.visible = True
                            break
                    r = posib(newreveal)
                    r.full = full
                    posibilities.append(r)
                if flag:
                    newflag = []
                    for sc in group.group:
                        newflag.append(sc.copy())
                    full = True
                    for scuare in newflag:
                        if not scuare.flagged and not scuare.visible:
                            full = False
                            scuare.flagged = True
                            break
                    f = posib(newflag)
                    f.full = full
                    posibilities.append(f)
                if reveal or flag:#desecha el grupo que fue dividido
                    group.split = False
                    group.failed = True
        acc(posibilities)
        clear = False
        while not clear:# X deletes all failed ones
            clear = True
            for group in posibilities:
                if group.failed:
                    clear = False
                    posibilities.remove(group)

        for group in posibilities:# X done = True if all posibilities are revelaed or flagged
            if not group.full:
                done = False
                group.full = True
                for scuare in group.group:
                    if not scuare.flagged and not scuare.visible:
                        group.full = False
        
        """for group in posibilities:#verificador
            if not group.full:
                sh = []
                for scuare in group.group:
                    if scuare.flagged:
                        sh.append(1)
                    elif scuare.visible:
                        sh.append(2)
                    else:
                        sh.append(0)
                print(sh)"""
        
        acc(posibilities)
        print("------------------")
        pygame.time.delay(2000)
    print("TOTAL POSIBILITIES:", len(posibilities))

    for group in posibilities:#adds to the counter list
        for scuare in group.group:
            if scuare.flagged:
                counter[group.group.index(scuare)] += 1
    #raise SystemExit(0)
    return counter