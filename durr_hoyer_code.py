import matplotlib.pyplot as plt
import numpy as np
from qiskit import Aer, ClassicalRegister, QuantumCircuit, QuantumRegister, execute
from qiskit.circuit.library import GroverOperator

def create_oracle(threshold, num_qubits, index_register):
    """Creates a quantum oracle that marks indices below the threshold."""
    oracle = QuantumCircuit(index_register)
    binary_threshold = f"{threshold:0{num_qubits}b}"
    for i, bit in enumerate(reversed(binary_threshold)):
        if bit == "0":
            oracle.x(index_register[i])

    # Apply logic to build oracle (multi-controlled Z gate)
    oracle.h(index_register[-1])
    oracle.mcx(list(range(num_qubits - 1)), index_register[-1])
    oracle.h(index_register[-1])
    oracle.name = f"Oracle (Threshold={threshold})"
    return oracle

def durr_hoyer(num_items, example_array):
    """Implements the Dürr-Høyer algorithm and visualizes results."""
    num_qubits = int(np.ceil(np.log2(num_items)))

    # Initialize registers
    index_register = QuantumRegister(num_qubits, "q")
    classical_register = ClassicalRegister(num_qubits, "c")
    combined_circuit = QuantumCircuit(index_register, classical_register)

    # Initialization step
    combined_circuit.h(index_register)

    # Start with maximum value as initial guess for minimum
    min_value = float("inf")
    min_index = None
    final_counts = None  # To store the counts of the final iteration

    for threshold in range(num_items - 1, -1, -1):  # Iterate through all possible thresholds
        oracle = create_oracle(threshold, num_qubits, index_register)
        grover_op = GroverOperator(oracle=oracle)

        # Apply the Grover operator
        combined_circuit.append(grover_op, index_register)

        # Add measurements to test results for this threshold (not part of the combined circuit)
        temp_circuit = combined_circuit.copy()
        temp_circuit.measure(index_register, classical_register)

        # Simulation
        simulator = Aer.get_backend("qasm_simulator")
        result = execute(temp_circuit, simulator, shots=1024).result()
        counts = result.get_counts()

        # Store the counts for visualization if this is the best threshold so far
        if counts:
            most_frequent_index = max(counts, key=counts.get)
            current_value = example_array[int(most_frequent_index, 2)]
            if current_value < min_value:
                min_value = current_value
                min_index = most_frequent_index
                final_counts = counts  # Update with the best iteration's counts

    if min_index is None:
        print("No results found satisfying the oracle's condition.")
        return

    # Display the combined quantum circuit
    #print("\nFinal Combined Quantum Circuit:")
    combined_circuit.measure(index_register, classical_register)  # Add final measurement
    combined_circuit.draw("mpl", scale=0.8)  # Display the circuit
    plt.show()

    # Display the results
    print("\nIndex of the Minimum Value:", min_index)
    print("Minimum Value in the Array:", min_value)

    # Display counts
    print("\nMeasurement Counts:")
    for outcome, count in final_counts.items():
        print(f" Outcome {outcome}: {count} counts")

    # Plot histogram of the final counts
    plt.bar(final_counts.keys(), final_counts.values(), color='blue', alpha=0.7)
    plt.xlabel('Measurement Outcome')
    plt.ylabel('Counts')
    plt.title('Measurement Results for the Minimum Value')
    plt.xticks(rotation=90)
    plt.show()

# Example usage
num_items = 8  # Number of items in the list (or range of values)
example_array = [5, 2, 8, 1, 7, 3, 6, 4]  # Example array
durr_hoyer(num_items, example_array)
# Visualize the circuit
print("\nQuantum Circuit:")
#print(circuit.draw(output='text'))

# Display the circuit as a diagram
circuit.draw('mpl')
