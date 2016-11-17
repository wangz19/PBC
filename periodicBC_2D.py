import numpy as np
import matplotlib.pyplot as plt
import re
import os
os.chdir(r"Z:\\Users\\zehaiwang\\GitHub\Periodical_BC")   #change to function directory to souce macro_modeing
from User_defined_func import * # import all the user_defined functions


#default
Assembly_name = 'Part-1-1'
model_name    = 'Model-1'
#customized
# Assembly_name ='Bone_mesh-1'

# module abbreviation
m=mdb.models[model_name]
r=m.rootAssembly
node=r.instances[Assembly_name].nodes

#ne 存储所有边界上的单元节点的编号 node ID on the edge
node_left=[] #node on the back boundary surface x_min
node_right=[] #node on the right boundary surface x_max
node_down=[] # node on the left boundary surface y_min
node_up=[] #node on the right boundary surface y_max
vertices = []  # nodes on the vertices

#reformat the node id, x, y, z postion in an Nx4 array
# as shown          1, 0, 0, 0
node_cell =np.zeros((len(node),4)) 
for i in range(len(node)):
    node_cell[i][1]=node[i].coordinates[0]  # x value
    node_cell[i][2]=node[i].coordinates[1]  # y value
    node_cell[i][3]=node[i].coordinates[2]  # z value
    node_cell[i][0]=node[i].label

print node_cell

# determine the surface position in character coordinates
# incase of rectangular model aligned with the global coordinate
x_min, x_max = np.min(node_cell[:,1]), np.max(node_cell[:,1])
y_min, y_max = np.min(node_cell[:,2]), np.max(node_cell[:,2])
# z_min, z_max = np.min(node_cell[:,3]),  np.max(node_cell[:,3])

# find boundary
for i in range(len(node_cell[:,0])):
    if abs(node_cell[i][1]-x_min)<0.001:            # back surface
        node_left.append(node_cell[i][0])
    if abs(node_cell[i][1]-x_max)<0.001:          #front surface
        node_right.append(node_cell[i][0])
    if abs(node_cell[i][2]-y_min)<0.001:          #left surface
        node_down.append(node_cell[i][0])
    if abs(node_cell[i][2]-y_max)<0.001:          #right surface
        node_up.append(node_cell[i][0])
# print node_down
# print node_up

# find vortecies label ## intersection of lists
# V_lowerLeft : V1  # V_lowerRight : V2  # V_upperRight : V3 # V_upperLeft : V4
V1 = np.intersect1d (node_down, node_left)
V2 = np.intersect1d (node_down, node_right)
V3 = np.intersect1d (node_up, node_right)
V4 = np.intersect1d (node_up, node_left)
vertices.append(V1)
vertices.append(V2)
vertices.append(V3)
vertices.append(V4)


r.Set(nodes=node[int(V1[0])-1:int(V1[0])], name ='set_downLeft')
r.Set(nodes=node[int(V2[0])-1:int(V2[0])], name ='set_downRight')
r.Set(nodes=node[int(V3[0])-1:int(V3[0])], name ='set_upperRight')
r.Set(nodes=node[int(V4[0])-1:int(V4[0])], name ='set_upperLeft')

# exclude vertices from boundary
node_down = np.setdiff1d(np.array(node_down),np.array(vertices))
node_up = np.setdiff1d(np.array(node_up),np.array(vertices))
node_left= np.setdiff1d(np.array(node_left),np.array(vertices))
node_right = np.setdiff1d(np.array(node_right),np.array(vertices))


def PBC_constrain (node_cell,node_set_1,node_set_2, vortex_1, vortex_2, coefficient_1,coefficient_2, coefficient_3, coefficient_4, dof_1,dof_2,dof_3,set_name):
    # pairing nodes in two opposite surface
    # where the node number on the two face need not to be equal
    # number of pair depend on the min node of the two surface
    # m=mdb.models['Model-1']
    # r=m.rootAssembly
    # node=r.instances['Part-1-1'].nodes
    # pair_num = min(len(node_left),len(node_right))
    # print pair_num
    pair = []    #temp position for front and back surface
    for x in node_set_1:
        mindist     = float("inf")  #initialize distance as inf large
        for y in node_set_2:
            dist = distance(node_cell, x, y)
            if dist< mindist:
                mindist     = dist  
                nearestpair = (int(x),int(y))   # convert float node label into int for future reference
        pair.append(nearestpair)
    print pair
    # loop over the paired two surface and coupled movement on the paired nodes
    # for example, we want to pair the movement of y direction on front and back surface
    r.Set(nodes=node[int(vortex_1[0])-1:int(vortex_1[0])], name ='set_v1'+set_name)
    r.Set(nodes=node[int(vortex_2[0])-1:int(vortex_2[0])], name ='set_v2'+set_name)
    for i in range(len(pair)):
        r.Set(nodes=node[pair[i][0]-1:pair[i][0]],name='set_0'+set_name+str(i+1))  #select pair_fb[i][0], here the node should be given in
                                                                               #tuple form, ie nodes= node[0:1],select node[1]
        r.Set(nodes=node[pair[i][1]-1:pair[i][1]],name='set_1'+set_name+str(i+1))
        #Given the MPC on
        if dof_1 == 1:
            m.Equation(name='con_dof_1_'+set_name+str(i+1),terms=((coefficient_1,'set_0'+set_name+str(i+1),1),(coefficient_2,'set_1'+set_name+str(i+1),1),(coefficient_3,'set_v1'+set_name,1),(coefficient_4,'set_v2'+set_name,1)))
        if dof_2 == 1: 
            m.Equation(name='con_dof_2_'+set_name+str(i+1),terms=((coefficient_1,'set_0'+set_name+str(i+1),2),(coefficient_2,'set_1'+set_name+str(i+1),2),(coefficient_3,'set_v1'+set_name,2),(coefficient_4,'set_v2'+set_name,2)))
        # if dof_3 == 1:   # z freedom
            # m.Equation(name='con_dof_3_'+set_name+str(i+1),terms=((coefficient_1,'set_0'+set_name+str(i+1),3),(coefficient_2,'set_1'+set_name+str(i+1),3)))

#def PBC_constrain (node_cell,node_set_1,node_set_2, vortex_1, vortex_2, coefficient_1,coefficient_2, coefficient_3, coefficient_4, dof_1,dof_2,dof_3,set_name):
# PBC_constrain (node_cell,node_left,node_right,V1,V2,1,-1,0,-1,1,0,0,'LR_x')
# PBC_constrain (node_cell,node_left,node_right,V1,V2,1,-1,0,0,0,1,0,'LR_y')

# PBC_constrain (node_cell,node_up,node_down,V1,V4,1,-1,0,0,1,0,0,'UD_x')
# PBC_constrain (node_cell,node_up,node_down,V1,V4,1,-1,0,-1,0,1,0,'UD_y')

PBC_constrain (node_cell,node_left,node_right,V1,V2,1,-1,-1,+1,1,0,0,'LR_x')
PBC_constrain (node_cell,node_left,node_right,V1,V2,1,-1,-1,+1,0,1,0,'LR_y')

PBC_constrain (node_cell,node_up,node_down,V1,V4,1,-1,1,-1,1,0,0,'UD_x')
PBC_constrain (node_cell,node_up,node_down,V1,V4,1,-1,1,-1,0,1,0,'UD_y')

# set constrain on vorteices
m.Equation(name='con_VtoV_dof1', terms=((1,'set_downLeft',1),(-1,'set_downRight',1),(1,'set_upperRight',1),(-1,'set_upperLeft',1)))
m.Equation(name='con_VtoV_dof2', terms=((1,'set_downLeft',2),(-1,'set_downRight',2),(1,'set_upperRight',2),(-1,'set_upperLeft',2)))

# set boundary condition

