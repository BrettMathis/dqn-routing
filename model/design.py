#!/usr/bin/env python3

import sys,math

from model import params, net

# Basically a 2-dimensional matrix
class design:
    
    # Each square is [{n -> [v]},{L -> c}]
##    grid=[[]]
    # Stored just because old code convention
    # calls on the coder to store list sizes
##    xdim=0
##    ydim=0

    # Dictionary of net objects. {name -> net}
##    nets={}

    # Only one vertex "active" at a time
    # Switch action must be taken to switch
##    active=[0,0]

    # DEF: [(cell_name,cell_type,llx,lly)]
    # stdcells: [(cell_type,(out_pins),(in_pins)]
    # nets: [net_name]
    # netlist: [(cell_name,cell_type,{pin_name -> net_name})]
    def __init__(self,DEF,stdcells,nets,netlist):

        self.grid=[[]]
        self.xdim=0
        self.ydim=0
        self.nets={}
        self.active=[0,0]

        # Define grid itself
        # Each square is [x,y,{n -> [v]},{L -> c}]

        # Grab the dimensions of the grid and initialize it
        round_up = lambda x,y: int(x/y)+(x%y > 0)
        self.xdim=round_up(params.GX,params.GSQ)
        self.ydim=round_up(params.GY,params.GSQ)
        self.grid=[[[{},{}] for j in range(self.ydim)] for i in range(self.xdim)]

        # Parse the inputs
        std_cell_dic = {a:{'out_pins':b,'in_pins':c} for a,b,c in stdcells}
        cell_dic = {a:{'type':b,'x/y':(x,y)} for a,b,x,y in DEF}
        net_dic = {a:[] for a in nets}

        # Get ready to create the net data structures
        for a in netlist:
            (cell_name,cell_type,pin_dic)=a
            (x,y)=cell_dic[cell_name]['x/y']
        
            # Go through all pins in the netlist
            # Assign each to a net
            # This needs to be done backwards like this because
            # the netlist is organized by cell, not by net
            for pin_name,net_name in a[-1].items():

                # Check for input/output so we can init the net data structure
                pin_dir=-1
                if pin_name in std_cell_dic[cell_type]['out_pins']:
                    pin_dir=1
                    net_dic[net_name]=[[x,y]]+net_dic[net_name]
                if pin_name in std_cell_dic[cell_type]['in_pins']:
                    pin_dir=0
                    net_dic[net_name]=net_dic[net_name]+[[x,y]]

                # Raise exception if one of the pins doesn't match the std cell
                if pin_dir==-1:
                    raise ValueError("Pin with undefined direction: "+cell_name+" "+pin_name)
        
        # Iterate through net_dic
        for name,n in net_dic.items():
            # Create net objects
            self.nets[name]=net.net(n)
            # Populate the grid object's net dict
            for i in range(len(n)):
                x = n[i]
                ret=self.grid[x[0]][x[1]][0].get(name,[])
                ret.append(i)
                self.grid[x[0]][x[1]][0][name]=ret
        # Since we're init-ing, congestion only depends on vertices
        for x in range(self.xdim):
            for y in range(self.ydim):
                # Initial pins are on layers 0 and 1
                self.grid[x][y][-1][0]=len(self.grid[x][y][0])
                self.grid[x][y][-1][1]=self.grid[x][y][-1][0]

        # Choose random starting active net for now
        active_net = list(self.nets.keys())[0]
        n_temp = self.nets[active_net]
        v_temp = 0
        self.active = [active_net,v_temp]

    def get_state(self):
        # State will be 3-dimensional matrix
        # One dimension is X
        # One dimension is Y
        # Remaining dimension is "depth"
        # "depth" is 2 * MM deep and records:
        # - congestion on each layer (MM total entries)
        # - number of vertices on each layer (MM total entries)
        # The latter is not technically needed, but
        # this is a neural network. That information can help it
        # figure out how switching works, since it actually sees
        # the vertices it can switch to.
        state=[[0 for j in range(self.ydim)] for i in range(self.xdim)]
        for a in range(self.xdim):
            for b in range(self.ydim):
                el = self.grid[a][b]
                ndic = el[0]
                ndic_parsed = {}
                el_parsed = []
                # Turn the 1st element of a grid square, {n -> [v]}
                # Into a count of vertices per layer
                for n,v in ndic.items():
                    net_obj = self.nets[n]
                    vertices = [net_obj.v[x] for x in v]
                    for l in [x[-1] for x in vertices]:
                        for k in l:
                            ndic_parsed[k]=ndic_parsed.get(k,0)+1
                for i in range(params.MM+1):
                    el_parsed.append(el[-1].get(i,0))
                for i in range(params.MM+1):
                    el_parsed.append(ndic_parsed.get(i,0))
                state[a][b]=el_parsed
        return state

    def do_action(self,X):
        # Get names of active net and vertex
        [active_n,active_v] = self.active
        # Get actual net object
        net_obj = self.nets[active_n]
        # Store name and contents of old vertex
        old_n,old_v = (active_v,net_obj.v[active_v])

        # Act only if action is valid
        # Otherwise nothing happens
        # We don't stop the NN from choosing invalid actions?
        # We just ignore and do nothing?
        # I guess the NN can just shout into the void if it feels the need
        # I know routing can be pretty frustrating.
        if X in net_obj.valid_actions(active_v):
            # Move, and store name and contents of new vertex
            new_n,new_v=net_obj.move(active_v,X)

            # Congestion ALWAYS increases
            # in new location
            # ONLY on active Layer
            self.grid[new_v[0]][new_v[1]][-1][new_v[-2]]+=1

            # Update new position with vertex, if vertex moved
            tmp=self.grid[new_v[0]][new_v[1]][0].get(active_n,[])
            if new_n not in tmp:
                tmp.append(new_n)
            self.grid[new_v[0]][new_v[1]][0][active_n]=tmp
            del tmp

            # If the vertex moved, modify the old vertex
            if len(old_v[-1])==1:
                tmp=self.grid[old_v[0]][old_v[1]][0][active_n]
                tmp.remove(old_n)
                self.grid[old_v[0]][old_v[1]][0][active_n]=tmp

            # Switch active to new vertex
            self.active=[active_n,new_n]
        # Need to implement switch
        pass

    def scale_congestion(self,state,x,y,L):
        cong=state[x][y][L]
        ret=math.exp(cong/params.MT[L])-1
        return ret

    def global_loss(self,state):
        ret1=0
        ret2=0
        for n in self.nets.values():
            ret1+=n.loss()
        for x in range(self.xdim):
            for y in range(self.ydim):
                for L in range(1,params.MM):
                    ret2+=self.scale_congestion(state,x,y,L)
        # Average it out. No need, but it does lower the number.
        # Maybe normalizing is good because nets vs congestion.
        ret1 = ret1/len(self.nets)
#        ret2 = ret2/self.xdim
#        ret2 = ret2/self.ydim
        return ret1+ret2

    def switching_factor(self):
        ret={}
        [active_n,active_v] = self.active
        v_coords = self.nets[active_n].v[active_v][:2]
        for n_name,n in self.nets.items():
            for v_name,v in n.v.items():
                if v_name in n.close:
                    continue
                if active_n==n_name and active_v==v_name:
                    continue
                key=n_name+"_"+str(v_name)
                key_coords=v[:2]
                ret[key]=n.loss()/max([net.Mdist(v_coords,key_coords),1])
        return ret

