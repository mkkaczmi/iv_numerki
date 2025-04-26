# Nonlinear Equations Solver

This project implements and compares two methods for finding roots (zeros) of nonlinear equations:
1. Bisection Method
2. Secant Method

## Features

- Implementation of both bisection and secant methods
- Comparison of method performance
- Visualization of results
- Support for various types of nonlinear equations

## Requirements

- Python 3.x
- NumPy
- Matplotlib

## Usage

1. Run the main script:
   ```bash
   python main.py
   ```

2. Follow the on-screen instructions to:
   - Choose the method (bisection or secant)
   - Input the function
   - Set the interval [a, b]
   - Set the precision (epsilon)

## Example

For the equation f(x) = x^2 - 4:
- Choose method
- Input function: x**2 - 4
- Set interval: [1, 3]
- Set precision: 0.0001

The program will find the root and display the results.

## License

This project is licensed under the MIT License. 