# src/utils/validation.py

import numpy as np
from typing import Optional, List, Union, Type
from src.state_preparation.state_constants import STATE_CLASSES
from src.noise_models import NOISE_CLASSES


def validate_inputs(
    num_qubits: int,
    state_type: str,
    noise_type: str,
    sim_mode: str,
    angle: float = None,
    error_rate: float = None,
    z_prob: float = None,
    i_prob: float = None,
    t1: float = None,
    t2: float = None,
) -> None:
    """
    Validates input parameters for the experiment.
    """
    if num_qubits < 1:
        raise ValueError("Number of qubits must be at least 1.")

    valid_states = list(STATE_CLASSES.keys())
    if state_type not in valid_states:
        raise ValueError(
            f"Invalid state type: {state_type}. Choose from {valid_states}"
        )

    valid_noises = list(NOISE_CLASSES.keys())
    if noise_type not in valid_noises:
        raise ValueError(
            f"Invalid noise type: {noise_type}. Choose from {valid_noises}"
        )

    if sim_mode not in ["qasm", "density"]:
        raise ValueError(
            f"Invalid simulation mode: {sim_mode}. Choose from ['qasm', 'density']"
        )

    if state_type == "CLUSTER" and angle is not None:
        if not (0 <= angle <= 2 * np.pi):
            raise ValueError(
                "Angle for CLUSTER state must be between 0 and 2π radians."
            )

    if error_rate is not None and not (0 <= error_rate <= 1):
        raise ValueError("Error rate must be between 0 and 1.")

    if noise_type == "PHASE_FLIP" and (z_prob is not None or i_prob is not None):
        if z_prob is None or i_prob is None:
            raise ValueError(
                "Both z_prob and i_prob must be provided for PHASE_FLIP noise."
            )
        if not (
            0 <= z_prob <= 1 and 0 <= i_prob <= 1 and abs(z_prob + i_prob - 1) < 1e-10
        ):
            raise ValueError(
                "Z and I probabilities for PHASE_FLIP must sum to 1 and be between 0 and 1."
            )

    if noise_type == "THERMAL_RELAXATION" and (t1 is not None or t2 is not None):
        if t1 is None or t2 is None:
            raise ValueError(
                "Both t1 and t2 must be provided for THERMAL_RELAXATION noise."
            )
        if t1 <= 0 or t2 <= 0 or t2 > t1:
            raise ValueError(
                "T1 and T2 must be positive, with T2 <= T1 for realistic relaxation."
            )


class InputValidator:
    """Handles input validation for user prompts."""

    @staticmethod
    def validate_choice(
        user_input: str,
        valid_options: Optional[List[str]],
        case_sensitive: bool = False,
    ) -> bool:
        """
        Validates if the user input is one of the valid options.

        Args:
            user_input (str): The user's input.
            valid_options (List[str], optional): List of valid options.
            case_sensitive (bool): Whether the comparison should be case-sensitive.

        Returns:
            bool: True if the input is valid, False otherwise.
        """
        if not valid_options:
            return True
        if not case_sensitive:
            user_input = user_input.lower()
            valid_options = [opt.lower() for opt in valid_options]
        return user_input in valid_options

    @staticmethod
    def validate_numeric(
        user_input: str, expected_type: Type[Union[int, float]]
    ) -> Union[int, float, None]:
        """
        Validates and converts numeric input to the expected type.

        Args:
            user_input (str): The user's input.
            expected_type (Type[Union[int, float]]): The expected numeric type (int or float).

        Returns:
            Union[int, float, None]: The converted value if valid, None if invalid.
        """
        try:
            return expected_type(user_input)
        except ValueError:
            return None

    @staticmethod
    def validate_yes_no(user_input: str) -> bool:
        """
        Validates yes/no input.

        Args:
            user_input (str): The user's input.

        Returns:
            bool: True if yes, False if no or invalid.
        """
        return user_input.lower() in ["y", "yes", "t", "true"]
