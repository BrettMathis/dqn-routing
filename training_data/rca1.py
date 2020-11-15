import sys
import math
sys.path.append("..")

from model import params
from training_data.gates import *

#RCA datapath is literally just 8 full adders in series
def make_rca1(y_max):

	#This is a demo for the default gate if you want to see it
	#test_gate = gate();
	#test_gate.get_info();
	
	##
	##NO EDGES WILL BE INITIALIZED TO ENSURE ROUTING ALGORITHM
	##HAS NO STARING INFORMATION 
	##
	##IO PORT NAMES WILL BE KEPT IDENTICAL
	##
	##For example:
	##
	## XOR1 will return for output - {"XOR1_OUT" : None}
	## but the XOR2 gate it connects to will return - {"XOR1_OUT" : None, "CIN" : None}
	## for input.
	##
	
	##set global params to: X = 50, Y = 8 for condensed grid space
	
	grid_y = 100*y_max;
	grid_x = 100*y_max;
	
	#creating a grid data structure with the dimsions specified in params
	#not using a dictionary because order is important for routing - fight me
	rca1 = [[None for i in range(grid_y)] for i in range(grid_x)];
	
	#bookkeeping
	gate_number = 1;
	max_y = y_max;
	current_y = 0;
	current_x = 0;
	
	#Making the first of 8 sequantial full adders - requires 2 XOR's, 3 AND's and 2 OR's
	
	'''FULL ADDER 0'''
	
	#######################################################
	#######################################################
	#Sum0##################################################
	XOR1 = gate();
	XOR1.set_name("XOR1");
	XOR1.set_number(gate_number);
	XOR1.set_position(current_x,current_y);
	XOR1.add_input("A0", None);
	XOR1.add_input("B0", None);
	XOR1.add_output("XOR1_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = XOR1.get_position();
	rca1[temppos[0]][temppos[1]] = XOR1;
	#
	#######################################################
	#
	XOR2 = gate();
	XOR2.set_name("XOR2");
	XOR2.set_number(gate_number);
	XOR2.set_position(current_x,current_y);
	XOR2.add_input("CIN", None);
	XOR2.add_input("XOR1_OUT", None);
	XOR2.add_output("SUM0", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = XOR2.get_position();
	rca1[temppos[0]][temppos[1]] = XOR2;
	#
	#######################################################
	#######################################################
	#C0####################################################
	AND1 = gate();
	AND1.set_name("AND1");
	AND1.set_number(gate_number);
	AND1.set_position(current_x,current_y);
	AND1.add_input("A0", None);
	AND1.add_input("B0", None);
	AND1.add_output("AND1_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND1.get_position();
	rca1[temppos[0]][temppos[1]] = AND1;
	#
	#######################################################
	#
	AND2 = gate();
	AND2.set_name("AND2");
	AND2.set_number(gate_number);
	AND2.set_position(current_x,current_y);
	AND2.add_input("B0", None);
	AND2.add_input("CIN", None);
	AND2.add_output("AND2_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND2.get_position();
	rca1[temppos[0]][temppos[1]] = AND2;
	#
	#######################################################
	#
	AND3 = gate();
	AND3.set_name("AND3");
	AND3.set_number(gate_number);
	AND3.set_position(current_x,current_y);
	AND3.add_input("CIN", None);
	AND3.add_input("A0", None);
	AND3.add_output("AND3_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND3.get_position();
	rca1[temppos[0]][temppos[1]] = AND3;
	#
	#######################################################
	#
	OR1 = gate();
	OR1.set_name("OR1");
	OR1.set_number(gate_number);
	OR1.set_position(current_x,current_y);
	OR1.add_input("AND1_OUT", None);
	OR1.add_input("AND2_OUT", None);
	OR1.add_output("OR1_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = OR1.get_position();
	rca1[temppos[0]][temppos[1]] = OR1;
	#
	#######################################################
	#
	OR2 = gate();
	OR2.set_name("OR2");
	OR2.set_number(gate_number);
	OR2.set_position(current_x,current_y);
	OR2.add_input("OR1_OUT", None);
	OR2.add_input("AND3_OUT", None);
	OR2.add_output("C0", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
	#Done with FA, update row
	current_x = current_x + 1;
	temppos = OR2.get_position();
	rca1[temppos[0]][temppos[1]] = OR2;
	#######################################################
	#######################################################
	
	'''print("RCA placed cell grid: ");
	print(rca1);
	#get placed gate count - sanity checking grid for duplicates and misplaced gates
	#there could still be typos - just fyi
	placed_count = 0;
	duplicate_gate_count = 0;
	for i in range(len(rca1)):
	
		for j in range(len(rca1[i])):
		
			if(rca1[i][j] != None):
				placed_count = placed_count + 1;
				##UNCOMMENT FOR GATE INFO
				#rca1[i][j].get_info();
				
			#Performing list check for inputs and outputs
			
			for k in range(len(rca1)):
			
				for l in range(len(rca1[k])):
				
					if(rca1[i][j] != None and rca1[k][l] != None and (i != k and j != l)):
							gate1_in = str(rca1[i][j].inputs);
							gate2_in = str(rca1[k][l].inputs);
							
							gate1_out = str(rca1[i][j].outputs);
							gate2_out = str(rca1[k][l].outputs);
							
							if(gate1_in == gate2_in and gate1_out == gate2_out):
								rca1[i][j].get_info();
								duplicate_gate_count = duplicate_gate_count + 1;
	
	print("Number of gates placed: ");
	print(placed_count);
	print("Rought estimate of duplicates (based on IO names) :");
	print(duplicate_gate_count/2);
	print("Duplicate strings found during search: ");
	print(duplicate_gate_count);
	if(duplicate_gate_count == 0):
		print("no duplicates found! :DDDDDD");
	else:
		print("duplicates found :'(");'''
	return rca1;

#I like having a main method because I'm particular like that.
#Also you scrolled down this far. Good on you.
def main():

	circuit_design = make_rca1(10);
	
main();	
