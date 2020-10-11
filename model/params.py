#!/usr/bin/env python3

# hyper-parameters
# 4 currently implemented

SWITCH_MAX = 6
ALPHA = 0.1
GRID_SQ_SIZE = 1
OPEN_CIRCUIT_K = 10

# short-hand

SM = SWITCH_MAX
GSQ = GRID_SQ_SIZE
OCK = OPEN_CIRCUIT_K


# tech parameters
# in the future these should be automatically read from LEF/DEF maybe

MAX_METAL = 5
METAL_IMPEDANCE = [3,2,2,1,1]

GRID_X = 100
GRID_Y = 100

# short-hand

MM = MAX_METAL
MI = METAL_IMPEDANCE
GX = GRID_X
GY = GRID_Y
