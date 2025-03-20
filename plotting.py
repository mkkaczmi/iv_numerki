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
    y = []
    
    # Calculate y values with protection against very large values
    y_min, y_max = float('inf'), float('-inf')
    for xi in x:
        try:
            yi = f(xi)
            # Limit the y values to reasonable range
            if abs(yi) > 10:
                yi = np.sign(yi) * 10
            y.append(yi)
            y_min = min(y_min, yi)
            y_max = max(y_max, yi)
        except (ValueError, OverflowError):
            y.append(np.nan)  # Use NaN for undefined points
    
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, 'b-', label='Function')
    plt.axhline(y=0, color='k', linestyle='--', alpha=0.3)
    
    # Plot roots
    for root in roots:
        try:
            root_y = f(root)
            if abs(root_y) > 10:
                root_y = np.sign(root_y) * 10
            plt.plot(root, root_y, 'ro', label=f'Root: {root:.6f}')
        except (ValueError, OverflowError):
            continue
    
    # Set reasonable y-axis limits
    y_range = y_max - y_min
    plt.ylim([max(y_min - 0.1 * y_range, -10), min(y_max + 0.1 * y_range, 10)])
    
    plt.title(title)
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.grid(True)
    plt.legend()
    plt.show()