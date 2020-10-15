#!/usr/bin/env python3

import sys
import math
sys.path.append("..")

from model import params
from gates import *

#RCA datapath is literally just 8 full adders in series
def make_rca8():

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
	grid_x = 50;
	
	#creating a grid data structure with the dimsions specified in params
	#not using a dictionary because order is important for routing - fight me
	rca8 = [[None for i in range(grid_y)] for i in range(grid_x)];
	
	#bookkeeping
	gate_number = 1;
	max_y = 6;
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
	rca8[temppos[0]][temppos[1]] = XOR1;
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
	rca8[temppos[0]][temppos[1]] = XOR2;
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
	rca8[temppos[0]][temppos[1]] = AND1;
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
	rca8[temppos[0]][temppos[1]] = AND2;
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
	rca8[temppos[0]][temppos[1]] = AND3;
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
	rca8[temppos[0]][temppos[1]] = OR1;
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
	rca8[temppos[0]][temppos[1]] = OR2;
	#######################################################
	#######################################################
	
	'''FULL ADDER 1'''
	
	
	#######################################################
	#######################################################
	#Sum1##################################################
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
	rca8[temppos[0]][temppos[1]] = XOR3;
	#
	#######################################################
	#
	XOR4 = gate();
	XOR4.set_name("XOR4");
	XOR4.set_number(gate_number);
	XOR4.set_position(current_x,current_y);
	XOR4.add_input("C0", None);
	XOR4.add_input("XOR3_OUT", None);
	XOR4.add_output("SUM1", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = XOR4.get_position();
	rca8[temppos[0]][temppos[1]] = XOR4;
	#
	#######################################################
	#######################################################
	#C1####################################################
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
	rca8[temppos[0]][temppos[1]] = AND4;
	#
	#######################################################
	#
	AND5 = gate();
	AND5.set_name("AND5");
	AND5.set_number(gate_number);
	AND5.set_position(current_x,current_y);
	AND5.add_input("B1", None);
	AND5.add_input("C0", None);
	AND5.add_output("AND5_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND5.get_position();
	rca8[temppos[0]][temppos[1]] = AND5;
	#
	#######################################################
	#
	AND6 = gate();
	AND6.set_name("AND6");
	AND6.set_number(gate_number);
	AND6.set_position(current_x,current_y);
	AND6.add_input("C0", None);
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
	rca8[temppos[0]][temppos[1]] = AND6;
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
	rca8[temppos[0]][temppos[1]] = OR3;
	#
	#######################################################
	#
	OR4 = gate();
	OR4.set_name("OR4");
	OR4.set_number(gate_number);
	OR4.set_position(current_x,current_y);
	OR4.add_input("OR3_OUT", None);
	OR4.add_input("AND6_OUT", None);
	OR4.add_output("C1", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
	#Done with FA, update row
	current_x = current_x + 1;
	temppos = OR4.get_position();
	rca8[temppos[0]][temppos[1]] = OR4;
	#######################################################
	#######################################################
	
	'''FULL ADDER 2'''
	
	
	#######################################################
	#######################################################
	#Sum2##################################################
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
	rca8[temppos[0]][temppos[1]] = XOR5;
	#
	#######################################################
	#
	XOR6 = gate();
	XOR6.set_name("XOR6");
	XOR6.set_number(gate_number);
	XOR6.set_position(current_x,current_y);
	XOR6.add_input("C1", None);
	XOR6.add_input("XOR5_OUT", None);
	XOR6.add_output("SUM2", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = XOR6.get_position();
	rca8[temppos[0]][temppos[1]] = XOR6;
	#
	#######################################################
	#######################################################
	#C2####################################################
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
	rca8[temppos[0]][temppos[1]] = AND7;
	#
	#######################################################
	#
	AND8 = gate();
	AND8.set_name("AND8");
	AND8.set_number(gate_number);
	AND8.set_position(current_x,current_y);
	AND8.add_input("B2", None);
	AND8.add_input("C1", None);
	AND8.add_output("AND8_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND8.get_position();
	rca8[temppos[0]][temppos[1]] = AND8;
	#
	#######################################################
	#
	AND9 = gate();
	AND9.set_name("AND9");
	AND9.set_number(gate_number);
	AND9.set_position(current_x,current_y);
	AND9.add_input("C1", None);
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
	rca8[temppos[0]][temppos[1]] = AND9;
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
	rca8[temppos[0]][temppos[1]] = OR5;
	#
	#######################################################
	#
	OR6 = gate();
	OR6.set_name("OR6");
	OR6.set_number(gate_number);
	OR6.set_position(current_x,current_y);
	OR6.add_input("OR5_OUT", None);
	OR6.add_input("AND9_OUT", None);
	OR6.add_output("C2", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
	#Done with FA, update row
	current_x = current_x + 1;
	temppos = OR6.get_position();
	rca8[temppos[0]][temppos[1]] = OR6;
	#######################################################
	#######################################################
	
	'''FULL ADDER 3'''
	
	
	#######################################################
	#######################################################
	#Sum3##################################################
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
	rca8[temppos[0]][temppos[1]] = XOR7;
	#
	#######################################################
	#
	XOR8 = gate();
	XOR8.set_name("XOR8");
	XOR8.set_number(gate_number);
	XOR8.set_position(current_x,current_y);
	XOR8.add_input("C2", None);
	XOR8.add_input("XOR8_OUT", None);
	XOR8.add_output("SUM3", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = XOR8.get_position();
	rca8[temppos[0]][temppos[1]] = XOR8;
	#
	#######################################################
	#######################################################
	#C3####################################################
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
	rca8[temppos[0]][temppos[1]] = AND10;
	#
	#######################################################
	#
	AND11 = gate();
	AND11.set_name("AND11");
	AND11.set_number(gate_number);
	AND11.set_position(current_x,current_y);
	AND11.add_input("B3", None);
	AND11.add_input("C2", None);
	AND11.add_output("AND11_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND11.get_position();
	rca8[temppos[0]][temppos[1]] = AND11;
	#
	#######################################################
	#
	AND12 = gate();
	AND12.set_name("AND12");
	AND12.set_number(gate_number);
	AND12.set_position(current_x,current_y);
	AND12.add_input("C2", None);
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
	rca8[temppos[0]][temppos[1]] = AND12;
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
	rca8[temppos[0]][temppos[1]] = OR7;
	#
	#######################################################
	#
	OR8 = gate();
	OR8.set_name("OR6");
	OR8.set_number(gate_number);
	OR8.set_position(current_x,current_y);
	OR8.add_input("OR7_OUT", None);
	OR8.add_input("AND12_OUT", None);
	OR8.add_output("C3", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
	#Done with FA, update row
	current_x = current_x + 1;
	temppos = OR8.get_position();
	rca8[temppos[0]][temppos[1]] = OR8;
	#######################################################
	#######################################################
	
	'''FULL ADDER 4'''
	
	
	#######################################################
	#######################################################
	#Sum4##################################################
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
	rca8[temppos[0]][temppos[1]] = XOR9;
	#
	#######################################################
	#
	XOR10 = gate();
	XOR10.set_name("XOR10");
	XOR10.set_number(gate_number);
	XOR10.set_position(current_x,current_y);
	XOR10.add_input("C3", None);
	XOR10.add_input("XOR10_OUT", None);
	XOR10.add_output("SUM4", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = XOR10.get_position();
	rca8[temppos[0]][temppos[1]] = XOR10;
	#
	#######################################################
	#######################################################
	#C4####################################################
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
	rca8[temppos[0]][temppos[1]] = AND13;
	#
	#######################################################
	#
	AND14 = gate();
	AND14.set_name("AND14");
	AND14.set_number(gate_number);
	AND14.set_position(current_x,current_y);
	AND14.add_input("B4", None);
	AND14.add_input("C3", None);
	AND14.add_output("AND14_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND14.get_position();
	rca8[temppos[0]][temppos[1]] = AND14;
	#
	#######################################################
	#
	AND15 = gate();
	AND15.set_name("AND15");
	AND15.set_number(gate_number);
	AND15.set_position(current_x,current_y);
	AND15.add_input("C3", None);
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
	rca8[temppos[0]][temppos[1]] = AND15;
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
	rca8[temppos[0]][temppos[1]] = OR9;
	#
	#######################################################
	#
	OR10 = gate();
	OR10.set_name("OR10");
	OR10.set_number(gate_number);
	OR10.set_position(current_x,current_y);
	OR10.add_input("OR9_OUT", None);
	OR10.add_input("AND15_OUT", None);
	OR10.add_output("C4", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
	#Done with FA, update row
	current_x = current_x + 1;
	temppos = OR10.get_position();
	rca8[temppos[0]][temppos[1]] = OR10;
	#######################################################
	#######################################################
	
	
	'''FULL ADDER 5'''
	
	
	#######################################################
	#######################################################
	#Sum5##################################################
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
	rca8[temppos[0]][temppos[1]] = XOR11;
	#
	#######################################################
	#
	XOR12 = gate();
	XOR12.set_name("XOR12");
	XOR12.set_number(gate_number);
	XOR12.set_position(current_x,current_y);
	XOR12.add_input("C4", None);
	XOR12.add_input("XOR11_OUT", None);
	XOR12.add_output("SUM5", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = XOR12.get_position();
	rca8[temppos[0]][temppos[1]] = XOR12;
	#
	#######################################################
	#######################################################
	#C5####################################################
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
	rca8[temppos[0]][temppos[1]] = AND16;
	#
	#######################################################
	#
	AND17 = gate();
	AND17.set_name("AND17");
	AND17.set_number(gate_number);
	AND17.set_position(current_x,current_y);
	AND17.add_input("B5", None);
	AND17.add_input("C4", None);
	AND17.add_output("AND17_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND17.get_position();
	rca8[temppos[0]][temppos[1]] = AND17;
	#
	#######################################################
	#
	AND18 = gate();
	AND18.set_name("AND18");
	AND18.set_number(gate_number);
	AND18.set_position(current_x,current_y);
	AND18.add_input("C4", None);
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
	rca8[temppos[0]][temppos[1]] = AND18;
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
	rca8[temppos[0]][temppos[1]] = OR11;
	#
	#######################################################
	#
	OR12 = gate();
	OR12.set_name("OR12");
	OR12.set_number(gate_number);
	OR12.set_position(current_x,current_y);
	OR12.add_input("OR11_OUT", None);
	OR12.add_input("AND18_OUT", None);
	OR12.add_output("C5", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
	#Done with FA, update row
	current_x = current_x + 1;
	temppos = OR12.get_position();
	rca8[temppos[0]][temppos[1]] = OR12;
	#######################################################
	#######################################################
	
	'''FULL ADDER 6'''
	
	
	#######################################################
	#######################################################
	#Sum6##################################################
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
	rca8[temppos[0]][temppos[1]] = XOR13;
	#
	#######################################################
	#
	XOR14 = gate();
	XOR14.set_name("XOR14");
	XOR14.set_number(gate_number);
	XOR14.set_position(current_x,current_y);
	XOR14.add_input("C5", None);
	XOR14.add_input("XOR13_OUT", None);
	XOR14.add_output("SUM6", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = XOR14.get_position();
	rca8[temppos[0]][temppos[1]] = XOR14;
	#
	#######################################################
	#######################################################
	#C6####################################################
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
	rca8[temppos[0]][temppos[1]] = AND19;
	#
	#######################################################
	#
	AND20 = gate();
	AND20.set_name("AND20");
	AND20.set_number(gate_number);
	AND20.set_position(current_x,current_y);
	AND20.add_input("B6", None);
	AND20.add_input("C5", None);
	AND20.add_output("AND20_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND20.get_position();
	rca8[temppos[0]][temppos[1]] = AND20;
	#
	#######################################################
	#
	AND21 = gate();
	AND21.set_name("AND21");
	AND21.set_number(gate_number);
	AND21.set_position(current_x,current_y);
	AND21.add_input("C5", None);
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
	rca8[temppos[0]][temppos[1]] = AND21;
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
	rca8[temppos[0]][temppos[1]] = OR13;
	#
	#######################################################
	#
	OR14 = gate();
	OR14.set_name("OR14");
	OR14.set_number(gate_number);
	OR14.set_position(current_x,current_y);
	OR14.add_input("OR13_OUT", None);
	OR14.add_input("AND21_OUT", None);
	OR14.add_output("C6", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
	#Done with FA, update row
	current_x = current_x + 1;
	temppos = OR14.get_position();
	rca8[temppos[0]][temppos[1]] = OR14;
	#######################################################
	#######################################################
	
	'''FULL ADDER 7'''
	
	
	#######################################################
	#######################################################
	#Sum7##################################################
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
	rca8[temppos[0]][temppos[1]] = XOR15;
	#
	#######################################################
	#
	XOR16 = gate();
	XOR16.set_name("XOR16");
	XOR16.set_number(gate_number);
	XOR16.set_position(current_x,current_y);
	XOR16.add_input("C6", None);
	XOR16.add_input("XOR15_OUT", None);
	XOR16.add_output("SUM7", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = XOR16.get_position();
	rca8[temppos[0]][temppos[1]] = XOR16;
	#
	#######################################################
	#######################################################
	#COUT####################################################
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
	rca8[temppos[0]][temppos[1]] = AND22;
	#
	#######################################################
	#
	AND23 = gate();
	AND23.set_name("AND23");
	AND23.set_number(gate_number);
	AND23.set_position(current_x,current_y);
	AND23.add_input("B7", None);
	AND23.add_input("C6", None);
	AND23.add_output("AND23_OUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
		current_x = current_x + 1;
	temppos = AND23.get_position();
	rca8[temppos[0]][temppos[1]] = AND23;
	#
	#######################################################
	#
	AND24 = gate();
	AND24.set_name("AND24");
	AND24.set_number(gate_number);
	AND24.set_position(current_x,current_y);
	AND24.add_input("C6", None);
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
	rca8[temppos[0]][temppos[1]] = AND24;
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
	rca8[temppos[0]][temppos[1]] = OR15;
	#
	#######################################################
	#
	OR16 = gate();
	OR16.set_name("OR16");
	OR16.set_number(gate_number);
	OR16.set_position(current_x,current_y);
	OR16.add_input("OR15_OUT", None);
	OR16.add_input("AND24_OUT", None);
	OR16.add_output("COUT", None);
	#update positions
	gate_number = gate_number + 1;
	if(current_y < max_y):
		current_y = current_y + 2;
	else:
		current_y = (current_x + 1) % 2;
	#Done with FA, update row
	current_x = current_x + 1;
	temppos = OR16.get_position();
	rca8[temppos[0]][temppos[1]] = OR16;
	#######################################################
	#######################################################
	
	print("RCA placed cell grid: ");
	print(rca8);
	#get placed gate count - sanity checking grid for duplicates and misplaced gates
	#there could still be typos - just fyi
	placed_count = 0;
	duplicate_gate_count = 0;
	for i in range(len(rca8)):
	
		for j in range(len(rca8[i])):
		
			if(rca8[i][j] != None):
				placed_count = placed_count + 1;
				##UNCOMMENT FOR GATE INFO
				#rca8[i][j].get_info();
				
			#Performing list check for inputs and outputs
			
			for k in range(len(rca8)):
			
				for l in range(len(rca8[k])):
				
					if(rca8[i][j] != None and rca8[k][l] != None and (i != k and j != l)):
							gate1_in = str(rca8[i][j].inputs);
							gate2_in = str(rca8[k][l].inputs);
							
							gate1_out = str(rca8[i][j].outputs);
							gate2_out = str(rca8[k][l].outputs);
							
							if(gate1_in == gate2_in and gate1_out == gate2_out):
								rca8[i][j].get_info();
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

	make_rca8();
	
main();	
