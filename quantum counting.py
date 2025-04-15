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
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import C4XGate
# def create_grover_oracle_gate():
#     qreg_q = QuantumRegister(10, 'q')  # 0-3: data, 4-9: key
#     qreg_a = QuantumRegister(1, 'a')   # ancilla
#     qc = QuantumCircuit(qreg_q, qreg_a, name="G")

#     # # plain text q0 -> q3
#     qc.x(qreg_q[0])
#     qc.x(qreg_q[1])

#     # Round 1 - Add roundkey
#     qc.cx(qreg_q[9], qreg_q[0])
#     qc.cx(qreg_q[5], qreg_q[1])
#     qc.cx(qreg_q[4], qreg_q[2])
#     qc.cx(qreg_q[7], qreg_q[3])

#     # Round 1 - S-box
#     qc.cx(qreg_q[2], qreg_q[1])
#     qc.x(qreg_q[0])
#     qc.ccx(qreg_q[1], qreg_q[2], qreg_q[3])
#     qc.ccx(qreg_q[1], qreg_q[3], qreg_q[2])
#     qc.cx(qreg_q[3], qreg_q[1])
#     qc.x(qreg_q[3])
#     qc.ccx(qreg_q[2], qreg_q[0], qreg_q[1])
#     qc.cx(qreg_q[0], qreg_q[2])
#     qc.cx(qreg_q[3], qreg_q[0])
#     qc.cx(qreg_q[1], qreg_q[2])
#     qc.id(qreg_q[0])
#     qc.id(qreg_q[0])
#     qc.ccx(qreg_q[1], qreg_q[2], qreg_q[3])
#     qc.id(qreg_q[0])
#     qc.swap(qreg_q[2], qreg_q[3])

#     # Round 1 - Linear
#     qc.swap(qreg_q[0], qreg_q[3])
#     qc.swap(qreg_q[2], qreg_q[3])
#     qc.swap(qreg_q[3], qreg_q[1])

#     # Round 2 - Add roundkey
#     qc.cx(qreg_q[6], qreg_q[0])
#     qc.cx(qreg_q[8], qreg_q[1])
#     qc.cx(qreg_q[9], qreg_q[2])
#     qc.cx(qreg_q[5], qreg_q[3])

#     # Round 2 - S-box
#     qc.cx(qreg_q[2], qreg_q[1])
#     qc.x(qreg_q[0])
#     qc.ccx(qreg_q[1], qreg_q[2], qreg_q[3])
#     qc.ccx(qreg_q[1], qreg_q[3], qreg_q[2])
#     qc.cx(qreg_q[3], qreg_q[1])
#     qc.x(qreg_q[3])
#     qc.ccx(qreg_q[2], qreg_q[0], qreg_q[1])
#     qc.cx(qreg_q[0], qreg_q[2])
#     qc.cx(qreg_q[3], qreg_q[0])
#     qc.cx(qreg_q[1], qreg_q[2])
#     qc.id(qreg_q[0])
#     qc.id(qreg_q[0])
#     qc.ccx(qreg_q[1], qreg_q[2], qreg_q[3])
#     qc.id(qreg_q[0])
#     qc.swap(qreg_q[2], qreg_q[3])

#     # Round 2 - Linear
#     qc.swap(qreg_q[0], qreg_q[3])
#     qc.swap(qreg_q[2], qreg_q[3])
#     qc.swap(qreg_q[3], qreg_q[1])

#     # Oracle marking
#     qc.x(qreg_q[1])
#     qc.x(qreg_q[2])
#     qc.x(qreg_q[3])
#     qc.append(C4XGate(), [qreg_q[3], qreg_q[0], qreg_q[1], qreg_q[2], qreg_a[0]])
#     qc.x(qreg_q[1])
#     qc.x(qreg_q[2])
#     qc.x(qreg_q[3])

#     # Reverse Round 2 - Linear
#     qc.swap(qreg_q[3], qreg_q[1])
#     qc.swap(qreg_q[2], qreg_q[3])
#     qc.swap(qreg_q[0], qreg_q[3])

#     # Reverse Round 2 - S-box
#     qc.swap(qreg_q[2], qreg_q[3])
#     qc.id(qreg_q[0])
#     qc.ccx(qreg_q[1], qreg_q[2], qreg_q[3])
#     qc.cx(qreg_q[3], qreg_q[0])
#     qc.cx(qreg_q[1], qreg_q[2])
#     qc.x(qreg_q[3])
#     qc.cx(qreg_q[0], qreg_q[2])
#     qc.ccx(qreg_q[2], qreg_q[0], qreg_q[1])
#     qc.cx(qreg_q[3], qreg_q[1])
#     qc.x(qreg_q[0])
#     qc.ccx(qreg_q[1], qreg_q[3], qreg_q[2])
#     qc.id(qreg_q[0])
#     qc.id(qreg_q[0])
#     qc.ccx(qreg_q[1], qreg_q[2], qreg_q[3])
#     qc.id(qreg_q[0])
#     qc.cx(qreg_q[2], qreg_q[1])
#     qc.id(qreg_q[3])
#     qc.id(qreg_q[3])
#     qc.id(qreg_q[1])
#     qc.id(qreg_q[0])
#     qc.id(qreg_q[2])

#     # Reverse Round 2 - Add roundkey
#     qc.cx(qreg_q[6], qreg_q[0])
#     qc.cx(qreg_q[8], qreg_q[1])
#     qc.cx(qreg_q[9], qreg_q[2])
#     qc.cx(qreg_q[5], qreg_q[3])

#     # Reverse Round 1 - Linear
#     qc.swap(qreg_q[3], qreg_q[1])
#     qc.swap(qreg_q[2], qreg_q[3])
#     qc.swap(qreg_q[0], qreg_q[3])

#     # Reverse Round 1 - S-box
#     qc.swap(qreg_q[2], qreg_q[3])
#     qc.id(qreg_q[0])
#     qc.ccx(qreg_q[1], qreg_q[2], qreg_q[3])
#     qc.cx(qreg_q[3], qreg_q[0])
#     qc.cx(qreg_q[1], qreg_q[2])
#     qc.x(qreg_q[3])
#     qc.cx(qreg_q[0], qreg_q[2])
#     qc.ccx(qreg_q[2], qreg_q[0], qreg_q[1])
#     qc.cx(qreg_q[3], qreg_q[1])
#     qc.x(qreg_q[0])
#     qc.ccx(qreg_q[1], qreg_q[3], qreg_q[2])
#     qc.id(qreg_q[0])
#     qc.id(qreg_q[0])
#     qc.ccx(qreg_q[1], qreg_q[2], qreg_q[3])
#     qc.id(qreg_q[0])
#     qc.cx(qreg_q[2], qreg_q[1])
#     qc.id(qreg_q[3])
#     qc.id(qreg_q[3])
#     qc.id(qreg_q[1])
#     qc.id(qreg_q[0])
#     qc.id(qreg_q[2])

#     # Reverse Round 1 - Add roundkey
#     qc.cx(qreg_q[9], qreg_q[0])
#     qc.cx(qreg_q[5], qreg_q[1])
#     qc.cx(qreg_q[4], qreg_q[2])
#     qc.cx(qreg_q[7], qreg_q[3])
#         # # plain text q0 -> q3
#     qc.x(qreg_q[0])
#     qc.x(qreg_q[1])

#     #Grover Diffusion
#     #//////////////
#     qc.h(qreg_q[6])
#     qc.h(qreg_q[5])
#     qc.h(qreg_q[4])
#     qc.h(qreg_q[7])
#     qc.h(qreg_q[8])
#     qc.h(qreg_q[9])
#     qc.x(qreg_q[8])
#     qc.x(qreg_q[9])
#     qc.x(qreg_q[7])
#     qc.x(qreg_q[6])
#     qc.x(qreg_q[5])
#     qc.x(qreg_q[4])
#     qc.h(qreg_q[9])
#     gate = MCXGate(5)
#     qc.append(gate, [4, 5, 6, 7, 8,9])
#     qc.h(qreg_q[9])
#     qc.x(qreg_q[8])
#     qc.x(qreg_q[9])
#     qc.x(qreg_q[4])
#     qc.x(qreg_q[5])
#     qc.x(qreg_q[6])
#     qc.x(qreg_q[7])
#     qc.h(qreg_q[4])
#     qc.h(qreg_q[5])
#     qc.h(qreg_q[6])
#     qc.h(qreg_q[7])
#     qc.h(qreg_q[8])
#     qc.h(qreg_q[9])

#     return qc.to_gate()

def create_grover_oracle_gate():
    qreg_q = QuantumRegister(10, 'q')  # 0-3: data, 4-9: key
    qreg_a = QuantumRegister(1, 'a')   # ancilla
    circuit = QuantumCircuit(qreg_q, qreg_a, name="G")
    # # plain text q0 -> q3
    circuit.x(qreg_q[2])
    circuit.x(qreg_q[3])
    circuit.x(qreg_q[4])
    circuit.cx(qreg_q[9], qreg_q[4])
    circuit.cx(qreg_q[8], qreg_q[3])
    circuit.cx(qreg_q[7], qreg_q[2])
    circuit.cx(qreg_q[6], qreg_q[1])
    circuit.cx(qreg_q[5], qreg_q[0])

    # #KEY GEN
    circuit.cx(qreg_q[8], qreg_q[5])
    circuit.cx(qreg_q[9], qreg_q[6])
    circuit.cx(qreg_q[5], qreg_q[7])
    circuit.cx(qreg_q[6], qreg_q[8])
    circuit.cx(qreg_q[7], qreg_q[9])
    # # Add roundkey
    circuit.cx(qreg_q[9], qreg_q[4])
    circuit.cx(qreg_q[8], qreg_q[3])
    circuit.cx(qreg_q[7], qreg_q[2])
    circuit.cx(qreg_q[6], qreg_q[1])
    circuit.cx(qreg_q[5], qreg_q[0])
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

    circuit.cx(qreg_q[9], qreg_q[4])
    circuit.cx(qreg_q[8], qreg_q[3])
    circuit.cx(qreg_q[7], qreg_q[2])
    circuit.cx(qreg_q[6], qreg_q[1])
    circuit.cx(qreg_q[5], qreg_q[0])
    #REV KEY GEN
    circuit.cx(qreg_q[7], qreg_q[9])
    circuit.cx(qreg_q[6], qreg_q[8])
    circuit.cx(qreg_q[5], qreg_q[7])
    circuit.cx(qreg_q[9], qreg_q[6])
    circuit.cx(qreg_q[8], qreg_q[5])
    # # Add roundkey
    circuit.cx(qreg_q[9], qreg_q[4])
    circuit.cx(qreg_q[8], qreg_q[3])
    circuit.cx(qreg_q[7], qreg_q[2])
    circuit.cx(qreg_q[6], qreg_q[1])
    circuit.cx(qreg_q[5], qreg_q[0])
    # #End Rev 
    ##REV Add Roundkey
    circuit.x(qreg_q[2])
    circuit.x(qreg_q[3])
    circuit.x(qreg_q[4])

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

    return circuit.to_gate()
# service = QiskitRuntimeService()
c = ClassicalRegister(5, 'c')
qreg_q = QuantumRegister(15, 'q')
qreg_a = QuantumRegister(1, 'a')
# creg_c0 = ClassicalRegister(6, 'c0')
circuit = QuantumCircuit(qreg_q, qreg_a,c)
# circuit.x(qreg_q[0])
# Quantum superposition + Phase kickback
# circuit.x(qreg_a[0])
for i in range(0,5):
    circuit.h(qreg_q[i])
for i in range(10,15):
    circuit.h(qreg_q[i])
circuit.x(qreg_a[0])
circuit.h(qreg_a[0])

#tao cong control

oracle_gate = create_grover_oracle_gate()
controlled_oracle_gate_0 = oracle_gate.control(1)
for i in range(0,1):
    circuit.append(controlled_oracle_gate_0, [qreg_q[4]] + list(qreg_q[5:]) + [qreg_a[0]])
for i in range(0,2):
    circuit.append(controlled_oracle_gate_0, [qreg_q[3]] + list(qreg_q[5:]) + [qreg_a[0]])
for i in range(0,4):
    circuit.append(controlled_oracle_gate_0, [qreg_q[2]] + list(qreg_q[5:]) + [qreg_a[0]])
for i in range(0,8):
    circuit.append(controlled_oracle_gate_0, [qreg_q[1]] + list(qreg_q[5:]) + [qreg_a[0]])
for i in range(0,16):
    circuit.append(controlled_oracle_gate_0, [qreg_q[0]] + list(qreg_q[5:]) + [qreg_a[0]])

circuit.swap(qreg_q[0],qreg_q[4])
circuit.swap(qreg_q[1],qreg_q[3])
circuit.h(qreg_q[4])
circuit.cp(-pi/2,qreg_q[4],qreg_q[3])
circuit.h(qreg_q[3])
circuit.cp(-pi/4,qreg_q[4],qreg_q[2])
circuit.cp(-pi/2,qreg_q[3],qreg_q[2])
circuit.h(qreg_q[2])
circuit.cp(-pi/8,qreg_q[4],qreg_q[1])
circuit.cp(-pi/4,qreg_q[3],qreg_q[1])
circuit.cp(-pi/2,qreg_q[2],qreg_q[1])
circuit.h(qreg_q[1])
circuit.cp(-pi/16,qreg_q[4],qreg_q[0])
circuit.cp(-pi/8,qreg_q[3],qreg_q[0])
circuit.cp(-pi/4,qreg_q[2],qreg_q[0])
circuit.cp(-pi/2,qreg_q[1],qreg_q[0])

circuit.h(qreg_q[0])

circuit.measure(qreg_q[0], c[4])
circuit.measure(qreg_q[1], c[3])
circuit.measure(qreg_q[2], c[2])
circuit.measure(qreg_q[3], c[1])
circuit.measure(qreg_q[4], c[0])

# circuit.append(controlled_oracle_gate_0, [qreg_q[0]] + list(qreg_q[4:]) + [qreg_a[0]])
# circuit.append(controlled_oracle_gate_1, [qreg_q[1]] + list(qreg_q[4:]) + [qreg_a[0]])
# circuit.append(controlled_oracle_gate_2, [qreg_q[2]] + list(qreg_q[4:]) + [qreg_a[0]])

# circuit.append(controlled_oracle_gate, [qreg_q[0]] + list(qreg_q[1:]) + [qreg_a[0]])
# circuit.append(controlled_oracle_gate, [qreg_q[0]] + list(qreg_q[1:]) + [qreg_a[0]])


# #//////////////
# #3 Grover iterator

# oracle_gate = create_grover_oracle_gate()
# circuit.append(oracle_gate, list(qreg_q) + [qreg_a[0]])
# circuit.append(oracle_gate, list(qreg_q) + [qreg_a[0]])
# circuit.append(oracle_gate, list(qreg_q) + [qreg_a[0]])


# #////////////////Measure
# circuit.h(qreg_a[0])
# for i in range(5,11):
#     circuit.measure(qreg_q[i], creg_c0[i-5])


# circuit.decompose()
circuit.draw("mpl")
plt.show()


aersim = AerSimulator()
# Perform an ideal simulation
result_ideal = aersim.run(circuit.decompose()).result()
counts_ideal = result_ideal.get_counts(0)
#sorting the result
sorted_counts = dict(sorted(counts_ideal.items(), key=lambda item: -item[1])) 
print(sorted_counts)

plot_histogram(sorted_counts, sort = 'value', title='Result').show()
plt.show()


# # Construct a simulator using a noise model
# # from a real backend.
# provider = QiskitRuntimeService()
# backend = provider.get_backend("ibm_brisbane")
# aersim_backend = AerSimulator.from_backend(backend)

# # Perform noisy simulation
# result_noise = aersim_backend.run(circuit).result()
# counts_noise = result_noise.get_counts(0)
# sorted_counts = dict(sorted(counts_noise.items(), key=lambda item: -item[1])) 

# print('Counts(real backend):', sorted_counts)

# plot_histogram(sorted_counts, sort = 'value', title='Result').show()
# plt.show()



