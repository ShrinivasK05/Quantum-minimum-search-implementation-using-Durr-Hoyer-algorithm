# Quantum Minimum Search using the Dürr-Høyer Algorithm

This project implements the **Dürr-Høyer algorithm**, a quantum approach for finding the **minimum value in an unsorted list**, leveraging **Grover’s search algorithm** and **quantum superposition** principles. The implementation includes both **Qiskit (Python)** for quantum simulation and a **C-based version** for FPGA simulation, validating its feasibility across hardware and quantum platforms.

## Project Title

**"Realizing the Quantum Circuit to Implement the Dürr-Høyer Algorithm"**

## Key Concepts

- **Quantum Superposition**
- **Amplitude Amplification (Grover’s Search)**
- **Quantum Oracle Construction**
- **Threshold Updating**
- **FPGA-based Quantum-Inspired Simulation**

##  Algorithm Overview

The algorithm aims to find the minimum element in an unsorted array using quantum principles:

1. **Initialize Registers**: Prepare quantum states using Hadamard gates.
2. **Apply Oracle**: Mark states with values less than the current threshold.
3. **Grover Diffusion**: Amplify marked states.
4. **Update Threshold**: Replace if a better candidate is found.
5. **Repeat**: Iterate until the best minimum is identified with high probability.
6. **Measurement**: Final state collapses to the index of the minimum value.

##  Tools and Platforms

- **Python**: Qiskit, NumPy, Matplotlib
- **Quantum Simulators**: IBM QASM Simulator
- **Hardware Simulation**: C implementation for FPGA (e.g., ZedBoard)


