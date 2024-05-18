import subprocess
import sys
	

#USAGE:
#	FIRST PARAM: NAME OF THE FILE

#I.E:	python3 build_structure.py 1wf4.pdb 

def build_top_atom(pdb_file):
	top_file_name = pdb_file[1:]

	cmd_vmd = "set a [atomselect top \"chain A and protein\"]\n" + "$a writepdb "+ top_file_name + "\n" + "exit"

	tmp_file = 'vmd_script.tcl'
	with open(tmp_file, 'w') as f:
		f.write(cmd_vmd)
	prc = subprocess.run(['vmd '+ pdb_file + ' -dispdev text -e vmd_script.tcl'], shell = True)		


# gives out a systempsf, system.pdb and top_protein.pgn
def build_pgn(pdb_file):
	top_file_name = pdb_file[1:]
	cmd_vmd = "package require psfgen\ntopology top_all27_prot_lipid.inp\npdbalias residue TPQ TYR\npdbalias residue CU TYR\npdbalias residue HIS HSE\npdbalias atom ILE CD1 CD\npdbalias atom TPQ C1 C\npdbalias atom TPQ C2 C\npdbalias atom TPQ C3 C\npdbalias atom TPQ C4 C\npdbalias atom TPQ C5 C\npdbalias atom TPQ C6 C\npdbalias atom TPQ O2 O\npdbalias atom TPQ O4 O\npdbalias atom TPQ O5 O\npdbalias atom PRO CG C\nsegment A {pdb " + top_file_name + 	"}\ncoordpdb "+ top_file_name + " A\nguesscoord\nwritepdb system.pdb\nwritepsf system.psf\nexit\n"""
	
		
	pgn_file = pdb_file[1:-4] + '.pgn'
	with open(pgn_file, 'w') as f: # write the pgn content
		f.write(cmd_vmd)
	tmp_file = 'execute_pgn.tcl'
	with open(tmp_file, 'w') as f: # write the command "source protein.pgn"
		f.write("source " + pgn_file)
	prc = subprocess.run(['vmd ' + pdb_file +' -dispdev text -e execute_pgn.tcl'], shell = True)	
	


pdb = sys.argv[1]


build_top_atom(pdb)
build_pgn(pdb)

