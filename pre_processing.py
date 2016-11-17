# define material
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


#default
m=mdb.models['Model-1']         # model name
Assembly_name ='Part-1-1'


##--------------------Material setting-------------------------##
m.Material(name='hard')
m.materials['hard'].Elastic(noCompression=ON, table=((
    80000.0, 0.3), ))
m.Material(name='soft')
m.materials['soft'].Hyperelastic(
    materialType=ISOTROPIC, testData=OFF, type=MOONEY_RIVLIN, 
    volumetricResponse=VOLUMETRIC_DATA, table=((1000.0, 100.0, 9.13e-06), 
    ))

##--------------------Steps setting-------------------------##
a = m.rootAssembly
m.StaticStep(name='Step-1', previous='Initial', 
    maxNumInc=1000, initialInc=0.01, maxInc=0.05, nlgeom=ON)


##--------------------Load Case-------------------------##
# Z-axis tension E_33
region=m.rootAssembly.sets ['RefPoint-3']
m.DisplacementBC (name='BC_e33',
createStepName='Step-1' , region=region,u3=5 ,fixed=OFF, fieldName='' , localCsys=None)

##--------------------Job-------------------------##