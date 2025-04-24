import numpy as np
import matplotlib.pyplot as plt

def compose_functions(functions):
    def composed(x):
        result = x
        for f in reversed(functions):
            result = f(result)
        return result
    return composed

def evaluate_polynomial(x, coefficients):
    result = 0
    for coef in coefficients:
        result = result * x + coef
    return result

def create_polynomial_function(coefficients):
    return lambda x: evaluate_polynomial(x, coefficients)

def apply_trigonometric(x, trig_type, a, b, c, d):
    if trig_type == 1:
        return a * np.sin(b * x + c) + d
    elif trig_type == 2:
        return a * np.cos(b * x + c) + d
    else:
        return a * np.tan(b * x + c) + d

def create_function(function_type, polynomial_degree=None):
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

def calculate_divided_differences(x, y):
    n = len(x)
    f = np.zeros((n, n))
    f[:, 0] = y
    
    for j in range(1, n):
        for i in range(n - j):
            f[i, j] = (f[i+1, j-1] - f[i, j-1]) / (x[i+j] - x[i])
    
    return f[0, :]

def newton_interpolation(x, y, x_eval):
    n = len(x)
    f = calculate_divided_differences(x, y)
    result = f[0]
    
    for i in range(1, n):
        term = f[i]
        for j in range(i):
            term *= (x_eval - x[j])
        result += term
    
    return result

def read_input_from_file(filename):
    x = []
    y = []
    with open(filename, 'r') as file:
        for line in file:
            if line.strip():
                xi, yi = map(float, line.strip().split())
                x.append(xi)
                y.append(yi)
    return x, y

def plot_interpolation(x_nodes, y_nodes, original_func, a, b, n_points=1000):
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
    n_compositions = int(input("Podaj liczbę składanych funkcji (1 dla pojedynczej funkcji): "))
    functions = []
    
    for i in range(n_compositions):
        print(f"\nFunkcja {i+1}:")
        print("Wybierz typ funkcji:")
        print("1. Liniowa")
        print("2. Modułowa")
        print("3. Wielomianowa")
        print("4. Trygonometryczna")
        
        function_type = int(input("Podaj wybór (1-4): "))
        
        if function_type == 1:
            print("\nPodaj parametry dla funkcji ax + b")
            a = float(input("a = "))
            b = float(input("b = "))
            functions.append(lambda x, a=a, b=b: a * x + b)
        elif function_type == 2:
            functions.append(lambda x: abs(x))
        elif function_type == 3:
            degree = int(input("Podaj stopień wielomianu: "))
            functions.append(create_function('polynomial', degree))
        else:
            functions.append(create_function('trigonometric'))
    
    selected_function = compose_functions(functions)
    
    a = float(input("Podaj początek przedziału: "))
    b = float(input("Podaj koniec przedziału: "))
    
    print("\nWybierz metodę wprowadzania danych:")
    print("1. Wprowadzenie ręczne")
    print("2. Wczytanie z pliku")
    input_choice = int(input("Wybierz opcję (1-2): "))
    
    if input_choice == 1:
        n = int(input("Podaj liczbę węzłów interpolacji: "))
        x_nodes = np.linspace(a, b, n)
        y_nodes = [selected_function(xi) for xi in x_nodes]
    else:
        filename = input("Podaj nazwę pliku: ")
        x_nodes, y_nodes = read_input_from_file(filename)
        n = len(x_nodes)
        print(f"Wczytano {n} węzłów interpolacji z pliku")
    
    plot_interpolation(x_nodes, y_nodes, selected_function, a, b)

if __name__ == "__main__":
    main()
