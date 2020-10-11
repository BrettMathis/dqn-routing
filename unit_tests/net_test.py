#!/usr/bin/env python3

import sys
sys.path.append("..")

from model import model,params

net = model.net([[5,5],[0,0],[10,10]])
print(net)
assert net.v[0][:2]==[5,5]
assert net.next_name==3
assert net.imped(1)==(5+5)*params.OCK
assert net.imped(2)==(5+5)*params.OCK

print(net.N(0))
print(net)
assert net.next_name==4
assert net.v[3][:2]==[5,6]
assert net.imped(1)==(5+5)*params.OCK
assert net.imped(2)==(4+5)*params.OCK+1*params.MI[1]

print(net.N(3))
print(net)
assert net.next_name==4
assert net.v[3][:2]==[5,7]
assert net.imped(1)==(5+5)*params.OCK
assert net.imped(2)==(3+5)*params.OCK+2*params.MI[1]

print(net.E(3))
print(net)
assert net.next_name==4
assert net.v[3][:2]==[6,7]
assert net.imped(1)==(5+5)*params.OCK
assert net.imped(2)==(3+4)*params.OCK+3*params.MI[1]

print(net.up(3))
print(net)
assert net.next_name==4
assert net.v[3][:2]==[6,7]
assert net.v[3][-1]==[1,2]
assert net.imped(1)==(5+5)*params.OCK
print(net.imped(2))
assert net.imped(2)==(3+4)*params.OCK+3*params.MI[1]

print(net.E(3))
print(net)
assert net.next_name==5
assert net.v[3][:2]==[6,7]
assert net.v[4][:2]==[7,7]
assert net.imped(1)==(5+5)*params.OCK
assert net.imped(2)==(3+4)*params.OCK+3*params.MI[1]

print(net.E(4))
print(net)
assert net.next_name==5
assert net.v[4][:2]==[8,7]
assert net.imped(1)==(5+5)*params.OCK
assert net.imped(2)==(3+3)*params.OCK+2*params.MI[2]+3*params.MI[1]

net.E(4)
net.E(4)
net.N(4)
net.N(4)
net.N(4)
print(net.down(4))
print(net)
print(net.imped(2))
