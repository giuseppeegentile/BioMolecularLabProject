import sys
import os
import subprocess
import numpy as np

# Translate the 3 letter code of residue to single letter code
def mapping_residue_single_code(aa_original):
	fi = ""
	# A starting				
	if aa_original == "ALA":
		fi = "A"
	elif aa_original == "ARG":
		fi = "R"
	elif aa_original == "ASN":
		fi = "N"
	elif aa_original == "ASP":
		fi = "D"
#C
	elif aa_original == "CYS":
		fi = "C"
#G					
	elif aa_original == "GLU":
		fi = "E"
	elif aa_original == "GLN":
		fi = "Q"
	elif aa_original == "GLY":
		fi = "G"
# H						
	elif aa_original == "HIS":
		fi = "H"
# I						
	elif aa_original == "ILE":
		fi = "I"
# L						
	elif aa_original == "LEU":
		fi = "L"
	elif aa_original == "LYS":
		fi = "K"
# M						
	elif aa_original == "MET":
		fi = "M"
# P					
	elif aa_original == "PHE":
		fi = "F"
	elif aa_original == "PRO":
		fi = "P"
# S					
	elif aa_original == "SER":
		fi = "S"
# T					
	elif aa_original == "THR":
		fi = "T"
	elif aa_original == "TRP":
		fi = "W"
	elif aa_original == "TYR" or aa_original == "TPQ":
		fi = "Y"
# V					
	elif aa_original == "VAL":
		fi = "V"
	elif aa_original == "CU": # we decide to treat Copper as Tyrosine
		fi = "Y"														
	else:
		print("Error, an unexpected residue found: %s" %aa_original)	
	return fi



def remove_residues(pdb_file,threshold):
	protein_name = pdb_file[:-4]

	candidates = np.array([]) 
	os.system("foldx_5 --command=AlaScan --pdb=" + pdb_file) # mutate all residues with ALA
	count = 0
	with open(protein_name + "_AS.fxout", "r") as f:# read the output of the ALA scan
		for line in f:
			words = line.split()
			res_number    = words[1]
			gibbs_energy  = float(words[-1])
			
			if gibbs_energy < -float(threshold): # apply a threshold that can go from 0(very conservative), to -0.5 (a compromise) to -1 (very strong)
 				candidates = np.append(candidates, int(res_number))
 				count += 1
	c = 0
	thr = [2,3,4]
	while count == 0:
		with open(protein_name + "_AS.fxout", "r") as f:
			for line in f:
				words = line.split()
				res_number    = words[1]
				gibbs_energy  = float(words[-1])
				
				if gibbs_energy < -float(threshold)/thr[c]: # apply a threshold that can go from 0(very conservative), to -0.5 (a compromise) to -1 (very strong)
					candidates = np.append(candidates, int(res_number))
					count += 1
		c += 1
	
			
	print("Counter mutazioni: %d" %count)
		
			
			
	candidates = np.array(candidates)			
	#print(candidates)
	np.savetxt('filtered_res_byALA.txt', candidates.astype(int),fmt='%i')
	
	

# by using ALA scan to make cut of initial mutations
def generate_mutations_v3(pdb_file):
	mutations = set()
	matrix = np.loadtxt("filtered_res_byALA.txt")
	count_all = 0
	count = 0 # remove this for the real test
	single_code_list = ["A","R","N","D","C","E","Q","G","H","I","L","K","M","F","P","S","T","W","Y","V"]
	with open(pdb_file, 'r') as pdb_file:
		for line in pdb_file:
			if line.startswith("ATOM") and len(line) >= 26:
				aa_original = line[17:20].strip()
				aa_number = line[22:26].strip()
				chain_id = line[21]
				 # remove the check on count for the real test
				if (int(aa_number) in matrix): # only add the mutations if the res number is in the list of the passed euristic of ALA
					fi = mapping_residue_single_code(aa_original)
				
					#if int(aa_number) != 639:
					filtered = [x for x in single_code_list if x != fi] # translate into single code residue
					for r in filtered:
						mutations.add(f"{fi}{chain_id}{aa_number}{r}") # add the entry in foldx file
					count_all+=1
					count +=1

	print("Total mutations (reduced for this attempt to save time): %d" %len(mutations))

	# write the mutation file for foldx
	with open("individual_list.txt","w") as f:
		str = ""
		for i,m in enumerate(mutations):
		#for i,m in enumerate(random.sample(mutations,3)):      ######## rimetti tutte le mutazioni ! ! ! 
			str += m
			if i < (len(mutations)):
				str += ";\n"
		f.write(str)

	return mutations	


pdb_file = sys.argv[1]
threshold = sys.argv[2]
remove_residues(pdb_file, threshold)
generate_mutations_v3(pdb_file)
