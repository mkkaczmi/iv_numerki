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

def predefined_functions():
    # Define the functions
    functions = {
        'a': lambda x: 2*x**3 + 5*x**2 + 2*x - 1,
        'b': lambda x: 2*np.cos(x) - 4*np.sin(x),
        'c': lambda x: abs(x - 6),
        'd': lambda x: abs(np.cos(x) - 1.5)
    }
    
    # Define intervals for each function
    intervals = {
        'a': (-3, 1),
        'b': (-2*np.pi, 2*np.pi),
        'c': (0, 12),
        'd': (-2*np.pi, 2*np.pi)
    }
    
    # Define node points for each function (less and more)
    nodes = {
        'a': {
            'less': [-3, -1.2, 0.3],
            'more': [-3, -2.7, -1.8, -0.4, 0.8]
        },
        'b': {
            'less': [-2*np.pi, -np.pi/2, np.pi/3, 3*np.pi/2],
            'more': [-2*np.pi, -5*np.pi/4, -np.pi/3, np.pi/4, 3*np.pi/2, 7*np.pi/4]
        },
        'c': {
            'less': [0, 2.5, 5.8, 8.2, 12],
            'more': [0, 1.2, 3.7, 5.1, 6.8, 8.9, 10.3, 12]
        },
        'd': {
            'less': [-2*np.pi, -4*np.pi/3, -np.pi/2, np.pi/3, 5*np.pi/4],
            'more': [-2*np.pi, -5*np.pi/3, -3*np.pi/4, -np.pi/6, np.pi/2, 4*np.pi/3, 7*np.pi/4]
        }
    }
    
    return functions, intervals, nodes

def plot_predefined_function(func_name, func, interval, nodes_less, nodes_more):
    a, b = interval
    x_plot = np.linspace(a, b, 1000)
    y_original = [func(xi) for xi in x_plot]
    
    # Plot for less nodes
    y_nodes_less = [func(xi) for xi in nodes_less]
    y_interpolated_less = [newton_interpolation(nodes_less, y_nodes_less, xi) for xi in x_plot]
    
    plt.figure(figsize=(10, 6))
    plt.plot(x_plot, y_original, label='Funkcja oryginalna')
    plt.plot(x_plot, y_interpolated_less, label='Wielomian interpolacyjny')
    plt.scatter(nodes_less, y_nodes_less, color='red', label='Węzły interpolacji')
    plt.legend()
    plt.grid(True)
    plt.title(f'Interpolacja Newtona - {func_name} (mniej węzłów)')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.savefig(f'{func_name}_less.png')
    plt.close()
    
    # Plot for more nodes
    y_nodes_more = [func(xi) for xi in nodes_more]
    y_interpolated_more = [newton_interpolation(nodes_more, y_nodes_more, xi) for xi in x_plot]
    
    plt.figure(figsize=(10, 6))
    plt.plot(x_plot, y_original, label='Funkcja oryginalna')
    plt.plot(x_plot, y_interpolated_more, label='Wielomian interpolacyjny')
    plt.scatter(nodes_more, y_nodes_more, color='red', label='Węzły interpolacji')
    plt.legend()
    plt.grid(True)
    plt.title(f'Interpolacja Newtona - {func_name} (więcej węzłów)')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.savefig(f'{func_name}_more.png')
    plt.close()

def run_predefined_functions():
    functions, intervals, nodes = predefined_functions()
    
    for func_name in functions:
        print(f"\nGenerowanie wykresów dla funkcji {func_name}...")
        plot_predefined_function(
            func_name,
            functions[func_name],
            intervals[func_name],
            nodes[func_name]['less'],
            nodes[func_name]['more']
        )
    print("\nWszystkie wykresy zostały zapisane do plików.")

def main():
    print("Wybierz tryb pracy:")
    print("1. Własne funkcje")
    print("2. Predefiniowane funkcje")
    mode = int(input("Podaj wybór (1-2): "))
    
    if mode == 1:
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
    else:
        run_predefined_functions()

if __name__ == "__main__":
    main()
