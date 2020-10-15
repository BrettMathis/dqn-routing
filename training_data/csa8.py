import sys
import math
sys.path.append("..")

from model import params
from gates import *


#This will be a 4:2 CSA datapath. This means we're gonna have two rows of paralel FA's
#The second row connects to the output of the first - offset by one bit
#Basically the opposite of an RCA layout - super parallel and fast
#Note: the output will be in carry-save format - not conventional binary

def make_csa8():

	#This is a demo for the default gate if you want to see it
	#test_gate = gate();
	#test_gate.get_info();
	
	##
	##NO EDGES WILL BE INITIALIZED TO ENSURE ROUTING ALGORITHM
	##HAS NO STARING INFORMATION 
	##
	##IO PORT NAMES WILL BE KEPT IDENTICAL
	##
	##For example (RCA):
	##
	## XOR1 will return for output - {"XOR1_OUT" : None}
	## but the XOR2 gate it connects to will return - {"XOR1_OUT" : None, "CIN" : None}
	## for input.
	##
	
	##set global params to: X = 50, Y = 16 for condensed (and more parallel) grid space
	
	grid_y = 16;
	grid_x = 40;
	
	#creating a grid data structure with the dimsions specified in params
	#not using a dictionary because order is important for routing - fight me
	csa8 = [[None for i in range(grid_y)] for i in range(grid_x)];
	
	#bookkeeping
	gate_number = 1;
	max_y = 6;
	current_y = 0;
	current_x = 0;
	
	##
	##THIS IS THE FIRST LAYER OF FULL ADDERS 
	##
	
	'''FULL ADDER 0'''
	
	#######################################################
	#######################################################
	#SUMLAYER1_0##################################################
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
	csa8[temppos[0]][temppos[1]] = XOR1;
	#
	#######################################################
	#
	XOR2 = gate();
	XOR2.set_name("XOR2");
	XOR2.set_number(gate_number);
	XOR2.set_position(current_x,current_y);
	XOR2.add_input("CA0", None);
	XOR2.add_input("XOR1_OUT", None);
	XOR2.add_output("SUMLAYER1_0", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = XOR2.get_position();
	csa8[temppos[0]][temppos[1]] = XOR2;
	#
	#######################################################
	#######################################################
	#CLAYER1_1####################################################
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
	csa8[temppos[0]][temppos[1]] = AND1;
	#
	#######################################################
	#
	AND2 = gate();
	AND2.set_name("AND2");
	AND2.set_number(gate_number);
	AND2.set_position(current_x,current_y);
	AND2.add_input("B0", None);
	AND2.add_input("CA0", None);
	AND2.add_output("AND2_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND2.get_position();
	csa8[temppos[0]][temppos[1]] = AND2;
	#
	#######################################################
	#
	AND3 = gate();
	AND3.set_name("AND3");
	AND3.set_number(gate_number);
	AND3.set_position(current_x,current_y);
	AND3.add_input("CA0", None);
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
	csa8[temppos[0]][temppos[1]] = AND3;
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
	csa8[temppos[0]][temppos[1]] = OR1;
	#
	#######################################################
	#
	OR2 = gate();
	OR2.set_name("OR2");
	OR2.set_number(gate_number);
	OR2.set_position(current_x,current_y);
	OR2.add_input("OR1_OUT", None);
	OR2.add_input("AND3_OUT", None);
	OR2.add_output("CLAYER1_1", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
	#Done with FA, update row
	current_x = current_x + 1;
	temppos = OR2.get_position();
	csa8[temppos[0]][temppos[1]] = OR2;
	#######################################################
	#######################################################
	
	'''FULL ADDER 1'''
	
	
	#######################################################
	#######################################################
	#SUMLAYER1_1##################################################
	XOR3 = gate();
	XOR3.set_name("XOR3");
	XOR3.set_number(gate_number);
	XOR3.set_position(current_x,current_y);
	XOR3.add_input("A1", None);
	XOR3.add_input("B1", None);
	XOR3.add_output("XOR3_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = XOR3.get_position();
	csa8[temppos[0]][temppos[1]] = XOR3;
	#
	#######################################################
	#
	XOR4 = gate();
	XOR4.set_name("XOR4");
	XOR4.set_number(gate_number);
	XOR4.set_position(current_x,current_y);
	XOR4.add_input("CA1", None);
	XOR4.add_input("XOR3_OUT", None);
	XOR4.add_output("SUMLAYER1_1", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = XOR4.get_position();
	csa8[temppos[0]][temppos[1]] = XOR4;
	#
	#######################################################
	#######################################################
	#CLAYER1_2####################################################
	AND4 = gate();
	AND4.set_name("AND4");
	AND4.set_number(gate_number);
	AND4.set_position(current_x,current_y);
	AND4.add_input("A1", None);
	AND4.add_input("B1", None);
	AND4.add_output("AND4_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND4.get_position();
	csa8[temppos[0]][temppos[1]] = AND4;
	#
	#######################################################
	#
	AND5 = gate();
	AND5.set_name("AND5");
	AND5.set_number(gate_number);
	AND5.set_position(current_x,current_y);
	AND5.add_input("B1", None);
	AND5.add_input("CA1", None);
	AND5.add_output("AND5_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND5.get_position();
	csa8[temppos[0]][temppos[1]] = AND5;
	#
	#######################################################
	#
	AND6 = gate();
	AND6.set_name("AND6");
	AND6.set_number(gate_number);
	AND6.set_position(current_x,current_y);
	AND6.add_input("CA1", None);
	AND6.add_input("A1", None);
	AND6.add_output("AND6_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND6.get_position();
	csa8[temppos[0]][temppos[1]] = AND6;
	#
	#######################################################
	#
	OR3 = gate();
	OR3.set_name("OR3");
	OR3.set_number(gate_number);
	OR3.set_position(current_x,current_y);
	OR3.add_input("AND4_OUT", None);
	OR3.add_input("AND5_OUT", None);
	OR3.add_output("OR3_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = OR3.get_position();
	csa8[temppos[0]][temppos[1]] = OR3;
	#
	#######################################################
	#
	OR4 = gate();
	OR4.set_name("OR4");
	OR4.set_number(gate_number);
	OR4.set_position(current_x,current_y);
	OR4.add_input("OR3_OUT", None);
	OR4.add_input("AND6_OUT", None);
	OR4.add_output("CLAYER1_2", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
	#Done with FA, update row
	current_x = current_x + 1;
	temppos = OR4.get_position();
	csa8[temppos[0]][temppos[1]] = OR4;
	#######################################################
	#######################################################
	
	'''FULL ADDER 2'''
	
	
	#######################################################
	#######################################################
	#SUMLAYER1_2##################################################
	XOR5 = gate();
	XOR5.set_name("XOR5");
	XOR5.set_number(gate_number);
	XOR5.set_position(current_x,current_y);
	XOR5.add_input("A2", None);
	XOR5.add_input("B2", None);
	XOR5.add_output("XOR5_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = XOR5.get_position();
	csa8[temppos[0]][temppos[1]] = XOR5;
	#
	#######################################################
	#
	XOR6 = gate();
	XOR6.set_name("XOR6");
	XOR6.set_number(gate_number);
	XOR6.set_position(current_x,current_y);
	XOR6.add_input("CA2", None);
	XOR6.add_input("XOR5_OUT", None);
	XOR6.add_output("SUMLAYER1_2", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = XOR6.get_position();
	csa8[temppos[0]][temppos[1]] = XOR6;
	#
	#######################################################
	#######################################################
	#CLAYER1_3####################################################
	AND7 = gate();
	AND7.set_name("AND7");
	AND7.set_number(gate_number);
	AND7.set_position(current_x,current_y);
	AND7.add_input("A2", None);
	AND7.add_input("B2", None);
	AND7.add_output("AND7_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND7.get_position();
	csa8[temppos[0]][temppos[1]] = AND7;
	#
	#######################################################
	#
	AND8 = gate();
	AND8.set_name("AND8");
	AND8.set_number(gate_number);
	AND8.set_position(current_x,current_y);
	AND8.add_input("B2", None);
	AND8.add_input("CA2", None);
	AND8.add_output("AND8_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND8.get_position();
	csa8[temppos[0]][temppos[1]] = AND8;
	#
	#######################################################
	#
	AND9 = gate();
	AND9.set_name("AND9");
	AND9.set_number(gate_number);
	AND9.set_position(current_x,current_y);
	AND9.add_input("CA2", None);
	AND9.add_input("A2", None);
	AND9.add_output("AND9_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND9.get_position();
	csa8[temppos[0]][temppos[1]] = AND9;
	#
	#######################################################
	#
	OR5 = gate();
	OR5.set_name("OR5");
	OR5.set_number(gate_number);
	OR5.set_position(current_x,current_y);
	OR5.add_input("AND7_OUT", None);
	OR5.add_input("AND8_OUT", None);
	OR5.add_output("OR5_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = OR5.get_position();
	csa8[temppos[0]][temppos[1]] = OR5;
	#
	#######################################################
	#
	OR6 = gate();
	OR6.set_name("OR6");
	OR6.set_number(gate_number);
	OR6.set_position(current_x,current_y);
	OR6.add_input("OR5_OUT", None);
	OR6.add_input("AND9_OUT", None);
	OR6.add_output("CLAYER1_3", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
	#Done with FA, update row
	current_x = current_x + 1;
	temppos = OR6.get_position();
	csa8[temppos[0]][temppos[1]] = OR6;
	#######################################################
	#######################################################
	
	'''FULL ADDER 3'''
	
	
	#######################################################
	#######################################################
	#SUMLAYER1_3##################################################
	XOR7 = gate();
	XOR7.set_name("XOR7");
	XOR7.set_number(gate_number);
	XOR7.set_position(current_x,current_y);
	XOR7.add_input("A3", None);
	XOR7.add_input("B3", None);
	XOR7.add_output("XOR7_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = XOR7.get_position();
	csa8[temppos[0]][temppos[1]] = XOR7;
	#
	#######################################################
	#
	XOR8 = gate();
	XOR8.set_name("XOR8");
	XOR8.set_number(gate_number);
	XOR8.set_position(current_x,current_y);
	XOR8.add_input("CA3", None);
	XOR8.add_input("XOR8_OUT", None);
	XOR8.add_output("SUMLAYER1_3", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = XOR8.get_position();
	csa8[temppos[0]][temppos[1]] = XOR8;
	#
	#######################################################
	#######################################################
	#CLAYER1_4####################################################
	AND10 = gate();
	AND10.set_name("AND10");
	AND10.set_number(gate_number);
	AND10.set_position(current_x,current_y);
	AND10.add_input("A3", None);
	AND10.add_input("B3", None);
	AND10.add_output("AND10_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND10.get_position();
	csa8[temppos[0]][temppos[1]] = AND10;
	#
	#######################################################
	#
	AND11 = gate();
	AND11.set_name("AND11");
	AND11.set_number(gate_number);
	AND11.set_position(current_x,current_y);
	AND11.add_input("B3", None);
	AND11.add_input("CA3", None);
	AND11.add_output("AND11_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND11.get_position();
	csa8[temppos[0]][temppos[1]] = AND11;
	#
	#######################################################
	#
	AND12 = gate();
	AND12.set_name("AND12");
	AND12.set_number(gate_number);
	AND12.set_position(current_x,current_y);
	AND12.add_input("CA3", None);
	AND12.add_input("A3", None);
	AND12.add_output("AND12_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND12.get_position();
	csa8[temppos[0]][temppos[1]] = AND12;
	#
	#######################################################
	#
	OR7 = gate();
	OR7.set_name("OR7");
	OR7.set_number(gate_number);
	OR7.set_position(current_x,current_y);
	OR7.add_input("AND10_OUT", None);
	OR7.add_input("AND11_OUT", None);
	OR7.add_output("OR7_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = OR7.get_position();
	csa8[temppos[0]][temppos[1]] = OR7;
	#
	#######################################################
	#
	OR8 = gate();
	OR8.set_name("OR6");
	OR8.set_number(gate_number);
	OR8.set_position(current_x,current_y);
	OR8.add_input("OR7_OUT", None);
	OR8.add_input("AND12_OUT", None);
	OR8.add_output("CLAYER1_4", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
	#Done with FA, update row
	current_x = current_x + 1;
	temppos = OR8.get_position();
	csa8[temppos[0]][temppos[1]] = OR8;
	#######################################################
	#######################################################
	
	'''FULL ADDER 4'''
	
	
	#######################################################
	#######################################################
	#SUMLAYER1_4##################################################
	XOR9 = gate();
	XOR9.set_name("XOR9");
	XOR9.set_number(gate_number);
	XOR9.set_position(current_x,current_y);
	XOR9.add_input("A4", None);
	XOR9.add_input("B4", None);
	XOR9.add_output("XOR9_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = XOR9.get_position();
	csa8[temppos[0]][temppos[1]] = XOR9;
	#
	#######################################################
	#
	XOR10 = gate();
	XOR10.set_name("XOR10");
	XOR10.set_number(gate_number);
	XOR10.set_position(current_x,current_y);
	XOR10.add_input("CA4", None);
	XOR10.add_input("XOR10_OUT", None);
	XOR10.add_output("SUMLAYER1_4", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = XOR10.get_position();
	csa8[temppos[0]][temppos[1]] = XOR10;
	#
	#######################################################
	#######################################################
	#CLAYER1_5####################################################
	AND13 = gate();
	AND13.set_name("AND13");
	AND13.set_number(gate_number);
	AND13.set_position(current_x,current_y);
	AND13.add_input("A4", None);
	AND13.add_input("B4", None);
	AND13.add_output("AND13_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND13.get_position();
	csa8[temppos[0]][temppos[1]] = AND13;
	#
	#######################################################
	#
	AND14 = gate();
	AND14.set_name("AND14");
	AND14.set_number(gate_number);
	AND14.set_position(current_x,current_y);
	AND14.add_input("B4", None);
	AND14.add_input("CA4", None);
	AND14.add_output("AND14_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND14.get_position();
	csa8[temppos[0]][temppos[1]] = AND14;
	#
	#######################################################
	#
	AND15 = gate();
	AND15.set_name("AND15");
	AND15.set_number(gate_number);
	AND15.set_position(current_x,current_y);
	AND15.add_input("CA4", None);
	AND15.add_input("A4", None);
	AND15.add_output("AND15_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND15.get_position();
	csa8[temppos[0]][temppos[1]] = AND15;
	#
	#######################################################
	#
	OR9 = gate();
	OR9.set_name("OR9");
	OR9.set_number(gate_number);
	OR9.set_position(current_x,current_y);
	OR9.add_input("AND13_OUT", None);
	OR9.add_input("AND14_OUT", None);
	OR9.add_output("OR9_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = OR9.get_position();
	csa8[temppos[0]][temppos[1]] = OR9;
	#
	#######################################################
	#
	OR10 = gate();
	OR10.set_name("OR10");
	OR10.set_number(gate_number);
	OR10.set_position(current_x,current_y);
	OR10.add_input("OR9_OUT", None);
	OR10.add_input("AND15_OUT", None);
	OR10.add_output("CLAYER1_5", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
	#Done with FA, update row
	current_x = current_x + 1;
	temppos = OR10.get_position();
	csa8[temppos[0]][temppos[1]] = OR10;
	#######################################################
	#######################################################
	
	
	'''FULL ADDER 5'''
	
	
	#######################################################
	#######################################################
	#SUMLAYER1_5##################################################
	XOR11 = gate();
	XOR11.set_name("XOR11");
	XOR11.set_number(gate_number);
	XOR11.set_position(current_x,current_y);
	XOR11.add_input("A5", None);
	XOR11.add_input("B5", None);
	XOR11.add_output("XOR11_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = XOR11.get_position();
	csa8[temppos[0]][temppos[1]] = XOR11;
	#
	#######################################################
	#
	XOR12 = gate();
	XOR12.set_name("XOR12");
	XOR12.set_number(gate_number);
	XOR12.set_position(current_x,current_y);
	XOR12.add_input("CA5", None);
	XOR12.add_input("XOR11_OUT", None);
	XOR12.add_output("SUMLAYER1_5", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = XOR12.get_position();
	csa8[temppos[0]][temppos[1]] = XOR12;
	#
	#######################################################
	#######################################################
	#CLAYER1_6####################################################
	AND16 = gate();
	AND16.set_name("AND16");
	AND16.set_number(gate_number);
	AND16.set_position(current_x,current_y);
	AND16.add_input("A5", None);
	AND16.add_input("B5", None);
	AND16.add_output("AND16_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND16.get_position();
	csa8[temppos[0]][temppos[1]] = AND16;
	#
	#######################################################
	#
	AND17 = gate();
	AND17.set_name("AND17");
	AND17.set_number(gate_number);
	AND17.set_position(current_x,current_y);
	AND17.add_input("B5", None);
	AND17.add_input("CA5", None);
	AND17.add_output("AND17_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND17.get_position();
	csa8[temppos[0]][temppos[1]] = AND17;
	#
	#######################################################
	#
	AND18 = gate();
	AND18.set_name("AND18");
	AND18.set_number(gate_number);
	AND18.set_position(current_x,current_y);
	AND18.add_input("CA5", None);
	AND18.add_input("A5", None);
	AND18.add_output("AND18_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND18.get_position();
	csa8[temppos[0]][temppos[1]] = AND18;
	#
	#######################################################
	#
	OR11 = gate();
	OR11.set_name("OR11");
	OR11.set_number(gate_number);
	OR11.set_position(current_x,current_y);
	OR11.add_input("AND16_OUT", None);
	OR11.add_input("AND17_OUT", None);
	OR11.add_output("OR11_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = OR11.get_position();
	csa8[temppos[0]][temppos[1]] = OR11;
	#
	#######################################################
	#
	OR12 = gate();
	OR12.set_name("OR12");
	OR12.set_number(gate_number);
	OR12.set_position(current_x,current_y);
	OR12.add_input("OR11_OUT", None);
	OR12.add_input("AND18_OUT", None);
	OR12.add_output("CLAYER1_6", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
	#Done with FA, update row
	current_x = current_x + 1;
	temppos = OR12.get_position();
	csa8[temppos[0]][temppos[1]] = OR12;
	#######################################################
	#######################################################
	
	'''FULL ADDER 6'''
	
	
	#######################################################
	#######################################################
	#SUMLAYER1_6##################################################
	XOR13 = gate();
	XOR13.set_name("XOR13");
	XOR13.set_number(gate_number);
	XOR13.set_position(current_x,current_y);
	XOR13.add_input("A6", None);
	XOR13.add_input("B6", None);
	XOR13.add_output("XOR13_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = XOR13.get_position();
	csa8[temppos[0]][temppos[1]] = XOR13;
	#
	#######################################################
	#
	XOR14 = gate();
	XOR14.set_name("XOR14");
	XOR14.set_number(gate_number);
	XOR14.set_position(current_x,current_y);
	XOR14.add_input("CA6", None);
	XOR14.add_input("XOR13_OUT", None);
	XOR14.add_output("SUMLAYER1_6", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = XOR14.get_position();
	csa8[temppos[0]][temppos[1]] = XOR14;
	#
	#######################################################
	#######################################################
	#CLAYER1_7####################################################
	AND19 = gate();
	AND19.set_name("AND19");
	AND19.set_number(gate_number);
	AND19.set_position(current_x,current_y);
	AND19.add_input("A6", None);
	AND19.add_input("B6", None);
	AND19.add_output("AND19_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND19.get_position();
	csa8[temppos[0]][temppos[1]] = AND19;
	#
	#######################################################
	#
	AND20 = gate();
	AND20.set_name("AND20");
	AND20.set_number(gate_number);
	AND20.set_position(current_x,current_y);
	AND20.add_input("B6", None);
	AND20.add_input("CA6", None);
	AND20.add_output("AND20_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND20.get_position();
	csa8[temppos[0]][temppos[1]] = AND20;
	#
	#######################################################
	#
	AND21 = gate();
	AND21.set_name("AND21");
	AND21.set_number(gate_number);
	AND21.set_position(current_x,current_y);
	AND21.add_input("CA6", None);
	AND21.add_input("A6", None);
	AND21.add_output("AND21_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND21.get_position();
	csa8[temppos[0]][temppos[1]] = AND21;
	#
	#######################################################
	#
	OR13 = gate();
	OR13.set_name("OR13");
	OR13.set_number(gate_number);
	OR13.set_position(current_x,current_y);
	OR13.add_input("AND19_OUT", None);
	OR13.add_input("AND20_OUT", None);
	OR13.add_output("OR13_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = OR13.get_position();
	csa8[temppos[0]][temppos[1]] = OR13;
	#
	#######################################################
	#
	OR14 = gate();
	OR14.set_name("OR14");
	OR14.set_number(gate_number);
	OR14.set_position(current_x,current_y);
	OR14.add_input("OR13_OUT", None);
	OR14.add_input("AND21_OUT", None);
	OR14.add_output("CLAYER1_7", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
	#Done with FA, update row
	current_x = current_x + 1;
	temppos = OR14.get_position();
	csa8[temppos[0]][temppos[1]] = OR14;
	#######################################################
	#######################################################
	
	'''FULL ADDER 7'''
	
	
	#######################################################
	#######################################################
	#SUMLAYER1_7##################################################
	XOR15 = gate();
	XOR15.set_name("XOR15");
	XOR15.set_number(gate_number);
	XOR15.set_position(current_x,current_y);
	XOR15.add_input("A7", None);
	XOR15.add_input("B7", None);
	XOR15.add_output("XOR15_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = XOR15.get_position();
	csa8[temppos[0]][temppos[1]] = XOR15;
	#
	#######################################################
	#
	XOR16 = gate();
	XOR16.set_name("XOR16");
	XOR16.set_number(gate_number);
	XOR16.set_position(current_x,current_y);
	XOR16.add_input("CA7", None);
	XOR16.add_input("XOR15_OUT", None);
	XOR16.add_output("SUMLAYER1_7", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = XOR16.get_position();
	csa8[temppos[0]][temppos[1]] = XOR16;
	#
	#######################################################
	#######################################################
	#CLAYER1_OUT####################################################
	AND22 = gate();
	AND22.set_name("AND22");
	AND22.set_number(gate_number);
	AND22.set_position(current_x,current_y);
	AND22.add_input("A7", None);
	AND22.add_input("B7", None);
	AND22.add_output("AND22_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND22.get_position();
	csa8[temppos[0]][temppos[1]] = AND22;
	#
	#######################################################
	#
	AND23 = gate();
	AND23.set_name("AND23");
	AND23.set_number(gate_number);
	AND23.set_position(current_x,current_y);
	AND23.add_input("B7", None);
	AND23.add_input("CA7", None);
	AND23.add_output("AND23_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND23.get_position();
	csa8[temppos[0]][temppos[1]] = AND23;
	#
	#######################################################
	#
	AND24 = gate();
	AND24.set_name("AND24");
	AND24.set_number(gate_number);
	AND24.set_position(current_x,current_y);
	AND24.add_input("CA7", None);
	AND24.add_input("A7", None);
	AND24.add_output("AND24_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND24.get_position();
	csa8[temppos[0]][temppos[1]] = AND24;
	#
	#######################################################
	#
	OR15 = gate();
	OR15.set_name("OR15");
	OR15.set_number(gate_number);
	OR15.set_position(current_x,current_y);
	OR15.add_input("AND22_OUT", None);
	OR15.add_input("AND23_OUT", None);
	OR15.add_output("OR15_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = OR15.get_position();
	csa8[temppos[0]][temppos[1]] = OR15;
	#
	#######################################################
	#
	OR16 = gate();
	OR16.set_name("OR16");
	OR16.set_number(gate_number);
	OR16.set_position(current_x,current_y);
	OR16.add_input("OR15_OUT", None);
	OR16.add_input("AND24_OUT", None);
	OR16.add_output("CLAYER1_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
	#Done with FA, update row
	current_x = current_x + 1;
	temppos = OR16.get_position();
	csa8[temppos[0]][temppos[1]] = OR16;
	#######################################################
	#######################################################
	
	
	##
	##THIS IS THE SECOND LAYER OF FULL ADDERS 
	##
	
	'''FULL ADDER 8'''
	
	#######################################################
	#######################################################
	#SUMOUT_0##################################################
	XOR17 = gate();
	XOR17.set_name("XOR17");
	XOR17.set_number(gate_number);
	XOR17.set_position(current_x,current_y);
	XOR17.add_input("SUMLAYER1_0", None);
	XOR17.add_input("VSS", None);
	XOR17.add_output("XOR17_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = XOR17.get_position();
	csa8[temppos[0]][temppos[1]] = XOR17;
	#
	#######################################################
	#
	XOR18 = gate();
	XOR18.set_name("XOR18");
	XOR18.set_number(gate_number);
	XOR18.set_position(current_x,current_y);
	XOR18.add_input("CB0", None);
	XOR18.add_input("XOR17_OUT", None);
	XOR18.add_output("SUMOUT_0", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = XOR18.get_position();
	csa8[temppos[0]][temppos[1]] = XOR18;
	#
	#######################################################
	#######################################################
	#COUT_1####################################################
	AND25 = gate();
	AND25.set_name("AND25");
	AND25.set_number(gate_number);
	AND25.set_position(current_x,current_y);
	AND25.add_input("SUMLAYER1_0", None);
	AND25.add_input("VSS", None);
	AND25.add_output("AND25_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND25.get_position();
	csa8[temppos[0]][temppos[1]] = AND25;
	#
	#######################################################
	#
	AND26 = gate();
	AND26.set_name("AND26");
	AND26.set_number(gate_number);
	AND26.set_position(current_x,current_y);
	AND26.add_input("VSS", None);
	AND26.add_input("CB0", None);
	AND26.add_output("AND26_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND26.get_position();
	csa8[temppos[0]][temppos[1]] = AND26;
	#
	#######################################################
	#
	AND27 = gate();
	AND27.set_name("AND27");
	AND27.set_number(gate_number);
	AND27.set_position(current_x,current_y);
	AND27.add_input("CB0", None);
	AND27.add_input("SUMLAYER1_0", None);
	AND27.add_output("AND27_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND27.get_position();
	csa8[temppos[0]][temppos[1]] = AND27;
	#
	#######################################################
	#
	OR17 = gate();
	OR17.set_name("OR17");
	OR17.set_number(gate_number);
	OR17.set_position(current_x,current_y);
	OR17.add_input("AND25_OUT", None);
	OR17.add_input("AND26_OUT", None);
	OR17.add_output("OR17_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = OR17.get_position();
	csa8[temppos[0]][temppos[1]] = OR17;
	#
	#######################################################
	#
	OR18 = gate();
	OR18.set_name("OR18");
	OR18.set_number(gate_number);
	OR18.set_position(current_x,current_y);
	OR18.add_input("OR17_OUT", None);
	OR18.add_input("AND27_OUT", None);
	OR18.add_output("COUT_1", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
	#Done with FA, update row
	current_x = current_x + 1;
	temppos = OR18.get_position();
	csa8[temppos[0]][temppos[1]] = OR18;
	#######################################################
	#######################################################
	
	'''FULL ADDER 9'''
	
	
	#######################################################
	#######################################################
	#SUMOUT_1##################################################
	XOR19 = gate();
	XOR19.set_name("XOR19");
	XOR19.set_number(gate_number);
	XOR19.set_position(current_x,current_y);
	XOR19.add_input("SUMLAYER1_1", None);
	XOR19.add_input("CLAYER1_1", None);
	XOR19.add_output("XOR19_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = XOR19.get_position();
	csa8[temppos[0]][temppos[1]] = XOR19;
	#
	#######################################################
	#
	XOR20 = gate();
	XOR20.set_name("XOR20");
	XOR20.set_number(gate_number);
	XOR20.set_position(current_x,current_y);
	XOR20.add_input("CB1", None);
	XOR20.add_input("XOR19_OUT", None);
	XOR20.add_output("SUMOUT_1", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = XOR20.get_position();
	csa8[temppos[0]][temppos[1]] = XOR20;
	#
	#######################################################
	#######################################################
	#COUT_2####################################################
	AND28 = gate();
	AND28.set_name("AND28");
	AND28.set_number(gate_number);
	AND28.set_position(current_x,current_y);
	AND28.add_input("SUMLAYER1_1", None);
	AND28.add_input("CLAYER1_1", None);
	AND28.add_output("AND28_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND28.get_position();
	csa8[temppos[0]][temppos[1]] = AND28;
	#
	#######################################################
	#
	AND29 = gate();
	AND29.set_name("AND29");
	AND29.set_number(gate_number);
	AND29.set_position(current_x,current_y);
	AND29.add_input("CLAYER1_1", None);
	AND29.add_input("CB1", None);
	AND29.add_output("AND29_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND29.get_position();
	csa8[temppos[0]][temppos[1]] = AND29;
	#
	#######################################################
	#
	AND30 = gate();
	AND30.set_name("AND30");
	AND30.set_number(gate_number);
	AND30.set_position(current_x,current_y);
	AND30.add_input("CB1", None);
	AND30.add_input("SUMLAYER1_1", None);
	AND30.add_output("AND30_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND30.get_position();
	csa8[temppos[0]][temppos[1]] = AND30;
	#
	#######################################################
	#
	OR19 = gate();
	OR19.set_name("OR19");
	OR19.set_number(gate_number);
	OR19.set_position(current_x,current_y);
	OR19.add_input("AND29_OUT", None);
	OR19.add_input("AND30_OUT", None);
	OR19.add_output("OR19_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = OR19.get_position();
	csa8[temppos[0]][temppos[1]] = OR19;
	#
	#######################################################
	#
	OR20 = gate();
	OR20.set_name("OR20");
	OR20.set_number(gate_number);
	OR20.set_position(current_x,current_y);
	OR20.add_input("OR19_OUT", None);
	OR20.add_input("AND30_OUT", None);
	OR20.add_output("COUT_2", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
	#Done with FA, update row
	current_x = current_x + 1;
	temppos = OR20.get_position();
	csa8[temppos[0]][temppos[1]] = OR20;
	#######################################################
	#######################################################
	
	'''FULL ADDER 10'''
	
	
	#######################################################
	#######################################################
	#SUMOUT_2##################################################
	XOR21 = gate();
	XOR21.set_name("XOR21");
	XOR21.set_number(gate_number);
	XOR21.set_position(current_x,current_y);
	XOR21.add_input("SUMLAYER1_2", None);
	XOR21.add_input("CLAYER1_2", None);
	XOR21.add_output("XOR21_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = XOR21.get_position();
	csa8[temppos[0]][temppos[1]] = XOR21;
	#
	#######################################################
	#
	XOR22 = gate();
	XOR22.set_name("XOR22");
	XOR22.set_number(gate_number);
	XOR22.set_position(current_x,current_y);
	XOR22.add_input("CB2", None);
	XOR22.add_input("XOR21_OUT", None);
	XOR22.add_output("SUMOUT_2", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = XOR22.get_position();
	csa8[temppos[0]][temppos[1]] = XOR22;
	#
	#######################################################
	#######################################################
	#COUT_3####################################################
	AND31 = gate();
	AND31.set_name("AND31");
	AND31.set_number(gate_number);
	AND31.set_position(current_x,current_y);
	AND31.add_input("SUMLAYER1_2", None);
	AND31.add_input("CLAYER1_2", None);
	AND31.add_output("AND31_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND31.get_position();
	csa8[temppos[0]][temppos[1]] = AND31;
	#
	#######################################################
	#
	AND32 = gate();
	AND32.set_name("AND32");
	AND32.set_number(gate_number);
	AND32.set_position(current_x,current_y);
	AND32.add_input("CLAYER1_2", None);
	AND32.add_input("CB2", None);
	AND32.add_output("AND32_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND32.get_position();
	csa8[temppos[0]][temppos[1]] = AND32;
	#
	#######################################################
	#
	AND33 = gate();
	AND33.set_name("AND33");
	AND33.set_number(gate_number);
	AND33.set_position(current_x,current_y);
	AND33.add_input("CB2", None);
	AND33.add_input("SUMLAYER1_2", None);
	AND33.add_output("AND32_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND33.get_position();
	csa8[temppos[0]][temppos[1]] = AND33;
	#
	#######################################################
	#
	OR21 = gate();
	OR21.set_name("OR21");
	OR21.set_number(gate_number);
	OR21.set_position(current_x,current_y);
	OR21.add_input("AND31_OUT", None);
	OR21.add_input("AND32_OUT", None);
	OR21.add_output("OR21_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = OR21.get_position();
	csa8[temppos[0]][temppos[1]] = OR21;
	#
	#######################################################
	#
	OR22 = gate();
	OR22.set_name("OR22");
	OR22.set_number(gate_number);
	OR22.set_position(current_x,current_y);
	OR22.add_input("OR21_OUT", None);
	OR22.add_input("AND33_OUT", None);
	OR22.add_output("COUT_3", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
	#Done with FA, update row
	current_x = current_x + 1;
	temppos = OR22.get_position();
	csa8[temppos[0]][temppos[1]] = OR22;
	#######################################################
	#######################################################
	
	'''FULL ADDER 11'''
	
	
	#######################################################
	#######################################################
	#SUMOUT_3##################################################
	XOR23 = gate();
	XOR23.set_name("XOR23");
	XOR23.set_number(gate_number);
	XOR23.set_position(current_x,current_y);
	XOR23.add_input("SUMLAYER1_3", None);
	XOR23.add_input("CLAYER1_3", None);
	XOR23.add_output("XOR23_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = XOR23.get_position();
	csa8[temppos[0]][temppos[1]] = XOR23;
	#
	#######################################################
	#
	XOR24 = gate();
	XOR24.set_name("XOR24");
	XOR24.set_number(gate_number);
	XOR24.set_position(current_x,current_y);
	XOR24.add_input("CB3", None);
	XOR24.add_input("XOR23_OUT", None);
	XOR24.add_output("SUMOUT_3", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = XOR24.get_position();
	csa8[temppos[0]][temppos[1]] = XOR24;
	#
	#######################################################
	#######################################################
	#COUT_4####################################################
	AND34 = gate();
	AND34.set_name("AND34");
	AND34.set_number(gate_number);
	AND34.set_position(current_x,current_y);
	AND34.add_input("SUMLAYER1_3", None);
	AND34.add_input("CLAYER1_3", None);
	AND34.add_output("AND34_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND34.get_position();
	csa8[temppos[0]][temppos[1]] = AND34;
	#
	#######################################################
	#
	AND35 = gate();
	AND35.set_name("AND35");
	AND35.set_number(gate_number);
	AND35.set_position(current_x,current_y);
	AND35.add_input("CLAYER1_3", None);
	AND35.add_input("CB3", None);
	AND35.add_output("AND35_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND35.get_position();
	csa8[temppos[0]][temppos[1]] = AND35;
	#
	#######################################################
	#
	AND36 = gate();
	AND36.set_name("AND36");
	AND36.set_number(gate_number);
	AND36.set_position(current_x,current_y);
	AND36.add_input("CB3", None);
	AND36.add_input("SUMLAYER1_3", None);
	AND36.add_output("AND36_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND36.get_position();
	csa8[temppos[0]][temppos[1]] = AND36;
	#
	#######################################################
	#
	OR23 = gate();
	OR23.set_name("OR23");
	OR23.set_number(gate_number);
	OR23.set_position(current_x,current_y);
	OR23.add_input("AND34_OUT", None);
	OR23.add_input("AND35_OUT", None);
	OR23.add_output("OR23_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = OR23.get_position();
	csa8[temppos[0]][temppos[1]] = OR23;
	#
	#######################################################
	#
	OR24 = gate();
	OR24.set_name("OR24");
	OR24.set_number(gate_number);
	OR24.set_position(current_x,current_y);
	OR24.add_input("OR23_OUT", None);
	OR24.add_input("AND36_OUT", None);
	OR24.add_output("COUT_4", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
	#Done with FA, update row
	current_x = current_x + 1;
	temppos = OR24.get_position();
	csa8[temppos[0]][temppos[1]] = OR24;
	#######################################################
	#######################################################
	
	'''FULL ADDER 12'''
	
	
	#######################################################
	#######################################################
	#SUMOUT_4##################################################
	XOR25 = gate();
	XOR25.set_name("XOR25");
	XOR25.set_number(gate_number);
	XOR25.set_position(current_x,current_y);
	XOR25.add_input("SUMLAYER1_4", None);
	XOR25.add_input("CLAYER1_4", None);
	XOR25.add_output("XOR25_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = XOR25.get_position();
	csa8[temppos[0]][temppos[1]] = XOR25;
	#
	#######################################################
	#
	XOR26 = gate();
	XOR26.set_name("XOR26");
	XOR26.set_number(gate_number);
	XOR26.set_position(current_x,current_y);
	XOR26.add_input("CB4", None);
	XOR26.add_input("XOR125_OUT", None);
	XOR26.add_output("SUMOUT_4", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = XOR26.get_position();
	csa8[temppos[0]][temppos[1]] = XOR26;
	#
	#######################################################
	#######################################################
	#COUT_5####################################################
	AND37 = gate();
	AND37.set_name("AND37");
	AND37.set_number(gate_number);
	AND37.set_position(current_x,current_y);
	AND37.add_input("SUMLAYER1_4", None);
	AND37.add_input("CLAYER1_4", None);
	AND37.add_output("AND37_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND37.get_position();
	csa8[temppos[0]][temppos[1]] = AND37;
	#
	#######################################################
	#
	AND38 = gate();
	AND38.set_name("AND38");
	AND38.set_number(gate_number);
	AND38.set_position(current_x,current_y);
	AND38.add_input("CLAYER1_4", None);
	AND38.add_input("CB4", None);
	AND38.add_output("AND38_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND38.get_position();
	csa8[temppos[0]][temppos[1]] = AND38;
	#
	#######################################################
	#
	AND39 = gate();
	AND39.set_name("AND39");
	AND39.set_number(gate_number);
	AND39.set_position(current_x,current_y);
	AND39.add_input("CB4", None);
	AND39.add_input("SUMLAYER1_4", None);
	AND39.add_output("AND39_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND39.get_position();
	csa8[temppos[0]][temppos[1]] = AND39;
	#
	#######################################################
	#
	OR25 = gate();
	OR25.set_name("OR25");
	OR25.set_number(gate_number);
	OR25.set_position(current_x,current_y);
	OR25.add_input("AND37_OUT", None);
	OR25.add_input("AND38_OUT", None);
	OR25.add_output("OR25_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = OR25.get_position();
	csa8[temppos[0]][temppos[1]] = OR25;
	#
	#######################################################
	#
	OR26 = gate();
	OR26.set_name("OR26");
	OR26.set_number(gate_number);
	OR26.set_position(current_x,current_y);
	OR26.add_input("OR25_OUT", None);
	OR26.add_input("AND39_OUT", None);
	OR26.add_output("COUT_5", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
	#Done with FA, update row
	current_x = current_x + 1;
	temppos = OR26.get_position();
	csa8[temppos[0]][temppos[1]] = OR26;
	#######################################################
	#######################################################
	
	
	'''FULL ADDER 13'''
	
	
	#######################################################
	#######################################################
	#SUMOUT_5##################################################
	XOR27 = gate();
	XOR27.set_name("XOR27");
	XOR27.set_number(gate_number);
	XOR27.set_position(current_x,current_y);
	XOR27.add_input("SUMLAYER1_5", None);
	XOR27.add_input("CLAYER1_5", None);
	XOR27.add_output("XOR27_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = XOR27.get_position();
	csa8[temppos[0]][temppos[1]] = XOR27;
	#
	#######################################################
	#
	XOR28 = gate();
	XOR28.set_name("XOR28");
	XOR28.set_number(gate_number);
	XOR28.set_position(current_x,current_y);
	XOR28.add_input("CB5", None);
	XOR28.add_input("XOR27_OUT", None);
	XOR28.add_output("SUMOUT_5", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = XOR28.get_position();
	csa8[temppos[0]][temppos[1]] = XOR28;
	#
	#######################################################
	#######################################################
	#COUT_6####################################################
	AND40 = gate();
	AND40.set_name("AND40");
	AND40.set_number(gate_number);
	AND40.set_position(current_x,current_y);
	AND40.add_input("SUMLAYER1_5", None);
	AND40.add_input("CLAYER1_5", None);
	AND40.add_output("AND40_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND40.get_position();
	csa8[temppos[0]][temppos[1]] = AND40;
	#
	#######################################################
	#
	AND41 = gate();
	AND41.set_name("AND41");
	AND41.set_number(gate_number);
	AND41.set_position(current_x,current_y);
	AND41.add_input("CLAYER1_5", None);
	AND41.add_input("CB5", None);
	AND41.add_output("AND41_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND41.get_position();
	csa8[temppos[0]][temppos[1]] = AND41;
	#
	#######################################################
	#
	AND42 = gate();
	AND42.set_name("AND42");
	AND42.set_number(gate_number);
	AND42.set_position(current_x,current_y);
	AND42.add_input("CB5", None);
	AND42.add_input("SUMLAYER1_5", None);
	AND42.add_output("AND42_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND42.get_position();
	csa8[temppos[0]][temppos[1]] = AND42;
	#
	#######################################################
	#
	OR27 = gate();
	OR27.set_name("OR27");
	OR27.set_number(gate_number);
	OR27.set_position(current_x,current_y);
	OR27.add_input("AND39_OUT", None);
	OR27.add_input("AND40_OUT", None);
	OR27.add_output("OR27_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = OR27.get_position();
	csa8[temppos[0]][temppos[1]] = OR27;
	#
	#######################################################
	#
	OR28 = gate();
	OR28.set_name("OR28");
	OR28.set_number(gate_number);
	OR28.set_position(current_x,current_y);
	OR28.add_input("OR27_OUT", None);
	OR28.add_input("AND41_OUT", None);
	OR28.add_output("COUT_6", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
	#Done with FA, update row
	current_x = current_x + 1;
	temppos = OR28.get_position();
	csa8[temppos[0]][temppos[1]] = OR28;
	#######################################################
	#######################################################
	
	'''FULL ADDER 14'''
	
	
	#######################################################
	#######################################################
	#SUMOUT_6##################################################
	XOR29 = gate();
	XOR29.set_name("XOR29");
	XOR29.set_number(gate_number);
	XOR29.set_position(current_x,current_y);
	XOR29.add_input("SUMLAYER1_6", None);
	XOR29.add_input("CLAYER1_6", None);
	XOR29.add_output("XOR29_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = XOR29.get_position();
	csa8[temppos[0]][temppos[1]] = XOR29;
	#
	#######################################################
	#
	XOR30 = gate();
	XOR30.set_name("XOR30");
	XOR30.set_number(gate_number);
	XOR30.set_position(current_x,current_y);
	XOR30.add_input("CB6", None);
	XOR30.add_input("XOR29_OUT", None);
	XOR30.add_output("SUMOUT_6", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = XOR30.get_position();
	csa8[temppos[0]][temppos[1]] = XOR30;
	#
	#######################################################
	#######################################################
	#COUT_7####################################################
	AND43 = gate();
	AND43.set_name("AND43");
	AND43.set_number(gate_number);
	AND43.set_position(current_x,current_y);
	AND43.add_input("SUMLAYER1_6", None);
	AND43.add_input("CLAYER1_6", None);
	AND43.add_output("AND43_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND43.get_position();
	csa8[temppos[0]][temppos[1]] = AND43;
	#
	#######################################################
	#
	AND44 = gate();
	AND44.set_name("AND44");
	AND44.set_number(gate_number);
	AND44.set_position(current_x,current_y);
	AND44.add_input("CLAYER1_6", None);
	AND44.add_input("CB6", None);
	AND44.add_output("AND44_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND44.get_position();
	csa8[temppos[0]][temppos[1]] = AND44;
	#
	#######################################################
	#
	AND45 = gate();
	AND45.set_name("AND45");
	AND45.set_number(gate_number);
	AND45.set_position(current_x,current_y);
	AND45.add_input("CB6", None);
	AND45.add_input("SUMLAYER1_6", None);
	AND45.add_output("AND45_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND45.get_position();
	csa8[temppos[0]][temppos[1]] = AND45;
	#
	#######################################################
	#
	OR29 = gate();
	OR29.set_name("OR29");
	OR29.set_number(gate_number);
	OR29.set_position(current_x,current_y);
	OR29.add_input("AND43_OUT", None);
	OR29.add_input("AND44_OUT", None);
	OR29.add_output("OR29_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = OR29.get_position();
	csa8[temppos[0]][temppos[1]] = OR29;
	#
	#######################################################
	#
	OR30 = gate();
	OR30.set_name("OR30");
	OR30.set_number(gate_number);
	OR30.set_position(current_x,current_y);
	OR30.add_input("OR29_OUT", None);
	OR30.add_input("AND45_OUT", None);
	OR30.add_output("COUT_7", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
	#Done with FA, update row
	current_x = current_x + 1;
	temppos = OR30.get_position();
	csa8[temppos[0]][temppos[1]] = OR30;
	#######################################################
	#######################################################
	
	'''FULL ADDER 15'''
	
	
	#######################################################
	#######################################################
	#SUMOUT_7##################################################
	XOR31 = gate();
	XOR31.set_name("XOR31");
	XOR31.set_number(gate_number);
	XOR31.set_position(current_x,current_y);
	XOR31.add_input("SUMLAYER1_7", None);
	XOR31.add_input("CLAYER1_7", None);
	XOR31.add_output("XOR31_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = XOR31.get_position();
	csa8[temppos[0]][temppos[1]] = XOR31;
	#
	#######################################################
	#
	XOR32 = gate();
	XOR32.set_name("XOR32");
	XOR32.set_number(gate_number);
	XOR32.set_position(current_x,current_y);
	XOR32.add_input("CB7", None);
	XOR32.add_input("XOR31_OUT", None);
	XOR32.add_output("SUMOUT_7", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = XOR32.get_position();
	csa8[temppos[0]][temppos[1]] = XOR32;
	#
	#######################################################
	#######################################################
	#COUT_OUT####################################################
	AND46 = gate();
	AND46.set_name("AND46");
	AND46.set_number(gate_number);
	AND46.set_position(current_x,current_y);
	AND46.add_input("SUMLAYER1_7", None);
	AND46.add_input("CLAYER1_7", None);
	AND46.add_output("AND46_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND46.get_position();
	csa8[temppos[0]][temppos[1]] = AND46;
	#
	#######################################################
	#
	AND47 = gate();
	AND47.set_name("AND47");
	AND47.set_number(gate_number);
	AND47.set_position(current_x,current_y);
	AND47.add_input("CLAYER1_7", None);
	AND47.add_input("CB7", None);
	AND47.add_output("AND47_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND47.get_position();
	csa8[temppos[0]][temppos[1]] = AND47;
	#
	#######################################################
	#
	AND48 = gate();
	AND48.set_name("AND48");
	AND48.set_number(gate_number);
	AND48.set_position(current_x,current_y);
	AND48.add_input("CB7", None);
	AND48.add_input("SUMLAYER1_7", None);
	AND48.add_output("AND48_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND48.get_position();
	csa8[temppos[0]][temppos[1]] = AND48;
	#
	#######################################################
	#
	OR31 = gate();
	OR31.set_name("OR31");
	OR31.set_number(gate_number);
	OR31.set_position(current_x,current_y);
	OR31.add_input("AND46_OUT", None);
	OR31.add_input("AND47_OUT", None);
	OR31.add_output("OR31_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = OR31.get_position();
	csa8[temppos[0]][temppos[1]] = OR31;
	#
	#######################################################
	#
	OR32 = gate();
	OR32.set_name("OR32");
	OR32.set_number(gate_number);
	OR32.set_position(current_x,current_y);
	OR32.add_input("OR31_OUT", None);
	OR32.add_input("AND48_OUT", None);
	OR32.add_output("COUT_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
	#Done with FA, update row
	current_x = current_x + 1;
	temppos = OR32.get_position();
	csa8[temppos[0]][temppos[1]] = OR32;
	#######################################################
	#######################################################
	
	print("CSA placed cell grid: ");
	print(csa8);
	#get placed gate count - sanity checking grid for duplicates and misplaced gates
	#there could still be typos - just fyi
	placed_count = 0;
	duplicate_gate_count = 0;
	for i in range(len(csa8)):
	
		for j in range(len(csa8[i])):
		
			if(csa8[i][j] != None):
				placed_count = placed_count + 1;
				##UNCOMMENT FOR GATE INFO
				csa8[i][j].get_info();
				
			#Performing list check for inputs and outputs
			
			for k in range(len(csa8)):
			
				for l in range(len(csa8[k])):
				
					if(csa8[i][j] != None and csa8[k][l] != None and (i != k and j != l)):
							gate1_in = str(csa8[i][j].inputs);
							gate2_in = str(csa8[k][l].inputs);
							
							gate1_out = str(csa8[i][j].outputs);
							gate2_out = str(csa8[k][l].outputs);
							
							if(gate1_in == gate2_in and gate1_out == gate2_out):
								csa8[i][j].get_info();
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
		print("duplicates found :'(");

#I like having a main method because I'm particular like that.
#Also you scrolled down this far. Good on you.
def main():

	make_csa8();
	
main();	