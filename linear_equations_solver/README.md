# Linear Equations Solver

This project implements a system for solving linear equations using Gaussian elimination.

## Features

- Implementation of Gaussian elimination method
- Support for systems of up to 10 equations
- Multiple input methods:
  - File input
  - Manual input
  - Dataset processing
- Error handling for:
  - Inconsistent systems
  - Indeterminate systems
  - Invalid input

## Requirements

- Python 3.x
- NumPy

## Usage

1. Run the main script:
   ```bash
   python main.py
   ```

2. Choose from the following options:
   - Load equations from a file
   - Enter equations manually
   - Solve all systems from the dataset directory
   - Exit the program

## Input Format

### File Input
Create a text file with the following format:
```
n
a11 a12 ... a1n b1
a21 a22 ... a2n b2
...
an1 an2 ... ann bn
```
where:
- n is the number of equations
- aij are coefficients
- bi are constants

### Manual Input
Follow the prompts to enter:
1. Number of equations (1-10)
2. Coefficients for each equation

## Example

For the system:
```
2x + y = 5
x - y = 1
```

Input file format:
```
2
2 1 5
1 -1 1
```

## License

This project is licensed under the MIT License. 