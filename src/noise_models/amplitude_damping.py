# src/noise_models/amplitude_damping.py

from qiskit_aer.noise import amplitude_damping_error, NoiseModel
from .base_noise import BaseNoise

class AmplitudeDampingNoise(BaseNoise):
    """
    Amplitude damping noise, modeling energy loss (e.g., qubit relaxation to |0>).
    Useful for studying irreversible energy decay and its effect on quantum states.
    """
    def apply(self, noise_model: NoiseModel, gate_list: list, qubits_for_error: int = None) -> None:
        # Only apply amplitude damping to single-qubit gates
        valid_gates = [g for g in gate_list if g in ["id", "u1", "u2", "u3"]]
        if not valid_gates:
            self.log_noise_application(
                noise_type="AMPLITUDE_DAMPING",
                gates=gate_list,
                extra_info={"warning": "No valid 1-qubit gates found, skipping"}
            )
            return

        # Amplitude damping is always 1-qubit, so ignore qubits_for_error
        noise = amplitude_damping_error(self.error_rate)
        noise_model.add_all_qubit_quantum_error(noise, valid_gates)
        self.log_noise_application(
            noise_type="AMPLITUDE_DAMPING",
            gates=valid_gates,
            extra_info={"error_rate": self.error_rate}
        )
