import sys
import os
def launch_simulation(fn):
	cf_file = "sample.conf"
	with open(cf_file, 'r') as file:
		lines = file.readlines()
		
		
	lines[0] = ("set inputname   cg-"+fn[:-4]+"-fixed\n").format()
	lines[1] = ("set outputname   eq-cg-"+fn[:-4]+"-fixed\n").format()

	with open(cf_file, 'w') as file:
		file.writelines(lines)
		
	os.system('namd2 +p20 sample.conf')	

launch_simulation(sys.argv[1])






