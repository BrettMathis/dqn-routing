#!/usr/bin/env python3

import sys,math

from model import params,net
import numpy as np

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
        self.switches=[]
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
            # If the net does not connect to anything:
            if len(n)==1:
                continue
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
        self.switches = self.switching_factor()

    def get_state(self):
        # State will be 3-dimensional matrix
        # One dimension is X
        # One dimension is Y
        # Remaining dimension is Z
        # Z is MM+1 + 1 deep and records:
        # - congestion on each layer (MM total entries)
        # - position of switch vectors (weighted by priority)
        # The latter is not technically needed, but
        # this is a neural network. That information can help it
        # figure out how switching works, since it actually sees
        # the vertices it can switch to.
        state=[[0 for j in range(self.ydim)] for i in range(self.xdim)]
        parsed_switch = [x.split('%') for x in self.switches]
        switch_loc = [self.nets[x[0]].v[int(x[1])][0:2] for x in parsed_switch]
        active_loc = [self.nets[self.active[0]].v[self.active[1]][0:2]]
        for a in range(self.xdim):
            for b in range(self.ydim):
                el = self.grid[a][b]
                el_parsed = []
                for i in range(params.MM+1):
                    el_parsed.append(el[-1].get(i,0))
                el_parsed.append(0)
                state[a][b]=el_parsed
        for x in range(params.SN):
            [a,b]=switch_loc[x]
            state[a][b][-1]=(x+1)**2
        for a,b in active_loc:
            state[a][b][-1]=(params.SN+1)**2
        return state

    def do_action(self,raw_X,translate=True):
        # Convert raw numerical action to action name
        translate_action = {0:'N',1:'S',2:'E',3:'W',4:'up',5:'down'}
        for a in range(params.SN):
            translate_action[6+a]='switch'+str(a)
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

        # Two things we need to do:
        # 1) Update congestion
        # 2) Update grid (which just holds vertex locations)
        # 2 has to be done for both new vertex (2.a) and old vertex (2.b)

            # Move, and store name and contents of new vertex
            new_n,new_v,was_cloned=net_obj.move(active_v,X)

            # 1)
            # Congestion ALWAYS increases
            # in new location
            # ONLY on active Layer
            # unless this move reached a net sink
            if new_n not in net_obj.close:
                tmp=self.grid[new_v[0]][new_v[1]][-1].get(new_v[-2],0)
                tmp+=1
                self.grid[new_v[0]][new_v[1]][-1][new_v[-2]]=tmp
                del tmp


            # 2.a)
            # Update position with new vertex
            tmp=self.grid[new_v[0]][new_v[1]][0].get(active_n,[])
            if new_n not in tmp:
                tmp.append(new_n)
            self.grid[new_v[0]][new_v[1]][0][active_n]=tmp
            del tmp

            # 2.b)
            # If we haven't fully routed a wire with this move
            if not (new_n in net_obj.close and net_obj.done[new_n]):
                # If the vertex moved, modify the old vertex
                if (not was_cloned) and (new_v[0]!=old_v[0] or new_v[1]!=old_v[1]):
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

            # If the net is completely routed (all wires)
            # We have to trim
            # TO-DO: TRIM VIAS
            if net_obj.all_done:
#                print('ALL DONE\n')
#                if net_obj.v[0][0:2]==[0,0]:
#                    assert net_obj.v[1][0:2]==[5,5]
#                if net_obj.v[0][0:2]==[5,5]:
#                    assert net_obj.v[1][0:2]==[3,3]
#                if net_obj.v[0][0:2]==[3,3]:
#                    assert net_obj.v[1][0:2]==[0,0]
#                    assert net_obj.v[2][0:2]==[5,5]
#                print('ALL DONE\n')
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
                    [x,y,_,_,Lv]=net_obj.v[v]
                    [v1,v2,coords,Le]=net_obj.edict[v]
                    # Delete references to vertices in grid
                    tmp=self.grid[x][y][0][active_n]
                    tmp.remove(v)
                    self.grid[x][y][0][active_n]=tmp
                    # Delete congestion due to vertices
                    for l in Lv:
                        self.grid[x][y][-1][l]-=1
                    # Delete congestion due to edges
                    for (a,b) in coords[1:-1]:
                        if (a,b)!=(x,y):
                            self.grid[a][b][-1][Le]-=1
                    # Delete vertices
                    del net_obj.v[v]
                    # Delete edges
                    del net_obj.edict[v]

            # Switch active to new vertex
            self.active=[active_n,new_n]

            # Is this good? Is this bad? Unsure
            # But I'll put it in anyway
            # If the net is completely routed
            # JUMP
            if net_obj.all_done:
                self.switches = self.switching_factor()
                self.do_action(6)
                return
        
        # Switch action
        if "switch" in X:
            dest = int(X.replace("switch",""))
            switch = self.switches[dest]
            self.active=switch.split('%')
            self.active[1]=int(self.active[1])
            self.switches = self.switching_factor()

    def scale_congestion(self,state,x,y,L):
        cong=state[x][y][L]
        #ret=math.exp(cong/params.MT[L])-1
        ret=params.CF(cong/params.MT[L])
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
                key=n_name+'%'+str(v_name)
                key_coords=v[:2]
                ret[key]=n.loss()/max([net.Mdist(v_coords,key_coords),1])
        if ret=={}:
            retl=[active_n+'%'+str(active_v)]*params.SN
            self.no_switch=True
        else:
            retl = [k for k,v in sorted(ret.items(),key=lambda x: x[1])]
        if len(retl)<params.SN:
            retl = retl*params.SN
        retl = retl[:params.SN]
        return retl

    def done(self):
        if (self.no_switch and self.nets[self.active[0]].all_done):
            print("\n\nALL DONE\n\n")
        return self.no_switch and self.nets[self.active[0]].all_done

    def visualize(self):
        state=self.get_state()
        ret=np.zeros((params.MM+1+1,self.ydim,self.xdim)).tolist()
        for x in range(self.xdim):
            for y in range(self.ydim):
                for z in range(params.MM+1+1):
                    ret[z][y][x]=state[x][y][z]
        return ret
