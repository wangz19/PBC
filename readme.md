This repository apply periodical boundary condition (PBC) in ABAQUS 6.14
other version in not teste

You need unitcell with matching node on the opposite surfaces, the code will automatically creat node_sets
and use multiple points constrain to apply PBC with reference point.

Note: strain is asscoiated with DOF1 in each reference points:
RP-1 DOF1-> E11 (uniaxial tension in x direction)
RP-2 DOF1-> E22 (uniaxial tension in y direction)
RP-3 DOF1-> E33 (uniaxial tension in z direction)
RP-4 DOF1-> E23 (pure shear in  yz plane)
RP-5 DOF1-> E13 (pure shear in  xz plane)
RP-6 DOF1-> E12 (pure shear in  xy plane)

Rigid body motion is eliminated by fix 3 DOF in cp-4 (min(x,y,z) corner point)

Hope that will help!!
