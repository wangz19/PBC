# PBC unit-cell in ABAQUS
#### Update20161129:
##### PeriodicBC.py is currently the excutible code, you need to modify the fileName and assembly name
##### Note: current version can only be apply to cubic and rectangular unit cell model

Applying __periodical boundary condition (PBC)__ is easy in molecular dynamic simulation. However, applying PBC in FEM packages, especially with non-matching mesh (often for cases with stochastic inclusions) is not trivial. This repository is a small program help applying PBC in ABAQUS 6.14, with python 2.7 and python 3.0+.

The main file:

You need unitcell with matching nodes on the opposite surfaces, the code will automatically creat node_sets
and use multiple points constrain to apply PBC with reference point.

Note: strain is asscoiated with DOF1 in each reference points:
 - ..RP-1 DOF1-> E11 (uniaxial tension in x direction)
 - ..RP-2 DOF1-> E22 (uniaxial tension in y direction)
 - ..RP-3 DOF1-> E33 (uniaxial tension in z direction)
 - ..RP-4 DOF1-> E23 (pure shear in  yz plane)
- ..RP-5 DOF1-> E13 (pure shear in  xz plane)
- ..RP-6 DOF1-> E12 (pure shear in  xy plane)

Rigid body motion is eliminated by fix 3 DOF in cp-4 (min(x,y,z) corner point)

Hope that will help!!


