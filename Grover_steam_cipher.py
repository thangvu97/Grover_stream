from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.quantum_info import SparsePauliOp
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, EstimatorV2 as Estimator
from qiskit_aer import AerSimulator
from qiskit.circuit.library import MCXGate, C4XGate
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
from numpy import pi

def apply_plaintext(circuit, qreg_q):
    """Áp dụng plaintext vào các quantum register"""
    circuit.x(qreg_q[2])
    circuit.x(qreg_q[3])
    circuit.x(qreg_q[4])

def apply_first_round_key(circuit, qreg_q):
    """Áp dụng round key đầu tiên"""
    for i in range(5):
        circuit.cx(qreg_q[9-i], qreg_q[4-i])

def apply_key_generation(circuit, qreg_q):
    """Thực hiện quá trình sinh khóa"""
    circuit.cx(qreg_q[8], qreg_q[5])
    circuit.cx(qreg_q[9], qreg_q[6])
    circuit.cx(qreg_q[5], qreg_q[7])
    circuit.cx(qreg_q[6], qreg_q[8])
    circuit.cx(qreg_q[7], qreg_q[9])

def apply_output_check(circuit, qreg_q):
    """Kiểm tra output với cổng MCX"""
    circuit.x(qreg_q[0])
    circuit.x(qreg_q[2])
    circuit.x(qreg_q[4])
    gate = MCXGate(5)
    circuit.append(gate, [0,1,2,3,4,10])
    circuit.x(qreg_q[0])
    circuit.x(qreg_q[2])
    circuit.x(qreg_q[4])

def apply_reverse_operations(circuit, qreg_q):
    """Thực hiện các phép toán ngược lại"""
    apply_first_round_key(circuit, qreg_q)
    
    # Đảo ngược quá trình sinh khóa
    circuit.cx(qreg_q[7], qreg_q[9])
    circuit.cx(qreg_q[6], qreg_q[8])
    circuit.cx(qreg_q[5], qreg_q[7])
    circuit.cx(qreg_q[9], qreg_q[6])
    circuit.cx(qreg_q[8], qreg_q[5])
    
    apply_first_round_key(circuit, qreg_q)
    apply_plaintext(circuit, qreg_q)

def apply_grover_diffusion(circuit, qreg_q):
    """Áp dụng phép khuếch tán Grover"""
    # Áp dụng cổng H
    for i in [5,6,7,8,9]:
        circuit.h(qreg_q[i])
    
    # Áp dụng cổng X
    for i in range(5,10):
        circuit.x(qreg_q[i])
    
    # Thực hiện phép toán có điều kiện
    circuit.h(qreg_q[9])
    gate = MCXGate(4)
    circuit.append(gate, [5,6,7,8,9])
    circuit.h(qreg_q[9])
    
    # Đảo ngược cổng X
    for i in range(5,10):
        circuit.x(qreg_q[i])
    
    # Đảo ngược cổng H
    for i in [5,6,7,8,9]:
        circuit.h(qreg_q[i])

def create_grover_oracle_gate():
    """Tạo cổng Oracle cho thuật toán Grover"""
    qreg_q = QuantumRegister(10, 'q')  # 0-3: data, 4-9: key
    qreg_a = QuantumRegister(1, 'a')   # ancilla
    circuit = QuantumCircuit(qreg_q, qreg_a, name="G")

    apply_plaintext(circuit, qreg_q)
    apply_first_round_key(circuit, qreg_q)
    apply_key_generation(circuit, qreg_q)
    apply_first_round_key(circuit, qreg_q)
    apply_output_check(circuit, qreg_q)
    apply_reverse_operations(circuit, qreg_q)
    apply_grover_diffusion(circuit, qreg_q)

    return circuit.to_gate()

def initialize_quantum_circuit():
    """Khởi tạo mạch quantum"""
    qreg_q = QuantumRegister(10, 'q')
    qreg_a = QuantumRegister(1, 'a')
    creg_c0 = ClassicalRegister(5, 'c0')
    return QuantumCircuit(qreg_q, qreg_a, creg_c0), qreg_q, qreg_a, creg_c0

def apply_quantum_superposition(circuit, qreg_q, qreg_a):
    """Áp dụng chồng chất lượng tử và Phase kickback"""
    circuit.barrier()
    circuit.x(qreg_a[0])
    for i in range(5,10):
        circuit.h(qreg_q[i])
    circuit.h(qreg_a[0])

def apply_oracle_iterations(circuit, qreg_q, qreg_a, iterations=4):
    """Áp dụng cổng Oracle nhiều lần"""
    oracle_gate = create_grover_oracle_gate()
    for _ in range(iterations):
        circuit.append(oracle_gate, list(qreg_q[0:])+[qreg_a[0]])

def add_measurements(circuit, qreg_q, creg_c0):
    """Thêm phép đo vào mạch"""
    for i in range(5):
        circuit.measure(qreg_q[i+5], creg_c0[i])

def visualize_results(circuit, counts):
    """Hiển thị kết quả mô phỏng"""
    circuit.draw("mpl", initial_state=True, fold=58, interactive=True)
    plt.show()
    print("Số lượng cổng:", dict(circuit.count_ops()))
    print("Độ sâu mạch:", circuit.depth())
    plot_histogram(counts, title='Kết quả').show()
    plt.show()

def main():
    """Hàm chính thực thi chương trình"""
    # Khởi tạo mạch
    circuit, qreg_q, qreg_a, creg_c0 = initialize_quantum_circuit()
    
    # Áp dụng các phép toán quantum
    apply_quantum_superposition(circuit, qreg_q, qreg_a)
    apply_oracle_iterations(circuit, qreg_q, qreg_a)
    
    # Thêm phép đo
    circuit.h(qreg_a[0])
    add_measurements(circuit, qreg_q, creg_c0)
    
    # Mô phỏng và hiển thị kết quả
    aersim = AerSimulator()
    result = aersim.run(circuit.decompose(), shots=100000).result()
    counts = result.get_counts(0)
    sorted_counts = dict(sorted(counts.items(), key=lambda item: -item[1]))
    
    print("Kết quả đo:", sorted_counts)
    visualize_results(circuit, sorted_counts)

if __name__ == "__main__":
    main()
