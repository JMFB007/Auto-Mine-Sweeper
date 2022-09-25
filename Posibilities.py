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
        if isinstance(a.type, int) and a.visible:#each number arround the scuare
            for sa in a.arround:#arround the numbers
                ammount = int(a.type)
                flagged = 0
                if sa.checked and sa.flagged:
                    flagged += 1
            if ammount < flagged:#imposible
                posible = False
    return posible

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
    print("------")

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
    #todavia hay una posibilidad donde queda en tbd
    while not done:#runs through all groups
        acc(posibilities)
        done = True
        for group in posibilities:# X works on groups if obvious
            if not group.full:
                for scuare in group.group:
                    if not scuare.flagged and not scuare.visible:
                        obvious = False
                        mined = False
                        for a in scuare.arround:#arround each scuare
                            if isinstance(a.type, int) and a.visible:
                                ammount = int(a.type)
                                flagged = 0
                                invis = 0
                                for a in scuare.arround:
                                    if a.checked:
                                        if a.flagged:
                                            flagged += 1
                                        elif not a.visible:
                                            invis += 1
                                if ammount == invis:#100% all mines
                                    obvious = True
                                    mined = True
                                elif ammount == flagged:#100% all safe
                                    obvious = True
                                #else it remains false in obvious
                        if obvious:
                            if mined:
                                scuare.flagged = True
                            else:
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
                        scuare.visible = True
                        reveal = checkposib(scuare)
                        scuare.visible = False
                        scuare.flagged = True
                        flag = checkposib(scuare)
                        break
                print(f"reveal: {reveal}, flag: {flag}")
                if reveal:
                    newreveal = group.group[:]
                    full = True
                    for scuare in newreveal:
                        if not scuare.flagged and not scuare.visible:
                            print("split and revealed")
                            full = False
                            scuare.visible = True
                            break
                    r = posib(newreveal)
                    r.full = full
                    posibilities.append(r)
                if flag:
                    newflag = group.group[:]
                    full = True
                    for scuare in newflag:
                        if not scuare.flagged and not scuare.visible:
                            print("split and flagged")
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
                    if not scuare.flagged or not scuare.visible:
                        group.full = False
        acc(posibilities)
        print("------------------")
    print("TOTAL POSIBILITIES:", len(posibilities))
    raise SystemExit(0)

    for group in posibilities:#adds to the counter list
        for scuare in group.group:
            if scuare.flagged:
                counter[group.group.index(scuare)] += 1
    return counter