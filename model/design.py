#!/usr/bin/env python3

import sys
sys.path.append("..")

from model import params, net

def scale_congestion(x):
    return math.exp(x)-1

# Basically a 2-dimensional matrix
class design:
    
    # Each square is [{n -> [v]},{L -> c}]
    grid=[[]]
    # Stored just because old code convention
    # calls on the coder to store list sizes
    x_dim=0
    y_dim=0

    # Dictionary of net objects. {name -> net}
    nets={}

    # Only one net "active" at a time
    # Switch action must be taken to switch
    active_net=-1

    # DEF: [(cell_name,cell_type,llx,lly)]
    # stdcells: [(cell_type,(out_pins),(in_pins)]
    # nets: [net_name]
    # netlist: [(cell_name,cell_type,{pin_name -> net_name})]
    def __init__(self,DEF,stdcells,nets,netlist):

        # Define grid itself
        # Each square is [x,y,{n -> [v]},{L -> c}]

        # Grab the dimensions of the grid and initialize it
        round_up = lambda x,y: int(x/y)+(x%y > 0)
        self.x_dim=round_up(params.GX,params.GSQ)
        self.y_dim=round_up(params.GY,params.GSQ)
        self.grid=[[[{},{}] for j in range(self.y_dim)] for i in range(self.x_dim)]

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
            net_obj=net.net(n)
            self.nets[name]=net_obj
            # Populate the grid object's net dict
            for i in range(len(n)):
                x = n[i]
                ret=self.grid[x[0]][x[1]][0].get(name,[])
                ret.append(i)
                self.grid[x[0]][x[1]][0][name]=ret
        # Since we're init-ing, congestion only depends on vertices
        for x in range(self.x_dim):
            for y in range(self.y_dim):
                # Initial pins are on layers 0 and 1
                self.grid[x][y][-1][0]=len(self.grid[x][y][0])
                self.grid[x][y][-1][1]=self.grid[x][y][-1][0]

        # Choose random starting active net for now
        active_net = list(self.nets.keys())[0]

    def get_state():
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
        state=[[]*self.y_dim]*self.x_dim
        for a in self.xdim:
            for b in self.ydim:
                el = self.grid[a][b]
                ndic = el[0]
                ndic_parsed = {}
                el_parsed = []
                # Turn the 1st element of a grid square, {n -> [v]}
                # Into a count of vertices per layer
                for v in ndic.values():
                    for l in v[-1]:
                        ndic_parsed[l]=ndic_parsed.get(l,0)+1
                for i in range(params.MMi+1):
                    el_parsed.append(el[-1][i])
                for i in range(params.MMi+1):
                    el_parsed.append(ndic_parsed[i])
                state[a][b]=el_parsed
        return state

    def do_action(X):
        if X in ['N','S','E','W','up','down']:
            self.active_net.move(X)
            # Need to change grid object
            return
        # Need to implement switch
        pass

    def global_loss(state):
        ret1=0
        ret2=0
        for n in self.nets:
            ret+=n.loss()
        for (x,y) in zip(range(self.xdim),range(self.ydim)):
            for L in range(params.MM):
                ret1+=scale_congestion(state[x][y][L])
        # Average it out. No need, but it does lower the number.
        # Maybe normalizing is good because nets vs congestion.
        ret1 = ret1/len(self.nets)
        ret2 = ret2/self.xdim
        ret2 = ret2/self.ydim

        return ret1+ret2


