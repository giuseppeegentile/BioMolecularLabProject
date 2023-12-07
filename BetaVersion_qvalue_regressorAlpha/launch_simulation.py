
import numpy as np
import subprocess
import sys
def setup_box(ionized_pdb_file):
	cf_file = "sample.conf"
	with open(cf_file, 'r') as file:
		lines = file.readlines()
		
		
	lines[11] = ("structure          system.psf\n").format()
	lines[12] = ("coordinates        system.pdb\n").format()


	with open(cf_file, 'w') as file:
		file.writelines(lines)
		
def launch_simulation():
	buffer_file = open("out.txt", "w")
	prc = subprocess.run(['setsid namd3 +p2 sample.conf'], shell = True, stdout=buffer_file)		
setup_box(sys.argv[1])
launch_simulation()






