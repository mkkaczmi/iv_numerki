import numpy as np
import matplotlib.pyplot as plt
from typing import Callable, List

def plot_function_and_roots(
    f: Callable[[float], float],
    roots: List[float],
    a: float,
    b: float,
    title: str = "Function and its roots"
) -> None:
    """
    Plot the function and mark its roots.
    
    Args:
        f: Function to plot
        roots: List of roots to mark
        a: Left endpoint of interval
        b: Right endpoint of interval
        title: Title of the plot
    """
    x = np.linspace(a, b, 1000)
    y = [f(xi) for xi in x]
    
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, 'b-', label='Function')
    plt.axhline(y=0, color='k', linestyle='--', alpha=0.3)
    
    # Plot roots
    for root in roots:
        plt.plot(root, f(root), 'ro', label=f'Root: {root:.6f}')
    
    plt.title(title)
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.grid(True)
    plt.legend()
    plt.show()