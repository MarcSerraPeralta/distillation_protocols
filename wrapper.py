import subprocess as sub
import os
import numpy as np
from tqdm import tqdm

################################################################

# /!\ PUT THIS FILE INSIDE THE PROTOCOL'S FOLDER (TOGETHER WITH `app_bob.py` AND `app_alice.py`)

file_name = "app_bob.py" # script that saves the output values in a file (only `app_bob.py` OR `app_alice.py` should do it, NOT BOTH)

N_rep = 200 # number of simulations
P_range = list(np.linspace(0.5, 1, 21)) # list of points for the parameter of the depolarising channel to calculate (related to EPR fidelity)
G_range = list(np.linspace(0.8, 1, 21)) # list of points for gate fidelity to calculate (G = gate fidelity)


################################################################

def update_network(Pi, Gi):
	"""
	Updates the "network.yaml" file to execute the simultion for the given Pi and Gi. 

	:param Pi: parameter of the depolarising channel (EPR initial fidelity = (1+3*Pi)/4)
	:param Gi: gate fidelity
	"""
    string = \
"""nodes:
  - name: "the_hague"
    gate_fidelity: {0:0.4f}
    qubits:
      - id: 0
        t1: 0
        t2: 0
      - id: 1
        t1: 0
        t2: 0
  - name: "delft"
    gate_fidelity: {0:0.4f}
    qubits:
      - id: 0
        t1: 0
        t2: 0
      - id: 1
        t1: 0
        t2: 0

links:
  - name: ch1
    node_name1: "delft"
    node_name2: "the_hague"
    noise_type: Depolarise
    fidelity: {1:0.4f}""".format(Gi, Pi)

    f = open("network.yaml", "w")
    f.write(string)
    f.close()

    return

def update_script(Pi, Gi):
	"""
	Updates app file given by "file_name" to save results of the current simulation (characterized by Pi, Gi). 

	:param Pi: parameter of the depolarising channel (EPR initial fidelity = (1+3*Pi)/4)
	:param Gi: gate fidelity
	"""
	f = open(file_name, "r")
	txt = f.read()
	f.close()

	txt = txt.split("\n")
	line = [l for l in range(len(txt)) if "f = open" in txt[l]][0] # get line that has the open file
	str_line = txt[line] # get string in line

	output_file_name = ("P{:0.4f}_G{:0.4f}".format(Pi, Gi)).replace(".", "-") + ".txt" # file to store the output values for Pi and Gi
	txt[line] = str_line[:str_line.find("f = open")] + """f = open("data/{}", "a")""".format(output_file_name) # update file name (it ensures that the identation is the correct one)
	
	new_script = "\n".join(txt)
	f = open(file_name, "w") # to save the new script
	f.write(new_script)
	f.close()

	return

def post_processing(file_name):
	"""
	Returns success probability "p" and success fidelity "fidelity" (and their standard deviations) for the 
	results of the simulation stored in "file_name" (file inside "data" folder).

	:output: [p, std_p, fidelity, std_f]
	"""
	f = open("data/" + file_name, "r")
	txt = f.read()
	f.close()

	data = []
	for line in txt.split("\n")[:-1]:
		line = line.split(" ")
		succ, fidelity = int(line[0]), float(line[1])
		data += [[succ, fidelity]]

	# P_SUCC
	values = np.array([i[0] for i in data])
	p = np.average(values)
	std_p = np.std(values)/np.sqrt(len(values))

	# FIDELITY
	values = np.array([i[1] for i in data if i[0] == 1])
	fidelity = np.average(values)
	std_f = np.std(values)/np.sqrt(len(values))

	return p, std_p, fidelity, std_f

################################################################

if "data" not in os.listdir(): # create folder for storing all txt files if it does not exist
	os.mkdir("data") 


for Pi in P_range:
	for Gi in G_range:
		
		N_simulations_done = 0 # number of simulations done for Pi and Gi

		# check if this values have been already calculated and how many simulations have already been done
		output_file_name = ("P{:0.4f}_G{:0.4f}".format(Pi, Gi)).replace(".", "-") + ".txt"
		if output_file_name in os.listdir("data"): # get the number of simulations done
			f = open("data/" + output_file_name, "r") 
			txt = f.read()
			f.close()
			N_simulations_done = len(txt.split("\n")) - 1 # -1 because there is an extra empty line


		# Update Pi, Gi in the python script for the simulation
		update_script(Pi, Gi)

		# Update Pi, Gi in the network configuration
		update_network(Pi, Gi)

		# Print status
		print("Pi = {:0.4f} / Gi = {:0.4f}".format(Pi, Gi))

		# Perform simulations
		for k in tqdm(range(N_rep - N_simulations_done)):
			sub.run(["netqasm", "simulate"])

		# Post processing
		p, std_p, fidelity, std_f = post_processing(output_file_name)
		print("initial fidelity:", (1+3*Pi)/4)
		print("p_succ:", p, std_p)
		print("fidelity:", fidelity, std_f)

		print("\n")