import sys
import math
sys.path.append("..")

from model import params
from gates import *

#This is gonna be a big one - datapath for an 8-bit carry lookahead adder.
#We need 7 reduced full adders with spread XOR logic to use in both propagate
#and generate signal production. 1 normal full adder with spread logic to produce
#an output carry (slightly faster than otherwise).
#The propagte and generate signals are fed into (for radix 4 in this case) a CLA
#logic block for generating the carries from propagate and generate signals in bit 3:0,
#then into another for bits 7:4. These carries flow into the corresponding RFA/FA's for 
#each bit.

def make_cla8():

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
	
	grid_y = 8;
	grid_x = 70;
	
	#creating a grid data structure with the dimsions specified in params
	#not using a dictionary because order is important for routing - fight me
	cla8 = [[None for i in range(grid_y)] for i in range(grid_x)];
	
	#bookkeeping
	gate_number = 1;
	max_y = 6;
	current_y = 0;
	current_x = 0;
	
	'''Gen C0'''
	#######################################################
	#
	AND47 = gate();
	AND47.set_name("AND47");
	AND47.set_number(gate_number);
	AND47.set_position(current_x,current_y);
	AND47.add_input("B0", None);
	AND47.add_input("A0", None);
	AND47.add_output("AND47_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND47.get_position();
	cla8[temppos[0]][temppos[1]] = AND47;
	#
	#######################################################
	#
	AND48 = gate();
	AND48.set_name("AND48");
	AND48.set_number(gate_number);
	AND48.set_position(current_x,current_y);
	AND48.add_input("B0", None);
	AND48.add_input("CIN", None);
	AND48.add_output("AND48_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND48.get_position();
	cla8[temppos[0]][temppos[1]] = AND48;
	#
	#######################################################
	#
	AND49 = gate();
	AND49.set_name("AND49");
	AND49.set_number(gate_number);
	AND49.set_position(current_x,current_y);
	AND49.add_input("A0", None);
	AND49.add_input("CIN", None);
	AND49.add_output("AND49_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND49.get_position();
	cla8[temppos[0]][temppos[1]] = AND49;
	#
	#######################################################
	#
	OR25 = gate();
	OR25.set_name("OR25");
	OR25.set_number(gate_number);
	OR25.set_position(current_x,current_y);
	OR25.add_input("AND47_OUT", None);
	OR25.add_input("AND48_OUT", None);
	OR25.add_output("OR25_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = OR25.get_position();
	cla8[temppos[0]][temppos[1]] = OR25;
	#
	#######################################################
	#
	OR26 = gate();
	OR26.set_name("OR26");
	OR26.set_number(gate_number);
	OR26.set_position(current_x,current_y);
	OR26.add_input("OR25_OUT", None);
	OR26.add_input("AND49_OUT", None);
	OR26.add_output("C0", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
	current_x = current_x + 1;
	temppos = OR26.get_position();
	cla8[temppos[0]][temppos[1]] = OR26;
	
	
	'''REDUCED FULL ADDER 0'''
	
	#######################################################
	#######################################################
	#Sum0, P0, G0##################################################
	AND1 = gate();
	AND1.set_name("AND1");
	AND1.set_number(gate_number);
	AND1.set_position(current_x,current_y);
	AND1.add_input("A0", None);
	AND1.add_input("B0", None);
	AND1.add_output("G0", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND1.get_position();
	cla8[temppos[0]][temppos[1]] = AND1;
	#
	#######################################################
	#
	INV1 = gate();
	INV1.set_name("INV1");
	INV1.set_number(gate_number);
	INV1.set_position(current_x,current_y);
	INV1.add_input("G0", None);
	INV1.add_output("INV1_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = INV1.get_position();
	cla8[temppos[0]][temppos[1]] = INV1;
	#
	#######################################################
	#
	OR1 = gate();
	OR1.set_name("OR1");
	OR1.set_number(gate_number);
	OR1.set_position(current_x,current_y);
	OR1.add_input("A0", None);
	OR1.add_input("B0", None);
	OR1.add_output("P0", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = OR1.get_position();
	cla8[temppos[0]][temppos[1]] = OR1;
	#
	#######################################################
	#
	AND2 = gate();
	AND2.set_name("AND2");
	AND2.set_number(gate_number);
	AND2.set_position(current_x,current_y);
	AND2.add_input("P0", None);
	AND2.add_input("INV1_OUT", None);
	AND2.add_output("AND2_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND2.get_position();
	cla8[temppos[0]][temppos[1]] = AND2;
	#
	#######################################################
	#
	XOR1 = gate();
	XOR1.set_name("XOR1");
	XOR1.set_number(gate_number);
	XOR1.set_position(current_x,current_y);
	XOR1.add_input("CIN", None);
	XOR1.add_input("AND2_OUT", None);
	XOR1.add_output("SUM0", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
	#Done with FA, update row
	current_x = current_x + 1;
	temppos = XOR1.get_position();
	cla8[temppos[0]][temppos[1]] = XOR1;
	#
	#######################################################
	
	
	'''REDUCED FULL ADDER 1'''
	
	#######################################################
	#######################################################
	#Sum1, P1, G1##################################################
	AND3 = gate();
	AND3.set_name("AND3");
	AND3.set_number(gate_number);
	AND3.set_position(current_x,current_y);
	AND3.add_input("A1", None);
	AND3.add_input("B1", None);
	AND3.add_output("G1", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND3.get_position();
	cla8[temppos[0]][temppos[1]] = AND3;
	#
	#######################################################
	#
	INV2 = gate();
	INV2.set_name("INV2");
	INV2.set_number(gate_number);
	INV2.set_position(current_x,current_y);
	INV2.add_input("G1", None);
	INV2.add_output("INV2_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = INV2.get_position();
	cla8[temppos[0]][temppos[1]] = INV2;
	#
	#######################################################
	#
	OR2 = gate();
	OR2.set_name("OR2");
	OR2.set_number(gate_number);
	OR2.set_position(current_x,current_y);
	OR2.add_input("A1", None);
	OR2.add_input("B1", None);
	OR2.add_output("P1", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = OR2.get_position();
	cla8[temppos[0]][temppos[1]] = OR2;
	#
	#######################################################
	#
	AND4 = gate();
	AND4.set_name("AND4");
	AND4.set_number(gate_number);
	AND4.set_position(current_x,current_y);
	AND4.add_input("P1", None);
	AND4.add_input("INV2_OUT", None);
	AND4.add_output("AND4_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND4.get_position();
	cla8[temppos[0]][temppos[1]] = AND4;
	#
	#######################################################
	#
	XOR2 = gate();
	XOR2.set_name("XOR2");
	XOR2.set_number(gate_number);
	XOR2.set_position(current_x,current_y);
	XOR2.add_input("C0", None);
	XOR2.add_input("AND4_OUT", None);
	XOR2.add_output("SUM1", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
	#Done with FA, update row
	current_x = current_x + 1;
	temppos = XOR2.get_position();
	cla8[temppos[0]][temppos[1]] = XOR2;
	#
	#######################################################
	
	
	'''REDUCED FULL ADDER 2'''
	
	#######################################################
	#######################################################
	#Sum2, P2, G2##################################################
	AND5 = gate();
	AND5.set_name("AND5");
	AND5.set_number(gate_number);
	AND5.set_position(current_x,current_y);
	AND5.add_input("A2", None);
	AND5.add_input("B2", None);
	AND5.add_output("G2", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND5.get_position();
	cla8[temppos[0]][temppos[1]] = AND5;
	#
	#######################################################
	#
	INV3 = gate();
	INV3.set_name("INV3");
	INV3.set_number(gate_number);
	INV3.set_position(current_x,current_y);
	INV3.add_input("G2", None);
	INV3.add_output("INV3_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = INV3.get_position();
	cla8[temppos[0]][temppos[1]] = INV3;
	#
	#######################################################
	#
	OR3 = gate();
	OR3.set_name("OR3");
	OR3.set_number(gate_number);
	OR3.set_position(current_x,current_y);
	OR3.add_input("A2", None);
	OR3.add_input("B2", None);
	OR3.add_output("P2", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = OR3.get_position();
	cla8[temppos[0]][temppos[1]] = OR3;
	#
	#######################################################
	#
	AND6 = gate();
	AND6.set_name("AND6");
	AND6.set_number(gate_number);
	AND6.set_position(current_x,current_y);
	AND6.add_input("P2", None);
	AND6.add_input("INV3_OUT", None);
	AND6.add_output("AND6_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND6.get_position();
	cla8[temppos[0]][temppos[1]] = AND6;
	#
	#######################################################
	#
	XOR3 = gate();
	XOR3.set_name("XOR3");
	XOR3.set_number(gate_number);
	XOR3.set_position(current_x,current_y);
	XOR3.add_input("C1", None);
	XOR3.add_input("AND6_OUT", None);
	XOR3.add_output("SUM2", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
	#Done with FA, update row
	current_x = current_x + 1;
	temppos = XOR3.get_position();
	cla8[temppos[0]][temppos[1]] = XOR3;
	#
	#######################################################
	
	
	'''REDUCED FULL ADDER 3'''
	
	#######################################################
	#######################################################
	#Sum3, P3, G3##################################################
	AND7 = gate();
	AND7.set_name("AND7");
	AND7.set_number(gate_number);
	AND7.set_position(current_x,current_y);
	AND7.add_input("A3", None);
	AND7.add_input("B3", None);
	AND7.add_output("G3", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND7.get_position();
	cla8[temppos[0]][temppos[1]] = AND7;
	#
	#######################################################
	#
	INV4 = gate();
	INV4.set_name("INV4");
	INV4.set_number(gate_number);
	INV4.set_position(current_x,current_y);
	INV4.add_input("G3", None);
	INV4.add_output("INV4_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = INV4.get_position();
	cla8[temppos[0]][temppos[1]] = INV4;
	#
	#######################################################
	#
	OR4 = gate();
	OR4.set_name("OR4");
	OR4.set_number(gate_number);
	OR4.set_position(current_x,current_y);
	OR4.add_input("A3", None);
	OR4.add_input("B3", None);
	OR4.add_output("P3", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = OR4.get_position();
	cla8[temppos[0]][temppos[1]] = OR4;
	#
	#######################################################
	#
	AND8 = gate();
	AND8.set_name("AND8");
	AND8.set_number(gate_number);
	AND8.set_position(current_x,current_y);
	AND8.add_input("P3", None);
	AND8.add_input("INV4_OUT", None);
	AND8.add_output("AND8_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND8.get_position();
	cla8[temppos[0]][temppos[1]] = AND8;
	#
	#######################################################
	#
	XOR4 = gate();
	XOR4.set_name("XOR4");
	XOR4.set_number(gate_number);
	XOR4.set_position(current_x,current_y);
	XOR4.add_input("C2", None);
	XOR4.add_input("AND8_OUT", None);
	XOR4.add_output("SUM3", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
	#Done with FA, update row
	current_x = current_x + 1;
	temppos = XOR4.get_position();
	cla8[temppos[0]][temppos[1]] = XOR4;
	#
	#######################################################
	
	
	'''REDUCED FULL ADDER 4'''
	
	#######################################################
	#######################################################
	#Sum4, P4, G4##################################################
	AND9 = gate();
	AND9.set_name("AND9");
	AND9.set_number(gate_number);
	AND9.set_position(current_x,current_y);
	AND9.add_input("A4", None);
	AND9.add_input("B4", None);
	AND9.add_output("G4", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND9.get_position();
	cla8[temppos[0]][temppos[1]] = AND9;
	#
	#######################################################
	#
	INV5 = gate();
	INV5.set_name("INV5");
	INV5.set_number(gate_number);
	INV5.set_position(current_x,current_y);
	INV5.add_input("G4", None);
	INV5.add_output("INV5_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = INV5.get_position();
	cla8[temppos[0]][temppos[1]] = INV5;
	#
	#######################################################
	#
	OR5 = gate();
	OR5.set_name("OR5");
	OR5.set_number(gate_number);
	OR5.set_position(current_x,current_y);
	OR5.add_input("A4", None);
	OR5.add_input("B4", None);
	OR5.add_output("P4", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = OR5.get_position();
	cla8[temppos[0]][temppos[1]] = OR5;
	#
	#######################################################
	#
	AND10 = gate();
	AND10.set_name("AND10");
	AND10.set_number(gate_number);
	AND10.set_position(current_x,current_y);
	AND10.add_input("P4", None);
	AND10.add_input("INV5_OUT", None);
	AND10.add_output("AND10_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND10.get_position();
	cla8[temppos[0]][temppos[1]] = AND10;
	#
	#######################################################
	#
	XOR5 = gate();
	XOR5.set_name("XOR5");
	XOR5.set_number(gate_number);
	XOR5.set_position(current_x,current_y);
	XOR5.add_input("C3", None);
	XOR5.add_input("AND10_OUT", None);
	XOR5.add_output("SUM4", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
	#Done with FA, update row
	current_x = current_x + 1;
	temppos = XOR5.get_position();
	cla8[temppos[0]][temppos[1]] = XOR5;
	#
	#######################################################
	
	
	'''REDUCED FULL ADDER 5'''
	
	#######################################################
	#######################################################
	#Sum5, P5, G5##################################################
	AND11 = gate();
	AND11.set_name("AND11");
	AND11.set_number(gate_number);
	AND11.set_position(current_x,current_y);
	AND11.add_input("A5", None);
	AND11.add_input("B5", None);
	AND11.add_output("G5", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND11.get_position();
	cla8[temppos[0]][temppos[1]] = AND11;
	#
	#######################################################
	#
	INV6 = gate();
	INV6.set_name("INV6");
	INV6.set_number(gate_number);
	INV6.set_position(current_x,current_y);
	INV6.add_input("G5", None);
	INV6.add_output("INV6_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = INV6.get_position();
	cla8[temppos[0]][temppos[1]] = INV6;
	#
	#######################################################
	#
	OR6 = gate();
	OR6.set_name("OR6");
	OR6.set_number(gate_number);
	OR6.set_position(current_x,current_y);
	OR6.add_input("A5", None);
	OR6.add_input("B5", None);
	OR6.add_output("P5", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = OR6.get_position();
	cla8[temppos[0]][temppos[1]] = OR6;
	#
	#######################################################
	#
	AND12 = gate();
	AND12.set_name("AND12");
	AND12.set_number(gate_number);
	AND12.set_position(current_x,current_y);
	AND12.add_input("P5", None);
	AND12.add_input("INV6_OUT", None);
	AND12.add_output("AND12_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND12.get_position();
	cla8[temppos[0]][temppos[1]] = AND12;
	#
	#######################################################
	#
	XOR6 = gate();
	XOR6.set_name("XOR6");
	XOR6.set_number(gate_number);
	XOR6.set_position(current_x,current_y);
	XOR6.add_input("C4", None);
	XOR6.add_input("AND12_OUT", None);
	XOR6.add_output("SUM5", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
	#Done with FA, update row
	current_x = current_x + 1;
	temppos = XOR6.get_position();
	cla8[temppos[0]][temppos[1]] = XOR6;
	#
	#######################################################
	
	
	'''REDUCED FULL ADDER 6'''
	
	#######################################################
	#######################################################
	#Sum6, P6, G6##################################################
	AND13 = gate();
	AND13.set_name("AND13");
	AND13.set_number(gate_number);
	AND13.set_position(current_x,current_y);
	AND13.add_input("A6", None);
	AND13.add_input("B6", None);
	AND13.add_output("G6", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND13.get_position();
	cla8[temppos[0]][temppos[1]] = AND13;
	#
	#######################################################
	#
	INV7 = gate();
	INV7.set_name("INV7");
	INV7.set_number(gate_number);
	INV7.set_position(current_x,current_y);
	INV7.add_input("G6", None);
	INV7.add_output("INV7_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = INV7.get_position();
	cla8[temppos[0]][temppos[1]] = INV7;
	#
	#######################################################
	#
	OR7 = gate();
	OR7.set_name("OR7");
	OR7.set_number(gate_number);
	OR7.set_position(current_x,current_y);
	OR7.add_input("A6", None);
	OR7.add_input("B6", None);
	OR7.add_output("P6", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = OR7.get_position();
	cla8[temppos[0]][temppos[1]] = OR7;
	#
	#######################################################
	#
	AND14 = gate();
	AND14.set_name("AND14");
	AND14.set_number(gate_number);
	AND14.set_position(current_x,current_y);
	AND14.add_input("P6", None);
	AND14.add_input("INV7_OUT", None);
	AND14.add_output("AND14_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND14.get_position();
	cla8[temppos[0]][temppos[1]] = AND14;
	#
	#######################################################
	#
	XOR7 = gate();
	XOR7.set_name("XOR7");
	XOR7.set_number(gate_number);
	XOR7.set_position(current_x,current_y);
	XOR7.add_input("C5", None);
	XOR7.add_input("AND14_OUT", None);
	XOR7.add_output("SUM6", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
	#Done with FA, update row
	current_x = current_x + 1;
	temppos = XOR7.get_position();
	cla8[temppos[0]][temppos[1]] = XOR7;
	#
	#######################################################
	
	
	'''FULL ADDER 7'''
	
	
	#######################################################
	#######################################################
	#Sum7##################################################
	XOR8 = gate();
	XOR8.set_name("XOR8");
	XOR8.set_number(gate_number);
	XOR8.set_position(current_x,current_y);
	XOR8.add_input("A7", None);
	XOR8.add_input("B7", None);
	XOR8.add_output("XOR8_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = XOR8.get_position();
	cla8[temppos[0]][temppos[1]] = XOR8;
	#
	#######################################################
	#
	XOR16 = gate();
	XOR16.set_name("XOR9");
	XOR16.set_number(gate_number);
	XOR16.set_position(current_x,current_y);
	XOR16.add_input("C6", None);
	XOR16.add_input("XOR8_OUT", None);
	XOR16.add_output("SUM7", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = XOR16.get_position();
	cla8[temppos[0]][temppos[1]] = XOR16;
	#
	#######################################################
	#######################################################
	#COUT####################################################
	AND15 = gate();
	AND15.set_name("AND15");
	AND15.set_number(gate_number);
	AND15.set_position(current_x,current_y);
	AND15.add_input("A7", None);
	AND15.add_input("B7", None);
	AND15.add_output("AND15_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND15.get_position();
	cla8[temppos[0]][temppos[1]] = AND15;
	#
	#######################################################
	#
	AND16 = gate();
	AND16.set_name("AND16");
	AND16.set_number(gate_number);
	AND16.set_position(current_x,current_y);
	AND16.add_input("B7", None);
	AND16.add_input("C6", None);
	AND16.add_output("AND16_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND16.get_position();
	cla8[temppos[0]][temppos[1]] = AND16;
	#
	#######################################################
	#
	AND17 = gate();
	AND17.set_name("AND17");
	AND17.set_number(gate_number);
	AND17.set_position(current_x,current_y);
	AND17.add_input("C6", None);
	AND17.add_input("A7", None);
	AND17.add_output("AND17_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND17.get_position();
	cla8[temppos[0]][temppos[1]] = AND17;
	#
	#######################################################
	#
	OR8 = gate();
	OR8.set_name("OR8");
	OR8.set_number(gate_number);
	OR8.set_position(current_x,current_y);
	OR8.add_input("AND15_OUT", None);
	OR8.add_input("AND16_OUT", None);
	OR8.add_output("OR8_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = OR8.get_position();
	cla8[temppos[0]][temppos[1]] = OR8;
	#
	#######################################################
	#
	OR9 = gate();
	OR9.set_name("OR9");
	OR9.set_number(gate_number);
	OR9.set_position(current_x,current_y);
	OR9.add_input("OR8_OUT", None);
	OR9.add_input("AND17_OUT", None);
	OR9.add_output("COUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
	#Done with FA, update row
	current_x = current_x + 1;
	temppos = OR9.get_position();
	cla8[temppos[0]][temppos[1]] = OR9;
	#######################################################
	#######################################################
	
	
	##
	#######
	##
	#######
	##
	#######
	##
	
	
	##
	##FIRST CLA LOGIC BLOCK
	##
	#
	##C1#######################################################
	#
	#######################################################
	#
	OR10 = gate();
	OR10.set_name("OR10");
	OR10.set_number(gate_number);
	OR10.set_position(current_x,current_y);
	OR10.add_input("G0", None);
	OR10.add_input("AND18_OUT", None);
	OR10.add_output("C1", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = OR10.get_position();
	cla8[temppos[0]][temppos[1]] = OR10;
	#
	#######################################################
	#
	AND18 = gate();
	AND18.set_name("AND18");
	AND18.set_number(gate_number);
	AND18.set_position(current_x,current_y);
	AND18.add_input("P0", None);
	AND18.add_input("CIN", None);
	AND18.add_output("AND18_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND18.get_position();
	cla8[temppos[0]][temppos[1]] = AND18;
	#
	##C2#######################################################
	#
	#######################################################
	#
	OR11 = gate();
	OR11.set_name("OR11");
	OR11.set_number(gate_number);
	OR11.set_position(current_x,current_y);
	OR11.add_input("G1", None);
	OR11.add_input("AND19_OUT", None);
	OR11.add_output("OR11_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = OR11.get_position();
	cla8[temppos[0]][temppos[1]] = OR11;
	#
	#######################################################
	#
	AND19 = gate();
	AND19.set_name("AND19");
	AND19.set_number(gate_number);
	AND19.set_position(current_x,current_y);
	AND19.add_input("P1", None);
	AND19.add_input("G0", None);
	AND19.add_output("AND19_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND19.get_position();
	cla8[temppos[0]][temppos[1]] = AND19;
	#
	#######################################################
	#
	OR12 = gate();
	OR12.set_name("OR12");
	OR12.set_number(gate_number);
	OR12.set_position(current_x,current_y);
	OR12.add_input("OR11_OUT", None);
	OR12.add_input("AND21_OUT", None);
	OR12.add_output("C2", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = OR12.get_position();
	cla8[temppos[0]][temppos[1]] = OR12;
	#
	#######################################################
	#
	AND20 = gate();
	AND20.set_name("AND20");
	AND20.set_number(gate_number);
	AND20.set_position(current_x,current_y);
	AND20.add_input("P1", None);
	AND20.add_input("P0", None);
	AND20.add_output("AND20_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND20.get_position();
	cla8[temppos[0]][temppos[1]] = AND20;
	#
	#######################################################
	#
	AND21 = gate();
	AND21.set_name("AND21");
	AND21.set_number(gate_number);
	AND21.set_position(current_x,current_y);
	AND21.add_input("C0", None);
	AND21.add_input("AND20_OUT", None);
	AND21.add_output("AND21_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND21.get_position();
	cla8[temppos[0]][temppos[1]] = AND21;
	#
	##C3#######################################################
	#
	#######################################################
	#
	OR13 = gate();
	OR13.set_name("OR13");
	OR13.set_number(gate_number);
	OR13.set_position(current_x,current_y);
	OR13.add_input("G2", None);
	OR13.add_input("AND22_OUT", None);
	OR13.add_output("OR13_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = OR13.get_position();
	cla8[temppos[0]][temppos[1]] = OR13;
	#
	#######################################################
	#
	AND22 = gate();
	AND22.set_name("AND22");
	AND22.set_number(gate_number);
	AND22.set_position(current_x,current_y);
	AND22.add_input("P2", None);
	AND22.add_input("G1", None);
	AND22.add_output("AND22_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND22.get_position();
	cla8[temppos[0]][temppos[1]] = AND22;
	#
	#######################################################
	#
	OR14 = gate();
	OR14.set_name("OR14");
	OR14.set_number(gate_number);
	OR14.set_position(current_x,current_y);
	OR14.add_input("OR13_OUT", None);
	OR14.add_input("AND24_OUT", None);
	OR14.add_output("OR14_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = OR14.get_position();
	cla8[temppos[0]][temppos[1]] = OR14;
	#
	#######################################################
	#
	AND23 = gate();
	AND23.set_name("AND23");
	AND23.set_number(gate_number);
	AND23.set_position(current_x,current_y);
	AND23.add_input("P2", None);
	AND23.add_input("P1", None);
	AND23.add_output("AND23_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND23.get_position();
	cla8[temppos[0]][temppos[1]] = AND23;
	#
	#######################################################
	#
	AND24 = gate();
	AND24.set_name("AND24");
	AND24.set_number(gate_number);
	AND24.set_position(current_x,current_y);
	AND24.add_input("AND23_OUT", None);
	AND24.add_input("G0", None);
	AND24.add_output("AND24_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND24.get_position();
	cla8[temppos[0]][temppos[1]] = AND24;
	#
	#######################################################
	#
	OR15 = gate();
	OR15.set_name("OR15");
	OR15.set_number(gate_number);
	OR15.set_position(current_x,current_y);
	OR15.add_input("OR14_OUT", None);
	OR15.add_input("AND27_OUT", None);
	OR15.add_output("C3", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = OR15.get_position();
	cla8[temppos[0]][temppos[1]] = OR15;
	#
	#######################################################
	#
	AND25 = gate();
	AND25.set_name("AND25");
	AND25.set_number(gate_number);
	AND25.set_position(current_x,current_y);
	AND25.add_input("P2", None);
	AND25.add_input("P3", None);
	AND25.add_output("AND25_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND25.get_position();
	cla8[temppos[0]][temppos[1]] = AND25;
	#
	#######################################################
	#
	AND26 = gate();
	AND26.set_name("AND26");
	AND26.set_number(gate_number);
	AND26.set_position(current_x,current_y);
	AND26.add_input("P0", None);
	AND26.add_input("C0", None);
	AND26.add_output("AND26_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND26.get_position();
	cla8[temppos[0]][temppos[1]] = AND26;
	#
	#######################################################
	#
	AND27 = gate();
	AND27.set_name("AND27");
	AND27.set_number(gate_number);
	AND27.set_position(current_x,current_y);
	AND27.add_input("AND25_OUT", None);
	AND27.add_input("AND26_OUT", None);
	AND27.add_output("AND27_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND27.get_position();
	cla8[temppos[0]][temppos[1]] = AND27;
	#
	####P3:0#################################################
	#
	AND28 = gate();
	AND28.set_name("AND28");
	AND28.set_number(gate_number);
	AND28.set_position(current_x,current_y);
	AND28.add_input("P3", None);
	AND28.add_input("P2", None);
	AND28.add_output("AND28_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND28.get_position();
	cla8[temppos[0]][temppos[1]] = AND28;
	#
	######################################################
	#
	AND29 = gate();
	AND29.set_name("AND29");
	AND29.set_number(gate_number);
	AND29.set_position(current_x,current_y);
	AND29.add_input("P1", None);
	AND29.add_input("P0", None);
	AND29.add_output("AND29_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND29.get_position();
	cla8[temppos[0]][temppos[1]] = AND29;
	#
	######################################################
	#
	AND30 = gate();
	AND30.set_name("AND30");
	AND30.set_number(gate_number);
	AND30.set_position(current_x,current_y);
	AND30.add_input("AND28_OUT", None);
	AND30.add_input("AND29_OUT", None);
	AND30.add_output("P30_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
	current_x = current_x + 1;
	temppos = AND30.get_position();
	cla8[temppos[0]][temppos[1]] = AND30;
	#
	######################################################
	#
	#
	####G3:0#################################################
	#
	OR16 = gate();
	OR16.set_name("OR16");
	OR16.set_number(gate_number);
	OR16.set_position(current_x,current_y);
	OR16.add_input("G3", None);
	OR16.add_input("AND31_OUT", None);
	OR16.add_output("OR16_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = OR16.get_position();
	cla8[temppos[0]][temppos[1]] = OR16;
	#
	#######################################################
	#
	AND31 = gate();
	AND31.set_name("AND31");
	AND31.set_number(gate_number);
	AND31.set_position(current_x,current_y);
	AND31.add_input("P3", None);
	AND31.add_input("G2", None);
	AND31.add_output("AND31_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND31.get_position();
	cla8[temppos[0]][temppos[1]] = AND31;
	#
	#######################################################
	#
	OR17 = gate();
	OR17.set_name("OR17");
	OR17.set_number(gate_number);
	OR17.set_position(current_x,current_y);
	OR17.add_input("OR16_OUT", None);
	OR17.add_input("AND33_OUT", None);
	OR17.add_output("OR17_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = OR17.get_position();
	cla8[temppos[0]][temppos[1]] = OR17;
	#
	#######################################################
	#
	AND32 = gate();
	AND32.set_name("AND32");
	AND32.set_number(gate_number);
	AND32.set_position(current_x,current_y);
	AND32.add_input("P3", None);
	AND32.add_input("P2", None);
	AND32.add_output("AND32_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND32.get_position();
	cla8[temppos[0]][temppos[1]] = AND32;
	#
	#######################################################
	#
	AND33 = gate();
	AND33.set_name("AND33");
	AND33.set_number(gate_number);
	AND33.set_position(current_x,current_y);
	AND33.add_input("AND32_OUT", None);
	AND33.add_input("G1", None);
	AND33.add_output("AND33_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND33.get_position();
	cla8[temppos[0]][temppos[1]] = AND33;
	#
	#######################################################
	#
	OR18 = gate();
	OR18.set_name("OR18");
	OR18.set_number(gate_number);
	OR18.set_position(current_x,current_y);
	OR18.add_input("OR17_OUT", None);
	OR18.add_input("AND36_OUT", None);
	OR18.add_output("G30_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = OR18.get_position();
	cla8[temppos[0]][temppos[1]] = OR18;
	#
	#######################################################
	#
	AND34 = gate();
	AND34.set_name("AND34");
	AND34.set_number(gate_number);
	AND34.set_position(current_x,current_y);
	AND34.add_input("P2", None);
	AND34.add_input("P3", None);
	AND34.add_output("AND34_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND34.get_position();
	cla8[temppos[0]][temppos[1]] = AND34;
	#
	#######################################################
	#
	AND35 = gate();
	AND35.set_name("AND35");
	AND35.set_number(gate_number);
	AND35.set_position(current_x,current_y);
	AND35.add_input("G0", None);
	AND35.add_input("P1", None);
	AND35.add_output("AND35_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND35.get_position();
	cla8[temppos[0]][temppos[1]] = AND35;
	#
	#######################################################
	#
	AND36 = gate();
	AND36.set_name("AND36");
	AND36.set_number(gate_number);
	AND36.set_position(current_x,current_y);
	AND36.add_input("AND34_OUT", None);
	AND36.add_input("AND35_OUT", None);
	AND36.add_output("AND36_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
	current_x = current_x + 1;
	temppos = AND36.get_position();
	cla8[temppos[0]][temppos[1]] = AND36;
	
	##
	######
	##
	######
	##
	######
	##
	
	##
	##SECOND CLA LOGIC BLOCK
	##
	#
	##C4#######################################################
	#
	#######################################################
	#
	OR19 = gate();
	OR19.set_name("OR19");
	OR19.set_number(gate_number);
	OR19.set_position(current_x,current_y);
	OR19.add_input("G30_OUT", None);
	OR19.add_input("AND37_OUT", None);
	OR19.add_output("C4", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = OR19.get_position();
	cla8[temppos[0]][temppos[1]] = OR19;
	#
	#######################################################
	#
	AND37 = gate();
	AND37.set_name("AND37");
	AND37.set_number(gate_number);
	AND37.set_position(current_x,current_y);
	AND37.add_input("P30_OUT", None);
	AND37.add_input("C0", None);
	AND37.add_output("AND37_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND37.get_position();
	cla8[temppos[0]][temppos[1]] = AND37;
	#
	##C5#######################################################
	#
	#######################################################
	#
	OR20 = gate();
	OR20.set_name("OR20");
	OR20.set_number(gate_number);
	OR20.set_position(current_x,current_y);
	OR20.add_input("G4", None);
	OR20.add_input("AND38_OUT", None);
	OR20.add_output("OR20_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = OR20.get_position();
	cla8[temppos[0]][temppos[1]] = OR20;
	#
	#######################################################
	#
	AND38 = gate();
	AND38.set_name("AND38");
	AND38.set_number(gate_number);
	AND38.set_position(current_x,current_y);
	AND38.add_input("P4", None);
	AND38.add_input("G30_OUT", None);
	AND38.add_output("AND38_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND38.get_position();
	cla8[temppos[0]][temppos[1]] = AND38;
	#
	#######################################################
	#
	OR21 = gate();
	OR21.set_name("OR21");
	OR21.set_number(gate_number);
	OR21.set_position(current_x,current_y);
	OR21.add_input("OR20_OUT", None);
	OR21.add_input("AND40_OUT", None);
	OR21.add_output("C5", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = OR21.get_position();
	cla8[temppos[0]][temppos[1]] = OR21;
	#
	#######################################################
	#
	AND39 = gate();
	AND39.set_name("AND39");
	AND39.set_number(gate_number);
	AND39.set_position(current_x,current_y);
	AND39.add_input("P4", None);
	AND39.add_input("P30_OUT", None);
	AND39.add_output("AND39_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND39.get_position();
	cla8[temppos[0]][temppos[1]] = AND39;
	#
	#######################################################
	#
	AND40 = gate();
	AND40.set_name("AND40");
	AND40.set_number(gate_number);
	AND40.set_position(current_x,current_y);
	AND40.add_input("AND39_OUT", None);
	AND40.add_input("C0", None);
	AND40.add_output("AND40_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND40.get_position();
	cla8[temppos[0]][temppos[1]] = AND40;
	#
	##C3#######################################################
	#
	#######################################################
	#
	OR22 = gate();
	OR22.set_name("OR22");
	OR22.set_number(gate_number);
	OR22.set_position(current_x,current_y);
	OR22.add_input("G5", None);
	OR22.add_input("AND41_OUT", None);
	OR22.add_output("OR22_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = OR9.get_position();
	cla8[temppos[0]][temppos[1]] = OR9;
	#
	#######################################################
	#
	AND41 = gate();
	AND41.set_name("AND41");
	AND41.set_number(gate_number);
	AND41.set_position(current_x,current_y);
	AND41.add_input("P5", None);
	AND41.add_input("G4", None);
	AND41.add_output("AND41_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND41.get_position();
	cla8[temppos[0]][temppos[1]] = AND41;
	#
	#######################################################
	#
	OR23 = gate();
	OR23.set_name("OR23");
	OR23.set_number(gate_number);
	OR23.set_position(current_x,current_y);
	OR23.add_input("OR22_OUT", None);
	OR23.add_input("AND43_OUT", None);
	OR23.add_output("OR23_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = OR23.get_position();
	cla8[temppos[0]][temppos[1]] = OR23;
	#
	#######################################################
	#
	AND42 = gate();
	AND42.set_name("AND42");
	AND42.set_number(gate_number);
	AND42.set_position(current_x,current_y);
	AND42.add_input("P5", None);
	AND42.add_input("P4", None);
	AND42.add_output("AND42_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND42.get_position();
	cla8[temppos[0]][temppos[1]] = AND42;
	#
	#######################################################
	#
	AND43 = gate();
	AND43.set_name("AND43");
	AND43.set_number(gate_number);
	AND43.set_position(current_x,current_y);
	AND43.add_input("G30_OUT", None);
	AND43.add_input("AND42_OUT", None);
	AND43.add_output("AND43_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND43.get_position();
	cla8[temppos[0]][temppos[1]] = AND43;
	#
	#######################################################
	#
	OR24 = gate();
	OR24.set_name("OR24");
	OR24.set_number(gate_number);
	OR24.set_position(current_x,current_y);
	OR24.add_input("OR23_OUT", None);
	OR24.add_input("AND46_OUT", None);
	OR24.add_output("C6", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = OR24.get_position();
	cla8[temppos[0]][temppos[1]] = OR24;
	#
	#######################################################
	#
	AND44 = gate();
	AND44.set_name("AND44");
	AND44.set_number(gate_number);
	AND44.set_position(current_x,current_y);
	AND44.add_input("P30_OUT", None);
	AND44.add_input("C0", None);
	AND44.add_output("AND44_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND44.get_position();
	cla8[temppos[0]][temppos[1]] = AND44;
	#
	#######################################################
	#
	AND45 = gate();
	AND45.set_name("AND45");
	AND45.set_number(gate_number);
	AND45.set_position(current_x,current_y);
	AND45.add_input("P5", None);
	AND45.add_input("P4", None);
	AND45.add_output("AND45_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND45.get_position();
	cla8[temppos[0]][temppos[1]] = AND45;
	#
	#####################################################
	#
	AND46 = gate();
	AND46.set_name("AND46");
	AND46.set_number(gate_number);
	AND46.set_position(current_x,current_y);
	AND46.add_input("AND44_OUT", None);
	AND46.add_input("AND45_OUT", None);
	AND46.add_output("AND46_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
	current_x = current_x + 1;
	temppos = AND46.get_position();
	cla8[temppos[0]][temppos[1]] = AND46;
	#
	######################################################
	#
	
	
	
	
	print("CLAs placed cell grid: ");
	print(cla8);
	#get placed gate count - sanity checking grid for duplicates and misplaced gates
	#there could still be typos - just fyi
	placed_count = 0;
	duplicate_gate_count = 0;
	for i in range(len(cla8)):
	
		for j in range(len(cla8[i])):
		
			if(cla8[i][j] != None):
				placed_count = placed_count + 1;
				##UNCOMMENT FOR GATE INFO
				#cla8[i][j].get_info();
				
			#Performing list check for inputs and outputs
			
			for k in range(len(cla8)):
			
				for l in range(len(cla8[k])):
				
					if(cla8[i][j] != None and cla8[k][l] != None and (i != k and j != l)):
							gate1_in = str(cla8[i][j].inputs);
							gate2_in = str(cla8[k][l].inputs);
							
							gate1_out = str(cla8[i][j].outputs);
							gate2_out = str(cla8[k][l].outputs);
							
							if(gate1_in == gate2_in and gate1_out == gate2_out):
								cla8[i][j].get_info();
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

	make_cla8();
	
main();	