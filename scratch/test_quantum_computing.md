# Quantum Computing Fundamentals

This document provides a primer on quantum information science, qubits, and quantum circuit architectures.
Unlike classical bits which are deterministically 0 or 1, a qubit exists in a linear superposition of orthonormal basis states.

## Superposition and Bloch Sphere

A pure qubit state can be geometrically visualized on the surface of the Bloch sphere.
State vectors are described using Dirac bra-ket notation:
$$\psi = \alpha |0\rangle + \beta |1\rangle$$
where $\alpha$ and $\beta$ are complex probability amplitudes satisfying $|\alpha|^2 + |\beta|^2 = 1$.

### Quantum Gates and Unitary Transformations

Single-qubit operations correspond to rotations on the Bloch sphere represented by 2x2 unitary matrices.
The Hadamard gate (H) creates equal superposition from computational basis states.
Pauli-X serves as the quantum bit-flip NOT gate, while Pauli-Z applies a phase flip.

## Quantum Entanglement and Teleportation

Entanglement represents non-local quantum correlations with no classical counterpart.
The canonical maximally entangled two-qubit Bell states form an orthonormal basis for two-qubit Hilbert space.
Using a shared Bell pair and classical communication channels, quantum state teleportation faithfully transmits unknown quantum states without physical matter transfer.
