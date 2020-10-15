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
nets.append("net3")

netlist.append(["cell1","INV",{"A":"net3","Y":"net1"}])
netlist.append(["cell3","INV",{"A":"net2","Y":"net3"}])
netlist.append(["cell2","AND",{"A":"net1","B":"net3","Y":"net2"}])

des = design.design(DEF,stdcells,nets,netlist)


for n in des.nets.values():
    print(n)

print(des.grid[0][0])
print(des.grid[5][5])
print(des.grid[3][3])
print(des.active)

state=des.get_state()
print(des.nets["net1"].loss())
print(des.nets["net2"].loss())
print(des.nets["net3"].loss())
print(des.global_loss(state))

print(des.nets["net1"].loss())
print(des.global_loss(state))
print(des.switching_factor())
print(des.nets["net1"])

des.do_action("N")
print(des.nets["net1"].loss())
print(des.global_loss(state))
print(des.switching_factor())
print(des.nets["net1"])
des.do_action("N")
des.do_action("N")
des.do_action("E")
des.do_action("E")
des.do_action("N")
des.do_action("N")
des.do_action("E")
des.do_action("E")
des.do_action("E")
print(des.nets["net1"].loss())
print(des.global_loss(state))
print(des.switching_factor())
print(des.nets["net1"])

#for a in des.nets.values():
#    print(a.loss())

state=des.get_state()
print(des.global_loss(state))
