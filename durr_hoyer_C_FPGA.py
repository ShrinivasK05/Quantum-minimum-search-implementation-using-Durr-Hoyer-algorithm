#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <complex.h>
#include <limits.h>

typedef double complex qampl;

void hadamard(qampl *state, int qubit, int num_qubits) {
    int num_states = 1 << num_qubits;
    for (int i = 0; i < num_states; i++) {
        if ((i >> qubit) & 1) {
            qampl temp = state[i];
            state[i] = (temp + state[i ^ (1 << qubit)]) / sqrt(2);
            state[i ^ (1 << qubit)] = (temp - state[i ^ (1 << qubit)]) / sqrt(2);
        }
    }
}

void cnot(qampl *state, int control, int target, int num_qubits) {
    int num_states = 1 << num_qubits;
    for (int i = 0; i < num_states; i++) {
        if (((i >> control) & 1) && !((i >> target) & 1)) {
            qampl temp = state[i];
            state[i] = state[i ^ (1 << target)];
            state[i ^ (1 << target)] = temp;
        }
    }
}

void phase_oracle(qampl *state, int threshold, int num_qubits) {
    int num_states = 1 << num_qubits;
    for (int i = 0; i < num_states; i++) {
        if (i < threshold) {
            state[i] *= -1;
        }
    }
}

void grover_diffusion(qampl *state, int num_qubits) {
    for (int i = 0; i < num_qubits; i++) {
        hadamard(state, i, num_qubits);
    }
    phase_oracle(state, 0, num_qubits);
    for (int i = 0; i < num_qubits; i++) {
        hadamard(state, i, num_qubits);
    }
}

int measure(qampl *state, int qubit, int num_qubits) {
    double probability_0 = 0.0;
    int num_states = 1 << num_qubits;

    for (int i = 0; i < num_states; i++) {
        if (!((i >> qubit) & 1)) {
probability_0 += (creal(state[i]) * creal(state[i])) + (cimag(state[i]) * cimag(state[i]));
        }
    }

    if ((double)rand() / RAND_MAX < probability_0) {
        return 0;
    } else {
        return 1;
    }
}

int main() {
    int num_qubits = 3;
    int num_states = 1 << num_qubits;
    qampl *state = (qampl *)malloc(num_states * sizeof(qampl));

    for (int i = 0; i < num_states; i++) {
        state[i] = (i == 0) ? 1.0 : 0.0;
    }

    for (int i = 0; i < num_qubits; i++) {
        hadamard(state, i, num_qubits);
    }

    int array[] = {5, 2, 8, 1, 7, 3, 6, 4};
    int min_value = INT_MAX;
    int min_index = -1;

    for (int threshold = num_states - 1; threshold >= 0; threshold--) {
        phase_oracle(state, threshold, num_qubits);
        grover_diffusion(state, num_qubits);

        int measured_index = 0;
        for (int i = 0; i < num_qubits; i++) {
            measured_index |= (measure(state, i, num_qubits) << i);
        }

        if (array[measured_index] < min_value) {
            min_value = array[measured_index];
            min_index = measured_index;
        }
    }

    printf("Index of Minimum Value: %d\n", min_index);
    printf("Minimum Value: %d\n", min_value);

    free(state);
    return 0;
}
