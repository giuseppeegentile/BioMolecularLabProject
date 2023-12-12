mol load pdb repa_167_114_32_214.pdb
set protsel [atomselect top "protein"]
$protsel writepdb temp.pdb
package require psfgen
resetpsf
pdbalias residue HIS HSD
pdbalias atom ILE CD1 CD
topology all27_prot_lipid_cmap.top
segment P {
  pdb temp.pdb
  first nter
  last cter
}
coordpdb temp.pdb P
guesscoord
writepsf AA-repa_167_114_32_214.psf
writepdb AA-repa_167_114_32_214.pdb
exit
