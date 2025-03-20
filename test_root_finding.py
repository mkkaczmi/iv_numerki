from main import check_root_existence, create_custom_function
from root_finding import bisection_method, secant_method
from functions import AVAILABLE_FUNCTIONS
import numpy as np

def run_tests():
    # Test parameters
    epsilon = 0.0001
    max_iterations = 100
    
    # Test cases from example_functions.txt
    test_cases = [
        # Polynomial Functions
        ("x^3 - 2*x^2 + 4*x - 8", 0, 4),      # Expected root ≈ 2
        ("x^4 - 3*x^2 + 2", -2, 2),           # Expected roots ≈ ±1, ±√2
        ("x^5 - 5*x^3 + 4*x", -3, 3),         # Expected roots: 0, ±1, ±2
        ("x^2 + 2*x + 1", -2, 0),             # Expected root: -1
        ("x^3 + 3*x^2 + 3*x + 1", -2, 0),     # Expected root: -1
        
        # Non-polynomial functions (these will use standard evaluation)
        ("sin(x) + cos(x)", 2, 4),
        ("e^x - 2", 0, 2),
        ("sin(x^2) + e^(-x)", 0, 3)
    ]
    
    print("Root Finding Methods Test Results")
    print("================================")
    print(f"Epsilon: {epsilon}")
    print(f"Maximum iterations: {max_iterations}\n")
    
    for i, (func_str, a, b) in enumerate(test_cases, 1):
        print(f"\nTest {i}: {func_str}")
        print(f"Interval: [{a}, {b}]")
        
        try:
            f = create_custom_function(func_str)
        except Exception as e:
            print(f"Error creating function: {e}")
            continue
        
        root_message = check_root_existence(f, a, b)
        print(f"Root existence check: {root_message}")
        
        try:
            bisection_root, bisection_iter = bisection_method(f, a, b, epsilon, max_iterations)
            if bisection_root is not None:
                print(f"Bisection Method - Root: {bisection_root:.6f}, Iterations: {bisection_iter}")
                print(f"f(root) = {f(bisection_root):.10f}")
            else:
                print("Bisection Method - No root found")
        except Exception as e:
            print(f"Bisection Method Error: {e}")
        
        try:
            secant_root, secant_iter = secant_method(f, a, b, epsilon, max_iterations)
            if secant_root is not None:
                print(f"Secant Method - Root: {secant_root:.6f}, Iterations: {secant_iter}")
                print(f"f(root) = {f(secant_root):.10f}")
            else:
                print("Secant Method - No root found")
        except Exception as e:
            print(f"Secant Method Error: {e}")
        
        print("-" * 50)

if __name__ == "__main__":
    run_tests() 