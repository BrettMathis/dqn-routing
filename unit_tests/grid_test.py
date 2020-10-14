#!/usr/bin/env python3

import sys
sys.path.append("..")

from model import design,net,params

DEF=[]
stdcells=[]
nets=[]
netlist=[]

stdcells.append(["INV",["Y"],["A"]])
stdcells.append(["AND",["Y"],["A","B"]])

DEF.append(["cell1","INV",0,0])
DEF.append(["cell2","AND",5,5])
DEF.append(["cell3","INV",3,3])

nets.append("net1")
nets.append("net2")

netlist.append(["cell1","INV",{"Y":"net1"}])
netlist.append(["cell3","INV",{"A":"net2"}])
netlist.append(["cell2","AND",{"A":"net1","Y":"net2"}])

des = design.design(DEF,stdcells,nets,netlist)

print(des.grid[0][0])
print(des.grid[5][5])
print(des.grid[3][3])
