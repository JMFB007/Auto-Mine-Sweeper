import pygame

class Node():
    def __init__(self, scuare):
        self.scuare = scuare
        self.level = 0
        self.left = None
        self.right = None

class Tree():
    def __init__(self,group):
        self.root = Node(group[0])
        self.group = group
        self.groupper = [len(group)]
    
    def PreorderTraversal(self):
      for sc in self.group:
        if sc != self.root:
            obvio = False
            tienemina = False
            for subsc in sc.arround:#es obvio? (alrededor del inicial) x
                if subsc.visible and not subsc.flagged and isinstance(subsc.type, int) and not subsc.checked:
                    ammount = int(subsc.type)
                    invis = 0
                    for a in sc.arround:#conteo banderas y vacios por alrededor del inicial
                        if a.flagged:
                            ammount -= 1
                        elif not a.visible:
                            invis += 1
                    if ammount == invis:
                        obvio = True
                        tienemina = True
                    elif ammount == 0:
                        obvio = True
                        tienemina = False
      if root:
         res.append(root.data)
         res = res + self.PreorderTraversal(root.left)
         res = res + self.PreorderTraversal(root.right)
      return res