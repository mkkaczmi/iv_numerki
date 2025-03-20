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
    
    # Replace e^(-x) and similar expressions with exp(-x)
    expression = re.sub(r'e\^(\([^)]+\))', r'exp\1', expression)  # Handle expressions in parentheses
    expression = re.sub(r'e\^(-?x)', r'exp(\1)', expression)      # Handle -x or x
    expression = re.sub(r'e\^(\d+)', r'exp(\1)', expression)      # Handle numbers
    
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
            return eval(expression, {"np": np, "x": x})
        except Exception as e:
            raise ValueError(f"Error evaluating function: {e}")
    
    return custom_function

def get_user_input() -> Tuple[Callable[[float], float], float, float, float, int, bool]:
    """
    Get input from user for function selection and parameters.
    
    Returns:
        Tuple of (selected function, interval start, interval end, epsilon, max iterations, use_epsilon_condition)
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
                if not re.match(r'^[0-9x\s\+\-\*\/\^\(\)\.\,a-z\s]+$', expression):
                    print("Invalid characters in expression. Use only numbers, x, basic operators, and function names.")
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
    
    print("\nChoose stop condition:")
    print("1. |x_i - x_(i-1)| < ε")
    print("2. Maximum number of iterations")
    
    while True:
        try:
            stop_choice = int(input("\nSelect stop condition (1 or 2): "))
            if stop_choice in [1, 2]:
                break
            print("Invalid choice. Please enter 1 or 2.")
        except ValueError:
            print("Please enter a valid number.")
    
    use_epsilon_condition = (stop_choice == 1)
    
    return selected_function, a, b, epsilon, max_iterations, use_epsilon_condition

def check_root_existence(f: Callable[[float], float], a: float, b: float) -> str:
    """
    Check if a root exists in the interval by checking signs at endpoints.
    
    Returns:
        Message describing the situation with roots
    """
    fa = f(a)
    fb = f(b)
    
    if fa * fb > 0:
        return "No root guaranteed in this interval (same signs at endpoints)"
    elif fa * fb < 0:
        return "At least one root exists in this interval"
    else:  # fa * fb == 0
        if fa == 0:
            return f"Root found at x = {a}"
        else:
            return f"Root found at x = {b}"

def main():
    """Main program function."""
    print("Root Finding Methods Comparison")
    print("==============================")
    
    # Get user input
    f, a, b, epsilon, max_iterations, use_epsilon_condition = get_user_input()
    
    # Check root existence and print message
    root_message = check_root_existence(f, a, b)
    print(f"\nRoot existence check: {root_message}")
    
    if "No root guaranteed" in root_message:
        print("\nWarning: Function has the same sign at both endpoints!")
        print("This means either:")
        print("1. There is no root in this interval, or")
        print("2. There is an even number of roots in this interval")
        proceed = input("\nDo you want to try finding roots anyway? (y/n): ")
        if proceed.lower() != 'y':
            # Plot the function without roots to help visualize
            plot_function_and_roots(f, [], a, b)
            return
    
    print("\nCalculating roots...")
    
    # Find roots using both methods
    try:
        bisection_root, bisection_iterations = bisection_method(
            f, a, b, epsilon, max_iterations, use_epsilon_condition
        )
        print(f"\nBisection Method:")
        if bisection_root is not None:
            print(f"Root: {bisection_root:.6f}")
            print(f"Iterations: {bisection_iterations}")
            print(f"f(root) = {f(bisection_root):.10f}")
        else:
            print("No root found in the given interval")
            print(f"Iterations performed: {bisection_iterations}")
    except ValueError as e:
        print(f"\nBisection Method Error: {e}")
        bisection_root = None
    
    try:
        secant_root, secant_iterations = secant_method(
            f, a, b, epsilon, max_iterations, use_epsilon_condition
        )
        print(f"\nSecant Method:")
        if secant_root is not None:
            print(f"Root: {secant_root:.6f}")
            print(f"Iterations: {secant_iterations}")
            print(f"f(root) = {f(secant_root):.10f}")
        else:
            print("No root found in the given interval")
            print(f"Iterations performed: {secant_iterations}")
    except Exception as e:
        print(f"\nSecant Method Error: {e}")
        secant_root = None
    
    # Plot results only if roots were found
    roots = [root for root in [bisection_root, secant_root] if root is not None]
    if roots:
        plot_function_and_roots(f, roots, a, b)
    else:
        plot_function_and_roots(f, [], a, b)  # Plot function without roots

if __name__ == "__main__":
    main()