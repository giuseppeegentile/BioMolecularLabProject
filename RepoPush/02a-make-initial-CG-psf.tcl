atomselect macro cgprotein {resname ALA ARG ASN ASP CYS GLN GLU GLY HSD HSE HSP HIS ILE LEU LYS MET PHE PRO SER THR TRP TYR VAL}

# load coarse-grained pdb
set cgmol [mol new cg-repa_167_114_32_214.pdb]

# make preliminary psf
package require psfgen
resetpsf
topology martini-protein.top

file delete -force -- segments-protein
file mkdir segments-protein

set protsel [atomselect $cgmol "cgprotein"]
foreach seg [lsort -unique [$protsel get segname]] {
  set sel [atomselect $cgmol "segname $seg"]
  $sel writepdb segments-protein/segment_$seg.pdb
  $sel delete
}

foreach seg [lsort -unique [$protsel get segname]] {
  segment $seg {
    pdb segments-protein/segment_$seg.pdb
    first none
    last none
  }
  coordpdb segments-protein/segment_$seg.pdb $seg
}
$protsel delete

# initial pdb/psf pair
writepdb cg-repa_167_114_32_214-init.pdb
writepsf cg-repa_167_114_32_214-init.psf

file delete -force -- segments-protein

exit