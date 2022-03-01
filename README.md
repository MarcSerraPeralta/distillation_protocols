# Performance of Distillation Protocols under EPR Pair Initialization and Gate Errors

Analysis of the performance of BBPSSW, DEJMPS, 3-to-1 (described in [1](https://doi.org/10.1016/j.physleta.2011.11.006)) and EPL protocols for entanglement distillation when using Werner states and imperfect gates.
The results are obtained by numerical simulation using the [NetSquid simulator](https://netsquid.org/).

## Abstract

Sharing maximally entangled pairs is essential in quantum information processing, but the unwanted interactions with the environment limit the entanglement fidelity of the produced pairs. A method to overcome such problem is entanglement distillation, whose aim is to create higher-fidelity entangled pairs from a larger number of lower-fidelity pairs. In this report, we analyse the performance of BBPSSW, DEJMPS, 3-to-1 (described in [1](https://doi.org/10.1016/j.physleta.2011.11.006)) and EPL protocols for entanglement distillation when using Werner states and imperfect gates. In particular, this report is focused on the dependence of the increase of fidelity with respect to the input pair and gate fidelities. The results are obtained by numerical simulation using the NetSquid simulator. Upon the characterization of the numerical errors, we show that all four protocols display an increase in the pair fidelity for a gate fidelity higher than ∼0.96 and that the higher the success fidelity, the lower success probability, as predicted theoretically. Moreover, we build a simple recipe to select the most useful protocol given a list of requirements and hardware performance. The results obtained in the simulations highlight the practical limitations of entanglement distillation protocols and reflect the necessity for further investigation. These include a theoretical model for the EPL protocol implemented with Werner states, the addition of noisy measurements in the simulated protocols and the increase in the number of simulations to achieve higher accuracy.

## Repository Structure

### 1) wrapper.py

Script for simulation automatization given a list of points related to the initial EPR and gate fidelities. 
It should be placed in the same folder as `app_bob.py` and `app_alice.py` for each of the protocols .

### 2) EPL, BBPSSW, DEJMPS and 3-to-1 folders

They contain the scripts needed to execute the NetQASM simulator, using the following command
```
netqasm simulate
```
The input information related to the initial EPR and gate fidelities is stored in `network.yaml`. 

### 3) plotting folder

Scripts for plotting:
- success probability and success fidelity as a function of initial EPR fidelity (including standard deviations and theoretical values)
- increase of fidelity as a function of initial EPR fidelity and gate fidelity (the script can be easily modified to plot other variables)

## Results and Formulas used

Read the following sections of the [report](report.pdf)
- I. Introduction
- IV. Results
- VI. Supplementary Information 

## Authors

- Matteo Arfini
- Daniel Bedialauneta Rodrígez
- Marc Serra Peralta
- Ksenia Shagalov

## Notes
- We do not provide any support or assistance for the supplied code nor we offer any other compilation/variant of it.
- We assume no responsibility regarding the provided code.
