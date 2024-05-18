# load all-atom protein 
set aamol [mol new AA-repa_167_114_32_214.psf]
mol addfile AA-repa_167_114_32_214.pdb waitfor all

# source script
source fix_martini_psf.tcl

fix_martini_psf $aamol martini-protein.top cg-repa_167_114_32_214-init.psf cg-repa_167_114_32_214-init.pdb cg-repa_167_114_32_214-fixed 0 0 0 0 
 
exit