How to perform multiple mutation at the same time
    1. repair protein:
        foldx_20231231 --command=RepairPDB --pdb=1av4.pdb

        this outputs a new pdb called: 1av4_Repair.pdb

        WHY?
            repair it to the most stable state as predicted by FoldX. Running the RepairPDB command, will ask FoldX to change the conformation of the side-chains to avoid clashes and optimize overall the stability of the structure. FoldX does not change the backbone of the structure, only moving the side-chains. This repair can take 5-10 minutes to conclude depending on the size of the protein.
    
    2. now analyze the PDB file, taking a portion of it:
        ATOM    591  CG2 VAL A  88      24.452  -5.593  42.962  1.00 36.60           C  
        ATOM    592  N   GLU A  89      27.569  -6.083  40.558  1.00 35.66           N  
        ATOM    593  CA  GLU A  89      27.463  -6.339  39.126  1.00 36.70           C  
        ATOM    594  C   GLU A  89      26.349  -7.358  38.935  1.00 34.23           C  
        ATOM    595  O   GLU A  89      26.364  -8.422  39.555  1.00 35.93           O  
        ATOM    596  CB  GLU A  89      28.771  -6.892  38.555  1.00 39.67           C  
        ATOM    597  CG  GLU A  89      29.825  -5.837  38.259  1.00 46.92           C  
        ATOM    598  CD  GLU A  89      30.908  -6.324  37.297  1.00 51.72           C  
        ATOM    599  OE1 GLU A  89      30.923  -7.527  36.939  1.00 51.20           O  
        ATOM    600  OE2 GLU A  89      31.746  -5.487  36.892  1.00 52.60           O  
        ATOM    601  N   LEU A  90      25.369  -7.017  38.107  1.00 29.29           N  
        ATOM    602  CA  LEU A  90      24.248  -7.911  37.854  1.00 29.63           C  
        ATOM    603  C   LEU A  90      24.515  -8.882  36.719  1.00 30.21           C  
        ATOM    604  O   LEU A  90      25.292  -8.604  35.807  1.00 34.93           O  
        ATOM    605  CB  LEU A  90      22.993  -7.109  37.513  1.00 26.89           C  
        ATOM    606  CG  LEU A  90      22.154  -6.442  38.602  1.00 27.99           C  
        ATOM    607  CD1 LEU A  90      22.956  -6.185  39.858  1.00 31.06           C  
        ATOM    608  CD2 LEU A  90      21.589  -5.156  38.041  1.00 26.77           C  
        ATOM    609  N   ASP A  91      23.867 -10.032  36.799  1.00 29.41           N  
        ATOM    610  CA  ASP A  91      23.959 -11.047  35.769  1.00 29.17           C  
        ATOM    611  C   ASP A  91      22.524 -11.052  35.252  1.00 29.89           C  
        ATOM    612  O   ASP A  91      21.676 -11.786  35.766  1.00 27.13           O  
        ATOM    613  CB  ASP A  91      24.335 -12.395  36.388  1.00 28.45           C  


        Suppose you now want to modify the aminoacid LEU (L) of sidechain A @ position 90 into an A residue, an E and a W   
        - >create a "individual_list.txt" like this:
            LA90A;
            LA90E;
            LA90W;
    3. foldx_20231231 --command=BuildModel --wildtype=sequences.buildmodel --pdb=1av4_Repair.pdb --mutant-file=individual_list.txt
        this will print out information about the mutation and the new pdbs

    4. Predicted energy differences in “Dif_1av4_Repair.fxout” which will have an entry per mutation in the same order as the list of mutations. 
    The output contains information on the total 𝚫𝚫G as well as different components that contribute to the total score.  (tabular mode)


How to perform single mutation: the ALANINE one (which seems very popular): faster but less accurate
 output: “1a4v_Repair_AS.fxout” containing the predicted impact of mutating each residue to alanine in seperate lines. 
