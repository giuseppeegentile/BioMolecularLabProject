import subprocess
import sys
	
def get_qvalue(pdb_file):
	name = pdb_file[1:-4]
	buffer_file = open("output_qvalue.txt", "w")
	prc = subprocess.run(['vmd system.psf eq.dcd -dispdev text -e native_contacts.tcl'], shell = True, stdout=buffer_file)		
	
	buffer_file.close()
	
	output_content =  open("output_qvalue.txt", "r") 
	lines = output_content.readlines()
	
#	print(lines[-5])
	
	output_content.close()	
	return float(lines[-4].split(" ")[2][:-1])

	

pdb = sys.argv[1]
q = get_qvalue(pdb)
print(f"{q}")
