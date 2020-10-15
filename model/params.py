#!/usr/bin/env python3

import math

# hyper-parameters
# 4 currently implemented

SWITCH_NUMBER_OF = 6
ALPHA = 0.1
GRID_SQ_SIZE = 1
OPEN_CIRCUIT_K = 10
CONGESTION_FACTOR = OPEN_CIRCUIT_K*GRID_SQ_SIZE
CONGESTION_FUNCTION = lambda x: CONGESTION_FUNCTION*(exp(x)-1)

# short-hand

SN = SWITCH_NUMBER_OF
GSQ = GRID_SQ_SIZE
OCK = OPEN_CIRCUIT_K
CF = CONGESTION_FUNCTION


# tech parameters
# in the future these should be automatically read from LEF/DEF maybe

MAX_METAL = 5
METAL_IMPEDANCE = [-1,3,2,2,1,1]
TRACK_SCALING_FACTOR = GRID_SQ_SIZE/1.0
MAX_TRACKS = [int(TRACK_SCALING_FACTOR/x) for x in [-1,0.25,0.25,0.5,0.5,1]]

GRID_X = 10
GRID_Y = 10

# short-hand

MM = MAX_METAL
MI = METAL_IMPEDANCE
GX = GRID_X
GY = GRID_Y
MT = MAX_TRACKS
