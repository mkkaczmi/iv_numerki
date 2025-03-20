from typing import Tuple, Callable
import numpy as np

def bisection_method(
    f: Callable[[float], float],
    a: float,
    b: float,
    epsilon: float,
    max_iterations: int
) -> Tuple[float, int]:
    """
    Find root using bisection method.
    
    Args:
        f: Function to find root of
        a: Left endpoint of interval
        b: Right endpoint of interval
        epsilon: Tolerance for convergence
        max_iterations: Maximum number of iterations
        
    Returns:
        Tuple of (root, number of iterations)
    """
    if f(a) * f(b) >= 0:
        raise ValueError("Function must have opposite signs at endpoints")
    
    iterations = 0
    x_prev = a
    
    while iterations < max_iterations:
        c = (a + b) / 2
        if abs(c - x_prev) < epsilon:
            return c, iterations + 1
            
        if f(c) == 0:
            return c, iterations + 1
            
        if f(c) * f(a) < 0:
            b = c
        else:
            a = c
            
        x_prev = c
        iterations += 1
        
    return (a + b) / 2, iterations

def secant_method(
    f: Callable[[float], float],
    x0: float,
    x1: float,
    epsilon: float,
    max_iterations: int
) -> Tuple[float, int]:
    """
    Find root using secant method.
    
    Args:
        f: Function to find root of
        x0: First initial point
        x1: Second initial point
        epsilon: Tolerance for convergence
        max_iterations: Maximum number of iterations
        
    Returns:
        Tuple of (root, number of iterations)
    """
    iterations = 0
    x_prev = x0
    x_curr = x1
    
    while iterations < max_iterations:
        f_prev = f(x_prev)
        f_curr = f(x_curr)
        
        # Check if we found the root exactly
        if abs(f_curr) < epsilon:
            return x_curr, iterations + 1
        
        # Avoid division by very small numbers
        if abs(f_curr - f_prev) < epsilon:
            # If function values are very close, take a smaller step
            x_next = (x_curr + x_prev) / 2
        else:
            x_next = x_curr - f_curr * (x_curr - x_prev) / (f_curr - f_prev)
        
        # Check for convergence
        if abs(x_next - x_curr) < epsilon:
            # Additional check: return the point with smallest function value
            if abs(f(x_next)) < abs(f_curr):
                return x_next, iterations + 1
            else:
                return x_curr, iterations + 1
        
        x_prev = x_curr
        x_curr = x_next
        iterations += 1
    
    return x_curr, iterations