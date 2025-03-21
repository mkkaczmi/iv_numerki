import numpy as np
from typing import Callable, Dict
from horner import evaluate_polynomial

def polynomial(x: float) -> float:
    """Example polynomial function: x^3 - 2x^2 + 4x - 8"""
    coefficients = [1, -2, 4, -8]  # coefficients from highest to lowest degree
    return evaluate_polynomial(x, coefficients, len(coefficients))

def trigonometric(x: float) -> float:
    """Example trigonometric function: sin(x) + cos(x)"""
    return np.sin(x) + np.cos(x)

def exponential(x: float) -> float:
    """Example exponential function: e^x - 2"""
    return np.exp(x) - 2

def composite(x: float) -> float:
    """Example composite function: sin(x^2) + e^(-x)"""
    return np.sin(x**2) + np.exp(-x)

# Dictionary of available functions
AVAILABLE_FUNCTIONS: Dict[str, Callable[[float], float]] = {
    "polynomial": polynomial,
    "trigonometric": trigonometric,
    "exponential": exponential,
    "composite": composite
}