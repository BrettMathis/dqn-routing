import sys
sys.path.append("..")

from model import params


##
##A few rules to ensure the design has at least a few local optima in 
##paths to route with:
##
##1.) No vertex in the grid occupied by a gate can have a neighboring
##	 entry that is also a gate
##
##2.) The archiecture will be layed out as parallel as possible. Just because
##	 it can fit within a grid space of two rows, even with alternating gates, 
##	 does not mean this will properly train the model. This will ensure there
##	 are at least a few parallel groups for the algorithm to route with even for
##	 low radix.
##
##3.) Just to make things readable, each row will be a logical gate level,
##	 as opposed to column-wise layout.
##
##4.) Only gate data will be maintained for the grid structure. The routing 
##	 algorithm can check if a cell is occupied by a gate and choose how many 
##	 metal layers to limit accordingly. If a need arises to keep track of all
##	 edges in a list, please use a separate data structure.
##

#creatign a gate class to represent each gate-occupied vertex

#This has support for taking the data from innovus
#Reformatted from previous iterations
class gate:

	#bookkeeping for each gate

	#these are the IO connections for each gate cell
	#If they're connected in the design
	##Each dictionary value is index by its
	##connected wire (ALA Innovus A:WIRE1)	

	def __init__(self):
		#For example, input A on an and gate would be
		#inputs={"A" : "WIRE1"}
		self.inputs={};
		self.outputs={};
		
		#this is the type of gate used
		self.name={"name" : None};
	
		#invalid gate number as inital
		#equivalent to innovus cell number
		self.gate_num = -1;
	
		#invalid position on grid as initial values
		#we're using integer values for our grid, so
		#innovus values will have to be normalized
		#to integers or spaced out for now
		self.position = [-1.0,-1.0];
	
	def set_position(self, x, y):
		self.position = [x,y];
	
	def get_position(self):
		return self.position;
	
	def set_number(self, num):
		self.gate_num = num;
	
	def get_number(self):
		return self.gate_num;
	
	def set_name(self, name):
		self.name.clear();
		self.name.update({"name" : name});
	
	def get_name(self):
		return self.name;
	
	#wire can be None for no connection
	def add_input(self, name, wire):
		self.inputs.update({name : wire});
	
	#wire can be None for no connection
	def add_output(self, name, wire):
		self.outputs.update({name : wire});
	
	def delete_input(self, name):
		self.inputs.pop(name);
	
	def delete_output(self, name):
		self.outputs.pop(name);
	
	def clear_input(self):
		self.inputs.clear();
	
	def clear_output(self):
		self.outputs.clear();
	
	def get_info(self):
		print("Invididualized gate info for gate " + str(self.gate_num) + " of name/type " + str(self.name["name"]) + ":");
		print("Position X: " + str(self.position[0]) + " Position Y: " + str(self.position[1]));
		print("Input list: " + str(self.inputs));
		print("Output list: " + str(self.outputs));

def compile_design(reference):


    DEF=[]
    stdcells=[]
    nets=[]
    netlist=[]

    stdcells.append(["INV",["Y"],["A"]])
    stdcells.append(["BUF",["Y"],["A"]])
    stdcells.append(["AND",["Y"],["A","B"]])
    stdcells.append(["OR",["Y"],["A","B"]])
    stdcells.append(["XOR",["Y"],["A","B"]])

    design_x = len(reference);
    design_y = len(reference[0]);

    for i in range(design_x):

        for j in range(design_y):

            cell = reference[i][j];

            if(cell != None):
                temp_list = [];
                for key in reference[i][j].get_name() : temp_list.append(reference[i][j].get_name()[key]);
                name = temp_list;
                temp_list = [];
                #print(name);

                [cell_x, cell_y] = reference[i][j].get_position();
                #print(str(cell_x), ' , ' + str(cell_y));

                for key in reference[i][j].inputs : temp_list.append(key);
                inputs = temp_list;
                temp_list = [];
                #print(inputs);

                for key in reference[i][j].outputs : temp_list.append(key);
                outputs = temp_list;
                temp_list = [];
                #print(outputs);

                stdcell_list = [];
                cell_type = None;
                for k in range(len(stdcells)):

                    stdcell_list.append(stdcells[k][0]);
                
                for k in range(len(stdcell_list)):

                    if stdcell_list[k] in name[0]:
                        cell_type = stdcell_list[k];

                #print(cell_type);
                #DEF
                DEF.append([name[0], cell_type, cell_x, cell_y]);

                #nets
                for k in range(len(inputs)):
                    if inputs[k] in nets:
                        pass
                    else:
                        nets.append(inputs[k]);

                for k in range(len(outputs)):
                    if outputs[k] in nets:
                        pass
                    else:
                        nets.append(outputs[k]);

                #netlist
                cell_inputs = []; 
                cell_outputs = [];
                cell_dict = {};
                for k in range(len(stdcells)):

                    if(cell_type == stdcells[k][0]):
                        
                        cell_inputs = stdcells[k][2];
                        cell_outputs = stdcells[k][1];

                for k in range(len(cell_inputs)):

                    cell_dict.update({cell_inputs[k]:inputs[k]});

                for k in range(len(cell_outputs)):

                    cell_dict.update({cell_outputs[k]:outputs[k]});

                netlist.append([name[0], cell_type, cell_dict]);

    return DEF, stdcells, nets, netlist;


