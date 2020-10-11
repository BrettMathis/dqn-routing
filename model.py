#!/usr/bin/env python3

import params

def Mdist(a,b):
    return sum([abs(x-y) for x,y in zip(a,b)])

# weakly-connected DAG
class net:

# vertices are name -> [x, y, dist_from_source,
#                       current layer being actively drawn on, layers]
    v={}
# edges are [v1, v2, layer]
# do we need this array? do we ever use it? do i dare take it out?
# the answer to all the above questions is "no"
    e=[]
# edict is {v -> (unique edge with v as the sink) for all v in vertices}
    edict={}
# close tracks the closest routed vertex to each sink
# {v -> [closest_vertex, distance]}
    close={}
# this is the unique source
    p=''
# this is a list of final sinks
# i also technically don't need this array
# since by definition self.close.keys() == self.k
    k=[]
# next available name for vertex creation
    next_name=0

# port_dic:
# 'name' -> [x,y]
    def __init__(self,port_dic):
        for a,b in port_dic:
            if a[0]==0:
                self.p=a
                dist=0
            else:
                self.k.append(a)
                dist=-1
            self.v[a]=[*b[:2],dist,1,[0,1]]
        for a in self.k:
            self.close[a]=self.p
        next_name+=len(list(port_dic.keys()))

    # Shortest path from source to target vertex
    def shortest(self,v):
        return self.v[v][2]

    # Modeling the impedance from source to target vertex
    # The impedance approximation is composed of two parts:
    # - Weighted sum of currently-routed wire segments along the shortest path
    # - As-of-yet-unrouted distance scaled up by the OPEN_CIRCUIT_K parameter
    def imped(self,v):
        c = self.close(v)
        ret = Mdist(self.v[v][0:2],self.v[c][0:2])*params.OCK
        ret += self.shortest(c)

    # Sum of impedances from source to all sinks
    # This is a piss-poor loss function
    def loss(self):
        ret = 0
        for a in k:
            ret+=self.imped(a)
        return ret

    # The following are wrappers for the QN movement actions
    # These are the ways that the net graph can be modified

    def valid_actions(self,v):
        ret = []

        L = self.v[v][-1]
        x = self.v[v][0]
        y = self.v[v][1]

        if L[0]>0:
            ret.append('down')
        if L[-1]<params.MM:
            ret.append('up')
        if x>params.GSQ:
            ret.append('W')
        if x<(params.GX-params.GSQ):
            ret.append('E')
        if y>params.GSQ:
            ret.append('S')
        if y<(params.GY-params.GSQ):
            ret.append('N')

    # Via up
    def up(self,v):
        L = self.v[v][-1]
        aL = self.v[v][-2]+1
        self.v[v][-2] = aL
        if aL not in L:
            L = L+[aL]

    # Via down
    def down(self,v):
        L = self.v[v][-1]
        aL = self.v[v][-2]-1
        self.v[v][-2] = aL
        if aL not in L:
            L = [aL]+L

    # General move function for all directions
    # If possible, extend the previous net and just move this vertex
    def move(self,v,man_dir):
        # Grab vertex info
        [X,Y,dist,aL,L] = self.v[v]

        # We can go ahead and update the distance-from-source now
        dist += params.GSQ * params.MI[aL]

        # We can also go ahead and update the position
        if man_dir=='N':
            Y+=params.GSQ
        if man_dir=='S':
            Y-=params.GSQ
        if man_dir=='E':
            X+=params.GSQ
        if man_dir=='W':
            X-=params.GSQ

        # Grab the edge that terminates in this node
        prev_e = self.edict.get(v,[0,0,'',0])

        # If we can extend the edge
        if prev_e[-1] == aL:
        # Just move the vertex :)
            self.v[v]=[X,Y,aL,L]
            return

        # If we cannot extend the edge, make a new vertex and edge
        # This is the only time in this entire class that new e/v are made
        new_v = [X,Y,dist,aL,[aL]]
        new_name = self.next_name
        self.v[new_name]=new_v
        new_e = [v,new_name,aL]
        self.e.append(new_e)
        self.edict[new_name] = new_e
        self.next_name+=1
        
        # Update self.close
        for a in self.close:
            new_dist = Mdist(self.v[v][0:2],self.v[a][0:2])
            if new_dist < self.close[a][-1]:
                self.close[a]=[new_name,new_dist]

    def N(self,v):
        self.move(v,'N')
    def S(self,v):
        self.move(v,'S')
    def W(self,v):
        self.move(v,'W')
    def E(self,v):
        self.move(v,'E')
