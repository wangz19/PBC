#coding:utf-8
# This code is modifeid from J.T.B. Overvelde
#2016/11/01 Zehai Wang for rectangular unitcell
#Latest update 2016/11/15
# === Modules ===
from math import *
from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *
import numpy as np
# import matplotlib.pyplot as plt
import re
import time
import os
from itertools import chain # 用chain的方法合并集合
# os.chdir(r"Z:\\Users\\zehaiwang\\GitHub\Periodical_BC")  #change to function directory to souce macro_modeing

#default
m=mdb.models['Model-1']         # model name
Assembly_name ='Part-1-1'
# m= mdb.models['bone_d6_L15'] 
# Assembly_name ='BONE_D6_L15-1'       # part name
r=m.rootAssembly
node=r.instances[Assembly_name].nodes

#ne 存储所有边界上的单元节点的编号 node ID on the suface
nb=[]   #node on the back boundary surface x_min
nf=[]   #node on the right boundary surface x_max
nl=[]   #node on the left boundary surface y_min
nr=[]   #node on the right boundary surface y_max
nu=[]   #node on the right boundary surface z_max
nd=[]   #node on the right boundary surface z_max

#reformat the node id, x, y, z postion in an Nx4 array
# as shown          1, 0, 0, 0
node_cell =np.zeros((len(node),4)) 
for i in range(len(node)):
    node_cell[i][1]=node[i].coordinates[0]  #x
    node_cell[i][2]=node[i].coordinates[1]  #y
    node_cell[i][3]=node[i].coordinates[2]  #z
    node_cell[i][0]=node[i].label

# print node_cell
# determine the surface position in character coordinates
x_min = np.min(node_cell[:,1])
x_max = np.max(node_cell[:,1])
y_min = np.min(node_cell[:,2])
y_max = np.max(node_cell[:,2])
z_min = np.min(node_cell[:,3])
z_max = np.max(node_cell[:,3])

# center of the unit cell
lxc = 0.5*(x_min+x_max)
lyc = 0.5*(y_min+y_max)
lzc = 0.5*(z_min+z_max)
# dimension of the unit cell
lx = 0.5*(x_min+x_max)
ly = 0.5*(y_min+y_max)
lz = 0.5*(z_min+z_max)

for i in range(len(node_cell[:,0])):
    if abs(node_cell[i][1]-x_min)<0.001:          # back surface
        nb.append(int(node_cell[i][0]))
    if abs(node_cell[i][1]-x_max)<0.001:          #front surface
        nf.append(int(node_cell[i][0]))
    if abs(node_cell[i][2]-y_min)<0.001:          #left surface
        nl.append(int(node_cell[i][0]))
    if abs(node_cell[i][2]-y_max)<0.001:          #right surface
        nr.append(int(node_cell[i][0]))
    if abs(node_cell[i][3]-z_max)<0.001:          #upper surface
        nu.append(int(node_cell[i][0]))
    if abs(node_cell[i][3]-z_min)<0.001:          #right surface
        nd.append(int(node_cell[i][0])) 
# print nl
# print nr

# 合并表面节点
surface_temp   = chain(nb,nf,nl,nr,nd) 

#Define nodes on the edges
fd = set(nf).intersection(nd)
rd = set(nr).intersection(nd)
bd = set(nb).intersection(nd)
ld = set(nl).intersection(nd)
fu = set(nf).intersection(nu)
ru = set(nr).intersection(nu)
bu = set(nb).intersection(nu)
lu = set(nl).intersection(nu)
lf = set(nl).intersection(nf)
fr = set(nf).intersection(nr)
rb = set(nr).intersection(nb)
bl = set(nb).intersection(nl)
# print fd,rd,bd,ld,fu,ru,bu,lu,lf,fr,rb,bl

# Define coner points
nc_1 = fd.intersection(ld)
nc_2 = fd.intersection(rd)
nc_3 = rd.intersection(bd)
nc_4 = bd.intersection(ld)
nc_5 = fu.intersection(lu)
nc_6 = fu.intersection(ru)
nc_7 = ru.intersection(bu)
nc_8 = bu.intersection(lu)
## check coner points
# print nc_1,nc_2,nc_3,nc_4,nc_5,nc_6,nc_7,nc_8

# form edge group and conor group
edge_group  = []
coner_group = []
edge_temp   = chain(fd,rd,bd,ld,fu,ru,bu,lu,lf,fr,rb,bl)    # this is including the corner points
coner_temp = chain(nc_1,nc_2,nc_3,nc_4,nc_5,nc_6,nc_7,nc_8)
for item in edge_temp:
    edge_group.append(item)

for item in coner_temp:
    coner_group.append(item)

# find node that only on the SURFACES but not edges and corners
nf = list(set(nf)-set(edge_group))
nb = list(set(nb)-set(edge_group))
nr = list(set(nr)-set(edge_group))
nl = list(set(nl)-set(edge_group))
nu = list(set(nu)-set(edge_group))
nd = list(set(nd)-set(edge_group))

#find nodes on the EDGES not corners
fd = list(set(fd)-set(coner_group))
rd = list(set(rd)-set(coner_group))
bd = list(set(bd)-set(coner_group))
ld = list(set(ld)-set(coner_group))
fu = list(set(fu)-set(coner_group))
ru = list(set(ru)-set(coner_group))
bu = list(set(bu)-set(coner_group))
lu = list(set(lu)-set(coner_group))
lf = list(set(lf)-set(coner_group))
fr = list(set(fr)-set(coner_group))
rb = list(set(rb)-set(coner_group))
bl = list(set(bl)-set(coner_group))


#Create reference parts and assemble
NameRef1='RefPoint-1'; NameRef2='RefPoint-2'; NameRef3='RefPoint-3'
m.Part(dimensionality=THREE_D, name=NameRef1, type=
                           DEFORMABLE_BODY)
m.parts[NameRef1].ReferencePoint(point=(10.0, 0.0, 0.0))
m.Part(dimensionality=THREE_D, name=NameRef2, type=
                           DEFORMABLE_BODY)
m.parts[NameRef2].ReferencePoint(point=(20.0, 0.0, 0.0))
m.Part(dimensionality=THREE_D, name=NameRef3, type=
                           DEFORMABLE_BODY)
m.parts[NameRef3].ReferencePoint(point=(30.0, 0.0, 0.0))
m.rootAssembly.Instance(dependent=ON, name=NameRef1,
                                            part=m.parts[NameRef1])
m.rootAssembly.Instance(dependent=ON, name=NameRef2,
                                            part=m.parts[NameRef2])
m.rootAssembly.Instance(dependent=ON, name=NameRef3,
                                            part=m.parts[NameRef3])

#Create set of reference points
m.rootAssembly.Set(name=NameRef1, referencePoints=(
    m.rootAssembly.instances[NameRef1].referencePoints[1],))
m.rootAssembly.Set(name=NameRef2, referencePoints=(
    m.rootAssembly.instances[NameRef2].referencePoints[1],))
m.rootAssembly.Set(name=NameRef3, referencePoints=(
    m.rootAssembly.instances[NameRef3].referencePoints[1],))

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


def PBC_constrain (node_cell,node_set_1,node_set_2,dof_1,dof_2,dof_3,ReferencePoint,set_name):
    # node_cell is collection of all the nodes and coordinates
    # node_set_1 and _2 are opposite boundaries
    # pairing nodes in two opposite surface
    # where the node number on the two face need not to be equal
    # number of pair depend on the min node of the two surface
    # m=mdb.models['Model-1']
    # r=m.rootAssembly
    # node=r.instances['Part-1-1'].nodes
    # pair_num = min(len(nb),len(nf))
    # print pair_num
    pair = []    #temp position for front and back surface
    for x in node_set_1:
        mindist     = float("inf")  #initialize distance as infinite large
        for y in node_set_2:
            dist = distance(node_cell, x, y)
            if dist< mindist:
                mindist     = dist  
                nearestpair = (int(x),int(y))   # convert float node label into int for future reference
        pair.append(nearestpair)
    if len(pair)!=len(node_set_1):
        print 'Error happend with node piaring, node pair missing'
    # loop over the paired two surface and coupled movement on the paired nodes
    # for example, we want to pair the movement of y direction on front and back surface
    for i in range(len(pair)):
        r.Set(nodes=node[pair[i][0]-1:pair[i][0]],name='set0_'+set_name+str(i+1))  #select pair_fb[i][0], here the node should be given in
                                                                                #tuple form, ie nodes= node[0:1],select node[1]
        r.Set(nodes=node[pair[i][1]-1:pair[i][1]],name='set1_'+set_name+str(i+1))
        #Given the MPC on
        if dof_1 == 1:
            m.Equation(name=set_name+'_dof_1_'+str(i+1),terms=((1.0,'set0_'+set_name+str(i+1),1),(-1.0,'set1_'+set_name+str(i+1),1),(-1.0, ReferencePoint, 1)))
        if dof_2 == 1:
            m.Equation(name=set_name+'_dof_2_'+str(i+1),terms=((1.0,'set0_'+set_name+str(i+1),2),(-1.0,'set1_'+set_name+str(i+1),2),(-1.0, ReferencePoint, 2)))
        if dof_3 == 1:
            m.Equation(name=set_name+'_dof_3_'+str(i+1),terms=((1.0,'set0_'+set_name+str(i+1),3),(-1.0,'set1_'+set_name+str(i+1),3),(-1.0, ReferencePoint, 3)))

#def PBC_constrain (node_cell,nb,nf,coefficient_1,coefficient_2,dof_1,dof_2,dof_3):
# creat surface constrain equations
start1 = time.time()
PBC_constrain (node_cell,nf,nb,1,1,1,'RefPoint-1','fb')
PBC_constrain (node_cell,nr,nl,1,1,1,'RefPoint-2','rl')
PBC_constrain (node_cell,nu,nd,1,1,1,'RefPoint-3','ud')

#creat edge constrain equations
# Y-Z
PBC_constrain (node_cell,ru,lu,1,1,1,'RefPoint-2','edge_rlu')
PBC_constrain (node_cell,lu,ld,1,1,1,'RefPoint-3','edge_udl')
PBC_constrain (node_cell,rd,ld,1,1,1,'RefPoint-2','edge_rld')
#X-Z
PBC_constrain (node_cell,fu,bu,1,1,1,'RefPoint-1','edge_fbu')
PBC_constrain (node_cell,bu,bd,1,1,1,'RefPoint-3','edge_bud')
PBC_constrain (node_cell,fd,bd,1,1,1,'RefPoint-1','edge_fbd')
#X-Y
PBC_constrain (node_cell,rb,bl,1,1,1,'RefPoint-2','edge_rbl')
PBC_constrain (node_cell,lf,bl,1,1,1,'RefPoint-1','edge_lfb')
PBC_constrain (node_cell,fr,lf,1,1,1,'RefPoint-2','edge_frl')

#Create cornor constrains
for i in range(8):
    r.Set(nodes=node[coner_group[i]-1:coner_group[i]],name='c_'+str(i+1)) # front left corner (x+,0,0)

PBC_constrain (node_cell,nc_5,nc_8,1,1,1,'RefPoint-1','cp_1')
PBC_constrain (node_cell,nc_6,nc_7,1,1,1,'RefPoint-1','cp_2')
PBC_constrain (node_cell,nc_2,nc_3,1,1,1,'RefPoint-1','cp_3')
PBC_constrain (node_cell,nc_1,nc_4,1,1,1,'RefPoint-1','cp_4')
PBC_constrain (node_cell,nc_7,nc_8,1,1,1,'RefPoint-2','cp_5')
PBC_constrain (node_cell,nc_3,nc_4,1,1,1,'RefPoint-2','cp_6')
PBC_constrain (node_cell,nc_8,nc_4,1,1,1,'RefPoint-3','cp_7')

# # move 3 dof for rigid body motion
region=m. rootAssembly . sets [ 'c_4' ]
m. DisplacementBC (name='BC-rigid',
createStepName='Initial' , region=region , u1=0.0 ,
u2=0.0 , u3=0.0 ,fixed=OFF, fieldName='' , localCsys=None)


end1 = time.time()
print 'Nodes Coupling takes %ds'%(end1 - start1)
print 'dimension of the unit cell: %dx%dx%d'%(lx,ly,lz)
print 'nodes for strain cal: [%d,%d,%d,%d]'%(list(nc_6)[0],list(nc_7)[0],list(nc_5)[0],list(nc_2)[0])


