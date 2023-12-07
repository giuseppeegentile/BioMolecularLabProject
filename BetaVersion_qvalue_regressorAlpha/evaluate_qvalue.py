import subprocess
import sys
	
import numpy as np
	
def get_qvalue():
	buffer_file = open("output_qvalue.txt", "w")
	prc = subprocess.run(['vmd system.psf eq.dcd -dispdev text -e native_contacts.tcl'], shell = True, stdout=buffer_file)		
	
	buffer_file.close()
	
	output_content =  open("output_qvalue.txt", "r") 
	lines = output_content.readlines()
	
#	print(lines)
	
	qvs = np.array([])
	for l in lines:
		if l.startswith("Frame"):
			#print(float(l.split(" ")[2][:-1]))
			qvs = np.append(qvs, float(l.split(" ")[2][:-1]))
	
	output_content.close()	
	#return float(lines[-4].split(" ")[2][:-1])
	with open('qvalues.npy', 'wb') as f:
		np.save(f, qvs)
	return qvs
	
q = get_qvalue()

# how to read numpy array
#with open('qvalues.npy', 'rb') as f:
#    a = np.load(f)
#    print(a)
