#!/usr/bin/env python3

import sys
sys.path.append("..")

from model import params, net

# Basically a 2-dimensional matrix
class design:
    
    # Each square is [x,y,{n -> [v]},{L -> c}]
    grid=[[]]
    # Stored just because old code convention
    # calls on the coder to store list sizes
    x_dim=0
    y_dim=0

    # List of net objects
    nets=[]

    # Only one net "active" at a time
    # Switch action must be taken to switch
    active_net=-1

    # DEF: [(cell_name,cell_type,llx,lly)]
    # stdcells: [(cell_type,(out_pins),(in_pins)]
    # nets: [net_name]
    # netlist: [(cell_name,cell_type,{pin_name -> net_name})]
    def __init__(DEF,stdcells,nets,netlist):

        # Define grid itself
        # Each square is [x,y,{n -> [v]},{L -> c}]
        empty_sq = [-1,-1,{},{}]
        round_up = lambda x,y: int(x/y)+(x%y > 0)
        self.x_dim=round_up(params.GX,params.GSQ)
        self.y_dim=round_up(params.GY,params.GSQ)
        grid=[empty_sq*self.y_dim]*self.x_dim

        std_cell_dic = {a:{'out_pins':b,'in_pins':c} for a,b,c in stdcells}
        cell_dic = {a:{'type':b,'x/y':(x,y)} for a,b,x,y in DEF}
        net_dic = {a:[] for a in nets}
        for a in netlist:
            (cell_name,cell_type,pin_dic)=a
            (x,y)=cell_dic[cell_name]['x/y']
            for pin_name,net_name in a[-1].items():
                pin_dir=-1
                if pin_name in std_cells[cell_name]['out_pins']:
                    pin_dir=1
                    net_dic[net_name]=[x,y]+net_dic[net_name]
                if pin_name in std_cells[cell_name]['in_pins']:
                    pin_dir=0
                    net_dic[net_name]=net_dic[net_name]+[x,y]
                if pin_dir==-1:
                    print("Pin with undefined direction: "+cell_name+" "+pin_name)
        
        for n in net_dic.values():
            self.net.append(net.net(n))

        # Choose random starting active net for now
        active_net = self.net[0]

        # Still need to actually store info in the grid object


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
                ndic = el[2]
                ndic_parsed = {}
                el_parsed = []
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
                ret1+=state[x][y][L]
        # Average it out. No need, but it does lower the number.
        # Maybe normalizing is good because nets vs congestion.
        ret1 = ret1/len(self.nets)
        ret2 = ret2/self.xdim
        ret2 = ret2/self.ydim

        return ret1+ret2


