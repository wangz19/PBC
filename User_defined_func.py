# this is user defined function specially for periodicBC.py currently 20160303
import numpy as np

# function calculate distance between two node in given node list
# def distance( node list with nodeID and x,y,z, nodeID_1, nodeID_2):
def distance( node_cell, nodeID_1, nodeID_2):
	# assuming the nodeID is arranged sequencially in the node-list
	x1 = node_cell[nodeID_1-1][1]
	y1 = node_cell[nodeID_1-1][2]
	z1 = node_cell[nodeID_1-1][3]
	x2 = node_cell[nodeID_2-1][1]
	y2 = node_cell[nodeID_2-1][2]
	z2 = node_cell[nodeID_2-1][3]

	d = np.sqrt((x1-x2)**2+(y1-y2)**2+(z1-z2)**2)
	return d

