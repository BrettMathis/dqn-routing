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
# Randomly chosen
assert(des.active==['net1',0])

state=des.get_state()
#print(des.nets["net1"].loss())
#print(des.nets["net2"].loss())
#print(des.nets["net3"].loss())
print(des.global_loss(state))

#print(des.nets["net1"].loss())
#print(des.switching_factor())
#print(des.nets["net1"])

des.do_action(translate=False,"N")
state=des.get_state()
#print(des.nets["net1"].loss())
print(des.global_loss(state))
#print(des.nets["net1"])
assert(des.active==['net1',2])

des.do_action(translate=False,"switch2")
assert(des.active==['net1',0])
print(des.global_loss(des.get_state()))

des.do_action(translate=False,"E")
print(des.global_loss(des.get_state()))
des.do_action(translate=False,"E")
print(des.global_loss(des.get_state()))
des.do_action(translate=False,"N")
print(des.global_loss(des.get_state()))
des.do_action(translate=False,"up")
print(des.global_loss(des.get_state()))
des.do_action(translate=False,"W")
print(des.global_loss(des.get_state()))
des.do_action(translate=False,"W")
print(des.global_loss(des.get_state()))

print(des.switching_factor())
exit()

des.do_action(translate=False,"switch4")
assert(des.active==['net1',2])


des.do_action(translate=False,"N")
print(des.global_loss(des.get_state()))
des.do_action(translate=False,"N")
print(des.global_loss(des.get_state()))
des.do_action(translate=False,"E")
print(des.global_loss(des.get_state()))
des.do_action(translate=False,"E")
print(des.global_loss(des.get_state()))
des.do_action(translate=False,"N")
print(des.global_loss(des.get_state()))
des.do_action(translate=False,"N")
print(des.global_loss(des.get_state()))
des.do_action(translate=False,"E")
print(des.global_loss(des.get_state()))
des.do_action(translate=False,"E")
print(des.global_loss(des.get_state()))
des.do_action(translate=False,"E")

# Check net1 is finished
assert(des.nets["net1"].all_done)

# Check clean-up was done properly
for x in des.nets["net1"].v:
    assert(x in [0,1])

# Check net1 can no longer be switched to
for x in des.switching_factor():
    assert("net1" not in x)

state=des.get_state()

#Check all metal2 routing was properly cleaned
for x in state:
    for y in x:
        assert(y[2]==0)
        assert(y[2+params.MM+1]==0)

print(des.global_loss(state))
