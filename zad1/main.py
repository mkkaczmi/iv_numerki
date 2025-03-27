import numpy as np
import matplotlib.pyplot as plt

def bisection_method(f, a, b, epsilon, iterations, use_epsilon_condition):
    try:
        fa = f(a)
        fb = f(b)
    except (ValueError, OverflowError):
        return None, 0
    
    if fa * fb >= 0:
        return None, 0
    
    i = 0
    x_prev = a
    
    while i < iterations:
        c = (a + b) / 2
        try:
            fc = f(c)
        except (ValueError, OverflowError):
            return None, i
        
        if use_epsilon_condition and abs(c - x_prev) < epsilon:
            return c, i + 1
        
        if fc == 0 or abs(fc) < epsilon:
            return c, i + 1
        
        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc
        
        x_prev = c
        i += 1
    
    return c, i

def secant_method(f, a, b, epsilon, iterations, use_epsilon_condition):
    i = 0
    x_prev = a
    x_curr = b
    
    try:
        f_prev = f(x_prev)
        f_curr = f(x_curr)
    except (ValueError, OverflowError):
        return None, 0
    
    while i < iterations:
        try:
            denominator = f_curr - f_prev
            if abs(denominator) < 1e-10:
                return None, i
            
            x_next = x_curr - f_curr * (x_curr - x_prev) / denominator
            f_next = f(x_next)
        except (ValueError, OverflowError):
            return None, i
        
        if use_epsilon_condition and abs(x_next - x_curr) < epsilon:
            return x_next, i + 1
        
        if abs(f_next) < epsilon:
            return x_next, i + 1
        
        x_prev, f_prev = x_curr, f_curr
        x_curr, f_curr = x_next, f_next
        i += 1
    
    return x_curr, i

def plot_function_and_roots(f, roots_dict, a, b, title = "Funkcja i jej pierwiastek"):
    x = np.linspace(a, b, 1000)
    y = []
    
    # Obliczanie wartości y z zabezpieczeniem przed bardzo dużymi wartościami
    y_min, y_max = float('inf'), float('-inf')
    for xi in x:
        try:
            yi = f(xi)
            # Ograniczenie wartości y do rozsądnego zakresu
            if abs(yi) > 10:
                yi = np.sign(yi) * 10
            y.append(yi)
            y_min = min(y_min, yi)
            y_max = max(y_max, yi)
        except (ValueError, OverflowError):
            y.append(np.nan)  # Użyj NaN dla nieokreślonych punktów
    
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, 'b-', label='Funkcja')
    plt.axhline(y=0, color='k', linestyle='--', alpha=0.3)
    
    # Rysowanie pierwiastków z różnymi kolorami i etykietami dla każdej metody
    colors = {'bisekcja': 'red', 'sieczna': 'green'}
    markers = {'bisekcja': 'o', 'sieczna': 's'}
    
    # Rysowanie pierwiastków
    for method, root in roots_dict.items():
        if root is not None:
            try:
                root_y = f(root)
                if abs(root_y) > 10:
                    root_y = np.sign(root_y) * 10
                plt.plot(root, root_y, 
                        color=colors[method], 
                        marker=markers[method], 
                        label=f'Pierwiastek ({method}): {root:.6f}')
            except (ValueError, OverflowError):
                continue
    
    # Ustawienie rozsądnych granic osi y
    y_range = y_max - y_min
    plt.ylim([max(y_min - 0.1 * y_range, -10), min(y_max + 0.1 * y_range, 10)])
    
    plt.title(title)
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.grid(True)
    plt.legend()
    plt.show()

def evaluate_polynomial(x, coefficients):
    result = 0
    for coef in coefficients:
        result = result * x + coef
    return result

def polynomial_function(x, coefficients):
    return evaluate_polynomial(x, coefficients)

def create_polynomial_function(coefficients):
    return lambda x: polynomial_function(x, coefficients)

def apply_trigonometric(x, trig_type, a, b, c, d):
    if trig_type == 1:
        return a * np.sin(b * x + c) + d
    elif trig_type == 2:
        return a * np.cos(b * x + c) + d
    else:
        return a * np.tan(b * x + c) + d

def apply_exponential(x, exp_type, a, b, c, p=None):
    if exp_type == 1:
        return a * np.exp(b * x) + c
    else:
        return a * (p ** (b * x)) + c

def create_function(function_type, polynomial_degree):
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
    
    elif function_type == 'exponential':
        print("\nWybierz podstawę funkcji wykładniczej:")
        print("1. Liczba e (funkcja: a*e^(bx) + c)")
        print("2. Własna podstawa (funkcja: a*p^(bx) + c)")
        exp_choice = int(input("Podaj wybór (1-2): "))
        
        a = float(input("a = "))
        b = float(input("b = "))
        c = float(input("c = "))
        
        if exp_choice == 1:
            return lambda x: apply_exponential(x, exp_choice, a, b, c)
        else:
            p = float(input("Podaj podstawę p = "))
            return lambda x: apply_exponential(x, exp_choice, a, b, c, p)

def get_user_input():
    print("\nPodaj przedział [a, b]:")
    a = float(input("a = "))
    b = float(input("b = "))
    
    print("\nWybierz warunek stopu:")
    print("1. |x_i - x_(i-1)| < ε")
    print("2. Liczba iteracji")
    stop_choice = int(input("Podaj wybór (1-2): "))
    
    use_epsilon_condition = (stop_choice == 1)
    if use_epsilon_condition:
        epsilon = float(input("Podaj wartość ε: "))
        iterations = 1000
    else:
        epsilon = 1e-10
        iterations = int(input("Podaj liczbę iteracji: "))
        
    return a, b, epsilon, iterations, use_epsilon_condition

def get_example_functions():
    functions = [
        lambda x: x**2 - 2*np.exp(2*x),
        lambda x: 3*np.exp(x) - np.cos(x),
        lambda x: np.cos(x) + 2*x - 3,
        lambda x: np.cos(x) + np.exp(-x) - 1
    ]
    return functions

def apply_composite_function(x, functions):
    result = x
    for f in reversed(functions):
        result = f(result)
    return result

def main():
    print("\nWybierz tryb:")
    print("1. Użyj przykładowych funkcji")
    print("2. Wprowadź własną funkcję")
    mode_choice = int(input("Podaj wybór (1-2): "))
    
    if mode_choice == 1:
        print("\nDostępne funkcje przykładowe:")
        print("1. x² - 2e^(2x)")
        print("2. 3e^x - cos(x)")
        print("3. cos(x) + 2x - 3")
        print("4. cos(x) + e^(-x) - 1")
        
        function_choice = int(input("Wybierz funkcję (1-4): ")) - 1
        example_functions = get_example_functions()
        composite_function = example_functions[function_choice]
        
    else:
        n_compositions = int(input("Podaj liczbę składanych funkcji (1 dla pojedynczej funkcji): "))
        
        functions = []
        for i in range(n_compositions):
            print(f"\nFunkcja {i+1}:")
            print("Wybierz typ funkcji:")
            print("1. Wielomian")
            print("2. Trygonometryczna (sin/cos/tan)")
            print("3. Wykładnicza (e^x lub a^x)")
            
            choice = int(input("Podaj wybór (1-3): "))
            function_type = {1: 'polynomial', 2: 'trigonometric', 3: 'exponential'}[choice]
            
            polynomial_degree = None
            if function_type == 'polynomial':
                polynomial_degree = int(input("Podaj stopień wielomianu: "))
            
            f = create_function(function_type, polynomial_degree)
            functions.append(f)
        
        composite_function = lambda x: apply_composite_function(x, functions)

    a, b, epsilon, iterations, use_epsilon_condition = get_user_input()
    
    print("\nStosowanie metody bisekcji...")
    root_bisection, iters_bisection = bisection_method(
        composite_function, a, b, epsilon, iterations, use_epsilon_condition
    )
    
    print("\nStosowanie metody siecznych...")
    root_secant, iters_secant = secant_method(
        composite_function, a, b, epsilon, iterations, use_epsilon_condition
    )
    
    print("\nWyniki:")
    if root_bisection is not None:
        print(f"Metoda bisekcji: Pierwiastek = {root_bisection}, Liczba iteracji = {iters_bisection}")
    else:
        print("Metoda bisekcji: Nie udało się znaleźć pierwiastka")
        
    if root_secant is not None:
        print(f"Metoda siecznych: Pierwiastek = {root_secant}, Liczba iteracji = {iters_secant}")
    else:
        print("Metoda siecznych: Nie udało się znaleźć pierwiastka")
    
    roots_dict = {
        'bisekcja': root_bisection,
        'sieczna': root_secant
    }
    if any(root is not None for root in roots_dict.values()):
        plot_function_and_roots(composite_function, roots_dict, a, b, 
                              "Funkcja i jej pierwiastki (Metody bisekcji i siecznych)")

if __name__ == "__main__":
    main()