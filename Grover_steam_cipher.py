from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, EstimatorV2 as Estimator
import matplotlib.pyplot as plt
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_aer import AerSimulator
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from numpy import pi
from qiskit.circuit.library import C4XGate
from qiskit.visualization import plot_histogram
from qiskit.circuit.library import MCXGate
from decimal import Decimal, getcontext

# service = QiskitRuntimeService()
qreg_q = QuantumRegister(10, 'q')
qreg_a = QuantumRegister(1, 'a')
creg_c0 = ClassicalRegister(5, 'c0')
circuit = QuantumCircuit(qreg_q, qreg_a, creg_c0)
# # Input plain text q0 -> q4
circuit.barrier()
# circuit.x(qreg_q[0])
# circuit.x(qreg_q[1])
circuit.x(qreg_q[2])
circuit.x(qreg_q[3])
circuit.x(qreg_q[4])

# # # Quantum superposition + Phase kickback
circuit.barrier()
circuit.x(qreg_a[0])
circuit.h(qreg_q[5])
circuit.h(qreg_q[6])
circuit.h(qreg_q[7])
circuit.h(qreg_q[8])    
circuit.h(qreg_q[9])
circuit.h(qreg_a[0])

# #//////////////
# #Round 1
# #//////////////


# # first Iterator
# # Add roundkey
circuit.barrier()
circuit.cx(qreg_q[9], qreg_q[4])
circuit.cx(qreg_q[8], qreg_q[3])
circuit.cx(qreg_q[7], qreg_q[2])
circuit.cx(qreg_q[6], qreg_q[1])
circuit.cx(qreg_q[5], qreg_q[0])

# #KEY GEN
circuit.barrier()
circuit.cx(qreg_q[8], qreg_q[5])
circuit.cx(qreg_q[9], qreg_q[6])
circuit.cx(qreg_q[5], qreg_q[7])
circuit.cx(qreg_q[6], qreg_q[8])
circuit.cx(qreg_q[7], qreg_q[9])
# # Add roundkey
circuit.barrier()
circuit.cx(qreg_q[9], qreg_q[4])
circuit.cx(qreg_q[8], qreg_q[3])
circuit.cx(qreg_q[7], qreg_q[2])
circuit.cx(qreg_q[6], qreg_q[1])
circuit.cx(qreg_q[5], qreg_q[0])
circuit.barrier()
# #//Check output q0 -> q4
circuit.x(qreg_q[0])
# circuit.x(qreg_q[1])
circuit.x(qreg_q[2])
# # circuit.x(qreg_q[3])
circuit.x(qreg_q[4])
gate = MCXGate(5)
circuit.append(gate, [0,1,2,3,4,10])
# circuit.barrier()
circuit.x(qreg_q[0])
# circuit.x(qreg_q[1])
circuit.x(qreg_q[2])
# # circuit.x(qreg_q[3])
circuit.x(qreg_q[4])
# #End check output
# #REV
# # REV Add roundkey
circuit.barrier()

circuit.cx(qreg_q[9], qreg_q[4])
circuit.cx(qreg_q[8], qreg_q[3])
circuit.cx(qreg_q[7], qreg_q[2])
circuit.cx(qreg_q[6], qreg_q[1])
circuit.cx(qreg_q[5], qreg_q[0])
#REV KEY GEN
circuit.barrier()
circuit.cx(qreg_q[7], qreg_q[9])
circuit.cx(qreg_q[6], qreg_q[8])
circuit.cx(qreg_q[5], qreg_q[7])
circuit.cx(qreg_q[9], qreg_q[6])
circuit.cx(qreg_q[8], qreg_q[5])
# # Add roundkey
circuit.barrier()
circuit.cx(qreg_q[9], qreg_q[4])
circuit.cx(qreg_q[8], qreg_q[3])
circuit.cx(qreg_q[7], qreg_q[2])
circuit.cx(qreg_q[6], qreg_q[1])
circuit.cx(qreg_q[5], qreg_q[0])
# #End Rev 
circuit.barrier()
#Grover Diffusion
#//////////////
circuit.h(qreg_q[5])
circuit.h(qreg_q[8])
circuit.h(qreg_q[9])
circuit.h(qreg_q[6])
circuit.h(qreg_q[7])

circuit.x(qreg_q[5])
circuit.x(qreg_q[6])
circuit.x(qreg_q[7])
circuit.x(qreg_q[8])
circuit.x(qreg_q[9])

circuit.h(qreg_q[9])
gate = MCXGate(4)
circuit.append(gate, [5,6,7,8,9])
circuit.h(qreg_q[9])
circuit.x(qreg_q[5])
circuit.x(qreg_q[6])
circuit.x(qreg_q[7])
circuit.x(qreg_q[8])
circuit.x(qreg_q[9])

circuit.h(qreg_q[5])
circuit.h(qreg_q[8])
circuit.h(qreg_q[9])
circuit.h(qreg_q[6])
circuit.h(qreg_q[7])

#Second iterator
# # Add roundkey
circuit.barrier()
circuit.cx(qreg_q[9], qreg_q[4])
circuit.cx(qreg_q[8], qreg_q[3])
circuit.cx(qreg_q[7], qreg_q[2])
circuit.cx(qreg_q[6], qreg_q[1])
circuit.cx(qreg_q[5], qreg_q[0])

# #KEY GEN
circuit.barrier()
circuit.cx(qreg_q[8], qreg_q[5])
circuit.cx(qreg_q[9], qreg_q[6])
circuit.cx(qreg_q[5], qreg_q[7])
circuit.cx(qreg_q[6], qreg_q[8])
circuit.cx(qreg_q[7], qreg_q[9])
# # Add roundkey
circuit.barrier()
circuit.cx(qreg_q[9], qreg_q[4])
circuit.cx(qreg_q[8], qreg_q[3])
circuit.cx(qreg_q[7], qreg_q[2])
circuit.cx(qreg_q[6], qreg_q[1])
circuit.cx(qreg_q[5], qreg_q[0])
circuit.barrier()
# #//Check output q0 -> q4
circuit.x(qreg_q[0])
# circuit.x(qreg_q[1])
circuit.x(qreg_q[2])
# # circuit.x(qreg_q[3])
circuit.x(qreg_q[4])
gate = MCXGate(5)
circuit.append(gate, [0,1,2,3,4,10])
circuit.barrier()
circuit.x(qreg_q[0])
# circuit.x(qreg_q[1])
circuit.x(qreg_q[2])
# # circuit.x(qreg_q[3])
circuit.x(qreg_q[4])
# #End check output
# #REV
# # REV Add roundkey
circuit.barrier()

circuit.cx(qreg_q[9], qreg_q[4])
circuit.cx(qreg_q[8], qreg_q[3])
circuit.cx(qreg_q[7], qreg_q[2])
circuit.cx(qreg_q[6], qreg_q[1])
circuit.cx(qreg_q[5], qreg_q[0])
#REV KEY GEN
circuit.barrier()
circuit.cx(qreg_q[7], qreg_q[9])
circuit.cx(qreg_q[6], qreg_q[8])
circuit.cx(qreg_q[5], qreg_q[7])
circuit.cx(qreg_q[9], qreg_q[6])
circuit.cx(qreg_q[8], qreg_q[5])
# # Add roundkey
circuit.barrier()
circuit.cx(qreg_q[9], qreg_q[4])
circuit.cx(qreg_q[8], qreg_q[3])
circuit.cx(qreg_q[7], qreg_q[2])
circuit.cx(qreg_q[6], qreg_q[1])
circuit.cx(qreg_q[5], qreg_q[0])
# #End Rev 
circuit.barrier()
#Grover Diffusion
#//////////////
circuit.h(qreg_q[5])
circuit.h(qreg_q[8])
circuit.h(qreg_q[9])
circuit.h(qreg_q[6])
circuit.h(qreg_q[7])

circuit.x(qreg_q[5])
circuit.x(qreg_q[6])
circuit.x(qreg_q[7])
circuit.x(qreg_q[8])
circuit.x(qreg_q[9])

circuit.h(qreg_q[9])
gate = MCXGate(4)
circuit.append(gate, [5,6,7,8,9])
circuit.h(qreg_q[9])
circuit.x(qreg_q[5])
circuit.x(qreg_q[6])
circuit.x(qreg_q[7])
circuit.x(qreg_q[8])
circuit.x(qreg_q[9])

circuit.h(qreg_q[5])
circuit.h(qreg_q[8])
circuit.h(qreg_q[9])
circuit.h(qreg_q[6])
circuit.h(qreg_q[7])
# 3rd
# # Add roundkey
circuit.barrier()
circuit.cx(qreg_q[9], qreg_q[4])
circuit.cx(qreg_q[8], qreg_q[3])
circuit.cx(qreg_q[7], qreg_q[2])
circuit.cx(qreg_q[6], qreg_q[1])
circuit.cx(qreg_q[5], qreg_q[0])

# #KEY GEN
circuit.barrier()
circuit.cx(qreg_q[8], qreg_q[5])
circuit.cx(qreg_q[9], qreg_q[6])
circuit.cx(qreg_q[5], qreg_q[7])
circuit.cx(qreg_q[6], qreg_q[8])
circuit.cx(qreg_q[7], qreg_q[9])
# # Add roundkey
circuit.barrier()
circuit.cx(qreg_q[9], qreg_q[4])
circuit.cx(qreg_q[8], qreg_q[3])
circuit.cx(qreg_q[7], qreg_q[2])
circuit.cx(qreg_q[6], qreg_q[1])
circuit.cx(qreg_q[5], qreg_q[0])
circuit.barrier()
# #//Check output q0 -> q4
circuit.x(qreg_q[0])
# circuit.x(qreg_q[1])
circuit.x(qreg_q[2])
# # circuit.x(qreg_q[3])
circuit.x(qreg_q[4])
gate = MCXGate(5)
circuit.append(gate, [0,1,2,3,4,10])
circuit.barrier()
circuit.x(qreg_q[0])
# circuit.x(qreg_q[1])
circuit.x(qreg_q[2])
# # circuit.x(qreg_q[3])
circuit.x(qreg_q[4])
# #End check output
# #REV
# # REV Add roundkey
circuit.barrier()

circuit.cx(qreg_q[9], qreg_q[4])
circuit.cx(qreg_q[8], qreg_q[3])
circuit.cx(qreg_q[7], qreg_q[2])
circuit.cx(qreg_q[6], qreg_q[1])
circuit.cx(qreg_q[5], qreg_q[0])
#REV KEY GEN
circuit.barrier()
circuit.cx(qreg_q[7], qreg_q[9])
circuit.cx(qreg_q[6], qreg_q[8])
circuit.cx(qreg_q[5], qreg_q[7])
circuit.cx(qreg_q[9], qreg_q[6])
circuit.cx(qreg_q[8], qreg_q[5])
# # Add roundkey
circuit.barrier()
circuit.cx(qreg_q[9], qreg_q[4])
circuit.cx(qreg_q[8], qreg_q[3])
circuit.cx(qreg_q[7], qreg_q[2])
circuit.cx(qreg_q[6], qreg_q[1])
circuit.cx(qreg_q[5], qreg_q[0])
# #End Rev 
circuit.barrier()
#Grover Diffusion
#//////////////
circuit.h(qreg_q[5])
circuit.h(qreg_q[8])
circuit.h(qreg_q[9])
circuit.h(qreg_q[6])
circuit.h(qreg_q[7])

circuit.x(qreg_q[5])
circuit.x(qreg_q[6])
circuit.x(qreg_q[7])
circuit.x(qreg_q[8])
circuit.x(qreg_q[9])

circuit.h(qreg_q[9])
gate = MCXGate(4)
circuit.append(gate, [5,6,7,8,9])
circuit.h(qreg_q[9])
circuit.x(qreg_q[5])
circuit.x(qreg_q[6])
circuit.x(qreg_q[7])
circuit.x(qreg_q[8])
circuit.x(qreg_q[9])

circuit.h(qreg_q[5])
circuit.h(qreg_q[8])
circuit.h(qreg_q[9])
circuit.h(qreg_q[6])
circuit.h(qreg_q[7])
#4-th
# # Add roundkey
circuit.barrier()
circuit.cx(qreg_q[9], qreg_q[4])
circuit.cx(qreg_q[8], qreg_q[3])
circuit.cx(qreg_q[7], qreg_q[2])
circuit.cx(qreg_q[6], qreg_q[1])
circuit.cx(qreg_q[5], qreg_q[0])

# #KEY GEN
circuit.barrier()
circuit.cx(qreg_q[8], qreg_q[5])
circuit.cx(qreg_q[9], qreg_q[6])
circuit.cx(qreg_q[5], qreg_q[7])
circuit.cx(qreg_q[6], qreg_q[8])
circuit.cx(qreg_q[7], qreg_q[9])
# # Add roundkey
circuit.barrier()
circuit.cx(qreg_q[9], qreg_q[4])
circuit.cx(qreg_q[8], qreg_q[3])
circuit.cx(qreg_q[7], qreg_q[2])
circuit.cx(qreg_q[6], qreg_q[1])
circuit.cx(qreg_q[5], qreg_q[0])
circuit.barrier()
# #//Check output q0 -> q4
circuit.x(qreg_q[0])
# circuit.x(qreg_q[1])
circuit.x(qreg_q[2])
# # circuit.x(qreg_q[3])
circuit.x(qreg_q[4])
gate = MCXGate(5)
circuit.append(gate, [0,1,2,3,4,10])
circuit.barrier()
circuit.x(qreg_q[0])
# circuit.x(qreg_q[1])
circuit.x(qreg_q[2])
# # circuit.x(qreg_q[3])
circuit.x(qreg_q[4])
# #End check output
# #REV
# # REV Add roundkey
circuit.barrier()

circuit.cx(qreg_q[9], qreg_q[4])
circuit.cx(qreg_q[8], qreg_q[3])
circuit.cx(qreg_q[7], qreg_q[2])
circuit.cx(qreg_q[6], qreg_q[1])
circuit.cx(qreg_q[5], qreg_q[0])
#REV KEY GEN
circuit.barrier()
circuit.cx(qreg_q[7], qreg_q[9])
circuit.cx(qreg_q[6], qreg_q[8])
circuit.cx(qreg_q[5], qreg_q[7])
circuit.cx(qreg_q[9], qreg_q[6])
circuit.cx(qreg_q[8], qreg_q[5])
# # Add roundkey
circuit.barrier()
circuit.cx(qreg_q[9], qreg_q[4])
circuit.cx(qreg_q[8], qreg_q[3])
circuit.cx(qreg_q[7], qreg_q[2])
circuit.cx(qreg_q[6], qreg_q[1])
circuit.cx(qreg_q[5], qreg_q[0])
# #End Rev 
circuit.barrier()
#Grover Diffusion
#//////////////
circuit.h(qreg_q[5])
circuit.h(qreg_q[8])
circuit.h(qreg_q[9])
circuit.h(qreg_q[6])
circuit.h(qreg_q[7])

circuit.x(qreg_q[5])
circuit.x(qreg_q[6])
circuit.x(qreg_q[7])
circuit.x(qreg_q[8])
circuit.x(qreg_q[9])

circuit.h(qreg_q[9])
gate = MCXGate(4)
circuit.append(gate, [5,6,7,8,9])
circuit.h(qreg_q[9])
circuit.x(qreg_q[5])
circuit.x(qreg_q[6])
circuit.x(qreg_q[7])
circuit.x(qreg_q[8])
circuit.x(qreg_q[9])

circuit.h(qreg_q[5])
circuit.h(qreg_q[8])
circuit.h(qreg_q[9])
circuit.h(qreg_q[6])
circuit.h(qreg_q[7])
# Measurement
circuit.h(qreg_a[0])
circuit.measure(qreg_q[5], creg_c0[0])
circuit.measure(qreg_q[6], creg_c0[1])
circuit.measure(qreg_q[7], creg_c0[2])
circuit.measure(qreg_q[8], creg_c0[3])
circuit.measure(qreg_q[9], creg_c0[4])
circuit.draw("mpl",initial_state = True,fold = 58, interactive= True)
plt.show()
print(dict(circuit.count_ops()))
print(circuit.depth())
aersim = AerSimulator()
# Perform an ideal simulation

result_ideal = aersim.run(circuit, shots = 10000000).result()
counts_ideal = result_ideal.get_counts(0)
#sorting the result
sorted_counts = dict(sorted(counts_ideal.items(), key=lambda item: -item[1])) 
# sorted_counts = dict(sorted(counts_ideal.items())) 

print(sorted_counts)

plot_histogram(sorted_counts, title='Result').show()
plt.show()


# Construct a simulator using a noise model
# from a real backend.
provider = QiskitRuntimeService()
backend = provider.get_backend("ibm_brisbane")
aersim_backend = AerSimulator.from_backend(backend)

# # Perform noisy simulation
result_noise = aersim_backend.run(circuit,shots = 10000).result()
counts_noise = result_noise.get_counts(0)
sorted_counts = dict(sorted(counts_noise.items(), key=lambda item: -item[1])) 
print('Counts(real backend):', sorted_counts)

plot_histogram(sorted_counts, title='Result').show()
plt.show()


