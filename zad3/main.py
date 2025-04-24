import numpy as np
import matplotlib.pyplot as plt
from typing import List, Callable

# Przykładowe funkcje
def linear_function(x: float) -> float:
    return 2 * x + 1

def absolute_function(x: float) -> float:
    return abs(x)

def polynomial_function(x: float) -> float:
    return x**3 - 2*x**2 + x - 1

def trigonometric_function(x: float) -> float:
    return np.sin(x) + np.cos(2*x)

def evaluate_polynomial(x: float, coefficients: List[float]) -> float:
    result = 0
    for coef in coefficients:
        result = result * x + coef
    return result

def create_polynomial_function(coefficients: List[float]) -> Callable[[float], float]:
    return lambda x: evaluate_polynomial(x, coefficients)

def apply_trigonometric(x: float, trig_type: int, a: float, b: float, c: float, d: float) -> float:
    if trig_type == 1:
        return a * np.sin(b * x + c) + d
    elif trig_type == 2:
        return a * np.cos(b * x + c) + d
    else:
        return a * np.tan(b * x + c) + d

def create_function(function_type: str, polynomial_degree: int = None) -> Callable[[float], float]:
    if function_type == 'polynomial':
        print(f"\nPodaj {polynomial_degree + 1} współczynników (od najwyższego do najniższego stopnia):")
        coefficients = []
        for i in range(polynomial_degree + 1):
            coef = float(input(f"Współczynnik przy x^{polynomial_degree - i}: "))
            coefficients.append(coef)
        return create_polynomial_function(coefficients)
    
    elif function_type == 'trigonometric':
        print("\nWybierz funkcję trygonometryczną:")
        print("1. Sinus (sin)")
        print("2. Cosinus (cos)")
        print("3. Tangens (tan)")
        trig_choice = int(input("Podaj wybór (1-3): "))
        
        print("\nPodaj parametry dla funkcji a*f(bx + c) + d")
        a = float(input("a = "))
        b = float(input("b = "))
        c = float(input("c = "))
        d = float(input("d = "))
        
        return lambda x: apply_trigonometric(x, trig_choice, a, b, c, d)

def calculate_divided_differences(x: List[float], y: List[float]) -> List[float]:
    n = len(x)
    f = np.zeros((n, n))
    f[:, 0] = y
    
    for j in range(1, n):
        for i in range(n - j):
            f[i, j] = (f[i+1, j-1] - f[i, j-1]) / (x[i+j] - x[i])
    
    return f[0, :]

def newton_interpolation(x: List[float], y: List[float], x_eval: float) -> float:
    n = len(x)
    f = calculate_divided_differences(x, y)
    result = f[0]
    
    for i in range(1, n):
        term = f[i]
        for j in range(i):
            term *= (x_eval - x[j])
        result += term
    
    return result

def read_input_from_file(filename: str) -> tuple[List[float], List[float]]:
    x = []
    y = []
    with open(filename, 'r') as file:
        for line in file:
            if line.strip():
                xi, yi = map(float, line.strip().split())
                x.append(xi)
                y.append(yi)
    return x, y

def plot_interpolation(x_nodes: List[float], y_nodes: List[float], 
                      original_func: Callable[[float], float], 
                      a: float, b: float, n_points: int = 1000):
    x_plot = np.linspace(a, b, n_points)
    y_original = [original_func(xi) for xi in x_plot]
    y_interpolated = [newton_interpolation(x_nodes, y_nodes, xi) for xi in x_plot]
    
    plt.figure(figsize=(10, 6))
    plt.plot(x_plot, y_original, label='Funkcja oryginalna')
    plt.plot(x_plot, y_interpolated, label='Wielomian interpolacyjny')
    plt.scatter(x_nodes, y_nodes, color='red', label='Węzły interpolacji')
    plt.legend()
    plt.grid(True)
    plt.title('Interpolacja Newtona')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()

def main():
    print("\nWybierz tryb:")
    print("1. Użyj przykładowych funkcji")
    print("2. Wprowadź własną funkcję")
    mode_choice = int(input("Podaj wybór (1-2): "))
    
    if mode_choice == 1:
        print("\nDostępne funkcje przykładowe:")
        print("1. Funkcja liniowa: 2x + 1")
        print("2. Funkcja modułowa: |x|")
        print("3. Funkcja wielomianowa: x^3 - 2x^2 + x - 1")
        print("4. Funkcja trygonometryczna: sin(x) + cos(2x)")
        
        choice = int(input("Wybierz funkcję (1-4): "))
        functions = {
            1: linear_function,
            2: absolute_function,
            3: polynomial_function,
            4: trigonometric_function
        }
        selected_function = functions[choice]
    else:
        print("\nWybierz typ funkcji:")
        print("1. Wielomian")
        print("2. Trygonometryczna")
        function_type = int(input("Podaj wybór (1-2): "))
        
        if function_type == 1:
            degree = int(input("Podaj stopień wielomianu: "))
            selected_function = create_function('polynomial', degree)
        else:
            selected_function = create_function('trigonometric')
    
    a = float(input("Podaj początek przedziału: "))
    b = float(input("Podaj koniec przedziału: "))
    n = int(input("Podaj liczbę węzłów interpolacji: "))
    
    print("\nWybierz metodę wprowadzania danych:")
    print("1. Wprowadzenie ręczne")
    print("2. Wczytanie z pliku")
    input_choice = int(input("Wybierz opcję (1-2): "))
    
    if input_choice == 1:
        x_nodes = np.linspace(a, b, n)
        y_nodes = [selected_function(xi) for xi in x_nodes]
    else:
        filename = input("Podaj nazwę pliku: ")
        x_nodes, y_nodes = read_input_from_file(filename)
    
    plot_interpolation(x_nodes, y_nodes, selected_function, a, b)

if __name__ == "__main__":
    main()
