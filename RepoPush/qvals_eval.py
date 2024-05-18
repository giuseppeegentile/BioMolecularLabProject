import MDAnalysis as mda
import numpy as np
from MDAnalysis.analysis import contacts
import sys


import sys
#python evals_eval.py cg-repa-init.psf eq-cg-repa-fixed.dcd 
# Load the trajectory and topology files
#topology = "cg-repa-init.psf"
#trajectory = "eq-cg-repa-fixed.dcd"
def calculate_native_contacts(trajectory_file, psf_file, cutoff_distance):
    # Load the trajectory and topology
    u = mda.Universe(psf_file, trajectory_file)

    # Select atoms of interest based on your system and criteria
    selection_atoms_A = u.select_atoms('all')
    selection_atoms_B = u.select_atoms('all')

    # Initialize an array to store native contacts
    native_contacts = np.zeros(len(u.trajectory))

    # Loop over trajectory frames
    for ts in u.trajectory:
        # Calculate distances between atoms in group A and atoms in group B
        distances = mda.lib.distances.distance_array(selection_atoms_A.positions,
                                                     selection_atoms_B.positions,
                                                     box=u.dimensions)

        # Determine native contacts based on the cutoff distance
        native_contacts_frame = np.sum(distances < cutoff_distance)

        # Store the result in the array
        native_contacts[ts.frame] = native_contacts_frame

    return native_contacts

#print(calculate_native_contacts(trajectory, topology, 2.6))

def calculate_native_contacts_V2(trajectory_file, psf_file, cutoff_distance):
    # example trajectory (transition of AdK from closed to open)
    u = mda.Universe(psf_file,trajectory_file)
    # crude definition of salt bridges as contacts between NH/NZ in ARG/LYS and
    # OE*/OD* in ASP/GLU. You might want to think a little bit harder about the
    # problem before using this for real work.
    sel_basic = "all"
    sel_acidic = "all"
    # reference groups (first frame of the trajectory, but you could also use a
    # separate PDB, eg crystal structure)
    acidic = u.select_atoms(sel_acidic)
    basic = u.select_atoms(sel_basic)
    # set up analysis of native contacts ("salt bridges"); salt bridges have a
    # distance <6 A
    ca1 = contacts.Contacts(u, select=(sel_acidic, sel_basic),
                            refgroup=(acidic, basic), radius=3.5)

    # iterate through trajectory and perform analysis of "native contacts" Q
    ca1.run()
    # print number of averave contacts
    print(ca1.timeseries[:,1])
    arr_save = np.array(ca1.timeseries[:,1])
    with open('qvalues.npy', 'wb') as f:
	    np.save(f, arr_save)
    average_contacts = np.mean(ca1.timeseries[:, 1])
    print('average contacts = {}'.format(average_contacts))


fn = sys.argv[1]

topology = "cg-"+fn[:-4]+"-fixed.psf"
trajectory = "eq-cg-"+fn[:-4]+"-fixed.dcd"
calculate_native_contacts_V2(trajectory, topology, 2.6)




























