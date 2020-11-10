#!/usr/bin/env python3

import sys
sys.path.append("..")

from model import design,net,params
from training_data.gates import *
from training_data.rca8 import *
from training_data.csa8 import *
from training_data.cskipa8 import *
from training_data.cla8 import *

DEF=[]
stdcells=[]
nets=[]
netlist=[]

ref_design = make_csa8(10);

[DEF, stdcells, nets, netlist] = compile_design(ref_design);

#stdcells.append(["INV",["Y"],["A"]])
#stdcells.append(["AND",["Y"],["A","B"]])

#DEF.append(["cell1","INV",0,0])
#DEF.append(["cell2","AND",5,5])
#DEF.append(["cell3","INV",3,3])

#nets.append("net1")
#nets.append("net2")
#nets.append("net3")

#netlist.append(["cell1","INV",{"A":"net3","Y":"net1"}])
#netlist.append(["cell3","INV",{"A":"net2","Y":"net3"}])
#netlist.append(["cell2","AND",{"A":"net1","B":"net3","Y":"net2"}])

print("DEF: ");
print(DEF);
print("stdcells: ");
print(stdcells);
print("nets: ");
print(nets);
print("netlist: ");
print(netlist);


