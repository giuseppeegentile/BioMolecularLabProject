atomselect macro cgprotein {resname ALA ARG ASN ASP CYS GLN GLU GLY HSD HSE HSP HIS ILE LEU LYS MET PHE PRO SER THR TRP TYR VAL}
package require cgtools
set aamol [mol new AA-repa_167_114_32_214.psf]
mol addfile AA-repa_167_114_32_214.pdb waitfor all
::cgtools::read_db martini-protein.cgc
::cgtools::apply_database $aamol cg-repa_167_114_32_214.pdb cg-repa_167_114_32_214.rcg
exit