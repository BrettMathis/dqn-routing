#!/usr/bin/env python3

from model import params

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
    p=0
# this is a list of final sinks
# i also technically don't need this array
# since by definition self.close.keys() == self.k
    k=[]
# next available name for vertex creation
    next_name=0

    def __str__(self):
        ret="Vertices\n"
        for name,v in self.v.items():
            ret+=str(name)+' -> '+str(v)+'\n'
            ret+="Valid actions: "+str(self.valid_actions(name))+'\n'
        ret+="Edges\n"
        for e in self.e:
            ret+=str(e)+'\n'
        return ret


# port_list:
# [[x,y], ... ]
# first element is source
    def __init__(self,port_list):
        tmpflag=True
        for b in port_list:
            a = self.next_name
            if tmpflag:
                p=a
                dist=0
                tmpflag=False
            else:
                self.k.append(a)
                dist=-1
            self.v[a]=[*b,dist,1,[0,1]]
            self.next_name+=1
        for a in self.close:
            self.close[a]=[self.p,Mdist(b,self.v[a][:2])]

    def _make_v(self,new_v):
        new_name = self.next_name
        self.next_name+=1
        self.v[new_name]=new_v
        return new_name

    def _make_e(self,new_e):
        self.e.append(new_e)
        self.edict[new_e[1]] = new_e

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

        if L[0]>1:
            ret.append('down')
        if L[-1]<params.MM:
            ret.append('up')
        if y<(params.GY-params.GSQ):
            ret.append('N')
        if y>params.GSQ:
            ret.append('S')
        if x<(params.GX-params.GSQ):
            ret.append('E')
        if x>params.GSQ:
            ret.append('W')
        return ret

    # Via up
    def up(self,v):
        [X,Y,dist,aL,L]=self.v[v][:]
        aL+=1
        if aL not in L:
            L = L+[aL]
        self.v[v]=[X,Y,dist,aL,L]
        return v

    # Via down
    def down(self,v):
        [X,Y,dist,aL,L]=self.v[v][:]
        aL-=1
        if aL not in L:
            L = [aL]+L
        self.v[v]=[X,Y,dist,aL,L]
        return v

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
            self.v[v]=[X,Y,dist,aL,L]
            return v

        # If we cannot extend the edge, make a new vertex and edge
        # 1 of 1 places where new v are made
        new_name=self._make_v([X,Y,dist,aL,[aL]])

        # 1 of 1 places where new e are made
        self._make_e([v,new_name,aL])

        # Update self.close
        for a in self.close:
            new_dist = Mdist(self.v[v][0:2],self.v[a][0:2])
            if new_dist < self.close[a][-1]:
                self.close[a]=[new_name,new_dist]

        return new_name

    def N(self,v):
        return self.move(v,'N')
    def S(self,v):
        return self.move(v,'S')
    def W(self,v):
        return self.move(v,'W')
    def E(self,v):
        return self.move(v,'E')
