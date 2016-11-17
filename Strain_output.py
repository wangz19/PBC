# This code calculate the total reaction force acting on RVE 
#during displacement control
import re
from odbAccess import *

# initialization of modulus name
#        =------------default---------------- -= #
# filePath     = '**'
# odbName  = 'intesity_check_disp.odb'
# os.chdir(r"Z:\\Users\\zehaiwang\\GitHub\Periodical_BC")  #change to function directory to souce macro_modeing

odbName = 'newBC'
stepName = 'Step-1'
assemblyName = 'PART-1-1'

#objective sets
ob_set = 'REFPOINT-2'
LX = 100                # 边长，根据unitcell改
LY = 100
LZ = 100
#calculated nodes for area and strain  
#get node label from node set
# index = ['C_6','C_7','C_5','C_2']
n = [1221,11,1211,1331]

# odbName = 'strain_50_c1000'
# stepName = 'Step-1'
# assemblyName = 'BONE_D6_L10-1'
# n = [41,44,47,42]
# ob_set = 'REFPOINT-2'
# LX = 30                # 边长，根据unitcell改
# LY = 30
# LZ = 54
# n_1 				# top up (50,50,100)
# n_2 				# give x
# n_3 				# give y
# n_4 				# give z
stress = []

# Open odb file
odb           = openOdb(path = odbName+'.odb')
Frames        = odb.steps[stepName].frames

#get node label from node set
# index = ['C_6','C_7','C_5','C_2']
# n = []
# for node_index in index:
# 	temp = odb.rootAssembly.nodeSets[node_index]
# 	n.append(temp.instances[0].nodes[0].label)

ZRFSet        = odb.rootAssembly.nodeSets[ob_set.upper()]
stressZ_histo = '%s_stressZ.txt'%odbName
strainZ_histo = '%s_strainZ.txt'%odbName
volume_histo  = '%s_volume.txt'%odbName
lx_histo      = '%s_lx.txt'%odbName
ly_histo      = '%s_ly.txt'%odbName
lz_histo      = '%s_lz.txt'%odbName
newfile_sZ    = open(stressZ_histo,'w')
newfile_nZ    = open(strainZ_histo,'w')
newfile_vol   = open(volume_histo,'w')

newfile_lx = open(lx_histo,'w')
newfile_ly = open(ly_histo,'w')
newfile_lz = open(lz_histo,'w')

my_instance = odb.rootAssembly.instances[assemblyName]

# i = 0 #initialize num counter
for frame in Frames:
# get field-output
	reaction_force = frame.fieldOutputs['RF']
	displacement = frame.fieldOutputs['U']
	# bottomSet      = odb.rootAssembly.instances[assemblyName].nodeSets['BOTTOM_NODES']
# Fx = reaction_force.getSubset(region = bottomSet).values[0].data[0]
# Fy = reaction_force.getSubset(region = bottomSet).values[0].data[1]   #output reaction force in NodeSet: values['node_inSet']
	Fz = reaction_force.getSubset(region = ZRFSet)
	fz = Fz.values[0].data[2]
	def_n = []
	for i in n:
		i = i-1
		temp_coordinate = my_instance.nodes[i].coordinates+displacement.values[i].data
		def_n.append(temp_coordinate)
	lx = sqrt((def_n[0][0]-def_n[1][0])**2+(def_n[0][1]-def_n[1][1])**2+(def_n[0][2]-def_n[1][2])**2)
	ly = sqrt((def_n[0][0]-def_n[2][0])**2+(def_n[0][1]-def_n[2][1])**2+(def_n[0][2]-def_n[2][2])**2)
	lz = sqrt((def_n[0][0]-def_n[3][0])**2+(def_n[0][1]-def_n[3][1])**2+(def_n[0][2]-def_n[3][2])**2)
	V_temp = lx*ly*lz
# calculate stress and strain in the srain
	s_temp = fz/(lx*ly)
	n_temp = log(lz/LZ)
	newfile_sZ.write(str(s_temp)+'\n')
	newfile_nZ.write(str(n_temp)+'\n')
	newfile_vol.write(str(V_temp)+'\n')
	newfile_lx.write(str(lx)+'\n')
	newfile_ly.write(str(ly)+'\n')
	newfile_lz.write(str(lz)+'\n')
	print fz,lx,ly,lz



newfile_sZ.close()
newfile_nZ.close()
newfile_vol.close()
newfile_lx.close()
newfile_ly.close()
newfile_lz.close()




