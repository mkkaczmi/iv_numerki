from typing import Tuple, Callable
from functions import AVAILABLE_FUNCTIONS
from root_finding import bisection_method, secant_method
from plotting import plot_function_and_roots
import numpy as np
import re
from horner import evaluate_polynomial

def create_custom_function(expression: str) -> Callable[[float], float]:
    """
    Tworzy funkcję z wyrażenia tekstowego.
    
    Args:
        expression: Wyrażenie matematyczne jako tekst
        
    Returns:
        Funkcja wyliczająca wartość wyrażenia
    """
    # Sprawdź czy wyrażenie jest wielomianem
    if re.match(r'^[0-9x\s\+\-\*]+$', expression):
        # Wyciągnij współczynniki wielomianu
        terms = expression.replace(' ', '').split('+')
        coefficients = []
        max_degree = 0
        
        # Znajdź maksymalny stopień wielomianu
        for term in terms:
            if 'x' in term:
                if '^' in term:
                    degree = int(term.split('^')[1])
                    max_degree = max(max_degree, degree)
                else:
                    max_degree = max(max_degree, 1)
        
        # Utwórz listę współczynników
        for i in range(max_degree + 1):
            coef = 0
            for term in terms:
                if 'x' in term:
                    if '^' in term:
                        degree = int(term.split('^')[1])
                        if degree == i:
                            coef_str = term.split('x')[0]
                            if coef_str == '':
                                coef = 1
                            elif coef_str == '-':
                                coef = -1
                            else:
                                coef = float(coef_str)
                    elif i == 1:
                        coef_str = term.split('x')[0]
                        if coef_str == '':
                            coef = 1
                        elif coef_str == '-':
                            coef = -1
                        else:
                            coef = float(coef_str)
                elif i == 0:
                    coef = float(term)
            coefficients.append(coef)
        
        # Użyj schematu Hornera
        def polynomial_function(x: float) -> float:
            return evaluate_polynomial(x, coefficients, len(coefficients))
        
        return polynomial_function
    
    # Jeśli nie jest wielomianem, użyj standardowej metody
    expression = expression.lower()
    
    # Zamiana e^(-x) i podobnych wyrażeń na exp(-x)
    expression = re.sub(r'e\^(\([^)]+\))', r'np.exp\1', expression)
    expression = re.sub(r'e\^(-?x)', r'np.exp(\1)', expression)
    expression = re.sub(r'e\^(\d+)', r'np.exp(\1)', expression)
    
    # Zamiana x^n na x**n dla potęgowania
    expression = re.sub(r'x\^(\d+)', r'x**\1', expression)
    expression = re.sub(r'(\d+)\^(\d+)', r'\1**\2', expression)
    
    # Dodanie operatora mnożenia między liczbą a x
    expression = re.sub(r'(\d+)x', r'\1*x', expression)
    
    # Zamiana funkcji matematycznych na odpowiedniki z numpy
    expression = expression.replace('sin', 'np.sin')
    expression = expression.replace('cos', 'np.cos')
    expression = expression.replace('tan', 'np.tan')
    expression = expression.replace('exp', 'np.exp')
    expression = expression.replace('log', 'np.log')
    expression = expression.replace('sqrt', 'np.sqrt')
    
    def custom_function(x: float) -> float:
        try:
            return eval(expression, {"np": np, "x": x})
        except Exception as e:
            raise ValueError(f"Błąd obliczania funkcji: {e}")
    
    return custom_function

def get_user_input() -> Tuple[Callable[[float], float], float, float, float, int, bool]:
    """
    Pobiera dane wejściowe od użytkownika.
    
    Returns:
        Krotka zawierająca (wybraną funkcję, początek przedziału, koniec przedziału, epsilon, max iteracje, warunek epsilon)
    """
    print("\nWybierz metodę wprowadzania:")
    print("1. Użyj predefiniowanej funkcji")
    print("2. Wprowadź własną funkcję")
    
    while True:
        try:
            input_choice = int(input("\nWybierz metodę wprowadzania (1 lub 2): "))
            if input_choice in [1, 2]:
                break
            print("Nieprawidłowy wybór. Wprowadź 1 lub 2.")
        except ValueError:
            print("Proszę wprowadzić prawidłową liczbę.")
    
    if input_choice == 1:
        print("\nDostępne predefiniowane funkcje:")
        for i, name in enumerate(AVAILABLE_FUNCTIONS.keys(), 1):
            print(f"{i}. {name}")
        
        while True:
            try:
                choice = int(input("\nWybierz funkcję (wprowadź numer): "))
                if 1 <= choice <= len(AVAILABLE_FUNCTIONS):
                    break
                print("Nieprawidłowy wybór. Spróbuj ponownie.")
            except ValueError:
                print("Proszę wprowadzić prawidłową liczbę.")
        
        selected_function = list(AVAILABLE_FUNCTIONS.values())[choice - 1]
    else:
        print("\nWprowadź funkcję jako wyrażenie matematyczne.")
        print("Dostępne funkcje: sin, cos, tan, exp, log, sqrt")
        print("Użyj x jako zmiennej. Przykład: x**2 + 2*x - 1")
        print("lub sin(x) + cos(x)")
        
        while True:
            try:
                expression = input("\nWprowadź funkcję: ").strip()
                if not expression:
                    print("Wyrażenie nie może być puste.")
                    continue
                    
                if not re.match(r'^[0-9x\s\+\-\*\/\^\(\)\.\,a-z\s]+$', expression):
                    print("Nieprawidłowe znaki w wyrażeniu. Używaj tylko liczb, x, operatorów i nazw funkcji.")
                    continue
                    
                test_func = create_custom_function(expression)
                test_func(0.0)
                selected_function = test_func
                break
            except Exception as e:
                print(f"Nieprawidłowa funkcja: {e}")
                print("Spróbuj ponownie.")
    
    while True:
        try:
            a = float(input("Wprowadź początek przedziału: "))
            b = float(input("Wprowadź koniec przedziału: "))
            if a >= b:
                print("Początek przedziału musi być mniejszy od końca.")
                continue
            break
        except ValueError:
            print("Proszę wprowadzić prawidłowe liczby.")
    
    while True:
        try:
            epsilon = float(input("Wprowadź tolerancję zbieżności (ε): "))
            if epsilon <= 0:
                print("Tolerancja musi być dodatnia.")
                continue
            break
        except ValueError:
            print("Proszę wprowadzić prawidłową liczbę.")
    
    while True:
        try:
            max_iterations = int(input("Wprowadź maksymalną liczbę iteracji: "))
            if max_iterations <= 0:
                print("Liczba iteracji musi być dodatnia.")
                continue
            break
        except ValueError:
            print("Proszę wprowadzić prawidłową liczbę.")
    
    print("\nWybierz warunek zatrzymania:")
    print("1. |x_i - x_(i-1)| < ε")
    print("2. Maksymalna liczba iteracji")
    
    while True:
        try:
            stop_choice = int(input("\nWybierz warunek zatrzymania (1 lub 2): "))
            if stop_choice in [1, 2]:
                break
            print("Nieprawidłowy wybór. Wprowadź 1 lub 2.")
        except ValueError:
            print("Proszę wprowadzić prawidłową liczbę.")
    
    use_epsilon_condition = (stop_choice == 1)
    
    return selected_function, a, b, epsilon, max_iterations, use_epsilon_condition

def check_root_existence(f: Callable[[float], float], a: float, b: float) -> str:
    """
    Sprawdza czy pierwiastek istnieje w przedziale poprzez sprawdzenie znaków na końcach.
    
    Args:
        f: Funkcja do sprawdzenia
        a: Lewy koniec przedziału
        b: Prawy koniec przedziału
        
    Returns:
        Komunikat opisujący sytuację z pierwiastkami
    """
    try:
        # Jeśli funkcja jest wielomianem (sprawdzamy przez atrybut __name__)
        if hasattr(f, '__name__') and 'polynomial' in f.__name__:
            fa = f(a)  # Używa już schematu Hornera wewnątrz funkcji
            fb = f(b)
        else:
            fa = f(a)
            fb = f(b)
            
        if fa * fb > 0:
            return "Brak gwarancji pierwiastka w tym przedziale (te same znaki na końcach)"
        elif fa * fb < 0:
            return "Co najmniej jeden pierwiastek istnieje w tym przedziale"
        else:  # fa * fb == 0
            if fa == 0:
                return f"Znaleziono pierwiastek w x = {a}"
            else:
                return f"Znaleziono pierwiastek w x = {b}"
                
    except (ValueError, OverflowError) as e:
        return f"Błąd przy sprawdzaniu pierwiastków: {e}"

def main():
    """Główna funkcja programu."""
    print("Porównanie metod znajdowania pierwiastków")
    print("========================================")
    
    f, a, b, epsilon, max_iterations, use_epsilon_condition = get_user_input()
    
    root_message = check_root_existence(f, a, b)
    print(f"\nSprawdzenie istnienia pierwiastka: {root_message}")
    
    if "No root guaranteed" in root_message:
        print("\nOstrzeżenie: Funkcja ma ten sam znak na obu końcach przedziału!")
        print("To oznacza, że:")
        print("1. Nie ma pierwiastka w tym przedziale, lub")
        print("2. Jest parzysta liczba pierwiastków w tym przedziale")
        proceed = input("\nCzy chcesz kontynuować poszukiwanie pierwiastków? (t/n): ")
        if proceed.lower() != 't':
            plot_function_and_roots(f, [], a, b)
            return
    
    print("\nObliczanie pierwiastków...")
    
    try:
        bisection_root, bisection_iterations = bisection_method(
            f, a, b, epsilon, max_iterations, use_epsilon_condition
        )
        print(f"\nMetoda bisekcji:")
        if bisection_root is not None:
            print(f"Pierwiastek: {bisection_root:.6f}")
            print(f"Liczba iteracji: {bisection_iterations}")
            print(f"f(pierwiastek) = {f(bisection_root):.10f}")
        else:
            print("Nie znaleziono pierwiastka w podanym przedziale")
            print(f"Wykonano iteracji: {bisection_iterations}")
    except ValueError as e:
        print(f"\nBłąd metody bisekcji: {e}")
        bisection_root = None
    
    try:
        secant_root, secant_iterations = secant_method(
            f, a, b, epsilon, max_iterations, use_epsilon_condition
        )
        print(f"\nMetoda siecznych:")
        if secant_root is not None:
            print(f"Pierwiastek: {secant_root:.6f}")
            print(f"Liczba iteracji: {secant_iterations}")
            print(f"f(pierwiastek) = {f(secant_root):.10f}")
        else:
            print("Nie znaleziono pierwiastka w podanym przedziale")
            print(f"Wykonano iteracji: {secant_iterations}")
    except Exception as e:
        print(f"\nBłąd metody siecznych: {e}")
        secant_root = None
    
    roots = [root for root in [bisection_root, secant_root] if root is not None]
    if roots:
        plot_function_and_roots(f, roots, a, b)
    else:
        plot_function_and_roots(f, [], a, b)

if __name__ == "__main__":
    main()