import sys
import os
fn = sys.argv[1]
str = "mol load pdb " + fn + "\nset protsel [atomselect top \"protein\"]\n$protsel writepdb temp.pdb\npackage require psfgen\nresetpsf\npdbalias residue HIS HSD\npdbalias atom ILE CD1 CD\ntopology all27_prot_lipid_cmap.top\nsegment P {\n  pdb temp.pdb\n  first nter\n  last cter\n}\ncoordpdb temp.pdb P\nguesscoord\nwritepsf AA-" + fn[:-4] + ".psf\nwritepdb AA-" + fn + "\nexit\n"
#print(str)
with open("00-make-AA-psf.tcl", "w") as f:
    f.write(str)

os.system("vmd -dispdev text -e 00-make-AA-psf.tcl")


step1 = "atomselect macro cgprotein {resname ALA ARG ASN ASP CYS GLN GLU GLY HSD HSE HSP HIS ILE LEU LYS MET PHE PRO SER THR TRP TYR VAL}\npackage require cgtools\nset aamol [mol new AA-"+fn[:-4]+".psf]\nmol addfile AA-"+fn+" waitfor all\n::cgtools::read_db martini-protein.cgc\n::cgtools::apply_database $aamol cg-"+fn+" cg-"+fn[:-4]+".rcg\nexit"
#print(step1)
with open("01-coarse-grain.tcl", "w") as f:
    f.write(step1)
os.system("vmd -dispdev text -e 01-coarse-grain.tcl")


step2a = """atomselect macro cgprotein {resname ALA ARG ASN ASP CYS GLN GLU GLY HSD HSE HSP HIS ILE LEU LYS MET PHE PRO SER THR TRP TYR VAL}

# load coarse-grained pdb
set cgmol [mol new cg-""" + fn + """]

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
writepdb cg-""" + fn[:-4] + """-init.pdb
writepsf cg-""" + fn[:-4] + """-init.psf

file delete -force -- segments-protein

exit"""
#print(step2a)
with open("02a-make-initial-CG-psf.tcl", "w") as f:
    f.write(step2a)
os.system("vmd -dispdev text -e 02a-make-initial-CG-psf.tcl")

step2b = """# load all-atom protein 
set aamol [mol new AA-""" + fn[:-4] + """.psf]
mol addfile AA-""" + fn[:-4] + """.pdb waitfor all

# source script
source fix_martini_psf.tcl

fix_martini_psf $aamol martini-protein.top cg-""" + fn[:-4] + """-init.psf cg-""" + fn[:-4] + """-init.pdb cg-""" + fn[:-4] + """-fixed 0 0 0 0 
 
exit"""

with open("02b-correct-CG-psf.tcl", "w") as f:
    f.write(step2b)
os.system("vmd -dispdev text -e 02b-correct-CG-psf.tcl")
