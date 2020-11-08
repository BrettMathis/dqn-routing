#!/usr/bin/env python3

import sys,math

from model import params,net

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
        self.no_switch=False

        # Define grid itself
        # Each square is [x,y,{n -> [v]},{L -> c}]

        # Grab the dimensions of the grid and initialize it
        round_up = lambda x,y: int(x/y)+(x%y > 0)
        self.xdim=round_up(params.GX+1,params.GSQ)
        self.ydim=round_up(params.GY+1,params.GSQ)
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

    def do_action(self,raw_X,translate=True):
        # Convert raw numerical action to action name
        translate_action = {0:'N',1:'S',2:'E',3:'W'}
        for a in range(params.SN):
            translate_action[4+a]='switch'+str(a)
        if translate:
            X=translate_action[raw_X]
        else:
            X=raw_X

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
            # unless this move reached a net sink
            if new_n not in net_obj.close:
                tmp=self.grid[new_v[0]][new_v[1]][-1].get(new_v[-2],0)
                tmp+=1
                self.grid[new_v[0]][new_v[1]][-1][new_v[-2]]=tmp
                del tmp

            # Update new position with vertex, if vertex moved
            tmp=self.grid[new_v[0]][new_v[1]][0].get(active_n,[])
            if new_n not in tmp:
                tmp.append(new_n)
            self.grid[new_v[0]][new_v[1]][0][active_n]=tmp
            del tmp

            if not (new_n in net_obj.close and net_obj.done[new_n]):
                # If the vertex moved, modify the old vertex
                if len(old_v[-1])==1 and X not in ['up','down']:
                    tmp=self.grid[old_v[0]][old_v[1]][0][active_n]
                    tmp.remove(old_n)
                    self.grid[old_v[0]][old_v[1]][0][active_n]=tmp
            # If we've fully routed a wire with this move
            else:
                # Delete the old vertex
                del net_obj.v[old_n]
                # Delete reference to the old vertex from the grid
                [x,y]=old_v[:2]
                tmp=self.grid[x][y][0][active_n]
                tmp.remove(old_n)
                self.grid[x][y][0][active_n]=tmp

            # If the net is completely routed, we have to trim
            if net_obj.all_done:
                # Figure out which vertices are not superfluous
                vital=[]
                # Recurse backwards from sink port
                def _trim(v):
                    vital.append(v)
                    if v not in net_obj.edict:
                        return
                    return _trim(net_obj.edict[v][0])
                # For each sink port
                for v in net_obj.done:
                    _trim(v)

                # All vertices which did not get flagged by recursion
                # should be removed
                bad = [v for v in net_obj.v if v not in vital]

                for v in bad:
                    [x,y,_,_,L]=net_obj.v[v]
                    # Delete vertices
                    del net_obj.v[v]
                    # Delete references to vertices in grid
                    tmp=self.grid[x][y][0][active_n]
                    tmp.remove(v)
                    self.grid[x][y][0][active_n]=tmp
                    # Delete congestion due to vertices
                    for l in L:
                        self.grid[x][y][-1][l]-=1
                    # Delete edges
                    [v1,v2,coords,L]=net_obj.edict[v]
                    del net_obj.edict[v]
                    # Delete congestion due to edges
                    for (a,b) in coords[1:-1]:
                        if (a,b)!=(x,y):
                            self.grid[a][b][-1][L]-=1
            # Switch active to new vertex
            self.active=[active_n,new_n]
        
        # Switch action
        if "switch" in X:
            dest = int(X.replace("switch",""))
            switches = self.switching_factor()
            switch = switches[dest]
            self.active=switch.split('_')
            self.active[1]=int(self.active[1])

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
        return -1*(ret1+ret2)

    def switching_factor(self):
        ret={}
        [active_n,active_v] = self.active
        v_coords = self.nets[active_n].v[active_v][:2]
        cur_key=''
        for n_name,n in self.nets.items():
            if n.all_done:
                continue
            for v_name,v in n.v.items():
                if v_name in n.close:
                    continue
                if active_n==n_name and active_v==v_name:
                    continue
                key=n_name+"_"+str(v_name)
                key_coords=v[:2]
                ret[key]=n.loss()/max([net.Mdist(v_coords,key_coords),1])
        if ret=={}:
            retl=[active_n+"_"+str(active_v)]*params.SN
            self.no_switch=True
        else:
            retl = [k for k,v in sorted(ret.items(),key=lambda x: x[1])]
        if len(retl)<params.SN:
            retl = retl*params.SN
        retl = retl[:params.SN]
        return retl

    def done(self):
        return self.no_switch and self.nets[self.active[0]].all_done
