#!/usr/bin/env python3

import sys
sys.path.append("..")

from model import model

net = model.net([[5,5],[0,0],[10,10]])
assert net.v[0][:2]==[5,5]
assert net.next_name==3
print(net)

print(net.N(0))
assert net.next_name==4
assert net.v[3][:2]==[5,6]
print(net)

print(net.N(3))
assert net.next_name==4
assert net.v[3][:2]==[5,7]
print(net)

print(net.E(3))
assert net.next_name==4
assert net.v[3][:2]==[6,7]
print(net)

print(net.up(3))
assert net.next_name==4
assert net.v[3][:2]==[6,7]
assert net.v[3][-1]==[1,2]
print(net)

print(net.E(3))
assert net.next_name==5
assert net.v[3][:2]==[6,7]
assert net.v[4][:2]==[7,7]
print(net)

print(net.E(4))
assert net.next_name==5
assert net.v[4][:2]==[8,7]
print(net)
