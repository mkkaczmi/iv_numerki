from typing import Tuple, Callable
from functions import AVAILABLE_FUNCTIONS
from root_finding import bisection_method, secant_method
from plotting import plot_function_and_roots
import numpy as np
import re

def create_custom_function(expression: str) -> Callable[[float], float]:
    """
    Create a function from a string expression.
    
    Args:
        expression: Mathematical expression as string
        
    Returns:
        Callable function that evaluates the expression
    """
    # Replace mathematical functions with numpy equivalents
    expression = expression.lower()
    
    # Replace x^n with x**n for power operations
    expression = re.sub(r'x\^(\d+)', r'x**\1', expression)
    expression = re.sub(r'(\d+)\^(\d+)', r'\1**\2', expression)
    
    # Add multiplication operator between number and x
    expression = re.sub(r'(\d+)x', r'\1*x', expression)
    
    # Replace mathematical functions with numpy equivalents
    expression = expression.replace('sin', 'np.sin')
    expression = expression.replace('cos', 'np.cos')
    expression = expression.replace('tan', 'np.tan')
    expression = expression.replace('exp', 'np.exp')
    expression = expression.replace('log', 'np.log')
    expression = expression.replace('sqrt', 'np.sqrt')
    
    # Create a function that evaluates the expression
    def custom_function(x: float) -> float:
        try:
            return eval(expression)
        except Exception as e:
            raise ValueError(f"Error evaluating function: {e}")
    
    return custom_function

def get_user_input() -> Tuple[Callable[[float], float], float, float, float, int]:
    """
    Get input from user for function selection and parameters.
    
    Returns:
        Tuple of (selected function, interval start, interval end, epsilon, max iterations)
    """
    print("\nChoose input method:")
    print("1. Use predefined function")
    print("2. Enter custom function")
    
    while True:
        try:
            input_choice = int(input("\nSelect input method (1 or 2): "))
            if input_choice in [1, 2]:
                break
            print("Invalid choice. Please enter 1 or 2.")
        except ValueError:
            print("Please enter a valid number.")
    
    if input_choice == 1:
        print("\nAvailable predefined functions:")
        for i, name in enumerate(AVAILABLE_FUNCTIONS.keys(), 1):
            print(f"{i}. {name}")
        
        while True:
            try:
                choice = int(input("\nSelect function (enter number): "))
                if 1 <= choice <= len(AVAILABLE_FUNCTIONS):
                    break
                print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a valid number.")
        
        selected_function = list(AVAILABLE_FUNCTIONS.values())[choice - 1]
    else:
        print("\nEnter your function as a mathematical expression.")
        print("Available functions: sin, cos, tan, exp, log, sqrt")
        print("Use x as the variable. Example: x**2 + 2*x - 1")
        print("or sin(x) + cos(x)")
        
        while True:
            try:
                expression = input("\nEnter function: ").strip()
                if not expression:
                    print("Expression cannot be empty.")
                    continue
                    
                # Basic validation of the expression
                if not re.match(r'^[0-9x\s\+\-\*\/\^\(\)\.\,\s]+$', expression):
                    print("Invalid characters in expression. Use only numbers, x, and basic operators.")
                    continue
                    
                # Test the function with a sample value
                test_func = create_custom_function(expression)
                test_func(0.0)  # Test with x = 0
                selected_function = test_func
                break
            except Exception as e:
                print(f"Invalid function: {e}")
                print("Please try again.")
    
    while True:
        try:
            a = float(input("Enter interval start: "))
            b = float(input("Enter interval end: "))
            if a >= b:
                print("Interval start must be less than interval end.")
                continue
            break
        except ValueError:
            print("Please enter valid numbers.")
    
    while True:
        try:
            epsilon = float(input("Enter convergence tolerance (ε): "))
            if epsilon <= 0:
                print("Tolerance must be positive.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")
    
    while True:
        try:
            max_iterations = int(input("Enter maximum number of iterations: "))
            if max_iterations <= 0:
                print("Number of iterations must be positive.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")
    
    return selected_function, a, b, epsilon, max_iterations

def main():
    """Main program function."""
    print("Root Finding Methods Comparison")
    print("==============================")
    
    # Get user input
    f, a, b, epsilon, max_iterations = get_user_input()
    
    # Check if function has opposite signs at endpoints
    if f(a) * f(b) >= 0:
        print("\nWarning: Function does not have opposite signs at endpoints!")
        print("This may lead to incorrect results or no convergence.")
        proceed = input("Do you want to continue? (y/n): ")
        if proceed.lower() != 'y':
            return
    
    print("\nCalculating roots...")
    
    # Find roots using both methods
    try:
        bisection_root, bisection_iterations = bisection_method(f, a, b, epsilon, max_iterations)
        print(f"\nBisection Method:")
        print(f"Root: {bisection_root:.6f}")
        print(f"Iterations: {bisection_iterations}")
        print(f"f(root) = {f(bisection_root):.10f}")
    except ValueError as e:
        print(f"\nBisection Method Error: {e}")
        bisection_root = None
    
    try:
        # For secant method, use the endpoints of the interval
        secant_root, secant_iterations = secant_method(f, a, b, epsilon, max_iterations)
        print(f"\nSecant Method:")
        print(f"Root: {secant_root:.6f}")
        print(f"Iterations: {secant_iterations}")
        print(f"f(root) = {f(secant_root):.10f}")
    except Exception as e:
        print(f"\nSecant Method Error: {e}")
        secant_root = None
    
    # Plot results
    roots = [root for root in [bisection_root, secant_root] if root is not None]
    if roots:
        plot_function_and_roots(f, roots, a, b)

if __name__ == "__main__":
    main()